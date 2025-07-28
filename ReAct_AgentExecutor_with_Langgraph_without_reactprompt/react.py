import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch # it has in-built description which is propagated to LLM 

load_dotenv()


# langchain tool
@tool
def triple(num: float) -> float:
    """
    :param num: a number to triple
    :return: the number tripled ->  multiplied by 3
    """
    return 3 * float(num)  


tools = [TavilySearch(max_results=1), triple]

llm = ChatGroq(groq_api_key=os.environ["GROQ_API_KEY"],
        model_name="llama-3.3-70b-versatile").bind_tools(
            tools
        ) # bind_tools -> function calling

