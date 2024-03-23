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

MODEL_NAME = "gpt-3.5-turbo-1106"
class GenerateListings:

    def __init__(self):
        self._parser = PydanticOutputParser(pydantic_object=Listing)
        print("API KEY: ", os.environ.get("OPENAI_API_KEY"))
        self._llm = ChatOpenAI(api_key=os.environ.get("OPENAI_API_KEY"), model=MODEL_NAME);
        self._listing=[]
        

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
    def generate_listings(self, query,db):

        # Generate the response
        chain = LLMChain(llm=self._llm, prompt=self._get_template())
        response = chain.invoke({"query":query})
        table = db.create_table("listings", mode="overwrite", exist_ok=True,schema=Listing)
        try:
            print("RESPONSE: ", response)
            print("RESPONSE TYPE: ", type(response))
            print("RESPONSE TEXT: ", response['text'])
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
               print("TYPE OF THE EMBEDDING IS: ",type(embeddings.generate_embeddings(i['description'])[0]))
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
            print(type(pydantic_model[0]))
            table.add(data = pydantic_model)

        except Exception as e:

            print(e)
            print("Error in parsing the response json_format")
            return None
    
        return table

    def generate_listings_runnable(self, query):
        # Generate the response
        #chain = LLMChain(llm=self._llm, prompt=self._get_template())
        chain = ({"query": RunnablePassthrough()}
                    | self._get_template()
                    | self._llm
                    )
        response = chain.invoke("query")
        print("TYPE OF RESPONSE: ", type(response))
        return response.to_json()