import cv2
import time

video_path = r"C:\Users\melan\Desktop\SLAM_ROV\video.mp4"  

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Impossible d'ouvrir la vidéo")
    exit(1)

frame_count = 0
t0 = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Simule un travail typique SLAM (conversion gris + pyramide)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pyr = cv2.pyrDown(gray)

    frame_count += 1

t1 = time.time()
cap.release()

elapsed = t1 - t0
fps = frame_count / elapsed if elapsed > 0 else 0.0

print(f"Frames traitées : {frame_count}")
print(f"Temps total    : {elapsed:.3f} s")
print(f"FPS moyen      : {fps:.2f}")