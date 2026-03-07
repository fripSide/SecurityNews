import json
import os
import sys
from datetime import datetime, UTC, timedelta
from pathlib import Path

from jinja2 import Template
from weasyprint import HTML

NEWSPAPERS_DIR = Path('data/newspapers')


def main():
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 7

    since_date = (datetime.now(UTC) - timedelta(days=days)).strftime('%Y-%m-%d')

    if not NEWSPAPERS_DIR.exists():
        print("No newspapers directory found. Skipping PDF generation.")
        sys.exit(0)

    # Load newspaper files from the past N days
    docs = []
    for filepath in sorted(NEWSPAPERS_DIR.glob('*.json')):
        if filepath.stem >= since_date:
            with open(filepath, encoding='utf-8') as f:
                docs.append(json.load(f))

    if not docs:
        print("No newspapers found in the past week. Skipping PDF generation.")
        sys.exit(0)

    # Collect all articles across all newspaper documents
    all_bleeping = []
    all_cs_cr = []
    all_cs_ai = []
    seen_ids = set()

    for doc in docs:
        articles = doc.get('articles', {})
        for item in articles.get('bleepingcomputer', []):
            if item['_id'] not in seen_ids:
                seen_ids.add(item['_id'])
                all_bleeping.append(item)
        for item in articles.get('arxiv_cs_cr', []):
            if item['_id'] not in seen_ids:
                seen_ids.add(item['_id'])
                all_cs_cr.append(item)
        for item in articles.get('arxiv_cs_ai', []):
            if item['_id'] not in seen_ids:
                seen_ids.add(item['_id'])
                all_cs_ai.append(item)

    # Date range from filenames
    start_date = docs[0]['generated_at'][:10]
    end_date = docs[-1]['generated_at'][:10]
    date_range = f"{start_date} ~ {end_date}"

    print(f"Date range: {date_range}")
    print(f"Articles: bleepingcomputer={len(all_bleeping)}, cs.cr={len(all_cs_cr)}, cs.ai={len(all_cs_ai)}")

    # Render HTML
    with open('bignews/prompt/newspaper.html.j2', encoding='utf-8') as f:
        template = Template(f.read())

    html_content = template.render(
        date_range=date_range,
        sections={
            'bleepingcomputer': all_bleeping,
            'arxiv_cs_cr': all_cs_cr,
            'arxiv_cs_ai': all_cs_ai,
        },
        generated_at=datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC'),
    )

    # Generate PDF
    os.makedirs('output', exist_ok=True)
    filename = f"SecurityNews_{start_date}_to_{end_date}.pdf"
    output_path = os.path.join('output', filename)

    HTML(string=html_content).write_pdf(output_path)
    print(f"PDF generated: {output_path}")


if __name__ == '__main__':
    main()
