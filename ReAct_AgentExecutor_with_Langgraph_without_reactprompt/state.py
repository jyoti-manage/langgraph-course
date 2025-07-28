# node receive state as input and state is updated when the node executes

# MessageGraph (which we use before) meant that our state was simply a list of messages, and every time a node in our then graph executes, that simply add the result into the state.
# input-> list of messages
# return one or more message as output
# But here we use our custom state



# upon every node execution we change the inner state of the graph. How do we change the state? So there are two ways. The first one is to use a set operation on a specific attribute of the state. And this is for example, to override some existing value. Or the other option is to add to the existing attribute.



import operator
from typing import Annotated, TypedDict, Union

from langchain_core.agents import AgentAction, AgentFinish

# we're creating a custom state, then LangChain recommend us to use a schema with a typeddictionary.
class AgentState(TypedDict):
    input: str   # user's input
    agent_outcome: Union[AgentAction, AgentFinish, None]    # current output of agent
    # it's a union of AgentAction, AgentFinish, None (none because when we run the first node, then we don't have anything in the state.)
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]
    # syntax
    # attribute_name: Annotated[type_of_attribute, method describing how to update the attribute]
    # first argument of Annotated is list which consists of a tuple, where the first element is the agent action, and second is the output of that action, which is going to be a string.
    #  intermediate_steps will be plugged in the placeholder, in the ReAct prompt as the agent scratch pad.

    # we can tell LangGraph in our annotation to add to the existing attribute and not to override it. So that's where the operator.add comes from. And LangGraph is going to enforce that annotation.
    
    # if we do not mention how to update, then if any new value comes it will replace old value and if no new value, then old value remains intact
    # for example, the agent_outcome is not having the operator.add. So that attribute is going to be replaced and overwritten with the new state, if the return value from the node after its execution has the specific attribute of agent_outcome.

    # In order to implement the agent executor, we basically need to keep track on three main attributes. The one is going to be the input that the user wanted. The second is going to be the current result of the agent of what to do. So it's either can be an action or to finish. And in our flow, this information helps our agent decide whether it needs to continue, and to perform some action to execute a tool, or to finish and to return the result to the user. And the third is the history ie. the intermediate steps