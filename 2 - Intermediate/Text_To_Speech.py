import pyttsx3

def text_to_speech(text, save_as_file=False, filename='output.mp3', gender='male'):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    if gender.lower() == 'female':
        engine.setProperty('voice', voices[1].id)  # Female voice
    else:
        engine.setProperty('voice', voices[0].id)  # Male voice

    engine.setProperty('rate', 125)
    engine.setProperty('volume', 0.8)
    engine.say(text)

    if save_as_file:
        engine.save_to_file(text, filename)
    else:
        engine.runAndWait()

# Example usage
# text_to_speech('Hello, how are you?', save_as_file=True, filename='greeting.mp3', gender='female')
