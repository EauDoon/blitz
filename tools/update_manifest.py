#!/usr/bin/env python3
"""Refresh only the candidate payload inventory after reviewed source edits."""
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / 'Blitz'
sys.path.insert(0, str(KIT / 'setup'))
from build_context import inventory
from verify_archive import validate_manifest


def main():
    files = inventory(KIT)
    manifest = json.loads(files.pop('manifest.json'))
    rows = []
    for name, data in sorted(files.items()):
        row = {'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        try:
            row['characters'] = len(data.decode('utf-8'))
        except UnicodeDecodeError:
            row['characters'] = None
        rows.append(row)
    manifest['files'] = rows
    manifest['licenses'] = sorted(name for name in files if Path(name).name.lower() in
        {'license', 'license.txt', 'license.md', 'notice', 'notice.md', 'third_party_licenses.md'})
    validate_manifest(manifest)
    data = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    (KIT / 'manifest.json').write_bytes(data)
    print(json.dumps({'result': 'inventory_updated', 'files': len(rows),
                      'manifest_sha256': hashlib.sha256(data).hexdigest()}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
