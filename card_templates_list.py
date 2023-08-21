from card_template import CardTemplate


CARD_TEMPLATES = {
    'Combustion Man': CardTemplate(
        name='Combustion Man',
        abilities=['Attacker', 'InvincibilityWhileAttacking'],
        cost=2,
        attack=1,
        health=1,
        creature_types=['Fire'],
    ),
    'Dai Li Agent': CardTemplate(
        name='Dai Li Agent',
        abilities=['OnRevealShackle'],
        cost=1,
        attack=1,
        health=1,
        creature_types=['Earth'],
    ),
    'Katara': CardTemplate(
        name='Katara',
        abilities=['Defender', 'StartOfTurnFullHeal'],
        cost=3,
        attack=2,
        health=5,
        creature_types=['Water'],
    ),
    'Korra': CardTemplate(
        name='Korra',
        abilities=['Defender', 'OnSurviveDamagePump'],
        cost=5,
        attack=6,
        health=6,
        creature_types=['Avatar'],
    ),
    'Meelo': CardTemplate(
        name='Meelo',
        abilities=['Defender'],
        cost=1,
        attack=2,
        health=2,
        creature_types=['Air'],
    ),
    'Pabu': CardTemplate(
        name='Pabu',
        abilities=['DoubleTowerDamage'],
        cost=1,
        attack=1,
        health=1,
        creature_types=['Fire'],
    ),
    'Tonraq': CardTemplate(
        name='Tonraq',
        abilities=['Defender'],
        cost=1,
        attack=1,
        health=4,
        creature_types=['Water'],
    ),
    'Zaheer': CardTemplate(
        name='Zaheer',
        abilities=['Attacker', 'Deathtouch'],
        cost=5,
        attack=1,
        health=6,
        creature_types=['Air'],
    ),
}