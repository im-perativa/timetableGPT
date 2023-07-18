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
        content="create a schedule for Person X on 6th February from 10am to 12pm in room Alpha",
        additional_kwargs={"name": "example_user_2"},
    ),
    AIMessage(
        content="""{'name': 'timetable_post', 'arguments': '{\
  \"person_requested\": \"Person X\",\
  \"datetime_start_requested\": \"2023-02-06T10:00:00\",\
  \"datetime_end_requested\": \"2023-02-06T12:00:00\",\
  \"room_requested\": \"Alpha\"\
}'}""",
        additional_kwargs={"name": "example_ai_2"},
    ),
    FunctionMessage(
        content="New schedule successfuly added to the Timetable",
        name="timetable_post",
        additional_kwargs={"name": "example_function_2"},
    ),
    AIMessage(
        content="I have successfully created a schedule for Person X on 6th February from 10am to 12pm in room Alpha",
        additional_kwargs={"name": "example_assistant_2"},
    ),
]

example_3 = [
    HumanMessage(
        content="what is the best time to arrange a 30 minutes meeting with Anna Koch and Wilson Cole on February 6th 2023?",
        additional_kwargs={"name": "example_user_3"},
    ),
    AIMessage(
        content="""{'name': 'timetable_availability', 'arguments': '{\
  \"person_requested\": [\"Anna Koch\", \"Person X\", \"Wilson Cole\"],\
  \"datetime_start_requested\": \"2023-02-06T00:00:00\",\
  \"datetime_end_requested\": \"2023-02-06T23:59:59\"\
}'}""",
        additional_kwargs={"name": "example_ai_3"},
    ),
    FunctionMessage(
        content="""
List of person in the Timetable are:
```
- Abby Montgomery
- Abdirahman Castaneda
- Anna Koch
- Wilson Cole
```

List of room in the Timetable are:
```
- Room Alpha
- Room Bravo
- Room Charlie
```

Person inavailability based on user requested time range are specified below:

```
- Anna Koch is unavailable/occupied from:
-- 09:10:00 to 10:50:00
-- 11:00:00 to 12:40:00
- Wilson Cole is unavailable/occupied from:
-- 10:10:00 to 12:40:00
```

Room inavailability based on user requested time range are specified below:

```
- Room Alpha is unavailable/occupied.
- Room Charlie is unavailable/occupied.
```
""",
        name="timetable_availability",
        additional_kwargs={"name": "example_function_3"},
    ),
    AIMessage(
        content="Based on the availability of Anna Koch and Wilson Cole, the best time to arrange 30 minutes for them is at 8.00 am to 9.30 am",
        additional_kwargs={"name": "example_assistant_3"},
    ),
]
