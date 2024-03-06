import random

def random_quote():
    quotes = [
        "Life is what happens when you're busy making other plans. - John Lennon",
        "The greatest glory in living lies not in never falling, but in rising every time we fall. - Nelson Mandela",
        "The way to get started is to quit talking and begin doing. - Walt Disney",
        "Your time is limited, don't waste it living someone else's life. - Steve Jobs"
    ]
    return random.choice(quotes)

# Test the function
print(random_quote())
