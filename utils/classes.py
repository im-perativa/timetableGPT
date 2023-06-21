# Classes
import datetime
from enum import Enum
from typing import Optional

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
    not_available_list: list[str] = Field(
        ...,
        description="List of person or room name to exclude because of their inavailability",
    )


class TimetableCheckInput(BaseModel):
    """Input for Timetable check."""

    person_requested: list[str] = Field(
        ..., description="List of person name to search the Timetable"
    )
    datetime_start_requested: Optional[datetime.datetime] = Field(
        default=datetime.datetime(1970, 1, 1, 0, 0, 0),
        description="Start date and start time specification from user request",
    )
    datetime_end_requested: Optional[datetime.datetime] = Field(
        default=datetime.datetime(1970, 1, 1, 0, 0, 0),
        description="End date and end time specification from user request",
    )
    room_requested: list[str] = Field(
        ..., description="List of room name to search in the Timetable"
    )

    class Config:
        arbitrary_types_allowed = True
