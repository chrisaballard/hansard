from dataclasses import dataclass, field
from collections import defaultdict
from typing import List, Optional
from enum import Enum

class TagType(Enum):
    MAJOR_HEADING = "major-heading"
    MINOR_HEADING = "minor-heading"
    SPEECH = "speech"
    DIVISION = "division"
    MPLIST = "mplist"
    MPNAME = "mpname"
    DIVISION_COUNT = "divisioncount"


class EntityType(Enum):
    PERSON = "PERSON"
    DATE = "DATE"


class VoteType(Enum):
    AYE = "aye"
    NO = "no"


@dataclass
class EntityAttributes:
    start: int
    end: int


@dataclass
class Person:
    id: str
    name: Optional[str] = None
    attributes: Optional[EntityAttributes] = field(default_factory=list)
    type: EntityType = EntityType.PERSON.value

@dataclass
class PersonVote:
    persion_id: str
    vote: str


@dataclass
class Division:
    id: str
    count_aye: Optional[int] = 0
    count_no: Optional[int] = 0
    votes: Optional[List[PersonVote]] = field(default_factory=list)


@dataclass
class Heading:
    id: str
    name: str
    headings: Optional[List["Heading"]] = field(default_factory=list)
    speeches: Optional[List["Speech"]] = field(default_factory=list)
    votes: Optional[Division] = field(default_factory=list)


@dataclass
class Paragraph:
    text: str
    person_entities: List[Person]


@dataclass
class Speech:
    id: str
    type: str
    text: List[Paragraph]
    person: Optional[Person] = None

