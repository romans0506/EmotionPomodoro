from fastapi import FastAPI # Web-server framework
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel 
import threading
import time
from emotion_pipeline import EmotionPipeline
from pomodoro import PomodoroTimer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

state = {
    "phase": "working",
    "time_left": "25:00",
    "session": 1,
    "fatigue": 0,
    "emotion": "detecting...",
    "break_info": ""
}

pipeline = EmotionPipeline()
timer = PomodoroTimer(work_minutes=1)
fatigue_score = 0
dominant_emotion = "detecting..."
skip_break = False
is_running = False

def update_fatigue():
    def on_emotion(avg):
        global fatigue_score, dominant_emotion
        sad = avg['sad']
        angry = avg['angry']
        fear = avg['fear']
        if sad < 20 and angry < 20 and fear < 20:
            fatigue_score = 0
        else:
            fatigue_score = sad + angry + fear
        dominant_emotion = max(avg, key=avg.get)
    pipeline.start_background(on_emotion)

    

def run_timer():
    global fatigue_score, skip_break

    while True:
        while not is_running:
            time.sleep(0.5)

        session = 0

        while is_running:
            session += 1
            seconds = timer.work_minutes * 60

            while seconds > 0:
                if not is_running:
                    break
                mins = seconds // 60
                secs = seconds % 60
                state["phase"] = "working"
                state["time_left"] = f"{mins:02d}:{secs:02d}"
                state["session"] = session
                state["fatigue"] = round(fatigue_score)
                state["emotion"] = dominant_emotion
                state["break_info"] = ""
                time.sleep(1)
                seconds -= 1

            if not is_running:
                break

            break_time = 5 + (fatigue_score / 100) * 5
            break_time = round(break_time)
            seconds = break_time * 60

            while seconds > 0:
                if skip_break:
                    skip_break = False
                    break
                if not is_running:
                    break
                mins = seconds // 60
                secs = seconds % 60
                state["phase"] = "break"
                state["time_left"] = f"{mins:02d}:{secs:02d}"
                state["fatigue"] = round(fatigue_score)
                state["emotion"] = dominant_emotion
                state["break_info"] = f"Break: {break_time} min"
                time.sleep(1)
                seconds -= 1

@app.get("/status")
def get_status():
    return state

class WorkTimeRequest(BaseModel):
    minutes: int

@app.post("/start")
def start(request: WorkTimeRequest):
    global is_running
    timer.work_minutes = request.minutes
    is_running = True
    return {"ok": True}

@app.post("/skip")
def skip():
    global skip_break
    skip_break = True
    return {"ok": True}

@app.post("/reset")
def reset():
    global is_running, skip_break
    is_running = False
    skip_break = False
    state["phase"] = "working"
    state["time_left"] = "25:00"
    state["session"] = 1
    state["break_info"] = ""
    return {"ok": True}

@app.on_event("startup")
def startup():
    threading.Thread(target=update_fatigue, daemon=True).start()
    threading.Thread(target=run_timer, daemon=True).start()