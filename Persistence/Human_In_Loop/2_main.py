from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv
load_dotenv()

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

graph = builder.compile(checkpointer=memory,  interrupt_before=["human_feedback"]) # interrupt stops execution of graph before "human_feedback" node

graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

if __name__ == "__main__":
    thread = {"configurable": {"thread_id": "1"}}  # a thread ID is as a session ID or a conversation ID, and this is what is going to help us differentiate between different runs of our graph.

    initial_input = {"input": "hello world"}

    for event in graph.stream(initial_input, thread, stream_mode="values"):
        print(event) # return the state
    # graph stops after first_node because of interrupt (and now, check the memory while debugging (variables->memory->storage->))

    print(graph.get_state(thread).next) # give us the next node that should run in our graph state according to the given thread.

    user_input = input("Tell me how you want to update the state: ") # in the interrupt

    graph.update_state(thread, {"user_feedback": user_input}, as_node="human_feedback") # So we'll update the current thread so its thread ID 1 and in the state -> user_feedback with user's choice. And we'll want to use the keyword of as_node equals human feedback. And this will actually update as if the node ran and updated the value in the execution. so, because you specify as_node="human_feedback", the graph begins partially executing from human_feedback node immediately.The graph.update_state() method in langgraph manually updates the current state of a running graph (thread) with new values, simulating as if these updates originated from a specific node (human_feedback), without actually executing the corresponding node function. (and the graph will start from after the human_feedback node when again graph.stream() is called)

    # pass
    # breakpoint and debug (graph.get_state(thread))

    print("--State after update--")
    print(graph.get_state(thread)) # output: StateSnapshot(values={'input': 'hello world', 'user_feedback': 'jyoty'}, next=('step_3',)

    print(graph.get_state(thread).next)

    # continue and stream our graph with the same thread ID
    for event in graph.stream(None, thread, stream_mode="values"):
        print(event)
    #  this should now finish the execution of our graph after the human feedback and the step 3


    
