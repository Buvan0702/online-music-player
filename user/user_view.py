"""
Main home page for the user interface.
"""

import os
import sys
import customtkinter as ctk
from tkinter import messagebox
import traceback

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import UI_THEME, UI_COLOR_THEME, COLORS, TEMP_DIR
from utils import get_current_user, connect_db, record_listening_history

from user_nav import UserNavigation

class UserHomePage:
    def __init__(self, root):
        self.root = root
        self.user = get_current_user()
        
        if not self.user:
            # User is not logged in, redirect to login page
            self.root.destroy()
            return
        
        # Initialize UI
        self.initialize_ui()
        
        # Load featured songs
        self.load_featured_songs()
    
    def initialize_ui(self):
        """Initialize the user interface"""
        self.root.title("Online Music System - Home")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        
        # ---------------- Main Frame ----------------
        self.main_frame = ctk.CTkFrame(self.root, fg_color=COLORS["content_bg"], corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # ---------------- Navigation Sidebar ----------------
        self.nav = UserNavigation(self.main_frame, active_item="home")
        
        # ---------------- Main Content ----------------
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS["content_bg"], corner_radius=10)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Header with username
        self.header_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["content_bg"], height=40)
        self.header_frame.pack(fill="x", padx=20, pady=(20, 0))
        
        # Left side: Home
        self.home_label = ctk.CTkLabel(self.header_frame, text="Home", font=("Arial", 18, "bold"), text_color="white")
        self.home_label.pack(side="left")
        
        # Right side: Username - updated with actual user name
        self.user_label = ctk.CTkLabel(self.header_frame, 
                                text=f"Hello, {self.user['first_name']} {self.user['last_name']}!", 
                                font=("Arial", 14), text_color=COLORS["text_secondary"])
        self.user_label.pack(side="right")
        
        # ---------------- Hero Section ----------------
        self.hero_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["content_bg"])
        self.hero_frame.pack(fill="x", padx=20, pady=(40, 20))
        
        # Main title
        self.title_label = ctk.CTkLabel(self.hero_frame, text="Discover Music & Play Instantly", 
                                      font=("Arial", 28, "bold"), text_color=COLORS["primary"])
        self.title_label.pack(anchor="w")
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(self.hero_frame, 
                                         text="Explore top trending songs, curated playlists, and personalized recommendations.", 
                                         font=("Arial", 14), text_color=COLORS["text_secondary"])
        self.subtitle_label.pack(anchor="w", pady=(10, 20))
        
        # Action Buttons with navigation
        self.button_frame = ctk.CTkFrame(self.hero_frame, fg_color=COLORS["content_bg"])
        self.button_frame.pack(anchor="w")
        
        # Trending button
        self.trending_btn = ctk.CTkButton(self.button_frame, text="🔥 Trending", font=("Arial", 14, "bold"), 
                                        fg_color=COLORS["secondary"], hover_color=COLORS["secondary_hover"], 
                                        corner_radius=8, height=40, width=150)
        self.trending_btn.pack(side="left", padx=(0, 10))
        
        # Playlists button
        self.playlists_btn = ctk.CTkButton(self.button_frame, text="🎵 Playlists", font=("Arial", 14, "bold"), 
                                         fg_color=COLORS["success"], hover_color=COLORS["success_hover"], 
                                         corner_radius=8, height=40, width=150,
                                         command=self.nav.open_playlist_page)
        self.playlists_btn.pack(side="left", padx=10)
        
        # Download button
        self.download_btn = ctk.CTkButton(self.button_frame, text="⬇️ Download", font=("Arial", 14, "bold"), 
                                        fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], 
                                        corner_radius=8, height=40, width=150,
                                        command=self.nav.open_download_page)
        self.download_btn.pack(side="left", padx=10)
        
        # ---------------- Featured Songs Section ----------------
        self.featured_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["content_bg"])
        self.featured_frame.pack(fill="x", padx=20, pady=20)
        
        # Section title
        self.featured_title = ctk.CTkLabel(self.featured_frame, text="🔥 Featured Songs", 
                                         font=("Arial", 18, "bold"), text_color=COLORS["primary"])
        self.featured_title.pack(anchor="w", pady=(0, 20))
        
        # Song cards container
        self.songs_frame = ctk.CTkFrame(self.featured_frame, fg_color=COLORS["content_bg"])
        self.songs_frame.pack(fill="x")
    
    def load_featured_songs(self):
        """Load featured songs from the database"""
        try:
            connection = connect_db()
            if not connection:
                return
                
            cursor = connection.cursor(dictionary=True)
            
            # Get songs with most plays in listening history
            query = """
            SELECT s.song_id, s.title, a.name as artist_name, COUNT(lh.history_id) as play_count 
            FROM Songs s
            JOIN Artists a ON s.artist_id = a.artist_id
            LEFT JOIN Listening_History lh ON s.song_id = lh.song_id
            GROUP BY s.song_id
            ORDER BY play_count DESC
            LIMIT 3
            """
            
            cursor.execute(query)
            songs = cursor.fetchall()
            
            # If no songs with play history, get newest songs
            if not songs:
                query = """
                SELECT s.song_id, s.title, a.name as artist_name 
                FROM Songs s
                JOIN Artists a ON s.artist_id = a.artist_id
                ORDER BY s.upload_date DESC
                LIMIT 3
                """
                cursor.execute(query)
                songs = cursor.fetchall()
            
            # Display songs if available
            if songs:
                for song in songs:
                    song_card = self.create_song_card(
                        self.songs_frame, 
                        song["song_id"], 
                        song["title"], 
                        song["artist_name"]
                    )
                    song_card.pack(side="left", padx=10)
            else:
                # No songs in database
                no_songs_label = ctk.CTkLabel(
                    self.songs_frame, 
                    text="No songs available. Check back later!", 
                    font=("Arial", 14),
                    text_color=COLORS["text_secondary"]
                )
                no_songs_label.pack(pady=30)
                
        except Exception as e:
            print(f"Error loading featured songs: {e}")
            traceback.print_exc()
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def create_song_card(self, parent, song_id, title, artist):
        """Create a clickable song card"""
        # Create song card frame
        song_card = ctk.CTkFrame(parent, fg_color=COLORS["card_bg"], corner_radius=10, 
                               width=150, height=180)
        song_card.pack_propagate(False)
        
        # Center the text vertically by adding a spacer frame
        spacer = ctk.CTkFrame(song_card, fg_color=COLORS["card_bg"], height=30)
        spacer.pack(side="top")
        
        # Song title with larger font
        song_label = ctk.CTkLabel(song_card, text=title, 
                                 font=("Arial", 16, "bold"), text_color="white")
        song_label.pack(pady=(5, 0))
        
        # Artist name below with smaller font
        artist_label = ctk.CTkLabel(song_card, text=artist, 
                                   font=("Arial", 12), text_color=COLORS["text_secondary"])
        artist_label.pack(pady=(5, 0))
        
        # Play button
        play_song_btn = ctk.CTkButton(song_card, text="▶️ Play", 
                                    font=("Arial", 12, "bold"),
                                    fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
                                    command=lambda: self.play_song(song_id, title, artist))
        play_song_btn.pack(pady=(15, 0))
        
        return song_card
    
    def play_song(self, song_id, title=None, artist=None):
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
            
            # Get additional info if not provided
            if title is None or artist is None:
                info_query = """
                SELECT s.title, a.name as artist_name 
                FROM Songs s 
                JOIN Artists a ON s.artist_id = a.artist_id 
                WHERE s.song_id = %s
                """
                cursor.execute(info_query, (song_id,))
                info = cursor.fetchone()
                if info:
                    title = info[0]
                    artist = info[1]
            
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
            
            # Record in listening history
            record_listening_history(self.user["user_id"], song_id)
            
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
        app = UserHomePage(root)
        root.mainloop()
    except Exception as e:
        print(f"Error in user home page: {e}")
        traceback.print_exc()
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()