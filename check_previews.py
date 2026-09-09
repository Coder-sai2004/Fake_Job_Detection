import os
from PIL import Image

PREVIEWS_DIR = "page_previews"
for i in range(1, 27):
    p = os.path.join(PREVIEWS_DIR, f"page_{i:02d}.png")
    if os.path.exists(p):
        im = Image.open(p)
        print(f"Page {i:02d}: size={im.size}")
