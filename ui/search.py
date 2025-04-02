import customtkinter as ctk

# ---------------- Initialize App ----------------
ctk.set_appearance_mode("dark")  # Dark mode
ctk.set_default_color_theme("blue")  # Default theme

root = ctk.CTk()
root.title("Online Music System - Search Songs")
root.geometry("1000x600")  # Adjusted to match the image proportions
root.resizable(False, False)

# ---------------- Main Frame ----------------
main_frame = ctk.CTkFrame(root, fg_color="#1E1E2E", corner_radius=15)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# ---------------- Sidebar Navigation ----------------
sidebar = ctk.CTkFrame(main_frame, width=250, height=580, fg_color="#111827", corner_radius=10)
sidebar.pack(side="left", fill="y", padx=(10, 0), pady=10)

# Sidebar Title
title_label = ctk.CTkLabel(sidebar, text="Online Music\nSystem", font=("Arial", 20, "bold"), text_color="white")
title_label.pack(pady=(25, 30))

# Sidebar Menu Items
menu_items = [
    ("🏠 Home", "#111827", "#A0A0A0"),
    ("🔍 Search", "#111827", "white"),  # Highlighted as active
    ("🎵 Playlist", "#111827", "#A0A0A0"),
    ("⬇️ Download", "#111827", "#A0A0A0"),
    ("🎧 Recommend Songs", "#111827", "#A0A0A0"),
    ("🚪 Logout", "#111827", "#A0A0A0")
]

for text, bg_color, text_color in menu_items:
    btn = ctk.CTkButton(sidebar, text=text, font=("Arial", 14), 
                      fg_color=bg_color, hover_color="#1E293B", text_color=text_color,
                      anchor="w", corner_radius=0, height=40)
    btn.pack(fill="x", pady=5, padx=10)

# Music player controls at bottom of sidebar
player_frame = ctk.CTkFrame(sidebar, fg_color="#111827", height=50)
player_frame.pack(side="bottom", fill="x", pady=20, padx=10)

# Control buttons
prev_btn = ctk.CTkButton(player_frame, text="⏮️", font=("Arial", 18), 
                         fg_color="#111827", hover_color="#1E293B", width=40, height=40)
prev_btn.pack(side="left", padx=10)

play_btn = ctk.CTkButton(player_frame, text="▶️", font=("Arial", 18), 
                         fg_color="#111827", hover_color="#1E293B", width=40, height=40)
play_btn.pack(side="left", padx=10)

next_btn = ctk.CTkButton(player_frame, text="⏭️", font=("Arial", 18), 
                         fg_color="#111827", hover_color="#1E293B", width=40, height=40)
next_btn.pack(side="left", padx=10)

# ---------------- Main Content ----------------
content_frame = ctk.CTkFrame(main_frame, fg_color="#131B2E", corner_radius=10)
content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Header with username
header_frame = ctk.CTkFrame(content_frame, fg_color="#131B2E", height=40)
header_frame.pack(fill="x", padx=20, pady=(20, 0))

# Left side: Search Songs
search_label = ctk.CTkLabel(header_frame, text="Search Songs", font=("Arial", 24, "bold"), text_color="white")
search_label.pack(side="left")

# Right side: Username
user_label = ctk.CTkLabel(header_frame, text="Hello, User!", font=("Arial", 14), text_color="#A0A0A0")
user_label.pack(side="right")

# ---------------- Search Bar ----------------
search_frame = ctk.CTkFrame(content_frame, fg_color="#131B2E")
search_frame.pack(fill="x", padx=20, pady=(30, 20))

# Search entry with rounded corners
search_entry = ctk.CTkEntry(search_frame, 
                          placeholder_text="Search for songs, artists, or albums...",
                          font=("Arial", 14), text_color="#FFFFFF",
                          fg_color="#1A1A2E", border_color="#2A2A4E", 
                          height=45, corner_radius=10)
search_entry.pack(fill="x")

# ---------------- Available Songs Section ----------------
songs_section = ctk.CTkFrame(content_frame, fg_color="#131B2E")
songs_section.pack(fill="both", expand=True, padx=20, pady=10)

# Section title
songs_title = ctk.CTkLabel(songs_section, text="Available Songs 🎵", 
                          font=("Arial", 20, "bold"), text_color="#B146EC")
songs_title.pack(anchor="w", pady=(0, 15))

# Song list
songs = [
    ("🎧 The Weeknd - Blinding Lights", "headphones"),
    ("🎵 Dua Lipa - Levitating", "musical_note"),
    ("🎸 Imagine Dragons - Believer", "guitar"),
    ("🎵 Ed Sheeran - Shape of You", "musical_note"),
    ("🎵 Post Malone - Circles", "musical_note"),
    ("🎧 Taylor Swift - Shake It Off", "headphones")
]

def play_song(song_name):
    print(f"Playing {song_name}")
    # In a real app, this would trigger the song to play

for i, (song, icon) in enumerate(songs):
    # Create a frame for each song row
    song_frame = ctk.CTkFrame(songs_section, fg_color="#1A1A2E", corner_radius=10, height=50)
    song_frame.pack(fill="x", pady=5)
    
    # Song name
    song_label = ctk.CTkLabel(song_frame, text=song, 
                            font=("Arial", 14), text_color="white",
                            anchor="w")
    song_label.pack(side="left", padx=15, fill="y")
    
    # Instead of using CTkButton with an image, we'll use a label for the play icon
    
    # Using an emoji as a button since we can't load images directly
    play_icon = ctk.CTkLabel(song_frame, text="▶️", font=("Arial", 16), text_color="#22C55E")
    play_icon.pack(side="right", padx=15)
    
    # Make the whole row clickable
    song_frame.bind("<Button-1>", lambda e, s=song.split(" - ")[1]: play_song(s))
    song_label.bind("<Button-1>", lambda e, s=song.split(" - ")[1]: play_song(s))
    play_icon.bind("<Button-1>", lambda e, s=song.split(" - ")[1]: play_song(s))

# ---------------- Run Application ----------------
root.mainloop()