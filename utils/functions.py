import datetime

import pandas as pd
import streamlit as st
from datetimerange import DateTimeRange


def __filter_intersection(
    timetable_df: pd.DataFrame,
    datetime_start_requested: datetime.datetime,
    datetime_end_requested: datetime.datetime,
):
    timetable_df["intersection"] = timetable_df.apply(
        lambda row: DateTimeRange(
            row["datetime_start"], row["datetime_end"]
        ).is_intersection(
            DateTimeRange(datetime_start_requested, datetime_end_requested)
        ),
        axis=1,
    )
    return timetable_df[timetable_df["intersection"]].sort_values(
        ["datetime_start", "datetime_end"]
    )


def get_availability(
    person_requested=None,
    datetime_start_requested=datetime.datetime(1970, 1, 1, 0, 0, 0),
    datetime_end_requested=datetime.datetime(1970, 1, 1, 0, 0, 0),
    room_requested=None,
):
    timetable_df = st.session_state["timetable"]
    timetable_df["initial_prompt_person"] = "- " + timetable_df["person"]
    timetable_df["initial_prompt_room"] = "- " + "Room " + timetable_df["room"]
    initial_prompt = (
        "List of person in the Timetable are: \n```\n"
        + "\n".join(timetable_df["initial_prompt_person"].sort_values().unique())
        + "\n```\n\nList of room in the Timetable are: \n```\n"
        + "\n".join(timetable_df["initial_prompt_room"].sort_values().unique())
    )

    if person_requested:
        timetable_df = timetable_df[timetable_df["person"].isin(person_requested)]
    if room_requested:
        timetable_df = timetable_df[timetable_df["room"].isin(room_requested)]

    timetable_intersect_df = __filter_intersection(
        timetable_df, datetime_start_requested, datetime_end_requested
    )
    timetable_intersect_df["prompt"] = (
        "-- "
        + timetable_intersect_df["datetime_start"].dt.strftime("%H:%M:%S")
        + " to "
        + timetable_intersect_df["datetime_end"].dt.strftime("%H:%M:%S")
    )

    person = (
        timetable_intersect_df[["person", "prompt"]]
        .groupby(["person"], as_index=False)
        .agg({"prompt": "\n".join})
    )
    person["prompt_person"] = (
        "- " + person["person"] + " is unavailable/occupied from: \n" + person["prompt"]
    )
    room = (
        timetable_intersect_df[["room", "prompt"]]
        .groupby(["room"], as_index=False)
        .agg({"prompt": "\n".join})
    )
    room["prompt_room"] = "- " + "Room " + room["room"] + " is unavailable/occupied."

    return (
        initial_prompt
        + "\n```\n\nPerson inavailability based on user requested time range are specified below:\n\n```\n"
        + "\n".join(person["prompt_person"].sort_values().unique())
        + "\n```\n\nRoom inavailability based on user requested time range are specified below:\n\n```\n"
        + "\n".join(room["prompt_room"].sort_values().unique())
        + "\n```\n"
    )


def get_availability_json(
    person_requested=None,
    datetime_start_requested=datetime.datetime(1970, 1, 1, 0, 0, 0),
    datetime_end_requested=datetime.datetime(1970, 1, 1, 0, 0, 0),
    room_requested=None,
):
    timetable_df = st.session_state["timetable"]
    list_all_person = list(timetable_df["person"].sort_values().unique())
    list_all_room = list(timetable_df["room"].sort_values().unique())

    if person_requested:
        timetable_df = timetable_df[timetable_df["person"].isin(person_requested)]
    if room_requested:
        timetable_df = timetable_df[timetable_df["room"].isin(room_requested)]

    timetable_intersect_df = __filter_intersection(
        timetable_df, datetime_start_requested, datetime_end_requested
    )

    list_person_unavailable = list(
        timetable_intersect_df["person"].sort_values().unique()
    )
    list_room_unavailable = list(timetable_intersect_df["room"].sort_values().unique())

    return {
        "list_all_person": list_all_person,
        "list_all_room": list_all_room,
        "list_person_unavailable": list_person_unavailable,
        "list_room_unavailable": list_room_unavailable,
    }


