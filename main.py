from crewai import Agent,Task,Crew,Process,LLM
import agentops
import os
import requests
from dotenv import load_dotenv


load_dotenv()

LLM_API_KEY = os.getenv("OPENROUTER_API_KEY")
AGENT_OPS_KEY = os.getenv("AGENTOPS_API_KEY")





