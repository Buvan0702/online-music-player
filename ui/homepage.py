import customtkinter as ctk

# ---------------- Initialize App ----------------
ctk.set_appearance_mode("dark")  # Dark mode
ctk.set_default_color_theme("blue")  # Default theme

root = ctk.CTk()
root.title("Online Music System - Home")
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
    ("🏠 Home", "#111827", "white"),
    ("🔍 Search", "#111827", "#A0A0A0"),
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

# Left side: Home
home_label = ctk.CTkLabel(header_frame, text="Home", font=("Arial", 18, "bold"), text_color="white")
home_label.pack(side="left")

# Right side: Username
user_label = ctk.CTkLabel(header_frame, text="Hello, User!", font=("Arial", 14), text_color="#A0A0A0")
user_label.pack(side="right")

# ---------------- Hero Section ----------------
hero_frame = ctk.CTkFrame(content_frame, fg_color="#131B2E")
hero_frame.pack(fill="x", padx=20, pady=(40, 20))

# Main title
title_label = ctk.CTkLabel(hero_frame, text="Discover Music & Play Instantly", 
                          font=("Arial", 28, "bold"), text_color="#B146EC")
title_label.pack(anchor="w")

# Subtitle
subtitle_label = ctk.CTkLabel(hero_frame, 
                             text="Explore top trending songs, curated playlists, and personalized recommendations.", 
                             font=("Arial", 14), text_color="#A0A0A0")
subtitle_label.pack(anchor="w", pady=(10, 20))

# Action Buttons
button_frame = ctk.CTkFrame(hero_frame, fg_color="#131B2E")
button_frame.pack(anchor="w")

# Trending button
trending_btn = ctk.CTkButton(button_frame, text="🔥 Trending", font=("Arial", 14, "bold"), 
                            fg_color="#2563EB", hover_color="#1D4ED8", 
                            corner_radius=8, height=40, width=150)
trending_btn.pack(side="left", padx=(0, 10))

# Playlists button
playlists_btn = ctk.CTkButton(button_frame, text="🎵 Playlists", font=("Arial", 14, "bold"), 
                             fg_color="#16A34A", hover_color="#15803D", 
                             corner_radius=8, height=40, width=150)
playlists_btn.pack(side="left", padx=10)

# Download button
download_btn = ctk.CTkButton(button_frame, text="⬇️ Download", font=("Arial", 14, "bold"), 
                            fg_color="#B146EC", hover_color="#9333EA", 
                            corner_radius=8, height=40, width=150)
download_btn.pack(side="left", padx=10)

# ---------------- Featured Songs Section ----------------
featured_frame = ctk.CTkFrame(content_frame, fg_color="#131B2E")
featured_frame.pack(fill="x", padx=20, pady=20)

# Section title
featured_title = ctk.CTkLabel(featured_frame, text="🔥 Featured Songs", 
                             font=("Arial", 18, "bold"), text_color="#B146EC")
featured_title.pack(anchor="w", pady=(0, 20))

# Song cards container
songs_frame = ctk.CTkFrame(featured_frame, fg_color="#131B2E")
songs_frame.pack(fill="x")

# Featured Songs
featured_songs = [
    ("Blinding\nLights", "The\nWeeknd"),
    ("Levitating", "Dua Lipa"),
    ("Shape of\nYou", "Ed\nSheeran")
]

# Create song cards
for song, artist in featured_songs:
    # Create song card
    song_card = ctk.CTkFrame(songs_frame, fg_color="#1A1A2E", corner_radius=10, 
                            width=150, height=180)
    song_card.pack(side="left", padx=10)
    
    # Add some minimum width to ensure cards display properly
    song_card.pack_propagate(False)
    
    # Center the text vertically by adding a spacer frame
    spacer = ctk.CTkFrame(song_card, fg_color="#1A1A2E", height=30)
    spacer.pack(side="top")
    
    # Song title with larger font
    song_label = ctk.CTkLabel(song_card, text=song, 
                             font=("Arial", 16, "bold"), text_color="white")
    song_label.pack(pady=(5, 0))
    
    # Artist name below with smaller font
    artist_label = ctk.CTkLabel(song_card, text=artist, 
                               font=("Arial", 12), text_color="#A0A0A0")
    artist_label.pack(pady=(5, 0))

# ---------------- Run Application ----------------
root.mainloop()