import customtkinter as ctk
from tkinter import filedialog

# ---------------- Initialize App ----------------
ctk.set_appearance_mode("dark")  # Enable dark mode
ctk.set_default_color_theme("blue")  # Set color theme

root = ctk.CTk()
root.title("Online Music System - Download Songs")
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
    ("🏠 Home", "#"),
    ("🎵 Playlist", "#"),
    ("⭐ Featured", "#"),
    ("⬇️ Download Songs", "#9f7aea"),  # Highlighted purple color
    ("🎧 Recommend Songs", "#"),
    ("🚪 Logout", "#FF4C4C")  # Red for logout
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

header_label = ctk.CTkLabel(header_frame, text="⬇️ Download Songs", font=("Arial", 16, "bold"), text_color="white")
header_label.pack(side="left")

user_label = ctk.CTkLabel(header_frame, text="Hello, User!", font=("Arial", 11), text_color="gray")
user_label.pack(side="right")

# ---------------- Song Selection Section ----------------
download_section = ctk.CTkFrame(main_content, fg_color="#1a202c")
download_section.pack(fill="x", pady=15)

download_title = ctk.CTkLabel(download_section, text="🎵 Download Your Favorite Songs", font=("Arial", 14, "bold"),
                              text_color="#9f7aea")
download_title.pack(pady=5)

download_info = ctk.CTkLabel(download_section, text="Select a song to download or upload your own.",
                             font=("Arial", 10), text_color="gray")
download_info.pack()

# Song List Frame
song_frame = ctk.CTkFrame(download_section, fg_color="#1a202c")
song_frame.pack(pady=10)

# Function to Select a Song
selected_song = None  # Variable to track selected song

def select_song(song_label, song_name):
    global selected_song
    for widget in song_frame.winfo_children():
        widget.configure(fg_color="#2d3748")  # Reset all backgrounds
    song_label.configure(fg_color="#4C4C6D")  # Highlight selected song
    selected_song = song_name  # Store selected song

# Songs Available for Download
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
    song_label.bind("<Button-1>", lambda e, lbl=song_label, s=song: select_song(lbl, s))

# ---------------- Upload Song Section ----------------
upload_section = ctk.CTkFrame(download_section, fg_color="#1a202c")
upload_section.pack(pady=10)

upload_label = ctk.CTkLabel(upload_section, text="📁 Upload Your Own Song", font=("Arial", 11, "bold"),
                            text_color="gray")
upload_label.pack()

def upload_song():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.flac")])
    if file_path:
        upload_label.configure(text=f"Uploaded: {file_path.split('/')[-1]}", text_color="green")

upload_btn = ctk.CTkButton(upload_section, text="📤 Choose File", font=("Arial", 11, "bold"), fg_color="#4a5568",
                           hover_color="#6b7280", text_color="white", corner_radius=10, command=upload_song)
upload_btn.pack(pady=5)

# ---------------- Download & Upload Buttons ----------------
buttons_section = ctk.CTkFrame(download_section, fg_color="#1a202c")
buttons_section.pack(pady=15)

def download_song():
    if selected_song:
        print(f"Downloading: {selected_song}")  # Simulate download action
    else:
        print("No song selected!")

download_button = ctk.CTkButton(buttons_section, text="⬇️ Download Selected", font=("Arial", 12, "bold"),
                                fg_color="#9f7aea", hover_color="#6b46c1", text_color="white", height=40,
                                corner_radius=10, command=download_song)
download_button.pack(side="left", padx=5)

upload_button = ctk.CTkButton(buttons_section, text="📤 Upload", font=("Arial", 12, "bold"), fg_color="#16a34a",
                              hover_color="#15803d", text_color="white", height=40, corner_radius=10,
                              command=upload_song)
upload_button.pack(side="left", padx=5)

# ---------------- Run Application ----------------
root.mainloop()
