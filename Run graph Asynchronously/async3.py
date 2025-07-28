# conditional branching with async execution in Lang-graph

# So we're going to start from node A. Then we're going to have three conditional branches to node B, C and D. And depending on our state we are either going to execute node B and C or going to execute node C and D in parallel. And after we do that we're going to execute node E.

from dotenv import load_dotenv

load_dotenv()


import operator
from typing import Annotated, Any, Sequence

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    aggregate: Annotated[list, operator.add]
    which: str #  this is going to hold which nodes we want to execute in this execution branching step. So it's either going to hold node B and C or it's either going to hold node C and D. And this value we're going to get from the user when we invoke the graph. And it's going to be a string. So it's going to be C and D concatenated or B and C concatenated together.


class ReturnNodeValue:
    def __init__(self, node_secret: str):
        self._value = node_secret

    def __call__(self, state: State) -> Any:
        import time

        time.sleep(1)
        print(f"Adding {self._value} to {state['aggregate']}")
        return {"aggregate": [self._value]}


builder = StateGraph(State)
builder.add_node("a", ReturnNodeValue("I'm A"))
builder.add_edge(START, "a")
builder.add_node("b", ReturnNodeValue("I'm B"))
builder.add_node("c", ReturnNodeValue("I'm C"))
builder.add_node("d", ReturnNodeValue("I'm D"))
builder.add_node("e", ReturnNodeValue("I'm E"))


def route_bc_or_cd(state: State) -> Sequence[str]:
    if state["which"] == "cd":
        return ["c", "d"]
    return ["b", "c"]


intermediates = ["b", "c", "d"] #  contain all the possible nodes to go from node A.
builder.add_conditional_edges(
    "a",
    route_bc_or_cd,
    intermediates, # path map is going to help us in our graph visualization. So it can either be a dictionary that is going to map strings into node names, or it's going to be a list of node names. Langgraph going to use those values here in order to draw our graph. Now if we didn't put this intermediate list over here of the nodes that we want to go, then in the graph, that lang_graph would draw for us, you can see that there are a lot of extra edges here that we don't really need, because langgraph simply assumes that we want to go from node A to every node. So that's the reason that we need to put this in order to make our code and and graph drawing more readable. So we explicitly say it when we create the edge. So it's very important.
)
for node in intermediates:
    builder.add_edge(node, "e")
builder.add_edge("e", END)
graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="async3.png")

if __name__ == "__main__":
    print("Helo Async Graph")
    graph.invoke(
        # {"aggregate": [], "which": ""}, {"configurable": {"thread_id": "foo"}}
        {"aggregate": [], "which": "cd"}, {"configurable": {"thread_id": "foo"}}
    )
