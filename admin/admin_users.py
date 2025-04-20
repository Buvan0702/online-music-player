"""
User management interface for admin.
"""

import os
import sys
import customtkinter as ctk
from tkinter import messagebox, simpledialog
import traceback

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import UI_THEME, UI_COLOR_THEME, COLORS
from utils import get_admin_info, connect_db, hash_password, validate_email

from admin_nav import AdminNavigation

class AdminUserManagement:
    def __init__(self, root):
        self.root = root
        self.admin = get_admin_info()
        
        if not self.admin:
            # Admin is not authenticated, redirect to login page
            self.root.destroy()
            return
        
        # Initialize UI
        self.initialize_ui()
        
        # Load users
        self.load_users()
    
    def initialize_ui(self):
        """Initialize the user interface"""
        self.root.title("Online Music System - Manage Users")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        
        # ---------------- Main Frame ----------------
        self.main_frame = ctk.CTkFrame(self.root, fg_color=COLORS["content_bg"], corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # ---------------- Navigation Sidebar ----------------
        self.nav = AdminNavigation(self.main_frame, active_item="users")
        
        # ---------------- Main Content ----------------
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS["content_bg"], corner_radius=10)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Header
        self.header_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["content_bg"], height=40)
        self.header_frame.pack(fill="x", padx=20, pady=(20, 0))
        
        # Left side: Manage Users title
        self.title_label = ctk.CTkLabel(self.header_frame, text="Manage Users", font=("Arial", 24, "bold"), text_color="white")
        self.title_label.pack(side="left")
        
        # Right side: Admin Name
        self.admin_label = ctk.CTkLabel(self.header_frame, 
                                     text=f"Hello, {self.admin['first_name']} {self.admin['last_name']}!", 
                                     font=("Arial", 14), text_color=COLORS["text_secondary"])
        self.admin_label.pack(side="right")
        
        # Search and add user section
        self.search_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["content_bg"], height=60)
        self.search_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Search entry
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search for users...", width=300)
        self.search_entry.pack(side="left")
        
        # Search button
        self.search_button = ctk.CTkButton(self.search_frame, text="Search", 
                                        fg_color=COLORS["secondary"], hover_color=COLORS["secondary_hover"],
                                        command=self.search_users)
        self.search_button.pack(side="left", padx=10)
        
        # Add user button
        self.add_button = ctk.CTkButton(self.search_frame, text="+ Add User", 
                                     fg_color=COLORS["success"], hover_color=COLORS["success_hover"],
                                     command=self.show_add_user_dialog)
        self.add_button.pack(side="right")
        
        # Refresh button
        self.refresh_button = ctk.CTkButton(self.search_frame, text="Refresh", 
                                         fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
                                         command=self.load_users)
        self.refresh_button.pack(side="right", padx=10)
        
        # Users list section
        self.users_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["content_bg"])
        self.users_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Column headers
        self.headers_frame = ctk.CTkFrame(self.users_frame, fg_color=COLORS["content_bg"], height=30)
        self.headers_frame.pack(fill="x", pady=(0, 5))
        
        ctk.CTkLabel(self.headers_frame, text="ID", width=50, font=("Arial", 12, "bold"), text_color=COLORS["text_secondary"]).pack(side="left")
        ctk.CTkLabel(self.headers_frame, text="Name", width=200, font=("Arial", 12, "bold"), text_color=COLORS["text_secondary"]).pack(side="left")
        ctk.CTkLabel(self.headers_frame, text="Email", width=250, font=("Arial", 12, "bold"), text_color=COLORS["text_secondary"]).pack(side="left")
        ctk.CTkLabel(self.headers_frame, text="Type", width=100, font=("Arial", 12, "bold"), text_color=COLORS["text_secondary"]).pack(side="left")
        ctk.CTkLabel(self.headers_frame, text="Actions", width=150, font=("Arial", 12, "bold"), text_color=COLORS["text_secondary"]).pack(side="left")
        
        # Scrollable frame for users
        self.users_list_frame = ctk.CTkScrollableFrame(self.users_frame, fg_color=COLORS["content_bg"])
        self.users_list_frame.pack(fill="both", expand=True)
    
    def load_users(self):
        """Load users from the database"""
        # Clear existing users
        for widget in self.users_list_frame.winfo_children():
            widget.destroy()
        
        try:
            connection = connect_db()
            if not connection:
                return
            
            cursor = connection.cursor(dictionary=True)
            
            # Get all users
            query = "SELECT user_id, first_name, last_name, email, is_admin FROM Users ORDER BY user_id"
            cursor.execute(query)
            
            users = cursor.fetchall()
            
            if not users:
                # No users found
                no_users_label = ctk.CTkLabel(
                    self.users_list_frame, 
                    text="No users found", 
                    font=("Arial", 14), 
                    text_color=COLORS["text_secondary"]
                )
                no_users_label.pack(pady=20)
                return
            
            # Display users
            for user in users:
                user_row = ctk.CTkFrame(self.users_list_frame, fg_color=COLORS["card_bg"], height=40, corner_radius=5)
                user_row.pack(fill="x", pady=2)
                user_row.pack_propagate(False)  # Prevent frame from resizing
                
                # User ID
                ctk.CTkLabel(user_row, text=str(user["user_id"]), width=50, text_color="white").pack(side="left")
                
                # User Name
                name = f"{user['first_name']} {user['last_name']}"
                ctk.CTkLabel(user_row, text=name, width=200, text_color="white").pack(side="left")
                
                # User Email
                ctk.CTkLabel(user_row, text=user["email"], width=250, text_color="white").pack(side="left")
                
                # User Type
                user_type = "Admin" if user["is_admin"] else "User"
                type_color = "#FFD700" if user["is_admin"] else "white"  # Gold for admin, white for user
                ctk.CTkLabel(user_row, text=user_type, width=100, text_color=type_color).pack(side="left")
                
                # Actions
                actions_frame = ctk.CTkFrame(user_row, fg_color=COLORS["card_bg"], width=150)
                actions_frame.pack(side="left")
                
                # Edit button
                edit_btn = ctk.CTkButton(
                    actions_frame, 
                    text="Edit", 
                    fg_color=COLORS["secondary"], 
                    hover_color=COLORS["secondary_hover"],
                    width=60, height=25,
                    command=lambda uid=user["user_id"]: self.show_edit_user_dialog(uid)
                )
                edit_btn.pack(side="left", padx=(0, 5))
                
                # Delete button (disabled for self and for admin if current user is not admin)
                delete_btn = ctk.CTkButton(
                    actions_frame, 
                    text="Delete", 
                    fg_color="#DC2626", 
                    hover_color="#B91C1C",
                    width=60, height=25,
                    command=lambda uid=user["user_id"]: self.confirm_delete_user(uid)
                )
                
                # Disable delete button for the current admin user
                if user["user_id"] == self.admin["user_id"]:
                    delete_btn.configure(state="disabled", fg_color="#555555", hover_color="#555555")
                
                delete_btn.pack(side="left", padx=5)
        
        except Exception as e:
            print(f"Error loading users: {e}")
            traceback.print_exc()
            
            # Show error message
            messagebox.showerror("Error", f"Failed to load users: {e}")
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def search_users(self):
        """Search for users based on search term"""
        search_term = self.search_entry.get()
        
        if not search_term:
            # If search term is empty, load all users
            self.load_users()
            return
        
        # Clear existing users
        for widget in self.users_list_frame.winfo_children():
            widget.destroy()
        
        try:
            connection = connect_db()
            if not connection:
                return
            
            cursor = connection.cursor(dictionary=True)
            
            # Search users by name or email
            query = """
            SELECT user_id, first_name, last_name, email, is_admin 
            FROM Users 
            WHERE first_name LIKE %s OR last_name LIKE %s OR email LIKE %s
            ORDER BY user_id
            """
            
            search_param = f"%{search_term}%"
            cursor.execute(query, (search_param, search_param, search_param))
            
            users = cursor.fetchall()
            
            if not users:
                # No users found
                no_users_label = ctk.CTkLabel(
                    self.users_list_frame, 
                    text=f"No users found matching '{search_term}'", 
                    font=("Arial", 14), 
                    text_color=COLORS["text_secondary"]
                )
                no_users_label.pack(pady=20)
                return
            
            # Display users (same as in load_users)
            for user in users:
                user_row = ctk.CTkFrame(self.users_list_frame, fg_color=COLORS["card_bg"], height=40, corner_radius=5)
                user_row.pack(fill="x", pady=2)
                user_row.pack_propagate(False)  # Prevent frame from resizing
                
                # User ID
                ctk.CTkLabel(user_row, text=str(user["user_id"]), width=50, text_color="white").pack(side="left")
                
                # User Name
                name = f"{user['first_name']} {user['last_name']}"
                ctk.CTkLabel(user_row, text=name, width=200, text_color="white").pack(side="left")
                
                # User Email
                ctk.CTkLabel(user_row, text=user["email"], width=250, text_color="white").pack(side="left")
                
                # User Type
                user_type = "Admin" if user["is_admin"] else "User"
                type_color = "#FFD700" if user["is_admin"] else "white"  # Gold for admin, white for user
                ctk.CTkLabel(user_row, text=user_type, width=100, text_color=type_color).pack(side="left")
                
                # Actions
                actions_frame = ctk.CTkFrame(user_row, fg_color=COLORS["card_bg"], width=150)
                actions_frame.pack(side="left")
                
                # Edit button
                edit_btn = ctk.CTkButton(
                    actions_frame, 
                    text="Edit", 
                    fg_color=COLORS["secondary"], 
                    hover_color=COLORS["secondary_hover"],
                    width=60, height=25,
                    command=lambda uid=user["user_id"]: self.show_edit_user_dialog(uid)
                )
                edit_btn.pack(side="left", padx=(0, 5))
                
                # Delete button (disabled for self)
                delete_btn = ctk.CTkButton(
                    actions_frame, 
                    text="Delete", 
                    fg_color="#DC2626", 
                    hover_color="#B91C1C",
                    width=60, height=25,
                    command=lambda uid=user["user_id"]: self.confirm_delete_user(uid)
                )
                
                # Disable delete button for the current admin user
                if user["user_id"] == self.admin["user_id"]:
                    delete_btn.configure(state="disabled", fg_color="#555555", hover_color="#555555")
                
                delete_btn.pack(side="left", padx=5)
        
        except Exception as e:
            print(f"Error searching users: {e}")
            traceback.print_exc()
            
            # Show error message
            messagebox.showerror("Error", f"Failed to search users: {e}")
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def show_add_user_dialog(self):
        """Show dialog to add a new user"""
        # Create a dialog window
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Add New User")
        dialog.geometry("400x450")
        dialog.resizable(False, False)
        dialog.transient(self.root)  # Make dialog modal
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Dialog content
        content_frame = ctk.CTkFrame(dialog, fg_color=COLORS["content_bg"])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        ctk.CTkLabel(content_frame, text="Add New User", font=("Arial", 18, "bold"), text_color="white").pack(pady=(0, 20))
        
        # First Name
        ctk.CTkLabel(content_frame, text="First Name", anchor="w", text_color="white").pack(fill="x", pady=(10, 0))
        first_name_entry = ctk.CTkEntry(content_frame)
        first_name_entry.pack(fill="x", pady=(0, 10))
        
        # Last Name
        ctk.CTkLabel(content_frame, text="Last Name", anchor="w", text_color="white").pack(fill="x", pady=(10, 0))
        last_name_entry = ctk.CTkEntry(content_frame)
        last_name_entry.pack(fill="x", pady=(0, 10))
        
        # Email
        ctk.CTkLabel(content_frame, text="Email", anchor="w", text_color="white").pack(fill="x", pady=(10, 0))
        email_entry = ctk.CTkEntry(content_frame)
        email_entry.pack(fill="x", pady=(0, 10))
        
        # Password
        ctk.CTkLabel(content_frame, text="Password", anchor="w", text_color="white").pack(fill="x", pady=(10, 0))
        password_entry = ctk.CTkEntry(content_frame, show="*")
        password_entry.pack(fill="x", pady=(0, 10))
        
        # Confirm Password
        ctk.CTkLabel(content_frame, text="Confirm Password", anchor="w", text_color="white").pack(fill="x", pady=(10, 0))
        confirm_password_entry = ctk.CTkEntry(content_frame, show="*")
        confirm_password_entry.pack(fill="x", pady=(0, 10))
        
        # Admin status
        is_admin_var = ctk.BooleanVar(value=False)
        admin_checkbox = ctk.CTkCheckBox(content_frame, text="Admin User", variable=is_admin_var)
        admin_checkbox.pack(pady=10)
        
        # Error label
        error_label = ctk.CTkLabel(content_frame, text="", text_color="#FF0000")
        error_label.pack(pady=5)
        
        # Buttons
        buttons_frame = ctk.CTkFrame(content_frame, fg_color=COLORS["content_bg"])
        buttons_frame.pack(fill="x", pady=(10, 0))
        
        # Function to handle user creation
        def add_user():
            # Get field values
            first_name = first_name_entry.get().strip()
            last_name = last_name_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get()
            confirm = confirm_password_entry.get()
            is_admin = is_admin_var.get()
            
            # Validate fields
            if not first_name or not last_name or not email or not password:
                error_label.configure(text="All fields are required")
                return
            
            if not validate_email(email):
                error_label.configure(text="Invalid email address")
                return
            
            if password != confirm:
                error_label.configure(text="Passwords do not match")
                return
            
            if len(password) < 6:
                error_label.configure(text="Password must be at least 6 characters")
                return
            
            # Add user to database
            try:
                connection = connect_db()
                if not connection:
                    error_label.configure(text="Database connection error")
                    return
                
                cursor = connection.cursor()
                
                # Check if email already exists
                cursor.execute("SELECT user_id FROM Users WHERE email = %s", (email,))
                if cursor.fetchone():
                    error_label.configure(text="Email already in use")
                    return
                
                # Hash password
                hashed_password = hash_password(password)
                
                # Insert new user
                cursor.execute(
                    "INSERT INTO Users (first_name, last_name, email, password, is_admin) VALUES (%s, %s, %s, %s, %s)",
                    (first_name, last_name, email, hashed_password, is_admin)
                )
                
                connection.commit()
                
                # Create default playlist for regular users
                if not is_admin:
                    user_id = cursor.lastrowid
                    cursor.execute(
                        "INSERT INTO Playlists (user_id, name, description) VALUES (%s, %s, %s)",
                        (user_id, "Favorites", "My favorite songs")
                    )
                    connection.commit()
                
                # Close dialog and refresh user list
                dialog.destroy()
                self.load_users()
                messagebox.showinfo("Success", f"User {first_name} {last_name} created successfully")
            
            except Exception as e:
                print(f"Error adding user: {e}")
                traceback.print_exc()
                error_label.configure(text=f"Error: {str(e)[:50]}")
            finally:
                if 'connection' in locals() and connection and connection.is_connected():
                    cursor.close()
                    connection.close()
        
        # Cancel button
        ctk.CTkButton(
            buttons_frame, 
            text="Cancel", 
            fg_color="#666666", 
            hover_color="#444444",
            command=dialog.destroy
        ).pack(side="left", padx=(0, 10), expand=True)
        
        # Save button
        ctk.CTkButton(
            buttons_frame, 
            text="Save", 
            fg_color=COLORS["success"], 
            hover_color=COLORS["success_hover"],
            command=add_user
        ).pack(side="left", expand=True)
    
    def show_edit_user_dialog(self, user_id):
        """Show dialog to edit a user"""
        try:
            # Get user data from database
            connection = connect_db()
            if not connection:
                return
            
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT user_id, first_name, last_name, email, is_admin FROM Users WHERE user_id = %s",
                (user_id,)
            )
            
            user = cursor.fetchone()
            if not user:
                messagebox.showerror("Error", "User not found")
                return
            
            # Create a dialog window
            dialog = ctk.CTkToplevel(self.root)
            dialog.title(f"Edit User: {user['first_name']} {user['last_name']}")
            dialog.geometry("400x400")
            dialog.resizable(False, False)
            dialog.transient(self.root)  # Make dialog modal
            dialog.grab_set()
            
            # Center the dialog
            dialog.update_idletasks()
            width = dialog.winfo_width()
            height = dialog.winfo_height()
            x = (dialog.winfo_screenwidth() // 2) - (width // 2)
            y = (dialog.winfo_screenheight() // 2) - (height // 2)
            dialog.geometry(f"{width}x{height}+{x}+{y}")
            
            # Dialog content
            content_frame = ctk.CTkFrame(dialog, fg_color=COLORS["content_bg"])
            content_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Header
            ctk.CTkLabel(content_frame, text=f"Edit User (ID: {user_id})", font=("Arial", 18, "bold"), text_color="white").pack(pady=(0, 20))
            
            # First Name
            ctk.CTkLabel(content_frame, text="First Name", anchor="w", text_color="white").pack(fill="x", pady=(10, 0))
            first_name_entry = ctk.CTkEntry(content_frame)
            first_name_entry.insert(0, user["first_name"])
            first_name_entry.pack(fill="x", pady=(0, 10))
            
            # Last Name
            ctk.CTkLabel(content_frame, text="Last Name", anchor="w", text_color="white").pack(fill="x", pady=(10, 0))
            last_name_entry = ctk.CTkEntry(content_frame)
            last_name_entry.insert(0, user["last_name"])
            last_name_entry.pack(fill="x", pady=(0, 10))
            
            # Email
            ctk.CTkLabel(content_frame, text="Email", anchor="w", text_color="white").pack(fill="x", pady=(10, 0))
            email_entry = ctk.CTkEntry(content_frame)
            email_entry.insert(0, user["email"])
            email_entry.pack(fill="x", pady=(0, 10))
            
            # Password (optional for editing)
            ctk.CTkLabel(content_frame, text="New Password (leave blank to keep unchanged)", anchor="w", text_color="white").pack(fill="x", pady=(10, 0))
            password_entry = ctk.CTkEntry(content_frame, show="*")
            password_entry.pack(fill="x", pady=(0, 10))
            
            # Admin status
            is_admin_var = ctk.BooleanVar(value=user["is_admin"])
            admin_checkbox = ctk.CTkCheckBox(content_frame, text="Admin User", variable=is_admin_var)
            admin_checkbox.pack(pady=10)
            
            # Disable admin checkbox if editing self
            if user_id == self.admin["user_id"]:
                admin_checkbox.configure(state="disabled")
            
            # Error label
            error_label = ctk.CTkLabel(content_frame, text="", text_color="#FF0000")
            error_label.pack(pady=5)
            
            # Buttons
            buttons_frame = ctk.CTkFrame(content_frame, fg_color=COLORS["content_bg"])
            buttons_frame.pack(fill="x", pady=(10, 0))
            
            # Function to handle user update
            def update_user():
                # Get field values
                first_name = first_name_entry.get().strip()
                last_name = last_name_entry.get().strip()
                email = email_entry.get().strip()
                password = password_entry.get()
                is_admin = is_admin_var.get()
                
                # Validate fields
                if not first_name or not last_name or not email:
                    error_label.configure(text="Name and email are required")
                    return
                
                if not validate_email(email):
                    error_label.configure(text="Invalid email address")
                    return
                
                # Update user in database
                try:
                    connection = connect_db()
                    if not connection:
                        error_label.configure(text="Database connection error")
                        return
                    
                    cursor = connection.cursor()
                    
                    # Check if email already exists for a different user
                    cursor.execute("SELECT user_id FROM Users WHERE email = %s AND user_id != %s", (email, user_id))
                    if cursor.fetchone():
                        error_label.configure(text="Email already in use by another user")
                        return
                    
                    # Update user info
                    if password:  # If password is provided, update it
                        hashed_password = hash_password(password)
                        cursor.execute(
                            "UPDATE Users SET first_name = %s, last_name = %s, email = %s, password = %s, is_admin = %s WHERE user_id = %s",
                            (first_name, last_name, email, hashed_password, is_admin, user_id)
                        )
                    else:  # Otherwise, don't update password
                        cursor.execute(
                            "UPDATE Users SET first_name = %s, last_name = %s, email = %s, is_admin = %s WHERE user_id = %s",
                            (first_name, last_name, email, is_admin, user_id)
                        )
                    
                    connection.commit()
                    
                    # Close dialog and refresh user list
                    dialog.destroy()
                    self.load_users()
                    messagebox.showinfo("Success", f"User {first_name} {last_name} updated successfully")
                
                except Exception as e:
                    print(f"Error updating user: {e}")
                    traceback.print_exc()
                    error_label.configure(text=f"Error: {str(e)[:50]}")
                finally:
                    if 'connection' in locals() and connection and connection.is_connected():
                        cursor.close()
                        connection.close()
            
            # Cancel button
            ctk.CTkButton(
                buttons_frame, 
                text="Cancel", 
                fg_color="#666666", 
                hover_color="#444444",
                command=dialog.destroy
            ).pack(side="left", padx=(0, 10), expand=True)
            
            # Save button
            ctk.CTkButton(
                buttons_frame, 
                text="Save", 
                fg_color=COLORS["success"], 
                hover_color=COLORS["success_hover"],
                command=update_user
            ).pack(side="left", expand=True)
        
        except Exception as e:
            print(f"Error showing edit dialog: {e}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to load user data: {e}")
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def confirm_delete_user(self, user_id):
        """Confirm and delete a user"""
        # Get user info for confirmation message
        try:
            connection = connect_db()
            if not connection:
                return
            
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT first_name, last_name FROM Users WHERE user_id = %s",
                (user_id,)
            )
            
            user = cursor.fetchone()
            if not user:
                messagebox.showerror("Error", "User not found")
                return
            
            # Cannot delete self (current admin)
            if user_id == self.admin["user_id"]:
                messagebox.showerror("Error", "You cannot delete your own account")
                return
            
            # Ask for confirmation
            confirm = messagebox.askyesno(
                "Confirm Delete", 
                f"Are you sure you want to delete user {user['first_name']} {user['last_name']}?\n\nThis will also delete all their playlists and listening history."
            )
            
            if confirm:
                # Delete the user
                cursor.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
                connection.commit()
                
                # Refresh user list
                self.load_users()
                messagebox.showinfo("Success", f"User {user['first_name']} {user['last_name']} deleted successfully")
        
        except Exception as e:
            print(f"Error deleting user: {e}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to delete user: {e}")
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
        app = AdminUserManagement(root)
        root.mainloop()
    except Exception as e:
        print(f"Error in admin user management: {e}")
        traceback.print_exc()
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()