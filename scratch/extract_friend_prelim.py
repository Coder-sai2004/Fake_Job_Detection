import os
import sys
import pypdf

pdf_path = r'C:\Users\Ram Sai\Downloads\23A91A0558 Report .pdf'
reader = pypdf.PdfReader(pdf_path)

with open(r'C:\Users\Ram Sai\OneDrive\Desktop\PROJECTS\Fake_Job_Detection\scratch\friend_prelim_pages.txt', 'w', encoding='utf-8') as f:
    for i in range(14):
        f.write(f"\n{'='*40} PAGE {i+1} {'='*40}\n")
        txt = reader.pages[i].extract_text()
        f.write(txt + "\n")
        f.write(f"\n--- Images on page {i+1} ---\n")
        for img in reader.pages[i].images:
            f.write(f"Image name: {img.name}\n")

print("Wrote friend prelim pages to scratch/friend_prelim_pages.txt")
