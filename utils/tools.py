import datetime
from typing import Optional, Type

import streamlit as st
from langchain.tools import BaseTool
from pydantic import BaseModel

from utils.classes import TimetableCheckInput


# Functions
def _filter_intersection(
    timetable_df, datetime_start_requested, datetime_end_requested
):
    return timetable_df[
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


def get_availability(
    person_requested=[],
    datetime_start_requested=datetime.datetime(1970, 1, 1, 0, 0, 0),
    datetime_end_requested=datetime.datetime(1970, 1, 1, 0, 0, 0),
    room_requested=[],
):
    timetable_df = st.session_state["timetable"]
    timetable_df["initial_prompt_person"] = timetable_df["person"]
    timetable_df["initial_prompt_room"] = "Room " + timetable_df["room"]
    initial_prompt = (
        "List of possible person in the Timetable are: \n"
        + "\n".join(timetable_df["initial_prompt_person"].sort_values().unique())
        + "\n\nList of possible room in the Timetable are: \n"
        + "\n".join(timetable_df["initial_prompt_room"].sort_values().unique())
    )

    if len(person_requested) > 0:
        timetable_df = timetable_df[timetable_df["person"].isin(person_requested)]

    if len(room_requested) > 0:
        timetable_df = timetable_df[timetable_df["room"].isin(room_requested)]

    timetable_df = _filter_intersection(
        timetable_df, datetime_start_requested, datetime_end_requested
    )
    timetable_df["prompt_person"] = timetable_df["person"] + " is unavailable/occupied."
    timetable_df["prompt_room"] = (
        "Room " + timetable_df["room"] + " is unavailable/occupied."
    )

    return (
        initial_prompt
        + "\n\nThe inavailability list are specified below:\n"
        + "\n".join(timetable_df["prompt_person"].unique())
        + "\n"
        + "\n".join(timetable_df["prompt_room"].unique())
    )


def filter_timetable(
    person_requested=[],
    datetime_start_requested=datetime.datetime(1970, 1, 1, 0, 0, 0),
    datetime_end_requested=datetime.datetime(9999, 1, 1, 0, 0, 0),
    room_requested=[],
):
    timetable_df = st.session_state["timetable"]
    if len(person_requested) > 0:
        timetable_df = timetable_df[timetable_df["person"].isin(person_requested)]
    if len(room_requested) > 0:
        timetable_df = timetable_df[timetable_df["room"].isin(room_requested)]

    timetable_df = _filter_intersection(
        timetable_df, datetime_start_requested, datetime_end_requested
    )
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

    timetable_df = _filter_intersection(
        timetable_df, datetime_start_requested, datetime_end_requested
    )

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
        person_requested: list[str] = [],
        datetime_start_requested: datetime.datetime = datetime.datetime(
            1970, 1, 1, 0, 0, 0
        ),
        datetime_end_requested: datetime.datetime = datetime.datetime(
            1970, 1, 1, 0, 0, 0
        ),
        room_requested: list[str] = [],
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
        person_requested: list[str] = [],
        datetime_start_requested: datetime.datetime = datetime.datetime(
            1970, 1, 1, 0, 0, 0
        ),
        datetime_end_requested: datetime.datetime = datetime.datetime(
            9999, 1, 1, 0, 0, 0
        ),
        room_requested: list[str] = [],
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
    description = "Useful for when you need to find if there's a conflict between user request and existing schedule listed in the timetable."

    def _run(
        self,
        person_requested: list[str] = [],
        datetime_start_requested: datetime.datetime = datetime.datetime(
            1970, 1, 1, 0, 0, 0
        ),
        datetime_end_requested: datetime.datetime = datetime.datetime(
            1970, 1, 1, 0, 0, 0
        ),
        room_requested: list[str] = [],
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
