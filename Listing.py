from pydantic import BaseModel, Field



"""
Neighborhood: Green Oaks
Price: 800,000
Bedrooms: 3
Bathrooms: 2
House Size: 2,000 sqft

Description: Welcome to this eco-friendly oasis nestled in the heart of Green Oaks. This charming 3-bedroom, 2-bathroom home boasts energy-efficient features such as solar panels and a well-insulated structure. Natural light floods the living spaces, highlighting the beautiful hardwood floors and eco-conscious finishes. The open-concept kitchen and dining area lead to a spacious backyard with a vegetable garden, perfect for the eco-conscious family. Embrace sustainable living without compromising on style in this Green Oaks gem.

Neighborhood Description: Green Oaks is a close-knit, environmentally-conscious community with access to organic grocery stores, community gardens, and bike paths. Take a stroll through the nearby Green Oaks Park or grab a cup of coffee at the cozy Green Bean Cafe. With easy access to public transportation and bike lanes, commuting is a breeze.
"""

#Define a class called Listing
class Listing(BaseModel):
    #Define the fields of the Listing class
    neighborhood: str = Field(description="The name of the neighborhood") 
    price: int = Field(description="The price of the home(without commas and dollar sign)")
    bedrooms: int = Field(description="The number of bedrooms in the home")
    bathrooms: int = Field(description="The number of bathrooms in the home")
    house_size: int = Field(description="The size of the home in square feet")
    description: str = Field(description="A description of the home")
    neighborhood_description: str = Field(description="A description of the neighborhood")
    #Define a validator method called validate_price
    

