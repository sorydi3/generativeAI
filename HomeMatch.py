
import lancedb
from GenerateListings import GenerateListings
from  MessageHistory import CustomChatMessageHistory

def create_lancedb_database():
    uri = "data/lancedblistings"
    db = lancedb.connect(uri)
    return db

def generate_listings(prompt:str = "5 random listing in json list. \n Note: you are a computer programe and do NOT add ANY extra data OR METADADA  and you are unable to express yourself. JUST THE OUTPUT" ) -> None:
    db = create_lancedb_database()
    print("")
    generate_listings = GenerateListings()
    listings = generate_listings.generate_listings(prompt,db)


if __name__ == "__main__":
    # Create a new instance of the GenerateListings class
    
    # Generate a list of listings based on the user query
    #generate_listings()  # uncomment this line to generate 10 new listings

    db = lancedb.connect("data/lancedblistings")
    table = db.open_table("listings")


    # Create a new instance of the GenerateListings class
    generate_listings = GenerateListings()

    # Generate a list of listings based on the user query
    generate_listings.tailor_listing_to_user_query("")
