import random

number = random.randrange(1,10)
guess = int(input("Guess a Number between 1 and 10: "))

while number != guess:
    if guess < number:
        print("Too Low, Try again!")
        guess = int(input("Guess a Number between 1 and 100: "))
    elif guess > number:
        print("Too Low, Try again!")
        guess = int(input("Guess a Number between 1 and 100: "))
    else:
        break

print("You Won!")