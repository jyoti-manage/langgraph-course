from langchain import hub
from langchain_core.output_parsers import StrOutputParser
# output parser that converts LLM response (which is a string only) or ChatModel reponse (it's a message with '.content' feild which is parsed into string) into string
from langchain_groq import ChatGroq

llm = ChatGroq(model_name="llama-3.3-70b-versatile")
prompt = hub.pull("rlm/rag-prompt")

generation_chain = prompt | llm | StrOutputParser()
