import time


class PomodoroTimer:

    def __init__(self,work_minutes = 25):
        self.work_minutes = work_minutes
        self.break_minutes = 5
        self.session = 0

    def get_break_time(self, fatigue_score):
        break_time = 5 + (fatigue_score /100 ) * 5
        return round(break_time)
    
    def work_session(self):
        self.session += 1
        seconds = self.work_minutes * 60
        print (f"\nSession {self.session} has started - work {self.work_minutes} minutes")

        while seconds > 0:
            mins = seconds // 60
            secs = seconds % 60
            print(f"Left: {mins:02d} : {secs:02d}", end = "\r")
            time.sleep(1)
            seconds -= 1

        print("\nTime is up!")


    def break_session(self, fatigue_score = 0):
        break_time = self.get_break_time(fatigue_score)
        print (f"Break {break_time} minutes (Tireness : {round(fatigue_score)}%)")
        seconds = break_time * 60

        while seconds > 0:
            mins = seconds // 60
            secs = seconds % 60
            print(f"Break: {mins:02d} : {secs:02d}", end = "\r")
            time.sleep(1)
            seconds -= 1

        print("\nBreak is up!")


