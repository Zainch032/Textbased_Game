import json

# Initialize player inventory and starting room
inventory = []
current_room = 'Entrance'

# Load the bank map from the file
with open("bank_map.json", 'r') as f:
    bank_map = json.load(f)

# Core game functions
def df(action, argument=None):
    """Handles core actions like 'look', 'go', 'take', 'drop', 'use', and 'solve'."""
    global current_room

    if action == "look":
        look(current_room)
    elif action == "go":
        go(argument)
    elif action == "take":
        take(argument)
    elif action == "drop":
        drop(argument)
    elif action == "use":
        use_item(argument)
    elif action == "inventory":
        show_inventory()
    elif action == "solve":
        solve_puzzle()
    else:
        print("Invalid command. Please try again.")

# Flags for specific actions
wants_to_get_access_card = False  # Flag to check if player wants to get Access card
wants_to_get_permission_letter = False  # Flag to check if player wants to get Permission letter

# Function to move between rooms
def go(direction):
    """Move to a different room if possible."""
    global current_room, wants_to_get_access_card, wants_to_get_permission_letter

    # Check if player tries to move east from Lobby without Access card
    if current_room == 'Lobby' and direction == 'east' and 'Access card' not in inventory:
        print("You need the Access card to enter the Counter.")
        response = input("Do you want to go back to the Entrance to get the Access card? (yes/no): ").lower().strip()

        if response == "yes":
            wants_to_get_access_card = True
            current_room = 'Entrance'  # Move to Entrance
            look(current_room)         # Show description of Entrance
        else:
            print("You decided to stay in the Lobby.")
        return  # Exit function after handling decision

    # Check if player tries to move west from Lobby without Permission letter
    if current_room == 'Lobby' and direction == 'west' and 'letter' not in inventory:
        print("You need the Permission letter to enter the Manager’s Office.")
        response = input("Do you want to go to the Counter to get the Permission letter? (yes/no): ").lower().strip()

        if response == "yes":
            wants_to_get_permission_letter = True
            current_room = 'Counter'  # Move to Counter
            look(current_room)        # Show description of Counter
        else:
            print("You decided to stay in the Lobby.")
        return  # Exit function after handling decision

    # Normal room movement
    if direction in bank_map[current_room]['exits']:
        current_room = bank_map[current_room]['exits'][direction]
        print(f"You moved to {current_room}.")
        look(current_room)  # Automatically display room description
    else:
        print("You can't go that way.")

# Function to take items from the room
def take(item):
    """Take an item from the current room."""
    # All item are in lower case so no need to check or convert them into lower case
    if item in bank_map[current_room]['items']:
        bank_map[current_room]['items'].remove(item)
        inventory.append(item)
        print(f"You took the {item}.")
    else:
        print(f"There is no {item} here.")

# Function to drop items into the room
def drop(item):
    """Drop an item from the inventory into the current room."""
    if item in inventory:
        inventory.remove(item)
        bank_map[current_room]['items'].append(item)
        print(f"You have dropped: {item}")
    else:
        print(f"You don't have {item} in your inventory.")

# Function to use items in the room
def use_item(item):
    """Use an item to interact with the current room."""
    item = item.lower()

    if item == 'pass' and current_room == 'Manager’s Office':
        print("You used the Emergency pass to exit through the emergency door.")
        df("go", "east")  # Assume emergency exit leads east
    elif item == 'gold key' and current_room == 'Locker Room':
        print("You used the Gold Key to open a locker.")
        bank_map['Locker Room']['items'].append('treasure')
        print("A treasure has been revealed!")
    else:
        print(f"You can't use {item} here.")

# Function to display inventory
def show_inventory():
    """Display the player's inventory."""
    if inventory:
        print("Your inventory contains:", ", ".join(inventory))
    else:
        print("Your inventory is empty.")

# Function to solve puzzles
def solve_puzzle():
                                                                          # Some puzzle have reward in it,which can be used item to open room
    if 'puzzle' in bank_map[current_room]:                                # Checking if there is a puzzle in the room
        puzzle = bank_map[current_room]['puzzle']
        print(f"There is a puzzle here: {puzzle['question']}")
        print("Give answer of it")
        answer = input("Your answer: ").strip()

        if answer == puzzle['answer']:
            print("Correct! The puzzle is solved.")
            if 'reward' in puzzle:
                reward = puzzle['reward']
                print(f"You received a reward: {reward}.")
                inventory.append(reward)                                      # Reward automatically added to inventory
            bank_map[current_room]['puzzle'] = None                           # Puzzle is no longer available after solving
        else:
            print("Incorrect answer. Try again or explore more for clues.")
    else:
        print("No puzzle to solve here.")

# Function to look around the room
def look(room):
    """Display the description and items in the current room."""
    print(f"\n{bank_map[room]['description']}")
    print("Items in this room:", ", ".join(bank_map[room]['items']))

# Save and load functions
def save_game(filename="savegame.json"):
    """Save the current game state to a file."""
    game_state = {
        'current_room': current_room,
        'inventory': inventory,
        'bank_map': bank_map
    }

    try:
        with open(filename, 'w') as file:
            json.dump(game_state, file)
        print(f"Game saved to {filename}.")
        print(f"Current location: {current_room}")
        print(f"Inventory: {', '.join(inventory) if inventory else 'None'}")
    except Exception as e:
        print(f"Failed to save game: {e}")

# Function to load a saved game state
def load_game(filename="savegame.json"):
    """Load the game state from a file."""
    global current_room, inventory, bank_map

    try:
        with open(filename, 'r') as file:
            game_state = json.load(file)
            current_room = game_state['current_room']
            inventory = game_state['inventory']
            bank_map = game_state['bank_map']
        print(f"Game loaded from {filename}.")
        print(f"Current location: {current_room}")
        print(f"Inventory: {', '.join(inventory) if inventory else 'None'}")
        look(current_room)  # Show the current room after loading
    except Exception as e:
        print(f"Failed to load game: {e}")

