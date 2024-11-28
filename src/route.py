from dataclasses import dataclass
from handler import HandlerFunc


@dataclass
class Route:
    cmd: str
    handler: HandlerFunc
