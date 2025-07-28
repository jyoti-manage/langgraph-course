from typing import List

from pydantic import BaseModel, Field

# we want to ensure that the output we get from the LLM is in a structured format. So we want the format to be with a response field that is having the original essay. We want the critique field, which is having the critique for that essay, and we want a search field, which will be a list of values that we should search for.
# And for that we're going to leverage function calling (tools=[] inside first_responder chain) and specifically function calling that would make sure that the output format of the LLM is going to be in a object we create.
class Reflection(BaseModel):
    missing: str = Field(description="Critique of what is missing.")
    superfluous: str = Field(description="Critique of what is superfluous")


class AnswerQuestion(BaseModel):
    """Answer the question."""

    answer: str = Field(description="~250 word detailed answer to the question.")
    reflection: Reflection = Field(description="Your reflection on the initial answer.")
    search_queries: List[str] = Field(
        description="1-3 search queries for researching improvements to address the critique of your current answer."
    )

# it will have all of AnswerQuestion's fields. It will also have the references field which is going to be a list of strings. And those strings are going to be citations of URLs mostly that we'll get from the search engine.
class ReviseAnswer(AnswerQuestion):
    """Revise your original answer to your question."""

    references: List[str] = Field(
        description="Citations motivating your updated answer."
    )