import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime
import os

FILE_NAME = "daily_tracking.csv"

# ---------------- FUNCTIONS ----------------
def initialize_csv():
    """Ensure CSV file exists with correct columns."""
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=["Date", "Day", "Login Time", "Logout Time", "Topics"])
        df.to_csv(FILE_NAME, index=False)

def load_data():
    """Load and display CSV data in the Treeview."""
    for row in tree.get_children():
        tree.delete(row)

    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))
    else:
        initialize_csv()

def update_datetime_fields():
    """Update date, time, and day display fields."""
    now = datetime.now()
    date_entry.config(state="normal")
    time_entry.config(state="normal")
    day_entry.config(state="normal")

    date_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)
    day_entry.delete(0, tk.END)

    date_entry.insert(0, now.strftime("%Y-%m-%d"))
    time_entry.insert(0, now.strftime("%H:%M"))
    day_entry.insert(0, now.strftime("%A"))

    date_entry.config(state="readonly")
    time_entry.config(state="readonly")
    day_entry.config(state="readonly")

def save_data(action):
    """Save login/logout data automatically with current date, time, and day."""
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    day = now.strftime("%A")
    current_time = now.strftime("%H:%M")
    topic = topic_entry.get().strip()

    df = pd.read_csv(FILE_NAME)

    if action == "Login":
        if not topic:
            messagebox.showerror("Error", "Please enter the topic before login.")
            return
        new_entry = pd.DataFrame([[date, day, current_time, "", topic]],
                                 columns=["Date", "Day", "Login Time", "Logout Time", "Topics"])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(FILE_NAME, index=False)
        messagebox.showinfo("Success", f"Login recorded at {current_time} on {day}")
        topic_entry.delete(0, tk.END)

    elif action == "Logout":
        mask = (df["Date"] == date) & ((df["Logout Time"].isna()) | (df["Logout Time"] == ""))
        if mask.any():
            df.loc[mask.idxmax(), "Logout Time"] = current_time
            df.to_csv(FILE_NAME, index=False)
            messagebox.showinfo("Success", f"Logout recorded at {current_time} on {day}")
        else:
            messagebox.showwarning("Warning", "No active login found for today. Please login first.")

    # Refresh table and update time display
    load_data()
    update_datetime_fields()

# ---------------- UI SETUP ----------------
root = tk.Tk()
root.title("📘 Daily Tracker")
root.geometry("700x520")
root.config(bg="#f5f6fa")

# Header
header = tk.Label(
    root, text="Daily Study Tracker", font=("Helvetica", 16, "bold"),
    bg="#2f3640", fg="white", pady=10
)
header.pack(fill="x")

# Frame for inputs
frame = tk.Frame(root, bg="#f5f6fa")
frame.pack(pady=15)

# Date
tk.Label(frame, text="📅 Date:", font=("Arial", 10, "bold"), bg="#f5f6fa").grid(row=0, column=0, padx=10, pady=5, sticky="e")
date_entry = tk.Entry(frame, width=25, font=("Arial", 10))
date_entry.grid(row=0, column=1, pady=5)

# Day
tk.Label(frame, text="🗓️ Day:", font=("Arial", 10, "bold"), bg="#f5f6fa").grid(row=1, column=0, padx=10, pady=5, sticky="e")
day_entry = tk.Entry(frame, width=25, font=("Arial", 10))
day_entry.grid(row=1, column=1, pady=5)

# Time
tk.Label(frame, text="⏰ Current Time:", font=("Arial", 10, "bold"), bg="#f5f6fa").grid(row=2, column=0, padx=10, pady=5, sticky="e")
time_entry = tk.Entry(frame, width=25, font=("Arial", 10))
time_entry.grid(row=2, column=1, pady=5)

# Topic
tk.Label(frame, text="🧠 Topics:", font=("Arial", 10, "bold"), bg="#f5f6fa").grid(row=3, column=0, padx=10, pady=5, sticky="e")
topic_entry = tk.Entry(frame, width=25, font=("Arial", 10))
topic_entry.grid(row=3, column=1, pady=5)

# Buttons frame
btn_frame = tk.Frame(root, bg="#f5f6fa")
btn_frame.pack(pady=10)

login_button = tk.Button(
    btn_frame, text="Login", command=lambda: save_data("Login"),
    bg="#44bd32", fg="white", font=("Arial", 10, "bold"),
    width=12, relief="ridge", cursor="hand2"
)
login_button.grid(row=0, column=0, padx=10)

logout_button = tk.Button(
    btn_frame, text="Logout", command=lambda: save_data("Logout"),
    bg="#e84118", fg="white", font=("Arial", 10, "bold"),
    width=12, relief="ridge", cursor="hand2"
)
logout_button.grid(row=0, column=1, padx=10)

refresh_button = tk.Button(
    btn_frame, text="🔄 Refresh", command=load_data,
    bg="#487eb0", fg="white", font=("Arial", 10, "bold"),
    width=12, relief="ridge", cursor="hand2"
)
refresh_button.grid(row=0, column=2, padx=10)

# Table Frame
table_frame = tk.Frame(root, bg="#f5f6fa")
table_frame.pack(pady=10, fill="both", expand=True)

columns = ("Date", "Day", "Login Time", "Logout Time", "Topics")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
tree.pack(side="left", fill="both", expand=True)

# Scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Set column headings
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=130, anchor="center")

# Footer
footer = tk.Label(
    root, text="Data saved in daily_tracking.csv", bg="#dcdde1",
    font=("Arial", 9), fg="#2f3640", pady=5
)
footer.pack(side="bottom", fill="x")

# ---------------- RUN APP ----------------
initialize_csv()
load_data()
update_datetime_fields()
root.mainloop()
