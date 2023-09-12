
LANE_REWARDS = {
    'Fire Nation': {
        'name': 'Fire Nation',
        'threshold': 45,
        'reward_description': 'ALL friendly characters get +3/+0.',
    },
    'Southern Air Temple': {
        'name': 'Southern Air Temple',
        'threshold': 25,
        'reward_description': 'Create a 4/4 in another lane.',
    },
    'Full Moon Bay': {
        'name': 'Full Moon Bay',
        'threshold': 10,
        'reward_description': 'Draw a card.',
    },
}

class LaneReward:
    def __init__(self, name: str, threshold: int, reward_description: str):
        self.name = name
        self.threshold = threshold
        self.reward_description = reward_description

    def to_json(self):
        return {
            "name": self.name,
            "threshold": self.threshold,
            "reward_description": self.reward_description,
        }
    
    @staticmethod
    def from_json(json: dict):
        return LaneReward(json["name"], json["threshold"], json["reward_description"])
    