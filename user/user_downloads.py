"""
Download and upload functionality for the Online Music System user interface.
"""

import os
import sys
import customtkinter as ctk
from tkinter import messagebox, filedialog, simpledialog
import traceback
import mutagen
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wave import WAVE

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import UI_THEME, UI_COLOR_THEME, COLORS, TEMP_DIR
from utils import get_current_user, connect_db, format_file_size

from user_nav import UserNavigation

class UserDownloadPage:
    def __init__(self, root):
        self.root = root
        self.user = get_current_user()
        
        if not self.user:
            # User is not logged in, redirect to login page
            self.root.destroy()
            return
        
        # Keep track of selected song
        self.selected_song = {
            "id": None,
            "title": None,
            "artist": None
        }
        
        # For storing song frames
        self.song_frames = []
        
        # Initialize UI
        self.initialize_ui()
        
        # Load song tabs
        self.display_favorite_songs_tab()
        self.display_popular_songs_tab()
    
    def initialize_ui(self):
        """Initialize the user interface"""
        self.root.title("Online Music System - Download Songs")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        
        # ---------------- Main Frame ----------------
        self.main_frame = ctk.CTkFrame(self.root, fg_color=COLORS["content_bg"], corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # ---------------- Navigation Sidebar ----------------
        self.nav = UserNavigation(self.main_frame, active_item="download")
        
        # ---------------- Main Content ----------------
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS["content_bg"], corner_radius=10)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Header with username
        self.header_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["content_bg"], height=40)
        self.header_frame.pack(fill="x", padx=20, pady=(20, 0))
        
        # Left side: Download Songs
        self.download_label = ctk.CTkLabel(self.header_frame, text="Download Songs", font=("Arial", 24, "bold"), text_color="white")
        self.download_label.pack(side="left")
        
        # Right side: Username
        self.user_label = ctk.CTkLabel(self.header_frame, 
                                    text=f"Hello, {self.user['first_name']} {self.user['last_name']}!", 
                                    font=("Arial", 14), text_color=COLORS["text_secondary"])
        self.user_label.pack(side="right")
        
        # ---------------- Download Your Favorite Songs ----------------
        self.favorite_songs_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["content_bg"])
        self.favorite_songs_frame.pack(fill="both", expand=True, padx=20, pady=(40, 0))
        
        # Section title - centered
        self.title_label = ctk.CTkLabel(self.favorite_songs_frame, text="Download Your Favorite Songs 🎵", 
                                      font=("Arial", 24, "bold"), text_color=COLORS["primary"])
        self.title_label.pack(pady=(0, 5))
        
        # Subtitle - centered
        self.subtitle_label = ctk.CTkLabel(self.favorite_songs_frame, text="Select a song to download or upload your own.", 
                                         font=("Arial", 14), text_color=COLORS["text_secondary"])
        self.subtitle_label.pack(pady=(0, 20))
        
        # Tabview for different song sections
        self.tabs = ctk.CTkTabview(self.favorite_songs_frame, fg_color=COLORS["content_bg"])
        self.tabs.pack(fill="both", expand=True)
        
        # Add tabs
        self.favorite_tab = self.tabs.add("Your Favorites")
        self.popular_tab = self.tabs.add("Popular Songs")
        
        # Button frame at the bottom
        self.button_frame = ctk.CTkFrame(self.favorite_songs_frame, fg_color=COLORS["content_bg"])
        self.button_frame.pack(pady=25)
        
        # Download button
        self.download_button = ctk.CTkButton(self.button_frame, text="⬇️ Download Selected", font=("Arial", 14, "bold"), 
                                           fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], 
                                           corner_radius=5, height=40, width=210, 
                                           command=self.download_selected_song)
        self.download_button.pack(side="left", padx=10)
        
        # Upload button
        self.upload_button = ctk.CTkButton(self.button_frame, text="⬆️ Upload New Song", font=("Arial", 14, "bold"), 
                                         fg_color=COLORS["secondary"], hover_color=COLORS["secondary_hover"], 
                                         corner_radius=5, height=40, width=210,
                                         command=self.handle_upload_song)
        self.upload_button.pack(side="left", padx=10)
    
    def display_favorite_songs_tab(self):
        """Display the user's favorite songs tab"""
        # Clear existing content
        for widget in self.favorite_tab.winfo_children():
            widget.destroy()
        
        # Get favorite songs
        favorite_songs = self.get_user_favorite_songs()
        
        if not favorite_songs:
            no_songs_label = ctk.CTkLabel(
                self.favorite_tab, 
                text="You haven't listened to any songs yet.", 
                font=("Arial", 14), 
                text_color=COLORS["text_secondary"]
            )
            no_songs_label.pack(pady=30)
            return
        
        # Create song frames for each song
        for song in favorite_songs:
            song_frame = ctk.CTkFrame(self.favorite_tab, fg_color=COLORS["card_bg"], corner_radius=10, height=50)
            song_frame.pack(fill="x", pady=5, ipady=5)
            
            # Prevent frame from resizing
            song_frame.pack_propagate(False)
            
            # Song icon and title - left side
            song_icon = "🎵"
            song_label = ctk.CTkLabel(
                song_frame, 
                text=f"{song_icon} {song['artist_name']} - {song['title']}", 
                font=("Arial", 14), 
                text_color="white",
                anchor="w"
            )
            song_label.pack(side="left", padx=20)
            
            # File size and type - right side
            file_info = ctk.CTkLabel(
                song_frame, 
                text=f"{song['file_size_formatted']} ({song['file_type']})", 
                font=("Arial", 12), 
                text_color=COLORS["text_secondary"]
            )
            file_info.pack(side="right", padx=(0, 20))
            
            # Play button - right side
            play_btn = ctk.CTkButton(
                song_frame, 
                text="▶️", 
                font=("Arial", 14), 
                fg_color="#1E293B",
                hover_color="#2A3749",
                width=30, height=30,
                command=lambda sid=song['song_id'], title=song['title'], artist=song['artist_name']: 
                self.play_song(sid, title, artist)
            )
            play_btn.pack(side="right", padx=5)
            
            # Make frame selectable
            song_frame.bind(
                "<Button-1>", 
                lambda e, sid=song['song_id'], title=song['title'], artist=song['artist_name'], frame=song_frame: 
                    self.select_song_for_download(sid, title, artist, frame)
            )
            song_label.bind(
                "<Button-1>", 
                lambda e, sid=song['song_id'], title=song['title'], artist=song['artist_name'], frame=song_frame: 
                    self.select_song_for_download(sid, title, artist, frame)
            )
            
            # Add to list of song frames
            self.song_frames.append(song_frame)
    
    def display_popular_songs_tab(self):
        """Display the popular songs tab"""
        # Clear existing content
        for widget in self.popular_tab.winfo_children():
            widget.destroy()
        
        # Get popular songs
        popular_songs = self.get_popular_songs()
        
        if not popular_songs:
            no_songs_label = ctk.CTkLabel(
                self.popular_tab, 
                text="No songs found in the database.", 
                font=("Arial", 14), 
                text_color=COLORS["text_secondary"]
            )
            no_songs_label.pack(pady=30)
            return
        
        # Create song frames for each song
        for song in popular_songs:
            song_frame = ctk.CTkFrame(self.popular_tab, fg_color=COLORS["card_bg"], corner_radius=10, height=50)
            song_frame.pack(fill="x", pady=5, ipady=5)
            
            # Prevent frame from resizing
            song_frame.pack_propagate(False)
            
            # Song icon and title - left side
            song_icon = "🎵"
            song_label = ctk.CTkLabel(
                song_frame, 
                text=f"{song_icon} {song['artist_name']} - {song['title']}", 
                font=("Arial", 14), 
                text_color="white",
                anchor="w"
            )
            song_label.pack(side="left", padx=20)
            
            file_info = ctk.CTkLabel(
                song_frame, 
                text=f"{song['file_size_formatted']} ({song['file_type']})", 
                font=("Arial", 12), 
                text_color=COLORS["text_secondary"]
            )
            file_info.pack(side="right", padx=(0, 20))
            
            # Play button - right side
            play_btn = ctk.CTkButton(
                song_frame, 
                text="▶️", 
                font=("Arial", 14), 
                fg_color="#1E293B",
                hover_color="#2A3749",
                width=30, height=30,
                command=lambda sid=song['song_id'], title=song['title'], artist=song['artist_name']: 
                self.play_song(sid, title, artist)
            )
            play_btn.pack(side="right", padx=5)
            
            # Make frame selectable
            song_frame.bind(
                "<Button-1>", 
                lambda e, sid=song['song_id'], title=song['title'], artist=song['artist_name'], frame=song_frame: 
                    self.select_song_for_download(sid, title, artist, frame)
            )
            song_label.bind(
                "<Button-1>", 
                lambda e, sid=song['song_id'], title=song['title'], artist=song['artist_name'], frame=song_frame: 
                    self.select_song_for_download(sid, title, artist, frame)
            )
            
            # Add to list of song frames
            self.song_frames.append(song_frame)
    
    def get_user_favorite_songs(self, limit=8):
        """Get the current user's favorite songs"""
        try:
            # Get current user ID
            user_id = self.user["user_id"]
                
            connection = connect_db()
            if not connection:
                return []
                
            cursor = connection.cursor(dictionary=True)
            
            # Get songs the user has listened to most
            query = """
            SELECT s.song_id, s.title, a.name as artist_name, COUNT(lh.history_id) as play_count,
                   g.name as genre_name, s.file_size, s.file_type
            FROM Listening_History lh
            JOIN Songs s ON lh.song_id = s.song_id
            JOIN Artists a ON s.artist_id = a.artist_id
            LEFT JOIN Genres g ON s.genre_id = g.genre_id
            WHERE lh.user_id = %s
            GROUP BY s.song_id
            ORDER BY play_count DESC
            LIMIT %s
            """
            
            cursor.execute(query, (user_id, limit))
            songs = cursor.fetchall()
            
            # Format file sizes to human-readable format
            for song in songs:
                song['file_size_formatted'] = format_file_size(song['file_size'])
                
            return songs
            
        except Exception as e:
            print(f"Error getting user favorite songs: {e}")
            return []
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def get_popular_songs(self, limit=8):
        """Get most popular songs from the database"""
        try:
            connection = connect_db()
            if not connection:
                return []
                
            cursor = connection.cursor(dictionary=True)
            
            # Get songs with most plays in listening history
            query = """
            SELECT s.song_id, s.title, a.name as artist_name, COUNT(lh.history_id) as play_count, 
                   g.name as genre_name, s.file_size, s.file_type
            FROM Songs s
            JOIN Artists a ON s.artist_id = a.artist_id
            LEFT JOIN Genres g ON s.genre_id = g.genre_id
            LEFT JOIN Listening_History lh ON s.song_id = lh.song_id
            GROUP BY s.song_id
            ORDER BY play_count DESC
            LIMIT %s
            """
            
            cursor.execute(query, (limit,))
            songs = cursor.fetchall()
            
            # If no songs with play history, get newest songs
            if not songs:
                query = """
                SELECT s.song_id, s.title, a.name as artist_name, s.file_size, s.file_type,
                       g.name as genre_name, 0 as play_count
                FROM Songs s
                JOIN Artists a ON s.artist_id = a.artist_id
                LEFT JOIN Genres g ON s.genre_id = g.genre_id
                ORDER BY s.upload_date DESC
                LIMIT %s
                """
                cursor.execute(query, (limit,))
                songs = cursor.fetchall()
                
            # Format file sizes to human-readable format
            for song in songs:
                song['file_size_formatted'] = format_file_size(song['file_size'])
                
            return songs
            
        except Exception as e:
            print(f"Error fetching popular songs: {e}")
            return []
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
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
            
            # Record in listening history
            self.record_listening_history(song_id)
            
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
    
    def record_listening_history(self, song_id):
        """Record that the current user listened to a song"""
        try:
            # Get current user ID
            user_id = self.user["user_id"]
                
            connection = connect_db()
            if not connection:
                return
                
            cursor = connection.cursor()
            
            query = "INSERT INTO Listening_History (user_id, song_id) VALUES (%s, %s)"
            cursor.execute(query, (user_id, song_id))
            connection.commit()
            
        except Exception as e:
            print(f"Error recording listening history: {e}")
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def select_song_for_download(self, song_id, title, artist, song_frame):
        """Select a song for download"""
        # Reset highlight on all frames
        for frame in self.song_frames:
            frame.configure(fg_color=COLORS["card_bg"])
        
        # Highlight selected frame
        song_frame.configure(fg_color="#2A2A4E")
        
        # Update selected song info
        self.selected_song["id"] = song_id
        self.selected_song["title"] = title
        self.selected_song["artist"] = artist
    
    def download_selected_song(self):
        """Download the selected song"""
        if not self.selected_song["id"]:
            messagebox.showwarning("Warning", "Please select a song to download")
            return
        
        # Download the song
        self.download_song(self.selected_song["id"])
    
    def download_song(self, song_id):
        """Download a song to local storage"""
        try:
            # Get song data
            connection = connect_db()
            if not connection:
                return False
                
            cursor = connection.cursor()
            
            # Get song data and info
            query = """
            SELECT s.file_data, s.file_type, s.title, a.name 
            FROM Songs s
            JOIN Artists a ON s.artist_id = a.artist_id
            WHERE s.song_id = %s
            """
            cursor.execute(query, (song_id,))
            
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Error", "Could not retrieve song data")
                return False
                
            file_data, file_type, title, artist = result
            
            # Format the filename
            filename = f"{artist} - {title}.{file_type}"
            # Replace invalid filename characters
            filename = filename.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
            
            # Ask user for download location
            downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
            save_path = filedialog.asksaveasfilename(
                initialdir=downloads_dir,
                initialfile=filename,
                defaultextension=f".{file_type}",
                filetypes=[(f"{file_type.upper()} files", f"*.{file_type}"), ("All files", "*.*")]
            )
            
            if not save_path:  # User cancelled
                return False
            
            # Write song data to file
            with open(save_path, 'wb') as f:
                f.write(file_data)
            
            messagebox.showinfo("Download Complete", f"Song has been downloaded to:\n{save_path}")
            return True
            
        except Exception as e:
            print(f"Error downloading song: {e}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Could not download song: {e}")
            return False
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def handle_upload_song(self):
        """Handle the upload song process"""
        # Ask user to select an audio file
        file_path = filedialog.askopenfilename(
            title="Select a song file",
            filetypes=[("Audio Files", "*.mp3 *.wav *.flac"), ("All files", "*.*")]
        )
        
        if not file_path:  # User cancelled
            return
        
        # Get song title from file name
        default_title = os.path.splitext(os.path.basename(file_path))[0]
        
        # Ask for song title
        title = simpledialog.askstring("Song Title", "Enter song title:", initialvalue=default_title)
        if not title:  # User cancelled
            return
        
        # Get artists from database
        artists = self.get_artists()
        if not artists:
            messagebox.showerror("Error", "No artists found in database")
            
            # Ask if user wants to add a new artist
            artist_name = simpledialog.askstring("New Artist", "Enter artist name:")
            if not artist_name:  # User cancelled
                return
                
            # Add new artist to database
            connection = connect_db()
            if not connection:
                return
                
            try:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO Artists (name) VALUES (%s)", (artist_name,))
                connection.commit()
                artist_id = cursor.lastrowid
                cursor.close()
                connection.close()
            except Exception as e:
                messagebox.showerror("Error", f"Could not add artist: {e}")
                return
        else:
            # Create a dialog to select artist
            artist_select = ctk.CTkToplevel(self.root)
            artist_select.title("Select Artist")
            artist_select.geometry("300x400")
            artist_select.transient(self.root)
            artist_select.grab_set()
            
            # Center the dialog
            artist_select.update_idletasks()
            width = artist_select.winfo_width()
            height = artist_select.winfo_height()
            x = (artist_select.winfo_screenwidth() // 2) - (width // 2)
            y = (artist_select.winfo_screenheight() // 2) - (height // 2)
            artist_select.geometry(f"{width}x{height}+{x}+{y}")
            
            # Label
            ctk.CTkLabel(artist_select, text="Select Artist", font=("Arial", 16, "bold")).pack(pady=10)
            
            # Create a scrollable frame for artists
            artists_frame = ctk.CTkScrollableFrame(artist_select, width=250, height=250)
            artists_frame.pack(pady=10, padx=10, fill="both", expand=True)
            
            # Artist variable
            artist_var = ctk.StringVar()
            
            # Add radio buttons for each artist
            for artist in artists:
                ctk.CTkRadioButton(artists_frame, text=artist["name"], variable=artist_var, value=str(artist["artist_id"])).pack(anchor="w", pady=5)
            
            # Select first artist by default
            if artists:
                artist_var.set(str(artists[0]["artist_id"]))
            
            # Button to add a new artist
            def add_new_artist():
                artist_name = simpledialog.askstring("New Artist", "Enter artist name:")
                if artist_name:
                    connection = connect_db()
                    if connection:
                        try:
                            cursor = connection.cursor()
                            cursor.execute("INSERT INTO Artists (name) VALUES (%s)", (artist_name,))
                            connection.commit()
                            new_id = cursor.lastrowid
                            cursor.close()
                            connection.close()
                            
                            # Add to list and select it
                            ctk.CTkRadioButton(artists_frame, text=artist_name, variable=artist_var, value=str(new_id)).pack(anchor="w", pady=5)
                            artist_var.set(str(new_id))
                        except Exception as e:
                            messagebox.showerror("Error", f"Could not add artist: {e}")
            
            ctk.CTkButton(artist_select, text="+ Add New Artist", command=add_new_artist).pack(pady=5)
            
            # Confirm button
            def confirm_artist():
                nonlocal artist_id
                if artist_var.get():
                    artist_id = int(artist_var.get())
                    artist_select.destroy()
                else:
                    messagebox.showwarning("Warning", "Please select an artist")
            
            # Variable to store selected artist ID
            artist_id = None
            
            ctk.CTkButton(artist_select, text="Confirm", command=confirm_artist).pack(pady=10)
            
            # Wait for dialog to close
            self.root.wait_window(artist_select)
            
            # If no artist selected, cancel upload
            if artist_id is None:
                return
        
        # Get genres from database
        genres = self.get_genres()
        
        # Create a dialog to select genre
        genre_select = ctk.CTkToplevel(self.root)
        genre_select.title("Select Genre")
        genre_select.geometry("300x400")
        genre_select.transient(self.root)
        genre_select.grab_set()
        
        # Center the dialog
        genre_select.update_idletasks()
        width = genre_select.winfo_width()
        height = genre_select.winfo_height()
        x = (genre_select.winfo_screenwidth() // 2) - (width // 2)
        y = (genre_select.winfo_screenheight() // 2) - (height // 2)
        genre_select.geometry(f"{width}x{height}+{x}+{y}")
        
        # Label
        ctk.CTkLabel(genre_select, text="Select Genre", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Create a scrollable frame for genres
        genres_frame = ctk.CTkScrollableFrame(genre_select, width=250, height=250)
        genres_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Genre variable
        genre_var = ctk.StringVar()
        
        # Add radio buttons for each genre
        for genre in genres:
            ctk.CTkRadioButton(genres_frame, text=genre["name"], variable=genre_var, value=str(genre["genre_id"])).pack(anchor="w", pady=5)
        
        # Option for no genre
        ctk.CTkRadioButton(genres_frame, text="No Genre", variable=genre_var, value="0").pack(anchor="w", pady=5)
        
        # Select first genre by default
        if genres:
            genre_var.set(str(genres[0]["genre_id"]))
        else:
            genre_var.set("0")  # No genre
        
        # Confirm button
        def confirm_genre():
            nonlocal genre_id
            genre_id = int(genre_var.get()) if genre_var.get() != "0" else None
            genre_select.destroy()
        
        # Variable to store selected genre ID
        genre_id = None
        
        ctk.CTkButton(genre_select, text="Confirm", command=confirm_genre).pack(pady=10)
        
        # Wait for dialog to close
        self.root.wait_window(genre_select)
        
        # Upload the song
        song_id = self.upload_song(file_path, title, artist_id, genre_id)
        
        if song_id:
            # Refresh the song list
            self.refresh_song_list()
    
    def get_artists(self):
        """Get list of artists from the database"""
        try:
            connection = connect_db()
            if not connection:
                return []
                
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT artist_id, name FROM Artists ORDER BY name"
            cursor.execute(query)
            
            return cursor.fetchall()
            
        except Exception as e:
            print(f"Error fetching artists: {e}")
            return []
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def get_genres(self):
        """Get list of genres from the database"""
        try:
            connection = connect_db()
            if not connection:
                return []
                
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT genre_id, name FROM Genres ORDER BY name"
            cursor.execute(query)
            
            return cursor.fetchall()
            
        except Exception as e:
            print(f"Error fetching genres: {e}")
            return []
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def upload_song(self, file_path, title, artist_id, genre_id=None):
        """Upload a song to the database"""
        try:
            if not os.path.exists(file_path):
                messagebox.showerror("Error", f"File not found: {file_path}")
                return None
            
            # Get file information
            file_size = os.path.getsize(file_path)
            file_type = os.path.splitext(file_path)[1][1:].lower()  # Get extension without dot
            
            # Get song duration using mutagen
            try:
                if file_type == 'mp3':
                    audio = MP3(file_path)
                elif file_type == 'flac':
                    audio = FLAC(file_path)
                elif file_type in ['wav', 'wave']:
                    audio = WAVE(file_path)
                else:
                    # Fallback for other formats
                    audio = mutagen.File(file_path)
                    
                duration = int(audio.info.length)
            except Exception as e:
                print(f"Error getting audio duration: {e}")
                duration = 0
            
            # Read file binary data
            with open(file_path, 'rb') as file:
                file_data = file.read()
            
            # Insert into database
            connection = connect_db()
            if not connection:
                return None
                
            cursor = connection.cursor()
            
            query = """
            INSERT INTO Songs (title, artist_id, genre_id, duration, file_data, file_type, file_size)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (title, artist_id, genre_id, duration, file_data, file_type, file_size)
            
            cursor.execute(query, values)
            connection.commit()
            
            # Return the new song ID
            new_song_id = cursor.lastrowid
            
            messagebox.showinfo("Success", f"Song '{title}' uploaded successfully!")
            return new_song_id
            
        except Exception as e:
            print(f"Error uploading song: {e}")
            traceback.print_exc()
            messagebox.showerror("Database Error", f"Failed to upload song: {e}")
            return None
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def refresh_song_list(self):
        """Refresh the song list"""
        # Clear current song frames list
        self.song_frames = []
        
        # Clear current songs
        for widget in self.favorite_songs_frame.winfo_children():
            if widget != self.title_label and widget != self.subtitle_label and widget != self.button_frame and widget != self.tabs:
                widget.destroy()
        
        # Display favorite songs tab
        self.display_favorite_songs_tab()
        
        # Display popular songs tab
        self.display_popular_songs_tab()

def main():
    try:
        # Set the appearance mode
        ctk.set_appearance_mode(UI_THEME)
        ctk.set_default_color_theme(UI_COLOR_THEME)
        
        # Create the main window
        root = ctk.CTk()
        app = UserDownloadPage(root)
        root.mainloop()
    except Exception as e:
        print(f"Error in user download page: {e}")
        traceback.print_exc()
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()