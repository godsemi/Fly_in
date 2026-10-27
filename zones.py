from typing import Optional


class TypeZone:

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Zone:

    def __init__(self,
                 name: str,
                 x: int,
                 y: int,
                 type_zone: str = TypeZone.NORMAL,
                 color: Optional[str] = None,
                 max_drones: int = 1,
                 is_start: bool = False,
                 is_end: bool = False
                 ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.type_zone = type_zone
        self.color = color
        self.max_drones = max_drones
        self.is_start = is_start
        self.is_end = is_end

    def __repr__(self) -> str:
        return (
            f"Zone(name={self.name}, type={self.type_zone}, "
            f"pos=({self.x},{self.y}), max_drones={self.max_drones})"
        )
