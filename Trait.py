from typing import List


class SetTrait:
    def __init__(self, style: str, min_level: int = 0, max_level: int = 10):
        self.style = style
        self.min_level = min_level
        self.max_level = max_level


class Trait:
    def __init__(self, milestones: List[SetTrait], name: str, description: str, trait_id: str) -> None:
        self.milestones = milestones
        self.name = name
        self.description = description
        self.trait_id = trait_id

    def __hash__(self) -> int:
        return self.name.__hash__()

    def __repr__(self) -> str:
        return self.name
