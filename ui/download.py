import tkinter as tk
from tkinter import ttk, filedialog

# ---------------- Main Application Window ----------------
root = tk.Tk()
root.title("Online Music System - Download Songs")
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
    ("🏠 Home", "#"),
    ("🎵 Playlist", "#"),
    ("⭐ Featured", "#"),
    ("⬇️ Download Songs", "#9f7aea"),  # Highlighted purple color
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

header_label = tk.Label(header_frame, text="⬇️ Download Songs", font=("Arial", 16, "bold"), bg="#1a202c", fg="white")
header_label.pack(side="left")

user_label = tk.Label(header_frame, text="Hello, User!", font=("Arial", 11), bg="#1a202c", fg="gray")
user_label.pack(side="right")

# ---------------- Song Selection Section ----------------
download_section = tk.Frame(main_content, bg="#1a202c")
download_section.pack(fill="x", pady=15)

download_title = tk.Label(download_section, text="🎵 Download Your Favorite Songs", font=("Arial", 14, "bold"),
                           bg="#1a202c", fg="#9f7aea")
download_title.pack(pady=5)

download_info = tk.Label(download_section, text="Select a song to download or upload your own.",
                         font=("Arial", 10), bg="#1a202c", fg="gray")
download_info.pack()

# Song List Frame
song_frame = tk.Frame(download_section, bg="#1a202c")
song_frame.pack(pady=10)

# Function to Select a Song
def select_song(song_label):
    for widget in song_frame.winfo_children():
        widget.config(bg="#2d3748")  # Reset all backgrounds
    song_label.config(bg="#4C4C6D")  # Highlight selected song

# Songs Available for Download
songs = [
    "🎧 The Weeknd - Blinding Lights",
    "🎶 Dua Lipa - Levitating",
    "🎸 Imagine Dragons - Believer",
    "🎵 Ed Sheeran - Shape of You"
]

for song in songs:
    song_label = tk.Label(song_frame, text=song, font=("Arial", 11, "bold"), bg="#2d3748", fg="white",
                          padx=10, pady=5, width=50, relief="flat", cursor="hand2")
    song_label.pack(pady=3)
    song_label.bind("<Button-1>", lambda e, lbl=song_label: select_song(lbl))

# ---------------- Upload Song Section ----------------
upload_section = tk.Frame(download_section, bg="#1a202c")
upload_section.pack(pady=10)

upload_label = tk.Label(upload_section, text="📁 Upload Your Own Song", font=("Arial", 11, "bold"),
                        bg="#1a202c", fg="gray")
upload_label.pack()

def upload_song():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.flac")])
    if file_path:
        upload_label.config(text=f"Uploaded: {file_path.split('/')[-1]}", fg="green")

upload_btn = tk.Button(upload_section, text="📤 Choose File", font=("Arial", 11, "bold"), bg="#4a5568", fg="white",
                        relief="flat", cursor="hand2", activebackground="#6b7280", command=upload_song)
upload_btn.pack(pady=5)

# ---------------- Download & Upload Buttons ----------------
buttons_section = tk.Frame(download_section, bg="#1a202c")
buttons_section.pack(pady=15)

download_button = tk.Button(buttons_section, text="⬇️ Download Selected", font=("Arial", 12, "bold"), bg="#9f7aea", fg="white",
                            relief="flat", cursor="hand2", height=2, activebackground="#6b46c1")
download_button.pack(side="left", padx=5)

upload_button = tk.Button(buttons_section, text="📤 Upload", font=("Arial", 12, "bold"), bg="#16a34a", fg="white",
                          relief="flat", cursor="hand2", height=2, activebackground="#15803d")
upload_button.pack(side="left", padx=5)

# ---------------- Run Application ----------------
root.mainloop()
