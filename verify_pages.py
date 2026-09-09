import os
import win32com.client
import pypdfium2

DOCX_PATH = r"C:\Users\Ram Sai\OneDrive\Documents\24A95A0503_T.Ram Sai_internship\ShieldJob_AI_Internship_Report_Formatted.docx"
PDF_PATH = r"C:\Users\Ram Sai\OneDrive\Documents\24A95A0503_T.Ram Sai_internship\ShieldJob_AI_Internship_Report_Formatted.pdf"
PREVIEWS_DIR = "page_previews"
os.makedirs(PREVIEWS_DIR, exist_ok=True)

print("Starting Word application...")
word = win32com.client.DispatchEx('Word.Application')
word.Visible = False

try:
    doc = word.Documents.Open(DOCX_PATH)
    # Save as PDF (Format type 17 = wdFormatPDF)
    doc.SaveAs(PDF_PATH, FileFormat=17)
    doc.Close()
    print("Exported PDF successfully:", PDF_PATH)
finally:
    word.Quit()

# Render pages to PNG
pdf = pypdfium2.PdfDocument(PDF_PATH)
print(f"Total Pages in Formatted Report: {len(pdf)}")

for i, page in enumerate(pdf):
    img = page.render(scale=150/72).to_pil()
    img_path = os.path.join(PREVIEWS_DIR, f"page_{i+1:02d}.png")
    img.save(img_path)
    print(f"Rendered Page {i+1:02d} -> {img_path}")

print("Verification render complete.")
