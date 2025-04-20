"""
Playlist management functionality for the Online Music System user interface.
"""

import os
import sys
import customtkinter as ctk
from tkinter import messagebox, simpledialog
import traceback

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import UI_THEME, UI_COLOR_THEME, COLORS, TEMP_DIR
from utils import get_current_user, connect_db, format_duration

from user_nav import UserNavigation

class UserPlaylistPage:
    def __init__(self, root):
        self.root = root
        self.user = get_current_user()
        
        if not self.user:
            # User is not logged in, redirect to login page
            self.root.destroy()
            return
        
        # Initialize UI
        self.initialize_ui()
        
        # Display playlists
        self.display_playlists()
    
    def initialize_ui(self):
        """Initialize the user interface"""
        self.root.title("Online Music System - Playlists")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        
        # ---------------- Main Frame ----------------
        self.main_frame = ctk.CTkFrame(self.root, fg_color=COLORS["content_bg"], corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # ---------------- Navigation Sidebar ----------------
        self.nav = UserNavigation(self.main_frame, active_item="playlist")
        
        # ---------------- Main Content ----------------
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS["content_bg"], corner_radius=10)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
    def display_playlists(self):
        """Create the playlists content in the main frame"""
        # Clear content frame first
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Header with username
        header_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["content_bg"], height=40)
        header_frame.pack(fill="x", padx=20, pady=(20, 0))

        # Left side: Featured
        featured_label = ctk.CTkLabel(header_frame, text="Playlists", font=("Arial", 24, "bold"), text_color="white")
        featured_label.pack(side="left")

        # Right side: Username
        user_label = ctk.CTkLabel(header_frame, 
                                text=f"Hello, {self.user['first_name']} {self.user['last_name']}!", 
                                font=("Arial", 14), text_color=COLORS["text_secondary"])
        user_label.pack(side="right")

        # ---------------- System Playlists ----------------
        our_playlists_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["content_bg"])
        our_playlists_frame.pack(fill="x", padx=20, pady=(40, 20))

        # Section title
        our_playlists_title = ctk.CTkLabel(our_playlists_frame, text="Featured Playlists :", 
                                          font=("Arial", 20, "bold"), text_color=COLORS["primary"])
        our_playlists_title.pack(anchor="w", pady=(0, 20))

        # Playlist cards container
        our_playlists_cards = ctk.CTkFrame(our_playlists_frame, fg_color=COLORS["content_bg"])
        our_playlists_cards.pack(fill="x")

        # Get system playlists
        system_playlists = self.get_system_playlists()
        
        if not system_playlists:
            # No featured playlists
            ctk.CTkLabel(our_playlists_cards, text="No featured playlists available", 
                       font=("Arial", 14), text_color=COLORS["text_secondary"]).pack(pady=10)
        else:
            # Create cards for each featured playlist
            for playlist in system_playlists:
                # Create playlist card
                card = ctk.CTkFrame(our_playlists_cards, fg_color=COLORS["card_bg"], corner_radius=15, 
                                   width=150, height=100)
                card.pack(side="left", padx=10)
                card.pack_propagate(False)  # Prevent resizing
                
                # Main label
                label = ctk.CTkLabel(card, text=playlist["name"], 
                                   font=("Arial", 16, "bold"), text_color="white")
                label.place(relx=0.5, rely=0.4, anchor="center")
                
                # Song count
                count_label = ctk.CTkLabel(card, text=f"{playlist['song_count']} songs", 
                                         font=("Arial", 12), text_color=COLORS["text_secondary"])
                count_label.place(relx=0.5, rely=0.65, anchor="center")
                
                # Make card clickable
                card.bind("<Button-1>", lambda e, pid=playlist["playlist_id"], 
                         pname=playlist["name"]: self.open_playlist(pid, pname))
                label.bind("<Button-1>", lambda e, pid=playlist["playlist_id"], 
                          pname=playlist["name"]: self.open_playlist(pid, pname))
                count_label.bind("<Button-1>", lambda e, pid=playlist["playlist_id"], 
                               pname=playlist["name"]: self.open_playlist(pid, pname))

        # ---------------- Your Playlists ----------------
        your_playlists_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["content_bg"])
        your_playlists_frame.pack(fill="x", padx=20, pady=(30, 20))

        # Section title
        your_playlists_title = ctk.CTkLabel(your_playlists_frame, text="Your Playlists :", 
                                           font=("Arial", 20, "bold"), text_color=COLORS["primary"])
        your_playlists_title.pack(anchor="w", pady=(0, 20))

        # Playlist cards container
        your_playlists_cards = ctk.CTkFrame(your_playlists_frame, fg_color=COLORS["content_bg"])
        your_playlists_cards.pack(fill="x")

        # Add new playlist button
        add_playlist = ctk.CTkFrame(your_playlists_cards, fg_color="#2A2A3E", corner_radius=15, 
                                   width=150, height=100)
        add_playlist.pack(side="left", padx=10)
        add_playlist.pack_propagate(False)  # Prevent resizing

        # Add Plus sign
        plus_label = ctk.CTkLabel(add_playlist, text="+", font=("Arial", 30, "bold"), text_color=COLORS["text_secondary"])
        plus_label.place(relx=0.5, rely=0.4, anchor="center")
        
        # Add text
        new_playlist_label = ctk.CTkLabel(add_playlist, text="New Playlist", 
                                        font=("Arial", 12), text_color=COLORS["text_secondary"])
        new_playlist_label.place(relx=0.5, rely=0.65, anchor="center")
        
        # Make button clickable
        add_playlist.bind("<Button-1>", lambda e: self.show_create_playlist_dialog())
        plus_label.bind("<Button-1>", lambda e: self.show_create_playlist_dialog())
        new_playlist_label.bind("<Button-1>", lambda e: self.show_create_playlist_dialog())

        # Get user playlists
        user_playlists = self.get_user_playlists()
        
        if not user_playlists:
            # No user playlists yet
            no_playlists_label = ctk.CTkLabel(your_playlists_cards, text="You haven't created any playlists yet", 
                                            font=("Arial", 14), text_color=COLORS["text_secondary"])
            no_playlists_label.pack(side="left", padx=20, pady=10)
        else:
            # Create cards for each user playlist
            for playlist in user_playlists:
                # Create playlist card
                card = ctk.CTkFrame(your_playlists_cards, fg_color=COLORS["card_bg"], corner_radius=15, 
                                   width=150, height=100)
                card.pack(side="left", padx=10)
                card.pack_propagate(False)  # Prevent resizing
                
                # Main label
                label = ctk.CTkLabel(card, text=playlist["name"], 
                                   font=("Arial", 16, "bold"), text_color="white")
                label.place(relx=0.5, rely=0.4, anchor="center")
                
                # Song count
                count_label = ctk.CTkLabel(card, text=f"{playlist['song_count']} songs", 
                                         font=("Arial", 12), text_color=COLORS["text_secondary"])
                count_label.place(relx=0.5, rely=0.65, anchor="center")
                
                # Make card clickable
                card.bind("<Button-1>", lambda e, pid=playlist["playlist_id"], 
                         pname=playlist["name"]: self.open_playlist(pid, pname))
                label.bind("<Button-1>", lambda e, pid=playlist["playlist_id"], 
                          pname=playlist["name"]: self.open_playlist(pid, pname))
                count_label.bind("<Button-1>", lambda e, pid=playlist["playlist_id"], 
                               pname=playlist["name"]: self.open_playlist(pid, pname))
    
    def open_playlist(self, playlist_id, playlist_name):
        """Open a playlist to view its songs"""
        # Clear the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Header with playlist name
        header_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["content_bg"], height=40)
        header_frame.pack(fill="x", padx=20, pady=(20, 0))

        # Left side: Playlist name
        playlist_title_label = ctk.CTkLabel(header_frame, text=f"Playlist: {playlist_name}", 
                                          font=("Arial", 24, "bold"), text_color="white")
        playlist_title_label.pack(side="left")

        # Right side: Back button
        back_btn = ctk.CTkButton(header_frame, text="← Back to Playlists", 
                               font=("Arial", 14), fg_color=COLORS["primary"], 
                               hover_color=COLORS["primary_hover"], command=self.display_playlists)
        back_btn.pack(side="right")
        
        # Songs section
        songs_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["content_bg"])
        songs_frame.pack(fill="both", expand=True, padx=20, pady=(20, 10))
        
        # Get songs in this playlist
        songs = self.get_playlist_songs(playlist_id)
        
        if not songs:
            # No songs in this playlist
            empty_label = ctk.CTkLabel(songs_frame, text="This playlist is empty.", 
                                     font=("Arial", 16), text_color=COLORS["text_secondary"])
            empty_label.pack(pady=30)
            
            # Add song button
            add_song_btn = ctk.CTkButton(songs_frame, text="+ Add Songs", 
                                        font=("Arial", 14, "bold"), fg_color=COLORS["primary"], 
                                        hover_color=COLORS["primary_hover"], 
                                        command=lambda: self.nav.open_search_page())
            add_song_btn.pack(pady=10)
        else:
            # Song list header
            header = ctk.CTkFrame(songs_frame, fg_color=COLORS["content_bg"], height=30)
            header.pack(fill="x", pady=(0, 10))
            
            ctk.CTkLabel(header, text="#", font=("Arial", 12, "bold"), text_color=COLORS["text_secondary"],
                       width=50).pack(side="left", padx=(10, 0))
            ctk.CTkLabel(header, text="TITLE", font=("Arial", 12, "bold"), text_color=COLORS["text_secondary"],
                       width=250).pack(side="left", padx=(10, 0))
            ctk.CTkLabel(header, text="ARTIST", font=("Arial", 12, "bold"), text_color=COLORS["text_secondary"],
                       width=200).pack(side="left", padx=(10, 0))
            ctk.CTkLabel(header, text="DURATION", font=("Arial", 12, "bold"), text_color=COLORS["text_secondary"],
                       width=100).pack(side="left", padx=(10, 0))
            
            # Songs list
            songs_list_frame = ctk.CTkScrollableFrame(songs_frame, fg_color=COLORS["content_bg"], 
                                                    height=400, corner_radius=0)
            songs_list_frame.pack(fill="both", expand=True, pady=(0, 10))
            
            # Add songs to list
            for i, song in enumerate(songs, 1):
                song_row = ctk.CTkFrame(songs_list_frame, fg_color=COLORS["card_bg"], corner_radius=5, height=40)
                song_row.pack(fill="x", pady=2, padx=5)
                
                # Track number
                ctk.CTkLabel(song_row, text=str(i), font=("Arial", 12), text_color="white",
                           width=50).pack(side="left", padx=(10, 0))
                
                # Song title
                ctk.CTkLabel(song_row, text=song["title"], font=("Arial", 12), text_color="white",
                           width=250, anchor="w").pack(side="left", padx=(10, 0))
                
                # Artist name
                ctk.CTkLabel(song_row, text=song["artist_name"], font=("Arial", 12), text_color=COLORS["text_secondary"],
                           width=200, anchor="w").pack(side="left", padx=(10, 0))
                
                # Duration
                ctk.CTkLabel(song_row, text=song["duration_formatted"], font=("Arial", 12), text_color=COLORS["text_secondary"],
                           width=100, anchor="w").pack(side="left", padx=(10, 0))
                
                # Play button
                play_btn = ctk.CTkButton(song_row, text="▶️", font=("Arial", 14), fg_color=COLORS["card_bg"],
                                       hover_color="#232342", width=30, height=30, 
                                       command=lambda sid=song["song_id"], title=song["title"], artist=song["artist_name"]: 
                                       self.play_song(sid, title, artist))
                play_btn.pack(side="right", padx=10)
                
                # Make row clickable
                song_row.bind("<Button-1>", lambda e, sid=song["song_id"], title=song["title"], artist=song["artist_name"]: 
                              self.play_song(sid, title, artist))
    
    def get_system_playlists(self):
        """Get featured/system playlists from the database"""
        try:
            connection = connect_db()
            if not connection:
                return []
                
            cursor = connection.cursor(dictionary=True)
            
            # Get playlists with most songs for featured playlists
            query = """
            SELECT p.playlist_id, p.name, COUNT(ps.song_id) AS song_count
            FROM Playlists p
            LEFT JOIN Playlist_Songs ps ON p.playlist_id = ps.playlist_id
            WHERE p.user_id = 1
            GROUP BY p.playlist_id
            ORDER BY song_count DESC
            LIMIT 3
            """
            
            cursor.execute(query)
            playlists = cursor.fetchall()
            
            return playlists
            
        except Exception as e:
            print(f"Error fetching system playlists: {e}")
            return []
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def get_user_playlists(self):
        """Get the current user's playlists"""
        try:
            user_id = self.user["user_id"]
                
            connection = connect_db()
            if not connection:
                return []
                
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT p.playlist_id, p.name, COUNT(ps.song_id) AS song_count
            FROM Playlists p
            LEFT JOIN Playlist_Songs ps ON p.playlist_id = ps.playlist_id
            WHERE p.user_id = %s
            GROUP BY p.playlist_id
            ORDER BY p.created_at DESC
            """
            
            cursor.execute(query, (user_id,))
            playlists = cursor.fetchall()
            
            return playlists
            
        except Exception as e:
            print(f"Error fetching user playlists: {e}")
            return []
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def create_new_playlist(self, name, description=""):
        """Create a new playlist for the current user"""
        try:
            user_id = self.user["user_id"]
                
            connection = connect_db()
            if not connection:
                return None
                
            cursor = connection.cursor()
            
            query = "INSERT INTO Playlists (user_id, name, description) VALUES (%s, %s, %s)"
            cursor.execute(query, (user_id, name, description))
            
            connection.commit()
            
            # Return the new playlist ID
            new_playlist_id = cursor.lastrowid
            return new_playlist_id
            
        except Exception as e:
            print(f"Error creating playlist: {e}")
            return None
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def get_playlist_songs(self, playlist_id):
        """Get songs in a playlist"""
        try:
            connection = connect_db()
            if not connection:
                return []
                
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT s.song_id, s.title, a.name as artist_name, s.duration,
                   ps.position
            FROM Playlist_Songs ps
            JOIN Songs s ON ps.song_id = s.song_id
            JOIN Artists a ON s.artist_id = a.artist_id
            WHERE ps.playlist_id = %s
            ORDER BY ps.position
            """
            
            cursor.execute(query, (playlist_id,))
            songs = cursor.fetchall()
            
            # Format durations to MM:SS
            for song in songs:
                song['duration_formatted'] = format_duration(song['duration'])
            
            return songs
            
        except Exception as e:
            print(f"Error fetching playlist songs: {e}")
            return []
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def show_create_playlist_dialog(self):
        """Show dialog to create a new playlist"""
        playlist_name = simpledialog.askstring("New Playlist", "Enter playlist name:")
        
        if playlist_name:
            if len(playlist_name.strip()) == 0:
                messagebox.showwarning("Invalid Name", "Playlist name cannot be empty.")
                return
                
            # Create the playlist
            new_playlist_id = self.create_new_playlist(playlist_name)
            
            if new_playlist_id:
                messagebox.showinfo("Success", f"Playlist '{playlist_name}' created!")
                self.display_playlists()  # Refresh the playlists view
            else:
                messagebox.showerror("Error", "Failed to create playlist.")
    
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
        app = UserPlaylistPage(root)
        root.mainloop()
    except Exception as e:
        print(f"Error in user playlist page: {e}")
        traceback.print_exc()
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()