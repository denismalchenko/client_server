from pydantic import BaseModel
from enum import Enum, auto
from uuid import UUID


class Status(Enum):
    created = auto()
    running = auto()
    ready = auto()
    error = auto()


class Task(BaseModel):
    id: UUID = UUID('00000000-0000-0000-0000-000000000000')
    status: Status = Status.created
    result: list = []
