from Agents.keywords_Search_Agent0 import create_keywords_search_agent
from Agents.Search_engine_Agent1 import Search_engine_agent
from Tasks.Create_Keywords_search_Task import create_keywords_search_task 
from Tasks.Search_engine_task1 import search_engine_task  
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


# Create tasks
keywords_search_task = create_keywords_search_task(
    product_name="macbook m2",
    websites_list=["www.amazon.eg", "www.jumia.com.eg"],
    country_name="Egypt",
    no_keywords=5,
    language="english",
    search_queries_recommendation_agent=keywords_search_agent
)
Search_engine_Task = search_engine_task(0.6, Search_engine_Agent)


# Define the crew
rankyx_crew = Crew(
    agents=[keywords_search_agent,Search_engine_Agent],
    tasks=[keywords_search_task,Search_engine_Task],
    process=Process.sequential,
    knowledge_sources=[company_context]
)

# Execute the crew
crew_results = rankyx_crew.kickoff()
