from crewai import Task
import os
from Tools import Scraping_Tool1


def Scraping_task(top_recommendations_no: float, scraping_agent) -> Task:
    """
    Creates a CrewAI Task to scrape product details from multiple e-commerce pages.

    Parameters:
    ----------
    top_recommendations_no : float
        The number of top recommended products to scrape from the search results.
    
    scraping_agent : Agent
        The CrewAI agent responsible for executing the scraping task.

    Returns:
    -------
    Task
        Configured CrewAI Task object for scraping e-commerce data.
    """

    # Define the output directory and file path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, '../Data')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "step_3_scraping_results.json")

    # Task description
    task_description = "\n".join([
        "Scrape detailed product information from a set of e-commerce store page URLs.",
        "Ensure the scraper navigates through multiple result pages if applicable.",
        f"Identify and extract data for the top {int(top_recommendations_no)} most relevant or best-rated products based on the search results."
    ])


    return Task(
        description=task_description,
        expected_output="A JSON object containing detailed product information.",
        output_json=Scraping_Tool1.AllExtractedProducts,
        output_file=output_path,
        agent=scraping_agent
    )
