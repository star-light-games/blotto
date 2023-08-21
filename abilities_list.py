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
        description='When I survive damage, I get +1+1.',
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
}