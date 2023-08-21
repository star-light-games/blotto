

class Ability:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description
        }
