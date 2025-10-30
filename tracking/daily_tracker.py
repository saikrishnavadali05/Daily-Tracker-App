import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd
from datetime import datetime
import os

FILE_NAME = "daily_schedule_tracking.csv"

# ------------------ Schedule Data ------------------
SCHEDULE = [
    ("5:00 AM", "Wake up -> Music / Devotional Songs Begin"),
    ("5:30 AM - 6:00 AM", "Omkaram & Suprabhatam"),
    ("6:10 AM - 6:30 AM", "Fitness Session"),
    ("7:10 AM - 7:30 AM", "Breakfast Counter Open"),
    ("9:00 AM", "College Begins (with Prayer)"),
    ("3:45 PM", "College Ends"),
    ("4:00 PM", "Return to Hostel"),
    ("4:00 PM - 4:30 PM", "Relaxation & Evening Snacks"),
    ("5:00 PM", "Start to Kulwant Hall"),
    ("5:15 PM", "Bhajans at Sai Kulwant Hall"),
    ("7:10 PM - 7:30 PM", "Dinner Counter Open"),
    ("8:00 PM - 9:45 PM", "Study Hours"),
    ("10:20 PM - 10:30 PM", "Night Prayer & Swami's Discourse Clip"),
]

# ------------------ Functions ------------------
def initialize_csv():
    """Create the CSV file if not present."""
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=["Date", "Day", "Scheduled Time", "Activity", "Login Time", "Logout Time", "Remarks"])
        df.to_csv(FILE_NAME, index=False)

def load_data():
    """Load data into the table view."""
    for row in tree.get_children():
        tree.delete(row)
    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

def record_action(activity, sched_time, action_type):
    """Record login or logout for the given activity."""
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    day = now.strftime("%A")
    current_time = now.strftime("%H:%M")

    df = pd.read_csv(FILE_NAME)

    # Check if an entry for this activity already exists today
    mask = (df["Date"] == date) & (df["Activity"] == activity)

    if action_type == "Login":
        if mask.any():
            messagebox.showinfo("Info", f"Login already recorded for '{activity}'.")
            return
        new_row = pd.DataFrame([[date, day, sched_time, activity, current_time, "", ""]],
                               columns=["Date", "Day", "Scheduled Time", "Activity", "Login Time", "Logout Time", "Remarks"])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(FILE_NAME, index=False)
        messagebox.showinfo("Success", f"✅ Login recorded for '{activity}' at {current_time}")

    elif action_type == "Logout":
        if mask.any():
            idx = df.index[mask][0]
            if pd.isna(df.at[idx, "Logout Time"]) or df.at[idx, "Logout Time"] == "":
                df.at[idx, "Logout Time"] = current_time
                df.to_csv(FILE_NAME, index=False)
                messagebox.showinfo("Success", f"✅ Logout recorded for '{activity}' at {current_time}")
            else:
                messagebox.showinfo("Info", f"Logout already recorded for '{activity}'.")
        else:
            messagebox.showwarning("Warning", f"No login found for '{activity}' today.")

    load_data()

def add_remarks():
    """Add remarks for selected activity in the table."""
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select an activity from the table.")
        return

    values = tree.item(selected_item, "values")
    date, activity = values[0], values[3]

    remark = simpledialog.askstring("Add Remarks", f"Enter your remark for '{activity}':")
    if remark is None or remark.strip() == "":
        return

    df = pd.read_csv(FILE_NAME)
    mask = (df["Date"] == date) & (df["Activity"] == activity)

    if mask.any():
        idx = df.index[mask][0]
        df.at[idx, "Remarks"] = remark
        df.to_csv(FILE_NAME, index=False)
        load_data()
        messagebox.showinfo("Success", f"📝 Remark added for '{activity}'.")
    else:
        messagebox.showwarning("Warning", "No record found for this activity.")

# ------------------ UI ------------------
root = tk.Tk()
root.title("📘 Daily Schedule Tracker (with Remarks)")
root.geometry("900x700")
root.config(bg="#f5f6fa")

# Header
header = tk.Label(
    root, text="Daily Schedule Tracker (with Remarks)", font=("Helvetica", 16, "bold"),
    bg="#2f3640", fg="white", pady=10
)
header.pack(fill="x")

# Table for schedule
schedule_frame = tk.Frame(root, bg="#f5f6fa")
schedule_frame.pack(pady=10, fill="both", expand=True)

columns = ("Scheduled Time", "Activity", "Login", "Logout")
schedule_table = ttk.Treeview(schedule_frame, columns=columns, show="headings", height=14)
schedule_table.pack(side="left", fill="both", expand=True)

for col in columns:
    schedule_table.heading(col, text=col, anchor="center")
    schedule_table.column(col, anchor="center", width=180)

# Scrollbar
scrollbar = ttk.Scrollbar(schedule_frame, orient="vertical", command=schedule_table.yview)
schedule_table.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Populate schedule
for time_slot, activity in SCHEDULE:
    schedule_table.insert("", "end", values=(time_slot, activity, "", ""))

# Button Frame
btn_frame = tk.Frame(root, bg="#f5f6fa")
btn_frame.pack(pady=10)

for i, (sched_time, activity) in enumerate(SCHEDULE):
    lbl = tk.Label(btn_frame, text=f"{sched_time} – {activity}", bg="#f5f6fa", anchor="w", width=55)
    lbl.grid(row=i, column=0, padx=5, pady=2, sticky="w")

    login_btn = tk.Button(
        btn_frame, text="Login", width=10, bg="#44bd32", fg="white",
        command=lambda a=activity, t=sched_time: record_action(a, t, "Login")
    )
    login_btn.grid(row=i, column=1, padx=5, pady=2)

    logout_btn = tk.Button(
        btn_frame, text="Logout", width=10, bg="#e84118", fg="white",
        command=lambda a=activity, t=sched_time: record_action(a, t, "Logout")
    )
    logout_btn.grid(row=i, column=2, padx=5, pady=2)

# Separator
ttk.Separator(root, orient="horizontal").pack(fill="x", pady=10)

# Data table (with Remarks)
data_frame = tk.Frame(root, bg="#f5f6fa")
data_frame.pack(pady=10, fill="both", expand=True)

data_columns = ("Date", "Day", "Scheduled Time", "Activity", "Login Time", "Logout Time", "Remarks")
tree = ttk.Treeview(data_frame, columns=data_columns, show="headings", height=8)
tree.pack(side="left", fill="both", expand=True)

for col in data_columns:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor="center")

scrollbar_data = ttk.Scrollbar(data_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar_data.set)
scrollbar_data.pack(side="right", fill="y")

# Remarks Button
remarks_btn = tk.Button(
    root, text="📝 Add Remark to Selected Activity", bg="#273c75", fg="white",
    font=("Arial", 10, "bold"), command=add_remarks
)
remarks_btn.pack(pady=10)

# Footer
footer = tk.Label(
    root, text="Data saved in daily_schedule_tracking.csv", bg="#dcdde1",
    font=("Arial", 9), fg="#2f3640", pady=5
)
footer.pack(side="bottom", fill="x")

# Initialize
initialize_csv()
load_data()
root.mainloop()
