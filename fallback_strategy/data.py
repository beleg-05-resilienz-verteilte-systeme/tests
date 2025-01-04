import uuid
from dataclasses import dataclass, field

@dataclass
class Item:
    name: str
    price: int
    id: str = field(default_factory = lambda: str(uuid.uuid4()))
    description: str | None = None

@dataclass
class Database:
    name: str
    items: list[Item] = field(default_factory=list)
