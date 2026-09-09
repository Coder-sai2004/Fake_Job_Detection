import docx

doc_friend = docx.Document(r'C:\Users\Ram Sai\OneDrive\Documents\24A95A0503_T.Ram Sai_internship\INTERNSHIP REPORT.docx')
for i, s in enumerate(doc_friend.sections):
    print(f"Section {i} footer xml:")
    for f_p in s.footer.paragraphs:
        print("  p text:", f_p.text)
        print("  p xml:", f_p._p.xml[:300])
