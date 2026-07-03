# app.py — Main ExcuseGeneratorApp class (GUI orchestration)

import tkinter as tk
from tkinter import ttk, scrolledtext
from threading import Thread
from datetime import datetime

from excuse_engine import generate_excuse, get_all_scenarios
from proof_generator import generate_proof, generate_apology, get_proof_types
from data_manager import load_excuse_data, save_excuse_data, add_to_history, add_to_favorites
from emergency import EmergencySystem
from voice_handler import VoiceHandler
from ui_components import setup_styles, create_header, create_scrollable_frame, show_notification, create_card


class ExcuseGeneratorApp:
    """
    Main GUI application class for the Intelligent Excuse Generator.
    Orchestrates all modules: excuse engine, proof generator,
    emergency system, voice handler, and data manager.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("✨ Advanced AI Excuse Generator ✨")
        self.root.geometry("1000x700")
        self.root.minsize(800, 500)
        self.root.configure(bg="#f5f5f5")

        # ── Core State ──
        self.last_used_times = []
        self.excuse_history = []
        self.favorite_excuses = []
        self.last_urgency = 5

        # ── Load Data ──
        self.excuse_data = load_excuse_data()

        # ── Modules ──
        self.voice = VoiceHandler()
        self.emergency = EmergencySystem(self.root, self.last_used_times)

        # ── Build UI ──
        setup_styles()
        self._build_ui()

        # ── Start Background Threads ──
        self.emergency.start()
        Thread(target=self._predict_excuse_needs, daemon=True).start()

    # ─────────────────────────────────────────
    # UI Construction
    # ─────────────────────────────────────────

    def _build_ui(self):
        create_header(self.root)
        _, self.scroll_frame = create_scrollable_frame(self.root)
        self._create_controls()
        self._create_output_area()
        self._create_history_favorites()
        self._create_action_buttons()

    def _create_controls(self):
        card = create_card(self.scroll_frame, "⚙️ Configure Your Excuse")

        # Scenario selector
        row1 = tk.Frame(card, bg="white")
        row1.pack(fill=tk.X, pady=4)
        ttk.Label(row1, text="Scenario:", background="white", width=14).pack(side=tk.LEFT)
        self.scenario_var = tk.StringVar(value="Work")
        ttk.Combobox(row1, textvariable=self.scenario_var,
                     values=get_all_scenarios(), state="readonly", width=20).pack(side=tk.LEFT)

        # Urgency slider
        row2 = tk.Frame(card, bg="white")
        row2.pack(fill=tk.X, pady=4)
        ttk.Label(row2, text="Urgency (1–10):", background="white", width=14).pack(side=tk.LEFT)
        self.urgency_var = tk.IntVar(value=5)
        ttk.Scale(row2, from_=1, to=10, variable=self.urgency_var,
                  orient=tk.HORIZONTAL, length=200).pack(side=tk.LEFT)
        ttk.Label(row2, textvariable=self.urgency_var, background="white").pack(side=tk.LEFT, padx=5)

        # Believability slider
        row3 = tk.Frame(card, bg="white")
        row3.pack(fill=tk.X, pady=4)
        ttk.Label(row3, text="Believability:", background="white", width=14).pack(side=tk.LEFT)
        self.believability_var = tk.IntVar(value=5)
        ttk.Scale(row3, from_=1, to=10, variable=self.believability_var,
                  orient=tk.HORIZONTAL, length=200).pack(side=tk.LEFT)
        ttk.Label(row3, textvariable=self.believability_var, background="white").pack(side=tk.LEFT, padx=5)

        # Language selector
        row4 = tk.Frame(card, bg="white")
        row4.pack(fill=tk.X, pady=4)
        ttk.Label(row4, text="Language:", background="white", width=14).pack(side=tk.LEFT)
        self.language_var = tk.StringVar(value="English")
        ttk.Combobox(row4, textvariable=self.language_var,
                     values=self.voice.get_available_languages(),
                     state="readonly", width=20).pack(side=tk.LEFT)

    def _create_output_area(self):
        card = create_card(self.scroll_frame, "📋 Generated Excuse / Output")
        self.output_text = scrolledtext.ScrolledText(
            card, wrap=tk.WORD, height=6,
            font=("Segoe UI", 11), state=tk.NORMAL
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)

    def _create_history_favorites(self):
        frame = tk.Frame(self.scroll_frame, bg="#f5f5f5")
        frame.pack(fill=tk.X, padx=15, pady=8)

        # History
        hist_card = create_card(frame, "🕓 Excuse History")
        self.history_listbox = tk.Listbox(hist_card, height=5, font=("Segoe UI", 9))
        self.history_listbox.pack(fill=tk.BOTH)
        self.history_listbox.bind("<Double-Button-1>", self._load_selected)

        # Favorites
        fav_card = create_card(frame, "⭐ Favorites")
        self.favorites_listbox = tk.Listbox(fav_card, height=5, font=("Segoe UI", 9))
        self.favorites_listbox.pack(fill=tk.BOTH)
        self.favorites_listbox.bind("<Double-Button-1>", self._load_selected)

        # Load saved favorites into listbox
        for fav in self.excuse_data.get("favorites", []):
            self.favorites_listbox.insert(tk.END, fav)

    def _create_action_buttons(self):
        card = create_card(self.scroll_frame, "🎮 Actions")
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(fill=tk.X, pady=5)

        buttons = [
            ("🎲 Generate Excuse", self.generate_excuse),
            ("📄 Generate Proof", self.generate_proof),
            ("😔 Generate Apology", self.generate_apology),
            ("🔊 Speak Excuse", self.speak_excuse),
            ("⭐ Add to Favorites", self.add_to_favorites),
            ("🚨 Trigger Emergency", self.emergency.trigger),
        ]

        for label, cmd in buttons:
            ttk.Button(btn_frame, text=label, command=cmd).pack(
                side=tk.LEFT, padx=5, pady=5
            )

    # ─────────────────────────────────────────
    # Core Actions
    # ─────────────────────────────────────────

    def generate_excuse(self):
        scenario = self.scenario_var.get()
        urgency = self.urgency_var.get()
        believability = self.believability_var.get()

        excuse = generate_excuse(scenario, urgency, believability)
        self._display(excuse)

        # Track usage
        now = datetime.now()
        self.last_used_times.append(now)
        self.excuse_history.append(excuse)
        self.history_listbox.insert(tk.END, excuse)
        add_to_history(self.excuse_data, excuse, scenario)

    def generate_proof(self):
        proof = generate_proof()
        self._display(proof)

    def generate_apology(self):
        style = "emotional" if self.urgency_var.get() >= 7 else "professional"
        apology = generate_apology(style)
        self._display(apology)

    def speak_excuse(self):
        text = self.output_text.get("1.0", tk.END).strip()
        if text:
            Thread(
                target=self.voice.speak,
                args=(text, self.language_var.get()),
                daemon=True
            ).start()

    def add_to_favorites(self):
        excuse = self.output_text.get("1.0", tk.END).strip()
        if excuse and excuse not in self.favorite_excuses:
            self.favorite_excuses.append(excuse)
            self.favorites_listbox.insert(tk.END, excuse)
            add_to_favorites(self.excuse_data, excuse)

    # ─────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────

    def _display(self, text: str):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)

    def _load_selected(self, event):
        listbox = event.widget
        selection = listbox.curselection()
        if selection:
            self._display(listbox.get(selection))

    def _predict_excuse_needs(self):
        """Background thread: predicts when user might need an excuse based on patterns."""
        import time, random
        while True:
            time.sleep(120)
            if len(self.last_used_times) > 3 and random.random() < 0.2:
                self.root.after(0, lambda: show_notification(
                    self.root,
                    "💡 Reminder",
                    "You might need an excuse soon based on your patterns!"
                ))
