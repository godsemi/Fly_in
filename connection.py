from typing import Optional
from parse_raise import PR


class Connection:
    def __init__(self,
                 name1: str,
                 name2: str,
                 link_capacity: Optional[int] = 1
                 ) -> None:
        """Initialize a connection between two zones."""
        self.name1 = name1
        self.name2 = name2
        self.link_capacity = link_capacity

    def valid_name(self, name: str) -> bool:
        """Check whether a zone name belongs to this connection."""
        return name == self.name1 or name == self.name2

    def return_other(self, name: str) -> str:
        """Return the opposite endpoint of the connection."""
        if name == self.name1:
            return self.name2
        if name == self.name2:
            return self.name1
        raise PR(f"Error: Zone {name} is not in the connection.")

    def __repr__(self) -> str:
        """Return a readable representation of the connection."""
        return (
            f"Connection({self.name1} <-> {self.name2}, "
            f"capacity={self.link_capacity})"
        )
