import time

import streamlit as st
from langchain.agents import AgentExecutor
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain.tools import format_tool_to_openai_function
from streamlit_chat import message

from components.about import about
from utils.tools import (
    TimetableAvailabilityTool,
    TimetableConflictCheckerTool,
    TimetableFilterTool,
)

tools = [
    TimetableConflictCheckerTool(),
    TimetableAvailabilityTool(),
    TimetableFilterTool(),
]
functions = [format_tool_to_openai_function(tool) for tool in tools]

prompt = OpenAIFunctionsAgent.create_prompt(
    system_message=SystemMessage(
        content="""
        You are a helpful assistant who is expert with time management and can handle multiple PERSON and/or ROOM schedule so that no schedule will overlap each other.
        You DO NOT answer anything unrelated to timetable and politely informs that you are programmed to only answer timetable related questions.
        ============
        While helping USER managing Timetable, keep in mind that:
        1 - USER cannot schedule to occupy a ROOM if the ROOM is still unavailable based on the Timetable.
        2 - USER cannot schedule a meeting with a PERSON if the PERSON is still unavailable based on the Timetable.
        3 - Similarly, each PERSON listed in the Timetable cannot schedule to meet with other PERSON if one of them is unavailable.
        4 - Outside of the schedule information listed in the Timetable, all PERSON and all ROOM listed in the Timetable is available.
        ============
        Before giving your answer, make sure to check if there is a conflict between user request and existing timetable configuration.
        """
    )
)

with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key",
        key="chatbot_api_key",
        help="You can get your API key from https://platform.openai.com/account/api-keys.",
    )
    st.markdown(
        "## How to use\n"
        "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"
        "2. Create, upload, or use existing template for your Timetable📆\n"
        "3. Ask a question about the timetable💬\n"
    )
    st.markdown(
        "[View the source code](https://github.com/im-perativa/timetableGPT/blob/main/Chatbot.py)"
        "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/im-perativa/timetableGPT?quickstart=1)"
    )
    about()

st.title("📆Timetable GPT")

if "timetable" not in st.session_state:
    st.error("Please input your Timetable first")
elif st.session_state["timetable"].shape[0] == 0:
    st.error("Please input your Timetable first")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

with st.form("chat_input", clear_on_submit=True):
    a, b = st.columns([4, 1])
    user_input = a.text_input(
        label="Your message:",
        placeholder="What would you like to know about the Timetable?",
        label_visibility="collapsed",
    )
    b.form_submit_button("Send", use_container_width=True)

for msg in st.session_state["messages"]:
    message(msg["content"], is_user=msg["role"] == "user")

if user_input and not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")


def generate_response(input_text):
    llm = ChatOpenAI(
        client="TimetableGPT",
        temperature=0,
        model="gpt-3.5-turbo-16k-0613",
        openai_api_key=openai_api_key,
    )
    open_ai_agent = OpenAIFunctionsAgent(tools=tools, llm=llm, prompt=prompt)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    open_ai_agent_executor = AgentExecutor.from_agent_and_tools(
        agent=open_ai_agent, tools=tools, verbose=True, memory=memory
    )

    return open_ai_agent_executor.run(input_text)


if user_input and openai_api_key:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    message(user_input, is_user=True, key=str(time.time_ns()))
    response = generate_response(user_input)
    st.session_state["messages"].append({"role": "assistant", "content": response})
    message(response, key=str(time.time_ns()))
