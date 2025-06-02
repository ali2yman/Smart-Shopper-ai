from crewai import LLM
import agentops
import os
from dotenv import load_dotenv


load_dotenv()

LLM_API_KEY = os.getenv("OPENROUTER_API_KEY")
AGENT_OPS_KEY = os.getenv("AGENTOPS_API_KEY")



agentops.init(
    api_key=AGENT_OPS_KEY,
    skip_auto_end_session=True,
    default_tags=["crewai"],
)

basic_llm = LLM(
    api_key=LLM_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    model = "openrouter.ai/deepseek/deepseek-r1-0528",
    temperature=0
)

