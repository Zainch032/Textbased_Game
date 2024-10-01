import json

# Initialize player inventory and starting room
inventory = []

player = {
    "current_room" : 'Entrance', 
    "items" : ["pass","letter" , "Access card" , "Gold Key"]
}
with open("bank_map.json", 'r') as f:
    bank_map = json.load(f)

# wants_to_get_access_card = False  # Flag to check if player wants to get Access card
# wants_to_get_permission_letter = False  # Flag to check if player wants to get Permission letter


def move(item_needed , direction):
  try:
    if item_needed != "None":
        if direction in bank_map[player["current_room"]]["exits"]: 
            next_room = bank_map[player["current_room"]]["exits"][direction]
            if item_needed in player["items"]:
                print(player['current_room'], next_room)
                player['current_room'] = next_room
                return
            else:
                print(f"You can't go that way because you do not have {item_needed}!")
        else:
            print("Direction not present")
    else:  
        if direction in bank_map[player["current_room"]]["exits"]:  # Check if direction exists
            next_room = bank_map[player["current_room"]]["exits"][direction]
            print(next_room)
            player['current_room'] = next_room
            return
        else:
            print("No room present!")
  except KeyError as e:
     print(f"Error: Invalid room or exit direction. Details: {e}")

def go(direction):
    try:
        if player['current_room'] == 'Entrance':
            move("Access card", direction)
        elif player["current_room"] == "Lobby":
            move("pass", direction)
        elif player["current_room"] == "Vault":
            move("Gold Key", direction)
        elif player["current_room"] == "Teller Counter":
            move("letter", direction)
        else:
            move(direction, "None")
    except KeyError as e:
        print(f"Error: Invalid room or direction. Details: {e}")
    finally:
        print(f"Current location: {player['current_room']}")

# Function to take items from the room
def take(item):
    """Take an item from the current room."""
    try:
        if item in bank_map[player['current_room']]['items']:
            bank_map[player['current_room']]['items'].remove(item)
            inventory.append(item)
            print(f"You took the {item}.")
        else:
            print(f"There is no {item} here.")
    except KeyError as e:
        print(f"Error while trying to take item: {e}")
    finally:
        print(f"Current inventory: {', '.join(inventory) if inventory else 'Empty'}")
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

