import json

# Initialize player inventory and starting room
inventory = []
current_room = 'Entrance'

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

wants_to_get_access_card = False  # Flag to check if player wants to get Access card
wants_to_get_permission_letter = False  # Flag to check if player wants to get Permission letter

def go(direction):
    """Move to a different room if possible."""
    global current_room, wants_to_get_access_card, wants_to_get_permission_letter

    # Check if the player is in the Lobby and tries to go east without the Access card
    if current_room == 'Lobby' and direction == 'east' and 'Access card' not in inventory:
        print("You need the Access card to enter the Counter.")
        
        # Ask if the player wants to go back to the Entrance to get the Access card
        response = input("Do you want to go back to the Entrance to get the Access card? (yes/no): ").lower().strip()
        
        if response == "yes":
            wants_to_get_access_card = True
        else:
            wants_to_get_access_card = False

        # If the player chooses to go to the Entrance
        if wants_to_get_access_card:
            print("You will be taken back to the Entrance to get the Access card.")
            current_room = 'Entrance'  # Move to Entrance
            look(current_room)         # Show description of Entrance
        else:
            print("You decided to stay in the Lobby.")
        
        return  # Exit function after handling decision

    # Check if the player is in the Lobby and tries to go west without the Permission letter
    if current_room == 'Lobby' and direction == 'west' and 'letter' not in inventory:
        print("You need the Permission letter to enter the Manager’s Office.")
        
        # Ask if the player wants to get the letter
        response = input("Do you want to go to the Counter to get the Permission letter? (yes/no): ").lower().strip()
        
        if response == "yes":
            wants_to_get_permission_letter = True
        else:
            wants_to_get_permission_letter = False

        # If the player chooses to go to the Counter for the Permission letter
        if wants_to_get_permission_letter:
            print("You will be taken to the Counter to get the Permission letter.")
            current_room = 'Counter'  # Move to Counter
            look(current_room)        # Show description of Counter
        else:
            print("You decided to stay in the Lobby.")
        
        return  # Exit function after handling decision

    # Regular movement between rooms if all conditions are met
    if direction in bank_map[current_room]['exits']:
        current_room = bank_map[current_room]['exits'][direction]
        print(f"You moved to {current_room}.")
        look(current_room)  # Automatically display room description
    else:
        print("You can't go that way.")

def take(item):
    """Take an item from the current room."""
    item = item.lower().strip("[]")  # Convert input to lowercase and remove brackets
    room_items = [i.lower() for i in bank_map[current_room]['items']]  # Lowercase room items for comparison

    if item in room_items:
        original_item = bank_map[current_room]['items'][room_items.index(item)]  # Get the exact item name
        inventory.append(original_item)
        bank_map[current_room]['items'].remove(original_item)
        print(f"You have taken: {original_item}")
    else:
        print("That item is not here.")

def drop(item):
    """Drop an item from the inventory into the current room."""
    if item in player['items']:
        inventory.remove(item)
        bank_map[current_room]['items'].append(item)
        print(f"You have dropped: {item}")
    else:
        print(f"You don't have {item} in your inventory.")


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

def show_inventory():
    """Display the player's inventory."""
    if inventory:
        print("Your inventory contains:", ", ".join(inventory))
    else:
        print("Your inventory is empty.")

def solve_puzzle():
    """Attempt to solve the current room's puzzle."""
    puzzle = bank_map[current_room].get('puzzle')
    if puzzle:
        answer = input("Solve the puzzle: " + puzzle['question'] + " ").lower().strip()
        if answer == puzzle['answer']:
            print("Correct! The puzzle is solved.")
        else:
            print("Incorrect answer.")
    else:
        print("No puzzle to solve here.")

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
