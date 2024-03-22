import openai
import lancedb
import os
from GenerateListings import GenerateListings
from Listing import Listing
from lancedb.pydantic import pydantic_to_schema



def create_lancedb_database():
    uri = "data/lancedblistings"
    db = lancedb.connect(uri)
    return db

if __name__ == "__main__":
    # Create a new instance of the GenerateListings class
    generate_listings = GenerateListings()
    # Generate a list of listings based on the user query

    db = create_lancedb_database()

    # Print the generated listings


    query = "3 random listing in json list."
    listings = generate_listings.generate_listings(query,db)
    db = lancedb.connect("data/lancedblistings")
    table = db.open_table("listingss")
    print(table.to_pandas().head())
    