from typing import Union


LANE_REWARDS = {reward['name']: {**reward, 'priority': i} for i, reward in enumerate([
    {
        'name': 'Earth Empire',
        'threshold': 40,
        'reward_description': 'Create an 8/8 Attacker with Twinstrike in another lane.',
        'effect': ['spawn', 'The Colossus'],
    },
    {
        'name': 'Fire Nation',
        'threshold': 35,
        'reward_description': 'Friendly characters in ALL lanes get +3/+0.',
        'effect': ['pumpAllFriendlies', 3, 0],
    },
    {
        'name': 'Republic City',
        'threshold': 35,
        'reward_description': 'Randomly play all cards in your hand to other lanes for free.',
        'effect': ['playAllCardsInHandForFree'],
    },
    {
        'name': 'Omashu',
        'threshold': 30,
        'reward_description': 'Friendly characters in ALL lanes make a bonus attack.',
        'effect': ['bonusAttackAllFriendlies'],
    },
    {
        'name': 'Aang Memorial Island',
        'threshold': 30,
        'reward_description': 'A random character in another lane gets +6/+6.',
        'effect': ['pumpRandomCharacterInAnotherLane', 6, 6],
    },
    {
        'name': 'Beifong Academy',
        'threshold': 25,
        'reward_description': 'Draw three random cards.',
        'effect': ['drawRandomCards', 3],
    },
    {
        'name': 'Agna Qel\'a',
        'threshold': 20,
        'reward_description': 'Fully heal friendly characters in ALL lanes.',
        'effect': ['healAllFriendlies'],
    },    
    {
        'name': 'Southern Air Temple',
        'threshold': 20,
        'reward_description': 'Create a 4/4 in another lane.',
        'effect': ['spawn', 'Air Nomads'],
    },    
    {
        'name': 'Hegemon\'s Folly',
        'threshold': 20,
        'reward_description': 'Discard your hand.',
        'effect': ['discardHand'],
    },    
    {
        'name': 'Ba Sing Se',
        'threshold': 20,
        'reward_description': 'Gain 2 mana next turn.',
        'effect': ['gainMana', 2],
    },    
    {
        'name': 'Western Air Temple',
        'threshold': 20,
        'reward_description': 'Friendly characters in this lane switch lanes.',
        'effect': ['friendlyCharactersInThisLaneSwitchLanes'],
    },
    {
        'name': 'Gaoling',
        'threshold': 15,
        'reward_description': 'Friendly characters in ALL lanes get +0/+2.',
        'effect': ['pumpAllFriendlies', 0, 2],
    },
    {
        'name': 'Bhanti Island',
        'threshold': 15,
        'reward_description': 'Draw two random cards.',
        'effect': ['drawRandomCards', 2],
    },
    {
        'name': 'Monkey Statue',
        'threshold': 10,
        'reward_description': 'Gain 1 mana next turn.',
        'effect': ['gainMana', 1],
    },
    {
        'name': 'Full Moon Bay',
        'threshold': 5,
        'reward_description': 'Draw a random card.',
        'effect': ['drawRandomCards', 1],
    },
    {
        'name': 'Spirit Oasis',
        'threshold': None,
        'reward_description': 'When you play your fourth character here, your characters here get +1/+1.',
        'effect': ['pumpAllCharactersPlayedHereWhenFilled', 1, 1],
    },
    {
        'name': 'Taihua Mountains',
        'threshold': None,
        'reward_description': 'Characters played here get +0/+2.',
        'effect': ['pumpAllCharactersPlayedHere', 0, 2],
    },
    {
        'name': 'Boiling Rock',
        'threshold': None,
        'reward_description': 'Characters played here get +1/+0.',
        'effect': ['pumpAllCharactersPlayedHere', 1, 0],
    },
    {
        'name': 'Foggy Swamp',
        'threshold': None,
        'reward_description': 'Characters played here get -1/-0.',
        'effect': ['pumpAllCharactersPlayedHere', -1, 0],
    },
    {
        'name': 'Si Wong Desert',
        'threshold': None,
        'reward_description': 'Characters played here get -0/-2 (min. 1 health).',
        'effect': ['pumpAllCharactersPlayedHere', 0, -2],
    },
    {
        'name': 'Chin Village',
        'threshold': None,
        'reward_description': 'Each player starts with two 1/1s in this lane.',
        'effect': ['spawnAtStart', 'Elephant Rat', 2],
    },
    {
        'name': 'Northern Water Tribe',
        'threshold': None,
        'reward_description': 'At the end of each turn, characters here fully heal.',
        'effect': ['healAllCharactersHereAtEndOfTurn'],
    },
    {
        'name': 'Serpent\'s Pass',
        'threshold': None,
        'reward_description': 'Characters here fight as though they were Attackers.',
        'effect': ['charactersHereFightAsAttackers'],
    },
    {
        'name': 'Shipwreck Cave',
        'threshold': None,
        'reward_description': 'When a character here dies, its owner gains +1 mana next turn.',
        'effect': ['ownerGainsManaNextTurnWhenCharacterDiesHere', 1],
    },
    {
        'name': 'Mt. Makapu',
        'threshold': None,
        'reward_description': 'At the end of each turn, deal 1 damage to all characters here.',
        'effect': ['dealDamageToAllCharactersHereAtEndOfTurn', 1],
    },
    {
        'name': 'Air Nomad Caves',
        'threshold': None,
        'reward_description': 'At the end of each turn, each side\'s first character switches lanes.',
        'effect': ['firstCharacterSwitchesLanesAtEndOfTurn'],
    },
])}

class LaneReward:
    def __init__(self, name: str, threshold: int, reward_description: str, effect: list[Union[str, int]], priority: int):
        self.name = name
        self.threshold = threshold
        self.reward_description = reward_description
        self.effect = effect
        self.priority = priority

    def to_json(self):
        return {
            "name": self.name,
            "threshold": self.threshold,
            "reward_description": self.reward_description,
            "effect": self.effect,
            "priority": self.priority,
        }
    
    @staticmethod
    def from_json(json: dict):
        return LaneReward(json["name"], json["threshold"], json["reward_description"], json["effect"], json["priority"])
    