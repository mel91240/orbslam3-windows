from pathlib import Path
import cv2

KEEP_EVERY = 2
OUT_W = 752
OUT_H = 480

src_dataset = Path(r"C:\Users\melan\Datasets\EuRoc\MH01")
src_cam0 = src_dataset / "mav0" / "cam0" / "data"
src_timestamps = Path(
    r"C:\Users\melan\Desktop\SLAM_ROV\orbslam3-windows\Examples\Monocular\EuRoC_TimeStamps\MH01.txt"
)

dst_dataset = Path(r"C:\Users\melan\Datasets\MH01_phone_style")
dst_cam0 = dst_dataset / "mav0" / "cam0" / "data"
dst_cam0.mkdir(parents=True, exist_ok=True)

dst_timestamps = Path(r"C:\Users\melan\Desktop\SLAM_ROV\MH01_phone_style_TimeStamps.txt")

with open(src_timestamps, "r", newline="\n") as f:
    src_stamps = [line.strip() for line in f if line.strip()]

print(f"Nombre timestamps source: {len(src_stamps)}")

kept = 0
with open(dst_timestamps, "w", newline="\n") as f_out:
    for idx, stamp in enumerate(src_stamps):
        if idx % KEEP_EVERY != 0:
            continue

        src_img = src_cam0 / f"{stamp}.png"
        if not src_img.exists():
            print(f"Image manquante: {src_img}")
            continue

        im = cv2.imread(str(src_img), cv2.IMREAD_UNCHANGED)
        if im is None:
            print(f"Image illisible: {src_img}")
            continue

        if (im.shape[1], im.shape[0]) != (OUT_W, OUT_H):
            im = cv2.resize(im, (OUT_W, OUT_H), interpolation=cv2.INTER_AREA)

        dst_img = dst_cam0 / f"{stamp}.png"
        cv2.imwrite(str(dst_img), im)
        f_out.write(stamp + "\n")
        kept += 1

print(f"Frames gardées: {kept}")
print(f"Dataset créé dans: {dst_dataset}")
print(f"Timestamps écrits dans: {dst_timestamps}")