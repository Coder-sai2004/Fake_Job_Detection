import os
import sys
import pypdf

pdf_path = r'C:\Users\Ram Sai\Downloads\23A91A0558 Report .pdf'
reader = pypdf.PdfReader(pdf_path)
print(f"Total pages in friend's PDF: {len(reader.pages)}")

# Extract text of first 10 pages
for i in range(min(12, len(reader.pages))):
    print(f"\n{'='*30} PAGE {i+1} {'='*30}")
    txt = reader.pages[i].extract_text()
    print(txt)

# Also extract images from first 10 pages
scratch_dir = r'C:\Users\Ram Sai\OneDrive\Desktop\PROJECTS\Fake_Job_Detection\scratch'
os.makedirs(scratch_dir, exist_ok=True)

img_count = 0
for i in range(min(12, len(reader.pages))):
    page = reader.pages[i]
    for img_idx, img_obj in enumerate(page.images):
        img_name = f"friend_page_{i+1}_img_{img_idx}_{img_obj.name}"
        img_out = os.path.join(scratch_dir, img_name)
        with open(img_out, "wb") as fp:
            fp.write(img_obj.data)
        print(f"Extracted image: {img_out}")
        img_count += 1
print(f"Total images extracted from first 12 pages: {img_count}")
