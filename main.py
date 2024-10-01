import game_functions

# A new menu to from which player can perform actions
def display_menu():
    print("\n" + "="*40)
    print("              GAME MENU")
    print("="*40)
    print("1. Movement:")
    print("   - go ")
    print("     Directions: north, south, east, west")
    print("\n2. Actions:")
    print("   - look: Observe the surroundings")
    print("   - take [item]: Pick up an item")
    print("   - drop [item]: Drop an item from inventory")
    print("   - use [item]: Use an item from inventory")
    print("\n3. Inventory Management:")
    print("   - inventory: Check items in your possession")
    print("\n4. Puzzle/Special Actions:")
    print("   - solve: Solve a puzzle in the room")
    print("\n5. Game Management:")
    print("   - save: Save your current progress")
    print("   - load: Load a saved game")
    print("   - quit: Exit the game")
    print("="*40)

# Call this function before asking for
def main():
    while True:
        game_functions.look(game_functions.player["current_room"])

        # Get the player's command and split into action and arguments
        display_menu()
        command = input("\nEnter a command: ").split()

        if len(command) == 0:
            print("Invalid command. Please try again.")
            continue
        action = command[0]  # The first word is the action

        # Handling various actions
        if action == "quit":
            print("Thanks for playing!")
            break
        elif action == "go" and len(command) > 1:
            print(command[1])
            game_functions.go(command[1])  # Second word is the direction
        elif action == "take" and len(command) > 1:
            game_functions.take(command[1]) # Join the remaining words as the item
        elif action == "drop" and len(command) > 1:
            game_functions.drop(command[1])  # Join the remaining words as the item
        elif action == "use" and len(command) > 1:
            game_functions.use_item(command[1])  # Join the remaining words as the item to use
        elif action == "inventory":
            game_functions.show_inventory()
        elif action == "save":
            game_functions.save_game()  # Save the game state
        elif action == "load":
            game_functions.load_game()  # Load the game state
        elif action == "solve":
            game_functions.df("solve")
        elif action == 'look':
            game_functions.look(game_functions.player["current_room"])
        else:
            print("Invalid command. Please try again.")

# Start the game
if __name__ == "__main__":
    main()