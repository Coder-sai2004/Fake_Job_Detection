import os
import pypdf

cert_pdf = r'C:\Users\Ram Sai\OneDrive\Documents\24A95A0503_T.Ram Sai_internship\Tanuku_Ram_Sai_certificate.pdf'
if not os.path.exists(cert_pdf):
    cert_pdf = r'C:\Users\Ram Sai\OneDrive\Documents\24A95A0503_T.Ram Sai_internship\Internship_Certificate_2026.pdf'

scratch_dir = r'C:\Users\Ram Sai\OneDrive\Desktop\PROJECTS\Fake_Job_Detection\scratch'

if os.path.exists(cert_pdf):
    reader = pypdf.PdfReader(cert_pdf)
    print(f"Reading {cert_pdf} ({len(reader.pages)} pages)...")
    for p_idx, page in enumerate(reader.pages):
        for img_idx, img in enumerate(page.images):
            out_name = os.path.join(scratch_dir, f"user_cert_img_{p_idx}_{img_idx}.png")
            with open(out_name, "wb") as fp:
                fp.write(img.data)
            print(f"Extracted user certificate image to: {out_name}")
else:
    print("Cert PDF not found")
