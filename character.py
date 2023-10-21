import random
from card_template import CardTemplate
from card_templates_list import CARD_TEMPLATES
from utils import generate_unique_id, on_reveal_animation
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from lane import Lane
    from game_state import GameState


class Character:
    def __init__(self, template: CardTemplate, lane: 'Lane', owner_number: int, owner_username: str):
        self.id = generate_unique_id()
        self.template = template
        self.current_health = template.health
        self.max_health = template.health
        self.current_attack = template.attack
        self.shackled_turns = 0
        self.has_attacked = False
        self.owner_number = owner_number
        self.owner_username = owner_username
        self.lane = lane
        self.new = True
        self.escaped_death = False
        self.did_on_reveal = False
        self.did_end_of_turn = False
        self.silenced = False

    def is_defender(self):
        return self.has_ability('Defender')
    
    def is_attacker(self):
        return self.has_ability('Attacker') or self.lane.lane_reward.effect[0] == 'charactersHereFightAsAttackers'
    
    def has_ability(self, ability_name):
        return any([ability_name == ability.name for ability in self.template.abilities]) and not self.silenced

    def number_of_ability(self, ability_name) -> int:
        ability = [ability for ability in self.template.abilities if ability.name == ability_name][0]
        assert ability.number is not None
        return ability.number

    def number_2_of_ability(self, ability_name) -> int:
        ability = [ability for ability in self.template.abilities if ability.name == ability_name][0]
        assert ability.number_2 is not None
        return ability.number_2
    
    def creature_type_of_ability(self, ability_name) -> str:
        ability = [ability for ability in self.template.abilities if ability.name == ability_name][0]
        assert ability.creature_type is not None
        return ability.creature_type

    def compute_damage_to_deal(self, damage_by_player: dict[int, int], is_tower_attack: bool = False, starting_current_attack: Optional[int] = None):
        multiplier = 2 if self.has_ability('DoubleTowerDamage') and is_tower_attack else 1
        extra_for_losing = self.number_of_ability('DealMoreDamageWhenLosing') if self.has_ability('DealMoreDamageWhenLosing') and damage_by_player[1 - self.owner_number] > damage_by_player[self.owner_number] else 0
        base_attack = starting_current_attack if starting_current_attack is not None else self.current_health if self.has_ability('DealDamageEqualToCurrentHealth') else self.current_attack
        damage_dealt = (base_attack + extra_for_losing) * multiplier
        return damage_dealt

    def deal_tower_damage(self, attacking_player: int, defending_characters: list['Character'], damage_by_player: dict[int, int], lane_number: int, log: list[str], animations: list, game_state: 'GameState'):
        damage_dealt = self.compute_damage_to_deal(damage_by_player, is_tower_attack=True)
        damage_by_player[self.owner_number] += damage_dealt
        if self.has_ability('OnTowerAttackDealMassDamage'):
            for character in defending_characters:
                character.current_health -= self.number_of_ability('OnTowerAttackDealMassDamage')
                log.append(f"{self.owner_username}'s {self.template.name} dealt 2 damage to {character.owner_username}'s {character.template.name} in Lane {lane_number + 1}. "
                            f"{character.template.name}'s health is now {character.current_health}.")
        log.append(f"{self.owner_username}'s {self.template.name} dealt {damage_dealt} damage to the enemy player in Lane {lane_number + 1}.")
        if self.has_ability('OnTowerAttackDrawCard'):
            game_state.draw_random_card(attacking_player)
            log.append(f"{self.owner_username}'s {self.template.name} drew a random card.")
        if self.has_ability('OnDamageTowerPumpTeam'):
            for character in self.lane.characters_by_player[self.owner_number]:
                if character.id != self.id:
                    character.current_attack += self.number_of_ability('OnDamageTowerPumpTeam')
                    character.current_health += self.number_2_of_ability('OnDamageTowerPumpTeam')
                    character.max_health += self.number_2_of_ability('OnDamageTowerPumpTeam')
                    log.append(f"{self.owner_username}'s {self.template.name} pumped {character.owner_username}'s {character.template.name}.")

        if self.has_ability('OnTowerDamageGainMana'):
            game_state.mana_by_player[self.owner_number] += 1
            log.append(f"{self.owner_username}'s {self.template.name} gained 1 mana.")

        try:
            attacking_character_array_index = [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id)
        except Exception:
            print('Attacking character not found')
            attacking_character_array_index = None

        animations.append({
                    "event_type": "TowerDamage",
                    'data': {
                        "lane": lane_number,
                        "acting_player": self.owner_number,
                        "from_character_index": attacking_character_array_index,
                    }, 
                    'game_state': game_state.to_json()})

        self.lane.maybe_give_lane_reward(attacking_player, game_state, log, animations)


    def attack(self, attacking_player: int, 
               damage_by_player: dict[int, int], 
               defending_characters: list['Character'], 
               lane_number: int,
               log: list[str],
               animations: list,
               game_state: 'GameState',
               do_not_set_has_attacked: bool = False):
        if not do_not_set_has_attacked:
            self.has_attacked = True
        is_attacker = self.is_attacker()
        defenders = [character for character in defending_characters if character.is_defender() and character.can_fight()]
        if len(defenders) == 0 and not is_attacker:
            self.deal_tower_damage(attacking_player, defending_characters, damage_by_player, lane_number, log, animations, game_state)
        else:
            if len(defenders) == 0:
                if len(defending_characters) > 0:
                    target_character = random.choice(defending_characters)
                else:
                    target_character = None
            else:
                target_character = random.choice(defenders)
            if target_character is not None:
                self.fight(target_character, lane_number, log, animations, game_state)
            if is_attacker:
                self.deal_tower_damage(attacking_player, defending_characters, damage_by_player, lane_number, log, animations, game_state)
        
        if self.has_ability('SwitchLanesAfterAttacking'):
            self.switch_lanes(log, animations, game_state)

        if self.has_ability('OnAttackDoubleAttack'):
            self.current_attack *= 2

    def punch(self, defending_character: 'Character', lane_number: int, log: list[str], animations: list, game_state: 'GameState',
              starting_current_attack: Optional[int] = None):
        if self.has_ability('Deathtouch'):
            defending_character.current_health = 0
            log.append(f"{self.owner_username}'s {self.template.name} deathtouched {defending_character.owner_username}'s {defending_character.template.name}.")
        elif self.has_ability('DoNotDamageEnemyCharacters'):
            return
        else:
            damage_to_deal = self.compute_damage_to_deal(self.lane.damage_by_player, starting_current_attack=starting_current_attack)
            defending_character.sustain_damage(damage_to_deal, log, animations, game_state, suppress_trigger=self.has_ability('OnDamageCharacterSilenceIt') and damage_to_deal > 0)
            log.append(f"{self.owner_username}'s {self.template.name} dealt {damage_to_deal} damage to the enemy {defending_character.template.name} in Lane {lane_number + 1}. "
                        f"{defending_character.template.name}'s health is now {defending_character.current_health}.")

            if damage_to_deal > 0 and self.has_ability('OnDamageCharacterSilenceIt'):
                defending_character.silence(self, log, animations, game_state, do_not_animate=True)


        if defending_character.current_health <= 0 and self.has_ability('OnKillBuffHealth'):
            self.current_attack += self.number_of_ability('OnKillBuffHealth')
            self.current_health += self.number_2_of_ability('OnKillBuffHealth')
            self.max_health += self.number_2_of_ability('OnKillBuffHealth')

        if defending_character.has_ability('OnSurviveDamagePump') and defending_character.current_health > 0:
            defending_character.current_attack += defending_character.number_of_ability('OnSurviveDamagePump')
            defending_character.current_health += defending_character.number_2_of_ability('OnSurviveDamagePump')
            defending_character.max_health += defending_character.number_2_of_ability('OnSurviveDamagePump')
            log.append(f"{defending_character.owner_username}'s {defending_character.template.name} got +{defending_character.number_of_ability('OnSurviveDamagePump')}/+{defending_character.number_2_of_ability('OnSurviveDamagePump')} for surviving damage.")

    def sustain_damage(self, damage: int, log: list[str], animations: list, game_state: 'GameState', suppress_trigger: bool = False):
        self.current_health -= damage

        if suppress_trigger:
            return

        if self.current_health > 0:
            if self.has_ability('OnSurviveDamagePump'):
                self.current_attack += self.number_of_ability('OnSurviveDamagePump')
                self.current_health += self.number_2_of_ability('OnSurviveDamagePump')
                self.max_health += self.number_2_of_ability('OnSurviveDamagePump')
                log.append(f"{self.owner_username}'s {self.template.name} got +{self.number_of_ability('OnSurviveDamagePump')}/+{self.number_2_of_ability('OnSurviveDamagePump')} for surviving damage.")
                self.on_trigger_survive_ability(log, animations, game_state)

            if self.has_ability('OnSurviveDrawCard'):
                game_state.draw_random_card(self.owner_number)
                log.append(f"{self.owner_username}'s {self.template.name} drew a random card.")
                self.on_trigger_survive_ability(log, animations, game_state)
            
            if self.has_ability('OnSurviveGainMana'):
                game_state.mana_by_player[self.owner_number] += 1
                log.append(f"{self.owner_username}'s {self.template.name} gained 1 mana.")
                self.on_trigger_survive_ability(log, animations, game_state)

    def on_trigger_survive_ability(self, log: list[str], animations: list, game_state: 'GameState'):
        for character in self.lane.characters_by_player[self.owner_number]:
            if character.has_ability('OnTriggerSurvivePumpSelf'):
                character.current_attack += character.number_of_ability('OnTriggerSurvivePumpSelf')
                character.current_health += character.number_2_of_ability('OnTriggerSurvivePumpSelf')
                character.max_health += character.number_2_of_ability('OnTriggerSurvivePumpSelf')
                log.append(f"{character.owner_username}'s {character.template.name} got +{character.number_of_ability('OnTriggerSurvivePumpSelf')}/+{character.number_2_of_ability('OnTriggerSurvivePumpSelf')} for {self.owner_username}'s {self.template.name} surviving damage.")
            if character.has_ability('OnTriggerSurvivePump'):
                self.current_attack += character.number_of_ability('OnTriggerSurvivePump')
                self.current_health += character.number_2_of_ability('OnTriggerSurvivePump')
                self.max_health += character.number_2_of_ability('OnTriggerSurvivePump')
                log.append(f"{self.owner_username}'s {self.template.name} got +{character.number_of_ability('OnTriggerSurvivePump')}/+{character.number_2_of_ability('OnTriggerSurvivePump')} for surviving damage.")

    def fight(self, defending_character: 'Character', lane_number: int, log: list[str], animations: list, game_state: 'GameState'):
        defender_starting_current_attack = defending_character.current_health if defending_character.has_ability('DealDamageEqualToCurrentHealth') else defending_character.current_attack
        self.punch(defending_character, lane_number, log, animations, game_state)
        if not self.has_ability('InvincibilityWhileAttacking'):
            defending_character.punch(self, lane_number, log, animations, game_state, starting_current_attack=defender_starting_current_attack)

        animations.append({
                        "event_type": "CharacterAttack",
                        "data": {
                            "lane": lane_number,
                            "acting_player": self.owner_number,
                            "from_character_index": [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id),
                            "to_character_index": [c.id for c in self.lane.characters_by_player[1 - self.owner_number]].index(defending_character.id),                            
                        },
                        "game_state": game_state.to_json(),
                    })

        if defending_character.current_health <= 0 and self.has_ability('OnKillSwitchLanes'):
            self.switch_lanes(log, animations, game_state)

    def can_fight(self):
        return self.current_health > 0


    def can_attack(self):
        return self.can_fight() and not self.has_attacked and self.shackled_turns == 0 and self.current_attack > 0


    def switch_lanes(self, log: list[str], animations: list, game_state: 'GameState', lane_number: Optional[int] = None, and_fully_heal_if_switching: bool = False) -> bool:
        original_spot_array_index = [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id)
        original_lane_number = self.lane.lane_number

        if lane_number is None:
            target_lane = game_state.find_random_empty_slot_in_other_lane(self.lane.lane_number, self.owner_number)
        else:
            target_lane = game_state.lanes[lane_number]
            if len(target_lane.characters_by_player[self.owner_number]) >= 4:
                return False

        if target_lane is None:
            return False

        self.lane.characters_by_player[self.owner_number] = [character for character in self.lane.characters_by_player[self.owner_number] if character.id != self.id]
        if and_fully_heal_if_switching:
            self.fully_heal()
        if self.current_health <= 0:
            return False

        target_lane.characters_by_player[self.owner_number].append(self)
        self.lane = target_lane

        animations.append(
            {
                "event_type": "CharacterSwitchLanes",
                "data": {
                    "acting_player": self.owner_number,
                    "from_character_index": original_spot_array_index,
                    "to_character_index": [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id),
                    "lane": original_lane_number,
                    "to_lane": self.lane.lane_number,
                },
                "game_state": game_state.to_json(),
            }
        )

        # pump friendly characters with CharacterMovesHerePumps ability
        for character in target_lane.characters_by_player[self.owner_number]:
            if character.has_ability('CharacterMovesHerePumps') and character.id != self.id:
                character.current_attack += character.number_of_ability('CharacterMovesHerePumps')
                character.current_health += character.number_2_of_ability('CharacterMovesHerePumps')
                character.max_health += character.number_2_of_ability('CharacterMovesHerePumps')

            if character.has_ability('CharacterMovesHereThatCharacterPumps') and character.id != self.id:
                self.current_attack += character.number_of_ability('CharacterMovesHereThatCharacterPumps')
                self.current_health += character.number_2_of_ability('CharacterMovesHereThatCharacterPumps')
                self.max_health += character.number_2_of_ability('CharacterMovesHereThatCharacterPumps')

            if character.has_ability('OnCharacterMoveHereMakeSpirit') and character.id != self.id:
                lane_to_spawn_in = game_state.find_random_empty_slot_in_other_lane(self.lane.lane_number, self.owner_number)
                if lane_to_spawn_in is not None:
                    character = Character(CARD_TEMPLATES['Spirit'], lane_to_spawn_in, self.owner_number, game_state.usernames_by_player[self.owner_number])
                    lane_to_spawn_in.characters_by_player[self.owner_number].append(character)
                
            if character.has_ability('OnCharacterMoveHereShackle') and character.id != self.id:
                random_enemy_character = self.lane.get_random_enemy_character(self.owner_number, exclude_characters=lambda c: c.shackled_turns > 0)
                if random_enemy_character is not None:
                    random_enemy_character.shackle(character, log, animations, game_state)

        return True
    

    def fully_heal(self):
        if self.current_health == self.max_health:
            return
        self.current_health = self.max_health

        # pump friendly characters with the PumpOnFriendlyHeal ability
        for character in self.lane.characters_by_player[self.owner_number]:
            if character.has_ability('PumpOnFriendlyHeal'):
                if character.id != self.id:
                    self.current_attack += character.number_of_ability('PumpOnFriendlyHeal')
                    self.current_health += character.number_2_of_ability('PumpOnFriendlyHeal')
                    self.max_health += character.number_2_of_ability('PumpOnFriendlyHeal')

            if character.has_ability('OnFriendlyHealPumpMyself'):
                if character.id != self.id:
                    character.current_attack += character.number_of_ability('OnFriendlyHealPumpMyself')
                    character.current_health += character.number_2_of_ability('OnFriendlyHealPumpMyself')
                    character.max_health += character.number_2_of_ability('OnFriendlyHealPumpMyself')


    def roll_turn(self, log: list[str], animations: list, game_state: 'GameState'):
        self.new = False

        if self.shackled_turns > 0:
            log.append(f"{self.owner_username}'s {self.template.name} is shackled for {self.shackled_turns} more turns.")
            self.shackled_turns -= 1


    def do_end_of_turn(self, log: list[str], animations: list, game_state: 'GameState'):
        if self.did_end_of_turn:
            return
        if self.has_ability('EndOfTurnFullHeal'):
            self.fully_heal()
            log.append(f"{self.owner_username}'s {self.template.name} healed to full health.")
        
        for character in self.lane.characters_by_player[self.owner_number]:
            if character.has_ability('EndOfTurnFullHealForAllFriendlies') and character.id != self.id:
                self.fully_heal()
                log.append(f"{self.owner_username}'s {self.template.name} healed to full health.")
        
        if self.lane.lane_reward.effect[0] == 'healAllCharactersHereAtEndOfTurn':
            self.fully_heal()
            log.append(f"{self.owner_username}'s {self.template.name} healed to full health.")

        if self.has_ability('SwitchLanesAtEndOfTurn'):
            self.switch_lanes(log, animations, game_state)

        self.has_attacked = False
        self.did_end_of_turn = True


    def silence(self, silencing_character: 'Character', log: list[str], animations: list, game_state: 'GameState', do_not_animate: bool = False):
        self.silenced = True
        self.current_attack = self.template.attack
        self.current_health = min(self.template.health, self.current_health)
        self.max_health = self.template.health

        log.append(f"{silencing_character.owner_username}'s {silencing_character.template.name} silenced {self.owner_username}'s {self.template.name}.")
        if not do_not_animate:
            animations.append({
                "event_type": "CharacterSilence",
                "data": {
                    "lane": self.lane.lane_number,
                    "acting_player": 1 - self.owner_number,
                    "from_character_index": [c.id for c in self.lane.characters_by_player[1 - self.owner_number]].index(silencing_character.id),
                    "to_character_index": [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id),
                },
                "game_state": game_state.to_json(),
            })


    def shackle(self, shackling_character: 'Character', log: list[str], animations: list, game_state: 'GameState', do_not_animate: bool = False):
        num_enemy_characters_that_increase_shackled_turns = len([character for character in self.lane.characters_by_player[1 - self.owner_number] if character.has_ability('ShacklesLastExtraTurn')])
        total_damage_from_shackles = sum([character.number_of_ability('ShacklesDealDamage') for character in self.lane.characters_by_player[1 - self.owner_number] if character.has_ability('ShacklesDealDamage')])
        cards_drawn_from_shackles = len([character for character in self.lane.characters_by_player[1 - self.owner_number] if character.has_ability('OnShackleDrawCard')])

        self.shackled_turns += 1 + num_enemy_characters_that_increase_shackled_turns
        self.current_health -= total_damage_from_shackles

        for _ in range(cards_drawn_from_shackles):
            game_state.draw_random_card(1 - self.owner_number)

        for character in self.lane.characters_by_player[1 - self.owner_number]:
            if character.has_ability('OnShacklePumpSelf'):
                character.current_attack += character.number_of_ability('OnShacklePumpSelf')
                character.current_health += character.number_2_of_ability('OnShacklePumpSelf')
                character.max_health += character.number_2_of_ability('OnShacklePumpSelf')

        log.append(f"{shackling_character.owner_username}'s {shackling_character.template.name} shackled {self.owner_username}'s {self.template.name}.")
        if not do_not_animate:
            animations.append({
                "event_type": "CharacterShackle",
                "data": {
                    "lane": self.lane.lane_number,
                    "acting_player": 1 - self.owner_number,
                    "from_character_index": [c.id for c in self.lane.characters_by_player[1 - self.owner_number]].index(shackling_character.id),
                    "to_character_index": [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id),
                },
                "game_state": game_state.to_json(),                
            })

    def do_all_on_reveal(self, log: list[str], animations: list, game_state: 'GameState'):
        self.do_very_early_on_reveal(log, animations, game_state)
        self.do_early_on_reveal(log, animations, game_state)
        self.do_regular_on_reveal(log, animations, game_state)
        self.do_late_on_reveal(log, animations, game_state)
        self.did_on_reveal = True

    def do_very_early_on_reveal(self, log: list[str], animations: list, game_state: 'GameState'):
        if self.did_on_reveal:
            return

        attack_buffs = [character.number_of_ability('PumpCharactersPlayedHere') for character in self.lane.characters_by_player[self.owner_number] if character.has_ability('PumpCharactersPlayedHere') and character.id != self.id]
        defense_buffs = [character.number_2_of_ability('PumpCharactersPlayedHere') for character in self.lane.characters_by_player[self.owner_number] if character.has_ability('PumpCharactersPlayedHere') and character.id != self.id]
        element_specific_attack_buffs = [character.number_of_ability('PumpFriendlyCharactersOfElementPlayedHere') for character in self.lane.characters_by_player[self.owner_number] 
                                            if (character.has_ability('PumpFriendlyCharactersOfElementPlayedHere') and (character.creature_type_of_ability('PumpFriendlyCharactersOfElementPlayedHere') in self.template.creature_types or 'Avatar' in self.template.creature_types)) and character.id != self.id]
        element_specific_defense_buffs = [character.number_2_of_ability('PumpFriendlyCharactersOfElementPlayedHere') for character in self.lane.characters_by_player[self.owner_number] 
                                            if (character.has_ability('PumpFriendlyCharactersOfElementPlayedHere') and (character.creature_type_of_ability('PumpFriendlyCharactersOfElementPlayedHere') in self.template.creature_types or 'Avatar' in self.template.creature_types)) and character.id != self.id]
        
        lane_attack_buff = self.lane.lane_reward.effect[1] if self.lane.lane_reward is not None and self.lane.lane_reward.effect[0] == 'pumpAllCharactersPlayedHere' else 0
        lane_defense_buff = self.lane.lane_reward.effect[2] if self.lane.lane_reward is not None and self.lane.lane_reward.effect[0] == 'pumpAllCharactersPlayedHere' else 0

        self.current_attack += sum(attack_buffs) + sum(element_specific_attack_buffs) + lane_attack_buff  # type: ignore
        self.current_health += sum(defense_buffs) + sum(element_specific_defense_buffs) + lane_defense_buff  # type: ignore
        self.max_health += sum(defense_buffs) + sum(element_specific_defense_buffs) + lane_defense_buff  # type: ignore

        if self.current_attack < 0:
            self.current_attack = 0


    def do_early_on_reveal(self, log: list[str], animations: list, game_state: 'GameState'):
        if self.did_on_reveal:
            return

        if self.new:
            if self.has_ability('OnRevealSilenceRandomEnemy'):
                random_enemy_character = self.lane.get_random_enemy_character(self.owner_number, exclude_characters=lambda c: c.silenced)
                if random_enemy_character is not None:
                    random_enemy_character.silence(self, log, animations, game_state)

            if self.has_ability('OnRevealSilenceAllCharacters'):
                for character in [*self.lane.characters_by_player[1 - self.owner_number], *self.lane.characters_by_player[self.owner_number]]:
                    if character.id != self.id:
                        character.silence(self, log, animations, game_state, do_not_animate=True)
                animations.append(
                    on_reveal_animation(self.lane.lane_number, self.owner_number, [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id), game_state)
                )


    def do_regular_on_reveal(self, log: list[str], animations: list, game_state: 'GameState'):
        if self.did_on_reveal:
            return
        if self.new:
            if self.has_ability('OnRevealShackle'):
                random_enemy_character = self.lane.get_random_enemy_character(self.owner_number, exclude_characters=lambda c: c.shackled_turns > 0)
                if random_enemy_character is not None:
                    random_enemy_character.shackle(self, log, animations, game_state)

            if self.has_ability('OnRevealShackleAllEnemies'):
                for character in self.lane.characters_by_player[1 - self.owner_number]:
                    if character.shackled_turns == 0:
                        character.shackle(self, log, animations, game_state, do_not_animate=True)
                animations.append(
                    on_reveal_animation(self.lane.lane_number, self.owner_number, [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id), game_state)
                )


            if self.has_ability('OnRevealPumpFriends'):
                for character in self.lane.characters_by_player[self.owner_number]:
                    if character.id != self.id:
                        character.current_attack += self.number_of_ability('OnRevealPumpFriends')
                        character.current_health += self.number_2_of_ability('OnRevealPumpFriends')
                        character.max_health += self.number_2_of_ability('OnRevealPumpFriends')
                        log.append(f"{self.owner_username}'s {self.template.name} pumped {character.owner_username}'s {character.template.name}.")
                animations.append(
                    on_reveal_animation(self.lane.lane_number, self.owner_number, [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id), game_state)
                )

            if self.has_ability('OnRevealPumpAttackers'):
                for character in self.lane.characters_by_player[self.owner_number]:
                    if character.is_attacker() and character.id != self.id:
                        character.current_attack += self.number_of_ability('OnRevealPumpAttackers')
                        character.current_health += self.number_2_of_ability('OnRevealPumpAttackers')
                        character.max_health += self.number_2_of_ability('OnRevealPumpAttackers')
                        log.append(f"{self.owner_username}'s {self.template.name} pumped {character.owner_username}'s {character.template.name}.")
                animations.append(
                    on_reveal_animation(self.lane.lane_number, self.owner_number, [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id), game_state)
                )

            if self.has_ability('OnRevealGainMana'):
                number = self.number_of_ability('OnRevealGainMana')
                game_state.mana_by_player[self.owner_number] += number
                log.append(f"{self.owner_username}'s {self.template.name} gained {number} mana.")

            if self.has_ability('HealFriendlyCharacterAndTower'):
                random_friendly_damaged_character = self.get_random_other_friendly_damaged_character()
                if random_friendly_damaged_character is not None:
                    random_friendly_damaged_character.fully_heal()
                    animations.append(
                        {
                            "event_type": "CharacterHeal",
                            "data": {
                                "acting_player": self.owner_number,
                                "lane": self.lane.lane_number,
                                "from_character_index": [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id),
                                "to_character_index": [c.id for c in self.lane.characters_by_player[self.owner_number]].index(random_friendly_damaged_character.id),
                            },
                            "game_state": game_state.to_json(),
                        },
                    )
                self.lane.damage_by_player[1 - self.owner_number] = max(0, self.lane.damage_by_player[1 - self.owner_number] - self.number_of_ability('HealFriendlyCharacterAndTower'))

            if self.has_ability('OnRevealHealAllFriendliesAndTowers'):
                for lane in game_state.lanes:
                    for character in lane.characters_by_player[self.owner_number]:
                        character.fully_heal()
                    lane.damage_by_player[1 - self.owner_number] = max(0, lane.damage_by_player[1 - self.owner_number] - self.number_of_ability('OnRevealHealAllFriendliesAndTowers'))
                animations.append(
                    on_reveal_animation(self.lane.lane_number, self.owner_number, [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id), game_state)
                )

            if self.has_ability('OnRevealLaneFightsFirst'):
                self.lane.additional_combat_priority -= 3

            if self.has_ability('OnRevealFriendliesSwitchLanes'):
                friendlies = self.lane.characters_by_player[self.owner_number][:]
                random.shuffle(friendlies)
                animations.append(
                    on_reveal_animation(self.lane.lane_number, self.owner_number, [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id), game_state)
                )                
                for character in friendlies:
                    if not character.id == self.id:
                        character.switch_lanes(log, animations, game_state)

            if self.has_ability('OnRevealDrawCards'):
                cards_to_draw = self.number_of_ability('OnRevealDrawCards')
                for _ in range(cards_to_draw):
                    game_state.draw_random_card(self.owner_number)

            if self.has_ability('OnRevealDamageSelf'):
                damage_amount = self.number_of_ability('OnRevealDamageSelf')
                self.current_health -= damage_amount
                log.append(f"{self.owner_username}'s {self.template.name} dealt {damage_amount} damage to itself.")
                animations.append(
                    on_reveal_animation(self.lane.lane_number, self.owner_number, [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id), game_state)
                )

            if 'Earth' in self.template.creature_types or 'Avatar' in self.template.creature_types:
                for character in self.lane.characters_by_player[self.owner_number]:
                    if character.has_ability('ShackleOnFriendlyEarth') and character.id != self.id:
                        random_enemy_character = self.lane.get_random_enemy_character(self.owner_number, exclude_characters=lambda c: c.shackled_turns > 0)
                        if random_enemy_character is not None:
                            random_enemy_character.shackle(character, log, animations, game_state)
            
            if self.has_ability('OnRevealPumpFriendlyCharactersOfElement'):
                for character in self.lane.characters_by_player[self.owner_number]:
                    if (self.creature_type_of_ability('OnRevealPumpFriendlyCharactersOfElement') in character.template.creature_types or 'Avatar' in character.template.creature_types) and character.id != self.id:
                        character.current_attack += self.number_of_ability('OnRevealPumpFriendlyCharactersOfElement')
                        character.current_health += self.number_2_of_ability('OnRevealPumpFriendlyCharactersOfElement')
                        character.max_health += self.number_2_of_ability('OnRevealPumpFriendlyCharactersOfElement')
                animations.append(
                    on_reveal_animation(self.lane.lane_number, self.owner_number, [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id), game_state)
                )

            if self.has_ability('OnRevealFillEnemyLaneWithCabbages'):
                while len(self.lane.characters_by_player[1 - self.owner_number]) < 4:
                    cabbage_character = Character(CARD_TEMPLATES['Cabbage'], self.lane, 1 - self.owner_number, game_state.usernames_by_player[1 - self.owner_number])
                    self.lane.characters_by_player[1 - self.owner_number].append(cabbage_character)
                    cabbage_character.do_all_on_reveal(log, animations, game_state)

            if self.has_ability('OnRevealSummonDesna'):
                animations.append(
                    on_reveal_animation(self.lane.lane_number, self.owner_number, [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id), game_state)
                )
                desna_character = Character(CARD_TEMPLATES['Desna'], self.lane, self.owner_number, game_state.usernames_by_player[self.owner_number])
                self.lane.characters_by_player[self.owner_number].append(desna_character)
                desna_character.do_all_on_reveal(log, animations, game_state)

            if self.has_ability('OnRevealStealEnemy'):
                animations.append(
                    on_reveal_animation(self.lane.lane_number, self.owner_number, [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id), game_state)
                )
                if len(self.lane.characters_by_player[self.owner_number]) < 4:
                    random_enemy_character = self.lane.get_random_enemy_character(self.owner_number)
                    if random_enemy_character is not None:
                        starting_character_index = [c.id for c in self.lane.characters_by_player[1 - self.owner_number]].index(random_enemy_character.id)
                        self.lane.characters_by_player[1 - self.owner_number] = [character for character in self.lane.characters_by_player[1 - self.owner_number] if character.id != random_enemy_character.id]
                        self.lane.characters_by_player[self.owner_number].append(random_enemy_character)
                        random_enemy_character.owner_number = self.owner_number
                        random_enemy_character.owner_username = self.owner_username

                        animations.append({
                            'event_type': 'SwitchSides',
                            'data': {
                                "acting_player": 1 - self.owner_number,
                                "lane": self.lane.lane_number,
                                "from_character_index": starting_character_index,
                                "to_character_index": [c.id for c in self.lane.characters_by_player[self.owner_number]].index(random_enemy_character.id),
                            },
                            "game_state": game_state.to_json(),
                        })

            if self.has_ability('OnRevealHealAndPumpSelf'):
                random_friendly_damaged_character = self.get_random_other_friendly_damaged_character()
                if random_friendly_damaged_character is not None:
                    amount_to_heal = random_friendly_damaged_character.max_health - random_friendly_damaged_character.current_health
                    random_friendly_damaged_character.fully_heal()
                    self.current_attack += amount_to_heal
                    self.current_health += amount_to_heal
                    self.max_health += amount_to_heal
                    animations.append(
                        {
                            "event_type": "CharacterHeal",
                            "data": {
                                "acting_player": self.owner_number,
                                "lane": self.lane.lane_number,
                                "from_character_index": [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id),
                                "to_character_index": [c.id for c in self.lane.characters_by_player[self.owner_number]].index(random_friendly_damaged_character.id),
                            },
                            "game_state": game_state.to_json(),
                        },
                    )



    def do_late_on_reveal(self, log: list[str], animations: list, game_state: 'GameState'):
        if self.did_on_reveal:
            return        

        if self.has_ability('OnRevealDiscardRandomCardAndDealDamageEqualToCost'):
            if len(game_state.hands_by_player[self.owner_number]) > 0:
                random_card = random.choice(game_state.hands_by_player[self.owner_number])
                game_state.hands_by_player[self.owner_number] = [card for card in game_state.hands_by_player[self.owner_number] if card.id != random_card.id]
                damage_to_deal = random_card.template.cost
                defending_character = self.lane.get_random_enemy_character(self.owner_number)
                if defending_character is not None:
                    defending_character.sustain_damage(damage_to_deal, log, animations, game_state)

                    animations.append({
                        "event_type": "CharacterAttack",
                        "data": {
                            "lane": self.lane.lane_number,
                            "acting_player": self.owner_number,
                            "from_character_index": [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id),
                            "to_character_index": [c.id for c in self.lane.characters_by_player[1 - self.owner_number]].index(defending_character.id),                            
                        },
                        "game_state": game_state.to_json(),
                    })

                    self.lane.process_dying_characters(log, animations, game_state) 

        if self.has_ability('OnRevealDamageToAll'):
            damage_amount = self.number_of_ability('OnRevealDamageToAll')
            for character in [*self.lane.characters_by_player[self.owner_number], *self.lane.characters_by_player[1 - self.owner_number]]:
                character.sustain_damage(damage_amount, log, animations, game_state)
                log.append(f"{self.owner_username}'s {self.template.name} dealt {damage_amount} damage to {character.owner_username}'s {character.template.name} in Lane {self.lane.lane_number + 1}. "
                            f"{character.template.name}'s health is now {character.current_health}.")
            animations.append(
                on_reveal_animation(self.lane.lane_number, self.owner_number, [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id), game_state)
            )
            self.lane.process_dying_characters(log, animations, game_state)

        if self.has_ability('OnRevealBonusAttack'):
            for _ in range(self.number_of_ability('OnRevealBonusAttack')):
                defending_characters = [character for character in self.lane.characters_by_player[1 - self.owner_number] if character.can_fight()]
                self.attack(self.owner_number, self.lane.damage_by_player, defending_characters, self.lane.lane_number, log, animations, game_state, do_not_set_has_attacked=True)
            self.lane.process_dying_characters(log, animations, game_state)

        if self.has_ability('OnRevealAllAttackersMakeBonusAttack'):
            for lane in game_state.lanes:
                for character in lane.characters_by_player[self.owner_number]:
                    if character.is_attacker() and character.id != self.id:
                        defending_characters = [character for character in lane.characters_by_player[1 - self.owner_number] if character.can_fight()]
                        character.attack(self.owner_number, lane.damage_by_player, defending_characters, lane.lane_number, log, animations, game_state, do_not_set_has_attacked=True)                
                lane.process_dying_characters(log, animations, game_state)


        self.did_on_reveal = True


    def get_random_other_friendly_damaged_character(self) -> Optional['Character']:
        friendly_characters = [character for character in self.lane.characters_by_player[self.owner_number] if character.current_health < character.max_health]
        if len(friendly_characters) == 0:
            return None
        else:
            return random.choice(friendly_characters)


    def to_json(self):
        return {
            "id": self.id,
            "template": self.template.to_json(),
            "current_health": self.current_health,
            "shackled_turns": self.shackled_turns,
            "max_health": self.max_health,
            "current_attack": self.current_attack,
            "has_attacked": self.has_attacked,
            "owner_number": self.owner_number,
            "owner_username": self.owner_username,
            "new": self.new,   
            "escaped_death": self.escaped_death,         
            "did_on_reveal": self.did_on_reveal,
            "did_end_of_turn": self.did_end_of_turn,
            "silenced": self.silenced,
            # Can't put lane in here because of infinite recursion
        }


    @staticmethod
    def from_json(json: dict, lane: 'Lane'):
        character = Character(
            template=CardTemplate.from_json(json['template']),
            lane=lane,
            owner_number=json['owner_number'],
            owner_username=json['owner_username'],
        )
        character.id = json['id']
        character.current_health = json['current_health']
        character.shackled_turns = json['shackled_turns']
        character.max_health = json['max_health']
        character.current_attack = json['current_attack']
        character.has_attacked = json['has_attacked']
        character.new = json['new']
        character.escaped_death = json['escaped_death']
        character.did_on_reveal = json['did_on_reveal']
        character.did_end_of_turn = json['did_end_of_turn']
        character.silenced = json['silenced']
        return character