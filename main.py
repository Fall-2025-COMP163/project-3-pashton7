"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice
    print("Select an Option")
    print("1. New Game\n2. Load Game\n3. Exit")
    choice = input("Your Choice (1-3): ")
    return int(choice)

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop
    char_name = input("Character Name: ")
    char_class = input("Character Class (Warrior, Mage, Rogue, Cleric): ")
    try:
        current_character = character_manager.create_character(char_name, char_class)
        character_manager.save_character(current_character)
        game_loop()
    except Exception as err:
        print(f"Error: {err}")
    

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop
    saved_list = character_manager.list_saved_characters()
    choice = None
    if len(saved_list) > 0:
        for char in saved_list:
            print(f"{saved_list[char]}")
        choice = input("Character to load: ")
        try:
            current_character = character_manager.load_character(choice)
            game_loop()
        except CharacterNotFoundError:
            print("Error: Character not found!")
        except SaveFileCorruptedError:
            print("Error: Save file is corrupted!")
    else:
        print("No save files found.")

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action
    while game_running:
        choice = game_menu()
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            game_running = False
        else:
            print("Invalid Choice")
        save_game()

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    # TODO: Implement game menu
    print("Options")
    print("1. View Character Stats\n2. View Inventory\n3. Quest Menu\n4. Explore (Find Battles)\n5. Shop\n6. Save and Quit")
    choice = input("Your Choice (1-6): ")
    return int(choice)

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler
    print("=== Character Stats ===")
    print(f"Name: {current_character['name']}")
    print(f"Class: {current_character['class']}")
    print(f"Level: {current_character['level']}")
    print(f"Health: {current_character['health']}")
    print(f"Strength: {current_character['strength']}")
    print(f"Magic: {current_character['magic']}")
    print(f"Gold: {current_character['gold']}")
    print(f"Experience: {current_character['experience']}")
    quest_handler.display_character_quest_progress(current_character, all_quests)


def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system
    inventory_system.display_inventory(current_character, all_items)
    print("Options:")
    print("1. Use item\n2. Equip weapon\n3. Equip armor\n4. Drop item")
    choice = input("Your choice (1-3): ")
    try:
        choice = int(choice)
        
        if choice == 1:
            choice2 = input("Name of item to use: ")
            inventory_system.use_item(current_character, choice2, all_items)
        elif choice == 2:
            choice3 = input("Name of weapon to equip: ")
            inventory_system.equip_weapon(current_character, choice3, all_items)
        elif choice == 3:
            choice4 = input("Name of armor to equip: ")
            inventory_system.equip_armor(current_character, choice4, all_items)
        elif choice == 4:
            choice5 = input("Name of item to drop: ")
            inventory_system.remove_item_from_inventory(current_character, choice5)
    except Exception as err:
        print(f"Error: {err}")

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler
    print("Quest Menu: ")
    print("1. View Active Quests\n2. View Available Quests\n3. View Completed Quests\n4. Accept Quest\n5. Abandon Quest\n6. Complete Quest (for testing)\n7. Back")
    choice = input("Your choice (1-7): ")
    try:
        choice = int(choice)
        if choice == 1:
            quest_handler.display_quest_list(quest_handler.get_active_quests(current_character, all_quests))
        elif choice == 2:
            quest_handler.display_quest_list(quest_handler.get_available_quests(current_character, all_quests))
        elif choice == 3:
            quest_handler.display_quest_info(quest_handler.get_completed_quests(current_character, all_quests))
        elif choice == 4:
            accept_choice = input("Name of Quest to accept: ")
            quest_handler.accept_quest(current_character, accept_choice, all_quests)
        elif choice == 5:
            abandon_choice = input("Name of Quest to abandon: ")
            quest_handler.abandon_quest(current_character, abandon_choice)
        elif choice == 6:
            complete_choice = input("Name of Quest to complete: ")
            quest_handler.complete_quest(current_character, complete_choice, all_quests)
        else:
            if choice != 7:
                print("Invalid Option")
    except Exception as err:
        print(f"Error: {err}")

def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions
    try:
        enemy = combat_system.get_random_enemy_for_level(current_character['level'])
        battle_results = combat_system.SimpleBattle(current_character, enemy).start_battle()
        if battle_results['winner'] != None:
            print(f"Winner: {battle_results['winner']}")
        else:
            print(f"{current_character['name']} escaped")
        if battle_results['winner'] == 'player':
            print(f"Gold Earned: {battle_results['gold_gained']}")
            print(f"XP Earned: {battle_results['xp_gained']}")
            current_character['experience'] += character_manager.gain_experience(current_character, battle_results['xp_gained'])
            current_character['gold'] += character_manager.add_gold(current_character, battle_results['gold_gained'])
    except Exception as err:
        print(f"Error: {err}")

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system
    print("Available Items: ")
    for item in all_items:
        print(f"{all_items[item]['name']}\n   Cost: {all_items[item]['cost']}   Description: {all_items[item]['description']}")
    print(f"Current Gold: {current_character['gold']}")
    print("Options: ")
    print("1. Buy item\n2. Sell item\n3. Back")
    choice = input("Input choice (1-3): ")
    try:
        choice = int(choice)
        if choice == 1:
            buy_choice = input("Item to buy: ")
            inventory_system.purchase_item(current_character, buy_choice, all_items)
        elif choice == 2:
            sell_choice = input("Item to sell: ")
            inventory_system.sell_item(current_character, sell_choice, all_items)
        else:
            if choice != 3:
                print("Invalid option")
    except Exception as err:
        print(f"Error: {err}")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions
    try:
        character_manager.save_character(current_character)
    except IOError as err:
        print(err)

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()
    try:
        all_quests = game_data.load_quests()
    except MissingDataFileError:
        print("File Missing, try reloading")
        game_data.create_default_data_files()
    except InvalidDataFormatError:
        print("Error: Quest data file is of invalid format")
    
    try:
        all_items = game_data.load_items()
    except MissingDataFileError:
        print("File Missing, try reloading")
        game_data.create_default_data_files()
    except InvalidDataFormatError:
        print("Error: Item data file is of invalid format")

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False
    print(f"{current_character['name']} has died")
    print("Options: ")
    print("1. Revive (100 gold)\n2. Quit")
    choice = input("Your choice (1-2): ")
    try:
        choice = int(choice)
        if choice == 1:
            try:
                character_manager.add_gold(current_character, -100)
                character_manager.revive_character(current_character)
            except ValueError:
                print("Insufficient Funds")
        elif choice == 2:
            game_running = False
        else:
            print("Invalid Option")
    except Exception as err:
        print(f"Error: {err}")

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

