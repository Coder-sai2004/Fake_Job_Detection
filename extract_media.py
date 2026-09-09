import docx
import os

friend_path = r'C:\Users\Ram Sai\OneDrive\Documents\24A95A0503_T.Ram Sai_internship\INTERNSHIP REPORT.docx'
user_path = r'C:\Users\Ram Sai\OneDrive\Documents\24A95A0503_T.Ram Sai_internship\ShieldJob_AI_Internship_Report.docx'

doc_f = docx.Document(friend_path)
doc_u = docx.Document(user_path)

os.makedirs('extracted_media/friend', exist_ok=True)
os.makedirs('extracted_media/user', exist_ok=True)

for rel in doc_f.part.rels.values():
    if 'image' in rel.target_ref:
        img_part = rel.target_part
        fname = os.path.basename(rel.target_ref)
        with open(os.path.join('extracted_media/friend', fname), 'wb') as f:
            f.write(img_part.blob)
        print(f"Friend image extracted: {fname}, size={len(img_part.blob)} bytes")

for rel in doc_u.part.rels.values():
    if 'image' in rel.target_ref:
        img_part = rel.target_part
        fname = os.path.basename(rel.target_ref)
        with open(os.path.join('extracted_media/user', fname), 'wb') as f:
            f.write(img_part.blob)
        print(f"User image extracted: {fname}, size={len(img_part.blob)} bytes")
