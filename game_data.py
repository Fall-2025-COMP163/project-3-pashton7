"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    quest_dict = {}
    if os.path.exists(filename):
        with open(filename, "r") as file:
            data = file.read()
            quest_dict = parse_quest_block(data)
            validate_quest_data(quest_dict)
            return quest_dict
        raise CorruptedDataError
    else:
        raise MissingDataFileError
                


def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle same exceptions as load_quests
    item_dict = {}
    if os.path.exists(filename):
        with open(filename, "r") as file:
            data = file.read()

            item_dict = parse_item_block(data)
            validate_item_data(item_dict)
            return item_dict
        raise CorruptedDataError
    else:
        raise MissingDataFileError

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    required_keys = ["title", "description", "reward_xp", "reward_gold", "required_level", "prerequisite"]
    for keys in quest_dict:
        for item in quest_dict[keys]:
            if not required_keys.count(item) > 0:
                raise InvalidDataFormatError
    return True

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    required_keys = ["name", "description", "type", "effect", "cost"]
    valid_type = ["weapon", "armor", "consumable"]
    for keys in item_dict:
        for item in item_dict[keys]:
            if not required_keys.count(item) > 0:
                raise InvalidDataFormatError
            if item == "type":
                if not valid_type.count(item_dict[keys][item]) > 0:
                    raise InvalidDataFormatError
    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    try:
        if not os.path.exists("data/"):
            os.mkdir("data")
        if not os.path.exists("data/quests.txt"):
            os.mkdir("data/quests.txt")
        if not os.path.exists("data/items.txt"):
            os.mkdir("data/items.txt")
    except Exception as err:
        print(f"Error: {err}")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    quest_dict = {}
    split_data = lines.split("\n")
    current_key = None
    for line in split_data:
        if line == "":
            continue
        line_split = line.split(":")
        if len(line_split) < 2:
            raise InvalidDataFormatError
        key = line_split[0].lower()
        val = line_split[1].strip()
        if key == "quest_id":
            current_key = val
            quest_dict[current_key] = {}
        else:
            quest_dict[current_key][key] = val
    return quest_dict
            

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    item_dict = {}
    split_data = lines.split("\n")
    current_key = None
    for line in split_data:
        if line == "":
            continue
        line_split = line.split(":")
        key = line_split[0].lower()
        val = line_split[1].strip()
        if key == "item_id":
            current_key = val
            item_dict[current_key] = {}
        else:
            item_dict[current_key][key] = val
    return item_dict

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    create_default_data_files()
    
    # Test loading quests
    try:
         quests = load_quests()
         print(f"Loaded {len(quests)} quests")
    except MissingDataFileError:
         print("Quest file not found")
    except InvalidDataFormatError as e:
         print(f"Invalid quest format: {e}")
    
    # Test loading items
    try:
         items = load_items()
         print(f"Loaded {len(items)} items")
    except MissingDataFileError:
         print("Item file not found")
    except InvalidDataFormatError as e:
         print(f"Invalid item format: {e}")

