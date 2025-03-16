import tkinter as tk
from tkinter import ttk

# ---------------- Main Application Window ----------------
root = tk.Tk()
root.title("Online Music System - Home")
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
    ("🏠 Home", "#9f7aea"),  # Highlighted purple color
    ("🎵 Playlist", "#"),
    ("⭐ Featured", "#"),
    ("⬇️ Download", "#"),
    ("🎧 Recommend Songs", "#"),
    ("🚪 Logout", "#FF4C4C")  # Red for logout
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

header_label = tk.Label(header_frame, text="🏠 Home", font=("Arial", 16, "bold"), bg="#1a202c", fg="white")
header_label.pack(side="left")

user_label = tk.Label(header_frame, text="Hello, User!", font=("Arial", 11), bg="#1a202c", fg="gray")
user_label.pack(side="right")

# ---------------- Hero Section ----------------
hero_section = tk.Frame(main_content, bg="#1a202c")
hero_section.pack(fill="x", pady=15)

hero_title = tk.Label(hero_section, text="🎶 Discover Music & Play Instantly", font=("Arial", 14, "bold"),
                       bg="#1a202c", fg="#9f7aea")
hero_title.pack(pady=5)

hero_info = tk.Label(hero_section, text="Explore top trending songs, curated playlists, and personalized recommendations.",
                     font=("Arial", 10), bg="#1a202c", fg="gray")
hero_info.pack()

# Buttons for Quick Access
buttons_frame = tk.Frame(hero_section, bg="#1a202c")
buttons_frame.pack(pady=10)

buttons = [
    ("🔥 Trending", "#2563eb"),
    ("🎵 Playlists", "#16a34a"),
    ("⬇️ Download", "#9f7aea")
]

for text, color in buttons:
    action_btn = tk.Button(buttons_frame, text=text, font=("Arial", 12, "bold"), bg=color, fg="white",
                           relief="flat", cursor="hand2", height=2, activebackground="#6b46c1")
    action_btn.pack(side="left", padx=5)

# ---------------- Featured Songs ----------------
featured_section = tk.Frame(main_content, bg="#1a202c")
featured_section.pack(fill="x", pady=15)

featured_title = tk.Label(featured_section, text="🔥 Featured Songs", font=("Arial", 14, "bold"),
                           bg="#1a202c", fg="#9f7aea")
featured_title.pack(anchor="w", pady=5)

featured_frame = tk.Frame(featured_section, bg="#1a202c")
featured_frame.pack(fill="x", pady=5)

# Featured Songs
featured_songs = [
    ("Blinding Lights", "The Weeknd"),
    ("Levitating", "Dua Lipa"),
    ("Shape of You", "Ed Sheeran")
]

def select_song(song_label):
    for widget in featured_frame.winfo_children():
        widget.config(bg="#2d3748")  # Reset all backgrounds
    song_label.config(bg="#4C4C6D")  # Highlight selected song

for song, artist in featured_songs:
    song_card = tk.Frame(featured_frame, bg="#2d3748", width=150, height=80, relief="flat", bd=2)
    song_card.pack(side="left", padx=5, pady=5)

    song_label = tk.Label(song_card, text=song, font=("Arial", 11, "bold"), fg="white", bg="#2d3748", cursor="hand2")
    song_label.pack()

    artist_label = tk.Label(song_card, text=artist, font=("Arial", 9), fg="gray", bg="#2d3748")
    artist_label.pack()

    song_label.bind("<Button-1>", lambda e, lbl=song_card: select_song(lbl))

# ---------------- Run Application ----------------
root.mainloop()
