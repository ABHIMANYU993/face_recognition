# main.py
import cv2
import sqlite3
import numpy as np
from utils.face_utils import get_face_embedding, cosine_similarity
from utils.db_utils import create_db
from datetime import datetime

create_db()
conn = sqlite3.connect("database/students.db")
cursor = conn.cursor()

cursor.execute("SELECT id, name, embedding FROM students")
known = [
    (row[0], row[1], np.frombuffer(row[2], dtype=np.float32))
    for row in cursor.fetchall()
]

attendance_set = set()
cap = cv2.VideoCapture("/home/icebyte/Projects/Personal/Python/Computer_Vision/face-recognition/face_attendance/test02.mp4")
print("[INFO] Press 'q' to quit. Automatically marking attendance...")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (1280, 720))

    face, emb = get_face_embedding(frame)
    if emb is not None:
        matched = False
        for sid, name, k_emb in known:
            sim = cosine_similarity(emb, k_emb)
            if sim > 0.6 and sid not in attendance_set:
                attendance_set.add(sid)
                cursor.execute(
                    "INSERT INTO attendance (id, name) VALUES (?, ?)", (sid, name)
                )
                conn.commit()
                print(
                    f"[ATTENDANCE] {name} marked at {datetime.now().strftime('%H:%M:%S')}"
                )
                bbox = face.bbox.astype(int)
                # Improved visual display
                cv2.rectangle(
                    frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2
                )
                cv2.putText(
                    frame,
                    f"{name} - Present",
                    (bbox[0], bbox[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2,
                )
                matched = True
                break
        if not matched:
            cv2.putText(
                frame, "Unknown", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
            )

    cv2.imshow("Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
conn.close()
