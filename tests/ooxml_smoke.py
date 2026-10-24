#!/usr/bin/env python3
import sys
import zipfile
from pathlib import Path

OOXML_CORE = "[Content_Types].xml"

def check(path: Path) -> int:
    print(f"
{path}")
    if not path.exists():
        print("  ERROR: missing")
        return 1
    try:
        with zipfile.ZipFile(path) as z:
            names = set(z.namelist())
            if OOXML_CORE not in names:
                print("  ERROR: not a valid OOXML package")
                return 1
            macro = any(n.lower().endswith("vbaproject.bin") for n in names)
            workbook = "xl/workbook.xml" in names
            print(f"  OOXML package: yes")
            print(f"  Spreadsheet workbook: {'yes' if workbook else 'no'}")
            print(f"  VBA project present: {'yes' if macro else 'no'}")
            print(f"  ZIP members: {len(names)}")
            return 0
    except zipfile.BadZipFile:
        print("  ERROR: invalid ZIP container")
        return 1

def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print("usage: ooxml_smoke.py FILE.xlsx [FILE.xlsm ...]", file=sys.stderr)
        return 2
    return max(check(Path(p)) for p in argv)


if __name__ == "__main__":
    raise SystemExit(main())
