import datetime
from typing import Optional, Type

from langchain.tools import BaseTool
from pydantic import BaseModel

from utils.classes import TimetableCheckInput, TimetablePostInput
from utils.functions import (
    delete_timetable,
    get_availability,
    get_conflict_status,
    get_timetable,
    post_timetable,
)


class TimetableAvailabilityTool(BaseTool):
    name = "timetable_availability"
    description = "Useful for when you need to find the availability of person and/or room(s) based on specific date and time"

    def _run(
        self,
        person_requested: Optional[list[str]] = None,
        datetime_start_requested: datetime.datetime = datetime.datetime(
            1970, 1, 1, 0, 0, 0
        ),
        datetime_end_requested: datetime.datetime = datetime.datetime(
            1970, 1, 1, 0, 0, 0
        ),
        room_requested: Optional[list[str]] = None,
    ):
        result = get_availability(
            person_requested,
            datetime_start_requested,
            datetime_end_requested,
            room_requested,
        )

        return result

    async def _arun(
        self,
        person_requested: Optional[list[str]] = None,
        datetime_start_requested: datetime.datetime = datetime.datetime(
            1970, 1, 1, 0, 0, 0
        ),
        datetime_end_requested: datetime.datetime = datetime.datetime(
            1970, 1, 1, 0, 0, 0
        ),
        room_requested: Optional[list[str]] = None,
    ):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = TimetableCheckInput


class TimetableGetTool(BaseTool):
    name = "timetable_get"
    description = "Useful for when you need to find the schedule of specific person or room based on user request"

    def _run(
        self,
        person_requested: Optional[list[str]] = None,
        datetime_start_requested: datetime.datetime = datetime.datetime(
            1970, 1, 1, 0, 0, 0
        ),
        datetime_end_requested: datetime.datetime = datetime.datetime(
            9999, 1, 1, 0, 0, 0
        ),
        room_requested: Optional[list[str]] = None,
    ):
        result = get_timetable(
            person_requested,
            datetime_start_requested,
            datetime_end_requested,
            room_requested,
        )

        return result

    async def _arun(
        self,
        person_requested: Optional[list[str]] = None,
        datetime_start_requested: datetime.datetime = datetime.datetime(
            1970, 1, 1, 0, 0, 0
        ),
        datetime_end_requested: datetime.datetime = datetime.datetime(
            9999, 1, 1, 0, 0, 0
        ),
        room_requested: Optional[list[str]] = None,
    ):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = TimetableCheckInput


class TimetableConflictCheckerTool(BaseTool):
    name = "timetable_check_conflict"
    description = "Useful for when you need to find if there's a conflict between user request and existing schedule listed in the timetable."

    def _run(
        self,
        person_requested: Optional[list[str]] = None,
        datetime_start_requested: datetime.datetime = datetime.datetime(
            1970, 1, 1, 0, 0, 0
        ),
        datetime_end_requested: datetime.datetime = datetime.datetime(
            1970, 1, 1, 0, 0, 0
        ),
        room_requested: Optional[list[str]] = None,
    ):
        result = get_conflict_status(
            person_requested,
            datetime_start_requested,
            datetime_end_requested,
            room_requested,
        )

        return result

    async def _arun(
        self,
        person_requested: Optional[list[str]] = None,
        datetime_start_requested: datetime.datetime = datetime.datetime(
            1970, 1, 1, 0, 0, 0
        ),
        datetime_end_requested: datetime.datetime = datetime.datetime(
            1970, 1, 1, 0, 0, 0
        ),
        room_requested: Optional[list[str]] = None,
    ):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = TimetableCheckInput


class TimetablePostTool(BaseTool):
    name = "timetable_post"
    description = """
    Useful for when you need to add new entry/schedule to the timetable. 
    User must include all required detail in their request before you use this tool.
    If the new entry/schedule cannot be created, explain the reason for the user.
    """

    def _run(
        self,
        person_requested: str,
        datetime_start_requested: datetime.datetime,
        datetime_end_requested: datetime.datetime,
        room_requested: str,
    ):
        result = post_timetable(
            person_requested,
            datetime_start_requested,
            datetime_end_requested,
            room_requested,
        )

        return result

    async def _arun(
        self,
        person_requested: str,
        datetime_start_requested: datetime.datetime,
        datetime_end_requested: datetime.datetime,
        room_requested: str,
    ):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = TimetablePostInput


class TimetableDeleteTool(BaseTool):
    name = "timetable_delete"
    description = "Useful for when you need to delete entry/schedule in the timetable based on user request."

    def _run(
        self,
        person_requested: Optional[list[str]] = None,
        datetime_start_requested: datetime.datetime = datetime.datetime(
            1970, 1, 1, 0, 0, 0
        ),
        datetime_end_requested: datetime.datetime = datetime.datetime(
            9999, 1, 1, 0, 0, 0
        ),
        room_requested: Optional[list[str]] = None,
    ):
        result = delete_timetable(
            person_requested,
            datetime_start_requested,
            datetime_end_requested,
            room_requested,
        )

        return result

    async def _arun(
        self,
        person_requested: Optional[list[str]] = None,
        datetime_start_requested: datetime.datetime = datetime.datetime(
            1970, 1, 1, 0, 0, 0
        ),
        datetime_end_requested: datetime.datetime = datetime.datetime(
            9999, 1, 1, 0, 0, 0
        ),
        room_requested: Optional[list[str]] = None,
    ):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = TimetableCheckInput
