# ui_components.py — Reusable UI components, styles, header, and scrollable window

import tkinter as tk
from tkinter import ttk


# ─────────────────────────────────────────────
# Style Setup
# ─────────────────────────────────────────────

def setup_styles():
    """Configure ttk styles for the application."""
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TFrame", background="#f5f5f5")
    style.configure("TLabel", background="#f5f5f5", font=("Segoe UI", 10))
    style.configure("TButton",
                    font=("Segoe UI", 10, "bold"),
                    padding=6,
                    background="#4CAF50",
                    foreground="white")
    style.map("TButton",
              background=[("active", "#388E3C")],
              foreground=[("active", "white")])

    style.configure("Header.TLabel",
                    font=("Segoe UI", 22, "bold"),
                    background="#2c3e50",
                    foreground="white")
    style.configure("Sub.TLabel",
                    font=("Segoe UI", 11),
                    background="#2c3e50",
                    foreground="#ecf0f1")
    style.configure("Card.TFrame", background="white", relief="raised")
    style.configure("Danger.TButton",
                    background="#e74c3c",
                    foreground="white",
                    font=("Segoe UI", 10, "bold"))
    style.map("Danger.TButton", background=[("active", "#c0392b")])


# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────

def create_header(parent: tk.Widget) -> tk.Frame:
    """
    Create and return the app header frame.

    Args:
        parent: Parent widget.

    Returns:
        tk.Frame: The header frame.
    """
    header = tk.Frame(parent, bg="#2c3e50", pady=15)
    header.pack(fill=tk.X)

    tk.Label(
        header,
        text="✨ Intelligent Excuse Generator ✨",
        font=("Segoe UI", 22, "bold"),
        bg="#2c3e50",
        fg="white"
    ).pack()

    tk.Label(
        header,
        text="AI-powered | Context-aware | Multi-language",
        font=("Segoe UI", 10),
        bg="#2c3e50",
        fg="#bdc3c7"
    ).pack()

    return header


# ─────────────────────────────────────────────
# Scrollable Window
# ─────────────────────────────────────────────

def create_scrollable_frame(parent: tk.Widget):
    """
    Create a scrollable frame inside the parent widget.

    Args:
        parent: The parent widget.

    Returns:
        tuple: (canvas, scrollable_frame) — place widgets inside scrollable_frame.
    """
    canvas = tk.Canvas(parent, bg="#f5f5f5", highlightthickness=0)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Mouse wheel scrolling
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

    return canvas, scrollable_frame


# ─────────────────────────────────────────────
# Notification Popup
# ─────────────────────────────────────────────

def show_notification(root: tk.Tk, title: str, message: str, duration_ms: int = 3000):
    """
    Show a temporary notification popup.

    Args:
        root (tk.Tk): The root window.
        title (str): Popup title.
        message (str): Popup message text.
        duration_ms (int): Time in ms before auto-close.
    """
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.geometry("300x100")
    popup.resizable(False, False)
    popup.attributes('-topmost', True)

    ttk.Label(popup, text=message, font=("Segoe UI", 11), wraplength=260).pack(pady=20, padx=10)
    popup.after(duration_ms, popup.destroy)


# ─────────────────────────────────────────────
# Card Frame Helper
# ─────────────────────────────────────────────

def create_card(parent: tk.Widget, title: str = "") -> ttk.Frame:
    """
    Create a styled card frame with an optional title label.

    Args:
        parent: Parent widget.
        title (str): Section title shown at the top of the card.

    Returns:
        ttk.Frame: The inner content frame.
    """
    outer = ttk.Frame(parent, style="Card.TFrame", padding=10)
    outer.pack(fill=tk.X, padx=15, pady=8)

    if title:
        ttk.Label(outer, text=title, font=("Segoe UI", 12, "bold"), background="white").pack(anchor="w")
        ttk.Separator(outer, orient="horizontal").pack(fill=tk.X, pady=5)

    return outer
