import time

def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        print(i)
        time.sleep(1)
    print("Time's up!")

seconds = int(60)
countdown_timer(seconds)