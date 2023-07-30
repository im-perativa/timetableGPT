import streamlit as st
import streamlit.components.v1 as components


def calendar(mode: str = "Room"):
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

    event_data_json = event_data.to_json(orient="records")

    components.html(
        f"""
    <html lang='en'>
        <head>
            <meta charset='utf-8' />
            <script src='https://cdn.jsdelivr.net/npm/fullcalendar-scheduler@6.1.8/index.global.min.js'></script>
            <script>

            document.addEventListener('DOMContentLoaded', function() {{
                var calendarEl = document.getElementById('calendar');
                var calendar = new FullCalendar.Calendar(calendarEl, {{
                    height: 520,
                    initialDate: '{initial_date}',
                    initialView: 'resourceTimelineDay',
                    hiddenDays: [0,6],
                    slotMinTime: '06:00:00',
                    slotMaxtime: '17:00:00',
                    headerToolbar: {{
                        left: 'prev,next today',
                        center: 'title',
                        right: 'resourceTimelineMonth,resourceTimelineWeek,resourceTimelineDay'
                    }},
                    resources: {str(resources)},
                    events: {str(event_data_json)}
                }});
                calendar.render();
            }});

            </script>
        </head>
        <body>
            <div id='calendar'></div>
        </body>
    </html>
    """,
        height=520,
    )
