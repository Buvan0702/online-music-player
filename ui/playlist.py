import customtkinter as ctk

# ---------------- Initialize App ----------------
ctk.set_appearance_mode("dark")  # Dark mode
ctk.set_default_color_theme("blue")  # Default theme

root = ctk.CTk()
root.title("Online Music System - Featured")
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
    ("🎵 Playlist", "#111827", "white"),  # Highlighted as active
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

# Left side: Featured
featured_label = ctk.CTkLabel(header_frame, text="Featured", font=("Arial", 24, "bold"), text_color="white")
featured_label.pack(side="left")

# Right side: Username
user_label = ctk.CTkLabel(header_frame, text="Hello, User!", font=("Arial", 14), text_color="#A0A0A0")
user_label.pack(side="right")

# ---------------- Our Playlists ----------------
our_playlists_frame = ctk.CTkFrame(content_frame, fg_color="#131B2E")
our_playlists_frame.pack(fill="x", padx=20, pady=(40, 20))

# Section title
our_playlists_title = ctk.CTkLabel(our_playlists_frame, text="Our Playlists :", 
                                  font=("Arial", 20, "bold"), text_color="#B146EC")
our_playlists_title.pack(anchor="w", pady=(0, 20))

# Playlist cards container
our_playlists_cards = ctk.CTkFrame(our_playlists_frame, fg_color="#131B2E")
our_playlists_cards.pack(fill="x")

# Playlist items
our_playlists = ["Coding", "LoFi", "Bass"]

for playlist in our_playlists:
    # Create playlist card
    card = ctk.CTkFrame(our_playlists_cards, fg_color="#1A1A2E", corner_radius=15, 
                       width=150, height=100)
    card.pack(side="left", padx=10)
    card.pack_propagate(False)  # Prevent resizing
    
    # Center text in card
    label = ctk.CTkLabel(card, text=playlist, font=("Arial", 16, "bold"), text_color="white")
    label.place(relx=0.5, rely=0.5, anchor="center")

# ---------------- Your Playlists ----------------
your_playlists_frame = ctk.CTkFrame(content_frame, fg_color="#131B2E")
your_playlists_frame.pack(fill="x", padx=20, pady=(30, 20))

# Section title
your_playlists_title = ctk.CTkLabel(your_playlists_frame, text="Your Playlists :", 
                                   font=("Arial", 20, "bold"), text_color="#B146EC")
your_playlists_title.pack(anchor="w", pady=(0, 20))

# Playlist cards container
your_playlists_cards = ctk.CTkFrame(your_playlists_frame, fg_color="#131B2E")
your_playlists_cards.pack(fill="x")

# Add new playlist button
add_playlist = ctk.CTkFrame(your_playlists_cards, fg_color="#2A2A3E", corner_radius=15, 
                           width=150, height=100)
add_playlist.pack(side="left", padx=10)
add_playlist.pack_propagate(False)  # Prevent resizing

# Add Plus sign
plus_label = ctk.CTkLabel(add_playlist, text="+", font=("Arial", 30, "bold"), text_color="#A0A0A0")
plus_label.place(relx=0.5, rely=0.5, anchor="center")

# Your playlist items
your_playlists = ["Playlist 1", "Playlist 2"]

for playlist in your_playlists:
    # Create playlist card
    card = ctk.CTkFrame(your_playlists_cards, fg_color="#1A1A2E", corner_radius=15, 
                       width=150, height=100)
    card.pack(side="left", padx=10)
    card.pack_propagate(False)  # Prevent resizing
    
    # Center text in card
    label = ctk.CTkLabel(card, text=playlist, font=("Arial", 16, "bold"), text_color="white")
    label.place(relx=0.5, rely=0.5, anchor="center")

# ---------------- Run Application ----------------
root.mainloop()