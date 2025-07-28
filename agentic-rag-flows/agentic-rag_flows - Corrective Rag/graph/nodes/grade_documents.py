from typing import Any, Dict

from graph.chains.retrieval_grader import retrieval_grader
from graph.state import GraphState

# So when we enter this node we have in our state the retrieved documents.So now we want to iterate over those documents and to determine whether they are indeed relevant to our question or not. So for that we're going to be writing a retrieval_grader chain, which is going to use structured output from our LLM and turning it into a Pydantic object that will have the information whether this document is relevant or not.
# And if the document is not relevant, we want to filter it out and keep only the documents which are relevant to the question. And if not all documents are relevant. So this means that at least one document is not relevant to our query. Then we want to mark the web search flag to be true.So we'll go in later search for this term.
def grade_documents(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run web search

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Filtered out irrelevant documents and updated web_search state
    """

    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]

    filtered_docs = []
    web_search = False
    for d in documents:
        score = retrieval_grader.invoke(
            {"question": question, "document": d.page_content}
        )
        grade = score.binary_score
        if grade.lower() == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            web_search = True
            continue
    return {"documents": filtered_docs, "question": question, "web_search": web_search}