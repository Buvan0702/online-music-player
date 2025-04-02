import customtkinter as ctk

# ---------------- Initialize App ----------------
ctk.set_appearance_mode("dark")  # Dark mode
ctk.set_default_color_theme("blue")  # Default theme

root = ctk.CTk()
root.title("Online Music System - Admin Dashboard")
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

# Sidebar Menu Items - Admin specific options
menu_items = [
    ("📊 Dashboard", "#111827", "white"),  # Highlighted as active
    ("👥 Manage Users", "#111827", "#A0A0A0"),
    ("🎵 Manage Songs", "#111827", "#A0A0A0"),
    ("📁 Manage Playlists", "#111827", "#A0A0A0"),
    ("📈 Reports & Analytics", "#111827", "#A0A0A0"),
    ("🚪 Logout", "#111827", "#A0A0A0")
]

for text, bg_color, text_color in menu_items:
    btn = ctk.CTkButton(sidebar, text=text, font=("Arial", 14), 
                      fg_color=bg_color, hover_color="#1E293B", text_color=text_color,
                      anchor="w", corner_radius=0, height=40)
    btn.pack(fill="x", pady=5, padx=10)

# ---------------- Main Content ----------------
content_frame = ctk.CTkFrame(main_frame, fg_color="#131B2E", corner_radius=10)
content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Header with username
header_frame = ctk.CTkFrame(content_frame, fg_color="#131B2E", height=40)
header_frame.pack(fill="x", padx=20, pady=(20, 0))

# Left side: Admin Dashboard
dashboard_label = ctk.CTkLabel(header_frame, text="Admin Dashboard", font=("Arial", 24, "bold"), text_color="white")
dashboard_label.pack(side="left")

# Right side: Username
user_label = ctk.CTkLabel(header_frame, text="Hello, Admin!", font=("Arial", 14), text_color="#A0A0A0")
user_label.pack(side="right")

# ---------------- Quick Overview Section ----------------
overview_frame = ctk.CTkFrame(content_frame, fg_color="#131B2E")
overview_frame.pack(fill="x", padx=20, pady=(40, 20))

# Section title
overview_title = ctk.CTkLabel(overview_frame, text="Quick Overview 📊", 
                             font=("Arial", 20, "bold"), text_color="#B146EC")
overview_title.pack(anchor="w", pady=(0, 15))

# Stats grid container
stats_frame = ctk.CTkFrame(overview_frame, fg_color="#131B2E")
stats_frame.pack(fill="x")

# Stats cards
stats = [
    ("👥 Total Users", "150", "#16A34A"),  # Green
    ("🎵 Total Songs", "320", "#2563EB"),  # Blue
    ("📁 Playlists Created", "45", "#FACC15"),  # Yellow
    ("⬇️ Total Downloads", "780", "#DC2626")  # Red
]

for name, value, color in stats:
    stat_card = ctk.CTkFrame(stats_frame, fg_color="#1A1A2E", corner_radius=10, width=160, height=90)
    stat_card.pack(side="left", padx=10, expand=True)
    stat_card.pack_propagate(False)  # Keep fixed size
    
    # Center the content vertically
    stat_icon = ctk.CTkLabel(stat_card, text=name, font=("Arial", 12, "bold"), text_color="white")
    stat_icon.pack(pady=(20, 5))
    
    stat_value = ctk.CTkLabel(stat_card, text=value, font=("Arial", 22, "bold"), text_color=color)
    stat_value.pack()

# ---------------- Manage Actions Section ----------------
actions_frame = ctk.CTkFrame(content_frame, fg_color="#131B2E")
actions_frame.pack(fill="x", padx=20, pady=(20, 0))

# Section title
actions_title = ctk.CTkLabel(actions_frame, text="Manage System ⚙️", 
                            font=("Arial", 20, "bold"), text_color="#B146EC")
actions_title.pack(anchor="w", pady=(0, 15))

# Action buttons container
buttons_frame = ctk.CTkFrame(actions_frame, fg_color="#131B2E")
buttons_frame.pack(fill="x")

# Action buttons
buttons = [
    ("👥 Manage Users", "#B146EC"),
    ("🎵 Manage Songs", "#2563EB"),
    ("📁 Manage Playlists", "#16A34A")
]

for text, color in buttons:
    action_btn = ctk.CTkButton(buttons_frame, text=text, font=("Arial", 14, "bold"), 
                              fg_color=color, hover_color="#1E293B", 
                              text_color="white", height=50, corner_radius=8)
    action_btn.pack(side="left", padx=10, expand=True)

# ---------------- Recent Activity Section ----------------
activity_frame = ctk.CTkFrame(content_frame, fg_color="#131B2E")
activity_frame.pack(fill="both", expand=True, padx=20, pady=(20, 20))

# Section title
activity_title = ctk.CTkLabel(activity_frame, text="Recent Activity 📝", 
                             font=("Arial", 20, "bold"), text_color="#B146EC")
activity_title.pack(anchor="w", pady=(0, 15))

# Activity list container
activity_list_frame = ctk.CTkFrame(activity_frame, fg_color="#1A1A2E", corner_radius=10)
activity_list_frame.pack(fill="both", expand=True)

# Activity items
activities = [
    ("👤 New user registered", "User123", "5 minutes ago"),
    ("🎵 New song uploaded", "Blinding Lights.mp3", "2 hours ago"),
    ("📁 Playlist created", "Summer Hits", "Yesterday"),
    ("⬇️ Song downloaded", "Shape of You.mp3", "2 days ago")
]

for action, item, time in activities:
    activity_item = ctk.CTkFrame(activity_list_frame, fg_color="#1A1A2E", height=40)
    activity_item.pack(fill="x", padx=10, pady=5)
    
    action_label = ctk.CTkLabel(activity_item, text=action, font=("Arial", 12, "bold"), text_color="white")
    action_label.pack(side="left", padx=10)
    
    item_label = ctk.CTkLabel(activity_item, text=item, font=("Arial", 12), text_color="#A0A0A0")
    item_label.pack(side="left", padx=10)
    
    time_label = ctk.CTkLabel(activity_item, text=time, font=("Arial", 12), text_color="#B146EC")
    time_label.pack(side="right", padx=10)

# ---------------- Run Application ----------------
root.mainloop()