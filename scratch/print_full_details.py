import json

with open('extracted_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('scratch/details.txt', 'w', encoding='utf-8') as out:
    out.write('========================================\n')
    out.write('           ALL SLIDES CONTENT           \n')
    out.write('========================================\n\n')
    for s in data['slides']:
        out.write(f"\n==================== SLIDE {s['slide_num']} ====================\n")
        for t in s['texts']:
            out.write(f"  {t}\n")
        if s['tables']:
            out.write(f"  [Tables]: {s['tables']}\n")
        if s['notes']:
            out.write(f"  [Notes]: {s['notes']}\n")

    out.write('\n\n========================================\n')
    out.write('           DOCX PARAGRAPHS             \n')
    out.write('========================================\n\n')
    for p in data['docx_paragraphs']:
        out.write(f"P{p['idx']} [{p['style']}]: {p['text']}\n")

    out.write('\n\n========================================\n')
    out.write('              DOCX TABLES              \n')
    out.write('========================================\n\n')
    for t in data['docx_tables']:
        out.write(f"\nTable {t['table_idx']}:\n")
        for r in t['rows']:
            out.write(f"  {r}\n")

print("Saved full details to scratch/details.txt")
