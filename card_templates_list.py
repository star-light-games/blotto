import random
from card_template import CardTemplate


CARD_TEMPLATES = {
    'Combustion Man': CardTemplate(
        name='Combustion Man',
        abilities=['Attacker', ('OnRevealBonusAttack', 1), 'InvincibilityWhileAttacking'],
        cost=1,
        attack=1,
        health=1,
        creature_types=['Fire'],
        rarity='common',
    ),
    'Dai Li Agent': CardTemplate(
        name='Dai Li Agent',
        abilities=['ShackleOnFriendlyEarth'],
        cost=1,
        attack=2,
        health=2,
        creature_types=['Earth'],
        rarity='common',
    ),
    'Katara': CardTemplate(
        name='Katara',
        abilities=['Defender', 'EndOfTurnFullHeal'],
        cost=3,
        attack=2,
        health=6,
        creature_types=['Water'],
        rarity='common',
    ),
    'Korra': CardTemplate(
        name='Korra',
        abilities=['Attacker', ('OnSurviveDamagePump', 1, 1)],
        cost=5,
        attack=6,
        health=8,
        creature_types=['Avatar'],
        rarity='rare',
    ),
    'Foot Soldier': CardTemplate(
        name='Foot Soldier',
        abilities=[],
        cost=1,
        attack=3,
        health=2,
        creature_types=['Fire'],
        rarity='common',
    ),
    'Pabu': CardTemplate(
        name='Pabu',
        abilities=['DoubleTowerDamage'],
        cost=1,
        attack=2,
        health=1,
        creature_types=['Fire'],
        rarity='common',
    ),
    'Tonraq': CardTemplate(
        name='Tonraq',
        abilities=['Defender', ('OnSurviveDamagePump', 0, 2)],
        cost=1,
        attack=1,
        health=4,
        creature_types=['Water'],
        rarity='common',
    ),
    'Zaheer': CardTemplate(
        name='Zaheer',
        abilities=['Attacker', 'Deathtouch'],
        cost=4,
        attack=1,
        health=6,
        creature_types=['Air'],
        rarity='common',
    ),
    'Ikki': CardTemplate(
        name='Ikki',
        abilities=['SwitchLanesAtEndOfTurn'],
        cost=1,
        attack=2,
        health=6,
        creature_types=['Air'],
        rarity='common',
    ),
    'Riley': CardTemplate(
        name='Riley',
        abilities=['Attacker', ('OnRevealPumpFriends', 1, 1)],
        cost=2,
        attack=2,
        health=3,
        creature_types=['Earth'],
        rarity='common',
    ),
    'Visola': CardTemplate(
        name='Visola',
        abilities=[('OnSurviveDamagePump', 1, 1)],
        cost=2,
        attack=3,
        health=7,
        creature_types=['Air'],
        rarity='common',
    ),
    'Southern Raider': CardTemplate(
        name='Southern Raider',
        abilities=[],
        cost=2,
        attack=4,
        health=3,
        creature_types=['Fire'],
        rarity='common',
    ),
    'Hakoda': CardTemplate(
        name='Hakoda',
        abilities=['Attacker', ('SurvivePumpFriendlyAttackers', 0, 2)],
        cost=2,
        attack=2,
        health=5,
        creature_types=['Air'],
        rarity='common',
    ),
    'Yon Rha': CardTemplate(
        name='Yon Rha',
        abilities=['Attacker', 'Shield', ('OnKillBuffHealth', 2, 2)],
        cost=4,
        attack=4,
        health=2,
        creature_types=['Fire'],
        rarity='common',
    ),
    'Sokka': CardTemplate(
        name='Sokka',
        abilities=['Attacker', 'EndOfTurnFullHeal', ('OnKillBuffHealth', 1, 1)],
        cost=3,
        attack=3,
        health=4,
        creature_types=['Water'],
        rarity='common',
    ),
    'Mai': CardTemplate(
        name='Mai',
        abilities=['DoubleTowerDamage', 'OnTriggerKillEnemyBonusAttack'],
        cost=3,
        attack=3,
        health=2,
        creature_types=['Fire'],
        rarity='rare',
    ),
    'Naga': CardTemplate(
        name='Naga',
        abilities=[('OnKillBuffHealth', 2, 2)],
        cost=3,
        attack=4,
        health=7,
        creature_types=['Water'],
        rarity='common',
    ),
    'Admiral Zhao': CardTemplate(
        name='Admiral Zhao',
        abilities=['Attacker', ('OnRevealPumpAttackers', 2, 2)],
        cost=4,
        attack=4,
        health=6,
        creature_types=['Fire'],
        rarity='common',
    ),
    'Iroh II': CardTemplate(
        name='Iroh II',
        abilities=[('PumpCharactersPlayedHere', 1, 0)],
        cost=1,
        attack=2,
        health=1,
        creature_types=['Fire'],
        rarity='common',
    ),
    'Professor Zei': CardTemplate(
        name='Professor Zei',
        abilities=['OnTowerAttackDrawCard'],
        cost=4,
        attack=5,
        health=2,
        creature_types=['Earth'],
        rarity='common',
    ),
    'Lin': CardTemplate(
        name='Lin',
        abilities=['OnRevealShackle', ('OnShacklePumpSelf', 2, 2)],
        cost=4,
        attack=3,
        health=3,
        creature_types=['Earth'],
        rarity='common',
    ),
    'Prince Wu': CardTemplate(
        name='Prince Wu',
        abilities=[('OnRevealGainMana', 1)],
        cost=2,
        attack=3,
        health=3,
        creature_types=['Earth'],
        rarity='common',
    ),
    'Suyin': CardTemplate(
        name='Suyin',
        abilities=[('OnRevealShackleSeveral', 3)],
        cost=5,
        attack=4,
        health=2,
        creature_types=['Earth'],
        rarity='rare',
    ),
    'Baatar Jr.': CardTemplate(
        name='Baatar Jr.',
        abilities=['OnRevealShackle', ('ShacklesDealDamage', 2)],
        cost=3,
        attack=3,
        health=4,
        creature_types=['Earth'],
        rarity='common',
    ),
    'Oogi': CardTemplate(
        name='Oogi',
        abilities=['Attacker', ('DealMoreDamageWhenLosing', 6)],
        cost=4,
        attack=2,
        health=6,
        creature_types=['Air'],
        rarity='common',
    ),
    'Momo': CardTemplate(
        name='Momo',
        abilities=['SwitchLanesAtEndOfTurn'],
        cost=2,
        attack=4,
        health=6,
        creature_types=['Air'],
        rarity='common',
    ),
    'Kya': CardTemplate(
        name='Kya',
        abilities=[('HealFriendlyCharacterAndTower', 3), ('PumpOnFriendlyHeal', 1, 1)],
        cost=2,
        attack=2,
        health=6,
        creature_types=['Water'],
        rarity='common',
    ),
    'Aang': CardTemplate(
        name='Aang',
        abilities=['Attacker', 'SwitchLanesInsteadOfDying'],
        cost=4,
        attack=4,
        health=2,
        creature_types=['Avatar'],
        rarity='rare',
    ),
    'Tenzin': CardTemplate(
        name='Tenzin',
        abilities=[('CharacterMovesHerePumps', 3, 3)],
        cost=4,
        attack=4,
        health=4,
        creature_types=['Air'],
        rarity='common',
    ),
    'Gran-Gran Kanna': CardTemplate(
        name='Gran-Gran Kanna',
        abilities=[('OnRevealHealAllFriendliesAndTowers', 5)],
        cost=4,
        attack=3,
        health=3,
        creature_types=['Water'],
        rarity='common',
    ),
    'Fire Lord Ozai': CardTemplate(
        name='Fire Lord Ozai',
        abilities=['Attacker', 'Twinstrike', ('OnRevealPumpFriendlyCharactersOfElement', 3, 0, 'Fire')],
        cost=5,
        attack=5,
        health=8,
        creature_types=['Fire'],
        rarity='common',
    ),
    'Ming-Hua': CardTemplate(
        name='Ming-Hua',
        abilities=['Attacker', 'KillEnemyAttackAgain'],
        cost=4,
        attack=4,
        health=7,
        creature_types=['Water'],
        rarity='common'
    ),
    'Master Pakku': CardTemplate(
        name='Master Pakku',
        abilities=['Defender', ('OnKillBuffHealth', 1, 1)],
        cost=5,
        attack=3,
        health=10,
        creature_types=['Water'],
        rarity='common',
    ),
    'Opal': CardTemplate(
        name='Opal',
        abilities=['Attacker', 'SwitchLanesAtEndOfTurn'],
        cost=3,
        attack=3,
        health=8,
        creature_types=['Air'],
        rarity='common',
    ),
    'Mother Kya': CardTemplate(
        name='Mother Kya',
        abilities=[('PumpOnFriendlyHeal', 3, 3)],
        cost=2,
        attack=2,
        health=5,
        creature_types=['Water'],
        rarity='common',
    ),
    'Air Nomads': CardTemplate(
        name='Air Nomads',
        abilities=[],
        cost=3,
        attack=4,
        health=4,
        creature_types=['Air'],
        not_in_card_pool=True,
        rarity='common',
    ),
    'Bato': CardTemplate(
        name='Bato',
        abilities=['Defender', ('OnSurviveDamagePump', 1, 1)],
        cost=4,
        attack=2,
        health=7,
        creature_types=['Water'],
        rarity='common',
    ),
    'Tarrlok': CardTemplate(
        name='Tarrlok',
        abilities=['OnRevealStealEnemy'],
        cost=6,
        attack=3,
        health=3,
        creature_types=['Water'],
        rarity='rare',
    ),
    'Appa': CardTemplate(
        name='Appa',
        abilities=['OnRevealFriendliesSwitchLanes'],
        cost=3,
        attack=4,
        health=4,
        creature_types=['Air'],
        rarity='common',
    ),
    'Monk Gyatso': CardTemplate(
        name='Monk Gyatso',
        abilities=[('CharacterMovesHereThatCharacterPumps', 2, 0)],
        cost=1,
        attack=2,
        health=2,
        creature_types=['Air'],
        rarity='common',
    ),
    'Ghazan': CardTemplate(
        name='Ghazan',
        abilities=['Attacker', ('OnRevealDamageToAll', 1)],
        cost=3,
        attack=3,
        health=6,
        creature_types=['Air'],
        rarity='common',
    ),
    'Elder Katara': CardTemplate(
        name='Elder Katara',
        abilities=['EndOfTurnFullHealForAllFriendlies', ('OnFriendlyHealPumpMyself', 2, 0)],
        cost=3,
        attack=2,
        health=6,
        creature_types=['Water'],
        rarity='rare',
    ),
    'Hama': CardTemplate(
        name='Hama',
        abilities=['OnRevealEnemiesFight'],
        cost=3,
        attack=3,
        health=1,
        creature_types=['Water'],
        rarity='rare',
    ),
    'Hiroshi': CardTemplate(
        name='Hiroshi',
        abilities=['Defender', ('OnRevealDrawCards', 1)],
        cost=1,
        attack=1,
        health=1,
        creature_types=['Earth'],
        rarity='common',
    ),
    'Zuko': CardTemplate(
        name='Zuko',
        abilities=[('OnRevealDamageSelf', 4)],
        cost=1,
        attack=3,
        health=5,
        creature_types=['Fire'],
        rarity='common',
    ),
    'Fire Lord Sozin': CardTemplate(
        name='Fire Lord Sozin',
        abilities=[('PumpCharactersPlayedHere', 2, 0)],
        cost=3,
        attack=4,
        health=2,
        creature_types=['Fire'],
        rarity='rare',
    ),
    'Kyoshi': CardTemplate(
        name='Kyoshi',
        abilities=['Attacker', ('OnRevealDamageToAll', 2)],
        cost=5,
        attack=5,
        health=10,
        creature_types=['Avatar'],
        rarity='common',
    ),
    'The Big Bad Hippo': CardTemplate(
        name='The Big Bad Hippo',
        abilities=['Defender', ('OnRevealDrawCards', 2)],
        cost=3,
        attack=2,
        health=3,
        creature_types=['Earth'],
        rarity='common',
    ),
    'The Boulder': CardTemplate(
        name='The Boulder',
        abilities=['Defender', ('OnRevealDrawCards', 3)],
        cost=5,
        attack=3,
        health=6,
        creature_types=['Earth'],
        rarity='common',
    ),
    'La': CardTemplate(
        name='La',
        abilities=[('OnDrawCardPump', 2, 0)],
        cost=2,
        attack=1,
        health=2,
        creature_types=['Water'],
        rarity='common',
    ),
    'Moon Spirit Yang': CardTemplate(
        name='Moon Spirit Yang',
        abilities=['Attacker', ('OnDrawCardPump', 3, 3)],
        cost=4,
        attack=2,
        health=2,
        creature_types=['Water'],
        rarity='rare',
    ),
    'Izumi': CardTemplate(
        name='Izumi',
        abilities=[('OnDamageTowerPumpTeam', 1, 0)],
        cost=2,
        attack=3,
        health=2,
        creature_types=['Fire'],
        rarity='common',
    ),
    'Kai': CardTemplate(
        name='Kai',
        abilities=[('OnTowerDamageGainMana', 1)],
        cost=2,
        attack=1,
        health=3,
        creature_types=['Air'],
        rarity='common',
    ),
    'Roku': CardTemplate(
        name='Roku',
        abilities=['DoNotDamageEnemyCharacters'],
        cost=2,
        attack=5,
        health=8,
        creature_types=['Avatar'],
        rarity='common',
    ),
    'Kuvira': CardTemplate(
        name='Kuvira',
        abilities=['OnRevealShackle', 'OnShackleDrawCard'],
        cost=2,
        attack=2,
        health=2,
        creature_types=['Earth'],
        rarity='rare',
    ),
    'Jinora': CardTemplate(
        name='Jinora',
        abilities=['OnCharacterMoveHereMakeSpirit'],
        cost=3,
        attack=3,
        health=3,
        creature_types=['Air'],
        rarity='rare',
    ),
    'Spirit': CardTemplate(
        name='Spirit',
        abilities=[],
        cost=1,
        attack=4,
        health=2,
        creature_types=[],
        not_in_card_pool=True,
        rarity='common',
    ),
    'Unalaq': CardTemplate(
        name='Unalaq',
        abilities=['Attacker', ('OnRevealPumpFriendlyCharactersOfElement', 1, 3, 'Water')],
        cost=4,
        attack=3,
        health=9,
        creature_types=['Water'],
        rarity='common',
    ),
    'Bumi II': CardTemplate(
        name='Bumi II',
        abilities=[('PumpFriendlyCharactersOfElementPlayedHere', 2, 1, 'Air')],
        cost=2,
        attack=2,
        health=3,
        creature_types=['Air'],
        rarity='common',
    ),
    'Toph': CardTemplate(
        name='Toph',
        abilities=['Attacker', 'Twinstrike', 'OnAttackDoubleAttack'],
        cost=3,
        attack=1,
        health=8,
        creature_types=['Earth'],
        rarity='rare',
    ),
    'Uncle Iroh': CardTemplate(
        name='Uncle Iroh',
        abilities=['Defender', 'OnFriendlyCharacterDeathHealFullyAndSwitchLanes'],
        cost=4,
        attack=2,
        health=6,
        creature_types=['Fire'],
        rarity='rare',
    ),
    'Yangchen': CardTemplate(
        name='Yangchen',
        abilities=['OnCharacterMoveHereShackle'],
        cost=2,
        attack=3,
        health=4,
        creature_types=['Avatar'],
        rarity='common',
    ),
    'Cabbage Man': CardTemplate(
        name='Cabbage Man',
        abilities=['Attacker', 'Twinstrike', 'OnRevealFillEnemyLaneWithCabbages'],
        cost=1,
        attack=3,
        health=2,
        creature_types=['Earth'],
        rarity='rare',
    ),
    'Cabbage': CardTemplate(
        name='Cabbage',
        abilities=[],
        cost=0,
        attack=0,
        health=1,
        creature_types=[],
        not_in_card_pool=True,
        rarity='common',
    ),
    'generic_1drop': CardTemplate(
        name='generic_1drop',
        abilities=[],
        cost=1,
        attack=2,
        health=2,
        creature_types=[],
        not_in_card_pool=True,
        rarity='common',
    ),
    'generic_2drop': CardTemplate(
        name='generic_2drop',
        abilities=[],
        cost=2,
        attack=3,
        health=3,
        creature_types=[],
        not_in_card_pool=True,
        rarity='common',
    ),
    'generic_3drop': CardTemplate(
        name='generic_3drop',
        abilities=['Attacker'],
        cost=3,
        attack=3,
        health=5,
        creature_types=[],
        not_in_card_pool=True,
        rarity='common',
    ),
    'generic_4drop': CardTemplate(
        name='generic_4drop',
        abilities=['Attacker'],
        cost=4,
        attack=3,
        health=7,
        creature_types=[],
        not_in_card_pool=True,
        rarity='common',
    ),
    'Elephant Rat': CardTemplate(
        name='Elephant Rat',
        abilities=[],
        cost=1,
        attack=1,
        health=1,
        creature_types=[],
        not_in_card_pool=True,
        rarity='common',
    ),
    'The Colossus': CardTemplate(
        name='The Colossus',
        abilities=['Attacker', 'Twinstrike'],
        cost=8,
        attack=8,
        health=8,
        creature_types=[],
        not_in_card_pool=True,
        rarity='common',
    ),
    'The Painted Lady': CardTemplate(
        name='The Painted Lady',
        abilities=['DealDamageEqualToCurrentHealth'],
        cost=2,
        attack=1,
        health=4,
        creature_types=['Water'],
        rarity='common',
    ),
    'Azula': CardTemplate(
        name='Azula',
        abilities=['OnRevealDiscardRandomCardAndDealDamageEqualToCost'],
        cost=2,
        attack=3,
        health=4,
        creature_types=['Fire'],
        rarity='common',
    ),
    'Kuruk': CardTemplate(
        name='Kuruk',
        abilities=['Attacker', 'Twinstrike', 'OnRevealAllAttackersMakeBonusAttack'],
        cost=5,
        attack=4,
        health=9,
        creature_types=['Air'],
        rarity='rare',
    ),
    'Ty Lee': CardTemplate(
        name='Ty Lee',
        abilities=['OnRevealSilenceRandomEnemy'],
        cost=3,
        attack=4,
        health=4,
        creature_types=['Fire'],
        rarity='common',
    ),
    'Amon': CardTemplate(
        name='Amon',
        abilities=['Attacker', 'OnRevealSilenceAllCharacters'],
        cost=5,
        attack=3,
        health=7,
        creature_types=['Water'],
        rarity='rare',
    ),
    'Thod': CardTemplate(
        name='Thod',
        abilities=['Attacker', 'InvincibilityWhileAttacking', 'OnDamageCharacterSilenceIt'],
        cost=3,
        attack=1,
        health=1,
        creature_types=['Earth'],
        rarity='common',
    ),
    'Senna': CardTemplate(
        name='Senna',
        abilities=['Defender', ('OnSurviveGainMana', 1)],
        cost=3,
        attack=1,
        health=7,
        creature_types=['Water'],
        rarity='common',
    ),
    'Taqukaq': CardTemplate(
        name='Taqukaq',
        abilities=['Defender', ('OnKillBuffHealth', 1, 0)],
        cost=2,
        attack=1,
        health=8,
        creature_types=['Water'],
        rarity='common',
    ),
    'Eska': CardTemplate(
        name='Eska',
        abilities=['Attacker', 'OnRevealSummonDesna'],
        cost=4,
        attack=5,
        health=2,
        creature_types=['Water'],
        rarity='rare',
    ),
    'Desna': CardTemplate(
        name='Desna',
        abilities=['Defender'],
        cost=3,
        attack=2,
        health=5,
        creature_types=['Water'],
        not_in_card_pool=True,
        rarity='rare',
    ),
    'Kelsang': CardTemplate(
        name='Kelsang',
        abilities=[('OnTriggerSurvivePump', 1, 0)],
        cost=1,
        attack=2,
        health=4,
        creature_types=['Air'],
        rarity='common',
    ),
    'Varrick': CardTemplate(
        name='Varrick',
        abilities=[('OnTriggerSurvivePumpSelf', 2, 2)],
        cost=2,
        attack=2,
        health=2,
        creature_types=['Water'],
        rarity='common',
    ),
    'Princess Yue': CardTemplate(
        name='Princess Yue',
        abilities=[('OnTriggerSurvivePump', 2, 3)],
        cost=3,
        attack=2,
        health=3,
        creature_types=['Water'],
        rarity='rare',
    ),
    'Yagoda': CardTemplate(
        name='Yagoda',
        abilities=['OnRevealHealAndPumpSelf'],
        cost=3,
        attack=2,
        health=2,
        creature_types=['Water'],
        rarity='common',
    ),
    'Tashi': CardTemplate(
        name='Tashi',
        abilities=['Defender', 'SurviveSwitchLanes'],
        cost=4,
        attack=2,
        health=10,
        creature_types=['Air'],
        rarity='common',
    ),
    'Meelo': CardTemplate(
        name='Meelo',
        abilities=['Attacker', ('OnSurviveDamagePump', 1, 0)],
        cost=1,
        attack=1,
        health=6,
        creature_types=['Air'],
        rarity='common',
    ),
    'Tsemo': CardTemplate(
        name='Tsemo',
        abilities=['OnTowerAttackDrawCard', 'OnRevealDiscard'],
        cost=1,
        attack=1,
        health=1,
        creature_types=['Air'],
        rarity='rare',
    ),
    'Yung': CardTemplate(
        name='Yung',
        abilities=[('HitTowerPumpSelf', 2, 1)],
        cost=2,
        attack=2,
        health=2,
        creature_types=['Air'],
        rarity='common',
    ),
    'Juicy': CardTemplate(
        name='Juicy',
        abilities=['Attacker', 'OnRevealEnemiesSwitchLanes'],
        cost=5,
        attack=3,
        health=6,
        creature_types=['Air'],
        rarity='rare',
    ),
    'Otaku': CardTemplate(
        name='Otaku',
        abilities=[('OnDiscardPump', 3, 0)],
        cost=2,
        attack=3,
        health=5,
        creature_types=['Air'],
        rarity='rare',
    ),
    'Ryu': CardTemplate(
        name='Ryu',
        abilities=[('HitTowerDamageAllCharacters', 2)],
        cost=4,
        attack=4,
        health=8,
        creature_types=['Air'],
        rarity='rare',
    ),
    'Council of Elders': CardTemplate(
        name='Council of Elders',
        abilities=[('OnTriggerHitTowerPump', 3, 0)],
        cost=3,
        attack=4,
        health=3,
        creature_types=['Air'],
        rarity='rare',
    ),
    'Lefty': CardTemplate(
        name='Lefty',
        abilities=['HitTowerOtherCharactersSwitchLanes'],
        cost=2,
        attack=4,
        health=3,
        creature_types=['Air'],
        rarity='common',
    ),
    'Huu': CardTemplate(
        name='Huu',
        abilities=[('OnTriggerKillEnemyHealAndPumpSelf', 2, 2)],
        cost=3,
        attack=4,
        health=5,
        creature_types=['Water'],
        rarity='rare',
    ),
    'Master Yu': CardTemplate(
        name='Master Yu',
        abilities=['Attacker', 'InvincibilityAgainstShackled'],
        cost=3,
        attack=3,
        health=7,
        creature_types=['Earth'],
        rarity='common',
    ),
    'Joo Dee': CardTemplate(
        name='Joo Dee',
        abilities=['AttackersDontDealDamage'],
        cost=3,
        attack=0,
        health=1,
        creature_types=['Earth'],
        rarity='rare',
    ),
    'Teo': CardTemplate(
        name='Teo',
        abilities=['HitTowerGiveShield'],
        cost=2,
        attack=3,
        health=2,
        creature_types=['Earth'],
        rarity='common',
    ),
    'King Bumi': CardTemplate(
        name='King Bumi',
        abilities=['Attacker', 'Twinstrike', ('OnRevealDiscardHandAndPump', 4, 4)],
        cost=6,
        attack=3,
        health=3,
        creature_types=['Earth'],
        rarity='rare',
    ),
    'Suki': CardTemplate(
        name='Suki',
        abilities=['Defender', 'Shield', ('OnShieldBreakPumpSelf', 2, 2)],
        cost=4,
        attack=2,
        health=4,
        creature_types=['Earth'],
        rarity='common',
    ),
    'Badgermole': CardTemplate(
        name='Badgermole',
        abilities=['Shield'],
        cost=3,
        attack=4,
        health=5,
        creature_types=['Earth'],
        rarity='common',
    ),
    'Champion Ming': CardTemplate(
        name='Champion Ming',
        abilities=['EarlyFighter', 'HitTowerShackle'],
        cost=4,
        attack=5,
        health=4,
        creature_types=['Earth'],
        rarity='common',
    ),
    'Queen Hou-Ting': CardTemplate(
        name='Queen Hou-Ting',
        abilities=['OnTriggerHitTowerBonusAttack'],
        cost=4,
        attack=5,
        health=6,
        creature_types=['Earth'],
        rarity='rare',
    ),
    'Resistance Fighter': CardTemplate(
        name='Resistance Fighter',
        abilities=['DeathtouchAgainstDefenders'],
        cost=1,
        attack=2,
        health=4,
        creature_types=['Earth'],
        rarity='common',
    ),
    'Canyon Guide': CardTemplate(
        name='Canyon Guide',
        abilities=['Shield', 'OnRevealShieldFriendlies'],
        cost=3,
        attack=3,
        health=1,
        creature_types=['Earth'],
        rarity='common',
    ),
    'Bolin': CardTemplate(
        name='Bolin',
        abilities=['HitTowerDamageAllEnemiesEqualToDamage'],
        cost=5,
        attack=3,
        health=7,
        creature_types=['Earth'],
        rarity='rare',
    ),
    'Tyro': CardTemplate(
        name='Tyro',
        abilities=[('PumpOnGainShield', 2, 2)],
        cost=2,
        attack=3,
        health=3,
        creature_types=['Earth'],
        rarity='common',
    ),
    'Bum-Ju': CardTemplate(
        name='Bum-Ju',
        abilities=['Attacker', ('OnDrawCardPump', 1, 1)],
        cost=1,
        attack=1,
        health=1,
        creature_types=['Water'],
        rarity='common',
    ),
    'Guru Laghima': CardTemplate(
        name='Guru Laghima',
        abilities=['Attacker', 'FriendliesDealDamageEqualToCurrentHealth'],
        cost=5,
        attack=3,
        health=8,
        creature_types=['Air'],
        rarity='rare',
    ),
    'Yuyan Archers': CardTemplate(
        name='Yuyan Archers',
        abilities=['Attacker', 'EarlyFighter', 'InvincibilityWhileAttacking'],
        cost=3,
        attack=3,
        health=2,
        creature_types=['Fire'],
        rarity='rare',
    ),
    'Man in the Mask': CardTemplate(
        name='Man in the Mask',
        abilities=['Attacker', 'Shield', 'OnRevealDiscard'],
        cost=2,
        attack=3,
        health=1,
        creature_types=['Fire'],
        rarity='common',
    ),
    'Ran and Shaw': CardTemplate(
        name='Ran and Shaw',
        abilities=['Attacker', 'Twinstrike', 'Shield', 'MoreStrengthMeansDoubleDamage'],
        cost=5,
        attack=3,
        health=2,
        creature_types=['Fire'],
        rarity='rare',
    ),
    'June': CardTemplate(
        name='June',
        abilities=['Attacker', 'KillEnemySummonNyla'],
        cost=4,
        attack=5,
        health=4,
        creature_types=['Fire'],
        rarity='rare',
    ),
    'Nyla': CardTemplate(
        name='Nyla',
        abilities=['Attacker'],
        cost=3,
        attack=4,
        health=3,
        creature_types=['Fire'],
        not_in_card_pool=True,
        rarity='common',
    ),
    'Mako': CardTemplate(
        name='Mako',
        abilities=['Attacker', 'DealDoubleDamageAgainstShackled', ('OnKillBuffHealth', 1, 1)],
        cost=2,
        attack=2,
        health=5,
        creature_types=['Fire'],
        rarity='common',
    ),
    'Master Jeong Jeong': CardTemplate(
        name='Master Jeong Jeong',
        abilities=['Shield', ('ShieldedCharactersDealExtraDamage', 2)],
        cost=2,
        attack=1,
        health=2,
        creature_types=['Fire'],
        rarity='common',
    ),
    'Piandao': CardTemplate(
        name='Piandao',
        abilities=['Attacker', 'Shield', 'KillEnemyGainShield'],
        cost=5,
        attack=5,
        health=3,
        creature_types=['Fire'],
        rarity='rare',
    ),
    'P\'li': CardTemplate(
        name='P\'li',
        abilities=['Shield', ('OnRevealPumpCardsInHand', 1, 0)],
        cost=2,
        attack=2,
        health=1,
        creature_types=['Fire'],
        rarity='common',
    ),
    'Fire Lord Azulon': CardTemplate(
        name='Fire Lord Azulon',
        abilities=['Attacker', 'Twinstrike', ('OnRevealPumpAttackers', 2, 0), 'FriendlyAttackersAreInvincibleWhileAttacking'],
        cost=6,
        attack=4,
        health=8,
        creature_types=['Fire'],
        rarity='rare',
    ),
    'Wan': CardTemplate(
        name='Wan',
        abilities=['Attacker', 'Twinstrike', ('OnRevealPumpFriendliesIfFullMatchingLane', 4, 4)],
        cost=5,
        attack=6,
        health=6,
        creature_types=['Avatar'],
        rarity='rare',
    ),
    'Navy Officer': CardTemplate(
        name='Navy Officer',
        abilities=['OnRevealFriendliesMakeBonusAttack'],
        cost=3,
        attack=4,
        health=3,
        creature_types=['Fire'],
        rarity='common',
    ),
    'Dragon Bird Spirit': CardTemplate(
        name='Dragon Bird Spirit',
        abilities=['Attacker', ('DeathMoveCharactersHereAndPumpThem', 3, 3)],
        cost=6,
        attack=5,
        health=5,
        creature_types=[],
        rarity='rare',
    ),
}

def get_random_card_template_of_rarity(rarity: str) -> CardTemplate:
    return random.choice([card for card in CARD_TEMPLATES.values() if card.rarity == rarity and not card.not_in_card_pool])


def get_sample_card_templates_of_rarity(rarity: str, n: int) -> list[CardTemplate]:
    return random.sample([card for card in CARD_TEMPLATES.values() if card.rarity == rarity and not card.not_in_card_pool], n)

