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

    person_requested: Optional[list[str]] = Field(
        default=[], description="List of person name to search in the Timetable"
    )
    datetime_start_requested: Optional[datetime.datetime] = Field(
        default=datetime.datetime(1970, 1, 1, 0, 0, 0),
        description="Start date and start time specification",
    )
    datetime_end_requested: Optional[datetime.datetime] = Field(
        default=datetime.datetime(1970, 1, 1, 0, 0, 0),
        description="End date and end time specification",
    )
    room_requested: Optional[list[str]] = Field(
        default=[], description="List of room name to search in the Timetable"
    )

    class Config:
        arbitrary_types_allowed = True


class TimetablePostInput(BaseModel):
    """Input for Timetable check."""

    person_requested: str = Field(description="Person name to put in the Timetable")
    datetime_start_requested: datetime.datetime = Field(
        description="Start date and start time specification",
    )
    datetime_end_requested: datetime.datetime = Field(
        description="End date and end time specification",
    )
    room_requested: str = Field(description="Room name to put in the Timetable")

    class Config:
        arbitrary_types_allowed = True
