import customtkinter as ctk

# ---------------- Initialize App ----------------
ctk.set_appearance_mode("dark")  # Dark mode
ctk.set_default_color_theme("blue")  # Default theme

root = ctk.CTk()
root.title("Online Music System - Home")
root.geometry("800x500")
root.resizable(False, False)

# ---------------- Sidebar Navigation ----------------
sidebar = ctk.CTkFrame(root, width=200, height=500, fg_color="#2d3748")
sidebar.pack(side="left", fill="y")

# Sidebar Title
title_label = ctk.CTkLabel(sidebar, text="🎵 Online Music System", font=("Arial", 14, "bold"), text_color="white")
title_label.pack(pady=15)

# Sidebar Buttons
menu_items = [
    ("🏠 Home", "#9f7aea"),
    ("🎵 Playlist", "#"),
    ("⭐ Featured", "#"),
    ("⬇️ Download", "#"),
    ("🎧 Recommend Songs", "#"),
    ("🚪 Logout", "#FF4C4C")
]

for text, color in menu_items:
    btn = ctk.CTkButton(sidebar, text=text, font=("Arial", 11), fg_color="#2d3748", hover_color="#4a5568", text_color="white",
                        corner_radius=0)
    btn.pack(fill="x", pady=3)

# ---------------- Music Player Controls ----------------
player_frame = ctk.CTkFrame(sidebar, fg_color="#2d3748")
player_frame.pack(side="bottom", pady=10)

prev_btn = ctk.CTkButton(player_frame, text="⏮️", font=("Arial", 14), fg_color="#2d3748", hover_color="#4a5568", width=40)
prev_btn.pack(side="left", padx=5)

play_btn = ctk.CTkButton(player_frame, text="▶️", font=("Arial", 14), fg_color="#2d3748", hover_color="#4a5568", width=40)
play_btn.pack(side="left", padx=5)

next_btn = ctk.CTkButton(player_frame, text="⏭️", font=("Arial", 14), fg_color="#2d3748", hover_color="#4a5568", width=40)
next_btn.pack(side="left", padx=5)

# ---------------- Main Content ----------------
main_content = ctk.CTkFrame(root, fg_color="#1a202c", width=600, height=500)
main_content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

# Header Section
header_frame = ctk.CTkFrame(main_content, fg_color="#1a202c")
header_frame.pack(fill="x", pady=5)

header_label = ctk.CTkLabel(header_frame, text="🏠 Home", font=("Arial", 16, "bold"), text_color="white")
header_label.pack(side="left")

user_label = ctk.CTkLabel(header_frame, text="Hello, User!", font=("Arial", 11), text_color="gray")
user_label.pack(side="right")

# ---------------- Hero Section ----------------
hero_section = ctk.CTkFrame(main_content, fg_color="#1a202c")
hero_section.pack(fill="x", pady=15)

hero_title = ctk.CTkLabel(hero_section, text="🎶 Discover Music & Play Instantly", font=("Arial", 14, "bold"), text_color="#9f7aea")
hero_title.pack(pady=5)

hero_info = ctk.CTkLabel(hero_section, text="Explore top trending songs, curated playlists, and personalized recommendations.",
                         font=("Arial", 10), text_color="gray")
hero_info.pack()

# Buttons for Quick Access
buttons_frame = ctk.CTkFrame(hero_section, fg_color="#1a202c")
buttons_frame.pack(pady=10)

buttons = [
    ("🔥 Trending", "#2563eb"),
    ("🎵 Playlists", "#16a34a"),
    ("⬇️ Download", "#9f7aea")
]

for text, color in buttons:
    action_btn = ctk.CTkButton(buttons_frame, text=text, font=("Arial", 12, "bold"), fg_color=color, text_color="white",
                               corner_radius=8, height=35)
    action_btn.pack(side="left", padx=5)

# ---------------- Featured Songs ----------------
featured_section = ctk.CTkFrame(main_content, fg_color="#1a202c")
featured_section.pack(fill="x", pady=15)

featured_title = ctk.CTkLabel(featured_section, text="🔥 Featured Songs", font=("Arial", 14, "bold"), text_color="#9f7aea")
featured_title.pack(anchor="w", pady=5)

featured_frame = ctk.CTkFrame(featured_section, fg_color="#1a202c")
featured_frame.pack(fill="x", pady=5)

# Featured Songs
featured_songs = [
    ("Blinding Lights", "The Weeknd"),
    ("Levitating", "Dua Lipa"),
    ("Shape of You", "Ed Sheeran")
]

def select_song(song_frame):
    for widget in featured_frame.winfo_children():
        widget.configure(fg_color="#2d3748")  # Reset all backgrounds
    song_frame.configure(fg_color="#4C4C6D")  # Highlight selected song

for song, artist in featured_songs:
    song_card = ctk.CTkFrame(featured_frame, fg_color="#2d3748", width=150, height=80, corner_radius=10)
    song_card.pack(side="left", padx=5, pady=5)

    song_label = ctk.CTkLabel(song_card, text=song, font=("Arial", 11, "bold"), text_color="white")
    song_label.pack()

    artist_label = ctk.CTkLabel(song_card, text=artist, font=("Arial", 9), text_color="gray")
    artist_label.pack()

    song_card.bind("<Button-1>", lambda e, frame=song_card: select_song(frame))

# ---------------- Run Application ----------------
root.mainloop()
