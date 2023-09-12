from typing import Callable, Union
from ability import Ability


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
    'OnSurviveDamagePump': Ability(
        name='OnSurviveDamagePump',
        description='When I survive damage, I get +1/+1.',
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
    'StartOfTurnFullHeal': Ability(
        name='StartOfTurnFullHeal',
        description='At the start of each turn, I fully heal.',
    ),
    'OnRevealPumpFriends': Ability(
        name='OnRevealPumpFriends',
        description='On reveal: give +1/+1 to all friendly characters in this lane (including myself).',
    ),
    'OnTowerAttackDealMassDamage': Ability(
        name='OnTowerAttackDealMassDamage',
        description='When I attack the enemy tower, I deal 2 damage to all enemy characters.',
    ),
    'OnRevealPumpAttackers': Ability(
        name='OnRevealPumpAttackers',
        description='On reveal: give +2/+2 to all friendly attackers in this lane (including myself).',
    ),
    'PumpAttackOfCharactersPlayedHere': lambda x: Ability(
        name='PumpAttackOfCharactersPlayedHere',
        description=f'Whenever you play a character in this lane (including myself), it gets +{x}/+0.',
        number=x,
    ),
    'OnTowerAttackDrawCard': Ability(
        name='OnTowerAttackDrawCard',
        description='When I attack the enemy tower, draw a card.',
    ),
    'ShacklesLastExtraTurn': Ability(
        name='ShacklesLastExtraTurn',
        description='Shackles on enemy characters last an additional turn in this lane.',
    ),
    'OnRevealGainMana': Ability(
        name='OnRevealGainMana',
        description='On reveal: gain 1 mana next turn only.',
    ),
    'OnRevealShackleAllEnemies': Ability(
        name='OnRevealShackleAllEnemies',
        description='On reveal: shackle all enemy characters in this lane.',
    ),
    'ShacklesDealTwoDamage': Ability(
        name='ShacklesDealTwoDamage',
        description='When you shackle an enemy character in this lane, deal 2 damage to it.',
    ),
    'DealSixMoreDamageWhenLosing': Ability(
        name='DealSixMoreDamageWhenLosing',
        description='I deal 6 more damage when my team is losing this lane.',
    ),
    'SwitchLanesAfterAttacking': Ability(
        name='SwitchLanesAfterAttacking',
        description='After I attack, I switch lanes.',
    ),
    'HealFriendlyCharacterAndTower': Ability(
        name='HealFriendlyCharacterAndTower',
        description='When I am played, heal a friendly character fully and your tower for 3.',
    ),
    'SwitchLanesInsteadOfDying': Ability(
        name='SwitchLanesInsteadOfDying',
        description='When I would die for the first time each turn, I heal fully and switch lanes instead.',
    ),
    'CharacterMovesHerePumps': Ability(
        name='CharacterMovesHerePumps',
        description='Whenever a friendly character switches into this lane, I get +2/+2.',
    ),
    'OnRevealHealAllFriendliesAndTowers': Ability(
        name='OnRevealHealAllFriendliesAndTowers',
        description='On reveal: fully heal ALL friendly characters and ALL friendly towers for 5.',
    ),
    'OnRevealBonusAttack': Ability(
        name='OnRevealBonusAttack',
        description='On reveal: I make a bonus attack.',
    ),
    'OnRevealLaneFightsFirst': Ability(
        name='OnRevealLaneFightsFirst',
        description='On reveal: this lane fights first this turn.',
    ),
    'OnKillSwitchLanes': Ability(
        name='OnKillSwitchLanes',
        description='When I kill a character, I switch lanes.',
    ),
    'PumpOnFriendlyHeal': Ability(
        name='PumpOnFriendlyHeal',
        description='Whenever a friendly character in this lane is healed, I get +2/+2.',
    ),
    'OnKillBuffHealth': Ability(
        name='OnKillBuffHealth',
        description='When I kill a character, I get +0/+2.',
    ),
    'OnRevealFriendliesSwitchLanes': Ability(
        name='OnRevealFriendliesSwitchLanes',
        description='On reveal: all friendly characters in this lane switch lanes.',
    ),
    'CharacterMovesHereThatCharacterPumps': Ability(
        name='CharacterMovesHereThatCharacterPumps',
        description='Whenever a friendly character switches into this lane, it gets +1/+1.',
    ),
    'OnRevealDamageToAll': lambda x: Ability(
        name='OnRevealDamageToAll',
        description=f'On reveal: deal {x} damage to ALL characters in this lane (including your own).',
        number=x,
    ),
    'EndOfTurnFullHealForAllFriendlies': Ability(
        name='EndOfTurnFullHealForAllFriendlies',
        description='At the end of each turn, fully heal all friendly characters.',
    ),
    'OnFriendlyHealPumpMyself': Ability(
        name='OnFriendlyHealPumpMyself',
        description='Whenever a friendly character is healed, I get +1/+1.',
    ),
    'OnRevealDamageSelf': lambda x: Ability(
        name='OnRevealDamageSelf',
        description=f'On reveal: I deal {x} damage to myself.',
        number=x,
    ),
    'OnRevealDrawCards': lambda x: Ability(
        name='OnRevealDrawCards',
        description=f'On reveal: draw {x} card{"" if x != 1 else "s"}.',
        number=x,
    ),
    'OnDrawCardPump': lambda x, y: Ability(
        name='OnDrawCardPump',
        description=f'When you draw a card, I get +{x}/+{y}.',
        number=x,
        number_2=y,
    ),
}