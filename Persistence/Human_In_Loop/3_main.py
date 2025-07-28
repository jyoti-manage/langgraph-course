from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

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


# "checkpoints.sqlite": url to run a local DB in my file system
conn = sqlite3.connect("checkpoints.sqlite",check_same_thread=False)
# And we also want to enable the checksum thread equals false. So we'll be able to make DB operations even though we're going to run in different threads. Because in our main file we're going to run our graph. We're then going to stop the execution and then we're going to rerun it again. So it's going to be on different threads. And if we don't mark this flag as false we'll get an error because we tried to edit the DB from different threads.

memory = SqliteSaver(conn) # create checkpointer from connection string

graph = builder.compile(checkpointer=memory,  interrupt_before=["human_feedback"]) 

graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

if __name__ == "__main__":
    thread = {"configurable": {"thread_id": "1"}}  
    initial_input = {"input": "hello world"}

    for event in graph.stream(initial_input, thread, stream_mode="values"):
        print(event) 
 
    print(graph.get_state(thread).next) 

    user_input = input("Tell me how you want to update the state: ") # in the interrupt

    graph.update_state(thread, {"user_feedback": user_input}, as_node="human_feedback") 

    print("--State after update--")
    print(graph.get_state(thread)) 
    print(graph.get_state(thread).next)

    # continue and stream our graph with the same thread ID
    for event in graph.stream(None, thread, stream_mode="values"):
        print(event)

    # after the execution, check the created 'checkpoints.sqlite' with any database-tool, it will have a table 'checkpoints'. In that table, the states and everything is saved, Very similar to what we saw with the memory saver, But this one is persisted into disk. 
    # while debug using langsmith, it has option for go to threads also to see the execution.

    # As the persist memory is stored, we can now stop and resume this execution and to continue from the same place.
    # lets change the thread=777, when we run it, the state of '777' thread is stored into DB. Then an interrupt comes,  (we are going to stop the entire program there manually by commenting all below line from user_input) and when we continue for the same thread (from user_input commenting all above lines), it starts from the same state as it was persist in the DB corresponding to that thread-id in that table. (two times we run the program with diff. lines of code, but in 2nd time, it can access the state from previous execution corresponding to that same thread) This is the use-case of persistance.
    


    