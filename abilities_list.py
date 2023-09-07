from ability import Ability


ABILITIES: dict[str, Ability] = {
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
    'PumpAttackOfCharactersPlayedHere': Ability(
        name='PumpAttackOfCharactersPlayedHere',
        description='Whenever you play a character in this lane (including myself), it gets +1/+0.',
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
        description='Whenever a friendly character moves into this lane, it gets +2/+2.',
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
        description='Whenever a friendly character in this lane is healed, it gets +2/+2.',
    ),
    'OnKillBuffHealth': Ability(
        name='OnKillBuffHealth',
        description='When I kill a character, I get +0/+2.',
    ),
}