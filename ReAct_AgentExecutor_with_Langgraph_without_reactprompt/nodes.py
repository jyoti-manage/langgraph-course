from dotenv import load_dotenv
from langgraph.graph import MessagesState # dict with message key which is a list of object of HumanMessage and AIMessage
from langgraph.prebuilt import ToolNode # toolnode to execute tools. So it's going to check the last message between the agent and human. And if that last message is an AImessage that has a valid tool call, it's going to go and execute that tool call, assuming that tools is initiated with the tool node object.

from react import llm, tools

load_dotenv()

SYSYEM_MESSAGE="""
You are a helpful assistant that can use tools to answer questions.
"""

# node
def run_agent_reasoning(state: MessagesState) -> MessagesState:
    """
    Run the agent reasoning node.
    """
    response = llm.invoke([{"role": "system", "content": SYSYEM_MESSAGE}, *state["messages"]])
    return {"messages": [response]}

tool_node = ToolNode(tools)