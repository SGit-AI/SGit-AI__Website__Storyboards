#!/usr/bin/env python3
"""Bring a site's storyboards here, byte for byte, and record where they came from.

    python3 admin/build/import_series.py gen-z-developers PATH/TO/SGit-AI__Website__Gen-Z-Developers
    python3 admin/build/import_series.py pki PATH/TO/SGit-AI__Website__PKI

Copies admin/content/storyboards/cast.json and every NN__<slug>.json from the clone into content/series/<series>/
unchanged (the storyboard is the origin site's file; a correction goes there, or is made here and the origin told), and
writes the origin's commit into content/series/<series>/series.json. Everything this site adds about a series (its title,
blurb, shelves, how its cast stands on the shelf) lives in series.json, never in the storyboards themselves. Run it again
to take a newer commit: the storyboards are replaced, series.json keeps what this site wrote and moves the commit.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ORIGINS = {
    "gen-z-developers": {"site": "https://gen-z-developers.sgit.ai", "repo": "SGit-AI/SGit-AI__Website__Gen-Z-Developers"},
    "pki": {"site": "https://pki.sgit.ai", "repo": "SGit-AI/SGit-AI__Website__PKI"},
}


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ORIGINS:
        sys.exit(__doc__)
    series, clone = sys.argv[1], Path(sys.argv[2]).resolve()
    src = clone / "admin/content/storyboards"
    commit = subprocess.check_output(["git", "-C", str(clone), "rev-parse", "HEAD"], text=True).strip()
    date = subprocess.check_output(["git", "-C", str(clone), "log", "-1", "--format=%cs"], text=True).strip()
    out = ROOT / "content/series" / series
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("[0-9][0-9]__*.json"):
        old.unlink()
    files = sorted(src.glob("[0-9][0-9]__*.json"))
    for f in files + [src / "cast.json"]:
        shutil.copyfile(f, out / f.name)
    meta_path = out / "series.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {"slug": series}
    meta["origin"] = dict(ORIGINS[series], commit=commit, date=date, path="admin/content/storyboards/",
                          imported=[f.name for f in files] + ["cast.json"])
    meta_path.write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"import_series: {len(files)} storyboards and the cast from {ORIGINS[series]['repo']} at {commit[:8]} ({date}) -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
