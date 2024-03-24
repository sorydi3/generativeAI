
import lancedb
from GenerateListings import GenerateListings
from  MessageHistory import CustomChatMessageHistory

def create_lancedb_database():
    uri = "data/lancedblistings"
    db = lancedb.connect(uri)
    return db

def generate_listings(prompt:str = "15 random listing in json list. \n Note: you are a computer programe and do NOT add ANY extra data OR METADADA  and you are unable to express yourself. JUST THE OUTPUT" ) -> None:
    db = create_lancedb_database()
    generate_listings = GenerateListings()
    listings = generate_listings.generate_listings(prompt,db)


if __name__ == "__main__":
    # Create a new instance of the GenerateListings class
    
    # Generate a list of listings based on the user query
    
    #generate_listings()

    db = lancedb.connect("data/lancedblistings")
    table = db.open_table("listings")
    #print(table.to_pandas()['neighborhood'])     # Print the first 5 rows of the table   
    # Search the listings table for the query

    promt = """
       return the updated listings based on the user query,without adding any extra information or metadata in text formating.
       Note: I do not want any extra information or metadata in the listings.
        Example of the output OF THE LISTINGS AFTER UPDATING BASED ON THE USER QUERY:
            Neighborhood: Green Oaks
            Price: 800,000
            Bedrooms: 3
            Bathrooms: 2
            House Size: 2,000 sqft
            Description: Welcome to this eco-friendly oasis nestled 
            Neighborhood Description: Green Oaks is a close-knit, 
       
    """


    generate_listings = GenerateListings()
    generate_listings.tailor_listing_to_user_query("update the listins based on the user query,without adding any extra information or metadata.")




    history = CustomChatMessageHistory()


    


    
    