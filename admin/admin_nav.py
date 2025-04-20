"""
Navigation sidebar for admin interface.
"""

import os
import sys
import customtkinter as ctk
from tkinter import messagebox
import subprocess

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import COLORS, ADMIN_SESSION_FILE
from utils import get_admin_info

class AdminNavigation:
    """Admin navigation sidebar"""
    
    def __init__(self, master, active_item="dashboard"):
        """Initialize the navigation sidebar
        
        Args:
            master: Parent frame/window
            active_item: Current active page (dashboard, users, songs, playlists, reports)
        """
        self.master = master
        self.active_item = active_item
        
        # Check admin privileges
        self.admin = get_admin_info()
        if not self.admin:
            # Redirect to login if not admin
            messagebox.showerror("Access Denied", "You do not have admin privileges.")
            self.open_login_page()
            return
        
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
            ("dashboard", "📊 Dashboard", self.open_dashboard),
            ("users", "👥 Manage Users", self.open_manage_users),
            ("songs", "🎵 Manage Songs", self.open_manage_songs),
            ("playlists", "📁 Manage Playlists", self.open_manage_playlists),
            ("reports", "📈 Reports & Analytics", self.open_reports),
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
    
    # ------------------- Navigation Methods -------------------
    def open_dashboard(self):
        """Navigate to the dashboard page"""
        if self.active_item == "dashboard":
            return  # Already on dashboard
        try:
            subprocess.Popen(["python", "admin/admin_view.py"])
            self.master.winfo_toplevel().destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open dashboard: {e}")
    
    def open_manage_users(self):
        """Navigate to the users management page"""
        if self.active_item == "users":
            return  # Already on users page
        try:
            subprocess.Popen(["python", "admin/admin_users.py"])
            self.master.winfo_toplevel().destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open user management: {e}")
    
    def open_manage_songs(self):
        """Navigate to the songs management page"""
        if self.active_item == "songs":
            return  # Already on songs page
        try:
            subprocess.Popen(["python", "admin/admin_songs.py"])
            self.master.winfo_toplevel().destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open song management: {e}")
    
    def open_manage_playlists(self):
        """Navigate to the playlists management page"""
        if self.active_item == "playlists":
            return  # Already on playlists page
        try:
            subprocess.Popen(["python", "admin/admin_playlists.py"])
            self.master.winfo_toplevel().destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open playlist management: {e}")
    
    def open_reports(self):
        """Navigate to the reports and analytics page"""
        if self.active_item == "reports":
            return  # Already on reports page
        try:
            subprocess.Popen(["python", "admin/admin_reports.py"])
            self.master.winfo_toplevel().destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open reports: {e}")
    
    def open_login_page(self):
        """Redirect to the login page"""
        try:
            subprocess.Popen(["python", "login_signup.py"])
            self.master.winfo_toplevel().destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open login page: {e}")
    
    def logout(self):
        """Logout and open the login page"""
        try:
            # Remove admin session file
            if os.path.exists(ADMIN_SESSION_FILE):
                os.remove(ADMIN_SESSION_FILE)
                
            # Open login page
            subprocess.Popen(["python", "login_signup.py"])
            self.master.winfo_toplevel().destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to logout: {e}")

# Example of usage in an admin interface page
if __name__ == "__main__":
    # Test the navigation component
    root = ctk.CTk()
    root.title("Admin Navigation Test")
    root.geometry("400x500")
    
    # Create main frame
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True)
    
    # Add navigation
    nav = AdminNavigation(main_frame, active_item="dashboard")
    
    # Add some content
    content = ctk.CTkLabel(main_frame, text="Admin Navigation Test")
    content.pack(pady=50)
    
    root.mainloop()