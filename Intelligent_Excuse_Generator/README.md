# ✨ Intelligent Excuse Generator

An AI-powered, context-aware excuse generation desktop application built with Python and Tkinter.

---

## 📌 Project Overview

The Intelligent Excuse Generator is an AI-driven system designed to provide context-aware, highly customizable excuses for different scenarios — enhancing user credibility with automated reasoning and supportive proof generation.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🤖 AI-Generated Excuses | Context-based suggestions for Work, School, Social, Family, Personal |
| 🎛️ Scenario Customization | Refine excuses by urgency level and believability score |
| 📄 Proof Generator | AI-generated documents, chat screenshots, and location logs |
| 🚨 Emergency Call & Text | Auto-triggers fake emergency popups or call simulations |
| 😔 Apology Generator | Auto-creates professional or emotional apology messages |
| 🔊 Voice & Text Output | Generates excuses in both written and speech format via gTTS |
| ⭐ History & Favorites | Save and reload frequently used excuses |
| 📅 Auto-Scheduling | Predicts when an excuse might be needed based on past usage patterns |
| 🌍 Multi-Language Support | Excuses available in 11 languages |
| 🏆 Smart Excuse Ranking | AI ranks best excuse based on past effectiveness |

---

## 🗂️ Project Structure

```
intelligent-excuse-generator/
│
├── main.py                  # Entry point — launches the app
├── app.py                   # Main application class (ExcuseGeneratorApp)
├── excuse_engine.py         # Core excuse generation logic & excuse bank
├── emergency.py             # Emergency call/text trigger system
├── proof_generator.py       # Proof & apology generation
├── data_manager.py          # JSON data persistence (history, favorites, patterns)
├── ui_components.py         # UI widgets, styles, header, scrollable window
├── voice_handler.py         # gTTS voice/audio playback via pygame
├── excuse_data.json         # Auto-generated: stores history, favorites, rankings
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/intelligent-excuse-generator.git
cd intelligent-excuse-generator
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
python main.py
```

---

## 📦 Requirements

```
tkinter (built-in)
gtts
pygame
Pillow
```

---

## 🛠️ Technologies Used

- **Python** — Core language
- **Tkinter / ttk** — GUI framework
- **gTTS (Google Text-to-Speech)** — Voice output
- **pygame** — Audio playback
- **Pillow (PIL)** — Image handling for proof generation
- **JSON** — Persistent data storage for history & favorites
- **Threading** — Background emergency monitoring & prediction

---

## 📸 Screenshots

> *(Add screenshots of the app here)*

---

## 🏫 Project Context

Developed as an **AI Capstone Project** under **Launchzed**, demonstrating applied AI concepts including NLP-based text generation, behavioral pattern recognition, multi-language support, and automated alert systems.

---

## 📄 License

This project is for educational purposes only.
