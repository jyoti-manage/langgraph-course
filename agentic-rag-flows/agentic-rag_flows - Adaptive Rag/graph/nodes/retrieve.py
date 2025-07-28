from typing import Any, Dict

from graph.state import GraphState
from ingestion import retriever

# So this node is going to get the state. It's going to extract the question that the user asked. And it's going to retrieve the relevant documents for that state. So that is going to be using our vector store semantic search capabilities. And after this node we should update the state documents to hold the relevant documents from our vector store.

# And by now the retriever is supposed to reference our local vector store with all the embeddings stored already. (run ingestion file first)

def retrieve(state: GraphState) -> Dict[str, Any]:
    print("---RETRIEVE---")
    question = state["question"]

    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}
    # update the state, question updation was not needed though