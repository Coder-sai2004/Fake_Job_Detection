import docx

doc_f = docx.Document(r'C:\Users\Ram Sai\OneDrive\Documents\24A95A0503_T.Ram Sai_internship\INTERNSHIP REPORT.docx')
doc_u = docx.Document(r'C:\Users\Ram Sai\OneDrive\Documents\24A95A0503_T.Ram Sai_internship\ShieldJob_AI_Internship_Report.docx')

print("==================== FRIEND PRELIMINARY (P0 to P95) ====================")
for i in range(min(96, len(doc_f.paragraphs))):
    p = doc_f.paragraphs[i]
    if p.text.strip():
        print(f"[{i:02d}] {p.text.strip()}")

print("\n==================== USER PRELIMINARY (P0 to P45) ====================")
for i in range(min(45, len(doc_u.paragraphs))):
    p = doc_u.paragraphs[i]
    if p.text.strip():
        print(f"[{i:02d}] {p.text.strip()}")
