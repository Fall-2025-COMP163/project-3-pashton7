"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)
import random
# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

combat_active = False

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward
    enemies = {"goblin": {"name": "goblin", "health": 50, "max_health": 50, "strength": 8, "magic":2, "xp_reward": 25, "gold_reward": 10}, "orc": {"name": "orc", "health": 80, "max_health": 80, "strength": 12, "magic":5, "xp_reward": 50, "gold_reward": 25},
               "dragon": {"name": "dragon", "health": 200, "max_health": 200, "strength": 25, "magic":15, "xp_reward": 200, "gold_reward": 100}}
    if enemies.get(enemy_type, False):
        new_enemy = enemies.get(enemy_type)
        return new_enemy
    else:
        raise InvalidTargetError

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    if character_level <= 2:
        return create_enemy('goblin')
    elif character_level > 2 and character_level <= 5:
        return create_enemy('orc')
    else:
        return create_enemy('dragon')

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """

    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        self.character = character
        self.enemy = enemy
        self.turn_count = 0
        self.combat_active = True
       
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        if self.character['health'] <= 0:
            raise CharacterDeadError
        results = {'winner': None, 'xp_gained': 0, 'gold_gained': 0}
        

        while self.combat_active == True:
            display_combat_stats(self.character, self.enemy)
            self.player_turn()
            if self.combat_active == False: 
                break
            results['winner'] = self.check_battle_end()
            self.enemy_turn()
            results['winner'] = self.check_battle_end()

        if results['winner'] == 'player':
            earned_rewards =  get_victory_rewards(self.enemy)
            results['gold_gained'] = earned_rewards['gold']
            results['xp_gained'] = earned_rewards['xp']
        
        return results

    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        if not self.combat_active:
            raise CombatNotActiveError
        print("1. Basic Attack\n2. Special Ability\n3. Try to Run")
        player_choice = input()
        if player_choice == "1":
            self.apply_damage(self.enemy, self.calculate_damage(self.character, self.enemy))
        elif player_choice == "2":
            msg = use_special_ability(self.character, self.enemy)
            display_battle_log(f"{self.character['name']} used " + msg)
        elif player_choice == "3":
            escaped = self.attempt_escape()
            if escaped == True:
                display_battle_log(f"{self.character['name']} successfully escaped")
            else:
                display_battle_log(f"{self.character['name']} failed to escape")
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        if self.combat_active:
            self.apply_damage(self.character, self.calculate_damage(self.enemy, self.character))
        else:
            raise CombatNotActiveError
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        damage = int(attacker['strength'] - (defender['strength'] // 4))
        if damage < 1:
            damage = 1
        return damage
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        target['health'] -= damage
        if target['health'] < 0:
            target['health'] = 0
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        if self.character['health'] <= 0:
            
            return 'enemy'
        elif self.enemy['health'] <= 0:
           
            return 'player'
        else:
            return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        chance = random.randint(0,1)
        if chance == 1:
            self.combat_active = False
            return True
        return False

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    char_class = character['class']
    if char_class == "Warrior":
        return warrior_power_strike(character, enemy)
    elif char_class == "Mage":
        return mage_fireball(character, enemy)
    elif char_class == "Rogue":
       return rogue_critical_strike(character, enemy)
    elif char_class == "Cleric":
        return cleric_heal(character)


def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    dmg = character['strength'] * 2
    enemy['health'] -= dmg
    return f"Power Strike hit for {dmg} damage"

def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
    dmg = character['magic'] * 2
    enemy['health'] -= dmg
    return f"Fireball hit for {dmg} damage"

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    dmg = character['strength'] * 3
    chance = random.randint(0,1)
    if chance == 1:
        enemy['health'] -= dmg
        return f"Critical Strike hit for {dmg} damage"
        
    return "Critical Strike missed"

def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    character['health'] += 30
    if character['health'] > character['max_health']:
        character['health'] = character['max_health']
    return f"Heal for 30 health"

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    if character['health'] > 0 :
        return True
    else:
        return False

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    rewards = {'gold': enemy['gold_reward'], 'xp': enemy['xp_reward']}
    return rewards

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    try:
         goblin = create_enemy("goblin")
         print(f"Created {goblin['name']}")
    except InvalidTargetError as e:
         print(f"Invalid enemy: {e}")
    
    # Test battle
    test_char = {
         'name': 'Hero',
         'class': 'Warrior',
         'health': 120,
         'max_health': 120,
         'strength': 15,
         'magic': 5
    }
    #
    battle = SimpleBattle(test_char, goblin)
    try:
         result = battle.start_battle()
         print(f"Battle result: {result}")
    except CharacterDeadError:
         print("Character is dead!")

