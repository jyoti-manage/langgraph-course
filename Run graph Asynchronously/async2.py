from dotenv import load_dotenv

load_dotenv()

# We're first going to execute node A. We're then going to concurrently execute node B and C. After node B finish executing, We'll go and execute node B2. And ONLY AFTER completing execution of B2, since we've already executed node C then we're going to execute node D.

import operator
from typing import Annotated, Any

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    aggregate: Annotated[list, operator.add]    


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
builder.add_node("b2", ReturnNodeValue("I'm B2"))
builder.add_node("c", ReturnNodeValue("I'm C"))
builder.add_node("d", ReturnNodeValue("I'm D"))
builder.add_edge("a", "b")
builder.add_edge("a", "c")
builder.add_edge("b", "b2")
builder.add_edge(["b2", "c"], "d")  # b2->d and c->d
builder.add_edge("d", END) 
graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="async2.png")


if __name__ == "__main__":
    print("Helo Async Graph")
    graph.invoke({"aggregate": []}, {"configurable": {"thread_id": "foo"}})
