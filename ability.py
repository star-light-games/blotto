from typing import Optional


class Ability:
    def __init__(self, name: str, description: str, number: Optional[int] = None, number_2: Optional[int] = None):
        self.name = name
        self.description = description
        self.number = number
        self.number_2 = number_2

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "number": self.number,
            "number_2": self.number_2,
        }
