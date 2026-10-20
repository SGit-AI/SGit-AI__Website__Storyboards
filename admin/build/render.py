#!/usr/bin/env python3
"""Draws each storyboard's thumb.jpg (the cover, 480 wide) and og.jpg (1200 wide, the link preview) into www/, with the
API's own tools/render.mjs: the pinned release of the kit, in headless Chromium, from the same bundle.json the page
serves. The images are committed, not built (a font renders differently from one machine to the next, and the build
must be the same bytes twice); admin/build/renders.json records the bundle and the kit each was drawn from, and
build.py refuses a stale one.

    python3 admin/build/render.py            # only what is stale
    python3 admin/build/render.py --all      # everything

Needs node, Playwright's Chromium, and the API checkout ($STORYBOARDS_API, default ../SGit-AI__Website__Storyboards__API).
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402


def main():
    renders = json.loads(B.RENDERS.read_text(encoding="utf-8")) if B.RENDERS.exists() else {"what": "", "boards": {}}
    renders["what"] = ("What each committed thumb.jpg and og.jpg was drawn from: the sha256 of the storyboard's bundle.json and the API release. "
                       "Written by admin/build/render.py; build.py refuses a storyboard whose images are stale.")
    api = B.api_checkout()
    if not (api / B.API["path"]).exists():
        sys.exit(f"render: {api / B.API['path']} does not exist; set STORYBOARDS_API to an API checkout that has the pinned release")
    for rel in B.API["files"]:
        B.api_bytes(rel)  # the checkout's bytes are the pinned bytes, or this stops
    jobs, stamps = [], {}
    with tempfile.TemporaryDirectory() as tmp:
        for s in B.load_series():
            for b in s["boards"]:
                key = f"{s['meta']['slug']}/{b['sb']['slug']}"
                data = B.bundle_of(s["meta"], s["cast"], b["sb"])
                stamp = hashlib.sha256(data).hexdigest()
                r = renders["boards"].get(key, {})
                out = B.OUT / key
                if "--all" not in sys.argv and r.get("bundle_sha256") == stamp and r.get("api") == B.API["release"] and all((out / n).exists() for n in B.RENDERED):
                    continue
                path = Path(tmp) / (key.replace("/", "__") + ".json")
                path.write_bytes(data)
                jobs.append({"bundle": str(path), "out": str(out), "make": ["thumb", "og"]})
                stamps[key] = stamp
        if not jobs:
            print("render: every image is fresh")
            return
        jf = Path(tmp) / "jobs.json"
        jf.write_text(json.dumps(jobs), encoding="utf-8")
        env = dict(os.environ, SB_RELEASE=B.API["path"])
        subprocess.run(["node", str(api / "tools/render.mjs"), str(jf)], check=True, env=env)
    for key, stamp in stamps.items():
        renders["boards"][key] = {"bundle_sha256": stamp, "api": B.API["release"]}
    renders["boards"] = dict(sorted(renders["boards"].items()))
    B.RENDERS.write_text(json.dumps(renders, indent=1) + "\n", encoding="utf-8")
    print(f"render: drew {len(stamps)} storyboard(s)")


if __name__ == "__main__":
    main()
