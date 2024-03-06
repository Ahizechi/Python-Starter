import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime

def virtual_assistant():
    listener = sr.Recognizer()
    engine = pyttsx3.init()
    engine.setProperty('rate', 130)

    def talk(text):
        engine.say(text)
        engine.runAndWait()

    def take_command():
        try:
            with sr.Microphone() as source:
                print('Listening...')
                voice = listener.listen(source)
                command = listener.recognize_google(voice)
                command = command.lower()
                return command
        except:
            return ''

    def run_assistant():
        command = take_command()
        print(command)
        if 'play' in command:
            song = command.replace('play', '')
            talk(f'Playing {song}')
            pywhatkit.playonyt(song)
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk('Current time is ' + time)
        elif 'search' in command:
            search = command.replace('search', '')
            talk(f'Searching for {search}')
            pywhatkit.search(search)

    run_assistant()

# Example usage
# virtual_assistant()
