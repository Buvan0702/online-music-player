import customtkinter as ctk

# ---------------- Initialize CustomTkinter ----------------
ctk.set_appearance_mode("dark")  # "Dark", "Light", "System"
ctk.set_default_color_theme("blue")

# ---------------- Main Application Window ----------------
root = ctk.CTk()
root.title("Online Music System - Login")
root.geometry("750x450")
root.resizable(False, False)

# ---------------- Main Frame (Holds everything) ----------------
main_frame = ctk.CTkFrame(root, fg_color="white", corner_radius=0)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# ---------------- Left Side - Branding ----------------
left_frame = ctk.CTkFrame(main_frame, fg_color="#1a202c", width=300, height=450, corner_radius=0)
left_frame.pack(side="left", fill="y")

title_label = ctk.CTkLabel(left_frame, text="🎵 Online Music System",
                           font=("Arial", 18, "bold"), text_color="white")
title_label.place(relx=0.5, rely=0.4, anchor="center")

desc_label = ctk.CTkLabel(left_frame, text="Enjoy unlimited ad-free music anytime, anywhere.\n"
                                           "Access premium playlists and high-quality audio streaming.",
                          font=("Arial", 10), text_color="lightgray", wraplength=250)
desc_label.place(relx=0.5, rely=0.55, anchor="center")

# ---------------- Right Side - Login Form ----------------
right_frame = ctk.CTkFrame(main_frame, fg_color="white", width=450, height=450, corner_radius=0)
right_frame.pack(side="right", fill="both", expand=True, padx=30, pady=30)

ctk.CTkLabel(right_frame, text="Welcome Back!", font=("Arial", 16, "bold"), text_color="black").pack(anchor="w")
ctk.CTkLabel(right_frame, text="Login to explore a world of non-stop music.",
             font=("Arial", 10), text_color="gray").pack(anchor="w", pady=(0, 10))

# ---------------- Modern Styled Entry Boxes ----------------
# --- Email Entry ---
email_frame = ctk.CTkFrame(right_frame, fg_color="white", border_width=1, border_color="#ddd", corner_radius=0)
email_frame.pack(fill="x", pady=5)

email_icon = ctk.CTkLabel(email_frame, text="📧", font=("Arial", 14), text_color="black")
email_icon.pack(side="left", padx=10)

email_entry = ctk.CTkEntry(email_frame, font=("Arial", 12), fg_color="white", text_color="black",
                           border_width=0, placeholder_text="Enter your email")
email_entry.pack(side="left", padx=5, ipady=8, expand=True)

# --- Password Entry with Toggle ---
password_frame = ctk.CTkFrame(right_frame, fg_color="white", border_width=1, border_color="#ddd", corner_radius=0)
password_frame.pack(fill="x", pady=5)

password_icon = ctk.CTkLabel(password_frame, text="🔒", font=("Arial", 14), text_color="black")
password_icon.pack(side="left", padx=10)

password_entry = ctk.CTkEntry(password_frame, font=("Arial", 12), fg_color="white", text_color="black",
                              border_width=0, show="*", placeholder_text="Enter your password")
password_entry.pack(side="left", padx=5, ipady=8, expand=True)

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

# ---------------- Remember Me & Forgot Password ----------------
remember_frame = ctk.CTkFrame(right_frame, fg_color="white")
remember_frame.pack(fill="x", pady=5)

remember_var = ctk.BooleanVar()
remember_check = ctk.CTkCheckBox(remember_frame, text="Remember me", variable=remember_var, fg_color="white",
                                 text_color="black", font=("Arial", 10), checkbox_height=18, checkbox_width=18)
remember_check.pack(side="left")

forgot_pass = ctk.CTkLabel(remember_frame, text="Forgot password?", font=("Arial", 10), text_color="gray",
                           cursor="hand2")
forgot_pass.pack(side="right")

# ---------------- Login Button ----------------
login_button = ctk.CTkButton(right_frame, text="Login", font=("Arial", 12, "bold"),
                             fg_color="#1a202c", text_color="white", corner_radius=5, height=35)
login_button.pack(fill="x", pady=(10, 10))

# ---------------- Signup Link ----------------
signup_label = ctk.CTkLabel(right_frame, text="Don't have an account? Sign up",
                            font=("Arial", 10), text_color="black", cursor="hand2")
signup_label.pack(pady=5)

# ---------------- Social Media Login ----------------
ctk.CTkLabel(right_frame, text="Or sign in with", font=("Arial", 10), text_color="gray").pack()

social_frame = ctk.CTkFrame(right_frame, fg_color="white")
social_frame.pack(pady=5)

facebook_button = ctk.CTkButton(social_frame, text="Facebook", font=("Arial", 10, "bold"),
                                fg_color="#1877F2", text_color="white", width=90, corner_radius=5)
facebook_button.pack(side="left", padx=5)

google_button = ctk.CTkButton(social_frame, text="Google", font=("Arial", 10, "bold"),
                              fg_color="#DB4437", text_color="white", width=90, corner_radius=5)
google_button.pack(side="right", padx=5)

# ---------------- Run Application ----------------
root.mainloop()
