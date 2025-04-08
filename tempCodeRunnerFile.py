import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import hashlib
import subprocess  # To open login.py

# ------------------- Database Connection -------------------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="new_password",  # Replace with your MySQL password
        database="online_music_system"  # Replace with your database name
    )

# ------------------- Password Hashing -------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ------------------- Sign Up Function -------------------
def signup_user():
    full_name = fullname_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    # Check if any fields are empty
    if not full_name or not email or not password or not confirm_password:
        messagebox.showwarning("Input Error", "All fields are required.")
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
        cursor = connection.cursor()

        # Insert the user data into the database
        cursor.execute(
            "INSERT INTO Users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, email, hashed_password)
        )

        connection.commit()
        messagebox.showinfo("Success", "User registered successfully!")
        
        # After successful registration, redirect to login page
        open_login_page()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# ------------------- Open Login Page -------------------
def open_login_page():
    try:
        subprocess.Popen(["python", "login.py"])  # Open login.py after successful signup
        root.quit()  # Close the current signup window
    except Exception as e:
        messagebox.showerror("Error", f"Unable to open login page: {e}")

# ----------------- Setup -----------------
ctk.set_appearance_mode("light")  # Light Mode
ctk.set_default_color_theme("blue")

# Main window
root = ctk.CTk()
root.title("Online Music System - Sign Up")
root.geometry("1000x800")  
root.resizable(False, False)

# Main Frame with rounded corners
main_frame = ctk.CTkFrame(root, corner_radius=20)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Left Side - Branding with purple color
left_frame = ctk.CTkFrame(main_frame, fg_color="#B146EC", width=350, height=480, corner_radius=20)
left_frame.pack(side="left", fill="both")

# Title on the left side
title_label = ctk.CTkLabel(left_frame, text="Online Music System",
                          font=("Arial", 36, "bold"), text_color="white")
title_label.place(relx=0.5, rely=0.22, anchor="center")

# Description text with exact wording from the image
desc_label = ctk.CTkLabel(left_frame, 
                         text="Join now to experience unlimited **ad-free music**,\ncreate custom\nplaylists, and explore new songs.",
                         font=("Arial", 14), text_color="white", justify="center")
desc_label.place(relx=0.5, rely=0.40, anchor="center")

# Right Side - Signup Form
right_frame = ctk.CTkFrame(main_frame, fg_color="white", width=350, height=480, corner_radius=0)
right_frame.pack(side="right", fill="both", expand=True)

# Content container with padding
content_frame = ctk.CTkFrame(right_frame, fg_color="white")
content_frame.pack(fill="both", expand=True, padx=40, pady=40)

# Create an Account title
title_label = ctk.CTkLabel(content_frame, text="Create an Account", 
                          font=("Arial", 28, "bold"), text_color="#B146EC")
title_label.pack(anchor="w", pady=(0, 0))

# Subtitle
subtitle_label = ctk.CTkLabel(content_frame, text="Sign up to start your journey into the world of non-stop music.",
                             font=("Arial", 12), text_color="gray")
subtitle_label.pack(anchor="w", pady=(0, 25))

# Full Name label
fullname_label = ctk.CTkLabel(content_frame, text="Full Name", 
                             font=("Arial", 14, "bold"), text_color="#333333")
fullname_label.pack(anchor="w", pady=(0, 5))

# Full Name Entry with person icon
fullname_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
fullname_frame.pack(fill="x", pady=(0, 15))

fullname_entry = ctk.CTkEntry(fullname_frame, font=("Arial", 12), 
                             height=45, corner_radius=8,
                             border_width=1, border_color="#DDDDDD",
                             fg_color="white", text_color="black")
fullname_entry.pack(fill="x", side="left", expand=True)

person_icon = ctk.CTkLabel(fullname_frame, text="👤", font=("Arial", 14), fg_color="transparent")
person_icon.pack(side="right", padx=(0, 10))

# Email Address label
email_label = ctk.CTkLabel(content_frame, text="Email Address", 
                          font=("Arial", 14, "bold"), text_color="#333333")
email_label.pack(anchor="w", pady=(0, 5))

# Email Entry with envelope icon
email_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
email_frame.pack(fill="x", pady=(0, 15))

email_entry = ctk.CTkEntry(email_frame, font=("Arial", 12), 
                          height=45, corner_radius=8,
                          border_width=1, border_color="#DDDDDD",
                          fg_color="white", text_color="black")
email_entry.pack(fill="x", side="left", expand=True)

email_icon = ctk.CTkLabel(email_frame, text="✉️", font=("Arial", 14), fg_color="transparent")
email_icon.pack(side="right", padx=(0, 10))

# Password label
password_label = ctk.CTkLabel(content_frame, text="Password", 
                             font=("Arial", 14, "bold"), text_color="#333333")
password_label.pack(anchor="w", pady=(0, 5))

# Password Entry with lock icon
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

# Confirm Password label
confirm_password_label = ctk.CTkLabel(content_frame, text="Confirm Password", 
                                     font=("Arial", 14, "bold"), text_color="#333333")
confirm_password_label.pack(anchor="w", pady=(0, 5))

# Confirm Password Entry with lock icon
confirm_password_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
confirm_password_frame.pack(fill="x", pady=(0, 20))

confirm_password_entry = ctk.CTkEntry(confirm_password_frame, font=("Arial", 12), 
                                     height=45, corner_radius=8, 
                                     border_width=1, border_color="#DDDDDD",
                                     fg_color="white", text_color="black", 
                                     show="*")
confirm_password_entry.pack(fill="x", side="left", expand=True)

confirm_password_icon = ctk.CTkLabel(confirm_password_frame, text="🔒", font=("Arial", 14), fg_color="transparent")
confirm_password_icon.pack(side="right", padx=(0, 10))

# Sign Up button with icon
signup_button = ctk.CTkButton(content_frame, text="Sign Up", 
                             font=("Arial", 14, "bold"),
                             fg_color="#B146EC", hover_color="#9333EA", 
                             text_color="white", corner_radius=8, 
                             height=45, command=signup_user)
signup_button.pack(fill="x", pady=(15, 25))

# Add person plus icon to signup button
signup_icon = ctk.CTkLabel(signup_button, text="👤+", font=("Arial", 14, "bold"), text_color="white")
signup_icon.place(relx=0.3, rely=0.5, anchor="e")

# Already have an account text
login_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
login_frame.pack(pady=0)

account_label = ctk.CTkLabel(login_frame, text="Already have an account? ", 
                            font=("Arial", 12), text_color="#333333")
account_label.pack(side="left")

login_label = ctk.CTkLabel(login_frame, text="Login here", 
                          font=("Arial", 12, "bold"), 
                          text_color="#B146EC", cursor="hand2")
login_label.pack(side="left")
login_label.bind("<Button-1>", lambda e: open_login_page())

# Run the application
root.mainloop()