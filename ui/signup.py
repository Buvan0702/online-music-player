import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import hashlib
import subprocess
import os

# Database and user functions remain the same
def connect_db():
    """Connect to the MySQL database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="new_password",
            database="online_music_system"
        )
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Database Connection Error", 
                            f"Failed to connect to database: {err}")
        return None

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

def signup_user():
    """Register a new user in the database"""
    full_name = fullname_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    # Validation code remains the same
    if not full_name or not email or not password or not confirm_password:
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    if not validate_email(email):
        messagebox.showwarning("Email Error", "Please enter a valid email address.")
        return

    if not validate_password(password):
        messagebox.showwarning("Password Error", "Password must be at least 8 characters long.")
        return

    if password != confirm_password:
        messagebox.showwarning("Password Error", "Passwords do not match.")
        return

    # Split full name into first and last name
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

        # Database operations remain the same
        cursor.execute("SELECT user_id FROM Users WHERE email = %s", (email,))
        if cursor.fetchone():
            messagebox.showwarning("Registration Error", "This email is already registered.")
            return

        cursor.execute(
            "INSERT INTO Users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, email, hashed_password)
        )

        user_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO Playlists (user_id, name, description) VALUES (%s, %s, %s)",
            (user_id, "Favorites", "My favorite songs")
        )

        connection.commit()
        messagebox.showinfo("Success", "User registered successfully!")
        
        open_login_page()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def open_login_page():
    """Open the login page and close the signup page"""
    try:
        subprocess.Popen(["python", "login.py"])
        root.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Unable to open login page: {e}")

def update_layout(event=None):
    """Update layout based on window size - this is the responsive function"""
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    
    # Minimum sizes to prevent UI breaking
    if window_width < 600:
        window_width = 600
        root.geometry(f"{window_width}x{window_height}")
    
    if window_height < 500:
        window_height = 500
        root.geometry(f"{window_width}x{window_height}")
    
    # Adjust layout based on window width
    if window_width < 800:
        # Stack vertically on smaller screens
        left_frame.configure(width=window_width-20)
        left_frame.pack(side="top", fill="x", padx=10, pady=(10, 5), ipadx=10, ipady=10)
        
        right_frame.configure(width=window_width-20)
        right_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(5, 10))
        
        # Make left frame shorter for vertical layout
        title_label.configure(font=("Arial", 28, "bold"))
        title_label.place(relx=0.5, rely=0.35, anchor="center")
        
        desc_label.configure(font=("Arial", 12))
        desc_label.place(relx=0.5, rely=0.65, anchor="center")
        
        music_icon.place(relx=0.9, rely=0.5, anchor="center")
        
    else:
        # Side by side on larger screens
        left_frame.configure(width=window_width//2-15)
        left_frame.pack(side="left", fill="both", padx=(10, 5), pady=10)
        
        right_frame.configure(width=window_width//2-15)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)
        
        # Adjust font sizes for larger screens
        title_label.configure(font=("Arial", 36, "bold"))
        title_label.place(relx=0.5, rely=0.22, anchor="center")
        
        desc_label.configure(font=("Arial", 14))
        desc_label.place(relx=0.5, rely=0.40, anchor="center")
        
        music_icon.place(relx=0.5, rely=0.75, anchor="center")
    
    # Adjust padding for input fields based on height
    padding_factor = max(10, min(40, window_height // 20))
    content_frame.pack_configure(padx=padding_factor, pady=padding_factor)
    
    # Scale font sizes based on width
    font_size_factor = max(10, min(14, window_width // 80))
    signup_button.configure(font=("Arial", font_size_factor, "bold"))
    
    # Update the content frame to adjust to new size
    content_frame.update()

try:
    # Create temp directory for temporary files if it doesn't exist
    os.makedirs("temp", exist_ok=True)
    
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # Main window
    root = ctk.CTk()
    root.title("Online Music System - Sign Up")
    root.geometry("700x500")
    root.minsize(600, 500)  # Set minimum size
    
    # Make window resizable
    root.resizable(True, True)

    # Main Frame with rounded corners
    main_frame = ctk.CTkFrame(root, corner_radius=20)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Left Side - Branding with purple color
    left_frame = ctk.CTkFrame(main_frame, fg_color="#B146EC", corner_radius=20)
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
    music_icon = ctk.CTkLabel(left_frame, text="🎵🐦", font=("Arial", 40), text_color="white")
    music_icon.place(relx=0.5, rely=0.75, anchor="center")

    # Right Side - Signup Form
    right_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=0)
    right_frame.pack(side="right", fill="both", expand=True)

    # Content container with padding
    content_frame = ctk.CTkFrame(right_frame, fg_color="white")
    content_frame.pack(fill="both", expand=True, padx=40, pady=40)

    # Create an Account title
    title_label_right = ctk.CTkLabel(content_frame, text="Create an Account", 
                              font=("Arial", 28, "bold"), text_color="#B146EC")
    title_label_right.pack(anchor="w", pady=(0, 0))

    # Subtitle
    subtitle_label = ctk.CTkLabel(content_frame, text="Sign up to start your journey into the world of music.",
                                 font=("Arial", 12), text_color="gray")
    subtitle_label.pack(anchor="w", pady=(0, 25))

    # Remaining form elements with flexible layouts
    # Full Name
    fullname_label = ctk.CTkLabel(content_frame, text="Full Name", 
                                 font=("Arial", 14, "bold"), text_color="#333333")
    fullname_label.pack(anchor="w", pady=(0, 5))

    fullname_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    fullname_frame.pack(fill="x", pady=(0, 15))

    fullname_entry = ctk.CTkEntry(fullname_frame, font=("Arial", 12), 
                                 height=45, corner_radius=8,
                                 border_width=1, border_color="#DDDDDD",
                                 fg_color="white", text_color="black")
    fullname_entry.pack(fill="x", side="left", expand=True)

    person_icon = ctk.CTkLabel(fullname_frame, text="👤", font=("Arial", 14), fg_color="transparent")
    person_icon.pack(side="right", padx=(0, 10))

    # Email
    email_label = ctk.CTkLabel(content_frame, text="Email Address", 
                              font=("Arial", 14, "bold"), text_color="#333333")
    email_label.pack(anchor="w", pady=(0, 5))

    email_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    email_frame.pack(fill="x", pady=(0, 15))

    email_entry = ctk.CTkEntry(email_frame, font=("Arial", 12), 
                              height=45, corner_radius=8,
                              border_width=1, border_color="#DDDDDD",
                              fg_color="white", text_color="black")
    email_entry.pack(fill="x", side="left", expand=True)

    email_icon = ctk.CTkLabel(email_frame, text="✉️", font=("Arial", 14), fg_color="transparent")
    email_icon.pack(side="right", padx=(0, 10))

    # Password
    password_label = ctk.CTkLabel(content_frame, text="Password", 
                                 font=("Arial", 14, "bold"), text_color="#333333")
    password_label.pack(anchor="w", pady=(0, 5))

    password_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    password_frame.pack(fill="x", pady=(0, 15))

    password_entry = ctk.CTkEntry(password_frame, font=("Arial", 12), 
                                 height=45, corner_radius=8, 
                                 border_width=1, border_color="#DDDDDD",
                                 fg_color="white", text_color="black", 
                                 show="*")
    password_entry.pack(fill="x", side="left", expand=True)

    password_icon = ctk.CTkLabel(password_frame, text="🔒", font=("Arial", 14), fg_color="transparent")
    password_icon.pack(side="right", padx=(0, 10))

    # Confirm Password
    confirm_password_label = ctk.CTkLabel(content_frame, text="Confirm Password", 
                                         font=("Arial", 14, "bold"), text_color="#333333")
    confirm_password_label.pack(anchor="w", pady=(0, 5))

    confirm_password_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    confirm_password_frame.pack(fill="x", pady=(0, 15))

    confirm_password_entry = ctk.CTkEntry(confirm_password_frame, font=("Arial", 12), 
                                         height=45, corner_radius=8, 
                                         border_width=1, border_color="#DDDDDD",
                                         fg_color="white", text_color="black", 
                                         show="*")
    confirm_password_entry.pack(fill="x", side="left", expand=True)

    confirm_password_icon = ctk.CTkLabel(confirm_password_frame, text="🔒", font=("Arial", 14), fg_color="transparent")
    confirm_password_icon.pack(side="right", padx=(0, 10))

    # Sign Up button with arrow icon
    signup_button = ctk.CTkButton(content_frame, text="Sign Up", 
                                 font=("Arial", 14, "bold"),
                                 fg_color="#B146EC", hover_color="#9333EA", 
                                 text_color="white", corner_radius=8, 
                                 height=45, command=signup_user)
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
                              text_color="#B146EC", cursor="hand2")
    login_label.pack(side="left")
    login_label.bind("<Button-1>", lambda e: open_login_page())

    # Bind events for responsive layout
    root.bind("<Configure>", update_layout)
    
    # Initial layout update
    root.update_idletasks()
    update_layout()

    # Run the application
    root.mainloop()
    
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
    input("Press Enter to exit...")  # This keeps the console open