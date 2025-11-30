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

if __name__ == "__main__":
    thread = {"configurable": {"thread_id": "1"}}  
  
    for event in graph.stream({"state": "initial"}, thread, stream_mode="values"):
            print("event", event)

    while not graph.get_state(thread).next == ():

        user_input = input("Tell me how you want to update the state: ")

        graph.update_state(thread, {"user_feedback": user_input}) 
        # graph.update_state(thread, {"user_feedback": user_input}, as_node="step_2") 
        # why not as_node="step_2"?
        # ans: update_state(..., as_node="step_2") resumes execution starting from step_2 node instantly — it does NOT wait for graph.stream(), because you specify as_node="step_2". So the conditional edges (the approved() function) get evaluated instantly. Then when you call graph.stream(None, thread), that work has already happened, so you don’t see the conditional decision happening again.
        # now question is, why conditional edges function after step_2 is also executed instantly due to as_node="step_2"?
        # ans: Conditional edges functions are part of node execution. In LangGraph, execution of a node consists of 2 phases: Node Execution Phases - 1. Run the node function, 2. Immediately evaluate conditional edges for that node. So, You cannot execute a node without also executing its conditional edges function. If a conditional edge is connected to step_2, LangGraph runs the associated condition function(s) to evaluate the new state and decide which path to take next. Therefore, step_2 node execution includes its conditional edges function (approved()) also 

        print(graph.get_state(thread).next)
        print("Started after: ")
        for event in graph.stream(None, thread, stream_mode="values"):
            print("event", event)



    print("END Final state:", graph.get_state(thread).values)    
    print(graph.get_state(thread).values['state'])   

        
