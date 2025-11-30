from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

import sqlite3


from dotenv import load_dotenv
load_dotenv()

class State(TypedDict):
    state: str
    user_feedback: str


def processing(state: State) -> State:
    print("processing ", state)
    return {
        "state": "processed"
    }

def take_user_input(state: State) -> None:
    print("provided your feedback (approved/rejected): ")

def approved(state: State) -> str:
    print("checking approval ", state)
    if state.get("user_feedback") == "approved":
        return "step_3"
    return "step_1"


def resultant(state: State) -> State:
    print("resultant ", state)
    return {
        "state": "final"
    }


builder = StateGraph(State)
builder.add_node("step_1", processing)
builder.add_node("step_2", take_user_input)
builder.add_node("step_3", resultant)


builder.add_edge(START, "step_1")
builder.add_edge("step_1", "step_2")
builder.add_conditional_edges("step_2", approved)
builder.add_edge("step_3", END)

conn = sqlite3.connect("checkpoints.sqlite",check_same_thread=False)
memory = SqliteSaver(conn)

graph = builder.compile(checkpointer=memory, interrupt_before=["step_2"])

thread = {"configurable": {"thread_id": "1"}} 

# 1st run and then interrupt
def run_graph(state:str): 
    for event in graph.stream({"state": state}, thread, stream_mode="values"):
            print("event", event)
      
    return graph.get_state(thread).values['state']    

# after getting user input, continue the graph
def interactive_run(user_input: str): # user_input - approved/rejected
    graph.update_state(thread, {"user_feedback": user_input}) 

    for event in graph.stream(None, thread, stream_mode="values"):
        print("event", event)

    return graph.get_state(thread).values['state']    # if approved, it will return final, else again return processsed     

  


        
