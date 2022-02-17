from typing import List, Literal

from pydantic.dataclasses import dataclass


@dataclass
class CourseCreateForm:
    name: str
    title: str
    text: str
    categories: List[int]
    type: Literal['online', 'offline']
    links: str = ''


@dataclass
class CourseEditForm:
    id: str
    name: str
    title: str
    text: str
    categories: List[int]
    links: str


@dataclass
class CourseCopyForm:
    name: str


@dataclass
class CourseSubscribeForm:
    users: List[int]


@dataclass
class CategoryCopyForm:
    name: str
