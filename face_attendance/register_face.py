# register_face.py
import os
import cv2
import sqlite3

# import numpy as np  # Unused import removed
from utils.face_utils import get_face_embedding
from utils.db_utils import create_db, get_db_path

create_db()
conn = sqlite3.connect(get_db_path())
cursor = conn.cursor()

script_dir = os.path.dirname(os.path.abspath(__file__))
video_path = os.path.join(script_dir, "test02.mp4")
cap = cv2.VideoCapture(video_path)

# cv2.namedWindow("Register Face", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("Register Face", 1920, 1080)
# cv2.moveWindow("Register Face", 0, 0)

print("[INFO] Press 's' to register, 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1920, 1080))

    face, embedding = get_face_embedding(frame)
    if face is not None:
        bbox = face.bbox.astype(int)
        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
        cv2.putText(
            frame,
            "Face Detected",
            (bbox[0], bbox[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

    cv2.imshow("Register Face", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("s") and embedding is not None:
        name = input("Enter name: ")
        student_id = input("Enter ID: ")
        cursor.execute(
            "INSERT OR REPLACE INTO students (id, name, embedding) VALUES (?, ?, ?)",
        )
        conn.commit()
        print(f"[INFO] {name} registered.")
    elif key == ord("q"):
        break
print("helloh dsvihibb weihvwivb ehehehehhehehehehehehehehehehehehhe")
cap.release()
cv2.destroyAllWindows()
conn.close()
