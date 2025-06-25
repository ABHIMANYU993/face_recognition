import cv2
import mediapipe as mp
import time

url = "https://phone:833993@192.168.31.42:8080/video"
url2 = "https://phone:833993@100.122.3.51:8080/video"
rtsp_url = "rtsp://phone:833993@192.168.31.42:8080/h264_ulaw.sdp"
#

cap = cv2.VideoCapture(0)


while True:
    success, frame = cap.read()
    if not success:
        break

    # Resize to 1920x1080 using high-quality interpolation
    resized_frame = cv2.resize(frame, (1920, 1080), interpolation=cv2.INTER_AREA)

    cv2.imshow("4K Camera Downscaled to 1080p", resized_frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break


cap.release()
cv2.destroyAllWindows()
