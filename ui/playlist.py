import customtkinter as ctk

# ---------------- Initialize App ----------------
ctk.set_appearance_mode("dark")  # Enable dark mode
ctk.set_default_color_theme("blue")  # Set color theme

root = ctk.CTk()
root.title("Online Music System - Featured")
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
    ("⭐  Featured", "#9f7aea"),  # Highlighted purple color
    ("⬇️  Download", "#"),
    ("🎧  Recommend Songs", "#"),
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

header_label = ctk.CTkLabel(header_frame, text="⭐ Featured", font=("Arial", 16, "bold"), text_color="white")
header_label.pack(side="left")

user_label = ctk.CTkLabel(header_frame, text="Hello, User!", font=("Arial", 11), text_color="gray")
user_label.pack(side="right")

# ---------------- Featured Playlists ----------------
featured_section = ctk.CTkFrame(main_content, fg_color="#1a202c")
featured_section.pack(fill="x", pady=15)

featured_title = ctk.CTkLabel(featured_section, text="🎶 Our Playlists:", font=("Arial", 14, "bold"), text_color="#9f7aea")
featured_title.pack(anchor="w", pady=5)

featured_frame = ctk.CTkFrame(featured_section, fg_color="#1a202c")
featured_frame.pack(fill="x", pady=5)

# Playlist Buttons
playlists = ["Coding", "LoFi", "Bass"]
for name in playlists:
    btn = ctk.CTkButton(featured_frame, text=name, font=("Arial", 12, "bold"), fg_color="#2d3748",
                        hover_color="#4C4C6D", text_color="white", width=100, height=40, corner_radius=10)
    btn.pack(side="left", padx=5)

# ---------------- User Playlists ----------------
user_section = ctk.CTkFrame(main_content, fg_color="#1a202c")
user_section.pack(fill="x", pady=15)

user_title = ctk.CTkLabel(user_section, text="📁 Your Playlists:", font=("Arial", 14, "bold"), text_color="#9f7aea")
user_title.pack(anchor="w", pady=5)

user_frame = ctk.CTkFrame(user_section, fg_color="#1a202c")
user_frame.pack(fill="x", pady=5)

# Add New Playlist Button
add_playlist_btn = ctk.CTkButton(user_frame, text="+", font=("Arial", 14, "bold"), fg_color="#4a5568",
                                 hover_color="#6b7280", text_color="gray", width=50, height=40, corner_radius=10)
add_playlist_btn.pack(side="left", padx=5)

# User Playlists
user_playlists = ["Playlist 1", "Playlist 2"]
for name in user_playlists:
    btn = ctk.CTkButton(user_frame, text=name, font=("Arial", 12, "bold"), fg_color="#2d3748",
                        hover_color="#4C4C6D", text_color="white", width=100, height=40, corner_radius=10)
    btn.pack(side="left", padx=5)

# ---------------- Run Application ----------------
root.mainloop()
