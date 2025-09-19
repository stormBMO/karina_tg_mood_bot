from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class User:
    id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]

@dataclass
class Reflection:
    user_id: int
    mood: int  # 1..5
    text: str
    tags: str = ""
