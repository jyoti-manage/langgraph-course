from typing import List, Sequence

from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph
# The MessageGraph class is a special type of graph. The State of a MessageGraph is ONLY an array of messages. This class is rarely used except for chatbots, as most applications require the State to be more complex than an array of messages.
# At each node, the returned messages is appended into the array of messages

from chains import generate_chain, reflect_chain


# keys of nodes
REFLECT = "reflect"
GENERATE = "generate"

# recieve a state as input, which is basically a list of messages,  which is going to hold all the critiques and all the previous generations.
# Once we get our response back from the LM. So it will take the return value and it would append it to the state, which is just a list of messages.
def generation_node(state: Sequence[BaseMessage]):
    return generate_chain.invoke({"messages": state}) # place at the 'messages' in the prompt


def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    res = reflect_chain.invoke({"messages": messages})
    return [HumanMessage(content=res.content)]
    # The response we get back from the LLM, which usually would be with the role of the AI, then we now change it to be a human message. Because we want to trick the LLM to think that a human is sending this message. So that way we're going to have a conversation with the LLM back and forth, back and forth, critique, generate, critique, generate.


builder = MessageGraph()
builder.add_node(GENERATE, generation_node) # with the key "GENERATE"
builder.add_node(REFLECT, reflection_node)
builder.set_entry_point(GENERATE)

# So let's say we executed the generate node and we revised the tweet once. Now we want to implement the logic that would either say that the tweet is fine and we can finish our graph execution, or that we need a reflection step. So for that we'll be implementing a function which is called should continue, which will receive as the statean input, which is all of our messages. And it's going to decide which node should we go to. Either the end node if we finished or the reflection node. And the return value of this function is a string, and is the key of the node that we want to go to. The terminology in Landgragh for this type of object is called a conditional edge,
def should_continue(state: List[BaseMessage]):
    if len(state) > 6:
        return END
    return REFLECT


builder.add_conditional_edges(GENERATE, should_continue) 
builder.add_edge(REFLECT, GENERATE)

graph = builder.compile() # build graph
# It provides a few basic checks on the structure of your graph (no orphaned nodes, etc). It is also where you can specify runtime args like checkpointers and breakpoints.
print(graph.get_graph().draw_mermaid())
graph.get_graph().print_ascii()

if __name__ == "__main__":
    print("Hello LangGraph")
    inputs = HumanMessage(content="""Make this tweet better:"
                                    @LangChainAI
            — newly Tool Calling feature is seriously underrated.

            After a long wait, it's  here- making the implementation of agents across different models with function calling - super easy.

            Made a video covering their newest blog post

                                  """)
    response = graph.invoke(inputs) # return the state


# Trace in langsmith: The output at last is the final tweet. Final prompt to the LLM has all history and  all interaction of the agent with LLM. 
# So we can see we first started with a system message that we gave in the prompt. And then we started the graph iteration. And the first thing is to generate a revision for this tweet with the generate node that we did. We didn't finish our iterations, so we went into the reflection node and we can see the response we got back from the LLM, which is artificially tagged here as human is giving us feedback about this tweet. So after we finish this node then we need to go back to the generate node. We generate another tweet according to this feedback and so on and so on until we go and until we have the final output which is this one.
# you can see on the left side langchain even have traceability and observability for langgraph objects. So we have this should continue. We have the reflection nodes. And we have all of our linked graph objects built in into our trace.
# check each node's output and input while analysing (my pov)