import sys
import os
import json
import traceback
from datetime import datetime, UTC
from pathlib import Path

from bignews.util import fetch_rss, SOURCES

DATA_DIR = Path('data/articles')


def main():
    source = sys.argv[1]
    entries = fetch_rss(SOURCES[source])
    print(f'#entries: {len(entries)}')

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(UTC).strftime('%Y-%m-%d')
    filepath = DATA_DIR / f'{today}.jsonl'

    # Load existing IDs for dedup
    existing_ids = set()
    if filepath.exists():
        with open(filepath, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    existing_ids.add(json.loads(line)['_id'])

    # Write new entries
    new_count = 0
    with open(filepath, 'a', encoding='utf-8') as f:
        for entry in entries:
            if entry['_id'] not in existing_ids:
                # Convert datetime to ISO string for JSON serialization
                entry['fetched_at'] = entry['fetched_at'].isoformat()
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
                new_count += 1

    print(f"insert: {new_count}, skipped: {len(entries) - new_count}")


if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc()
