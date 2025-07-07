# 👨‍🏫 Face Recognition Attendance System (Streamlit)

> A browser-based, AI-powered attendance system using real-time face recognition built with deep learning, powered by Streamlit and OpenCV.

---

## 🚀 Overview

The **Face Recognition Attendance System** is a modern web application that uses your webcam to detect and recognize faces and mark attendance in real-time. Built using **Streamlit**, **face_recognition**, and **OpenCV**, it replaces traditional manual attendance with an automated and intelligent solution.

---

## 🌟 Features

### ✅ Face Registration
- Register users via webcam.
- Captured face images are saved under `known_faces/`.
- Each image is encoded using deep learning for accurate matching.

### 🧠 Face Recognition & Attendance
- Detects and matches faces live through your webcam.
- If a known face is found, attendance is marked automatically.
- Attendance is saved with Name, Date, and Time.

### 🕒 Timestamped Logging
- All attendance is logged in CSV format in `/attendance/`.
- Ensures integrity and easy analysis.

### 📆 Export Monthly Reports
- Filter attendance by month/year.
- Download logs as CSV for offline use.

### 📸 Webcam Integration
- Real-time video feed via OpenCV.
- High accuracy and performance.

### 📤 Export Attendance
- Easily download data for recordkeeping or submission.

### 🔐 Admin Login (Optional)
- Add password-protected access with Streamlit session states.

---

## 📦 Project Structure

face_attendance_streamlit/
├── app.py # Main Streamlit app
├── utils.py # Face encoding, recognition helpers
├── known_faces/ # Stored user face images
├── attendance/ # Attendance logs
├── requirements.txt # Required packages
└── README.md # Project overview


---

## 🛠️ Installation

### 💻 Requirements
- Python 3.7+
- Streamlit
- face_recognition
- OpenCV

### 🔧 Setup Instructions
   # Clone the repository
     git clone https://github.com/your-username/face-attendance-streamlit.git
     cd face-attendance-streamlit
   # Create and activate a virtual environment
     python -m venv venv
     venv\Scripts\activate  # On Windows
     source venv/bin/activate  # On Linux/Mac
   # Install dependencies
     pip install -r requirements.txt

   # Run the app
     streamlit run app.py
  
  
Then open in browser: http://localhost:8501

🖼️ Usage Instructions
   📌 Register a Face
    > Go to the “Register Face” tab.
    > Enter the person’s full name.
    > Click Capture — the webcam opens and captures an image.
    > Face image is encoded and stored in known_faces/.

  📝 Mark Attendance
    > Navigate to the “Attendance” tab.
    > Click Start Recognition.
    > Webcam will detect faces in real time.
    > If a match is found, attendance is logged with timestamp.

  📊 Export Monthly Reports
    > Go to the “Export” tab.
    > Select desired month and year.
    > Preview and download the report as a .csv.

🧠 How It Works
    > Uses face_recognition (built on dlib + deep ResNet).
    > Converts face images into 128-dimensional feature vectors.
    > Compares real-time face encodings to stored known encodings using Euclidean distance.
    > Matching is based on a configurable tolerance threshold (0.6 default).

🐍 Example Code
   1. Register a Face
      image = face_recognition.load_image_file("known_faces/alex.jpg")
      encoding = face_recognition.face_encodings(image)[0]
      # Store encoding and name for later matching

   2. Mark Attendance
      matches = face_recognition.compare_faces(known_encodings, current_encoding)
      if True in matches:
      mark_attendance(name) 


📱 APK Conversion (Android)
  You can convert this Streamlit app into an Android APK using:

  Option 1: Host App + TWA (Trusted Web Activity)
      > Deploy app to Render, HuggingFace Spaces, or Streamlit Cloud
      > Wrap with TWA using Bubblewrap

  Option 2: Android WebView
      > Create a simple Android app that loads your hosted Streamlit app in a WebView.

  Option 3: Kivy + Buildozer (Advanced)
      > Rebuild UI using Kivy and package to APK with Buildozer.

📘 Tutorial coming soon: "Convert Streamlit Web App to APK"


🛑 Common Issues
 1. Webcam Not Opening?
    > Ensure no other application is using the webcam.
    > Try cv2.VideoCapture(1) instead of 0.

 2. Face Not Recognized?
    > Use well-lit images for registration.
    > Ensure frontal face orientation.
    > Adjust tolerance in code if needed (e.g., tolerance=0.5).


📚 Related Articles & Tools
    > Modern Face Recognition with Deep Learning
    > Streamlit Documentation
    > face_recognition GitHub
    > Deploying Streamlit on Render


👨‍💻 Developer
    Urvashi Bapna
    GitHub: @urvashibapna
    Email: bapnaurvashi@gmail.com

📜 License
   This project is licensed under the MIT License.
   See LICENSE for full details.


🌟 Acknowledgments
  > @ageitgey for the face_recognition library 
  > Davis King for dlib
  > The awesome Python, OpenCV, and Streamlit communities

🙏 Support
   If you found this project helpful:
  ⭐ Star this repo
  🐞 Submit issues or suggestions
  📢 Share with others!




