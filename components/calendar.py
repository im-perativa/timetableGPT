import streamlit as st
from streamlit_calendar import calendar


def calendarComponent(mode: str = "Room"):
    event_data = st.session_state["timetable"].copy()

    event_data["datetime_start"] = event_data["datetime_start"].dt.strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
    event_data["datetime_end"] = event_data["datetime_end"].dt.strftime(
        "%Y-%m-%dT%H:%M:%S"
    )

    initial_date = ((event_data["datetime_start"].sort_values())[0].split("T"))[0]

    if mode == "Room":
        room_data = event_data["room"].unique()
        resources = [
            {"id": room, "title": f"Room {room}"} for room in sorted(room_data)
        ]

        event_data = event_data.rename(
            columns={
                "datetime_start": "start",
                "datetime_end": "end",
                "person": "title",
                "room": "resourceId",
            }
        )
    else:
        person_data = event_data["person"].unique()
        resources = [{"id": person, "title": person} for person in sorted(person_data)]

        event_data = event_data.rename(
            columns={
                "datetime_start": "start",
                "datetime_end": "end",
                "person": "resourceId",
                "room": "title",
            }
        )

    event_data_dict = event_data.to_dict(orient="records")

    calendar(
        events=event_data_dict,
        options={
            "height": 520,
            "initialDate": initial_date,
            "initialView": "resourceTimelineDay",
            "hiddenDays": [0, 6],
            "slotMinTime": "06:00:00",
            "slotMaxTime": "18:00:00",
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": "resourceTimelineMonth,resourceTimelineWeek,resourceTimelineDay",
            },
            "resources": resources,
        },
    )
