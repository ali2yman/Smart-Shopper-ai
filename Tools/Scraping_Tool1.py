import os
from typing import List
from pydantic import BaseModel, Field
from scrapegraph_py import Client
from crewai.tools import tool


# ==========================
# Environment Setup
# ==========================

SCRAPEGRAPH_API_KEY = os.getenv("ScrapeGraphAI_KEY")
scrapegraph = Client(api_key=SCRAPEGRAPH_API_KEY)


# ==========================
# Data Models
# ==========================

class ProductSpec(BaseModel):
    specification_name: str
    specification_value: str


class SingleExtractedProduct(BaseModel):
    page_url: str = Field(..., title="The original URL of the product page")
    product_title: str = Field(..., title="The title of the product")
    product_image_url: str = Field(..., title="The URL of the product image")
    product_url: str = Field(..., title="The URL of the product")
    product_current_price: float = Field(..., title="The current price of the product")
    product_original_price: float = Field(default=None, title="The original price of the product before discount. Set to None if no discount")
    product_discount_percentage: float = Field(default=None, title="The discount percentage of the product. Set to None if no discount")
    product_specs: List[ProductSpec] = Field(..., title="The specifications of the product. Focus on the most important specs to compare.", min_items=1, max_items=5)
    agent_recommendation_rank: int = Field(..., title="The rank of the product in the final procurement report (1 to 5, higher is better)")
    agent_recommendation_notes: List[str] = Field(..., title="Notes explaining why this product is recommended or not, compared to others.")


class AllExtractedProducts(BaseModel):
    products: List[SingleExtractedProduct]


# ==========================
# Web Scraping Tool
# ==========================

@tool
def web_scraping_tool(page_url: str):
    """
    AI tool to scrape a product page and extract structured data.

    Args:
        page_url (str): URL of the product page to scrape.

    Returns:
        dict: Contains the page URL and extracted product details.
    
    Example:
        web_scraping_tool(
            page_url="https://www.noon.com/egypt-en/15-bar-fully-automatic-espresso-machine-1-8-l-1500"
        )
    """
    schema_prompt = f"Extract ```json\n{SingleExtractedProduct.schema_json()}\n``` From the web page"

    details = scrapegraph.smartscraper(
        website_url=page_url,
        user_prompt=schema_prompt
    )

    return {
        "page_url": page_url,
        "details": details
    }
