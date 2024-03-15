from dataclasses import dataclass, field
from collections import defaultdict
from typing import List, Optional

@dataclass
class Heading:
    id: str
    name: str
    headings: Optional[List["Heading"]] = field(default_factory=list)
    speeches: Optional[List["Speech"]] = field(default_factory=list)

@dataclass
class Speech:
    id: str
    speakername: str
    type: str
    person_id: str
    text: List[str]
