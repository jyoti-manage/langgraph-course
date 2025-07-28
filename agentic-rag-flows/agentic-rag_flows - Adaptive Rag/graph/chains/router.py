from typing import Literal # a way to specify that a variable can only take one of predefined set of values like only ["vectorstore" or "websearch"]

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

# a question router chain, which will take the question and decide whether we're going to route it to the web search or to the retrieve node.

class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["vectorstore", "websearch"] = Field(
        ...,
        # ellipsis means that this field will be required once we instantiate an object of this class.
        description="Given a user question choose to route it to web search or a vectorstore.",
    )


llm = ChatGroq(model_name="llama-3.3-70b-versatile")

structured_llm_router = llm.with_structured_output(RouteQuery)

system = """You are an expert at routing a user question to a vectorstore or web search.
The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.
Use the vectorstore for questions on these topics. For all else, use web-search."""
route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)

question_router = route_prompt | structured_llm_router