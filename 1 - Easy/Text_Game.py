def adventure_game():
    print("Welcome to the Adventure Game!")
    print("You find yourself at the entrance of a dark forest. Do you enter?")
    choice = input("Enter Yes or No: ").lower()

    if choice == "yes":
        print("You encounter a dragon! Do you fight or run?")
        choice = input("Enter Fight or Run: ").lower()
        if choice == "fight":
            print("Brave! You defeated the dragon and found a treasure.")
        else:
            print("Good choice. Better safe than sorry!")
    else:
        print("You stay safe but miss an adventure.")

    print("Game Over.")

# Start the game
adventure_game()
