from typing import Optional


class Drone:
    def __init__(
            self, assigned_path: list[str], identifier: str
            ):
        """Initialize a drone with its assigned path."""
        self.path_index = 0
        self.assigned_path = assigned_path
        self.has_finished = False
        self.transiting = False
        self.identifier = identifier

    @property
    def actual_zone(self) -> str:
        """Return the drone's current zone name."""
        return self.assigned_path[self.path_index]

    @property
    def get_next_zone(self) -> Optional[str]:
        """Return the next zone in the drone's assigned path."""
        if self.path_index + 1 < len(self.assigned_path):
            return self.assigned_path[self.path_index]
        return None

    def movement(self, next_restricted: bool = False) -> None:
        """Advance the drone along its assigned path."""
        if self.has_finished:
            return

        if self.transiting:
            self.transiting = False
            self.path_index += 1

        elif next_restricted:
            self.transiting = True

        else:
            self.path_index += 1

        if self.path_index == len(self.assigned_path) - 1:
            self.has_finished = True
