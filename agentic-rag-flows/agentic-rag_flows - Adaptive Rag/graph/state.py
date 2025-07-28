# define our graph state, which is going to be passed around during our nodes execution.

from typing import List, TypedDict


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        web_search: whether to add search
        documents: list of documents
    """

    question: str           # user question to refer it whether to      determine if the documents retrieved are relevant to the question, or even to what to search online.
    generation: str         #   generated answer
    web_search: bool        #  flag that will tell us whether we need to search online for extra results or not
    documents: List[str]    #  the retrieved documents or the documents that we get back from the search result