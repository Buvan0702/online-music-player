import customtkinter as ctk

# ---------------- Initialize App ----------------
ctk.set_appearance_mode("dark")  # Dark mode
ctk.set_default_color_theme("blue")  # Default theme

root = ctk.CTk()
root.title("Online Music System - Recommended Songs")
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
    ("🔍 Search", "#111827", "#A0A0A0"),
    ("🎵 Playlist", "#111827", "#A0A0A0"),
    ("⬇️ Download", "#111827", "#A0A0A0"),
    ("🎧 Recommend Songs", "#111827", "white"),  # Highlighted as active
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

# Left side: Recommended Songs
recommend_label = ctk.CTkLabel(header_frame, text="Recommended Songs", font=("Arial", 24, "bold"), text_color="white")
recommend_label.pack(side="left")

# Right side: Username
user_label = ctk.CTkLabel(header_frame, text="Hello, User!", font=("Arial", 14), text_color="#A0A0A0")
user_label.pack(side="right")

# ---------------- Songs You Might Like ----------------
songs_frame = ctk.CTkFrame(content_frame, fg_color="#131B2E")
songs_frame.pack(fill="both", expand=True, padx=20, pady=(40, 0))

# Section title - centered
title_label = ctk.CTkLabel(songs_frame, text="Songs You Might Like 🎵", 
                          font=("Arial", 24, "bold"), text_color="#B146EC")
title_label.pack(pady=(0, 5))

# Subtitle - centered
subtitle_label = ctk.CTkLabel(songs_frame, text="Discover music based on your taste.", 
                             font=("Arial", 14), text_color="#A0A0A0")
subtitle_label.pack(pady=(0, 20))

# Songs list
songs = [
    ("🎧 The Weeknd - Blinding Lights", "1A1A2E"),
    ("🎵 Dua Lipa - Levitating", "1A1A2E"),
    ("🎸 Imagine Dragons - Believer", "1A1A2E"),
    ("🎵 Ed Sheeran - Shape of You", "1A1A2E")
]

# Create song rows
for song, bg_color in songs:
    song_frame = ctk.CTkFrame(songs_frame, fg_color=f"#{bg_color}", corner_radius=10, height=50)
    song_frame.pack(fill="x", pady=5, ipady=5)
    
    # Make sure the frame stays at desired height
    song_frame.pack_propagate(False)
    
    # Song label with icon
    song_label = ctk.CTkLabel(song_frame, text=song, font=("Arial", 14), text_color="white")
    song_label.place(relx=0.5, rely=0.5, anchor="center")

# Refresh button at the bottom
button_frame = ctk.CTkFrame(songs_frame, fg_color="#131B2E")
button_frame.pack(pady=25)

refresh_button = ctk.CTkButton(button_frame, text="⟳ Refresh", font=("Arial", 14, "bold"), 
                              fg_color="#B146EC", hover_color="#9333EA", 
                              corner_radius=5, height=40, width=140)
refresh_button.pack()

# ---------------- Run Application ----------------
root.mainloop()