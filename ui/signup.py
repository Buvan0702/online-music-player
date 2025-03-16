import tkinter as tk
from tkinter import ttk

# ---------------- Main Application Window ----------------
root = tk.Tk()
root.title("Online Music System - Sign Up")
root.geometry("750x500")  # Correct window size
root.resizable(False, False)  # Prevent resizing
root.configure(bg="#1a202c")  # Dark background

# ---------------- Main Frame (Holds everything) ----------------
main_frame = tk.Frame(root, bg="white", relief="flat")
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=750, height=500)

# ---------------- Left Side - Branding ----------------
left_frame = tk.Frame(main_frame, bg="#1a202c", width=300, height=500)
left_frame.pack(side="left", fill="y")

title_label = tk.Label(left_frame, text="🎵 Online Music System", font=("Arial", 18, "bold"), bg="#1a202c", fg="white")
title_label.place(relx=0.5, rely=0.35, anchor="center")  # Centered

desc_label = tk.Label(left_frame, text="Join now to experience unlimited ad-free music,\ncreate custom playlists, and explore new songs.",
                      font=("Arial", 10), bg="#1a202c", fg="lightgray", justify="center", wraplength=250)
desc_label.place(relx=0.5, rely=0.5, anchor="center")  # Centered below title

# ---------------- Right Side - Sign-Up Form ----------------
right_frame = tk.Frame(main_frame, bg="white", width=450, height=500)
right_frame.pack(side="right", fill="both", expand=True, padx=30, pady=20)

tk.Label(right_frame, text="Create an Account", font=("Arial", 16, "bold"), bg="white", fg="black").pack(anchor="w")
tk.Label(right_frame, text="Sign up to start your journey into the world of non-stop music.", font=("Arial", 10), bg="white", fg="gray").pack(anchor="w", pady=(0, 10))

# ---------------- Modern Styled Entry Boxes ----------------
def on_focus_in(event):
    event.widget.config(highlightbackground="#1a202c", highlightthickness=2)

def on_focus_out(event):
    event.widget.config(highlightbackground="#ddd", highlightthickness=1)

# --- Full Name Entry with Icon ---
name_frame = tk.Frame(right_frame, bg="white", bd=1, relief="solid", highlightbackground="#ddd", highlightthickness=1)
name_frame.pack(fill="x", pady=5)

name_icon = tk.Label(name_frame, text="👤", bg="white", font=("Arial", 14))
name_icon.pack(side="left", padx=10)

name_entry = tk.Entry(name_frame, font=("Arial", 12), bg="white", fg="black", relief="flat")
name_entry.pack(side="left", padx=5, ipady=8, expand=True)
name_entry.bind("<FocusIn>", on_focus_in)
name_entry.bind("<FocusOut>", on_focus_out)

# --- Email Entry with Icon ---
email_frame = tk.Frame(right_frame, bg="white", bd=1, relief="solid", highlightbackground="#ddd", highlightthickness=1)
email_frame.pack(fill="x", pady=5)

email_icon = tk.Label(email_frame, text="📧", bg="white", font=("Arial", 14))
email_icon.pack(side="left", padx=10)

email_entry = tk.Entry(email_frame, font=("Arial", 12), bg="white", fg="black", relief="flat")
email_entry.pack(side="left", padx=5, ipady=8, expand=True)
email_entry.bind("<FocusIn>", on_focus_in)
email_entry.bind("<FocusOut>", on_focus_out)

# --- Password Entry with Icon & Toggle ---
password_frame = tk.Frame(right_frame, bg="white", bd=1, relief="solid", highlightbackground="#ddd", highlightthickness=1)
password_frame.pack(fill="x", pady=5)

password_icon = tk.Label(password_frame, text="🔒", bg="white", font=("Arial", 14))
password_icon.pack(side="left", padx=10)

password_entry = tk.Entry(password_frame, show="*", font=("Arial", 12), bg="white", fg="black", relief="flat")
password_entry.pack(side="left", padx=5, ipady=8, expand=True)
password_entry.bind("<FocusIn>", on_focus_in)
password_entry.bind("<FocusOut>", on_focus_out)

def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        eye_icon.config(text="👁")
    else:
        password_entry.config(show="*")
        eye_icon.config(text="🔒")

eye_icon = tk.Label(password_frame, text="👁", bg="white", font=("Arial", 14), cursor="hand2")
eye_icon.pack(side="right", padx=10)
eye_icon.bind("<Button-1>", lambda e: toggle_password())

# --- Confirm Password Entry with Icon ---
confirm_password_frame = tk.Frame(right_frame, bg="white", bd=1, relief="solid", highlightbackground="#ddd", highlightthickness=1)
confirm_password_frame.pack(fill="x", pady=5)

confirm_password_icon = tk.Label(confirm_password_frame, text="🔒", bg="white", font=("Arial", 14))
confirm_password_icon.pack(side="left", padx=10)

confirm_password_entry = tk.Entry(confirm_password_frame, show="*", font=("Arial", 12), bg="white", fg="black", relief="flat")
confirm_password_entry.pack(side="left", padx=5, ipady=8, expand=True)
confirm_password_entry.bind("<FocusIn>", on_focus_in)
confirm_password_entry.bind("<FocusOut>", on_focus_out)

# ---------------- Sign-Up Button ----------------
signup_button = tk.Button(right_frame, text="Sign Up", font=("Arial", 12, "bold"), bg="#1a202c", fg="white",
                          relief="flat", cursor="hand2", height=2, activebackground="#333")
signup_button.pack(fill="x", pady=(10, 10))

# ---------------- Login Link ----------------
login_label = tk.Label(right_frame, text="Already have an account? Login here", font=("Arial", 10), bg="white", fg="black", cursor="hand2")
login_label.pack(pady=5)

# ---------------- Social Media Sign-Up ----------------
tk.Label(right_frame, text="Or sign up with", font=("Arial", 10), bg="white", fg="gray").pack()

social_frame = tk.Frame(right_frame, bg="white")
social_frame.pack(pady=5)

facebook_button = tk.Button(social_frame, text="Facebook", font=("Arial", 10, "bold"), bg="#1877F2", fg="white", width=12)
facebook_button.pack(side="left", padx=5)

google_button = tk.Button(social_frame, text="Google", font=("Arial", 10, "bold"), bg="#DB4437", fg="white", width=12)
google_button.pack(side="right", padx=5)

# ---------------- Run Application ----------------
root.mainloop()
