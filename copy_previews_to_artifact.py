import os
import shutil

ARTIFACT_DIR = r"C:\Users\Ram Sai\.gemini\antigravity-ide\brain\79879b1f-23d7-4ac0-a104-bc2a1d8ccb29"
PREVIEWS_DIR = "page_previews"

preview_pages = [
    ("page_01.png", "preview_cover.png"),
    ("page_02.png", "preview_college_cert.png"),
    ("page_04.png", "preview_internship_cert.png"),
    ("page_06.png", "preview_index.png"),
    ("page_07.png", "preview_abstract.png"),
    ("page_08.png", "preview_sdg.png"),
    ("page_13.png", "preview_implementation.png"),
    ("page_18.png", "preview_results.png"),
]

for src, dst in preview_pages:
    src_path = os.path.join(PREVIEWS_DIR, src)
    dst_path = os.path.join(ARTIFACT_DIR, dst)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        print(f"Copied {src} -> {dst_path}")

print("Previews copied to artifact directory.")
