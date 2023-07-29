import os

import langchain
import streamlit as st
from langchain.agents import AgentType, initialize_agent
from langchain.cache import InMemoryCache
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain.tools import format_tool_to_openai_function

from components.about import about
from components.timetable import timetable
from utils.fewshots import example_1, example_2, example_3
from utils.tools import (
    TimetableAvailabilityTool,
    TimetableDeleteTool,
    TimetableGetTool,
    TimetablePostTool,
)

os.environ["LANGCHAIN_TRACING_V2"] = st.secrets["LANGCHAIN_TRACING_V2"]
os.environ["LANGCHAIN_ENDPOINT"] = st.secrets["LANGCHAIN_ENDPOINT"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]

langchain.debug = True

langchain.llm_cache = InMemoryCache()

tools = [
    TimetableAvailabilityTool(),
    TimetableGetTool(),
    TimetablePostTool(),
    TimetableDeleteTool(),
]
functions = [format_tool_to_openai_function(tool) for tool in tools]

agent_kwargs = {
    "system_message": SystemMessage(
        content="""You are an helpful AI assistant who is expert with time management and can handle multiple PERSON and/or ROOM schedule so that no schedule will overlap each other.
You DO NOT answer anything unrelated to timetable and politely informs that you are programmed to only answer timetable related questions.
If you do not know the answer to a question, you truthfully says you do not know.
============
While helping USER managing Timetable, keep in mind that:
1 - USER cannot request to occupy a ROOM if there is an overlap between occupied time range and requested time range.
2 - USER cannot request to meet with a PERSON if there is an overlap between occupied time range and requested time range.
3 - Similarly, each PERSON listed in the Timetable cannot request to meet with other PERSON if one of them is unavailable.
============
Before giving your answer, make sure your answer _DOES NOT result in overlaps_ between user request and existing timetable configuration.
State your reasoning to the USER for every answer you give."""
    ),
    "extra_prompt_messages": [
        # Few shot examples
        *example_1,
        *example_2,
        *example_3,
        MessagesPlaceholder(variable_name="memory"),
    ],
}


def callback_function(state, key):
    st.session_state[state] = st.session_state[key]


st.set_page_config(
    page_title="TimetableGPT",
    page_icon="📆",
    layout="wide",
    initial_sidebar_state="expanded",
)

st_callback = StreamlitCallbackHandler(
    st.container(), collapse_completed_thoughts=False
)

if "openai_api_key_value" not in st.session_state:
    st.session_state["openai_api_key_value"] = ""

with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key",
        key="openai_api_key",
        help="You can get your API key from https://platform.openai.com/account/api-keys.",
        type="password",
        on_change=callback_function,
        args=("openai_api_key_value", "openai_api_key"),
        value=st.session_state["openai_api_key_value"]
        if "openai_api_key_value" in st.session_state
        else "",
    )
    model = st.selectbox(
        "OpenAI Model:", ("gpt-4", "gpt-3.5-turbo-16k", "gpt-3.5-turbo")
    )
    st.markdown(
        "# How to use\n"
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

tab1, tab2 = st.tabs(["Chat", "Timetable"])

with tab2:
    timetable()

if "timetable" not in st.session_state:
    st.error("Please input your Timetable first")
elif st.session_state["timetable"].shape[0] == 0:
    st.error("Please input your Timetable first")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with tab1:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="memory", return_messages=True
    )


if prompt := st.chat_input("Ask me about the timetable"):
    with tab1:
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        llm = ChatOpenAI(
            client="TimetableGPT",
            temperature=0,
            model=str(model),
            openai_api_key=openai_api_key,
            streaming=True,
        )

        open_ai_agent_executor = initialize_agent(
            tools,
            llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
            agent_kwargs=agent_kwargs,
            memory=st.session_state["memory"],
        )

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            st_callback = StreamlitCallbackHandler(
                st.container(), expand_new_thoughts=True
            )
            response = open_ai_agent_executor.run(prompt, callbacks=[st_callback])
            message_placeholder.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
