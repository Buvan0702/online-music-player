"""
Utility functions for the Online Music System.
"""

import os
import hashlib
import mysql.connector
import subprocess
from tkinter import messagebox
import customtkinter as ctk
from pygame import mixer
from config import DB_CONFIG, TEMP_DIR, USER_SESSION_FILE, ADMIN_SESSION_FILE

# ------------------- Database Functions -------------------
def connect_db():
    """Connect to the MySQL database"""
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Database Connection Error", 
                            f"Failed to connect to database: {err}")
        return None

def connect_db_server():
    """Connect to MySQL server without specifying a database"""
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        return None

# ------------------- User Session Functions -------------------
def get_current_user():
    """Get the current logged-in user information"""
    try:
        # Read user ID from file
        if not os.path.exists(USER_SESSION_FILE):
            messagebox.showerror("Error", "You are not logged in!")
            return None
            
        with open(USER_SESSION_FILE, "r") as f:
            user_id = f.read().strip()
            
        if not user_id:
            messagebox.showerror("Error", "User ID not found!")
            return None
            
        connection = connect_db()
        if not connection:
            return None
            
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT user_id, first_name, last_name, email, is_admin FROM Users WHERE user_id = %s",
            (user_id,)
        )
        
        user = cursor.fetchone()
        if not user:
            return None
            
        return user
        
    except Exception as e:
        print(f"Error getting current user: {e}")
        return None
    finally:
        if 'connection' in locals() and connection and connection.is_connected():
            cursor.close()
            connection.close()

def get_admin_info():
    """Get the current admin information"""
    try:
        # Read admin ID from file
        if not os.path.exists(ADMIN_SESSION_FILE):
            return None
            
        with open(ADMIN_SESSION_FILE, "r") as f:
            admin_id = f.read().strip()
            
        if not admin_id:
            return None
            
        connection = connect_db()
        if not connection:
            return None
            
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT user_id, first_name, last_name, email FROM Users WHERE user_id = %s AND is_admin = 1",
            (admin_id,)
        )
        
        admin = cursor.fetchone()
        return admin
        
    except Exception as e:
        print(f"Error getting admin info: {e}")
        return None
    finally:
        if 'connection' in locals() and connection and connection.is_connected():
            cursor.close()
            connection.close()

# ------------------- Security Functions -------------------
def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """Simple email validation"""
    import re
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Password validation - at least 8 characters"""
    return len(password) >= 8

# ------------------- File & Format Functions -------------------
def format_file_size(size_bytes):
    """Format file size from bytes to human-readable format"""
    if not size_bytes:
        return "0 B"
    
    # Define size units
    units = ['B', 'KB', 'MB', 'GB']
    size = float(size_bytes)
    unit_index = 0
    
    # Convert to appropriate unit
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    
    # Return formatted size
    return f"{size:.2f} {units[unit_index]}"

def format_duration(seconds):
    """Format duration in seconds to MM:SS format"""
    if seconds is None:
        return "0:00"
    
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}:{seconds:02d}"

def format_relative_time(time_diff):
    """Format time difference to relative time string"""
    if time_diff.days < 1:
        hours = time_diff.seconds // 3600
        minutes = (time_diff.seconds % 3600) // 60
        if hours > 0:
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        else:
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif time_diff.days == 1:
        return "Yesterday"
    else:
        return f"{time_diff.days} days ago"

# ------------------- Navigation Functions -------------------
def open_window(script_name, destroy_current=True, current_window=None):
    """Open a new window and optionally destroy the current one"""
    try:
        subprocess.Popen(["python", script_name])
        if destroy_current and current_window:
            current_window.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Unable to open {script_name}: {e}")

# ------------------- Music Player Functions -------------------
def init_player():
    """Initialize the music player"""
    try:
        mixer.init()
        return True
    except Exception as e:
        print(f"Error initializing music player: {e}")
        return False

def create_temp_directory():
    """Create a temp directory for storing temporary files"""
    try:
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)
        return True
    except Exception as e:
        print(f"Error creating temp directory: {e}")
        return False

def record_listening_history(user_id, song_id):
    """Record that a user listened to a song"""
    try:
        connection = connect_db()
        if not connection:
            return False
            
        cursor = connection.cursor()
        
        query = "INSERT INTO Listening_History (user_id, song_id) VALUES (%s, %s)"
        cursor.execute(query, (user_id, song_id))
        connection.commit()
        
        return True
        
    except Exception as e:
        print(f"Error recording listening history: {e}")
        return False
    finally:
        if 'connection' in locals() and connection and connection.is_connected():
            cursor.close()
            connection.close()

# ------------------- UI Helper Functions -------------------
def create_scrollable_frame(parent, **kwargs):
    """Create a standardized scrollable frame"""
    return ctk.CTkScrollableFrame(parent, **kwargs)

def create_centered_window(window, width, height):
    """Center a window on the screen"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
    return window