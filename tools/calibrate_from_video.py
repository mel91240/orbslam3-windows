import cv2
import numpy as np
from pathlib import Path

video_path = Path(r"C:\Users\melan\Desktop\SLAM_ROV\calib_chess.mp4")

pattern_size = (7, 10)   # nombre de coins intérieurs
square_size = 0.021      # 2.1 cm = 0.021 m

cap = cv2.VideoCapture(str(video_path))
if not cap.isOpened():
    raise RuntimeError(f"Impossible d'ouvrir la vidéo: {video_path}")

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"Resolution: {width} x {height}")
print(f"FPS: {fps:.2f}")

objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)
objp *= square_size

objpoints = []
imgpoints = []

frame_id = 0
used = 0
step = 10  # prend 1 frame sur 10

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_id % step != 0:
        frame_id += 1
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    found, corners = cv2.findChessboardCorners(gray, pattern_size, None)

    if found:
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        objpoints.append(objp)
        imgpoints.append(corners2)
        used += 1
        print(f"checkerboard detecté sur frame {frame_id}")

    frame_id += 1

cap.release()

print(f"\nFrames utilisées pour la calibration: {used}")

if used < 8:
    raise RuntimeError("Pas assez de détections fiables pour calibrer. Il en faut idéalement au moins 8-10.")

ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, (width, height), None, None)

print("\n=== RESULTATS CALIBRATION ===")
print(f"RMS reprojection error: {ret}")
print("Camera matrix K:")
print(K)
print("Distortion coefficients:")
print(dist.ravel())

fx = K[0, 0]
fy = K[1, 1]
cx = K[0, 2]
cy = K[1, 2]

d = dist.ravel()
k1 = d[0] if len(d) > 0 else 0.0
k2 = d[1] if len(d) > 1 else 0.0
p1 = d[2] if len(d) > 2 else 0.0
p2 = d[3] if len(d) > 3 else 0.0
k3 = d[4] if len(d) > 4 else 0.0

print("\n=== PARAMETRES ORB-SLAM3 ===")
print(f"Camera.fx: {fx}")
print(f"Camera.fy: {fy}")
print(f"Camera.cx: {cx}")
print(f"Camera.cy: {cy}")
print(f"Camera.k1: {k1}")
print(f"Camera.k2: {k2}")
print(f"Camera.p1: {p1}")
print(f"Camera.p2: {p2}")
print(f"Camera.k3: {k3}")
print(f"Camera.width: {width}")
print(f"Camera.height: {height}")
print(f"Camera.fps: {fps if fps > 0 else 30.0}")