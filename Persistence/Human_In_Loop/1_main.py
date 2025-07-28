# MemorySaver + Interrupts = Human In The Loop

# We're going to start from the starting node. We're going to execute step one, which is going to print us. Then we're going to have an interrupt before we get the human feedback. We take the human feedback and then we update our state with the human feedback. And then we continue the execution to go to step three and then to end.

from dotenv import load_dotenv
load_dotenv()
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
# MemorySaver is a checkpoint which stores the state after each node's execution. However, it stores it in-memory and this storage type is ephemeral, so it will be gone upon each run of our graph's execution.

class State(TypedDict):
    input: str
    user_feedback: str


def step_1(state: State) -> None:
    print("---Step 1---")


def human_feedback(state: State) -> None:
    print("---human_feedback---")


def step_3(state: State) -> None:
    print("---Step 3--")


builder = StateGraph(State)
builder.add_node("step_1", step_1)
builder.add_node("human_feedback", human_feedback)
builder.add_node("step_3", step_3)
builder.add_edge(START, "step_1")
builder.add_edge("step_1", "human_feedback")
builder.add_edge("human_feedback", "step_3")
builder.add_edge("step_3", END)


memory = MemorySaver()

graph = builder.compile(checkpointer=memory,  interrupt_before=["human_feedback"])
# once we compile the graph, we're going to give it the memory saver. And it's going to be responsible to persist in-memory our state upon each graph's execution.
# And what this will do is when we execute the graph before we execute the human feedback node, we'll stop the graph execution. And because we checkpointed the state of the graph and at what point we stopped, then we can go and get an input from the user. So some get some human feedback. And then we can go and actually resume our graph execution from exactly where we stopped. So this is all thanks to the check-pointer which is helping us to remember where we stopped and what was the state.

graph.get_graph().draw_mermaid_png(output_file_path="graph.png")


# --------------------------------- #
# If we create a graph and when we create it, we also pass the check pointer. Then what lang-graph is going to do under the hood is going to persist our state after each node execution. So basically after each nodes execute we're going to have a new state, which lang-graph is going to persist in our database that we can access and retrieve later if we want. So, once we do that it basically gives us the option to stop the graph execution because we have already persisted the state, to do something like get a user input and then continue exactly where we left because we have it in our database so we can retrieve it. So this is basically what the check pointer is doing when we plug it in into our graph.
