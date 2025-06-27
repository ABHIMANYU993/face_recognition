# System Architecture & Flow

This document details the system design, data flow, and interactions between the components of the Face Recognition Attendance System.

---

## 🏗️ High-Level System Overview

The system follows a modular architectural pattern consisting of three core layers:
1. **Perception Layer (OpenCV & Camera/Video Feed)**: Captures frames and handles display windows.
2. **Analysis Layer (InsightFace & ONNX Runtime)**: Detects face boundaries and extracts 512-dimensional numerical embedding vectors representing face features.
3. **Storage & Log Layer (SQLite)**: Stores face representations, student metadata, and appends time-stamped attendance logs.

```mermaid
graph TD
    A[Camera/Video Feed] -->|Frames| B[OpenCV Frame Capture]
    B -->|Image Matrix| C[InsightFace Analyzer]
    C -->|RetinaFace| D[Face Detection Bounding Box]
    C -->|ArcFace| E[512D Embedding Vector]
    
    %% Registration
    E -->|Register| F[register_face.py]
    F -->|SQLite Write| G[(students.db)]
    
    %% Attendance
    E -->|Recognize| H[main.py]
    G -->|Read Templates| H
    H -->|Cosine Similarity Comparison| I{Is similarity > 0.6?}
    I -->|Yes| J[Mark Attendance in DB]
    I -->|No| K[Label Unknown Face]
    J -->|SQL Insert| G
```

---

## 🔄 Detailed Process Flow

### 1. Face Registration Process (`register_face.py`)
1. **Camera Initialization**: Reads raw video frames from the configured media source.
2. **Detection**: Passes each frame through `insightface.app.FaceAnalysis`.
3. **Visual Feedback**: Bounding boxes are overlayed on detected faces in real-time.
4. **Registration Trigger**: When the user presses the `s` key:
   - The script prompts the user for the student's Name and ID via terminal standard input.
   - The current frame is processed to retrieve the `512` floating-point face embedding.
   - The ID, Name, and raw embedding bytes (`embedding.tobytes()`) are inserted into the database.
5. **Session Close**: Connection is closed upon pressing `q`.

```mermaid
sequenceDiagram
    actor User
    participant App as register_face.py
    participant Model as InsightFace
    participant DB as SQLite (students)
    
    App->>Model: Initialize buffalo_l model
    App->>App: Read frame from source
    App->>Model: get_face_embedding(frame)
    Model-->>App: Bounding Box & 512D Embedding
    App->>User: Display frame with green box
    User->>App: Press 's' (Save)
    App->>User: Prompt Name & ID
    User->>App: Input Name & ID
    App->>DB: INSERT OR REPLACE INTO students (id, name, embedding)
    DB-->>App: Transaction Commit
    App->>User: Print Confirmation
```

### 2. Live Face Recognition & Attendance Loop (`main.py`)
1. **Initial Load**: Reads all student registrations from SQLite and converts database blobs back to NumPy arrays (`np.frombuffer`).
2. **Continuous Frame Processing**:
   - Captures frame and resizes it to 1280x720.
   - Submits frame to `FaceAnalysis`.
3. **Similarity Check**:
   - For every detected face embedding, it calculates the Cosine Similarity against all loaded student embeddings.
4. **Verification Threshold**:
   - If the similarity value exceeds `0.6` (60% match confidence), the user is matched.
   - Checks if the user has already been marked present in the current session set `attendance_set`.
   - If not marked, logs the timestamped record in the `attendance` SQL table and prints the confirmation.
5. **Rendering Output**:
   - Draws a green bounding box and writes "[Name] - Present" on the face.
   - Draws a red "Unknown" text overlay if no registered templates match.

```mermaid
sequenceDiagram
    participant App as main.py
    participant DB as SQLite (students)
    participant Model as InsightFace
    participant Log as SQLite (attendance)
    
    App->>DB: Fetch all registered students
    DB-->>App: Returns (id, name, embedding_blob)
    App->>App: Deserialize embeddings to float32 NumPy arrays
    
    loop Frame Capture
        App->>App: Read next frame
        App->>Model: Analyze frame for faces
        Model-->>App: Returns (bbox, live_embedding)
        
        loop Compare Live vs Known Templates
            App->>App: Compute Cosine Similarity
        end
        
        alt Similarity > 0.6 & Not marked yet
            App->>Log: INSERT INTO attendance (id, name)
            Log-->>App: Commit log
            App->>App: Add ID to session attendance_set
            App->>App: Render Green Box & "Name - Present"
        else Match not found
            App->>App: Render "Unknown"
        end
    end
```
