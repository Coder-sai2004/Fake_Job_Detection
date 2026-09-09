import pypdf
import os

PDF_PATH = r"C:\Users\Ram Sai\OneDrive\Documents\24A95A0503_T.Ram Sai_internship\ShieldJob_AI_Internship_Report_Formatted.pdf"
reader = pypdf.PdfReader(PDF_PATH)

print(f"Total Pages: {len(reader.pages)}")

sections_to_find = [
    "Abstract", "SDG Mapping", "Introduction", "Objectives", "Methodology",
    "Implementation", "Results and Discussion", "Key Learnings", "Conclusion and Future Scope",
    "Outcomes", "Publication and Product Development", "About the Organization", "References"
]

page_mapping = {}

for idx, page in enumerate(reader.pages):
    text = page.extract_text()
    print(f"--- Page {idx+1} ({len(text)} chars) ---")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    first_lines = " | ".join(lines[:3]) if lines else "EMPTY / IMAGE"
    print(f"  Header/Start: {first_lines[:100]}")
    for sec in sections_to_find:
        if sec.lower() in text.lower() and sec not in page_mapping:
            # Check if it looks like heading
            for line in lines[:5]:
                if sec.lower() in line.lower():
                    page_mapping[sec] = idx + 1
                    break

print("\n=== DETECTED PAGE MAPPING ===")
for k, v in page_mapping.items():
    print(f"{k}: Page {v}")
