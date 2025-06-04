from crewai import Task
import os
from Tools import Scraping_Tool1


def Scraping_task(top_recommendations_no: int, scraping_agent) -> Task:

    # Define output directory and path
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Data'))
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "step_3_scraping_results.json")

    # Task description
    descriptionnn="\n".join([
        "The task is to extract product details from any ecommerce store page url.",
        "The task has to collect results from multiple pages urls.",
        "Collect the best {top_recommendations_no} products from the search results.",
    ])


    return Task(
        description=descriptionnn,
        expected_output="A JSON object containing detailed product information.",
        output_json=Scraping_Tool1.AllExtractedProducts,
        output_file=output_path,
        agent=scraping_agent
    )
