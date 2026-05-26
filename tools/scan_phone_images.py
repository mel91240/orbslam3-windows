import os
import cv2

root = r"C:\Users\melan\Datasets\PhoneTest2\mav0\cam0\data"

files = sorted(f for f in os.listdir(root) if f.lower().endswith(".png"))
print("Nb de fichiers:", len(files))

for i, name in enumerate(files):
    path = os.path.join(root, name)
    im = cv2.imread(path)
    if im is None:
        print("FAIL imread:", i, path)
        break
else:
    print("Done scan, no failures")