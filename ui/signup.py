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
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    # Check if any fields are empty
    if not first_name or not last_name or not email or not password or not confirm_password:
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    # Check if passwords match
    if password != confirm_password:
        messagebox.showwarning("Password Error", "Passwords do not match.")
        return

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
ctk.set_appearance_mode("dark")  # Dark Mode
ctk.set_default_color_theme("blue")  # Blue Theme

app = ctk.CTk()
app.title("Online Music System - Sign Up")
app.geometry("750x500")  
app.resizable(False, False)  

# ---------------- Main Frame (Holds everything) ----------------
main_frame = ctk.CTkFrame(app, fg_color="white", corner_radius=0)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# ---------------- Left Side - Branding ----------------
left_frame = ctk.CTkFrame(main_frame, fg_color="#1a202c", width=300, height=500, corner_radius=0)
left_frame.pack(side="left", fill="y")

title_label = ctk.CTkLabel(left_frame, text="🎵 Online Music System",
                           font=("Arial", 18, "bold"), text_color="white")
title_label.place(relx=0.5, rely=0.35, anchor="center")  

desc_label = ctk.CTkLabel(left_frame, text="Join now to experience unlimited ad-free music,\n"
                                           "create custom playlists, and explore new songs.",
                          font=("Arial", 10), text_color="lightgray", wraplength=250)
desc_label.place(relx=0.5, rely=0.5, anchor="center")  

# ---------------- Right Side - Sign-Up Form ----------------
right_frame = ctk.CTkFrame(main_frame, fg_color="white", width=450, height=500, corner_radius=0)
right_frame.pack(side="right", fill="both", expand=True, padx=30, pady=20)

ctk.CTkLabel(right_frame, text="Create an Account", font=("Arial", 16, "bold"), text_color="black").pack(anchor="w")
ctk.CTkLabel(right_frame, text="Sign up to start your journey into the world of non-stop music.",
             font=("Arial", 10), text_color="gray").pack(anchor="w", pady=(0, 10))

# ---------------- Modern Styled Entry Boxes ----------------
def on_focus_in(event):
    event.widget.configure(border_color="#1a202c")

def on_focus_out(event):
    event.widget.configure(border_color="#ddd")

# --- First Name Entry ---
first_name_entry = ctk.CTkEntry(right_frame, placeholder_text="First Name", font=("Arial", 12),
                                fg_color="white", text_color="black", border_color="#ddd", width=300)
first_name_entry.pack(pady=5)
first_name_entry.bind("<FocusIn>", on_focus_in)
first_name_entry.bind("<FocusOut>", on_focus_out)

# --- Last Name Entry ---
last_name_entry = ctk.CTkEntry(right_frame, placeholder_text="Last Name", font=("Arial", 12),
                               fg_color="white", text_color="black", border_color="#ddd", width=300)
last_name_entry.pack(pady=5)
last_name_entry.bind("<FocusIn>", on_focus_in)
last_name_entry.bind("<FocusOut>", on_focus_out)

# --- Email Entry ---
email_entry = ctk.CTkEntry(right_frame, placeholder_text="Email", font=("Arial", 12),
                           fg_color="white", text_color="black", border_color="#ddd", width=300)
email_entry.pack(pady=5)
email_entry.bind("<FocusIn>", on_focus_in)
email_entry.bind("<FocusOut>", on_focus_out)

# --- Password Entry with Toggle ---
password_frame = ctk.CTkFrame(right_frame, fg_color="white", width=300, height=40)
password_frame.pack(pady=5)

password_entry = ctk.CTkEntry(password_frame, placeholder_text="Password", font=("Arial", 12),
                              fg_color="white", text_color="black", border_color="#ddd", width=250, show="*")
password_entry.pack(side="left", padx=5, ipady=5, expand=True)

def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.configure(show="")
        eye_button.configure(text="👁")
    else:
        password_entry.configure(show="*")
        eye_button.configure(text="🔒")

eye_button = ctk.CTkLabel(password_frame, text="👁", font=("Arial", 14), text_color="black", cursor="hand2")
eye_button.pack(side="right", padx=10)
eye_button.bind("<Button-1>", lambda e: toggle_password())

# --- Confirm Password Entry ---
confirm_password_entry = ctk.CTkEntry(right_frame, placeholder_text="Confirm Password", font=("Arial", 12),
                                      fg_color="white", text_color="black", border_color="#ddd", width=300, show="*")
confirm_password_entry.pack(pady=5)
confirm_password_entry.bind("<FocusIn>", on_focus_in)
confirm_password_entry.bind("<FocusOut>", on_focus_out)

# ---------------- Sign-Up Button ----------------
signup_button = ctk.CTkButton(right_frame, text="Sign Up", font=("Arial", 12, "bold"),
                              fg_color="#1a202c", text_color="white", corner_radius=5, height=40, command=signup_user)
signup_button.pack(fill="x", pady=(10, 10))

# ---------------- Login Link ----------------
login_label = ctk.CTkLabel(right_frame, text="Already have an account? Login here",
                           font=("Arial", 10), text_color="black", cursor="hand2", command=open_login_page)
login_label.pack(pady=5)

# ---------------- Social Media Sign-Up ----------------
ctk.CTkLabel(right_frame, text="Or sign up with", font=("Arial", 10), text_color="gray").pack()

social_frame = ctk.CTkFrame(right_frame, fg_color="white")
social_frame.pack(pady=5)

facebook_button = ctk.CTkButton(social_frame, text="Facebook", font=("Arial", 10, "bold"),
                                fg_color="#1877F2", text_color="white", width=90, corner_radius=5)
facebook_button.pack(side="left", padx=5)

google_button = ctk.CTkButton(social_frame, text="Google", font=("Arial", 10, "bold"),
                              fg_color="#DB4437", text_color="white", width=90, corner_radius=5)
google_button.pack(side="right", padx=5)

# ---------------- Run Application ----------------
app.mainloop()
