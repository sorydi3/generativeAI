from Listing import Listing
import openai
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
import os
import json
from langchain.vectorstores import LanceDB
from langchain_core.runnables import RunnablePassthrough
from lancedb.pydantic import pydantic_to_schema

MODEL_NAME = "gpt-3.5-turbo-1106"
class GenerateListings:

    def __init__(self):
        self._parser = PydanticOutputParser(pydantic_object=Listing)
        self._llm = ChatOpenAI(api_key=os.environ.get("OPENAI_API_KEY"), model=MODEL_NAME);
        self._listing=[]
        

    def _get_template(self) -> PromptTemplate:
        return PromptTemplate(
            template="""\n {format_instructions} \n {query}""",
            input_variables=["query"],
            partial_variables={"format_instructions": self._parser.get_format_instructions()}   
        )
    
    def generate_listings(self, query,db):
        # Generate the response
        chain = LLMChain(llm=self._llm, prompt=self._get_template())
        response = chain.invoke({"query":query})
        try:
            print("RESPONSE: ", response)
            print("RESPONSE TYPE: ", type(response))
            print("RESPONSE TEXT: ", response['text'])
        except Exception as e:
            print(e)
            print("Error in parsing the response response['text'] ")
            return None
        json_format = json.loads(response['text'])
        try:
            print (json_format)
            
            pydantic_model = []
            for i in json_format:
               pydantic_model.append(
                   dict(Listing (
                        description = i['description'],
                        price = i['price'],
                        bedrooms= i['bedrooms'],
                        bathrooms=i['bathrooms'],
                        house_size=i['house_size'],
                        neighborhood_description=i['neighborhood_description'],
                        neighborhood=i['neighborhood'],
                   ))
               )
            table = db.create_table("listingss", mode="overwrite", exist_ok=True,schema=pydantic_to_schema(Listing))
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