import datetime
import time
from enum import Enum
from typing import Optional, Type

import streamlit as st
from langchain.agents import AgentExecutor
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain.tools import BaseTool, format_tool_to_openai_function
from pydantic import BaseModel, Field
from streamlit_chat import message


# Classes
class InstanceTypeEnum(str, Enum):
    PERSON = "person"
    ROOM = "room"


class TimetableInstanceFinderInput(BaseModel):
    """Input for Timetable check."""

    instance_type: InstanceTypeEnum = Field(
        ...,
        description="Type of object you want to search from the Timetable (person or room)",
    )
    query: str = Field(
        ...,
        description="Optional query to filter the result of object you want to search from the Timetable (person or room)",
    )


class TimetableCheckInput(BaseModel):
    """Input for Timetable check."""

    person_requested: list[str] = Field(
        ..., description="List of person name to search the Timetable"
    )
    datetime_start_requested: datetime.datetime = Field(
        ..., description="Start date and start time specification from user request"
    )
    datetime_end_requested: datetime.datetime = Field(
        ..., description="End date and end time specification from user request"
    )
    room_requested: list[str] = Field(
        ..., description="List of room name to search in the Timetable"
    )

    class Config:
        arbitrary_types_allowed = True


# Functions
def get_availability(
    person_requested=[],
    datetime_start_requested=datetime.datetime(1970, 1, 1, 0, 0, 0),
    datetime_end_requested=datetime.datetime(9999, 12, 31, 0, 0, 0),
    room_requested=[],
):
    timetable_df = st.session_state["timetable"]
    timetable_df["initial_prompt_person"] = timetable_df["person"] + " is available."
    timetable_df["initial_prompt_room"] = timetable_df["room"] + " is available."
    initial_prompt = (
        "\n".join(timetable_df["initial_prompt_person"].sort_values().unique())
        + "\n"
        + "\n".join(timetable_df["initial_prompt_room"].sort_values().unique())
    )

    if len(person_requested) > 0:
        timetable_df = timetable_df[timetable_df["person"].isin(person_requested)]

    if len(room_requested) > 0:
        timetable_df = timetable_df[timetable_df["room"].isin(room_requested)]

    timetable_df = timetable_df[
        (
            (timetable_df["datetime_start"] >= datetime_start_requested)
            & (timetable_df["datetime_end"] <= datetime_end_requested)
        )
        | (
            (timetable_df["datetime_start"] >= datetime_start_requested)
            & (timetable_df["datetime_start"] <= datetime_end_requested)
        )
        | (
            (timetable_df["datetime_end"] >= datetime_start_requested)
            & (timetable_df["datetime_end"] <= datetime_end_requested)
        )
        | (
            (timetable_df["datetime_start"] <= datetime_start_requested)
            & (timetable_df["datetime_end"] >= datetime_end_requested)
        )
    ]
    timetable_df["prompt"] = (
        timetable_df["person"]
        + " and room "
        + timetable_df["room"]
        + " is unavailable from "
        + timetable_df["datetime_start"].dt.strftime("%d %B %Y %H:%M:%S")
        + " to "
        + timetable_df["datetime_end"].dt.strftime("%d %B %Y %H:%M:%S")
        + "."
    )

    return initial_prompt + "\n" + "\n".join(timetable_df["prompt"])


def filter_timetable(
    person_requested=[],
    datetime_start_requested=datetime.datetime(1970, 1, 1, 0, 0, 0),
    datetime_end_requested=datetime.datetime(9999, 12, 31, 0, 0, 0),
    room_requested=[],
):
    timetable_df = st.session_state["timetable"]
    if len(person_requested) > 0:
        timetable_df = timetable_df[timetable_df["person"].isin(person_requested)]
    if len(room_requested) > 0:
        timetable_df = timetable_df[timetable_df["room"].isin(room_requested)]

    timetable_df = timetable_df[
        (
            (timetable_df["datetime_start"] >= datetime_start_requested)
            & (timetable_df["datetime_end"] <= datetime_end_requested)
        )
        | (
            (timetable_df["datetime_start"] >= datetime_start_requested)
            & (timetable_df["datetime_start"] <= datetime_end_requested)
        )
        | (
            (timetable_df["datetime_end"] >= datetime_start_requested)
            & (timetable_df["datetime_end"] <= datetime_end_requested)
        )
        | (
            (timetable_df["datetime_start"] <= datetime_start_requested)
            & (timetable_df["datetime_end"] >= datetime_end_requested)
        )
    ]
    timetable_df["prompt"] = (
        timetable_df["person"]
        + " has a schedule from "
        + timetable_df["datetime_start"].dt.strftime("%d %B %Y %H:%M:%S")
        + " to "
        + timetable_df["datetime_end"].dt.strftime("%d %B %Y %H:%M:%S")
        + " at room "
        + timetable_df["room"]
        + "."
    )

    return "\n".join(timetable_df["prompt"])


