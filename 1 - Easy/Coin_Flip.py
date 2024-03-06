import random

def coin_flip():
    return "Heads" if random.randint(0, 1) == 0 else "Tails"

# Test the function
print(coin_flip())
