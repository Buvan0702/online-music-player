"""
Admin dashboard view for the Online Music System.
"""

import os
import sys
import datetime
import customtkinter as ctk
from tkinter import messagebox
import traceback

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import UI_THEME, UI_COLOR_THEME, COLORS
from utils import get_admin_info, connect_db, format_relative_time

from admin_nav import AdminNavigation

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.admin = get_admin_info()
        
        if not self.admin:
            # Admin is not authenticated, redirect to login page
            self.root.destroy()
            return
        
        # Initialize UI
        self.initialize_ui()
        
        # Load dashboard data
        self.load_dashboard_data()
    
    def initialize_ui(self):
        """Initialize the user interface"""
        self.root.title("Online Music System - Admin Dashboard")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        
        # ---------------- Main Frame ----------------
        self.main_frame = ctk.CTkFrame(self.root, fg_color=COLORS["content_bg"], corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # ---------------- Navigation Sidebar ----------------
        self.nav = AdminNavigation(self.main_frame, active_item="dashboard")
        
        # ---------------- Main Content ----------------
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS["content_bg"], corner_radius=10)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Header with admin name
        self.header_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["content_bg"], height=40)
        self.header_frame.pack(fill="x", padx=20, pady=(20, 0))
        
        # Left side: Admin Dashboard
        self.dashboard_label = ctk.CTkLabel(self.header_frame, text="Admin Dashboard", font=("Arial", 24, "bold"), text_color="white")
        self.dashboard_label.pack(side="left")
        
        # Right side: Admin Name
        self.admin_label = ctk.CTkLabel(self.header_frame, 
                                    text=f"Hello, {self.admin['first_name']} {self.admin['last_name']}!", 
                                    font=("Arial", 14), text_color=COLORS["text_secondary"])
        self.admin_label.pack(side="right")
        
        # Refresh button on header
        self.refresh_btn = ctk.CTkButton(self.header_frame, text="🔄 Refresh", font=("Arial", 12), 
                                      fg_color=COLORS["secondary"], hover_color=COLORS["secondary_hover"], 
                                      text_color="white", corner_radius=5, 
                                      width=100, height=30, command=self.refresh_dashboard)
        self.refresh_btn.pack(side="right", padx=15)
        
        # ---------------- Quick Overview Section ----------------
        self.overview_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["content_bg"])
        self.overview_frame.pack(fill="x", padx=20, pady=(40, 20))
        
        # Section title
        self.overview_title = ctk.CTkLabel(self.overview_frame, text="Quick Overview 📊", 
                                         font=("Arial", 20, "bold"), text_color=COLORS["primary"])
        self.overview_title.pack(anchor="w", pady=(0, 15))
        
        # Stats grid container
        self.stats_frame = ctk.CTkFrame(self.overview_frame, fg_color=COLORS["content_bg"])
        self.stats_frame.pack(fill="x")
        
        # Stats cards
        stat_configs = [
            ("👥 Total Users", COLORS["success"]),  # Green
            ("🎵 Total Songs", COLORS["secondary"]),  # Blue
            ("📁 Playlists Created", "#FACC15"),  # Yellow
            ("⬇️ Total Plays", "#DC2626")  # Red
        ]
        
        # Create stats cards (to be populated later)
        self.stat_labels = []
        for i, (name, color) in enumerate(stat_configs):
            stat_card = ctk.CTkFrame(self.stats_frame, fg_color=COLORS["card_bg"], corner_radius=10, width=160, height=90)
            stat_card.pack(side="left", padx=10, expand=True)
            stat_card.pack_propagate(False)  # Keep fixed size
            
            # Center the content vertically
            stat_icon = ctk.CTkLabel(stat_card, text=name, font=("Arial", 12, "bold"), text_color="white")
            stat_icon.pack(pady=(20, 5))
            
            # Create a value label for later update
            value_label = ctk.CTkLabel(stat_card, text="0", font=("Arial", 22, "bold"), text_color=color)
            value_label.pack()
            
            # Store the label for later updates
            self.stat_labels.append(value_label)
        
        # ---------------- Manage Actions Section ----------------
        self.actions_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["content_bg"])
        self.actions_frame.pack(fill="x", padx=20, pady=(20, 0))
        
        # Section title
        self.actions_title = ctk.CTkLabel(self.actions_frame, text="Manage System ⚙️", 
                                        font=("Arial", 20, "bold"), text_color=COLORS["primary"])
        self.actions_title.pack(anchor="w", pady=(0, 15))
        
        # Action buttons container
        self.buttons_frame = ctk.CTkFrame(self.actions_frame, fg_color=COLORS["content_bg"])
        self.buttons_frame.pack(fill="x")
        
        # Action buttons with commands
        self.manage_users_action = ctk.CTkButton(self.buttons_frame, text="👥 Manage Users", 
                                               font=("Arial", 14, "bold"), 
                                               fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], 
                                               text_color="white", height=50, corner_radius=8,
                                               command=self.nav.open_manage_users)
        self.manage_users_action.pack(side="left", padx=10, expand=True)
        
        self.manage_songs_action = ctk.CTkButton(self.buttons_frame, text="🎵 Manage Songs", 
                                               font=("Arial", 14, "bold"), 
                                               fg_color=COLORS["secondary"], hover_color=COLORS["secondary_hover"], 
                                               text_color="white", height=50, corner_radius=8,
                                               command=self.nav.open_manage_songs)
        self.manage_songs_action.pack(side="left", padx=10, expand=True)
        
        self.manage_playlists_action = ctk.CTkButton(self.buttons_frame, text="📁 Manage Playlists", 
                                                  font=("Arial", 14, "bold"), 
                                                  fg_color=COLORS["success"], hover_color=COLORS["success_hover"], 
                                                  text_color="white", height=50, corner_radius=8,
                                                  command=self.nav.open_manage_playlists)
        self.manage_playlists_action.pack(side="left", padx=10, expand=True)
        
        # ---------------- Recent Activity Section ----------------
        self.activity_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["content_bg"])
        self.activity_frame.pack(fill="both", expand=True, padx=20, pady=(20, 20))
        
        # Section title
        self.activity_title = ctk.CTkLabel(self.activity_frame, text="Recent Activity 📝", 
                                         font=("Arial", 20, "bold"), text_color=COLORS["primary"])
        self.activity_title.pack(anchor="w", pady=(0, 15))
        
        # Activity list container
        self.activity_list_frame = ctk.CTkFrame(self.activity_frame, fg_color=COLORS["card_bg"], corner_radius=10)
        self.activity_list_frame.pack(fill="both", expand=True)
    
    def load_dashboard_data(self):
        """Load dashboard data from the database"""
        # Update stats
        stats = self.get_system_stats()
        
        # Update stat values
        self.stat_labels[0].configure(text=str(stats["total_users"]))  # Users
        self.stat_labels[1].configure(text=str(stats["total_songs"]))  # Songs
        self.stat_labels[2].configure(text=str(stats["total_playlists"]))  # Playlists
        self.stat_labels[3].configure(text=str(stats["total_downloads"]))  # Plays/downloads
        
        # Update recent activities
        self.update_activity_list()
    
    def refresh_dashboard(self):
        """Refresh dashboard data"""
        # Update all statistics and activities
        self.load_dashboard_data()
        messagebox.showinfo("Dashboard Refreshed", "Dashboard data has been updated.")
    
    def get_system_stats(self):
        """Get system statistics for the dashboard"""
        try:
            connection = connect_db()
            if not connection:
                return {
                    "total_users": 0,
                    "total_songs": 0,
                    "total_playlists": 0,
                    "total_downloads": 0
                }
                
            cursor = connection.cursor()
            
            # Get user count
            cursor.execute("SELECT COUNT(*) FROM Users")
            total_users = cursor.fetchone()[0]
            
            # Get song count
            cursor.execute("SELECT COUNT(*) FROM Songs")
            total_songs = cursor.fetchone()[0]
            
            # Get playlist count
            cursor.execute("SELECT COUNT(*) FROM Playlists")
            total_playlists = cursor.fetchone()[0]
            
            # Approximate downloads (listening history entries)
            cursor.execute("SELECT COUNT(*) FROM Listening_History")
            total_downloads = cursor.fetchone()[0]
            
            return {
                "total_users": total_users,
                "total_songs": total_songs,
                "total_playlists": total_playlists,
                "total_downloads": total_downloads
            }
            
        except Exception as e:
            print(f"Error getting system stats: {e}")
            traceback.print_exc()
            return {
                "total_users": 0,
                "total_songs": 0,
                "total_playlists": 0,
                "total_downloads": 0
            }
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def get_recent_activities(self, limit=4):
        """Get recent system activities"""
        try:
            connection = connect_db()
            if not connection:
                return []
                
            cursor = connection.cursor(dictionary=True)
            
            # Get recent user registrations
            user_query = """
            SELECT 'user_registered' as activity_type, 
                   CONCAT(first_name, ' ', last_name) as item,
                   created_at as timestamp
            FROM Users
            ORDER BY created_at DESC
            LIMIT %s
            """
            
            # Get recent song uploads
            song_query = """
            SELECT 'song_uploaded' as activity_type,
                   CONCAT(s.title, ' - ', a.name) as item,
                   s.upload_date as timestamp
            FROM Songs s
            JOIN Artists a ON s.artist_id = a.artist_id
            ORDER BY s.upload_date DESC
            LIMIT %s
            """
            
            # Get recent playlist creations
            playlist_query = """
            SELECT 'playlist_created' as activity_type,
                   p.name as item,
                   p.created_at as timestamp
            FROM Playlists p
            ORDER BY p.created_at DESC
            LIMIT %s
            """
            
            # Get recent listening activity (downloads)
            download_query = """
            SELECT 'song_played' as activity_type,
                   CONCAT(s.title, ' - ', a.name) as item,
                   lh.played_at as timestamp
            FROM Listening_History lh
            JOIN Songs s ON lh.song_id = s.song_id
            JOIN Artists a ON s.artist_id = a.artist_id
            ORDER BY lh.played_at DESC
            LIMIT %s
            """
            
            # Execute all queries
            cursor.execute(user_query, (limit,))
            users = cursor.fetchall()
            
            cursor.execute(song_query, (limit,))
            songs = cursor.fetchall()
            
            cursor.execute(playlist_query, (limit,))
            playlists = cursor.fetchall()
            
            cursor.execute(download_query, (limit,))
            downloads = cursor.fetchall()
            
            # Combine all activities
            all_activities = users + songs + playlists + downloads
            
            # Sort by timestamp (most recent first)
            all_activities.sort(key=lambda x: x["timestamp"], reverse=True)
            
            # Limit to requested number
            all_activities = all_activities[:limit]
            
            # Format activities for display
            formatted_activities = []
            for activity in all_activities:
                activity_type = activity["activity_type"]
                item = activity["item"]
                timestamp = activity["timestamp"]
                
                # Calculate relative time
                time_diff = datetime.datetime.now() - timestamp
                time_str = format_relative_time(time_diff)
                
                # Format action based on activity type
                if activity_type == "user_registered":
                    action = "👤 New user registered"
                elif activity_type == "song_uploaded":
                    action = "🎵 New song uploaded"
                elif activity_type == "playlist_created":
                    action = "📁 Playlist created"
                elif activity_type == "song_played":
                    action = "⬇️ Song played"
                else:
                    action = "🔄 System activity"
                
                formatted_activities.append((action, item, time_str))
            
            return formatted_activities
            
        except Exception as e:
            print(f"Error getting recent activities: {e}")
            traceback.print_exc()
            return []
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def update_activity_list(self):
        """Update the recent activities list in UI"""
        # First, clear existing activities
        for widget in self.activity_list_frame.winfo_children():
            widget.destroy()
        
        # Get fresh activities
        activities = self.get_recent_activities()
        
        # Display activities
        if not activities:
            no_activity_label = ctk.CTkLabel(
                self.activity_list_frame, 
                text="No recent activities found", 
                font=("Arial", 12), 
                text_color=COLORS["text_secondary"]
            )
            no_activity_label.pack(pady=20)
        else:
            for action, item, time in activities:
                activity_item = ctk.CTkFrame(self.activity_list_frame, fg_color=COLORS["card_bg"], height=40)
                activity_item.pack(fill="x", padx=10, pady=5)
                
                action_label = ctk.CTkLabel(activity_item, text=action, font=("Arial", 12, "bold"), text_color="white")
                action_label.pack(side="left", padx=10)
                
                item_label = ctk.CTkLabel(activity_item, text=item, font=("Arial", 12), text_color=COLORS["text_secondary"])
                item_label.pack(side="left", padx=10)
                
                time_label = ctk.CTkLabel(activity_item, text=time, font=("Arial", 12), text_color=COLORS["primary"])
                time_label.pack(side="right", padx=10)

def main():
    try:
        # Set the appearance mode
        ctk.set_appearance_mode(UI_THEME)
        ctk.set_default_color_theme(UI_COLOR_THEME)
        
        # Create the main window
        root = ctk.CTk()
        app = AdminDashboard(root)
        root.mainloop()
    except Exception as e:
        print(f"Error in admin dashboard: {e}")
        traceback.print_exc()
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()