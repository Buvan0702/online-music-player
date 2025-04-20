"""
Search functionality for the Online Music System user interface.
"""

import os
import sys
import customtkinter as ctk
from tkinter import messagebox
import traceback

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import UI_THEME, UI_COLOR_THEME, COLORS, TEMP_DIR
from utils import get_current_user, connect_db, format_duration

from user_nav import UserNavigation

class UserSearchPage:
    def __init__(self, root):
        self.root = root
        self.user = get_current_user()
        
        if not self.user:
            # User is not logged in, redirect to login page
            self.root.destroy()
            return
        
        # Initialize UI
        self.initialize_ui()
        
        # Load recent songs as default content
        self.load_recent_songs()
    
    def initialize_ui(self):
        """Initialize the user interface"""
        self.root.title("Online Music System - Search Songs")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        
        # ---------------- Main Frame ----------------
        self.main_frame = ctk.CTkFrame(self.root, fg_color=COLORS["content_bg"], corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # ---------------- Navigation Sidebar ----------------
        self.nav = UserNavigation(self.main_frame, active_item="search")
        
        # ---------------- Main Content ----------------
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS["content_bg"], corner_radius=10)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Header with username
        self.header_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["content_bg"], height=40)
        self.header_frame.pack(fill="x", padx=20, pady=(20, 0))
        
        # Left side: Search Songs
        self.search_label = ctk.CTkLabel(self.header_frame, text="Search Songs", font=("Arial", 24, "bold"), text_color="white")
        self.search_label.pack(side="left")
        
        # Right side: Username
        self.user_label = ctk.CTkLabel(self.header_frame, 
                                text=f"Hello, {self.user['first_name']} {self.user['last_name']}!", 
                                font=("Arial", 14), text_color=COLORS["text_secondary"])
        self.user_label.pack(side="right")
        
        # ---------------- Search Bar ----------------
        self.search_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["content_bg"])
        self.search_frame.pack(fill="x", padx=20, pady=(30, 20))
        
        # Search type selection
        self.search_type_frame = ctk.CTkFrame(self.search_frame, fg_color=COLORS["content_bg"])
        self.search_type_frame.pack(fill="x", pady=(0, 10))
        
        self.search_type_var = ctk.StringVar(value="all")
        
        # Search type options
        self.search_all_radio = ctk.CTkRadioButton(
            self.search_type_frame, 
            text="All", 
            variable=self.search_type_var, 
            value="all",
            fg_color=COLORS["primary"],
            text_color=COLORS["text_secondary"]
        )
        self.search_all_radio.pack(side="left", padx=(0, 20))
        
        self.search_songs_radio = ctk.CTkRadioButton(
            self.search_type_frame, 
            text="Songs", 
            variable=self.search_type_var, 
            value="song",
            fg_color=COLORS["primary"],
            text_color=COLORS["text_secondary"]
        )
        self.search_songs_radio.pack(side="left", padx=(0, 20))
        
        self.search_artists_radio = ctk.CTkRadioButton(
            self.search_type_frame, 
            text="Artists", 
            variable=self.search_type_var, 
            value="artist",
            fg_color=COLORS["primary"],
            text_color=COLORS["text_secondary"]
        )
        self.search_artists_radio.pack(side="left", padx=(0, 20))
        
        self.search_albums_radio = ctk.CTkRadioButton(
            self.search_type_frame, 
            text="Albums", 
            variable=self.search_type_var, 
            value="album",
            fg_color=COLORS["primary"],
            text_color=COLORS["text_secondary"]
        )
        self.search_albums_radio.pack(side="left")
        
        # Search entry with rounded corners
        self.search_entry = ctk.CTkEntry(self.search_frame, 
                                  placeholder_text="Search for songs, artists, or albums...",
                                  font=("Arial", 14), text_color="#FFFFFF",
                                  fg_color=COLORS["card_bg"], border_color="#2A2A4E", 
                                  height=45, corner_radius=10)
        self.search_entry.pack(side="left", fill="x", expand=True)
        
        # Bind Enter key to search
        self.search_entry.bind("<Return>", self.perform_search)
        
        # Search button
        self.search_button = ctk.CTkButton(
            self.search_frame, 
            text="Search", 
            font=("Arial", 14, "bold"),
            fg_color=COLORS["primary"], 
            hover_color=COLORS["primary_hover"], 
            corner_radius=10,
            command=self.perform_search,
            height=45,
            width=100
        )
        self.search_button.pack(side="right", padx=(10, 0))
        
        # ---------------- Songs Section ----------------
        self.songs_section = ctk.CTkFrame(self.content_frame, fg_color=COLORS["content_bg"])
        self.songs_section.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Section title
        self.songs_title = ctk.CTkLabel(self.songs_section, text="Recent Songs 🎵", 
                                 font=("Arial", 20, "bold"), text_color=COLORS["primary"])
        self.songs_title.pack(anchor="w", pady=(0, 15))
    
    def load_recent_songs(self):
        """Load recent songs as default content"""
        try:
            connection = connect_db()
            if not connection:
                return
                
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT s.song_id, s.title, a.name as artist_name 
            FROM Songs s
            JOIN Artists a ON s.artist_id = a.artist_id
            ORDER BY s.upload_date DESC
            LIMIT 6
            """
            
            cursor.execute(query)
            songs = cursor.fetchall()
            
            # Display songs
            self.display_songs(songs, "Recent Songs")
            
        except Exception as e:
            print(f"Error loading recent songs: {e}")
            traceback.print_exc()
            
            # Show error message in UI
            error_label = ctk.CTkLabel(
                self.songs_section, 
                text="Error loading songs. Please try again later.", 
                font=("Arial", 14),
                text_color=COLORS["text_secondary"]
            )
            error_label.pack(pady=20)
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def perform_search(self, event=None):
        """Search for songs and update the search results"""
        # Clear previous search results
        for widget in self.songs_section.winfo_children():
            if widget != self.songs_title:  # Keep the section title
                widget.destroy()
        
        # Get search query
        query = self.search_entry.get()
        
        if not query:
            # If no query, just show recent songs
            self.load_recent_songs()
            return
        
        # Get search type
        search_type = self.search_type_var.get()
        
        try:
            connection = connect_db()
            if not connection:
                return
                
            cursor = connection.cursor(dictionary=True)
            
            search_param = f"%{query}%"
            
            # Different queries based on search type
            if search_type == "song":
                query_sql = """
                SELECT s.song_id, s.title, a.name as artist_name, al.title as album_name, 
                       g.name as genre, s.duration
                FROM Songs s
                JOIN Artists a ON s.artist_id = a.artist_id
                LEFT JOIN Albums al ON s.album_id = al.album_id
                LEFT JOIN Genres g ON s.genre_id = g.genre_id
                WHERE s.title LIKE %s
                ORDER BY s.title
                """
                cursor.execute(query_sql, (search_param,))
            
            elif search_type == "artist":
                query_sql = """
                SELECT s.song_id, s.title, a.name as artist_name, al.title as album_name, 
                       g.name as genre, s.duration
                FROM Songs s
                JOIN Artists a ON s.artist_id = a.artist_id
                LEFT JOIN Albums al ON s.album_id = al.album_id
                LEFT JOIN Genres g ON s.genre_id = g.genre_id
                WHERE a.name LIKE %s
                ORDER BY s.title
                """
                cursor.execute(query_sql, (search_param,))
                
            elif search_type == "album":
                query_sql = """
                SELECT s.song_id, s.title, a.name as artist_name, al.title as album_name, 
                       g.name as genre, s.duration
                FROM Songs s
                JOIN Artists a ON s.artist_id = a.artist_id
                LEFT JOIN Albums al ON s.album_id = al.album_id
                LEFT JOIN Genres g ON s.genre_id = g.genre_id
                WHERE al.title LIKE %s
                ORDER BY s.title
                """
                cursor.execute(query_sql, (search_param,))
                
            else:  # "all" - search everything
                query_sql = """
                SELECT s.song_id, s.title, a.name as artist_name, al.title as album_name, 
                       g.name as genre, s.duration
                FROM Songs s
                JOIN Artists a ON s.artist_id = a.artist_id
                LEFT JOIN Albums al ON s.album_id = al.album_id
                LEFT JOIN Genres g ON s.genre_id = g.genre_id
                WHERE s.title LIKE %s OR a.name LIKE %s OR al.title LIKE %s
                ORDER BY s.title
                """
                cursor.execute(query_sql, (search_param, search_param, search_param))
            
            songs = cursor.fetchall()
            
            # Format durations to MM:SS
            for song in songs:
                song['duration_formatted'] = format_duration(song['duration'])
            
            # Display results
            self.display_songs(songs, f"Search Results for '{query}'")
            
        except Exception as e:
            print(f"Error searching songs: {e}")
            traceback.print_exc()
            
            # Show error message in UI
            error_label = ctk.CTkLabel(
                self.songs_section, 
                text="Error performing search. Please try again.", 
                font=("Arial", 14),
                text_color=COLORS["text_secondary"]
            )
            error_label.pack(pady=20)
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def display_songs(self, songs, section_subtitle=None):
        """Display songs in the search results section"""
        # Update section subtitle if provided
        if section_subtitle:
            self.songs_title.configure(text=f"🔍 {section_subtitle}")
        
        if not songs:
            # No songs found
            no_songs_label = ctk.CTkLabel(
                self.songs_section, 
                text="No songs found", 
                font=("Arial", 14),
                text_color=COLORS["text_secondary"]
            )
            no_songs_label.pack(pady=20)
            return
        
        # Create song rows
        for song in songs:
            # Create a frame for each song row
            song_frame = ctk.CTkFrame(self.songs_section, fg_color=COLORS["card_bg"], corner_radius=10, height=50)
            song_frame.pack(fill="x", pady=5)
            
            # Format the song display text
            if "album_name" in song and song["album_name"]:
                display_text = f"🎵 {song['artist_name']} - {song['title']} ({song['album_name']})"
            else:
                display_text = f"🎵 {song['artist_name']} - {song['title']}"
            
            # Add duration if available
            if "duration_formatted" in song:
                display_text += f" ({song['duration_formatted']})"
            
            # Song name and info
            song_label = ctk.CTkLabel(
                song_frame, 
                text=display_text, 
                font=("Arial", 14), 
                text_color="white",
                anchor="w"
            )
            song_label.pack(side="left", padx=15, fill="y")
            
            # Play button
            play_icon = ctk.CTkLabel(
                song_frame, 
                text="▶️", 
                font=("Arial", 16), 
                text_color=COLORS["success"]
            )
            play_icon.pack(side="right", padx=15)
            
            # Add play song command
            song_id = song["song_id"]
            
            # Make the whole row clickable
            song_frame.bind("<Button-1>", lambda e, sid=song_id, title=song["title"], artist=song["artist_name"]: 
                           self.play_song(sid, title, artist))
            song_label.bind("<Button-1>", lambda e, sid=song_id, title=song["title"], artist=song["artist_name"]: 
                           self.play_song(sid, title, artist))
            play_icon.bind("<Button-1>", lambda e, sid=song_id, title=song["title"], artist=song["artist_name"]: 
                           self.play_song(sid, title, artist))
    
    def play_song(self, song_id, title, artist):
        """Play a song and update player state"""
        try:
            from pygame import mixer
            
            # Get song data from database
            connection = connect_db()
            if not connection:
                return False
                
            cursor = connection.cursor()
            
            # Get file data
            query = "SELECT file_data, file_type FROM Songs WHERE song_id = %s"
            cursor.execute(query, (song_id,))
            
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Error", "Could not find song data")
                return False
            
            file_data, file_type = result
            
            # Create temp directory if doesn't exist
            os.makedirs(TEMP_DIR, exist_ok=True)
            
            # Save file data to temporary file
            temp_file = os.path.join(TEMP_DIR, f"song_{song_id}.{file_type}")
            with open(temp_file, 'wb') as f:
                f.write(file_data)
            
            # Play the song
            mixer.music.load(temp_file)
            mixer.music.play()
            
            # Update player state
            self.nav.update_playback_state(
                song_id=song_id,
                title=title,
                artist=artist,
                playing=True,
                paused=False
            )
            
            return True
            
        except Exception as e:
            print(f"Error playing song: {e}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Could not play song: {e}")
            return False
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()

def main():
    try:
        # Set the appearance mode
        ctk.set_appearance_mode(UI_THEME)
        ctk.set_default_color_theme(UI_COLOR_THEME)
        
        # Create the main window
        root = ctk.CTk()
        app = UserSearchPage(root)
        root.mainloop()
    except Exception as e:
        print(f"Error in user search page: {e}")
        traceback.print_exc()
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()