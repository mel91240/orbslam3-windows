import cv2
from pathlib import Path

video_path = Path(r"C:\Users\melan\Desktop\SLAM_ROV\calib_chess.mp4")
pattern_size = (7, 10)  # on ajustera ensuite

cap = cv2.VideoCapture(str(video_path))
if not cap.isOpened():
    raise RuntimeError("Impossible d'ouvrir la vidéo")

ret, frame = cap.read()
cap.release()

if not ret:
    raise RuntimeError("Impossible de lire la première frame")

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
found, corners = cv2.findChessboardCorners(gray, pattern_size, None)

print(f"pattern_size = {pattern_size}, found = {found}, nb corners = {0 if corners is None else len(corners)}")
print(f"frame shape: {gray.shape[1]} x {gray.shape[0]}")

cv2.imwrite(str(Path(r"C:\Users\melan\Desktop\SLAM_ROV\calib_frame0.png")), frame)
print("Frame sauvegardée sous calib_frame0.png")