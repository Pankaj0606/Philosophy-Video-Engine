# 🏛️ Philosophy Video Engine

An automated, cinematic documentary video generator engineered to produce long-form (20–40 minute) philosophical treatises exploring **Indian** (Charvaka, Mimamsa, Advaita, Nyaya) and **Western** (Socrates, Stoicism, Spinoza) traditions.

Orchestrated through **Google Sheets**, the engine conducts structured multi-act research, generates authentic Devanagari Sanskrit quote cards, creates bespoke 1080p artwork via **Flux AI**, and compiles video using **FFmpeg** with multi-axis camera drift and neural speech narration.

---

## 📽️ Key Features

- **Multi-Act Scripting:** Automatically structures documentaries into 5–7 thematic acts (Historical Hook, Epistemology, Metaphysics, Rival Clashes, and Modern Relevance).
- **Artistic Calligraphy Plates:** Automatically designs golden-accented Chapter Intros and Sanskrit/Greek quote cards using *Cinzel* and *Noto Serif Devanagari*.
- **Living Cinematography (No Basic Slideshow Zooms):** Implements varied non-linear camera maneuvers (diagonal dolly drift, wide reveals, push-ins) and warm color grading.
- **Natural Voice Narration:** Integrated with high-fidelity neural voice synthesis (`en-IN-PrabhatNeural`) tuned to a contemplative, documentary cadence.
- **Cloud Task Orchestration:** Reads pending topics directly from Google Sheets (`DSA_Instagram_Automation`) and marks them completed upon export.

---

## 🛠️ Tech Stack

- **Speech Synthesis:** `edge-tts` (Microsoft Neural Voices)
- **Visuals:** Flux.1 via Pollinations API + PIL (Pillow)
- **Video Composition & FX:** FFmpeg
- **Script Generation:** Groq LLM API
- **Task Orchestration:** `gspread` (Google Sheets API)

---

## 🚀 Setup & Local Execution

### 1. Clone & create virtual environment
```bash
git clone https://github.com/Pankaj0606/Philosophy-Video-Engine.git
cd Philosophy-Video-Engine
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt