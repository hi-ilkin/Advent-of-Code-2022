from dataclasses import dataclass, field
from typing import Union


@dataclass
class Directory:
    name: str
    size: int
    processed: bool = False
    files: list = field(default_factory=list)
    parent: Union[str, None] = None
    children: list = field(default_factory=list)
