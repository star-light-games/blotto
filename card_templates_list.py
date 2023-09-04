from card_template import CardTemplate


CARD_TEMPLATES = {
    'Combustion Man': CardTemplate(
        name='Combustion Man',
        abilities=['Attacker', 'InvincibilityWhileAttacking'],
        cost=1,
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
        abilities=['Attacker', 'OnSurviveDamagePump'],
        cost=5,
        attack=5,
        health=8,
        creature_types=['Avatar'],
    ),
    'Meelo': CardTemplate(
        name='Meelo',
        abilities=[],
        cost=1,
        attack=3,
        health=2,
        creature_types=['Air'],
    ),
    'Pabu': CardTemplate(
        name='Pabu',
        abilities=['DoubleTowerDamage'],
        cost=1,
        attack=2,
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
        cost=4,
        attack=1,
        health=5,
        creature_types=['Air'],
    ),
    'Ikki': CardTemplate(
        name='Ikki',
        abilities=[],
        cost=1,
        attack=2,
        health=5,
        creature_types=['Air'],
    ),
    'Riley': CardTemplate(
        name='Riley',
        abilities=['OnRevealPumpFriends'],
        cost=2,
        attack=1,
        health=1,
        creature_types=['Earth'],
    ),
    'Visola': CardTemplate(
        name='Visola',
        abilities=[],
        cost=2,
        attack=3,
        health=5,
        creature_types=['Water'],
    ),
    'Southern Raider': CardTemplate(
        name='Southern Raider',
        abilities=[],
        cost=2,
        attack=4,
        health=3,
        creature_types=['Fire'],
    ),
    'Hakoda': CardTemplate(
        name='Hakoda',
        abilities=['Attacker'],
        cost=2,
        attack=2,
        health=6,
        creature_types=['Water'],
    ),
    'Yon Rha': CardTemplate(
        name='Yon Rha',
        abilities=['OnTowerAttackDealMassDamage'],
        cost=4,
        attack=3,
        health=4,
        creature_types=['Fire'],
    ),
    'Sokka': CardTemplate(
        name='Sokka',
        abilities=['Attacker', 'StartOfTurnFullHeal'],
        cost=3,
        attack=3,
        health=5,
        creature_types=['Water'],
    ),
    'Zuko': CardTemplate(
        name='Zuko',
        abilities=['DoubleTowerDamage'],
        cost=3,
        attack=3,
        health=3,
        creature_types=['Fire'],
    ),
    'Naga': CardTemplate(
        name='Naga',
        abilities=[],
        cost=3,
        attack=4,
        health=6,
        creature_types=['Water'],
    ),
    'Admiral Zhao': CardTemplate(
        name='Admiral Zhao',
        abilities=['Attacker', 'OnRevealPumpAttackers'],
        cost=4,
        attack=2,
        health=3,
        creature_types=['Fire'],
    ),
    'Iroh II': CardTemplate(
        name='Iroh II',
        abilities=['PumpAttackOfCharactersPlayedHere'],
        cost=2,
        attack=2,
        health=2,
        creature_types=['Fire'],
    ),
    'Great Sage': CardTemplate(
        name='Great Sage',
        abilities=['OnTowerAttackDrawCard'],
        cost=4,
        attack=2,
        health=2,
        creature_types=['Fire'],
    ),
    'Lin': CardTemplate(
        name='Lin',
        abilities=['OnRevealShackle', 'ShacklesLastExtraTurn'],
        cost=4,
        attack=3,
        health=4,
        creature_types=['Earth'],
    ),
    'Prince Wu': CardTemplate(
        name='Prince Wu',
        abilities=['OnRevealGainMana'],
        cost=2,
        attack=1,
        health=1,
        creature_types=['Earth'],
    ),
    'Suyin': CardTemplate(
        name='Suyin',
        abilities=['OnRevealShackleAllEnemies'],
        cost=5,
        attack=2,
        health=3,
        creature_types=['Earth'],
    ),
    'Baatar Jr': CardTemplate(
        name='Baatar Jr',
        abilities=['OnRevealShackle', 'ShacklesDealTwoDamage'],
        cost=3,
        attack=1,
        health=2,
        creature_types=['Earth'],
    ),
    'Fang': CardTemplate(
        name='Fang',
        abilities=['Attacker', 'DealSixMoreDamageWhenLosing'],
        cost=4,
        attack=2,
        health=6,
        creature_types=['Air'],
    ),
    'Momo': CardTemplate(
        name='Momo',
        abilities=['SwitchLanesAfterAttacking'],
        cost=3,
        attack=3,
        health=4,
        creature_types=['Air'],
    ),
    'Kya': CardTemplate(
        name='Kya',
        abilities=['HealFriendlyCharacterAndTower'],
        cost=2,
        attack=2,
        health=3,
        creature_types=['Water'],
    ),
    'Aang': CardTemplate(
        name='Aang',
        abilities=['Attacker', 'SwitchLanesInsteadOfDying'],
        cost=5,
        attack=4,
        health=3,
        creature_types=['Avatar'],
    ),
    'Tenzin': CardTemplate(
        name='Tenzin',
        abilities=['CharacterMovesHerePumps'],
        cost=4,
        attack=4,
        health=4,
        creature_types=['Air'],
    ),
    'Gran Gran Kanna': CardTemplate(
        name='Gran Gran Kanna',
        abilities=['OnRevealHealAllFriendliesAndTowers'],
        cost=5,
        attack=2,
        health=2,
        creature_types=['Water'],
    ),
    'Fire Lord Ozai': CardTemplate(
        name='Fire Lord Ozai',
        abilities=['Attacker', 'OnRevealBonusAttack'],
        cost=5,
        attack=4,
        health=8,
        creature_types=['Fire'],
    ),
    'Ming Hua': CardTemplate(
        name='Ming Hua',
        abilities=['OnRevealLaneFightsFirst'],
        cost=4,
        attack=4,
        health=7,
        creature_types=['Water'],
    ),
    'Master Pakku': CardTemplate(
        name='Master Pakku',
        abilities=['Defender'],
        cost=5,
        attack=3,
        health=9,
        creature_types=['Water'],
    ),
}
