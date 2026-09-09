import os
from PIL import Image

scratch_dir = r'C:\Users\Ram Sai\OneDrive\Desktop\PROJECTS\Fake_Job_Detection\scratch'
for fname in sorted(os.listdir(scratch_dir)):
    if fname.startswith("friend_page_"):
        fpath = os.path.join(scratch_dir, fname)
        im = Image.open(fpath)
        print(f"{fname}: size={im.size}, mode={im.mode}")
