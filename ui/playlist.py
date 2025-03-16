import tkinter as tk
from tkinter import ttk

# ---------------- Main Application Window ----------------
root = tk.Tk()
root.title("Online Music System - Featured")
root.geometry("800x500")  # Fixed window size
root.resizable(False, False)  # Prevent resizing
root.configure(bg="#1a202c")  # Dark background

# ---------------- Sidebar Navigation ----------------
sidebar = tk.Frame(root, bg="#2d3748", width=200, height=500)
sidebar.pack(side="left", fill="y")

# Sidebar Title
title_label = tk.Label(sidebar, text="🎵 Online Music System", font=("Arial", 14, "bold"), bg="#2d3748", fg="white")
title_label.pack(pady=15)

# Sidebar Buttons
menu_items = [
    ("🏠  Home", "#"),
    ("🎵  Playlist", "#"),
    ("⭐  Featured", "#9f7aea"),  # Highlighted purple color
    ("⬇️  Download", "#"),
    ("🎧  Recommend Songs", "#"),
    ("🚪  Logout", "#FF4C4C")  # Red for logout
]

for text, color in menu_items:
    btn = tk.Button(sidebar, text=text, font=("Arial", 11), fg="white", bg="#2d3748", relief="flat", anchor="w",
                    padx=10, activebackground="#4a5568", activeforeground="white", bd=0)
    btn.pack(fill="x", pady=3)

# ---------------- Music Player Controls ----------------
player_frame = tk.Frame(sidebar, bg="#2d3748")
player_frame.pack(side="bottom", pady=10)

prev_btn = tk.Button(player_frame, text="⏮️", font=("Arial", 14), fg="white", bg="#2d3748", relief="flat",
                      activebackground="#4a5568")
prev_btn.pack(side="left", padx=5)

play_btn = tk.Button(player_frame, text="▶️", font=("Arial", 14), fg="white", bg="#2d3748", relief="flat",
                      activebackground="#4a5568")
play_btn.pack(side="left", padx=5)

next_btn = tk.Button(player_frame, text="⏭️", font=("Arial", 14), fg="white", bg="#2d3748", relief="flat",
                      activebackground="#4a5568")
next_btn.pack(side="left", padx=5)

# ---------------- Main Content ----------------
main_content = tk.Frame(root, bg="#1a202c", width=600, height=500)
main_content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

# Header Section
header_frame = tk.Frame(main_content, bg="#1a202c")
header_frame.pack(fill="x", pady=5)

header_label = tk.Label(header_frame, text="⭐ Featured", font=("Arial", 16, "bold"), bg="#1a202c", fg="white")
header_label.pack(side="left")

user_label = tk.Label(header_frame, text="Hello, User!", font=("Arial", 11), bg="#1a202c", fg="gray")
user_label.pack(side="right")

# ---------------- Featured Playlists ----------------
featured_section = tk.Frame(main_content, bg="#1a202c")
featured_section.pack(fill="x", pady=15)

featured_title = tk.Label(featured_section, text="🎶 Our Playlists:", font=("Arial", 14, "bold"),
                           bg="#1a202c", fg="#9f7aea")
featured_title.pack(anchor="w", pady=5)

featured_frame = tk.Frame(featured_section, bg="#1a202c")
featured_frame.pack(fill="x", pady=5)

# Playlist Buttons
playlists = ["Coding", "LoFi", "Bass"]
for name in playlists:
    btn = tk.Button(featured_frame, text=name, font=("Arial", 12, "bold"), fg="white", bg="#2d3748",
                    relief="flat", width=10, height=2, cursor="hand2", activebackground="#4C4C6D")
    btn.pack(side="left", padx=5)

# ---------------- User Playlists ----------------
user_section = tk.Frame(main_content, bg="#1a202c")
user_section.pack(fill="x", pady=15)

user_title = tk.Label(user_section, text="📁 Your Playlists:", font=("Arial", 14, "bold"),
                      bg="#1a202c", fg="#9f7aea")
user_title.pack(anchor="w", pady=5)

user_frame = tk.Frame(user_section, bg="#1a202c")
user_frame.pack(fill="x", pady=5)

# Add New Playlist Button
add_playlist_btn = tk.Button(user_frame, text="+", font=("Arial", 14, "bold"), fg="gray", bg="#4a5568",
                             relief="flat", width=5, height=2, cursor="hand2", activebackground="#6b7280")
add_playlist_btn.pack(side="left", padx=5)

# User Playlists
user_playlists = ["Playlist 1", "Playlist 2"]
for name in user_playlists:
    btn = tk.Button(user_frame, text=name, font=("Arial", 12, "bold"), fg="white", bg="#2d3748",
                    relief="flat", width=10, height=2, cursor="hand2", activebackground="#4C4C6D")
    btn.pack(side="left", padx=5)

# ---------------- Run Application ----------------
root.mainloop()
