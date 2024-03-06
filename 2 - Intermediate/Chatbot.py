import random
import nltk
from nltk.chat.util import Chat, reflections

# Customizing the chat pairs and reflections
pairs = [
    [r'hi|hello', ['Hello!', 'Hi there!']],
    [r'how are you?', ['I am doing well, how about you?', 'I am fine, thanks for asking.']],
    [r'(.*) your name?', ['I am a chatbot created by OpenAI.']],
    [r'(.*) created you?', ['I was created by an amazing programmer using Python and NLTK.']],
    [r'quit', ['Goodbye!', 'Have a nice day!']]
]

def chatbot():
    print('Hi, I\'m the chatbot. Type "quit" to leave.')
    nltk_chat = Chat(pairs, reflections)
    nltk_chat.converse()

# Example usage
chatbot()
