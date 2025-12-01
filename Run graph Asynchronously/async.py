from dotenv import load_dotenv

load_dotenv()


import operator
from typing import Annotated, Any

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    aggregate: Annotated[list, operator.add]    # a list of strings that we want to append to after each node execution


class ReturnNodeValue:
    def __init__(self, node_secret: str):
        self._value = node_secret

    # when we create an instance of this class, this instance is callable because we override the call method. so, we can call the instance like a function. ie. `a()` and this make this __call__ method to be executed.
    # when we add a node to the graph, it receives a state as an argument and updates the state
    def __call__(self, state: State) -> Any:
        import time

        time.sleep(1)
        print(f"Adding {self._value} to {state['aggregate']}")
        return {"aggregate": [self._value]}


builder = StateGraph(State)
builder.add_node("a", ReturnNodeValue("I'm A"))
builder.add_edge(START, "a")
builder.add_node("c", ReturnNodeValue("I'm C"))
builder.add_node("b", ReturnNodeValue("I'm B"))
builder.add_node("d", ReturnNodeValue("I'm D"))
builder.add_edge("a", "c")
builder.add_edge("a", "b")
builder.add_edge("b", "d")
builder.add_edge("c", "d")
# And this is what is going to create the parallel execution of the nodes b and c because we have one node 'a' which is fanning out into two nodes 'b' and 'c'.
builder.add_edge("d", END)
graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="async.png")


if __name__ == "__main__":
    print("Helo Async Graph")
    graph.invoke({"aggregate": []}, {"configurable": {"thread_id": "foo"}})

# output check in langgraph: the times of executions

# output: state in __call__ method before adding, for B and C are same (having only A in the state), that means they are executed concurrently. 



# when __call__ is executed:
# So when they add a node using builder.add_node, it's just registering the __call__ function to be run later, not executing it. The call actually happens once the graph is invoked, particularly after compiling or triggering the graph.
# after we call compile the graph and invoke it, then because of add_edge, __call__ is executed because normally we have chains or functions as node which are called when we execute the graph, but this time, it is a class object as a node. and as usually it calls object on execution of the graph, because of which __call__() get executed(my observation)

