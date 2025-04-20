"""
Navigation sidebar and player controls for user interface.
"""

import os
import customtkinter as ctk
from tkinter import messagebox
import subprocess
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pygame import mixer
from config import COLORS, USER_SESSION_FILE
from utils import get_current_user

class UserNavigation:
    """User navigation sidebar with music player controls"""
    
    def __init__(self, master, active_item="home"):
        """Initialize the navigation sidebar
        
        Args:
            master: Parent frame/window
            active_item: Current active page (home, search, playlist, download, recommend)
        """
        self.master = master
        self.active_item = active_item
        self.current_song = {
            "id": None,
            "title": "No song playing",
            "artist": "",
            "playing": False,
            "paused": False
        }
        
        # Initialize mixer if not already initialized
        if not mixer.get_init():
            mixer.init()
        
        # Create the sidebar
        self.create_sidebar()
    
    def create_sidebar(self):
        """Create the navigation sidebar"""
        # Main sidebar frame
        self.sidebar = ctk.CTkFrame(self.master, width=250, height=580, fg_color=COLORS["sidebar_bg"], corner_radius=10)
        self.sidebar.pack(side="left", fill="y", padx=(10, 0), pady=10)
        
        # Sidebar Title
        title_label = ctk.CTkLabel(self.sidebar, text="Online Music\nSystem", font=("Arial", 20, "bold"), text_color="white")
        title_label.pack(pady=(25, 30))
        
        # Menu items configuration
        menu_items = [
            ("home", "🏠 Home", self.open_home_page),
            ("search", "🔍 Search", self.open_search_page),
            ("playlist", "🎵 Playlist", self.open_playlist_page),
            ("download", "⬇️ Download", self.open_download_page),
            ("recommend", "🎧 Recommend Songs", self.open_recommend_page),
            (None, None, None),  # Spacer
            ("logout", "🚪 Logout", self.logout)
        ]
        
        # Create menu buttons
        for item_id, text, command in menu_items:
            if item_id is None:  # This is a spacer
                continue
                
            # Determine if this item is active
            is_active = (item_id == self.active_item)
            text_color = "white" if is_active else COLORS["text_secondary"]
            
            # Create button
            btn = ctk.CTkButton(
                self.sidebar, 
                text=text, 
                font=("Arial", 14), 
                fg_color=COLORS["sidebar_bg"], 
                hover_color=COLORS["sidebar_hover"], 
                text_color=text_color,
                anchor="w", 
                corner_radius=0, 
                height=40, 
                command=command
            )
            btn.pack(fill="x", pady=5, padx=10)
        
        # Now playing label
        self.now_playing_frame = ctk.CTkFrame(self.sidebar, fg_color=COLORS["sidebar_bg"], height=40)
        self.now_playing_frame.pack(side="bottom", fill="x", pady=(0, 10), padx=10)
        
        self.now_playing_label = ctk.CTkLabel(
            self.now_playing_frame, 
            text="Now Playing: No song playing", 
            font=("Arial", 12), 
            text_color=COLORS["text_secondary"],
            wraplength=220
        )
        self.now_playing_label.pack(pady=5)
        
        # Music player controls at bottom of sidebar
        self.player_frame = ctk.CTkFrame(self.sidebar, fg_color=COLORS["sidebar_bg"], height=50)
        self.player_frame.pack(side="bottom", fill="x", pady=10, padx=10)
        
        # Control buttons with functionality
        self.prev_btn = ctk.CTkButton(
            self.player_frame, 
            text="⏮️", 
            font=("Arial", 18), 
            fg_color=COLORS["sidebar_bg"], 
            hover_color=COLORS["sidebar_hover"], 
            width=40, height=40, 
            command=self.play_previous_song
        )
        self.prev_btn.pack(side="left", padx=10)
        
        self.play_btn = ctk.CTkButton(
            self.player_frame, 
            text="▶️", 
            font=("Arial", 18), 
            fg_color=COLORS["sidebar_bg"], 
            hover_color=COLORS["sidebar_hover"], 
            width=40, height=40, 
            command=self.toggle_play_pause
        )
        self.play_btn.pack(side="left", padx=10)
        
        self.next_btn = ctk.CTkButton(
            self.player_frame, 
            text="⏭️", 
            font=("Arial", 18), 
            fg_color=COLORS["sidebar_bg"], 
            hover_color=COLORS["sidebar_hover"], 
            width=40, height=40, 
            command=self.play_next_song
        )
        self.next_btn.pack(side="left", padx=10)
    
    def update_playback_state(self, song_id=None, title=None, artist=None, playing=False, paused=False):
        """Update the current playback state and UI controls"""
        # Update current song info if provided
        if song_id is not None:
            self.current_song["id"] = song_id
        if title is not None:
            self.current_song["title"] = title
        if artist is not None:
            self.current_song["artist"] = artist
        
        # Update playback state
        self.current_song["playing"] = playing
        self.current_song["paused"] = paused
        
        # Update UI elements
        if playing:
            self.play_btn.configure(text="⏸️")
        else:
            self.play_btn.configure(text="▶️")
        
        # Update now playing label
        self.now_playing_label.configure(
            text=f"Now Playing: {self.current_song['title']} - {self.current_song['artist']}" 
            if (self.current_song["playing"] or self.current_song["paused"]) else "No song playing"
        )
    
    def toggle_play_pause(self):
        """Toggle between play and pause states"""
        if self.current_song["id"] is None:
            # No song loaded - do nothing
            return
        elif self.current_song["paused"]:
            # Resume paused song
            mixer.music.unpause()
            self.update_playback_state(playing=True, paused=False)
        elif self.current_song["playing"]:
            # Pause playing song
            mixer.music.pause()
            self.update_playback_state(playing=False, paused=True)
    
    def play_previous_song(self):
        """Placeholder for playing previous song"""
        messagebox.showinfo("Info", "Previous song feature will be implemented with playlists")
    
    def play_next_song(self):
        """Placeholder for playing next song"""
        messagebox.showinfo("Info", "Next song feature will be implemented with playlists")
    
    # ------------------- Navigation Methods -------------------
    def open_home_page(self):
        """Navigate to the home page"""
        if self.active_item == "home":
            return  # Already on home page
        try:
            subprocess.Popen(["python", "user/user_view.py"])
            self.master.winfo_toplevel().destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open home page: {e}")
    
    def open_search_page(self):
        """Navigate to the search page"""
        if self.active_item == "search":
            return  # Already on search page
        try:
            subprocess.Popen(["python", "user/user_search.py"])
            self.master.winfo_toplevel().destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open search page: {e}")
    
    def open_playlist_page(self):
        """Navigate to the playlist page"""
        if self.active_item == "playlist":
            return  # Already on playlist page
        try:
            subprocess.Popen(["python", "user/user_playlist.py"])
            self.master.winfo_toplevel().destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open playlist page: {e}")
    
    def open_download_page(self):
        """Navigate to the download page"""
        if self.active_item == "download":
            return  # Already on download page
        try:
            subprocess.Popen(["python", "user/user_downloads.py"])
            self.master.winfo_toplevel().destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open download page: {e}")
    
    def open_recommend_page(self):
        """Navigate to the recommendations page"""
        if self.active_item == "recommend":
            return  # Already on recommend page
        try:
            subprocess.Popen(["python", "user/user_recommend.py"])
            self.master.winfo_toplevel().destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open recommendations page: {e}")
    
    def logout(self):
        """Logout and open the login page"""
        try:
            # Stop any playing music
            if mixer.music.get_busy():
                mixer.music.stop()
                
            # Remove current user file
            if os.path.exists(USER_SESSION_FILE):
                os.remove(USER_SESSION_FILE)
                
            # Open login page
            subprocess.Popen(["python", "login_signup.py"])
            self.master.winfo_toplevel().destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to logout: {e}")

# Example of usage in a user interface page
if __name__ == "__main__":
    # Test the navigation component
    root = ctk.CTk()
    root.title("Navigation Test")
    root.geometry("400x500")
    
    # Create main frame
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True)
    
    # Add navigation
    nav = UserNavigation(main_frame, active_item="home")
    
    # Add some content
    content = ctk.CTkLabel(main_frame, text="Navigation Test")
    content.pack(pady=50)
    
    root.mainloop()