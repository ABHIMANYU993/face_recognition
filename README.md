# Face Recognition Attendance System

An automated, real-time facial recognition and attendance tracking system built using Python, OpenCV, SQLite, and InsightFace.

The system performs facial detection and generates 512-dimensional embeddings for detected faces. It compares these embeddings with registered faces in an SQLite database using cosine similarity. When a match is found, attendance is automatically marked.

## 📺 Project Demo

<div align="center">

https://github.com/user-attachments/assets/22c53bb1-d2e3-400d-8caa-4388f7908e3c

</div>

---

## 📂 Project Structure

```text
face-recognition/
├── docs/                             # Documentation files
│   ├── architecture.md               # Architecture details & system flow
│   ├── database_schema.md            # SQLite schema details
│   └── face_embeddings.md            # Explanation of face embeddings & InsightFace
├── face_attendance/                  # Core application source
│   ├── database/                     # Directory for SQLite database
│   │   └── students.db               # SQLite database file
│   ├── models/                       # Downloaded InsightFace models (auto-generated)
│   ├── utils/                        # Utility modules
│   │   ├── db_utils.py               # Database helper operations (schema creation)
│   │   └── face_utils.py             # InsightFace initialization & embedding calculations
│   ├── fibnocci.py                   # Reference script (Fibonacci generator)
│   ├── main.py                       # Main attendance detection script
│   ├── register_face.py              # Face registration & training utility
│   ├── test02.mp4                    # Test video file
│   └── test03.mp4                    # Test video file
├── facebasic.py                      # Basic camera capture & downscaling script
├── requirements.txt                  # System dependencies
└── README.md                         # This project documentation
```

---

## 🛠️ Requirements & Setup

It is highly recommended to run this project inside a Python virtual environment (`.venv`).

### Dependencies
All dependencies are declared in `requirements.txt`:
* **OpenCV**: Image & frame capture, rendering windows, bounding boxes, text overlays.
* **InsightFace**: Deep learning library for face detection (RetinaFace) and face recognition (ArcFace). Uses the standard `buffalo_l` model.
* **ONNX Runtime (with GPU support)**: Executes the InsightFace models efficiently using CUDA.
* **NumPy**: Matrix math for computing cosine similarity.
* **SQLite3**: Lightweight relational database storing registered embeddings and log timestamps.

---

## 🚀 Running the Project

Run all commands from the **project root directory**. Activate your virtual environment first, or prefix `python` with your environment's path (e.g., `.venv/bin/python`).

### 1. Register a Face
To register new students/faces in the database:
```bash
python face_attendance/register_face.py
```
* **Controls**:
  * Focus on the camera/video frame window.
  * Press `s` to save the detected face and enter registration details (ID and Name) in your terminal.
  * Press `q` to quit the registration utility.

### 2. Run Attendance monitoring
To track attendance in real time:
```bash
python face_attendance/main.py
```
* The system automatically scans face embeddings, matches them against the database, and stores attendance timestamps if cosine similarity is $> 0.6$.
* **Controls**: Press `q` to exit the window.
