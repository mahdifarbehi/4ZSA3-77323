from dataclasses import dataclass, asdict


@dataclass
class UserDTO:
    id: int
    username: str

    def to_dict(self):
        return asdict(self)
