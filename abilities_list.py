from typing import Callable, Union
from ability import Ability
from utils import element_to_color, plural


ABILITIES: dict[str, Union[Ability, Callable]] = {
    'Defender': Ability(
        name='Defender',
        description='Defender',
    ),
    'Attacker': Ability(
        name='Attacker',
        description='Attacker',
    ),
    'OnRevealShackle': Ability(
        name='OnRevealShackle',
        description='On reveal: shackle a random enemy character in this lane.',
    ),
    'OnSurviveDamagePump': lambda x, y: Ability(
        name='OnSurviveDamagePump',
        description=f'When I survive damage, I get +{x}/+{y}.',
        number=x,
        number_2=y,
    ),
    'Deathtouch': Ability(
        name='Deathtouch',
        description='I kill any character I fight with.',
    ),
    'InvincibilityWhileAttacking': Ability(
        name='InvincibilityWhileAttacking',
        description='When I attack I don\'t take damage back.',
    ),
    'DoubleTowerDamage': Ability(
        name='DoubleTowerDamage',
        description='When I attack the enemy tower, I deal double damage.',
    ),
    'EndOfTurnFullHeal': Ability(
        name='EndOfTurnFullHeal',
        description='At the end of each turn, I fully heal.',
    ),
    'OnRevealPumpFriends': lambda x, y: Ability(
        name='OnRevealPumpFriends',
        description=f'On reveal: give +{x}/+{y} to all friendly characters in this lane (including myself).',
        number=x,
        number_2=y,
    ),
    'OnTowerAttackDealMassDamage': lambda x: Ability(
        name='OnTowerAttackDealMassDamage',
        description=f'When I attack the enemy tower, I deal {x} damage to all enemy characters in this lane.',
        number=x,
    ),
    'OnRevealPumpAttackers': lambda x, y: Ability(
        name='OnRevealPumpAttackers',
        description=f'On reveal: give +{x}/+{y} to all friendly attackers in this lane (including myself).',
        number=x,
        number_2=y,
    ),
    'PumpCharactersPlayedHere': lambda x, y: Ability(
        name='PumpCharactersPlayedHere',
        description=f'Whenever you play a character in this lane (including myself), it gets +{x}/+{y}.',
        number=x,
        number_2=y,
    ),
    'OnTowerAttackDrawCard': Ability(
        name='OnTowerAttackDrawCard',
        description='When I attack the enemy tower, draw a random card.',
    ),
    'ShacklesLastExtraTurn': Ability(
        name='ShacklesLastExtraTurn',
        description='Shackles on enemy characters last an additional turn in this lane.',
    ),
    'OnRevealGainMana': lambda x: Ability(
        name='OnRevealGainMana',
        description=f'On reveal: gain {x} mana next turn only.',
        number=x,
    ),
    'OnRevealShackleAllEnemies': Ability(
        name='OnRevealShackleAllEnemies',
        description='On reveal: shackle all enemy characters in this lane.',
    ),
    'ShacklesDealDamage': lambda x: Ability(
        name='ShacklesDealDamage',
        description=f'When you shackle an enemy character in this lane, deal {x} damage to it.',
        number=x,
    ),
    'DealMoreDamageWhenLosing': lambda x: Ability(
        name='DealMoreDamageWhenLosing',
        description=f'I deal {x} more damage when my team is losing this lane.',
        number=x,
    ),
    'SwitchLanesAfterAttacking': Ability(
        name='SwitchLanesAfterAttacking',
        description='After I attack, I switch lanes.',
    ),
    'HealFriendlyCharacterAndTower': lambda x: Ability(
        name='HealFriendlyCharacterAndTower',
        description=f'When I am played, heal a friendly character fully and your tower for {x}.',
        number=x,
    ),
    'SwitchLanesInsteadOfDying': Ability(
        name='SwitchLanesInsteadOfDying',
        description='When I would die for the first time each turn, I heal fully and switch lanes instead.',
    ),
    'CharacterMovesHerePumps': lambda x, y: Ability(
        name='CharacterMovesHerePumps',
        description=f'Whenever a friendly character switches into this lane, I get +{x}/+{y}.',
        number=x,
        number_2=y,
    ),
    'OnRevealHealAllFriendliesAndTowers': lambda x: Ability(
        name='OnRevealHealAllFriendliesAndTowers',
        description=f'On reveal: fully heal ALL friendly characters and ALL friendly towers for {x}.',
        number=x,
    ),
    'OnRevealBonusAttack': lambda x: Ability(
        name='OnRevealBonusAttack',
        description=f'On reveal: I make {x} bonus attack{plural(x)}.',
        number=x,
    ),
    'OnRevealLaneFightsFirst': Ability(
        name='OnRevealLaneFightsFirst',
        description='On reveal: this lane fights first this turn.',
    ),
    'OnKillSwitchLanes': Ability(
        name='OnKillSwitchLanes',
        description='When I kill a character, I switch lanes.',
    ),
    'PumpOnFriendlyHeal': lambda x, y: Ability(
        name='PumpOnFriendlyHeal',
        description=f'Whenever a friendly character in this lane is healed, that character gets +{x}/+{y}.',
        number=x,
        number_2=y,
    ),
    'OnKillBuffHealth': lambda x, y: Ability(
        name='OnKillBuffHealth',
        description=f'When I kill a character, I get +{x}/+{y}.',
        number=x,
        number_2=y,
    ),
    'OnRevealFriendliesSwitchLanes': Ability(
        name='OnRevealFriendliesSwitchLanes',
        description='On reveal: all friendly characters in this lane switch lanes.',
    ),
    'CharacterMovesHereThatCharacterPumps': lambda x, y: Ability(
        name='CharacterMovesHereThatCharacterPumps',
        description=f'Whenever a friendly character switches into this lane, it gets +{x}/+{y}.',
        number=x,
        number_2=y,
    ),
    'OnRevealDamageToAll': lambda x: Ability(
        name='OnRevealDamageToAll',
        description=f'On reveal: deal {x} damage to ALL characters in this lane (including your own).',
        number=x,
    ),
    'EndOfTurnFullHealForAllFriendlies': Ability(
        name='EndOfTurnFullHealForAllFriendlies',
        description='At the end of each turn, fully heal all friendly characters in this lane.',
    ),
    'OnFriendlyHealPumpMyself': lambda x, y: Ability(
        name='OnFriendlyHealPumpMyself',
        description=f'Whenever a friendly character in this lane is healed, I get +{x}/+{y}.',
        number=x,
        number_2=y,
    ),
    'OnRevealDamageSelf': lambda x: Ability(
        name='OnRevealDamageSelf',
        description=f'On reveal: I deal {x} damage to myself.',
        number=x,
    ),
    'OnRevealDrawCards': lambda x: Ability(
        name='OnRevealDrawCards',
        description=f'On reveal: draw {x} random card{plural(x)}.',
        number=x,
    ),
    'OnDrawCardPump': lambda x, y: Ability(
        name='OnDrawCardPump',
        description=f'When you draw a card, I get +{x}/+{y}.',
        number=x,
        number_2=y,
    ),
    'OnDamageTowerPumpTeam': lambda x, y: Ability(
        name='OnDamageTowerPumpTeam',
        description=f'When I damage the enemy tower, all friendly characters in this lane get +{x}/+{y}.',
        number=x,
        number_2=y,
    ),
    'OnFriendlySlayPump': lambda x, y: Ability(
        name='OnFriendlySlayPump',
        description=f'Whenever a friendly character kills an enemy character, I get +{x}/+{y}.',
        number=x,
        number_2=y,
    ),
    'OnTowerDamageGainMana': lambda x: Ability(
        name='OnTowerDamageGainMana',
        description=f'When I damage the enemy tower, gain {x} mana next turn.',
        number=x,
    ),
    'DoNotDamageEnemyCharacters': Ability(
        name='DoNotDamageEnemyCharacters',
        description='I do not damage enemy characters.',
    ),
    'ShackleOnFriendlyEarth': Ability(
        name='ShackleOnFriendlyEarth',
        description='When a friendly Earth (green) character is played (including me), shackle a random enemy character in this lane.',
    ),
    'OnShackleDrawCard': Ability(
        name='OnShackleDrawCard',
        description='When you shackle an enemy character in this lane, draw a random card.',
    ),
    'OnRevealPumpFriendlyCharactersOfElement': lambda x, y, z: Ability(
        name='OnRevealPumpFriendlyCharactersOfElement',
        description=f'On reveal: give +{x}/+{y} to all friendly {z} ({element_to_color(z)}) characters in this lane (including myself).',
        number=x,
        number_2=y,
        creature_type=z,
    ),
    'OnCharacterMoveHereMakeSpirit': Ability(
        name='OnCharacterMoveHereMakeSpirit',
        description='Whenever a friendly character moves into this lane, make a 3/1 Spirit in another lane.',
    ),
    'PumpFriendlyCharactersOfElementPlayedHere': lambda x, y, z: Ability(
        name='PumpFriendlyCharactersOfElementPlayedHere',
        description=f'Whenever you play a {z} ({element_to_color(z)}) character in this lane (including myself), it gets +{x}/+{y}.',
        number=x,
        number_2=y,
        creature_type=z,
    ),
    'OnAttackDoubleAttack': Ability(
        name='OnAttackDoubleAttack',
        description='After I attack, double my strength.',
    ),
    'OnFriendlyCharacterDeathHealFullyAndSwitchLanes': Ability(
        name='OnFriendlyCharacterDeathHealFullyAndSwitchLanes',
        description='If a friendly character in ANY other lane would die, heal it fully and switch it to my lane instead.',
    ),
    'OnCharacterMoveHereShackle': Ability(
        name='OnCharacterMoveHereShackle',
        description='Whenever a friendly character moves into this lane, shackle a random enemy character in this lane.',
    ),
    'SwitchLanesAtEndOfTurn': Ability(
        name='SwitchLanesAtEndOfTurn',
        description='At the end of each turn, I switch lanes.',
    ),
    'OnRevealFillEnemyLaneWithCabbages': Ability(
        name='OnRevealFillEnemyLaneWithCabbages',
        description='On reveal: fill the enemy lane with 0/1 Cabbages.',
    ),
}