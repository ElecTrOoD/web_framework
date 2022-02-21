from typing import Literal

from pydantic.dataclasses import dataclass


@dataclass
class UserCreateForm:
    first_name: str
    last_name: str
    email: str
    type: Literal['student', 'teacher']
