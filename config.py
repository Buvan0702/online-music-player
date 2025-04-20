"""
Configuration settings for the Online Music System application.
"""

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "new_password",
    "database": "online_music_system"
}

# File Paths
TEMP_DIR = "temp"
USER_SESSION_FILE = "current_user.txt"
ADMIN_SESSION_FILE = "current_admin.txt"

# UI Settings
UI_THEME = "dark"
UI_COLOR_THEME = "blue"
DEFAULT_WINDOW_SIZE = "1000x600"

# Colors
COLORS = {
    "primary": "#B146EC",      # Purple
    "primary_hover": "#9333EA", # Darker purple
    "secondary": "#2563EB",    # Blue
    "secondary_hover": "#1D4ED8", # Darker blue
    "success": "#16A34A",      # Green
    "success_hover": "#15803D", # Darker green
    "sidebar_bg": "#111827",   # Dark blue/black
    "sidebar_hover": "#1E293B", # Slightly lighter
    "content_bg": "#131B2E",   # Dark blue
    "card_bg": "#1A1A2E",      # Slightly lighter dark blue
    "text_primary": "white",
    "text_secondary": "#A0A0A0", # Gray
}

# Feature Flags
ENABLE_RECOMMENDATIONS = True
ENABLE_ANALYTICS = True