def get_conflict_status(
    person_requested=[],
    datetime_start_requested=datetime.datetime(1970, 1, 1, 0, 0, 0),
    datetime_end_requested=datetime.datetime(1970, 1, 1, 0, 0, 0),
    room_requested=[],
):
    timetable_df = st.session_state["timetable"]

    if len(person_requested) > 0:
        timetable_df = timetable_df[timetable_df["person"].isin(person_requested)]
    if len(room_requested) > 0:
        timetable_df = timetable_df[timetable_df["room"].isin(room_requested)]

    timetable_df = timetable_df[
        (
            (timetable_df["datetime_start"] >= datetime_start_requested)
            & (timetable_df["datetime_end"] <= datetime_end_requested)
        )
        | (
            (timetable_df["datetime_start"] >= datetime_start_requested)
            & (timetable_df["datetime_start"] <= datetime_end_requested)
        )
        | (
            (timetable_df["datetime_end"] >= datetime_start_requested)
            & (timetable_df["datetime_end"] <= datetime_end_requested)
        )
        | (
            (timetable_df["datetime_start"] <= datetime_start_requested)
            & (timetable_df["datetime_end"] >= datetime_end_requested)
        )
    ]

    return (
        "There is a conflict in the timetable"
        if (timetable_df.shape[0] > 0)
        else "There is no conflict in the timetable"
    )


# Tools
class TimetableAvailabilityTool(BaseTool):
    name = "timetable_availability"
    description = "Useful for when you need to find the availability of a person and/or room based on specific date and time from user request"

    def _run(
        self,
        person_requested: list[str],
        datetime_start_requested: datetime.datetime,
        datetime_end_requested: datetime.datetime,
        room_requested: list[str],
    ):
        result = get_availability(
            person_requested,
            datetime_start_requested,
            datetime_end_requested,
            room_requested,
        )

        return result

    def _arun(
        self,
        person_requested: list[str],
        datetime_start_requested: datetime.datetime,
        datetime_end_requested: datetime.datetime,
        room_requested: list[str],
    ):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = TimetableCheckInput


class TimetableFilterTool(BaseTool):
    name = "timetable_filter"
    description = "Useful for when you need to filter the timetable to find a schedule for specific person, room or datetime based on user request"

    def _run(
        self,
        person_requested: list[str],
        datetime_start_requested: datetime.datetime,
        datetime_end_requested: datetime.datetime,
        room_requested: list[str],
    ):
        result = filter_timetable(
            person_requested,
            datetime_start_requested,
            datetime_end_requested,
            room_requested,
        )

        return result

    def _arun(
        self,
        person_requested: list[str],
        datetime_start_requested: datetime.datetime,
        datetime_end_requested: datetime.datetime,
        room_requested: list[str],
    ):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = TimetableCheckInput


class TimetableConflictCheckerTool(BaseTool):
    name = "timetable_check_conflict"
    description = "Useful for when you need to find if there's a conflict between user request and existing schedule listed in the timetable"

    def _run(
        self,
        person_requested: list[str],
        datetime_start_requested: datetime.datetime,
        datetime_end_requested: datetime.datetime,
        room_requested: list[str],
    ):
        result = get_conflict_status(
            person_requested,
            datetime_start_requested,
            datetime_end_requested,
            room_requested,
        )

        return result

    def _arun(
        self,
        person_requested: list[str],
        datetime_start_requested: datetime.datetime,
        datetime_end_requested: datetime.datetime,
        room_requested: list[str],
    ):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = TimetableCheckInput


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
        1 - USER cannot schedule to occupy a ROOM if the ROOM is unavailable.
        2 - USER cannot schedule a meeting with a PERSON if the PERSON is unavailable.
        3 - Similarly, each PERSON listed in the Timetable cannot schedule to meet with other PERSON if one of them is unavailable.
        4 - Outside of the schedule information listed in the Timetable, all PERSON and all ROOM listed in the Timetable is available.
        ============
        """
    )
)

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key")
    "[View the source code](https://github.com/im-perativa/timetableGPT/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/im-perativa/timetableGPT?quickstart=1)"

st.title("📆 Timetable GPT")

st.session_state

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
