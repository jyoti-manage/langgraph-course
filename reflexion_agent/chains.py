import datetime

from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers.openai_tools import (
    JsonOutputToolsParser,
    PydanticToolsParser,
)
# openai function calling is nothing but a way for OpenAI models to interact with external tools
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq

from schemas import AnswerQuestion, ReviseAnswer

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
    )


parser = JsonOutputToolsParser(return_id=True)
#  its simply going to return us the function call invocation we got back from the LLM and transform it into a dictionary.
parser_pydantic = PydanticToolsParser(tools=[AnswerQuestion])
#  It is going to take the response from the LLM. It's going to search for the function calling invocation and it's going to parse it and transform it into an answer question object. So it's going to take the answer from the LLM. And it's going to create an answer question object that we can easily work with.

actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are expert researcher.
Current time: {time}

1. {first_instruction}
2. Reflect and critique your answer. Be severe to maximize improvement.
3. Recommend search queries to research information and improve your answer.""",
        ),
        MessagesPlaceholder(variable_name="messages"),  # history
        ("system", "Answer the user's question above using the required format."),
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
)  # time is computed only when we invoke our prompt template, while invoking the agent


first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer."
)

# And I remind you, the input for this agent is going to be the topic that we want to write about, and the agent is going to write us the initial response. Now in the answer of the agent we need the content, the first draft of the article. We want to also have a critique. So some criticism on the newly created article and some search terms that will help enhance the article.
first_responder = first_responder_prompt_template | llm.bind_tools(
    tools=[AnswerQuestion], tool_choice="AnswerQuestion"
)
# bind_tools method is specific to LangChain's integration with OpenAI's function calling feature. When you call bind_tools(...), you're telling LangChain to prepare the LLM to use a specific tool (function) when generating its response.
# This tools argument is where you pass in function specifications. Each item (like AnswerQuestion) represents a tool (function) that you define in code, typically as a Pydantic model describing the function’s name, input schema, and purpose. tools=[AnswerQuestion] is how you define OpenAI functions that the LLM can "call" using the function calling mechanism.
# The LLM uses the tools inside tools=[] to decide which tool to use (if tool_choice="auto") or is forced to use a specific one (if tool_choice="AnswerQuestion"). So, It returns the tool invocation (i.e., function name + arguments ie. {
#   "tool_calls": [
#     {
#       "name": "AnswerQuestion",
#       "arguments": {
#         "question": "What is the capital of Japan?"
#       }
#     }
#   ]
# }), for that tool (to use that tool) and that can then be parsed using an output parser like PydanticOutputParser or JsonOutputParser."


revise_instructions = """Revise your previous answer using the new information.
    - You should use the previous critique to add important information to your answer.
        - You MUST include numerical citations in your revised answer to ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
            - [1] https://example.com
            - [2] https://example.com
    - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 250 words.
"""

# this agent is going to revise the response projected from the critique that was already written, is going to take the search results from Tavily, and it's going to add this into our response and it's going to citate all the resources that we used from the internet.
revisor = actor_prompt_template.partial(
    first_instruction=revise_instructions
) | llm.bind_tools(tools=[ReviseAnswer], tool_choice="ReviseAnswer")


if __name__ == "__main__":
    human_message = HumanMessage(
        content="Write about AI-Powered SOC / autonomous soc  problem domain,"
        " list startups that do that and raised capital."
    )
    chain = (
        first_responder_prompt_template
        | llm.bind_tools(tools=[AnswerQuestion], tool_choice="AnswerQuestion")
        | parser_pydantic
    )

    res = chain.invoke(input={"messages": [human_message]})
    # To run a LangGraph workflow asynchronously with async nodes, define your nodes as async def functions and execute the graph using the await app.ainvoke() method (or app.astream() for streaming) within an asynchronous context. Ensure your nodes are defined using async def. Inside these nodes, use the await keyword for any asynchronous operations, such as calling an LLM's ainvoke(), tool.ainvoke() method or using asyncio.gather() for concurrent tasks. Compile the graph and invoke it using await app.ainvoke() within an asyncio event loop:
    # async def run_graph():
    # # Invoke the graph asynchronously
    # final_state = await compiled_app.ainvoke(
    #     {"messages": ["initial user message"]},
    #     # Optional: configure for streaming events
    #     # config={"stream_mode": ["messages-tuple"]}
    # )
    # print(final_state["messages"][-1].content)

# Run the main async function
if __name__ == "__main__":
    asyncio.run(run_graph())
    print(res)

    # And we got an error saying that we didn't provide the search queries field to answer question object. So this means that when the LLM produced the response it didn't actually give us a search queries in the answer (and this error is very normal while using pydantic). And this can be resolved if we do some prompt engineering like saying you must provide the search queries at all costs or something like that. Or even better, maybe to try and split up this query into a different prompt that will run independently.
