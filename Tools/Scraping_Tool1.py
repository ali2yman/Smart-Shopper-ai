import os
import json
from typing import List, Union
from pydantic import BaseModel, Field, ValidationError
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
    page_url: str = Field(..., title="The original url of the product page")
    product_title: str = Field(..., title="The title of the product")
    product_image_url: str = Field(..., title="The url of the product image")
    product_url: str = Field(..., title="The url of the product")
    product_current_price: float = Field(..., title="The current price of the product")
    product_original_price: float = Field(title="The original price of the product before discount. Set to None if no discount", default=None)
    product_discount_percentage: float = Field(title="The discount percentage of the product. Set to None if no discount", default=None)

    product_specs: List[ProductSpec] = Field(..., title="The specifications of the product. Focus on the most important specs to compare.", min_items=1, max_items=5)

    agent_recommendation_rank: int = Field(..., title="The rank of the product to be considered in the final procurement report. (out of 5, Higher is Better) in the recommendation list ordering from the best to the worst")
    agent_recommendation_notes: List[str]  = Field(..., title="A set of notes why would you recommend or not recommend this product to the company, compared to other products.")


class AllExtractedProducts(BaseModel):
    products: List[SingleExtractedProduct]


# ==========================
# Web Scraping Tool
# ==========================

@tool
def web_scraping_tool(page_url: str):
    """
    An AI Tool to help an agent to scrape a web page

    Example:
    web_scraping_tool(
        page_url="https://www.noon.com/egypt-en/15-bar-fully-automatic-espresso-machine-1-8-l-1500"
    )
    """
    details = scrapegraph.smartscraper(
        website_url=page_url,
        user_prompt="Extract ```json\n" + SingleExtractedProduct.model_json_schema() + "```\n From the web page"
    )

    return {
        "page_url": page_url,
        "details": details
    }
