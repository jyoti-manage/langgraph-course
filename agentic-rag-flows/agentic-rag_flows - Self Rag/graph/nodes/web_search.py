from typing import Any, Dict

from langchain.schema import Document
from langchain_tavily import TavilySearch
# langchain tool that runs the Tavelly search engine on the queries we provide

from graph.state import GraphState
from dotenv import load_dotenv

load_dotenv()
web_search_tool = TavilySearch(max_results=3)


def web_search(state: GraphState) -> Dict[str, Any]:
    print("---WEB SEARCH---")
    question = state["question"]
    documents = state["documents"]
    # Now notice because we execute the web search node only after we grade the documents, So it's after we filter them out irrevelent documents. So we're not supposed to have any non-relevant documents.

    tavily_results = web_search_tool.invoke({"query": question})
    joined_tavily_result = "\n\n".join(
    [tavily_result["content"] for tavily_result in tavily_results["results"]]
    )  # to get one huge string
    
    web_results = Document(page_content=joined_tavily_result) 
    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]
    return {"documents": documents, "question": question}


if __name__ == "__main__":
    web_search(state={"question": "agent memory", "documents": None})