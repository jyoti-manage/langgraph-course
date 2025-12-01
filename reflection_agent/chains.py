from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# message placeholder class: will allow us to place a placeholder for future messages we receive.
# message placeholder class: Prompt template that assumes variable is already list of messages. A placeholder which can be used to pass in a list of messages.
from langchain_groq import ChatGroq

# So we're going to set up the generation chain, which will be responsible for generating and revising our tweets until they get better and better.
# And we will implement the chain of reflection. So this chain will take our tweet and give us feedback. It will criticize it. And it's going to give us suggestions on how to improve it again and again. And at each iteration of our cycle in our graph, we will introduce this criticism into our generation chain and it will revise the tweet.



# ChatPromptTemplate store the message like = [("system", "You are a helpful AI bot. Your name is {name}."),
#             ("human", "Hello, how are you doing?"),
#             ("ai", "I'm doing well, thanks!")]
# which becomes internally:
# ChatPromptValue(
#    messages=[
#        SystemMessage(content='You are a helpful AI bot. Your name is Bob.'),
#        HumanMessage(content='Hello, how are you doing?'),
#        AIMessage(content="I'm doing well, thanks!"),
#        HumanMessage(content='What is your name?')
#    ]
# )
reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a viral twitter influencer grading a tweet. Generate critique and recommendations for the user's tweet."
            "Always provide detailed recommendations, including requests for length, virality, style, etc.",
        ),
        MessagesPlaceholder(variable_name="messages"), # messages will be like [("human", "..."), (AI, "response")], since this is how ChatPromptTemplate works and takes messages.
        # historical messages that agent will use to critique and provide recommendations over and over again
    ]
)

generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a twitter techie influencer assistant tasked with writing excellent twitter posts."
            " Generate the best twitter post possible for the user's request."
            " If the user provides critique, respond with a revised version of your previous attempts.",
        ),
        MessagesPlaceholder(variable_name="messages"),
        # placeholder here for all the thoughts and revisions we've had previously
    ]
)


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
    )
generate_chain = generation_prompt | llm  # return AIMessage object
reflect_chain = reflection_prompt | llm
