secret_word = "giraffe"
guess = ""
attempt = 0
max_attempts = 5

while guess != secret_word:
    guess = input("Enter your guess: ")
    attempt += 1

    if guess == secret_word:
        print("You Win!")
        break

    if attempt < max_attempts:
        print("Wrong guess. You have", max_attempts - attempt, "guesses left.")
    else:
        print("Game Over!")
        break

