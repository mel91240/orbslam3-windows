import cv2
from pathlib import Path

KEEP_EVERY = 2  # 2 = garder 1 frame sur 2, 3 = 1 sur 3, etc.
OUT_W = 960
OUT_H = 540
root = Path(r"C:\Users\melan\Desktop\SLAM_ROV")
video_path = root / "video_phone2.mp4"  # nouveau nom

dataset_root = Path(r"C:\Users\melan\Datasets\PhoneTest2")
cam0_data = dataset_root / "mav0" / "cam0" / "data"
cam0_data.mkdir(parents=True, exist_ok=True)

timestamps_file = root / "PhoneTest2_TimeStamps.txt"

cap = cv2.VideoCapture(str(video_path))
if not cap.isOpened():
    raise RuntimeError(f"Impossible d'ouvrir la vidéo: {video_path}")

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

if fps <= 0:
    fps = 30.0
dt = 1.0 / fps

print(f"Resolution: {width} x {height}")
print(f"FPS ~ {fps:.2f}, dt ~ {dt:.4f} s")

frame_idx = 0
timestamp_ns = 0

with open(timestamps_file, "w", newline="\n") as f_ts:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % KEEP_EVERY != 0:
            frame_idx += 1
            timestamp_ns += int(dt * 1e9)
            continue

        stamp_str = f"{timestamp_ns:019d}"
        out_path = cam0_data / f"{stamp_str}.png"

        frame_small = cv2.resize(frame, (OUT_W, OUT_H), interpolation=cv2.INTER_AREA)
        cv2.imwrite(str(out_path), frame_small)
        f_ts.write(f"{stamp_str}\n")

        frame_idx += 1
        timestamp_ns += int(dt * 1e9)

cap.release()
print(f"Frames extraites: {frame_idx}")
print(f"Timestamps écrits dans: {timestamps_file}")