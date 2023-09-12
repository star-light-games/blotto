from typing import Optional


class Ability:
    def __init__(self, name: str, description: str, number: Optional[int] = None):
        self.name = name
        self.description = description
        self.number = number

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "number": self.number,
        }
