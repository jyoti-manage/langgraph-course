from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

llm = ChatGroq(model_name="llama-3.3-70b-versatile")

# pydantic model
class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )



structured_llm_grader = llm.with_structured_output(GradeDocuments)
# A wrapper around the LLM that returns outputs formatted to match the given schema.
# Internally, It's going to use OpenAI function calling.
# EX: formatted_tool = convert_to_openai_tool(schema)
            # tool_name = formatted_tool["function"]["name"]
            # llm = self.bind_tools(
            #     [schema],
            #     tool_choice=tool_name,
            #     ls_structured_output_format={
            #         "kwargs": {"method": "function_calling"},
            #         "schema": formatted_tool,
            #     },
            # )
# And for every LLM call we make we are going to return a Pydantic object. So, the LLM is going to return in the schema that we want.


system = """You are a grader assessing relevance of a retrieved document to a user question. \n 
    If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant. \n
    Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""
grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
)


# this chain is going to receive as an input the original question and one retrieve document. And it's going to determine whether the document is relevant to the questions or not.
retrieval_grader = grade_prompt | structured_llm_grader
# returns a GradeDocuments object