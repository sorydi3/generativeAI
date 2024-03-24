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
        #print("API KEY: ", os.environ.get("OPENAI_API_KEY"))
        self._llm = ChatOpenAI(api_key=os.environ.get("OPENAI_API_KEY"), model=MODEL_NAME);
        self._listing=[]
    
    def get_table(self,db,table_name):
        table = db.open_table(table_name)
        return table

    def _get_template(self) -> PromptTemplate:
        return PromptTemplate(
            template="""\n {format_instructions} \n {query}""",
            input_variables=["query"],
            partial_variables={"format_instructions": self._parser.get_format_instructions()}   
        )
    """
    Generate the listings based on the model schema
    and save the listings in the database
    """

    def search_relevant_vectordb(self,query:str) -> None:
        db = lancedb.connect("data/lancedblistings")
        table = self.get_table(db,"listings")
        # Search the listings table for the query
        results = table.search(query).limit(3)
        #print(results.to_pandas()[['neighborhood','price','bedrooms','bathrooms','house_size','description','neighborhood_description']].to_dict('records'))
        return results.to_pandas()[['neighborhood','price','bedrooms','bathrooms','house_size','description','neighborhood_description']].to_dict('records')

    def generate_listings(self, query,db):

        # Generate the response
        chain = LLMChain(llm=self._llm, prompt=self._get_template())
        response = chain.invoke({"query":query})
        table = db.create_table("listings", mode="overwrite", exist_ok=True,schema=Listing)
        try:
            #print("RESPONSE: ", response)
            #print("RESPONSE TYPE: ", type(response))
            print("--------------LISTINGS------------------: ")
            print("RESPONSE TEXT: ", response['text'])
            print("--------------LISTINGS------------------: ")
            json_format = json.loads(response['text'])
        except Exception as e:
            print(e)
            print("Error in parsing the response response['text'] ")
            return None

        try:
            print (json_format)
            
            pydantic_model = []
            for i in json_format:
               embeddings = get_registry().get("openai").create()
               #print("TYPE OF THE EMBEDDING IS: ",type(embeddings.generate_embeddings(i['description'])[0]))
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
            p#rint(type(pydantic_model[0]))
            table.add(data = pydantic_model)

        except Exception as e:

            print(e)
            print("Error in parsing the response json_format")
            return None
    
        return table

    def _get_template_(self,query) -> PromptTemplate:
        return PromptTemplate(
            template=""" 
                As a real estate agent, your goal is to provide personalized property listings tailored to the preferences
                of potential buyers. You want to augment the property descriptions to resonate with the buyer's specific
                preferences while maintaining factual integrity and avoiding misrepresentation.\n

            CHAT HISTORY: \n
            {chat_history} \n

            LISTINGS TO BE TAILORED: \n
            {context} \n 
            
            USER QUERY: \n
            
            {query}\n
            
            NOTE: Please THE FINALE LISTING SHOULD BE list them in a bulleted format for easy reading.. FORMAT MUST  NOT BE IN JSON FORMAT. \n 

            """,
            input_variables=["query,context,chat_history"],
            partial_variables={"format_instructions": " "}   
        )

    
    def tailor_listing_to_user_query(self, query):
        # Generate the response
        history = CustomChatMessageHistory()

        template = self._get_template_(query)
        

        chain = LLMChain(llm=self._llm, prompt=self._get_template_(query))

        context = self.search_relevant_vectordb(history.get_questions())

        response = chain.invoke({
            "query":query,
            "chat_history":history.get_messages(), 
            "context":context
            })
        #print("-------------------------------------")
        #print ("ORIGINAL LISTING: \n\n\n", context)
        print("-------------------------------------")
        print("RESPONSE TAILORED: \n\n\n", response['text'])        
        print("-------------------------------------")
        return response