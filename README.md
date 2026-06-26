# ✨ Advanced AI Excuse Generator

A feature-rich desktop GUI application built with Python and Tkinter that generates context-aware excuses across multiple scenarios, with multilingual text-to-speech support, emergency simulations, and persistent history tracking.

---

## Features

- **Scenario-Based Excuse Generation** — Choose from categories like Work, Family, Personal, and more. Excuses are selected based on a configurable believability scale.
- **Multilingual Text-to-Speech** — Listen to your excuse read aloud in 11 languages including English, Spanish, French, Japanese, Arabic, Hindi, and more (powered by gTTS and pygame).
- **Excuse History & Favorites** — All generated excuses are saved to a local JSON file. Mark any excuse as a favorite for quick reuse.
- **Emergency Trigger Simulation** — A background monitor detects time patterns (e.g., morning/evening rush hours) and usage intervals, then simulates fake emergency popups or "incoming calls" to help sell your excuse.
- **Artificial Proof Generation** — Generates plausible-sounding supporting documents, chat screenshots, or location logs to accompany your excuse.
- **Apology Generator** — Produces a contextually appropriate apology to pair with any excuse.
- **Scrollable UI** — The main window is fully scrollable to accommodate all features comfortably.
- **Persistent Data** — Excuse history, favorites, effectiveness ratings, and usage patterns are stored in `excuse_data.json` between sessions.

---

## Requirements

- Python 3.8+
- [tkinter](https://docs.python.org/3/library/tkinter.html) (usually bundled with Python)
- [gTTS](https://pypi.org/project/gTTS/) — Google Text-to-Speech
- [pygame](https://pypi.org/project/pygame/) — Audio playback
- [Pillow](https://pypi.org/project/Pillow/) — Image handling

---

## Installation

1. **Clone or download** this repository.

2. **Install dependencies:**

   ```bash
   pip install gtts pygame Pillow
   ```

3. **Run the application:**

   ```bash
   python intelligent_excuse_generator.py
   ```

---

## Usage

1. Launch the app — the main window will open with all controls visible.
2. **Select a scenario** (e.g., Work, Family, Personal) from the dropdown.
3. **Adjust the believability slider** to control how elaborate the excuse is.
4. Click **Generate** to produce an excuse in the output area.
5. Optionally:
   - Click **Read Aloud** to hear the excuse via text-to-speech.
   - Click **Add to Favorites** to save it for later.
   - Click **Generate Proof** to produce supporting documentation text.
   - Double-click any item in the History or Favorites list to reload it.
6. The emergency monitor runs automatically in the background — dismiss any popups as needed.

---

## File Structure

```
├── intelligent_excuse_generator.py   # Main application source
├── excuse_data.json                  # Auto-created; stores history & favorites
└── README.md
```

---

## Configuration & Notes

- `excuse_data.json` is created automatically on first run in the working directory.
- Audio features require an active internet connection for gTTS (text is sent to Google's TTS API).
- The emergency monitor thread checks every 60 seconds and triggers with a random probability — this is intentional behavior.
- Audio playback is initialized with a fallback — a warning notification will appear if the audio system fails to initialize.

---

## Known Limitations

- Proof generation produces placeholder text only (no real document files are created).
- The emergency call simulation shows a popup instead of playing actual audio.
- gTTS requires internet access; offline TTS is not currently supported.

---

## License

This project is provided for entertainment and educational purposes. Use responsibly.
