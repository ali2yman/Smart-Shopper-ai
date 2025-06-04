from Agents.keywords_Search_Agent0 import create_keywords_search_agent
from Agents.Search_engine_Agent1 import Search_engine_agent
from Agents.Scraping_Agent2 import Scraping_agent   
from Tasks.Create_Keywords_search_Task import create_keywords_search_task 
from Tasks.Search_engine_task1 import search_engine_task  
from Tasks.Scraping_task2 import Scraping_task
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource  
from crewai import Crew, Process, LLM
from tavily import TavilyClient
import agentops
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv



# Load API keys from .env file
load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEP_SEEK_API_KEY")
AGENT_OPS_KEY = os.getenv("AGENTOPS_API_KEY")

# Initialize AgentOps
agentops.init(
    api_key=AGENT_OPS_KEY,
    skip_auto_end_session=True,
    default_tags=['crewai']
)

# Use LLM class from CrewAI, not openai.OpenAI
DeepSeek_llm = LLM(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    model="openai/deepseek/deepseek-chat:free"
)


# ------------------------------------------------------------------------------------------------

about_company = "Rankyx is a company that provides AI solutions to help websites refine their search and recommendation systems."   

company_context = StringKnowledgeSource(
    content=about_company
)

# Create agents
keywords_search_agent = create_keywords_search_agent(DeepSeek_llm)
Search_engine_Agent = Search_engine_agent(DeepSeek_llm)
scraping_agent = Scraping_agent(DeepSeek_llm)
# reporter_agent = Report_maker_Agent(DeepSeek_llm)


# Create tasks
keywords_search_task = create_keywords_search_task(
    product_name="iphone 12",
    websites_list=["www.amazon.eg"],
    country_name="Egypt",
    no_keywords=10,
    language="english",
    search_queries_recommendation_agent=keywords_search_agent
)
Search_engine_Task = search_engine_task(0.5, Search_engine_Agent)
Scraping_taskk = Scraping_task(top_recommendations_no=10, scraping_agent=scraping_agent)
# final_Reporter_taskk = final_Reporter_task(reporter_agent)


# Define the crew
rankyx_crew = Crew(
    agents=[keywords_search_agent,Search_engine_Agent,scraping_agent],
    tasks=[keywords_search_task,Search_engine_Task,Scraping_taskk],
    process=Process.sequential,
    knowledge_sources=[company_context]
)

# Execute the crew
crew_results = rankyx_crew.kickoff()
