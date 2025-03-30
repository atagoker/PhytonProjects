import time

# change these as needed
WORK_DURATION = 25
SHORT_BREAK = 5
LONG_BREAK = 15
SESSIONS_BEFORE_LONG_BREAK = 4

def countdown(minutes):
    seconds = minutes * 60
    while seconds:
        mins, secs = divmod(seconds, 60)
        print(f"\r⏳ {mins:02d}:{secs:02d}", end="")
        time.sleep(1)
        seconds -= 1
    print("\r⏰ 00:00 - Time's up!")

def pomodoro_timer():
    session_count = 0
    try:
        while True:
            print(f"\n🍅 Work Session {session_count + 1}")
            countdown(WORK_DURATION)

            session_count += 1
            if session_count % SESSIONS_BEFORE_LONG_BREAK == 0:
                print("\n💤 Take a long break!")
                countdown(LONG_BREAK)
            else:
                print("\n☕ Take a short break!")
                countdown(SHORT_BREAK)
    except KeyboardInterrupt:
        print("\n\n🛑 Pomodoro session ended.")

if __name__ == "__main__":
    pomodoro_timer()
