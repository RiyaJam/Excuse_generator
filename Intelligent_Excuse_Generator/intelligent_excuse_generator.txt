import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import random
import datetime
import json
import os
from gtts import gTTS
import pygame
import time
from threading import Thread
from PIL import Image, ImageTk, ImageDraw, ImageFont
from datetime import datetime, timedelta
import traceback
import tempfile

class ExcuseGeneratorApp:
    """
    A GUI application for generating excuses.
    """
    def __init__(self, root):
        """
        Initializes the main application window.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("✨ Advanced AI Excuse Generator ✨")
        self.root.geometry("1000x700")  # Adjusted for new features
        self.root.minsize(800, 500)
        self.root.configure(bg="#f5f5f5")
        
        # Initialize pygame for audio
        pygame.mixer.init()
        
        # Initialize attributes that were missing
        self.last_used_times = []  # Initialize before any threads access it
        self.languages = {
        "English": {"code": "en", "name": "English"},
        "Spanish": {"code": "es", "name": "Español"},
        "French": {"code": "fr", "name": "Français"},
        "German": {"code": "de", "name": "Deutsch"},
        "Italian": {"code": "it", "name": "Italiano"},
        "Portuguese": {"code": "pt", "name": "Português"},
        "Russian": {"code": "ru", "name": "Русский"},
        "Japanese": {"code": "ja", "name": "日本語"},
        "Chinese": {"code": "zh-CN", "name": "中文"},
        "Arabic": {"code": "ar", "name": "العربية"},
        "Hindi": {"code": "hi", "name": "हिन्दी"}
    }
        
        # Load or create excuse history data
        self.excuse_data_file = "excuse_data.json"
        self.load_excuse_data()
        
        # Initialize emergency trigger thread
        self.emergency_active = False
        
        # Create main container with scrollbar
        self.create_scrollable_window()
        
        # Custom styling
        self.setup_styles()
        
        # Create a header frame
        self.create_header()
        
        # Create the main content
        self.create_widgets()
        
        # Initialize data structures
        self.excuse_history = []
        self.favorite_excuses = []
        
        # Start threads after everything is initialized
        self.start_emergency_monitor()
        self.prediction_thread = Thread(target=self.predict_excuse_needs, daemon=True)
        self.prediction_thread.start()
        
        try:
          pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        except Exception as e:
            print(f"Audio initialization error: {str(e)}")
        self.show_notification("Warning", "Audio features may not work")


    def load_excuse_data(self):
        """Load excuse history data from file or create new"""
        if os.path.exists(self.excuse_data_file):
            with open(self.excuse_data_file, 'r') as f:
                self.excuse_data = json.load(f)
        else:
            self.excuse_data = {
                "history": [],
                "favorites": [],
                "effectiveness": {},
                "usage_patterns": []
            }

    def save_excuse_data(self):
        """Save excuse history data to file"""
        with open(self.excuse_data_file, 'w') as f:
            json.dump(self.excuse_data, f)

    def start_emergency_monitor(self):
        """Start thread to monitor for emergency triggers"""
        self.emergency_thread = Thread(target=self.monitor_emergency_triggers, daemon=True)
        self.emergency_thread.start()

    def monitor_emergency_triggers(self):
        """Monitor for situations that might trigger fake emergencies"""
        while True:
            # Check time patterns (more likely to need excuses at certain times)
            now = datetime.now()
            if (8 <= now.hour < 10 or 16 <= now.hour < 18) and random.random() < 0.3:
                self.trigger_fake_emergency()
            
            # Check usage patterns (if user frequently needs excuses at certain intervals)
            if len(self.last_used_times) > 2:
                avg_interval = sum((t2 - t1).total_seconds() 
                               for t1, t2 in zip(self.last_used_times[:-1], self.last_used_times[1:])) / (len(self.last_used_times) - 1)
                time_since_last = (datetime.now() - self.last_used_times[-1]).total_seconds()
                if time_since_last >= avg_interval * 0.9 and random.random() < 0.4:
                    self.trigger_fake_emergency()
            
            time.sleep(60)  # Check every minute

    def trigger_fake_emergency(self):
        """Trigger a fake emergency message or call"""
        if not self.emergency_active:
            self.emergency_active = True
            emergency_types = ["message", "call"]
            emergency_type = random.choice(emergency_types)
            
            if emergency_type == "message":
                self.show_emergency_message()
            else:
                self.play_emergency_call()
            
            self.emergency_active = False

    def show_emergency_message(self):
        """Show a fake emergency message popup"""
        emergency_messages = [
            "URGENT: Your presence is required immediately!",
            "EMERGENCY: Need you to respond ASAP!",
            "CRITICAL: Situation requires your attention now!",
            "ALERT: Immediate response needed!"
        ]
        
        msg = random.choice(emergency_messages)
        popup = tk.Toplevel(self.root)
        popup.title("⚠️ Emergency Notification ⚠️")
        popup.geometry("300x150")
        popup.resizable(False, False)
        
        label = ttk.Label(popup, text=msg, font=("Segoe UI", 12, "bold"), wraplength=250)
        label.pack(pady=20)
        
        close_btn = ttk.Button(popup, text="Dismiss", command=popup.destroy)
        close_btn.pack(pady=10)
        
        # Make the popup appear on top
        popup.attributes('-topmost', True)
        popup.after(100, lambda: popup.attributes('-topmost', False))

    def play_emergency_call(self):
        """Play a fake emergency call sound"""
        # In a real implementation, you would play an audio file
        # For this example, we'll just show a popup
        popup = tk.Toplevel(self.root)
        popup.title("📞 Incoming Emergency Call 📞")
        popup.geometry("300x200")
        popup.resizable(False, False)
        
        label = ttk.Label(popup, text="Incoming call from: EMERGENCY", 
                         font=("Segoe UI", 12, "bold"))
        label.pack(pady=20)
        
        # Add fake caller info
        callers = ["Hospital", "School", "Work", "Family", "Unknown"]
        caller = random.choice(callers)
        caller_label = ttk.Label(popup, text=f"Caller: {caller}")
        caller_label.pack(pady=5)
        
        # Add buttons
        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=15)
        
        answer_btn = ttk.Button(btn_frame, text="Answer", 
                               command=lambda: self.answer_emergency_call(popup, caller))
        answer_btn.grid(row=0, column=0, padx=5)
        
        decline_btn = ttk.Button(btn_frame, text="Decline", 
                                command=popup.destroy)
        decline_btn.grid(row=0, column=1, padx=5)
        
        # Make the popup appear on top
        popup.attributes('-topmost', True)
        popup.after(100, lambda: popup.attributes('-topmost', False))

    def answer_emergency_call(self, popup, caller):
        """Handle answering the fake emergency call"""
        popup.destroy()
        
        # Show call content
        call_content = {
            "Hospital": "We need you to come in immediately for test results.",
            "School": "Your child has been involved in an incident and needs to be picked up.",
            "Work": "Critical system failure - we need you to come in right away.",
            "Family": "There's been an emergency at home, please come immediately.",
            "Unknown": "This is an automated emergency alert. Please respond."
        }
        
        content = call_content.get(caller, "Emergency situation requires your immediate attention.")
        
        # Create call window
        call_window = tk.Toplevel(self.root)
        call_window.title(f"📞 On call with {caller} 📞")
        call_window.geometry("350x250")
        call_window.resizable(False, False)
        
        ttk.Label(call_window, text=f"Call with: {caller}", 
                 font=("Segoe UI", 12, "bold")).pack(pady=15)
        
        ttk.Label(call_window, text=content, wraplength=300).pack(pady=10)
        
        # Add fake audio visualization
        canvas = tk.Canvas(call_window, width=300, height=50, bg="white")
        canvas.pack(pady=10)
        
        # Animate sound waves
        def animate_waves():
            for i in range(10):
                canvas.delete("all")
                for j in range(15):
                    height = random.randint(5, 40)
                    canvas.create_rectangle(j*20, 25-height/2, j*20+15, 25+height/2, 
                                           fill="#4a6fa5", outline="")
                call_window.update()
                time.sleep(0.2)
        
        Thread(target=animate_waves, daemon=True).start()
        
        end_btn = ttk.Button(call_window, text="End Call", 
                            command=call_window.destroy)
        end_btn.pack(pady=10)

    def predict_excuse_needs(self):
        """Predict when an excuse might be needed based on patterns"""
        while True:
            if len(self.last_used_times) > 3:
                # Simple prediction based on average interval
                intervals = [(t2 - t1).total_seconds() 
                            for t1, t2 in zip(self.last_used_times[:-1], self.last_used_times[1:])]
                avg_interval = sum(intervals) / len(intervals)
                
                next_predicted = self.last_used_times[-1] + timedelta(seconds=avg_interval)
                time_until_next = (next_predicted - datetime.now()).total_seconds()
                
                if 0 < time_until_next < 3600:  # Within next hour
                    self.show_prediction_alert(next_predicted)
            
            time.sleep(60)  # Check every minute

    def show_prediction_alert(self, predicted_time):
        """Show an alert about predicted excuse need"""
        if not hasattr(self, 'prediction_shown') or not self.prediction_shown:
            self.prediction_shown = True
            
            popup = tk.Toplevel(self.root)
            popup.title("🔮 Excuse Prediction 🔮")
            popup.geometry("400x200")
            popup.resizable(False, False)
            
            time_str = predicted_time.strftime("%H:%M")
            msg = f"Based on your usage patterns, you may need an excuse around {time_str}.\n\nWould you like to prepare one now?"
            
            label = ttk.Label(popup, text=msg, wraplength=350)
            label.pack(pady=20)
            
            btn_frame = ttk.Frame(popup)
            btn_frame.pack(pady=10)
            
            yes_btn = ttk.Button(btn_frame, text="Yes", 
                               command=lambda: [self.prepare_excuse(), popup.destroy()])
            yes_btn.grid(row=0, column=0, padx=10)
            
            no_btn = ttk.Button(btn_frame, text="No", 
                               command=popup.destroy)
            no_btn.grid(row=0, column=1, padx=10)
            
            popup.protocol("WM_DELETE_WINDOW", lambda: [popup.destroy(), setattr(self, 'prediction_shown', False)])
            
            # Make the popup appear on top
            popup.attributes('-topmost', True)
            popup.after(100, lambda: popup.attributes('-topmost', False))

    def prepare_excuse(self):
        """Prepare an excuse in advance based on prediction"""
        self.scenario_combobox.set(random.choice(["Work", "School", "Social", "Family", "Personal"]))
        self.urgency_combobox.set(random.choice(["Low", "Medium", "High"]))
        self.believability_spinbox.set(random.randint(5, 9))
        self.generate_excuse()

    def create_scrollable_window(self):
        """Create the main container with scrollbar"""
        # Create main container frame
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)
        
        # Create a canvas for scrolling
        self.canvas = tk.Canvas(self.main_container)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Add scrollbar to canvas
        self.scrollbar = ttk.Scrollbar(self.main_container, 
                                     orient="vertical", 
                                     command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        # Configure the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', 
                        lambda e: self.canvas.configure(
                            scrollregion=self.canvas.bbox("all")))
        
        # Create a frame inside the canvas which will hold all widgets
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), 
                                window=self.scrollable_frame, 
                                anchor="nw")
        
        # Bind mousewheel to scroll
        self.scrollable_frame.bind("<Enter>", self._bind_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_mousewheel)

    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def setup_styles(self):
        """Configure custom styles for the application"""
        # Main style configuration
        style = ttk.Style()
        style.theme_use('clam')  # Use a modern theme as base
        
        # Colors
        primary_color = "#4a6fa5"
        secondary_color = "#6b8cae"
        accent_color = "#ff7e5f"
        light_bg = "#f5f5f5"
        dark_text = "#333333"
        
        # Frame style
        style.configure("TFrame", background=light_bg)
        style.configure("Header.TFrame", background=primary_color)
        
        # Label styles
        style.configure("TLabel", 
                        background=light_bg,
                        foreground=dark_text,
                        font=("Segoe UI", 10))
        style.configure("Header.TLabel",
                       background=primary_color,
                       foreground="white",
                       font=("Segoe UI", 14, "bold"))
        style.configure("Section.TLabel",
                       background=light_bg,
                       foreground=primary_color,
                       font=("Segoe UI", 11, "bold"))
        
        # Button styles
        style.configure("TButton",
                       padding=8,
                       relief="flat",
                       font=("Segoe UI", 10),
                       background=primary_color,
                       foreground="white")
        style.map("TButton",
                  background=[('active', secondary_color), ('disabled', '#cccccc')],
                  foreground=[('active', 'white'), ('disabled', '#888888')])
        
        style.configure("Accent.TButton",
                       background=accent_color)
        style.map("Accent.TButton",
                  background=[('active', '#ff9a8f'), ('disabled', '#cccccc')])
        
        # Combobox style
        style.configure("TCombobox",
                       fieldbackground="white",
                       background="white",
                       selectbackground=primary_color,
                       selectforeground="white",
                       insertcolor=dark_text,
                       font=("Segoe UI", 10))
        
        # Spinbox style
        style.configure("TSpinbox",
                       fieldbackground="white",
                       background="white",
                       insertcolor=dark_text,
                       font=("Segoe UI", 10))
        
        # Listbox style
        style.configure("TListbox",
                       background="white",
                       foreground=dark_text,
                       selectbackground=primary_color,
                       selectforeground="white",
                       font=("Segoe UI", 10),
                       relief="solid",
                       borderwidth=1)
        
        # Scrollbar style
        style.configure("Vertical.TScrollbar",
                       background=light_bg,
                       troughcolor=light_bg,
                       arrowcolor=primary_color)
        
        # ScrolledText style
        style.configure("TScrolledtext",
                       background="white",
                       foreground=dark_text,
                       insertcolor=dark_text,
                       font=("Segoe UI", 10),
                       relief="solid",
                       borderwidth=1)

    def create_header(self):
        """Create the application header"""
        header_frame = ttk.Frame(self.scrollable_frame, style="Header.TFrame", padding=(20, 10))
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        title_label = ttk.Label(header_frame, 
                               text="✨ Advanced AI Excuse Generator ✨",
                               style="Header.TLabel")
        title_label.pack(side="left")
        
        # Add a subtle separator
        separator = ttk.Separator(self.scrollable_frame, orient="horizontal")
        separator.grid(row=1, column=0, sticky="ew", pady=(0, 10))

    def create_widgets(self):
        """
        Creates and arranges the GUI elements.
        """
        # Main container frame
        main_frame = ttk.Frame(self.scrollable_frame, padding=15)
        main_frame.grid(row=2, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        
        # Input section
        self.create_input_section(main_frame)
        
        # Button section
        self.create_button_section(main_frame)
        
        # Output section
        self.create_output_section(main_frame)
        
        # History section
        self.create_history_section(main_frame)
        
        # New features section
        self.create_new_features_section(main_frame)

    def create_new_features_section(self, parent):
        """Create section for new features"""
        features_frame = ttk.LabelFrame(parent, text="Advanced Features", padding=15)
        features_frame.grid(row=4, column=0, sticky="ew", pady=(15, 0))
        features_frame.columnconfigure(0, weight=1)
        
        # Language selection
        ttk.Label(features_frame, text="Language:").grid(row=0, column=0, sticky="w", pady=5)
        self.language_combobox = ttk.Combobox(features_frame,values=[f"{lang_info['name']} ({code})" 
                                               for code, lang_info in 
                                               [(k, v) for k, v in self.languages.items()]],
                                        state="readonly")
        self.language_combobox.grid(row=0, column=1, sticky="ew", pady=5, padx=(5, 0))
        self.language_combobox.set("English (en)")
        
        # Format selection
        ttk.Label(features_frame, text="Output Format:").grid(row=1, column=0, sticky="w", pady=5)
        self.format_combobox = ttk.Combobox(features_frame,
                                          values=["Text", "Speech", "Both"],
                                          state="readonly")
        self.format_combobox.grid(row=1, column=1, sticky="ew", pady=5, padx=(5, 0))
        self.format_combobox.set("Text")
        
        # Proof type selection
        ttk.Label(features_frame, text="Proof Type:").grid(row=2, column=0, sticky="w", pady=5)
        self.proof_combobox = ttk.Combobox(features_frame,
                                         values=["Document", "Chat Screenshot", "Location Log", "Random"],
                                         state="readonly")
        self.proof_combobox.grid(row=2, column=1, sticky="ew", pady=5, padx=(5, 0))
        self.proof_combobox.set("Random")
        
        # Buttons for new features
        btn_frame = ttk.Frame(features_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        ttk.Button(btn_frame, text="View Best Excuses", 
                  command=self.show_best_excuses).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Generate Speech", 
                  command=self.generate_speech).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="View Proof", 
                  command=self.show_proof).pack(side="left", padx=5)

    def show_best_excuses(self):
        """Show a window with the best performing excuses"""
        best_excuses = sorted(self.excuse_data.get("effectiveness", {}).items(),
                             key=lambda x: x[1], reverse=True)[:5]
        
        popup = tk.Toplevel(self.root)
        popup.title("🏆 Top Performing Excuses 🏆")
        popup.geometry("500x300")
        
        if not best_excuses:
            label = ttk.Label(popup, text="No excuse effectiveness data available yet.")
            label.pack(pady=50)
            return
        
        frame = ttk.Frame(popup)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="Top Performing Excuses:", 
                 font=("Segoe UI", 12, "bold")).pack(pady=(0, 15))
        
        for i, (excuse, score) in enumerate(best_excuses, 1):
            row = ttk.Frame(frame)
            row.pack(fill="x", pady=5)
            
            ttk.Label(row, text=f"{i}.", width=3).pack(side="left")
            ttk.Label(row, text=excuse[:50] + ("..." if len(excuse) > 50 else ""), 
                     wraplength=350, anchor="w").pack(side="left", fill="x", expand=True)
            ttk.Label(row, text=f"Score: {score:.1f}").pack(side="right")

    def generate_speech(self, text, lang_code):
        """Generates and plays speech for the given text"""
        try:
            # Stop any current playback
            pygame.mixer.music.stop()

            # Create temporary file
            temp_path = os.path.join(tempfile.gettempdir(), f"excuse_{time.time()}.mp3")

            # Generate and save speech
            tts = gTTS(text=text, lang=lang_code)
            tts.save(temp_path)

            # Play the audio
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()

            # Clean up after playback completes
            def cleanup():
                time.sleep(5)  # Wait for playback to finish
                try:
                    os.remove(temp_path)
                except:
                    pass

            Thread(target=cleanup, daemon=True).start()

        except Exception as e:
            self.show_notification("Speech Error", f"Couldn't generate speech: {str(e)}")
            print(f"Speech Error: {traceback.format_exc()}")

    def show_proof(self):
        """Show generated proof in a new window"""
        proof_type = self.proof_combobox.get()
        
        if proof_type == "Random":
            proof_type = random.choice(["Document", "Chat Screenshot", "Location Log"])
        
        proof = self.generate_advanced_proof(proof_type)
        
        popup = tk.Toplevel(self.root)
        popup.title(f"Proof: {proof_type}")
        
        if proof_type == "Chat Screenshot":
            popup.geometry("400x600")
            
            # Display the image
            img_label = ttk.Label(popup)
            img_label.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Convert PIL image to PhotoImage
            photo = ImageTk.PhotoImage(proof)
            img_label.config(image=photo)
            img_label.image = photo  # Keep reference
            
        else:  # Document or Location Log
            popup.geometry("500x400")
            
            text = scrolledtext.ScrolledText(popup, wrap=tk.WORD, padx=10, pady=10)
            text.pack(fill="both", expand=True)
            text.insert(tk.END, proof)
            text.config(state=tk.DISABLED)
            
            # Add download button for documents
            if proof_type == "Document":
                btn_frame = ttk.Frame(popup)
                btn_frame.pack(fill="x", padx=10, pady=10)
                
                ttk.Button(btn_frame, text="Download PDF", 
                          command=lambda: self.save_as_pdf(proof)).pack(side="left")

    def generate_advanced_proof(self, proof_type):
        """
        Generates more realistic proof based on type.
        
        Args:
            proof_type (str): Type of proof to generate
            
        Returns:
            str or PIL.Image: The generated proof
        """
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M")
        
        if proof_type == "Document":
            doc_types = [
                "Medical Certificate", 
                "Official Notice", 
                "Incident Report", 
                "Verification Document"
            ]
            doc_type = random.choice(doc_types)
            
            doc = f"""
            {doc_type}
            Date: {date_str}
            Time: {time_str}
            Reference #: {random.randint(100000, 999999)}
            
            This document certifies that the individual was unable to fulfill their obligations
            due to unforeseen circumstances that required their immediate attention.
            
            The situation has been verified and this document serves as official confirmation.
            
            Authorized by: {random.choice(["Dr. Smith", "Office of Records", "HR Department", "Administration"])}
            Contact: {random.choice(["admin@example.com", "555-0100", "555-0200"])}
            
            This is an automatically generated document for verification purposes.
            """
            return doc
            
        elif proof_type == "Chat Screenshot":
            # Create a fake chat screenshot
            participants = [
                ("You", "#4a6fa5"),
                ("Boss", "#6b8cae"),
                ("HR", "#ff7e5f"),
                ("Colleague", "#8a6fa5")
            ]
            sender, color = random.choice(participants)
            
            # Create image
            width, height = 350, 500
            img = Image.new("RGB", (width, height), "#f5f5f5")
            draw = ImageDraw.Draw(img)
            
            # Add header
            draw.rectangle([0, 0, width, 60], fill="#4a6fa5")
            draw.text((10, 20), "Chat Conversation", fill="white", 
                     font=ImageFont.load_default(20))
            
            # Add fake messages
            y_pos = 70
            for i in range(random.randint(3, 6)):
                is_user = random.choice([True, False])
                if is_user:
                    name = "You"
                    bubble_color = "#e3f2fd"
                    x_pos = width - 150
                else:
                    name = sender
                    bubble_color = color
                    x_pos = 10
                
                # Draw message bubble
                message = random.choice([
                    "Hey, are you coming in today?",
                    "We need you for the meeting",
                    "Where are you?",
                    "Everything okay?",
                    "We're waiting for you"
                ]) if not is_user else random.choice([
                    "I'm having an emergency",
                    "I'll be late",
                    "Can't make it today",
                    "Something came up",
                    "I'll explain later"
                ])
                
                # Draw name
                draw.text((x_pos, y_pos), name, fill="#333333", 
                         font=ImageFont.load_default(14))
                y_pos += 20
                
                # Draw bubble
                bubble_height = 30 + (len(message) // 20) * 20
                draw.rounded_rectangle(
                    [x_pos, y_pos, x_pos + 140, y_pos + bubble_height],
                    radius=10, fill=bubble_color)
                
                # Draw message text
                draw.text((x_pos + 10, y_pos + 10), message, fill="#333333", 
                         font=ImageFont.load_default(12))
                
                # Draw time
                time_text = f"{random.randint(1, 12)}:{random.randint(0, 59):02d} {random.choice(['AM', 'PM'])}"
                draw.text((x_pos + 100, y_pos + bubble_height - 15), time_text, 
                         fill="#666666", font=ImageFont.load_default(10))
                
                y_pos += bubble_height + 20
            
            return img
            
        else:  # Location Log
            locations = [
                "Home", "Hospital", "School", "Airport", 
                "Highway", "Downtown", "Service Center"
            ]
            location = random.choice(locations)
            
            log = f"""
            Location History Log
            -------------------
            Date: {date_str}
            Time: {time_str}
            Device ID: D-{random.randint(1000, 9999)}
            
            Location Data:
            - {time_str}: {location} (Accuracy: {random.randint(5, 20)}m)
            - {now - timedelta(minutes=15):%H:%M}: En route to {location}
            - {now - timedelta(minutes=30):%H:%M}: {random.choice(locations)}
            
            This log confirms the device was at {location} at {time_str}.
            Data collected automatically by location services.
            
            Map URL: https://maps.example.com/?q={random.randint(10000, 99999)}
            """
            return log

    def save_as_pdf(self, text):
        """Save the document proof as PDF"""
        # In a real implementation, you would use a PDF library
        # For this example, we'll just show a message
        self.show_notification("PDF Saved", "The document has been saved as proof.pdf")

    def show_notification(self, title, message):
        """Show a notification popup"""
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("300x150")
        popup.resizable(False, False)
        
        label = ttk.Label(popup, text=message, wraplength=250)
        label.pack(pady=30)
        
        ttk.Button(popup, text="OK", command=popup.destroy).pack(pady=10)

    def create_input_section(self, parent):
        """Create the input controls section"""
        input_frame = ttk.LabelFrame(parent, text="Excuse Parameters", padding=15)
        input_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        input_frame.columnconfigure(1, weight=1)
        
        # Scenario selection
        ttk.Label(input_frame, text="Scenario:").grid(row=0, column=0, sticky="w", pady=5)
        self.scenario_combobox = ttk.Combobox(input_frame,
                                            values=["Work", "School", "Social", "Family", "Personal"],
                                            state="readonly")
        self.scenario_combobox.grid(row=0, column=1, sticky="ew", pady=5, padx=(5, 0))
        self.scenario_combobox.set("Social")
        
        # Urgency selection
        ttk.Label(input_frame, text="Urgency:").grid(row=1, column=0, sticky="w", pady=5)
        self.urgency_combobox = ttk.Combobox(input_frame,
                                           values=["Low", "Medium", "High"],
                                           state="readonly")
        self.urgency_combobox.grid(row=1, column=1, sticky="ew", pady=5, padx=(5, 0))
        self.urgency_combobox.set("Medium")
        
        # Believability selection
        ttk.Label(input_frame, text="Believability (1-10):").grid(row=2, column=0, sticky="w", pady=5)
        self.believability_spinbox = ttk.Spinbox(input_frame,
                                                from_=1, to=10,
                                                width=5)
        self.believability_spinbox.grid(row=2, column=1, sticky="w", pady=5, padx=(5, 0))
        self.believability_spinbox.set(5)

    def create_button_section(self, parent):
        """Create the action buttons section"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        # Configure grid for buttons
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        
        # Generate Excuse Button
        self.generate_button = ttk.Button(button_frame,
                                        text="Generate Excuse",
                                        command=self.generate_excuse,
                                        style="Accent.TButton")
        self.generate_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # Generate Proof Button
        self.proof_button = ttk.Button(button_frame,
                                      text="Generate Proof",
                                      command=self.generate_proof)
        self.proof_button.grid(row=0, column=1, sticky="ew", padx=5)
        
        # Generate Apology Button
        self.apology_button = ttk.Button(button_frame,
                                       text="Generate Apology",
                                       command=self.generate_apology)
        self.apology_button.grid(row=0, column=2, sticky="ew", padx=(5, 0))

    def create_output_section(self, parent):
        """Create the output display section"""
        output_frame = ttk.LabelFrame(parent, text="Generated Excuse", padding=15)
        output_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 15))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        # Text Area for Output
        self.output_text = scrolledtext.ScrolledText(output_frame,
                                                   wrap=tk.WORD,
                                                   height=10,
                                                   font=("Segoe UI", 10),
                                                   padx=10,
                                                   pady=10)
        self.output_text.grid(row=0, column=0, sticky="nsew")
        self.output_text.config(state=tk.DISABLED)

    def create_history_section(self, parent):
        """Create the history and favorites section"""
        history_frame = ttk.Frame(parent)
        history_frame.grid(row=3, column=0, sticky="nsew")
        history_frame.columnconfigure(0, weight=1)
        history_frame.columnconfigure(1, weight=1)
        
        # History panel
        history_panel = ttk.LabelFrame(history_frame, text="Excuse History", padding=10)
        history_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        history_panel.columnconfigure(0, weight=1)
        history_panel.rowconfigure(0, weight=1)
        
        self.history_listbox = tk.Listbox(history_panel,
                                        height=5,
                                        font=("Segoe UI", 10))
        self.history_listbox.grid(row=0, column=0, sticky="nsew")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(history_panel,
                                orient="vertical",
                                command=self.history_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        
        # Favorites panel
        favorites_panel = ttk.LabelFrame(history_frame, text="Favorites", padding=10)
        favorites_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        favorites_panel.columnconfigure(0, weight=1)
        favorites_panel.rowconfigure(0, weight=1)
        
        self.favorites_listbox = tk.Listbox(favorites_panel,
                                          height=5,
                                          font=("Segoe UI", 10))
        self.favorites_listbox.grid(row=0, column=0, sticky="nsew")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(favorites_panel,
                                orient="vertical",
                                command=self.favorites_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.favorites_listbox.config(yscrollcommand=scrollbar.set)
        
        # Add to Favorites button
        self.add_to_favorites_button = ttk.Button(history_frame,
                                                text="Add to Favorites",
                                                command=self.add_to_favorites)
        self.add_to_favorites_button.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        # Bind double-click events
        self.history_listbox.bind("<Double-1>", self.load_selected_excuse)
        self.favorites_listbox.bind("<Double-1>", self.load_selected_excuse)

    def generate_excuse(self):
        """
        Generates an excuse in selected language with speech output
        """
        try:
            # Get user inputs
            scenario = self.scenario_combobox.get()
            urgency = self.urgency_combobox.get()
            believability = self.believability_spinbox.get()
            output_format = self.format_combobox.get()

            # Validate inputs
            if not scenario or not urgency:
                self.show_notification("Error", "Please select scenario and urgency")
                return

            try:
                believability = int(believability)
                if not 1 <= believability <= 10:
                    self.show_notification("Error", "Believability must be 1-10")
                    return
            except ValueError:
                self.show_notification("Error", "Invalid believability value")
                return

            # Get selected language
            lang_name = self.language_combobox.get()
            lang_data = next((v for k,v in self.languages.items() if v['name'] in lang_name), 
                            {'code':'en', 'name':'English'})
            lang_code = lang_data['code']

            # Generate base excuse in English
            excuse_en = self.generate_artificial_excuse(scenario, urgency, believability)

            # Translate to selected language
            excuse = self.translate_excuse(excuse_en, lang_code)

             # Apply urgency prefix after translation
            if hasattr(self, 'last_urgency'):
                if self.last_urgency == "High":
                    excuse = "URGENT: " + excuse
                elif self.last_urgency == "Low":
                    excuse = "Minor issue: " + excuse
                        # Display the excuse
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, excuse)
            self.output_text.config(state=tk.DISABLED)

            # Add to history
            self.excuse_history.append(excuse)
            self.history_listbox.insert(tk.END, excuse[:50] + ("..." if len(excuse) > 50 else ""))

            # Generate speech if requested
            if output_format in ("Speech", "Both"):
                self.generate_speech(excuse, lang_code)

        except Exception as e:
            self.show_notification("Error", f"Excuse generation failed: {str(e)}")
            print(f"Error: {traceback.format_exc()}")


    def translate_excuse(self, excuse, lang_code):
        """Complete translations for all excuse patterns in all supported languages"""
        # First remove any existing language tag
        if excuse.startswith('[') and ']' in excuse:
            excuse = excuse.split(']', 1)[1].strip()
        translations = {
            # Technical Issues
            "Our company VPN went down and IT is still troubleshooting the issue.": {
                "es": "El VPN de nuestra empresa falló y TI aún está solucionando el problema.",
                "fr": "Le VPN de notre entreprise est tombé en panne et l'IT est toujours en train de résoudre le problème.",
                "de": "Unser Firmen-VPN ist ausgefallen und die IT arbeitet noch an der Lösung des Problems.",
                "it": "La VPN aziendale è caduta e l'IT sta ancora risolvendo il problema.",
                "pt": "O VPN da nossa empresa caiu e a TI ainda está resolvendo o problema.",
                "ru": "Корпоративный VPN перестал работать, и ИТ-отдел все еще устраняет неполадки.",
                "ja": "会社のVPNがダウンしており、IT部門が現在問題を解決中です。",
                "zh-CN": "我们公司的VPN出现故障，IT部门正在排查问题。",
                "ar": "انخفض VPN الخاص بشركتنا ولا يزال قسم تكنولوجيا المعلومات يعمل على حل المشكلة.",
                "hi": "हमारी कंपनी का VPN डाउन हो गया है और आईटी अभी भी समस्या का समाधान कर रहा है।"
            },
            "My work laptop decided to install Windows updates right before the meeting.": {
                "es": "Mi portátil de trabajo decidió instalar actualizaciones de Windows justo antes de la reunión.",
                "fr": "Mon ordinateur portable professionnel a décidé d'installer les mises à jour Windows juste avant la réunion.",
                "de": "Mein Arbeitslaptop beschloss, Windows-Updates genau vor dem Meeting zu installieren.",
                "it": "Il mio laptop di lavoro ha deciso di installare gli aggiornamenti di Windows proprio prima della riunione.",
                "pt": "Meu laptop de trabalho decidiu instalar atualizações do Windows logo antes da reunião.",
                "ru": "Мой рабочий ноутбук решил установить обновления Windows прямо перед встречей.",
                "ja": "仕事用のノートパソコンが会議直前にWindowsの更新を開始しました。",
                "zh-CN": "我的工作笔记本电脑在会议前突然开始安装Windows更新。",
                "ar": "قرر جهاز الكمبيوتر المحمول الخاص بي تثبيت تحديثات Windows قبل الاجتماع مباشرة.",
                "hi": "मेरे काम के लैपटॉप ने मीटिंग से ठीक पहले Windows अपडेट इंस्टॉल करने का फैसला किया।"
            },
            
            # Transportation Problems
            "There was a major accident on the highway that's causing hours-long delays.": {
                "es": "Hubo un accidente grave en la autopista que está causando retrasos de horas.",
                "fr": "Il y a eu un grave accident sur l'autoroute qui cause des retards de plusieurs heures.",
                "de": "Es gab einen schweren Unfall auf der Autobahn, der zu stundenlangen Verzögerungen führt.",
                "it": "C'è stato un grave incidente in autostrada che sta causando ritardi di ore.",
                "pt": "Houve um acidente grave na rodovia que está causando atrasos de horas.",
                "ru": "На шоссе произошла серьезная авария, вызывающая многочасовые задержки.",
                "ja": "幹線道路で重大な事故があり、数時間の遅れが生じています。",
                "zh-CN": "高速公路上发生了严重事故，导致长达数小时的延误。",
                "ar": "وقع حادث كبير على الطريق السريع مما تسبب في تأخير لساعات.",
                "hi": "हाईवे पर एक बड़ा हादसा हुआ है जिसके कारण घंटों लंबी देरी हो रही है।"
            },
            "My car battery died this morning and I'm waiting for roadside assistance.": {
                "es": "La batería de mi auto se agotó esta mañana y estoy esperando asistencia en carretera.",
                "fr": "La batterie de ma voiture est morte ce matin et j'attends l'assistance routière.",
                "de": "Meine Autobatterie ist heute Morgen gestorben und ich warte auf Pannenhilfe.",
                "it": "La batteria della mia auto si è esaurita stamattina e sto aspettando l'assistenza stradale.",
                "pt": "A bateria do meu carro descarregou esta manhã e estou aguardando o socorro na estrada.",
                "ru": "Сегодня утром сел аккумулятор в машине, и я жду помощи на дороге.",
                "ja": "今朝車のバッテリーが上がり、ロードサービスを待っています。",
                "zh-CN": "我的汽车电池今早没电了，正在等待道路救援。",
                "ar": "بطارية سيارتي نفدت هذا الصباح وأنا أنتظر المساعدة على الطريق.",
                "hi": "मेरी कार की बैटरी आज सुबह खत्म हो गई और मैं रोडसाइड सहायता का इंतजार कर रहा हूं।"
            },
            
            # Health Issues
            "I woke up with severe migraines and can't look at screens right now.": {
                "es": "Me desperté con migrañas severas y no puedo mirar pantallas en este momento.",
                "fr": "Je me suis réveillé avec de sévères migraines et je ne peux pas regarder d'écrans pour le moment.",
                "de": "Ich bin mit starken Migräneattacken aufgewacht und kann im Moment nicht auf Bildschirme schauen.",
                "it": "Mi sono svegliato con un'emicrania forte e al momento non posso guardare gli schermi.",
                "pt": "Acordei com enxaqueca severa e não consigo olhar para telas no momento.",
                "ru": "Я проснулся с сильной мигренью и сейчас не могу смотреть на экраны.",
                "ja": "激しい片頭痛で目が覚め、今は画面を見ることができません。",
                "zh-CN": "我醒来时患有严重偏头痛，现在无法看屏幕。",
                "ar": "استيقظت مع صداع نصفي شديد ولا يمكنني النظر إلى الشاشات الآن.",
                "hi": "मैं गंभीर माइग्रेन के साथ उठा हूँ और अभी स्क्रीन नहीं देख सकता।"
            },
            "I'm having an allergic reaction and need to visit urgent care.": {
                "es": "Estoy teniendo una reacción alérgica y necesito ir a urgencias.",
                "fr": "Je fais une réaction allergique et dois me rendre aux urgences.",
                "de": "Ich habe eine allergische Reaktion und muss die Notaufnahme aufsuchen.",
                "it": "Sto avendo una reazione allergica e devo andare al pronto soccorso.",
                "pt": "Estou tendo uma reação alérgica e preciso ir ao pronto-socorro.",
                "ru": "У меня аллергическая реакция, и мне нужно срочно обратиться к врачу.",
                "ja": "アレルギー反応が出ているため、緊急治療を受ける必要があります。",
                "zh-CN": "我出现了过敏反应，需要去急诊。",
                "ar": "أعاني من رد فعل تحسسي وأحتاج إلى زيارة الرعاية العاجلة.",
                "hi": "मुझे एलर्जी की प्रतिक्रिया हो रही है और मुझे तत्काल देखभाल की आवश्यकता है।"
            },
            
            # Family Emergencies
            "My child's school called - they're sick and need to be picked up immediately.": {
                "es": "La escuela de mi hijo llamó - están enfermos y necesitan que los recoja inmediatamente.",
                "fr": "L'école de mon enfant a appelé - il est malade et doit être récupéré immédiatement.",
                "de": "Die Schule meines Kindes hat angerufen - es ist krank und muss sofort abgeholt werden.",
                "it": "La scuola di mio figlio ha chiamato - è malato e deve essere ripreso immediatamente.",
                "pt": "A escola do meu filho ligou - ele está doente e precisa ser buscado imediatamente.",
                "ru": "Школа моего ребенка позвонила - он заболел, и его нужно немедленно забрать.",
                "ja": "子供の学校から連絡がありました。子供が病気なのですぐに迎えに来てください。",
                "zh-CN": "我孩子的学校打来电话说孩子生病了，需要立即接走。",
                "ar": "اتصلت مدرسة طفلي - إنهم مرضى ويحتاجون إلى أن يتم اصطحابهم على الفور.",
                "hi": "मेरे बच्चे के स्कूल ने फोन किया - वे बीमार हैं और उन्हें तुरंत लेने की आवश्यकता है।"
            },
            "A pipe burst in my home and I need to deal with the flooding.": {
                "es": "Una tubería reventó en mi casa y necesito ocuparme de la inundación.",
                "fr": "Une canalisation a éclaté dans ma maison et je dois m'occuper de l'inondation.",
                "de": "Eine Wasserleitung ist in meinem Haus geplatzt und ich muss mich um die Überschwemmung kümmern.",
                "it": "Una tubatura è scoppiata in casa mia e devo occuparmi dell'allagamento.",
                "pt": "Um cano estourou na minha casa e preciso lidar com o alagamento.",
                "ru": "У меня дома лопнула труба, и мне нужно устранять последствия потопа.",
                "ja": "自宅で水道管が破裂し、水漏れに対処する必要があります。",
                "zh-CN": "我家里的水管爆裂了，需要处理漏水问题。",
                "ar": "انفجر أنبوب في منزلي وأحتاج إلى التعامل مع الفيضان.",
                "hi": "मेरे घर में एक पाइप फट गया है और मुझे बाढ़ से निपटने की आवश्यकता है।"
            },
            
            # Add more categories and excuses as needed...
        }
        
        # Return translation if available, otherwise return English with language tag
        if excuse in translations and lang_code in translations[excuse]:
            return translations[excuse][lang_code]
        return f"[{lang_code.upper()}] {excuse}"

    def generate_proof(self):
        """
        Generates a simulated proof for the generated excuse and displays it.
        """
        proof_type = self.proof_combobox.get()
        
        if proof_type == "Random":
            proof_type = random.choice(["Document", "Chat Screenshot", "Location Log"])
        
        proof = self.generate_advanced_proof(proof_type)
        
        if isinstance(proof, str):
            self.display_message(proof)
        else:
            # For image proof, show in a new window
            self.show_proof()

    def generate_apology(self):
        """
        Generates a simulated apology and displays it in selected language.
        """
        apologies = {
            "en": [
                "I sincerely apologize for the inconvenience.",
                "Please accept my deepest apologies for my absence.",
                "I regret that I was unable to fulfill my obligation.",
                "I am truly sorry for the trouble caused.",
                "I take full responsibility and apologize for the issue.",
                "I understand my actions have caused problems, and I apologize.",
                "I want to express my sincere remorse for what happened.",
                "I am deeply sorry for the disruption.",
                "I offer my sincerest apologies for the misunderstanding.",
                "I am extremely sorry for the error.",
                "My apologies for the unexpected situation.",
                "Please forgive me for this oversight."
            ],
            "es": [
                "Sinceramente me disculpo por el inconveniente.",
                "Por favor acepte mis más sinceras disculpas por mi ausencia.",
                "Lamento no haber podido cumplir con mi obligación.",
                "Realmente lamento las molestias ocasionadas.",
                "Asumo toda la responsabilidad y pido disculpas por el problema.",
                "Entiendo que mis acciones han causado problemas, y me disculpo.",
                "Quiero expresar mi sincero remordimiento por lo ocurrido.",
                "Lamento profundamente la interrupción.",
                "Ofrezco mis más sinceras disculpas por el malentendido.",
                "Estoy extremadamente apenado por el error.",
                "Mis disculpas por la situación inesperada.",
                "Por favor perdóneme por este descuido."
            ],
            "fr": [
                "Je m'excuse sincèrement pour le dérangement.",
                "Veuillez accepter mes excuses les plus sincères pour mon absence.",
                "Je regrette de ne pas avoir pu m'acquitter de mon obligation.",
                "Je suis vraiment désolé pour les problèmes causés.",
                "J'assume l'entière responsabilité et je m'excuse pour ce problème.",
                "Je comprends que mes actions ont causé des problèmes et je m'en excuse.",
                "Je tiens à exprimer mes sincères remords pour ce qui s'est passé.",
                "Je suis profondément désolé pour la perturbation.",
                "Je présente mes excuses les plus sincères pour ce malentendu.",
                "Je suis extrêmement désolé pour cette erreur.",
                "Mes excuses pour cette situation inattendue.",
                "Veuillez me pardonner pour cette négligence."
            ],
            "de": [
                "Ich entschuldige mich aufrichtig für die Unannehmlichkeiten.",
                "Bitte akzeptieren Sie meine aufrichtigsten Entschuldigungen für mein Fehlen.",
                "Es tut mir leid, dass ich meine Verpflichtung nicht erfüllen konnte.",
                "Ich bedaure die verursachten Probleme zutiefst.",
                "Ich übernehme die volle Verantwortung und entschuldige mich für das Problem.",
                "Ich verstehe, dass meine Handlungen Probleme verursacht haben, und ich entschuldige mich.",
                "Ich möchte meine aufrichtige Reue für das Geschehene ausdrücken.",
                "Ich bedaure die Störung zutiefst.",
                "Ich bitte aufrichtig um Entschuldigung für das Missverständnis.",
                "Ich bedaure den Fehler außerordentlich.",
                "Meine Entschuldigung für die unerwartete Situation.",
                "Bitte verzeihen Sie mir diese Unachtsamkeit."
            ],
            "it": [
                "Mi scuso sinceramente per l'inconveniente.",
                "Per favore accetta le mie più sincere scuse per la mia assenza.",
                "Mi dispiace di non essere stato in grado di adempiere al mio obbligo.",
                "Sono veramente dispiaciuto per il problema causato.",
                "Mi assumo piena responsabilità e mi scuso per il problema.",
                "Capisco che le mie azioni hanno causato problemi e mi scuso.",
                "Voglio esprimere il mio sincero rimorso per quanto accaduto.",
                "Sono profondamente dispiaciuto per il disturbo.",
                "Offro le mie più sincere scuse per l'incomprensione.",
                "Sono estremamente dispiaciuto per l'errore.",
                "Le mie scuse per la situazione imprevista.",
                "Per favore perdonami per questa disattenzione."
            ],
            "pt": [
                "Peço sinceras desculpas pelo inconveniente.",
                "Por favor, aceite minhas mais sinceras desculpas pela minha ausência.",
                "Lamento não ter podido cumprir minha obrigação.",
                "Sinto muito pelo transtorno causado.",
                "Assumo total responsabilidade e peço desculpas pelo problema.",
                "Entendo que minhas ações causaram problemas e peço desculpas.",
                "Quero expressar meu sincero remorso pelo que aconteceu.",
                "Lamento profundamente a interrupção.",
                "Ofereço minhas mais sinceras desculpas pelo mal-entendido.",
                "Sinto muitíssimo pelo erro.",
                "Minhas desculpas pela situação inesperada.",
                "Por favor, me perdoe por este descuido."
            ],
            "ru": [
                "Искренне извиняюсь за неудобства.",
                "Пожалуйста, примите мои глубочайшие извинения за мое отсутствие.",
                "Сожалею, что не смог выполнить свои обязательства.",
                "Мне очень жаль за причиненные неудобства.",
                "Я беру на себя полную ответственность и извиняюсь за проблему.",
                "Я понимаю, что мои действия вызвали проблемы, и я извиняюсь.",
                "Хочу выразить свое искреннее сожаление о случившемся.",
                "Я глубоко сожалею о срыве.",
                "Приношу свои глубочайшие извинения за недоразумение.",
                "Мне очень жаль за эту ошибку.",
                "Мои извинения за неожиданную ситуацию.",
                "Пожалуйста, простите меня за эту невнимательность."
            ],
            "ja": [
                "ご不便をおかけして誠に申し訳ございません。",
                "欠席の件、深くお詫び申し上げます。",
                "義務を果たせなかったことを心よりお詫び申し上げます。",
                "ご迷惑をおかけし、大変申し訳ございませんでした。",
                "全責任を負い、問題についてお詫び申し上げます。",
                "自分の行動が問題を引き起こしたことを理解しており、お詫び申し上げます。",
                "発生したことに対して心から後悔の意を表明いたします。",
                "中断を深くお詫び申し上げます。",
                "誤解について心からお詫び申し上げます。",
                "この誤りについて大変申し訳なく思っております。",
                "予期せぬ事態となり申し訳ございません。",
                "この不注意についてお許しください。"
            ],
            "zh-CN": [
                "对于给您带来的不便，我深表歉意。",
                "请接受我对缺席的最诚挚的道歉。",
                "我很遗憾未能履行我的义务。",
                "我对造成的麻烦感到非常抱歉。",
                "我承担全部责任并为此问题道歉。",
                "我理解我的行为造成了问题，我为此道歉。",
                "我想对发生的事情表示诚挚的悔意。",
                "我对这次中断深表歉意。",
                "对于这个误会，我表示最诚挚的歉意。",
                "我对这个错误感到非常抱歉。",
                "对于这个意外情况，我表示歉意。",
                "请原谅我的这个疏忽。"
            ],
            "ar": [
                "أعتذر بصدق عن الإزعاج.",
                "يرجى قبول اعتذاري الصادق عن غيابي.",
                "أنا آسف لأنني لم أتمكن من الوفاء بالتزامي.",
                "أنا آسف حقًا للمتاعب التي سببتها.",
                "أتحمل المسؤولية الكاملة وأعتذر عن المشكلة.",
                "أفهم أن أفعالي تسببت في مشاكل وأعتذر.",
                "أريد أن أعبر عن ندمي الصادق لما حدث.",
                "أنا آسف بشأن الاضطراب.",
                "أقدم أصدق اعتذاري عن سوء الفهم.",
                "أنا آسف للغاية على الخطأ.",
                "اعتذاري عن الموقف غير المتوقع.",
                "من فضلك سامحني على هذا الإهمال."
            ],
            "hi": [
                "मैं असुविधा के लिए हार्दिक क्षमा चाहता हूँ।",
                "कृपया मेरी अनुपस्थिति के लिए मेरी गहरी क्षमा याचना स्वीकार करें।",
                "मुझे खेद है कि मैं अपने दायित्व को पूरा नहीं कर पाया।",
                "मैं पैदा की गई परेशानी के लिए सचमुच खेद प्रकट करता हूँ।",
                "मैं पूरी जिम्मेदारी लेता हूँ और इस मुद्दे के लिए क्षमा चाहता हूँ।",
                "मैं समझता हूँ कि मेरे कार्यों ने समस्याएँ पैदा की हैं, और मैं क्षमा चाहता हूँ।",
                "मैं हुई घटना के लिए अपनी हार्दिक पश्चाताप व्यक्त करना चाहता हूँ।",
                "मैं व्यवधान के लिए गहरा खेद प्रकट करता हूँ।",
                "मैं गलतफहमी के लिए अपनी हार्दिक क्षमा याचना प्रस्तुत करता हूँ।",
                "मुझे इस गलती के लिए अत्यंत खेद है।",
                "अप्रत्याशित स्थिति के लिए मेरी क्षमा याचना।",
                "कृपया मुझे इस असावधानी के लिए क्षमा करें।"
            ]
        }
    
        selected_lang = self.language_combobox.get().split(" ")[-1].strip("()")
        language = self.languages.get(selected_lang, {}).get("code", "en")
    
    # Get apologies for selected language, fallback to English
        lang_apologies = apologies.get(language, apologies["en"])
        apology = random.choice(lang_apologies)
    
        self.display_message(apology)
    
    # Handle output format
        output_format = self.format_combobox.get()
        if output_format == "Speech" or output_format == "Both":
            self.generate_speech()

    def display_message(self, message):
        """
        Displays a message in the output text area.

        Args:
            message (str): The message to display.
        """
        self.output_text.config(state=tk.NORMAL)  # Enable editing
        self.output_text.delete("1.0", tk.END)  # Clear previous text
        self.output_text.insert(tk.END, message)
        self.output_text.config(state=tk.DISABLED)  # Disable editing

    def generate_artificial_excuse(self, scenario, urgency, believability):
        """
        Generates an excuse with expanded variety. 

        Args:
            scenario (str): The scenario for the excuse.
            urgency (str): The urgency of the situation.
            believability (int): The believability level (1-10).

        Returns:
            str: The generated excuse.
        """
        excuses = {
            "Work": [
                # Technical issues
                "Our company VPN went down and IT is still troubleshooting the issue.",
                "My work laptop decided to install Windows updates right before the meeting.",
                "The power went out in my home office due to a local outage.",
                "Our project management system crashed and I lost access to critical files.",
                
                # Transportation problems
                "There was a major accident on the highway that's causing hours-long delays.",
                "My car battery died this morning and I'm waiting for roadside assistance.",
                "Public transportation is experiencing significant delays due to signal problems.",
                "My ride-share driver canceled last minute and I couldn't find a replacement.",
                
                # Health issues
                "I woke up with severe migraines and can't look at screens right now.",
                "I'm having an allergic reaction and need to visit urgent care.",
                "My chronic back pain is flaring up and I can't sit at my desk.",
                "I think I might be coming down with the flu and don't want to get others sick.",
                
                # Family emergencies
                "My child's school called - they're sick and need to be picked up immediately.",
                "My pet had a medical emergency and I need to take them to the vet.",
                "A pipe burst in my home and I need to deal with the flooding.",
                "My elderly parent had a fall and needs assistance getting to the doctor.",
                
                # Unusual circumstances
                "A tree fell on my driveway and I can't get my car out.",
                "There's a police investigation happening in my neighborhood and we're asked to stay inside.",
                "I'm locked out of my house and waiting for a locksmith.",
                "A swarm of bees has taken residence outside my front door."
            ],
            "School": [
                # Academic issues
                "I accidentally submitted the wrong draft of my paper and need to redo it.",
                "The library closed early and I couldn't access the resources I needed.",
                "My study group canceled last minute and I'm not prepared.",
                "I mixed up the due dates and thought this was due next week.",
                
                # Technology problems
                "My printer ran out of ink right as I was printing my assignment.",
                "The campus WiFi is down and I can't access online materials.",
                "My laptop charger broke and my battery is dead.",
                "The submission portal crashed right when I tried to upload my work.",
                
                # Health issues
                "I pulled an all-nighter and my eyes are too strained to focus.",
                "My allergies are so bad today I can't stop sneezing.",
                "I have a terrible ear infection and can't concentrate.",
                "I got food poisoning from the dining hall and need to recover.",
                
                # Transportation problems
                "My bike got a flat tire on the way to campus.",
                "The campus shuttle isn't running today due to driver shortages.",
                "My parking permit expired and I couldn't find alternative parking.",
                "There's construction blocking my usual route to class.",
                
                # Personal circumstances
                "My roommate accidentally took my backpack with all my materials.",
                "I left my notebook on the bus and it hasn't been turned in yet.",
                "My alarm didn't go off because of a power outage overnight.",
                "I got the dates confused because of daylight savings time change."
            ],
            "Social": [
                # Last-minute issues
                "My babysitter canceled last minute and I can't find a replacement.",
                "I just realized I double-booked myself for tonight.",
                "My outfit got ruined right before I was about to leave.",
                "My phone died and I lost all the event details.",
                
                # Transportation problems
                "My ride bailed on me at the last second.",
                "There's no parking available anywhere near the venue.",
                "My car is making a strange noise and I don't want to risk driving it.",
                "The trains are running on a holiday schedule and I can't get there.",
                
                # Health issues
                "I developed a sudden rash and need to figure out what's causing it.",
                "I threw out my back while getting ready.",
                "I have a terrible toothache and need to see a dentist.",
                "I'm experiencing vertigo and shouldn't be out in public.",
                
                # Household emergencies
                "My kitchen sink started leaking and I need to fix it.",
                "My smoke detector won't stop beeping and I need to replace the battery.",
                "I accidentally locked myself out of my apartment.",
                "My refrigerator stopped working and I need to save my food.",
                
                # Unusual circumstances
                "A stray cat had kittens in my garage and I need to help them.",
                "My neighbor locked their keys in their car with the engine running.",
                "There's a suspicious package in my building and we're evacuated.",
                "I just found out I'm allergic to the venue (pet dander/peanuts/etc)."
            ],
            "Family": [
                # Childcare issues
                "The daycare called - my child has a fever and needs to be picked up.",
                "Our regular babysitter is sick and we can't find coverage.",
                "My child has a school project due tomorrow we forgot about.",
                "There's an unexpected early dismissal at school today.",
                
                # Elder care
                "My mother's home health aide didn't show up today.",
                "My father's medication needs to be refilled urgently.",
                "We need to take my grandmother to an unexpected doctor's appointment.",
                "The assisted living facility is on lockdown due to a health inspection.",
                
                # Family emergencies
                "Our basement flooded after last night's heavy rain.",
                "Our carbon monoxide detector went off and we're waiting for the fire department.",
                "A family member was in a minor car accident and needs support.",
                "We're dealing with a sudden pest infestation in our home.",
                
                # Logistics issues
                "Our flight home got canceled and we're stuck at the airport.",
                "The hotel lost our reservation and we need to find new accommodations.",
                "Our luggage got lost and we're waiting for it to be delivered.",
                "Our rental car broke down in an unfamiliar area.",
                
                # Special circumstances
                "Today is the anniversary of a family member's passing and we're not up for socializing.",
                "We're fostering a rescue dog who's having separation anxiety.",
                "We're hosting unexpected out-of-town relatives.",
                "Our home security system triggered a false alarm and police are investigating."
            ],
            "Personal": [
                # Mental health
                "I'm experiencing severe anxiety today and need to take care of myself.",
                "My therapist recommended I take a mental health day.",
                "I'm feeling completely overwhelmed and need to reset.",
                "I haven't been sleeping well and can't function properly today.",
                
                # Physical health
                "I twisted my ankle while exercising and need to rest it.",
                "I have a migraine coming on and need to lie down.",
                "I got a bad sunburn and can't wear proper clothes.",
                "I'm recovering from a minor medical procedure.",
                
                # Home issues
                "My water heater broke and I need to get it fixed.",
                "There's a gas leak in my building and we had to evacuate.",
                "My apartment is being treated for bed bugs today.",
                "My air conditioning stopped working in this heat wave.",
                
                # Technology problems
                "My phone fell in water and I'm waiting for it to dry out.",
                "I got locked out of all my accounts due to a security breach.",
                "My smart home devices all malfunctioned at once.",
                "My internet provider is having an outage in my area.",
                
                # Unusual personal circumstances
                "I'm waiting for an important delivery that requires my signature.",
                "I'm being audited and need to gather tax documents.",
                "My wallet was stolen and I'm dealing with canceling cards.",
                "I'm being called for jury duty today."
            ]
        }
        
        excuses_list = excuses.get(scenario, [])
        index = (believability * len(excuses_list) // 10 - 1)
        index = max(0, min(index, len(excuses_list) - 1))
        excuse = excuses_list[index]
            
        # Store the urgency level separately instead of modifying the excuse text
        self.last_urgency = urgency  # Add this as a class attribute

        return excuse

    def generate_artificial_proof(self):
        """
        Generates a simulated proof. This is a placeholder.

        Returns:
            str: The generated proof.
        """
        proof_types = ["document", "chat screenshot", "location log"]
        proof_type = random.choice(proof_types)
        now = datetime.now()
        date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")

        if proof_type == "document":
            proof = f"Document Proof ({date_time_str}):\n" \
                    "This document certifies that the user was unable to attend due to unforeseen circumstances."
        elif proof_type == "chat screenshot":
            proof = f"Chat Screenshot ({date_time_str}):\n" \
                    " [Chat Screenshot] User: I will be delayed. Reason: [Reason]."
        else:  # location log
            proof = f"Location Log ({date_time_str}):\n" \
                    "[Location Data] User's location shows they were at [Location] during the time of the incident."
        return proof

    def generate_artificial_apology(self):
        """
        Generates a simulated apology. This is a placeholder.

        Returns:
            str: The generated apology.
        """
        apologies = [
            "I sincerely apologize for the inconvenience.",
            "Please accept my deepest apologies for my absence.",
            "I regret that I was unable to fulfill my obligation.",
            "I am truly sorry for the trouble caused.",
            "I take full responsibility and apologize for the issue.",
            "I understand my actions have caused problems, and I apologize.",
            "I want to express my sincere remorse for what happened.",
            "I am deeply sorry for the disruption.",
            "I offer my sincerest apologies for the misunderstanding.",
            "I am extremely sorry for the error."
        ]
        return random.choice(apologies)

    def add_to_favorites(self):
        """
        Adds the currently displayed excuse to the favorites list.
        """
        current_excuse = self.output_text.get("1.0", tk.END).strip()
        if current_excuse and current_excuse not in self.favorite_excuses:
            self.favorite_excuses.append(current_excuse)
            self.favorites_listbox.insert(tk.END, current_excuse)
            
            # Add to saved data
            if current_excuse not in self.excuse_data["favorites"]:
                self.excuse_data["favorites"].append(current_excuse)
                self.save_excuse_data()

    def load_selected_excuse(self, event):
        """
        Loads the selected excuse from the history or favorites listbox
        into the output text area.

        Args:
            event (Tkinter.Event): The event object (double-click).
        """
        listbox = event.widget
        selected_index = listbox.curselection()
        if selected_index:
            selected_excuse = listbox.get(selected_index)
            self.display_message(selected_excuse)

    def clear_audio(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        if self.current_audio_file and os.path.exists(self.current_audio_file):
            try:
                os.remove(self.current_audio_file)
            except:
                pass
            
            
if __name__ == "__main__":
    root = tk.Tk()
    app = ExcuseGeneratorApp(root)
    root.mainloop()