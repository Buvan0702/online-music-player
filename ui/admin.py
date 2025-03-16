import tkinter as tk
from tkinter import ttk

# ---------------- Main Application Window ----------------
root = tk.Tk()
root.title("Online Music System - Admin Dashboard")
root.geometry("800x500")  # Fixed window size
root.resizable(False, False)  # Prevent resizing
root.configure(bg="#1a202c")  # Dark background

# ---------------- Sidebar Navigation ----------------
sidebar = tk.Frame(root, bg="#2d3748", width=200, height=500)
sidebar.pack(side="left", fill="y")

# Sidebar Title
title_label = tk.Label(sidebar, text="🛠 Admin Dashboard", font=("Arial", 14, "bold"), bg="#2d3748", fg="white")
title_label.pack(pady=15)

# Sidebar Buttons
menu_items = [
    ("📊 Dashboard", "#9f7aea"),  # Highlighted purple color
    ("👥 Manage Users", "#"),
    ("🎵 Manage Songs", "#"),
    ("📁 Manage Playlists", "#"),
    ("📊 Reports & Analytics", "#"),
    ("🚪 Logout", "#FF4C4C")  # Red for logout
]

for text, color in menu_items:
    btn = tk.Button(sidebar, text=text, font=("Arial", 11), fg="white", bg="#2d3748", relief="flat", anchor="w",
                    padx=10, activebackground="#4a5568", activeforeground="white", bd=0)
    btn.pack(fill="x", pady=3)

# ---------------- Main Content ----------------
main_content = tk.Frame(root, bg="#1a202c", width=600, height=500)
main_content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

# Header Section
header_frame = tk.Frame(main_content, bg="#1a202c")
header_frame.pack(fill="x", pady=5)

header_label = tk.Label(header_frame, text="📊 Admin Dashboard", font=("Arial", 16, "bold"), bg="#1a202c", fg="white")
header_label.pack(side="left")

user_label = tk.Label(header_frame, text="Hello, Admin!", font=("Arial", 11), bg="#1a202c", fg="gray")
user_label.pack(side="right")

# ---------------- Quick Overview ----------------
overview_section = tk.Frame(main_content, bg="#1a202c")
overview_section.pack(fill="x", pady=15)

overview_title = tk.Label(overview_section, text="📌 Quick Overview", font=("Arial", 14, "bold"),
                          bg="#1a202c", fg="#9f7aea")
overview_title.pack(anchor="w", pady=5)

# Stats Grid
stats_frame = tk.Frame(overview_section, bg="#1a202c")
stats_frame.pack(fill="x")

stats = [
    ("👥 Total Users", "150", "#16a34a"),  # Green
    ("🎵 Total Songs", "320", "#2563eb"),  # Blue
    ("📁 Playlists Created", "45", "#facc15"),  # Yellow
    ("⬇️ Total Downloads", "780", "#dc2626")  # Red
]

for name, value, color in stats:
    stat_card = tk.Frame(stats_frame, bg="#2d3748", width=150, height=80, relief="flat", bd=2)
    stat_card.pack(side="left", padx=10, pady=5)

    stat_icon = tk.Label(stat_card, text=name, font=("Arial", 10, "bold"), fg="white", bg="#2d3748")
    stat_icon.pack(pady=5)

    stat_value = tk.Label(stat_card, text=value, font=("Arial", 14, "bold"), fg=color, bg="#2d3748")
    stat_value.pack()

# ---------------- Admin Actions ----------------
actions_section = tk.Frame(main_content, bg="#1a202c")
actions_section.pack(fill="x", pady=15)

actions_title = tk.Label(actions_section, text="⚙️ Manage", font=("Arial", 14, "bold"),
                         bg="#1a202c", fg="#9f7aea")
actions_title.pack(anchor="w", pady=5)

actions_frame = tk.Frame(actions_section, bg="#1a202c")
actions_frame.pack(fill="x")

# Action Buttons
buttons = [
    ("👥 Manage Users", "#9f7aea"),
    ("🎵 Manage Songs", "#2563eb"),
    ("📁 Manage Playlists", "#facc15")
]

for text, color in buttons:
    action_btn = tk.Button(actions_frame, text=text, font=("Arial", 12, "bold"), bg=color, fg="white",
                           relief="flat", cursor="hand2", height=2, activebackground="#6b46c1")
    action_btn.pack(side="left", padx=10, pady=5)

# ---------------- Run Application ----------------
root.mainloop()
