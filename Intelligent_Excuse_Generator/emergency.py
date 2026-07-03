# emergency.py — Fake emergency call and text trigger system

import random
import time
import tkinter as tk
from tkinter import ttk
from threading import Thread
from datetime import datetime


EMERGENCY_MESSAGES = [
    "URGENT: Your presence is required immediately!",
    "EMERGENCY: Need you to respond ASAP!",
    "CRITICAL: Situation requires your attention now!",
    "ALERT: Immediate response needed!"
]

FAKE_CALLERS = ["Hospital", "School", "Work", "Family Member", "Unknown Number"]


class EmergencySystem:
    """
    Manages background monitoring and triggering of fake emergency alerts.
    """

    def __init__(self, root: tk.Tk, last_used_times: list):
        """
        Initialize the emergency monitoring system.

        Args:
            root (tk.Tk): The main Tkinter window.
            last_used_times (list): Shared list of datetime objects from usage history.
        """
        self.root = root
        self.last_used_times = last_used_times
        self.emergency_active = False

    def start(self):
        """Start the background emergency monitor thread."""
        thread = Thread(target=self._monitor_loop, daemon=True)
        thread.start()

    def _monitor_loop(self):
        """Background loop that checks for trigger conditions every minute."""
        while True:
            now = datetime.now()

            # Trigger during peak excuse hours (morning commute / evening)
            if (8 <= now.hour < 10 or 16 <= now.hour < 18) and random.random() < 0.3:
                self.trigger()

            # Trigger based on usage interval pattern
            if len(self.last_used_times) > 2:
                intervals = [
                    (t2 - t1).total_seconds()
                    for t1, t2 in zip(self.last_used_times[:-1], self.last_used_times[1:])
                ]
                avg_interval = sum(intervals) / len(intervals)
                time_since_last = (datetime.now() - self.last_used_times[-1]).total_seconds()
                if time_since_last >= avg_interval * 0.9 and random.random() < 0.4:
                    self.trigger()

            time.sleep(60)

    def trigger(self):
        """Randomly trigger a fake message or call alert."""
        if not self.emergency_active:
            self.emergency_active = True
            alert_type = random.choice(["message", "call"])
            if alert_type == "message":
                self.root.after(0, self.show_emergency_message)
            else:
                self.root.after(0, self.show_emergency_call)
            self.emergency_active = False

    def show_emergency_message(self):
        """Display a fake emergency text message popup."""
        msg = random.choice(EMERGENCY_MESSAGES)

        popup = tk.Toplevel(self.root)
        popup.title("⚠️ Emergency Notification ⚠️")
        popup.geometry("320x160")
        popup.resizable(False, False)
        popup.attributes('-topmost', True)

        ttk.Label(
            popup,
            text=msg,
            font=("Segoe UI", 12, "bold"),
            wraplength=280
        ).pack(pady=20, padx=10)

        ttk.Button(popup, text="Dismiss", command=popup.destroy).pack(pady=10)
        popup.after(100, lambda: popup.attributes('-topmost', False))

    def show_emergency_call(self):
        """Display a fake incoming emergency call popup."""
        caller = random.choice(FAKE_CALLERS)

        popup = tk.Toplevel(self.root)
        popup.title("📞 Incoming Emergency Call 📞")
        popup.geometry("320x220")
        popup.resizable(False, False)
        popup.attributes('-topmost', True)

        ttk.Label(
            popup,
            text=f"📞 Incoming Call\nFrom: {caller}",
            font=("Segoe UI", 13, "bold"),
            justify="center"
        ).pack(pady=20)

        btn_frame = tk.Frame(popup)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="✅ Answer", command=popup.destroy).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="❌ Decline", command=popup.destroy).pack(side=tk.RIGHT, padx=10)

        popup.after(100, lambda: popup.attributes('-topmost', False))
