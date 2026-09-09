import json

with open('extracted_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('=== ALL SLIDES ===')
for s in data['slides']:
    print(f"\n==================== SLIDE {s['slide_num']} ====================")
    for t in s['texts']:
        print(f"  {t}")
    if s['tables']:
        print(f"  [Tables]: {s['tables']}")
    if s['notes']:
        print(f"  [Notes]: {s['notes']}")

print('\n=== DOCX CONTENT ===')
for p in data['docx_paragraphs']:
    print(f"P{p['idx']} [{p['style']}]: {p['text']}")

print('\n=== DOCX TABLES ===')
for t in data['docx_tables']:
    print(f"\nTable {t['table_idx']}:")
    for r in t['rows']:
        print(f"  {r}")
