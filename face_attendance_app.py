import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import cv2
import face_recognition
import numpy as np
import pandas as pd
import os
import glob
import time
from datetime import datetime

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123"

# Paths
IMAGE_DIR = 'images'
ATTENDANCE_FILE = 'Attendance.xlsx'

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Face recognition functions
def load_known_faces():
    images, names = [], []
    for filename in os.listdir(IMAGE_DIR):
        if filename.endswith(".jpg") and os.path.isfile(os.path.join(IMAGE_DIR, filename)):
            img_path = os.path.join(IMAGE_DIR, filename)
            img = cv2.imread(img_path)
            if img is not None:
                images.append(img)
                names.append(os.path.splitext(filename)[0])
    return images, names

def encode_faces(images):
    encodings = []
    for i, img in enumerate(images):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        enc = face_recognition.face_encodings(rgb)
        if enc:
            encodings.append(enc[0])
        else:
            print(f"Warning: No face found in known image #{i}")
    return encodings

def save_attendance_image(name, frame):
    person_dir = os.path.join(IMAGE_DIR, name)
    os.makedirs(person_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = os.path.join(person_dir, f"{timestamp}.jpg")
    cv2.imwrite(image_path, frame)

    images = sorted(glob.glob(os.path.join(person_dir, "*.jpg")), key=os.path.getmtime)
    if len(images) > 10:
        for old_img in images[:-10]:
            os.remove(old_img)

def mark_attendance(name):
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M:%S')

    try:
        df = pd.read_excel(ATTENDANCE_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Name', 'Date', 'Time'])

    already_marked = ((df['Name'] == name) & (df['Date'] == date_str)).any()

    if not already_marked:
        new_entry = pd.DataFrame([[name, date_str, time_str]], columns=['Name', 'Date', 'Time'])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_excel(ATTENDANCE_FILE, index=False)
        attendance_status_label.config(text=f"Attendance marked for {name}", fg="#00796B")

# --- Admin Functions ---

def add_new_person():
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Please enter a name.")
        return

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cam.isOpened():
        messagebox.showerror("Error", "Could not open webcam for capturing.")
        return

    messagebox.showinfo("Capture", "Press SPACE to capture image, ESC to cancel.")

    while True:
        ret, frame = cam.read()
        if not ret:
            messagebox.showerror("Error", "Failed to grab frame from webcam.")
            break
        cv2.imshow("Capture New Face", frame)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            break
        elif k % 256 == 32:
            img_path = os.path.join(IMAGE_DIR, f"{name}.jpg")
            cv2.imwrite(img_path, frame)
            messagebox.showinfo("Success", f"Image saved: {img_path}")
            break

    cam.release()
    cv2.destroyAllWindows()

def generate_2025_months():
    months = []
    for month in range(1, 13):
        dt = datetime(year=2025, month=month, day=1)
        display_name = dt.strftime("%B %Y")
        yyyy_mm = dt.strftime("%Y-%m")
        months.append((display_name, yyyy_mm))
    return months

def download_attendance():
    selected_display = month_var.get()
    if not selected_display:
        messagebox.showerror("Error", "Please select a month.")
        return

    yyyy_mm = None
    for disp, y in month_map:
        if disp == selected_display:
            yyyy_mm = y
            break

    if yyyy_mm is None:
        messagebox.showerror("Error", "Invalid month selected.")
        return

    try:
        df = pd.read_excel(ATTENDANCE_FILE)
    except FileNotFoundError:
        messagebox.showerror("Error", "Attendance file not found.")
        return

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])

    filtered_df = df[df['Date'].dt.strftime('%Y-%m') == yyyy_mm]

    if filtered_df.empty:
        messagebox.showinfo("No Data", f"No attendance records found for {selected_display}.")
        return

    filtered_df['Date'] = filtered_df['Date'].dt.strftime('%Y-%m-%d')
    save_path = f"Attendance_{yyyy_mm}.xlsx"
    filtered_df.to_excel(save_path, index=False)
    messagebox.showinfo("Download Complete", f"Attendance for {selected_display} saved as {save_path}")

# --- Attendance Recognition ---

