"""
Login and signup functionality for the Online Music System.
"""

import os
import subprocess
import customtkinter as ctk
from tkinter import messagebox
import traceback

from config import UI_THEME, UI_COLOR_THEME, COLORS, USER_SESSION_FILE, ADMIN_SESSION_FILE
from utils import (
    connect_db, hash_password, validate_email, validate_password, 
    create_centered_window
)

class LoginSignupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Music System - Login")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        create_centered_window(self.root, 700, 500)
        
        # Initialize UI
        self.create_login_ui()
        
    def create_login_ui(self):
        """Create the login interface"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.title("Online Music System - Login")
        
        # Main Frame with rounded corners
        main_frame = ctk.CTkFrame(self.root, corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Side - Branding
        left_frame = ctk.CTkFrame(main_frame, fg_color=COLORS["primary"], width=350, height=480, corner_radius=20)
        left_frame.pack(side="left", fill="both")

        # Title on the left side
        title_label = ctk.CTkLabel(left_frame, text="Online Music\nSystem",
                                  font=("Arial", 36, "bold"), text_color="white")
        title_label.place(relx=0.5, rely=0.22, anchor="center")

        # Description text below title
        desc_label = ctk.CTkLabel(left_frame, text="Enjoy unlimited *ad-free music*\nanytime, anywhere. Access premium\nplaylists and high-quality audio\nstreaming.",
                                  font=("Arial", 14), text_color="white", justify="center")
        desc_label.place(relx=0.5, rely=0.40, anchor="center")

        # Add music bird illustration
        ctk.CTkLabel(left_frame, text="🎵🐦", font=("Arial", 40), text_color="white").place(relx=0.5, rely=0.75, anchor="center")

        # Right Side - Login Form
        right_frame = ctk.CTkFrame(main_frame, fg_color="white", width=350, height=480, corner_radius=0)
        right_frame.pack(side="right", fill="both", expand=True)

        # Create a container for the right side content with proper padding
        content_frame = ctk.CTkFrame(right_frame, fg_color="white")
        content_frame.pack(fill="both", expand=True, padx=40, pady=40)

        # Welcome Back! label
        welcome_label = ctk.CTkLabel(content_frame, text="Welcome Back!", 
                                    font=("Arial", 28, "bold"), text_color=COLORS["primary"])
        welcome_label.pack(anchor="w", pady=(5, 0))

        # Subtitle
        subtitle_label = ctk.CTkLabel(content_frame, text="Login to explore a world of non-stop music.",
                                     font=("Arial", 12), text_color="gray")
        subtitle_label.pack(anchor="w", pady=(0, 30))

        # Email Address label
        email_label = ctk.CTkLabel(content_frame, text="Email Address", 
                                  font=("Arial", 14, "bold"), text_color="#333333")
        email_label.pack(anchor="w", pady=(0, 5))

        # Email entry with proper icon placement
        email_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        email_frame.pack(fill="x", pady=(0, 15))
        
        self.email_entry = ctk.CTkEntry(email_frame, font=("Arial", 12), 
                                  height=45, corner_radius=8,
                                  border_width=1, border_color="#DDDDDD",
                                  fg_color="white", text_color="black")
        self.email_entry.pack(fill="x", side="left", expand=True)
        
        email_icon = ctk.CTkLabel(email_frame, text="✉️", font=("Arial", 14), fg_color="transparent")
        email_icon.pack(side="right", padx=(0, 10))

        # Password label
        password_label = ctk.CTkLabel(content_frame, text="Password", 
                                     font=("Arial", 14, "bold"), text_color="#333333")
        password_label.pack(anchor="w", pady=(5, 5))

        # Password entry with proper icon placement
        password_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        password_frame.pack(fill="x", pady=(0, 15))
        
        self.password_entry = ctk.CTkEntry(password_frame, font=("Arial", 12), 
                                     height=45, corner_radius=8, 
                                     border_width=1, border_color="#DDDDDD",
                                     fg_color="white", text_color="black", 
                                     show="*")
        self.password_entry.pack(fill="x", side="left", expand=True)
        
        password_icon = ctk.CTkLabel(password_frame, text="🔒", font=("Arial", 14), fg_color="transparent")
        password_icon.pack(side="right", padx=(0, 10))

        # Remember Me & Forgot Password row
        remember_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        remember_frame.pack(fill="x", pady=(5, 20))

        # Remember me checkbox
        self.remember_var = ctk.BooleanVar()
        remember_check = ctk.CTkCheckBox(remember_frame, text="Remember me", 
                                        variable=self.remember_var, 
                                        text_color="#333333", font=("Arial", 12),
                                        fg_color=COLORS["primary"], border_color="#DDDDDD",
                                        checkbox_height=20, checkbox_width=20)
        remember_check.pack(side="left")

        # Forgot password link
        forgot_pass = ctk.CTkLabel(remember_frame, text="Forgot password?", 
                                  font=("Arial", 12), text_color="gray",
                                  cursor="hand2")
        forgot_pass.pack(side="right")
        forgot_pass.bind("<Button-1>", self.show_forgot_password)

        # Login button with login icon
        login_button = ctk.CTkButton(content_frame, text="Login", 
                                    font=("Arial", 14, "bold"),
                                    fg_color=COLORS["primary"], 
                                    hover_color=COLORS["primary_hover"], 
                                    text_color="white", corner_radius=8, 
                                    height=45, command=self.login_user)
        login_button.pack(fill="x", pady=(10, 25))
        
        # Add an arrow icon to the login button
        login_icon_label = ctk.CTkLabel(login_button, text="→", font=("Arial", 16, "bold"), text_color="white")
        login_icon_label.place(relx=0.9, rely=0.5, anchor="e")

        # Don't have an account text
        signup_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        signup_frame.pack(pady=0)

        account_label = ctk.CTkLabel(signup_frame, text="Don't have an account? ", 
                                    font=("Arial", 12), text_color="#333333")
        account_label.pack(side="left")

        # "Sign up" in purple and bold
        signup_label = ctk.CTkLabel(signup_frame, text="Sign up", 
                                   font=("Arial", 12, "bold"), 
                                   text_color=COLORS["primary"], cursor="hand2")
        signup_label.pack(side="left")
        signup_label.bind("<Button-1>", lambda e: self.create_signup_ui())
        
        # Set focus to email entry
        self.email_entry.focus_set()
    
    def create_signup_ui(self):
        """Create the signup interface"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.title("Online Music System - Sign Up")
        
        # Main Frame with rounded corners
        main_frame = ctk.CTkFrame(self.root, corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Side - Branding with purple color
        left_frame = ctk.CTkFrame(main_frame, fg_color=COLORS["primary"], width=350, height=480, corner_radius=20)
        left_frame.pack(side="left", fill="both")

        # Title on the left side
        title_label = ctk.CTkLabel(left_frame, text="Online Music\nSystem",
                                  font=("Arial", 36, "bold"), text_color="white")
        title_label.place(relx=0.5, rely=0.22, anchor="center")

        # Description text below title
        desc_label = ctk.CTkLabel(left_frame, 
                                 text="Join now to experience unlimited\n*ad-free music*, create custom\nplaylists, and explore new songs.",
                                 font=("Arial", 14), text_color="white", justify="center")
        desc_label.place(relx=0.5, rely=0.40, anchor="center")

        # Add music bird illustration
        bird_label = ctk.CTkLabel(left_frame, text="🎵🐦", font=("Arial", 40), text_color="white")
        bird_label.place(relx=0.5, rely=0.75, anchor="center")

        # Right Side - Signup Form
        right_frame = ctk.CTkFrame(main_frame, fg_color="white", width=350, height=480, corner_radius=0)
        right_frame.pack(side="right", fill="both", expand=True)

        # Content container with padding
        content_frame = ctk.CTkFrame(right_frame, fg_color="white")
        content_frame.pack(fill="both", expand=True, padx=40, pady=40)

        # Create an Account title
        right_title_label = ctk.CTkLabel(content_frame, text="Create an Account", 
                                  font=("Arial", 28, "bold"), text_color=COLORS["primary"])
        right_title_label.pack(anchor="w", pady=(0, 0))

        # Subtitle
        subtitle_label = ctk.CTkLabel(content_frame, text="Sign up to start your journey into the world of music.",
                                     font=("Arial", 12), text_color="gray")
        subtitle_label.pack(anchor="w", pady=(0, 25))

        # Full Name label
        fullname_label = ctk.CTkLabel(content_frame, text="Full Name", 
                                     font=("Arial", 14, "bold"), text_color="#333333")
        fullname_label.pack(anchor="w", pady=(0, 5))

        # Full Name Entry with person icon
        fullname_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        fullname_frame.pack(fill="x", pady=(0, 15))

        self.fullname_entry = ctk.CTkEntry(fullname_frame, font=("Arial", 12), 
                                     height=45, corner_radius=8,
                                     border_width=1, border_color="#DDDDDD",
                                     fg_color="white", text_color="black")
        self.fullname_entry.pack(fill="x", side="left", expand=True)

        person_icon = ctk.CTkLabel(fullname_frame, text="👤", font=("Arial", 14), fg_color="transparent")
        person_icon.pack(side="right", padx=(0, 10))

        # Email Address label
        email_label = ctk.CTkLabel(content_frame, text="Email Address", 
                                  font=("Arial", 14, "bold"), text_color="#333333")
        email_label.pack(anchor="w", pady=(0, 5))

        # Email Entry with envelope icon
        email_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        email_frame.pack(fill="x", pady=(0, 15))

        self.email_entry = ctk.CTkEntry(email_frame, font=("Arial", 12), 
                                  height=45, corner_radius=8,
                                  border_width=1, border_color="#DDDDDD",
                                  fg_color="white", text_color="black")
        self.email_entry.pack(fill="x", side="left", expand=True)

        email_icon = ctk.CTkLabel(email_frame, text="✉️", font=("Arial", 14), fg_color="transparent")
        email_icon.pack(side="right", padx=(0, 10))

        # Password label
        password_label = ctk.CTkLabel(content_frame, text="Password", 
                                     font=("Arial", 14, "bold"), text_color="#333333")
        password_label.pack(anchor="w", pady=(0, 5))

        # Password Entry with lock icon
        password_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        password_frame.pack(fill="x", pady=(0, 15))

        self.password_entry = ctk.CTkEntry(password_frame, font=("Arial", 12), 
                                     height=45, corner_radius=8, 
                                     border_width=1, border_color="#DDDDDD",
                                     fg_color="white", text_color="black", 
                                     show="*")
        self.password_entry.pack(fill="x", side="left", expand=True)

        password_icon = ctk.CTkLabel(password_frame, text="🔒", font=("Arial", 14), fg_color="transparent")
        password_icon.pack(side="right", padx=(0, 10))

        # Confirm Password label
        confirm_password_label = ctk.CTkLabel(content_frame, text="Confirm Password", 
                                             font=("Arial", 14, "bold"), text_color="#333333")
        confirm_password_label.pack(anchor="w", pady=(0, 5))

        # Confirm Password Entry with lock icon
        confirm_password_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        confirm_password_frame.pack(fill="x", pady=(0, 15))

        self.confirm_password_entry = ctk.CTkEntry(confirm_password_frame, font=("Arial", 12), 
                                             height=45, corner_radius=8, 
                                             border_width=1, border_color="#DDDDDD",
                                             fg_color="white", text_color="black", 
                                             show="*")
        self.confirm_password_entry.pack(fill="x", side="left", expand=True)

        confirm_password_icon = ctk.CTkLabel(confirm_password_frame, text="🔒", font=("Arial", 14), fg_color="transparent")
        confirm_password_icon.pack(side="right", padx=(0, 10))

        # Sign Up button with arrow icon
        signup_button = ctk.CTkButton(content_frame, text="Sign Up", 
                                     font=("Arial", 14, "bold"),
                                     fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], 
                                     text_color="white", corner_radius=8, 
                                     height=45, command=self.signup_user)
        signup_button.pack(fill="x", pady=(10, 20))

        # Add an arrow icon to the signup button
        signup_icon_label = ctk.CTkLabel(signup_button, text="→", font=("Arial", 16, "bold"), text_color="white")
        signup_icon_label.place(relx=0.9, rely=0.5, anchor="e")

        # Already have an account text
        login_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        login_frame.pack(pady=0)

        account_label = ctk.CTkLabel(login_frame, text="Already have an account? ", 
                                    font=("Arial", 12), text_color="#333333")
        account_label.pack(side="left")

        login_label = ctk.CTkLabel(login_frame, text="Login", 
                                  font=("Arial", 12, "bold"), 
                                  text_color=COLORS["primary"], cursor="hand2")
        login_label.pack(side="left")
        login_label.bind("<Button-1>", lambda e: self.create_login_ui())
        
        # Set focus to fullname entry
        self.fullname_entry.focus_set()
    
    def login_user(self):
        """Authenticate user and open home page if successful"""
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showwarning("Input Error", "Please enter both email and password.")
            return
        
        # Hash the password for security
        hashed_password = hash_password(password)

        try:
            connection = connect_db()
            if not connection:
                return
                
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT user_id, first_name, last_name, is_admin FROM Users WHERE email = %s AND password = %s",
                (email, hashed_password)
            )
            user = cursor.fetchone()

            if user:
                user_id = user["user_id"]
                first_name = user["first_name"]
                last_name = user["last_name"]
                is_admin = user["is_admin"]
                
                messagebox.showinfo("Success", f"Welcome {first_name} {last_name}!")
                
                # Save user ID to a file for session persistence
                with open(USER_SESSION_FILE, "w") as f:
                    f.write(str(user_id))
                
                # If admin, also create admin session file
                if is_admin:
                    with open(ADMIN_SESSION_FILE, "w") as f:
                        f.write(str(user_id))
                    # Open admin page
                    subprocess.Popen(["python", "admin/admin_view.py"])
                else:
                    # Open user home page
                    subprocess.Popen(["python", "user/user_view.py"])
                
                # Close the login window
                self.root.destroy()
            else:
                messagebox.showerror("Login Failed", "Invalid Email or Password.")
        
        except Exception as err:
            print(f"Login error: {err}")
            messagebox.showerror("Database Error", str(err))
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def signup_user(self):
        """Register a new user in the database"""
        full_name = self.fullname_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Check if any fields are empty
        if not full_name or not email or not password or not confirm_password:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        # Validate email format
        if not validate_email(email):
            messagebox.showwarning("Email Error", "Please enter a valid email address.")
            return

        # Validate password strength
        if not validate_password(password):
            messagebox.showwarning("Password Error", "Password must be at least 8 characters long.")
            return

        # Check if passwords match
        if password != confirm_password:
            messagebox.showwarning("Password Error", "Passwords do not match.")
            return

        # Split full name into first and last name (assuming space separator)
        name_parts = full_name.split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Hash the password
        hashed_password = hash_password(password)

        try:
            connection = connect_db()
            if not connection:
                return
                
            cursor = connection.cursor()

            # Check if email already exists
            cursor.execute("SELECT user_id FROM Users WHERE email = %s", (email,))
            if cursor.fetchone():
                messagebox.showwarning("Registration Error", "This email is already registered.")
                return

            # Insert the user data into the database
            cursor.execute(
                "INSERT INTO Users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                (first_name, last_name, email, hashed_password)
            )

            # Get the new user ID
            user_id = cursor.lastrowid

            # Create default playlist for the user
            cursor.execute(
                "INSERT INTO Playlists (user_id, name, description) VALUES (%s, %s, %s)",
                (user_id, "Favorites", "My favorite songs")
            )

            connection.commit()
            messagebox.showinfo("Success", "User registered successfully!")
            
            # After successful registration, redirect to login page
            self.create_login_ui()

        except Exception as err:
            print(f"Signup error: {err}")
            messagebox.showerror("Database Error", str(err))
        finally:
            if 'connection' in locals() and connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def show_forgot_password(self, event=None):
        """Show the forgot password dialog"""
        messagebox.showinfo("Forgot Password", "Please contact the system administrator to reset your password.")

# ------------------- Main Entry Point -------------------
def main():
    try:
        # Set the appearance mode
        ctk.set_appearance_mode(UI_THEME)
        ctk.set_default_color_theme(UI_COLOR_THEME)
        
        # Create the login window
        root = ctk.CTk()
        app = LoginSignupApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error in login/signup app: {e}")
        traceback.print_exc()
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()