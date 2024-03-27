from Listing import Listing
import openai
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
import os
import json
from langchain_community.vectorstores import LanceDB
from langchain_core.runnables import RunnablePassthrough
from lancedb.pydantic import pydantic_to_schema
from lancedb.embeddings import get_registry
import lancedb

from MessageHistory import CustomChatMessageHistory

MODEL_NAME = "gpt-3.5-turbo-1106"
class GenerateListings:

    def __init__(self):
        self._parser = PydanticOutputParser(pydantic_object=Listing)
        self._llm = ChatOpenAI(api_key=os.environ.get("OPENAI_API_KEY"), model=MODEL_NAME);
        self._listing=[]
    
    def _get_table(self,db,table_name):
        table = db.open_table(table_name)
        return table

    def _get_template(self) -> PromptTemplate:
        return PromptTemplate(
            template="""\n {format_instructions} \n {query}""",
            input_variables=["query"],
            partial_variables={"format_instructions": self._parser.get_format_instructions()}   
        )
  
    def _search_relevant_vectordb(self,query:str) -> None:
        db = lancedb.connect("data/lancedblistings")
        table = self._get_table(db,"listings")
        # Search the listings table for the query
        results = table.search(query).limit(2)
        """
        print("QUERY: ", query)
        print("RESULTS: ", results.to_pandas())
        """
        return results.to_pandas()[['neighborhood','price','bedrooms','bathrooms','house_size','description','neighborhood_description']].to_dict('records')
    


    """
        save the listings to a file in json format called listings.json
        param: listings: list of listings in json format
        return: None
    """
    def _save_listings_to_file(self, listings):
        with open("listings.json", "w") as file:
            json.dump(listings, file, indent=4)


    """
        generate the listings based on pydantic model LISTING and user query
        param: db: LanceDB object
        param: query: user query
        return: table: LanceDB table object
    """
    def generate_listings(self, query,db):

        # Generate the response
        chain = LLMChain(llm=self._llm, prompt=self._get_template())
        response = chain.invoke({"query":query})
        table = db.create_table("listings", mode="overwrite", exist_ok=True,schema=Listing)
        try:

            print("--------------LISTINGS------------------: ")
            print("RESPONSE TEXT: ", response['text'])
            print("--------------LISTINGS------------------: ")
            json_format = json.loads(response['text'])
            self._save_listings_to_file(json_format)
        except Exception as e:
            print(e)
            print("Error in parsing the response response['text'] ")
            return None

        try:
            print (json_format)
            
            pydantic_model = []
            for i in json_format:
               embeddings = get_registry().get("openai").create()
               pydantic_model.append(
                   {
                          "neighborhood": i['neighborhood'],
                          "price": i['price'],
                          "bedrooms": i['bedrooms'],
                          "bathrooms": i['bathrooms'],
                          "house_size": i['house_size'],
                          "description": i['description'],
                          "neighborhood_description": i['neighborhood_description']
                   }
               )
            #rint(type(pydantic_model[0]))
            table.add(data = pydantic_model)

        except Exception as e:

            print(e)
            print("Error in parsing the response json_format")
            return None
    
        return table

    def _get_template_(self,query) -> PromptTemplate:
        history = CustomChatMessageHistory()



        return PromptTemplate(
            template=""" 
                Your goal is to become a trusted advisor for potential buyers, uncovering their deepest desires and lifestyle needs. By analyzing their preferences, you'll curate personalized property listings with compelling descriptions that resonate on both emotional and practical levels.

                Here's the key:

                - Emphasize psychological benefits: While maintaining factual accuracy, highlight aspects of the property that align with the buyer's aspirations and personality. For example, for a buyer seeking a sense of community, describe a close-knit neighborhood with friendly porches and block parties.
                - Address subconscious desires: Use your knowledge of sycology to identify potential unspoken needs. For instance, a buyer mentioning a love for gardening might secretly crave a peaceful sanctuary – emphasize the serene backyard perfect for relaxation and plant nurturing.
                - Emotional connection is key: Craft language that evokes positive emotions and paints a vivid picture of the buyer's life thriving in the property.
                - Always maintain transparency: Never misrepresent the property. You want to build trust and ensure a happy long-term fit.
                
                The Bottom Line:

                Become the buyer's confidant and guide them towards their dream home, using your unique blend of real estate expertise and psychological understanding.

                Remember: It's not just about selling a house, it's about creating a perfect fit for their happiness and well-being. \n

            CHAT HISTORY: \n
            {chat_history} \n

            LISTINGS TO BE TAILORED: \n
            {context} \n 

            

            AUGMENTS THE AVAILABLE LISTINGS TO MAKE IT MORE APPEALING TO THE BUYER AND GIVE ME JUST FINAL RESPONSE WITH THE AUGMANTED LISTINGS WITH ALL PROPERTIES. \n


            
            """,
            input_variables=["query"],
            partial_variables={"format_instructions": self._parser.get_format_instructions(), "context": self._search_relevant_vectordb(history.get_answers()), "chat_history":history.get_messages()}   
        )

    def tailor_listing_to_user_query(self, query):
        # Generate the response
        history = CustomChatMessageHistory()

        template = self._get_template_(query)
        

        chain = LLMChain(llm=self._llm, prompt=self._get_template_(query))

        context = self._search_relevant_vectordb(history.get_questions())

        response = chain.invoke({
            "query":query,
        })
        
        # PRINT THE CONTEXT
        # print ("CONTEXT: \n", context)    

        print("-------------------------------------\n\n")
        print("TAILORED RESPONSE: \n\n", response['text'])        
        print("-------------------------------------\n\n")
        return response