def start_attendance():
    images, names = load_known_faces()
    if not images:
        messagebox.showwarning("Warning", "No registered faces found.")
        return

    known_encodings = encode_faces(images)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        attendance_status_label.config(text="Error: Could not open webcam.", fg="#D32F2F")
        messagebox.showerror("Error", "Could not open webcam. Please check your camera.")
        return

    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            attendance_status_label.config(text="Webcam error.", fg="#D32F2F")
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small)
        face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)

            if face_distances.size > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = names[best_match_index]
                    mark_attendance(name)
                    save_attendance_image(name, frame)

                    top, right, bottom, left = [v * 2 for v in face_location]
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left, top - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow("Attendance System (Auto-closes in 5s)", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break
        if time.time() - start_time > 5:
            break

    cap.release()
    cv2.destroyAllWindows()
    attendance_status_label.config(text="Attendance session ended.", fg="#00796B")

# --- Admin Login ---

def open_admin_panel():
    # Create new window for admin panel
    admin_win = tk.Toplevel(root)
    admin_win.title("Admin Panel")
    admin_win.geometry("550x360")
    admin_win.configure(bg="#E0F7FA")
    admin_win.resizable(False, False)

    # Styling for Combobox in admin window
    style = ttk.Style(admin_win)
    style.theme_use('default')
    style.configure("TCombobox", fieldbackground="white", background="#00ACC1", foreground="#006064")

    # Name Entry for Add New Face
    tk.Label(admin_win, text="Enter Name to Register:", font=("Arial", 12), bg="#E0F7FA", fg="#006064").pack(pady=10)
    global name_entry  # Needed so add_new_person() can access this
    name_entry = tk.Entry(admin_win, font=("Arial", 12), width=30, bg="white", fg="#006064",
                          highlightbackground="#00ACC1", highlightcolor="#00ACC1", highlightthickness=1)
    name_entry.pack(pady=5)

    tk.Button(admin_win, text="Add New Face", font=("Arial", 12), bg="#00ACC1", fg="white",
              activebackground="#00838F", command=add_new_person).pack(pady=10)

    # Download Attendance Section
    tk.Label(admin_win, text="Download Attendance by Month:", font=("Arial", 11), bg="#E0F7FA", fg="#006064").pack(pady=5)

    global month_map
    month_map = generate_2025_months()
    global month_var
    month_var = tk.StringVar()
    month_dropdown = ttk.Combobox(admin_win, textvariable=month_var, font=("Arial", 11), state="readonly",
                                  values=[m[0] for m in month_map])
    month_dropdown.pack(pady=5)

    tk.Button(admin_win, text="Download", font=("Arial", 11), bg="#00ACC1", fg="white",
              command=download_attendance).pack(pady=5)

    # Exit button closes admin panel window only
    tk.Button(admin_win, text="Exit", font=("Arial", 12), bg="#00ACC1", fg="white",
              command=admin_win.destroy).pack(pady=15)

def show_login_dialog():
    login_win = tk.Toplevel(root)
    login_win.title("Admin Login")
    login_win.geometry("300x200")
    login_win.configure(bg="#E0F7FA")
    login_win.resizable(False, False)
    login_win.grab_set()

    tk.Label(login_win, text="Username:", bg="#E0F7FA", fg="#006064", font=("Arial", 12)).pack(pady=5)
    username_entry = tk.Entry(login_win, font=("Arial", 12))
    username_entry.pack(pady=5)

    tk.Label(login_win, text="Password:", bg="#E0F7FA", fg="#006064", font=("Arial", 12)).pack(pady=5)
    password_entry = tk.Entry(login_win, show="*", font=("Arial", 12))
    password_entry.pack(pady=5)

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            login_win.destroy()
            open_admin_panel()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    tk.Button(login_win, text="Login", font=("Arial", 12), bg="#00ACC1", fg="white",
              command=attempt_login).pack(pady=10)

# --- Main Window ---

root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("480x260")
root.configure(bg="#E0F7FA")
root.resizable(False, False)

tk.Label(root, text="Face Recognition Attendance System", font=("Arial", 14, "bold"), bg="#E0F7FA", fg="#006064").pack(pady=15)

tk.Button(root, text="Start Attendance", font=("Arial", 14), bg="#00ACC1", fg="white",
          activebackground="#00838F", command=start_attendance).pack(pady=15)

attendance_status_label = tk.Label(root, text="", font=("Arial", 11), fg="#00796B", bg="#E0F7FA")
attendance_status_label.pack(pady=5)

tk.Button(root, text="Admin Login", font=("Arial", 12), bg="#00ACC1", fg="white",
          activebackground="#00838F", command=show_login_dialog).pack(pady=20)

tk.Button(root, text="Exit", font=("Arial", 12), bg="#00ACC1", fg="white",
          activebackground="#00838F", command=root.destroy).pack()

root.mainloop()