def get_timetable(
    person_requested=None,
    datetime_start_requested=datetime.datetime(1970, 1, 1, 0, 0, 0),
    datetime_end_requested=datetime.datetime(9999, 1, 1, 0, 0, 0),
    room_requested=None,
):
    timetable_df = st.session_state["timetable"]
    if person_requested:
        timetable_df = timetable_df[timetable_df["person"].isin(person_requested)]
    if room_requested:
        timetable_df = timetable_df[timetable_df["room"].isin(room_requested)]

    timetable_df = (
        __filter_intersection(
            timetable_df, datetime_start_requested, datetime_end_requested
        )
        if len(timetable_df) > 0
        else timetable_df
    )
    return timetable_df


def post_timetable(
    person_requested: str,
    datetime_start_requested: datetime.datetime,
    datetime_end_requested: datetime.datetime,
    room_requested: str,
):
    timetable_df = st.session_state["timetable"]
    timetable_df_person_filtered = timetable_df[
        timetable_df["person"] == person_requested
    ]
    timetable_df_room_filtered = timetable_df[timetable_df["room"] == room_requested]

    person_intersection_check = (
        __filter_intersection(
            timetable_df_person_filtered,
            datetime_start_requested,
            datetime_end_requested,
        )
        if len(timetable_df_person_filtered) > 0
        else pd.DataFrame()
    )
    room_intersection_check = (
        __filter_intersection(
            timetable_df_room_filtered,
            datetime_start_requested,
            datetime_end_requested,
        )
        if len(timetable_df_room_filtered) > 0
        else pd.DataFrame()
    )

    if len(person_intersection_check) > 0 or len(room_intersection_check) > 0:
        return "Cannot add requested schedule, there will be conflict in the Timetable"

    timetable_df.loc[len(timetable_df)] = {
        "person": person_requested,
        "datetime_start": datetime_start_requested,
        "datetime_end": datetime_end_requested,
        "room": room_requested,
    }
    st.session_state["timetable"] = timetable_df
    return "New schedule successfuly added to the Timetable"


def delete_timetable(
    person_requested=None,
    datetime_start_requested=datetime.datetime(1970, 1, 1, 0, 0, 0),
    datetime_end_requested=datetime.datetime(9999, 1, 1, 0, 0, 0),
    room_requested=None,
):
    timetable_df = st.session_state["timetable"]
    if person_requested:
        timetable_df = timetable_df[timetable_df["person"].isin(person_requested)]
    if room_requested:
        timetable_df = timetable_df[timetable_df["room"].isin(room_requested)]

    timetable_df = __filter_intersection(
        timetable_df, datetime_start_requested, datetime_end_requested
    )
    print(datetime_start_requested, datetime_end_requested)

    if len(timetable_df) == 0:
        return "No entries to be deleted"

    st.session_state["timetable"].drop(list(timetable_df.index), inplace=True)
    return "Sucessfully deleted entries"


def get_conflict_status(
    person_requested=None,
    datetime_start_requested=datetime.datetime(1970, 1, 1, 0, 0, 0),
    datetime_end_requested=datetime.datetime(1970, 1, 1, 0, 0, 0),
    room_requested=None,
):
    timetable_df = st.session_state["timetable"]

    if person_requested:
        timetable_df = timetable_df[timetable_df["person"].isin(person_requested)]
    if room_requested:
        timetable_df = timetable_df[timetable_df["room"].isin(room_requested)]

    timetable_df = __filter_intersection(
        timetable_df, datetime_start_requested, datetime_end_requested
    )

    return (
        "There is a conflict in the timetable"
        if (len(timetable_df) > 0)
        else "There is no conflict in the timetable"
    )
