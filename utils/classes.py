# Classes
import datetime
from enum import Enum

from pydantic import BaseModel, Field


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
