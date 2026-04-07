<h1 align="center">Emotion Pomodoro</h1>

<p align="center">
  <strong>AI-powered productivity timer that detects fatigue in real time and adapts your breaks</strong>
</p>

<p align="center">
  <a href="#how-it-works">How it works</a> &nbsp;&bull;&nbsp;
  <a href="#tech-stack">Tech Stack</a> &nbsp;&bull;&nbsp;
  <a href="#getting-started">Getting Started</a> &nbsp;&bull;&nbsp;
  <a href="#project-structure">Project Structure</a>
</p>

<br />

## About

**Emotion Pomodoro** is a focus timer that watches your face while you work. Using a pre-trained deep learning model, it detects your emotional state in real time and automatically adjusts your break duration — if you look tired, you get a longer break.

No manual input needed. Just start a session, work, and let the AI handle the rest.

<br />

## How it works

Each frame from your webcam is analyzed by DeepFace — a CNN-based facial emotion recognition model. Raw scores are smoothed using a **30-frame rolling average** to filter out blinks and random expressions.

Fatigue is calculated as: fatigue = sad + angry + fear
If all three are below 20% — fatigue score is 0 (you're focused).
Break duration adapts based on fatigue: break_time = 5 + (fatigue / 100) * 5

Minimum **5 minutes**, maximum **10 minutes**.

<br />

## Features

- **Real-time emotion detection** — webcam analyzed 30 times per second
- **Rolling average smoothing** — stable results, no jitter from single frames
- **Adaptive breaks** — break length adjusts automatically based on fatigue
- **Web interface** — clean dark UI, no installation needed in browser
- **Skip break** — manual override if you feel ready to continue
- **Session reset** — F5 resets everything cleanly

<br />

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **ML Model** | [DeepFace](https://github.com/serengil/deepface) (CNN, pre-trained) |
| **Computer Vision** | [OpenCV](https://opencv.org/) |
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Language** | Python 3.11 |
| **Frontend** | Vanilla JavaScript + HTML/CSS |
| **Parallelism** | Python Threading |

<br />

## Getting Started

### Prerequisites

- Python 3.11+
- Webcam (or virtual camera like Iriun,Camo and etc.)

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/emotion-pomodoro.git
cd emotion-pomodoro

# Install dependencies
pip install deepface tf-keras opencv-python fastapi uvicorn
```

### Run
```bash
uvicorn server:app --reload
```

Open `site.html` in your browser, set work duration and click **Start Session**.

<br />

## Project Structure
emotion_pipeline.py  — webcam capture + DeepFace inference pipeline
pomodoro.py          — pomodoro timer logic and break calculation
server.py            — FastAPI server, connects all modules via threading
site.html           — web interface, polls server every second

<br />

## ML Pipeline
webcam frame
↓
DeepFace.analyze() — CNN inference
↓
30-frame rolling average — smoothing
↓
fatigue score — sad + angry + fear
↓
adaptive break duration


The model runs on every frame in a separate thread, keeping the timer and UI completely unblocked.

<br />

## Author

**Roman Stepanenko** — [@romans0506](https://github.com/romans0506)

<br />

---

<p align="center">
  Built with Python, DeepFace, and a genuine interest in AI.
</p>