Daily Tracker App

A simple and elegant **Tkinter-based desktop app** built using **Python** to help you log your **daily study sessions**.  
It automatically stores login and logout times in a **CSV file** and displays them neatly in a **scrollable table view** inside the app.

Features
User-friendly and modern Tkinter UI  
Tracks **Login** and **Logout** times  
Saves all records in `daily_tracking.csv`  
Displays all entries in a **scrollable table view**  
Automatically updates date & time fields  
Clean and organized CSV format  

---

## 🖼️ App Interface

```

📅 Date (YYYY-MM-DD)
⏰ Time (HH:MM)
🧠 Topics
[ Login ]   [ Logout ]   [ Refresh ]
------------------------------------

| Date       | Login Time | Logout Time | Topics              |
| ---------- | ---------- | ----------- | ------------------- |
| 2025-10-26 | 09:00      | 10:30       | Python DSA Practice |
| 2025-10-26 | 11:00      | 12:00       | Tkinter UI Project  |

````

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/Daily-Tracker-App.git
````

### 2️⃣ Navigate into the folder

```bash
cd Daily-Tracker-App
```

### 3️⃣ Install dependencies

> Tkinter comes with Python. You only need pandas.

```bash
pip install pandas
```

### 4️⃣ Run the app

```bash
python daily_tracker.py
```

---

## 📄 File Structure

```
Daily-Tracker-App/
│
├── daily_tracker.py       # Main Python app file
├── daily_tracking.csv     # Auto-created data file
├── README.md              # Project description
└── .gitignore             # Optional (ignore CSV files)
```

---

## 📈 Example CSV Output

| Date       | Login Time | Logout Time | Topics             |
| ---------- | ---------- | ----------- | ------------------ |
| 2025-10-26 | 08:45      | 10:00       | DSA Revision       |
| 2025-10-26 | 11:15      | 12:30       | Tkinter UI Project |

---

## 🧰 Technologies Used

* 🐍 Python 3.x
* 🖼️ Tkinter (GUI)
* 📊 Pandas (Data handling)


