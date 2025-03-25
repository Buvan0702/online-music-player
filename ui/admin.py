import customtkinter as ctk

# ---------------- Initialize App ----------------
ctk.set_appearance_mode("dark")  # Enable dark mode
ctk.set_default_color_theme("blue")  # Set color theme

root = ctk.CTk()
root.title("Online Music System - Admin Dashboard")
root.geometry("800x500")
root.resizable(False, False)

# ---------------- Sidebar Navigation ----------------
sidebar = ctk.CTkFrame(root, width=200, height=500, fg_color="#2d3748")
sidebar.pack(side="left", fill="y")

# Sidebar Title
title_label = ctk.CTkLabel(sidebar, text="🛠 Admin Dashboard", font=("Arial", 14, "bold"), text_color="white")
title_label.pack(pady=15)

# Sidebar Buttons
menu_items = [
    ("📊 Dashboard", "#9f7aea"),  # Highlighted purple color
    ("👥 Manage Users", "#"),
    ("🎵 Manage Songs", "#"),
    ("📁 Manage Playlists", "#"),
    ("📊 Reports & Analytics", "#"),
    ("🚪 Logout", "#FF4C4C")  # Red for logout
]

for text, color in menu_items:
    btn = ctk.CTkButton(sidebar, text=text, font=("Arial", 11), fg_color="#2d3748", hover_color="#4a5568",
                        text_color="white", corner_radius=0)
    btn.pack(fill="x", pady=3)

# ---------------- Main Content ----------------
main_content = ctk.CTkFrame(root, fg_color="#1a202c", width=600, height=500)
main_content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

# Header Section
header_frame = ctk.CTkFrame(main_content, fg_color="#1a202c")
header_frame.pack(fill="x", pady=5)

header_label = ctk.CTkLabel(header_frame, text="📊 Admin Dashboard", font=("Arial", 16, "bold"), text_color="white")
header_label.pack(side="left")

user_label = ctk.CTkLabel(header_frame, text="Hello, Admin!", font=("Arial", 11), text_color="gray")
user_label.pack(side="right")

# ---------------- Quick Overview ----------------
overview_section = ctk.CTkFrame(main_content, fg_color="#1a202c")
overview_section.pack(fill="x", pady=15)

overview_title = ctk.CTkLabel(overview_section, text="📌 Quick Overview", font=("Arial", 14, "bold"),
                              text_color="#9f7aea")
overview_title.pack(anchor="w", pady=5)

# Stats Grid
stats_frame = ctk.CTkFrame(overview_section, fg_color="#1a202c")
stats_frame.pack(fill="x")

stats = [
    ("👥 Total Users", "150", "#16a34a"),  # Green
    ("🎵 Total Songs", "320", "#2563eb"),  # Blue
    ("📁 Playlists Created", "45", "#facc15"),  # Yellow
    ("⬇️ Total Downloads", "780", "#dc2626")  # Red
]

for name, value, color in stats:
    stat_card = ctk.CTkFrame(stats_frame, fg_color="#2d3748", width=160, height=80, corner_radius=10)
    stat_card.pack(side="left", padx=10, pady=5, expand=True)

    stat_icon = ctk.CTkLabel(stat_card, text=name, font=("Arial", 10, "bold"), text_color="white")
    stat_icon.pack(pady=5)

    stat_value = ctk.CTkLabel(stat_card, text=value, font=("Arial", 14, "bold"), text_color=color)
    stat_value.pack()

# ---------------- Admin Actions ----------------
actions_section = ctk.CTkFrame(main_content, fg_color="#1a202c")
actions_section.pack(fill="x", pady=15)

actions_title = ctk.CTkLabel(actions_section, text="⚙️ Manage", font=("Arial", 14, "bold"),
                             text_color="#9f7aea")
actions_title.pack(anchor="w", pady=5)

actions_frame = ctk.CTkFrame(actions_section, fg_color="#1a202c")
actions_frame.pack(fill="x")

# Action Buttons
buttons = [
    ("👥 Manage Users", "#9f7aea"),
    ("🎵 Manage Songs", "#2563eb"),
    ("📁 Manage Playlists", "#facc15")
]

for text, color in buttons:
    action_btn = ctk.CTkButton(actions_frame, text=text, font=("Arial", 12, "bold"), fg_color=color,
                               hover_color="#6b46c1", text_color="white", height=40, corner_radius=10)
    action_btn.pack(side="left", padx=10, pady=5, expand=True)

# ---------------- Run Application ----------------
root.mainloop()
