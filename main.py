import game_functions

def main():
    while True:
        game_functions.look(game_functions.current_room)

        # Get the player's command and split into action and arguments
        command = input("\nEnter a command (look, go [direction], take [item], drop [item], use [item], inventory, solve, save, load, quit): ").split()

        if len(command) == 0:
            print("Invalid command. Please try again.")
            continue

        action = command[0]  # The first word is the action

        # Handling various actions
        if action == "quit":
            print("Thanks for playing!")
            break
        elif action == "go" and len(command) > 1:
            game_functions.df("go", command[1])  # Second word is the direction
        elif action == "take" and len(command) > 1:
            game_functions.df("take", " ".join(command[1:]))  # Join the remaining words as the item
        elif action == "drop" and len(command) > 1:
            game_functions.df("drop", " ".join(command[1:]))  # Join the remaining words as the item
        elif action == "use" and len(command) > 1:
            game_functions.df("use", " ".join(command[1:]))  # Join the remaining words as the item to use
        elif action == "inventory":
            game_functions.df("inventory")
        elif action == "save":
            game_functions.save_game()  # Save the game state
        elif action == "load":
            game_functions.load_game()  # Load the game state
        elif action == "solve":
            game_functions.df("solve")
        else:
            print("Invalid command. Please try again.")

# Start the game
if __name__ == "__main__":
    main()