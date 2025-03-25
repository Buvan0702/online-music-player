import customtkinter as ctk

# ---------------- Initialize App ----------------
ctk.set_appearance_mode("dark")  # Enable dark mode
ctk.set_default_color_theme("blue")  # Set color theme

root = ctk.CTk()
root.title("Online Music System - Recommended Songs")
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
    ("🏠  Home", "#"),
    ("🎵  Playlist", "#"),
    ("⭐  Featured", "#"),
    ("⬇️  Download", "#"),
    ("🎧  Recommend Songs", "#9f7aea"),  # Highlighted purple color
    ("🚪  Logout", "#FF4C4C")  # Red for logout
]

for text, color in menu_items:
    btn = ctk.CTkButton(sidebar, text=text, font=("Arial", 11), fg_color="#2d3748", hover_color="#4a5568",
                        text_color="white", corner_radius=0)
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

header_label = ctk.CTkLabel(header_frame, text="🎧 Recommended Songs", font=("Arial", 16, "bold"), text_color="white")
header_label.pack(side="left")

user_label = ctk.CTkLabel(header_frame, text="Hello, User!", font=("Arial", 11), text_color="gray")
user_label.pack(side="right")

# ---------------- Recommended Songs Section ----------------
recommended_section = ctk.CTkFrame(main_content, fg_color="#1a202c")
recommended_section.pack(fill="x", pady=15)

recommended_title = ctk.CTkLabel(recommended_section, text="🎵 Songs You Might Like 🎶", font=("Arial", 14, "bold"),
                                 text_color="#9f7aea")
recommended_title.pack(pady=5)

recommended_info = ctk.CTkLabel(recommended_section, text="Discover music based on your taste.",
                                font=("Arial", 10), text_color="gray")
recommended_info.pack()

# Song List Frame
song_frame = ctk.CTkFrame(recommended_section, fg_color="#1a202c")
song_frame.pack(pady=10)

# Recommended Songs
songs = [
    "🎧 The Weeknd - Blinding Lights",
    "🎶 Dua Lipa - Levitating",
    "🎸 Imagine Dragons - Believer",
    "🎵 Ed Sheeran - Shape of You"
]

for song in songs:
    song_label = ctk.CTkLabel(song_frame, text=song, font=("Arial", 11, "bold"), fg_color="#2d3748", text_color="white",
                              width=250, height=30, corner_radius=10)
    song_label.pack(pady=3)

# ---------------- Refresh Button ----------------
refresh_button = ctk.CTkButton(recommended_section, text="🔄 Refresh", font=("Arial", 12, "bold"), fg_color="#9f7aea",
                               hover_color="#6b46c1", text_color="white", height=40, corner_radius=10)
refresh_button.pack(pady=10)

# ---------------- Run Application ----------------
root.mainloop()
