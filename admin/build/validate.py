#!/usr/bin/env python3
"""The gate: www/ holds together, or the release stops. Run after build.py, before every push; CI runs it on every commit.

    python3 admin/build/validate.py

Checks, each of which a sibling site's gate has caught a real defect with (sgit.ai/docs/guidance/repositories.html, section 4):
  1. one version everywhere: every page's site-version, the badge, llms.txt and the newest row of content/versions.json
  2. every internal link and asset resolves to a file in www/ (query and fragment stripped; absolute links to this host too)
  3. every page has its markdown twin, and the sitemap lists exactly the pages (404 aside)
  4. every file loaded from api.storyboards.sgit.ai is on the pinned path, is in the pinned manifest, and carries its integrity
  5. canonical and og:url name this host
  6. no key shapes anywhere in www/ or content/ (sgit vault keys, private key blocks, cloud and provider API keys)
  7. no em-dashes in this site's own prose (content/articles, content/pages, the agent-written part of briefs/)
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
WWW = ROOT / "www"
HOST = "storyboards.sgit.ai"
API = json.loads((ROOT / "admin/build/api.json").read_text(encoding="utf-8"))
API_BASE = f"{API['host']}/{API['path']}/"
V = json.loads((ROOT / "content/versions.json").read_text(encoding="utf-8"))["releases"][0]["version"]
KEYS = [re.compile(p) for p in (r"sgit_private_\S+", r"-----BEGIN [A-Z ]*PRIVATE KEY-----", r"\bAKIA[0-9A-Z]{16}\b", r"\bsk-(?:or-|ant-)?[A-Za-z0-9_-]{24,}",
                                r"\bghp_[A-Za-z0-9]{30,}", r"\bxox[bap]-[A-Za-z0-9-]{20,}")]
errors = []


def err(m):
    errors.append(m)


pages = sorted(p for p in WWW.rglob("*.html"))
if not pages:
    sys.exit("validate: www/ has no pages; run admin/build/build.py")
for p in pages:
    rel = p.relative_to(WWW).as_posix()
    t = p.read_text(encoding="utf-8")
    # 1. the version
    m = re.search(r'<meta name="site-version" content="([^"]+)">', t)
    if not m or m.group(1) != V:
        err(f"{rel}: site-version is {m.group(1) if m else 'missing'}, the site is {V}")
    b = re.search(r'<span class="ver">site <a [^>]*>(v[\d.]+)</a></span>', t)
    if not b or b.group(1) != V:
        err(f"{rel}: the version badge is {b.group(1) if b else 'missing'}, the site is {V}")
    # 2. links
    for attr, url in re.findall(r'\b(href|src)="([^"]+)"', t):
        u = urlparse(url)
        if u.scheme in ("mailto", "data", "javascript"):
            continue
        if u.scheme in ("http", "https"):
            if u.netloc != HOST:
                continue
            target = WWW / u.path.lstrip("/")
        elif url.startswith("#") or not u.path:
            continue
        elif u.path.startswith("/"):
            target = WWW / u.path.lstrip("/")
        else:
            target = (p.parent / u.path)
        if target.is_dir() or u.path.endswith("/"):
            target = target / "index.html"
        if not target.resolve().exists():
            err(f"{rel}: {attr}={url} does not resolve")
    # 3. the twin
    tw = re.search(r'<link rel="alternate" type="text/markdown" href="([^"]+)">', t)
    if rel != "404.html" and (not tw or not (p.parent / tw.group(1)).exists()):
        err(f"{rel}: no markdown twin")
    # 4. the API
    for tag in re.findall(r'<(?:script|link)\b[^>]*api\.storyboards\.sgit\.ai[^>]*>', t):
        url = re.search(r'(?:src|href)="([^"]+)"', tag).group(1)
        if not url.startswith(API_BASE):
            err(f"{rel}: loads {url}, not from the pinned release {API_BASE}")
            continue
        f = url[len(API_BASE):]
        if f not in API["files"]:
            err(f"{rel}: loads {f}, which is not in the pinned release's manifest")
        elif f'integrity="{API["files"][f]["integrity"]}"' not in tag or 'crossorigin="anonymous"' not in tag:
            err(f"{rel}: loads {f} without its integrity string and crossorigin")
    # 5. canonical
    for prop in re.findall(r'<link rel="canonical" href="([^"]+)">|<meta property="og:url" content="([^"]+)">', t):
        u = prop[0] or prop[1]
        if urlparse(u).netloc != HOST:
            err(f"{rel}: canonical or og:url {u} is not on {HOST}")

sm = (WWW / "sitemap.xml").read_text(encoding="utf-8")
listed = {u.replace(f"https://{HOST}/", "") for u in re.findall(r"<loc>([^<]+)</loc>", sm)}
listed = {(u + "index.html") if (u == "" or u.endswith("/")) else u for u in listed}
have = {p.relative_to(WWW).as_posix() for p in pages} - {"404.html"}
for x in sorted(have - listed):
    err(f"sitemap.xml: {x} is missing")
for x in sorted(listed - have):
    err(f"sitemap.xml: lists {x}, which is not a page")
llms = (WWW / "llms.txt").read_text(encoding="utf-8")
if f"Site {V}." not in llms:
    err(f"llms.txt does not say Site {V}.")

# 6. keys
for base in (WWW, ROOT / "content", ROOT / "briefs", ROOT / "admin"):
    for p in base.rglob("*"):
        if p.is_file() and p != Path(__file__).resolve() and p.suffix in (".html", ".md", ".json", ".txt", ".js", ".css", ".py", ".xml", ".mjs"):
            text = p.read_text(encoding="utf-8", errors="replace")
            for k in KEYS:
                if k.search(text):
                    err(f"{p.relative_to(ROOT)}: matches the key shape {k.pattern}")

# 7. em-dashes in our own prose (the imported storyboards and the transcript are other people's words, and stay as written)
for p in list((ROOT / "content/articles").glob("*.md")) + list((ROOT / "content/pages").rglob("*.md")):
    if "—" in p.read_text(encoding="utf-8"):
        err(f"{p.relative_to(ROOT)}: an em-dash in prose")
for p in (ROOT / "briefs").glob("*.md"):
    t = p.read_text(encoding="utf-8")
    if "—" in t.split("## Part 2", 1)[-1]:
        err(f"{p.relative_to(ROOT)}: an em-dash in the agent-written part")

if errors:
    print("\n".join("validate: " + e for e in errors[:80]))
    sys.exit(f"validate: {len(errors)} problem(s)")
print(f"validate: {len(pages)} pages, site {V}, kit {API['release']}: links, twins, sitemap, the pinned API, canonicals, key shapes and prose all hold")
