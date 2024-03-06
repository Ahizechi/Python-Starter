import datetime
import time

def alarm_clock(set_time):
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == set_time:
            print("Alarm! Time is up.")
            break
        time.sleep(30)  # Check every 30 seconds

set_time = "11:17"
alarm_clock(set_time)