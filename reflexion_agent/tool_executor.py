from dotenv import load_dotenv

load_dotenv()

from langchain_core.tools import StructuredTool # convert a Python function into a tool that can be used by Llms. So it's going to take that function and provide to the LLM a structured schema for that function, which will help the LLM understand how to use this tool.
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode 
# ToolNode is a node in Landgraaf that we can invoke. And it's going to look in the state for the messages key. It's going to check the last message, and it's then going to see if there's any tool calls that were decided by the LLM. And if there are, it's going to execute those tools for us.

from schemas import AnswerQuestion, ReviseAnswer

tavily_tool = TavilySearch(max_results=5) # return a langchain tool with the function of the search engine

# So we want to take the original Tavily tool and its functionality, and we want to create from it two different tools. It's going to be two different tools with the same functionality of the tavily search. But they're going to have different names because they serve different purposes in the application workflow. So we're going to have an answer question tool, which is going to be used during the initial research phase when the agent is first answering the question. And then we want to have this revised answer tool which is used during the revision phase when the agent is improving its answer based on the reflection. So both tools are going to run the tavily search. And that's why we need those objects - the answer question object and the revised answer object. Because we want to get their names in order to label those tools.



# receive as an input the search queries which is a list of strings.
def run_queries(search_queries: list[str], **kwargs):
    """Run the generated queries."""
    return tavily_tool.batch([{"query": query} for query in search_queries])

#  This node is going to take as an input the AI message, which would be the last message,  which is going to have the information of the wanted search queries or Tool_call. And it's going to run tavily to get us real time results and real time information from the web.
execute_tools = ToolNode(
    [
        StructuredTool.from_function(run_queries, name=AnswerQuestion.__name__),
        # StructuredTool receives a function 'run_queries' and convert it into a tool with the schema and description for LLM
        StructuredTool.from_function(run_queries, name=ReviseAnswer.__name__),
    ]
)