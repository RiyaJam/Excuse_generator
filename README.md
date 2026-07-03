# 🎭 Intelligent Excuse Generator

> *An AI-powered, context-aware desktop application that helps you generate the perfect excuse for any situation.*

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-lightgrey?style=flat-square)
![License](https://img.shields.io/badge/License-Educational-green?style=flat-square)

The **Intelligent Excuse Generator** is an advanced Python desktop application designed to provide highly customizable, context-aware excuses. Whether you're running late for work, avoiding a social gathering, or needing a quick out from a family event, this app generates plausible excuses, complete with synthesized voice output and generated "proof."

---

## ✨ Key Features

- 🧠 **Smart Excuse Engine**: Context-based suggestions categorized by Work, School, Social, Family, and Personal scenarios.
- 🎛️ **Scenario Customization**: Fine-tune your excuses by adjusting urgency levels and believability scores.
- 📄 **Proof & Apology Generator**: Automatically creates generated documents, chat screenshots, location logs, and professional apology messages to back up your story.
- 🚨 **Emergency Simulator**: Triggers fake emergency popups or simulates incoming calls to give you an immediate exit strategy.
- 🔊 **Voice Synthesis (Text-to-Speech)**: Uses `gTTS` and `pygame` to read excuses out loud.
- ⭐ **History & Favorites**: Automatically saves your most effective excuses for quick retrieval later.
- 📅 **Usage Analytics & Scheduling**: Predicts when you might need an excuse based on past usage patterns.
- 🌍 **Multi-Language Support**: Generate excuses in over 11 different languages.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have Python 3.8 or higher installed on your system. 

### Installation

1. **Navigate to the project directory** (or clone the repository if you haven't already):
   ```bash
   cd Intelligent_Excuse_Generator
   ```

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *Dependencies include `gTTS`, `pygame`, and `Pillow`.*

3. **Run the application**:
   ```bash
   python main.py
   ```

---

## 🗂️ Project Architecture

The application is modularized for easy maintenance and extensibility:

- **`main.py`** - The entry point that initializes the Tkinter root and launches the app.
- **`app.py`** - The main GUI application class (`ExcuseGeneratorApp`).
- **`excuse_engine.py`** - Core logic for generating, ranking, and retrieving excuses.
- **`proof_generator.py`** - Handles the generation of mock evidence and apologies.
- **`emergency.py`** - System for simulating emergency popups and calls.
- **`voice_handler.py`** - Manages text-to-speech audio playback.
- **`data_manager.py`** - Handles saving and loading persistent data (history, favorites).
- **`ui_components.py`** - Custom UI widgets, styling, and layout definitions.

---

## 🛠️ Built With

- **Python** - Core application logic.
- **Tkinter & ttk** - Native graphical user interface.
- **gTTS (Google Text-to-Speech)** - High-quality voice generation.
- **pygame** - Lightweight audio playback engine.
- **Pillow (PIL)** - Image processing for proof generation.

---

## 🎓 About

This project was developed as an **AI Capstone Project** under **Launchzed**. It demonstrates practical applications of applied AI concepts, including NLP-based text generation, behavioral pattern recognition, audio synthesis, and event-driven GUI programming.

---
*Disclaimer: This project is intended for educational and entertainment purposes only.*
