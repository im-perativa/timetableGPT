from langchain.schema import AIMessage, FunctionMessage, HumanMessage

example_1 = [
    HumanMessage(
        content="list all unoccupied room on February 6th, 2023 from 10am to 12pm",
        additional_kwargs={"name": "example_user"},
    ),
    AIMessage(
        content="""{'name': 'timetable_availability', 'arguments': '{\
  \"datetime_start_requested\": \"2023-02-06T10:00:00\",\
  \"datetime_end_requested\": \"2023-02-06T12:00:00\"\
}'}""",
        additional_kwargs={"name": "example_ai"},
    ),
    FunctionMessage(
        content="""
List of person in the Timetable are:
```
- Abby Montgomery
- Abdirahman Castaneda
```

List of room in the Timetable are:
```
- Room Alpha
- Room Bravo
- Room Charlie
```

Person inavailability based on user requested time range are specified below:

```
- Abby Montgomery is unavailable/occupied from:
-- 09:10:00 to 10:50:00
-- 11:00:00 to 12:40:00
- Abdirahman Castaneda is unavailable/occupied from:
-- 10:10:00 to 12:40:00
```

Room inavailability based on user requested time range are specified below:

```
- Room Alpha is unavailable/occupied.
- Room Charlie is unavailable/occupied.
```
""",
        name="timetable_availability",
        additional_kwargs={"name": "example_function"},
    ),
    AIMessage(
        content="The list of unoccupied rooms on February 6th, 2023 from 10am to 12pm is as follows:\n - Room Bravo",
        additional_kwargs={"name": "example_assistant"},
    ),
]

example_2 = [
    HumanMessage(
        content="list the schedule for Abdirahman Castaneda on February 6th, 2023",
        additional_kwargs={"name": "example_user_2"},
    ),
    AIMessage(
        content="""{'name': 'timetable_availability', 'arguments': '{\
  \"datetime_start_requested\": \"2023-02-06T10:00:00\",\
  \"datetime_end_requested\": \"2023-02-06T12:00:00\"\
}'}""",
        additional_kwargs={"name": "example_ai_2"},
    ),
    FunctionMessage(
        content="""
List of person in the Timetable are:
```
- Abby Montgomery
- Abdirahman Castaneda
```

List of room in the Timetable are:
```
- Room Alpha
- Room Bravo
- Room Charlie
```

Person inavailability based on user requested time range are specified below:

```
- Abby Montgomery is unavailable/occupied from:
-- 09:10:00 to 10:50:00
-- 11:00:00 to 12:40:00
- Abdirahman Castaneda is unavailable/occupied from:
-- 10:10:00 to 12:40:00
```

Room inavailability based on user requested time range are specified below:

```
- Room Alpha is unavailable/occupied.
- Room Charlie is unavailable/occupied.
```
""",
        name="timetable_availability",
        additional_kwargs={"name": "example_function_2"},
    ),
    AIMessage(
        content="Abdirahman Castaneda is unavailable/occupied from 10:10:00 to 12:40:00",
        additional_kwargs={"name": "example_assistant_2"},
    ),
]
