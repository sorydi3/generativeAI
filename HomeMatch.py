
import lancedb
from GenerateListings import GenerateListings



def create_lancedb_database():
    uri = "data/lancedblistings"
    db = lancedb.connect(uri)
    return db

def get_table(db,table_name):
    table = db.open_table(table_name)
    return table

def embeddings():
    embeddings = get_registry().get("openai").create()
    return embeddings

def generate_listings(prompt:str = "3 random listing in json list." ) -> None:
    db = create_lancedb_database()
    generate_listings = GenerateListings()
    listings = generate_listings.generate_listings(promp,db)


def search_listings(query:str) -> None:
    db = lancedb.connect("data/lancedblistings")
    table = get_table(db,"listings")
    # Search the listings table for the query
    results = table.search(query).limit(1)
    print(results.to_pandas().head())

    
    

if __name__ == "__main__":
    # Create a new instance of the GenerateListings class
    
    # Generate a list of listings based on the user query
    #generate_listings()

    db = lancedb.connect("data/lancedblistings")
    table = db.open_table("listings")
    print(table.to_pandas().head())     # Print the first 5 rows of the table   
    # Search the listings table for the query
    search_listings("great restaurants")
    