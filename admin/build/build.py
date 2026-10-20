#!/usr/bin/env python3
"""Builds storyboards.sgit.ai into www/ from content/, drawing nothing: every panel is drawn in the reader's browser by
the storyboard kit, loaded from the release of api.storyboards.sgit.ai pinned in admin/build/api.json.

    python3 admin/build/build.py              # write www/
    python3 admin/build/build.py --check      # build into a temporary folder and fail if www/ differs (CI)
    python3 admin/build/build.py --pin DIR    # pin the API release that DIR (an API checkout) names as current

What it reads: content/series/<series>/ (series.json, cast.json, NN__<slug>.json: the storyboards, byte for byte as
the origin site wrote them), content/articles/*.md, content/pages/*.md, content/versions.json (the newest row is the
site's version) and briefs/. What it writes, per storyboard, at /<series>/<slug>/: the page (deck, grid, script), its
markdown twin (index.md, the script), storyboard.json (the data, unchanged), bundle.json (the data with its cast, for
an embed), graph.json (the storyboard as a semantic graph). thumb.jpg and og.jpg are drawn by admin/build/render.py
and committed; this build checks they are fresh. The markdown and the graph come from the API's own formats.js, run by
node, so this site and a reader's browser make the same bytes from the same data.

The API's files are found in the checkout named by $STORYBOARDS_API (default ../SGit-AI__Website__Storyboards__API) or
fetched from the live host, and every byte is checked against the pinned hash either way.
"""
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md import front_matter, render as md_render  # noqa: E402
import abp as ABP  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
HOST = "storyboards.sgit.ai"
SITE = f"https://{HOST}"
REPO = "https://github.com/SGit-AI/SGit-AI__Website__Storyboards"
API_REPO = "https://github.com/SGit-AI/SGit-AI__Website__Storyboards__API"
CONTENT = ROOT / "content"
OUT = ROOT / "www"
PIN_FILE = ROOT / "admin/build/api.json"
RENDERS = ROOT / "admin/build/renders.json"
RENDERED = ("thumb.jpg", "og.jpg")
esc = lambda s: html.escape(str(s if s is not None else ""), quote=True)


def die(msg):
    sys.exit(f"build: {msg}")


# ------------------------------------------------------------------ the pinned API release
def api_checkout():
    return Path(os.environ.get("STORYBOARDS_API") or ROOT.parent / "SGit-AI__Website__Storyboards__API")


def pin(api_dir):
    api_dir = Path(api_dir)
    v = json.loads((api_dir / "tools/version.json").read_text(encoding="utf-8"))["release"]
    M, m, _ = v[1:].split(".")
    path = f"v{M}/v{M}.{m}/{v}"
    man = json.loads((api_dir / path / "manifest.json").read_text(encoding="utf-8"))
    obj = {"what": "The release of api.storyboards.sgit.ai this site loads, and the hash of every file in it, copied from its manifest. "
                   "Every page loads the kit from this exact path with these integrity strings; build.py --pin DIR moves it.",
           "host": "https://api.storyboards.sgit.ai", "release": v, "path": path,
           "files": {f["path"]: {"sha256": f["sha256"], "integrity": f["integrity"]} for f in man["files"]}}
    PIN_FILE.write_text(json.dumps(obj, indent=1) + "\n", encoding="utf-8")
    print(f"build: pinned api.storyboards.sgit.ai {v} ({len(obj['files'])} files)")


API = json.loads(PIN_FILE.read_text(encoding="utf-8")) if PIN_FILE.exists() else None
API_BASE = f"{API['host']}/{API['path']}/" if API else ""


def api_bytes(rel):
    """A file of the pinned release, from the checkout or the live host, refused unless its hash is the pinned one."""
    want = API["files"][rel]["sha256"]
    local = api_checkout() / API["path"] / rel
    data = local.read_bytes() if local.exists() else urllib.request.urlopen(API_BASE + rel, timeout=30).read()
    if hashlib.sha256(data).hexdigest() != want:
        die(f"{rel} from {'the checkout ' + str(local) if local.exists() else API_BASE} is not the pinned bytes of {API['release']}")
    return data


def api_tag(rel, attrs=""):
    f = API["files"][rel]
    if rel.endswith(".css"):
        return f'<link rel="stylesheet" href="{API_BASE}{rel}" integrity="{f["integrity"]}" crossorigin="anonymous">'
    return f'<script src="{API_BASE}{rel}" integrity="{f["integrity"]}" crossorigin="anonymous"{attrs}></script>'


def kit_scripts(packs, export=False):
    tags = [api_tag("vendor/rough-4.6.6.js")] + [api_tag(f"props/{p}.js") for p in packs] + [api_tag("storyboard.js")]
    if export:
        tags.append(api_tag("export.js"))
    return "".join(tags)


# ------------------------------------------------------------------ content
def load_versions():
    v = json.loads((CONTENT / "versions.json").read_text(encoding="utf-8"))
    rows = v["releases"]
    for r in rows:
        if not re.fullmatch(r"v\d+\.\d+\.\d+", r["version"]) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["date"]) or not r.get("what"):
            die(f"content/versions.json: a row needs version vX.Y.Z, date YYYY-MM-DD and what: {r}")
    t = lambda s: tuple(int(x) for x in s[1:].split("."))
    if [r["version"] for r in rows] != sorted((r["version"] for r in rows), key=t, reverse=True):
        die("content/versions.json: rows must be newest first")
    return rows


def load_series():
    out = []
    for d in sorted((CONTENT / "series").iterdir()):
        meta = json.loads((d / "series.json").read_text(encoding="utf-8"))
        if meta["slug"] != d.name:
            die(f"{d.name}/series.json names slug {meta['slug']}")
        # ABP-SB-002: a storyboard and its cast are the origin site's bytes; a file changed here, or added without an import, stops the build
        imported = meta["origin"].get("imported", {})
        for f in sorted(d.glob("[0-9][0-9]__*.json")) + [d / "cast.json"]:
            want = imported.get(f.name)
            if want is None:
                die(f"{d.name}/{f.name} was not imported (ABP-SB-002): bring storyboards in with admin/build/import_series.py, from their origin site")
            if hashlib.sha256(f.read_bytes()).hexdigest() != want:
                die(f"{d.name}/{f.name} is not the bytes imported from {meta['origin']['repo']} at {meta['origin']['commit'][:8]} (ABP-SB-002): "
                    "correct it at the origin and re-import with admin/build/import_series.py; this site does not edit another site's storyboard")
        for name in imported:
            if not (d / name).exists():
                die(f"{d.name}/{name} was imported and is missing")
        cast = json.loads((d / "cast.json").read_text(encoding="utf-8"))
        boards = []
        for f in sorted(d.glob("[0-9][0-9]__*.json")):
            raw = f.read_bytes()
            sb = json.loads(raw)
            if f.name[4:-5] != sb["slug"]:
                die(f"{d.name}/{f.name}: the file name and the slug {sb['slug']} disagree")
            boards.append({"file": f.name, "n": f.name[:2], "raw": raw, "sb": sb, "series": meta["slug"]})
        slugs = [b["sb"]["slug"] for b in boards]
        placed = [s for sh in meta["shelves"] for s in sh["boards"]]
        for s in slugs:
            if placed.count(s) != 1:
                die(f"{d.name}: storyboard {s} is on {placed.count(s)} shelves in series.json; it must be on exactly one")
        for s in placed:
            if s not in slugs:
                die(f"{d.name}: series.json shelves name {s}, which is not a storyboard")
        if meta["start"] not in slugs:
            die(f"{d.name}: series.json starts with {meta['start']}, which is not a storyboard")
        ids = {c["id"] for c in cast["characters"]}
        for k in meta.get("stance", {}):
            if k not in ids:
                die(f"{d.name}: series.json stance names {k}, who is not in the cast")
        out.append({"meta": meta, "cast": cast, "cast_raw": (d / "cast.json").read_bytes(), "boards": boards})
    return out


def run_formats(series):
    """Every storyboard through the API's formats.js: errors (which stop the build), markdown, graph, stats."""
    with tempfile.TemporaryDirectory() as tmp:
        fj = Path(tmp) / "formats.js"
        fj.write_bytes(api_bytes("formats.js"))
        packs = json.loads(subprocess.check_output(["node", "-e", f"process.stdout.write(JSON.stringify(require({json.dumps(str(fj))}).PACKS))"]))
        jobs = []
        for s in series:
            props = [k for p in s["meta"]["packs"] for k in packs[p]]
            for b in s["boards"]:
                url = f"{SITE}/{s['meta']['slug']}/{b['sb']['slug']}/"
                jobs.append({"key": f"{s['meta']['slug']}/{b['sb']['slug']}", "storyboard": b["sb"], "cast": s["cast"], "props": props,
                             "url": url, "castHref": "../cast.json", "seriesTitle": s["meta"]["title"]})
        r = subprocess.run(["node", str(ROOT / "admin/build/formats.mjs"), str(fj)], input=json.dumps(jobs), capture_output=True, text=True)
        if r.returncode:
            die("formats.mjs failed: " + r.stderr[-2000:])
        res = json.loads(r.stdout)
    errors = [e for k in res for e in res[k]["errors"]]
    if errors:
        die("the storyboards do not validate against the kit's vocabulary:\n  " + "\n  ".join(errors))
    return res


# ------------------------------------------------------------------ the chrome
NAV = [("Storyboards", "index.html#series"), ("Embed", "embed/index.html"), ("Formats", "formats/index.html"),
       ("Articles", "articles/index.html"), ("The brief", "brief/index.html"), ("About", "about/index.html"), ("Behaviour policy", "abp/index.html"), ("Developers \u2197", "https://api.storyboards.sgit.ai/docs/index.html")]


def page(rel, title, body, desc, version, crumbs=(), head="", scripts="", twin=None, og=None, narrow=False, current=None):
    """One page of the site: rel is its path under www/, links are relative to it."""
    depth = rel.count("/")
    up = "../" * depth
    canon = f"{SITE}/{rel}".removesuffix("index.html")
    nav = "".join(f'<a href="{href if href.startswith("https://") else up + href}"{" aria-current=\"page\"" if current == label else ""}>{label}</a>' for label, href in NAV)
    crumb = ""
    if crumbs:
        crumb = '<p class="crumb"><a href="' + up + 'index.html">Home</a> / ' + " / ".join(
            f'<a href="{up}{h}">{esc(t)}</a>' if h else esc(t) for t, h in crumbs) + "</p>"
    twin_href = twin if twin is not None else (Path(rel).with_suffix(".md").name)
    og_url = og or f"{SITE}/og.jpg"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · storyboards.sgit.ai</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canon)}">
<link rel="alternate" type="text/markdown" href="{esc(twin_href)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canon)}">
<meta property="og:type" content="website">
<meta property="og:image" content="{esc(og_url)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="site-version" content="{version}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect x='4' y='10' width='56' height='44' rx='6' fill='%23fbf7ee' stroke='%2323262b' stroke-width='4'/%3E%3Cpath d='M12 44 Q32 30 52 40' stroke='%23dc2626' stroke-width='4' fill='none'/%3E%3Ccircle cx='24' cy='26' r='6' fill='%2323262b'/%3E%3C/svg%3E">
{api_tag("fonts.css")}
{api_tag("storyboard.css")}
<link rel="stylesheet" href="{up}assets/site.css">
<script>window.StoryboardPrefsKey = 'storyboards.sgit.ai.v1';</script>
<script src="{up}assets/site.js"></script>
{head}</head>
<body>
<a class="skip" href="#main">Skip to the content</a>
<nav class="site" aria-label="Site"><div class="row">
<a class="brand" href="{up}index.html">storyboards<span>.sgit.ai</span></a>
<div class="nav-items">{nav}</div>
<div class="nav-tools"><a class="parent" href="https://sgit.ai" title="One of the sgit.ai network of sites">&#8599; part of <b>sgit.ai</b></a>
<a class="parent" href="https://api.storyboards.sgit.ai/" title="The kit that draws every panel">API {API["release"]}</a>
<button type="button" class="theme" aria-label="Switch the theme">dark</button>
<span class="ver">site <a href="{up}admin/versions.html" title="Site release history">{version}</a></span></div>
</div></nav>
<main id="main"{' class="narrow"' if narrow else ''}>
{crumb}
{body}
</main>
<footer class="site"><div class="row">
<div><b>storyboards.sgit.ai</b>: make, share and embed storyboards that are data, drawn by code. Panels drawn by <a href="https://api.storyboards.sgit.ai/">api.storyboards.sgit.ai</a> {API["release"]} (<a href="{API_BASE}manifest.json">manifest</a>); content CC BY 4.0, code Apache-2.0.</div>
<div class="netline"><a href="https://sgit.ai">&#8599; sgit.ai</a>, the parent project &middot; <a href="https://gen-z-developers.sgit.ai/storyboards/index.html">&#8599; gen-z-developers.sgit.ai</a>, where the storyboards began &middot; <a href="https://pki.sgit.ai/storyboards/index.html">&#8599; pki.sgit.ai</a> &middot; <a href="https://newsroom.sgit.ai">&#8599; newsroom.sgit.ai</a> &middot; <a href="https://sgit.ai/network/index.html">&#8599; the network</a></div>
<div>&#9888; Participant disclosure: published by the sgit project, which builds the tools these storyboards explain. <a href="{up}about/participant.html">Read the disclosure</a>.</div>
<div>Site {version} &middot; <a href="{up}admin/versions.html">release history</a> &middot; <a href="{esc(twin_href)}">this page as markdown</a> &middot; <a href="{up}llms.txt">llms.txt</a> &middot; <a href="{up}catalogue.json">catalogue.json</a> &middot; <a href="{REPO}">GitHub</a></div>
</div></footer>
{scripts}
</body>
</html>
"""


def md_twin(title, url, body_md, desc=""):
    return f"# {title}\n\n> {desc}\n\n*Source: <{url}>. This file is the page as markdown, generated from the same content.*\n\n---\n\n{body_md.strip()}\n"


# ------------------------------------------------------------------ the storyboard toolbar (gen-z-developers.sgit.ai's markup)
def sb_tools(views):
    v = ('<span class="sb-views" role="group" aria-label="View">'
         '<button type="button" data-view="deck" title="One panel at a time (d)">Deck</button>'
         '<button type="button" data-view="grid" title="Every panel on one page (g)">Grid</button>'
         '<button type="button" data-view="script" title="The storyboard as text (t)">Script</button></span>') if views else ""
    cols = "".join(f'<option value="{n}">{n}</option>' for n in range(1, 7))
    keys = ("<kbd>d</kbd> <kbd>g</kbd> <kbd>t</kbd> views &middot; " if views else "") + \
        "<kbd>a</kbd> animation &middot; <kbd>x</kbd> text &middot; <kbd>+</kbd><kbd>&minus;</kbd> per row &middot; <kbd>/</kbd> filter &middot; <kbd>p</kbd> play" + \
        (" &middot; <kbd>&larr;</kbd><kbd>&rarr;</kbd> <kbd>n</kbd> notes <kbd>f</kbd> full screen" if views else "")
    return (f'<div class="sb-tools" role="toolbar" aria-label="How to view the panels">{v}'
            f'<label class="sb-for-grid">Per row <select class="sb-cols">{cols}</select></label>'
            '<label title="Panels play as they arrive (a)"><input type="checkbox" class="sb-anim"> Animation</label>'
            '<label class="sb-for-grid" title="Each panel\'s script under it (x)"><input type="checkbox" class="sb-showtext"> Text</label>'
            '<button type="button" class="sb-playall sb-for-grid" title="Play the panels one after another (p)">Play in order</button>'
            '<input type="search" class="sb-filter sb-for-list" placeholder="Filter: a word, a name, a mood, a kind" aria-label="Filter the panels">'
            f'<span class="sb-keys">{keys}</span></div>')


def payload(obj):
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def jdump(obj):
    return (json.dumps(obj, indent=1, ensure_ascii=False) + "\n").encode("utf-8")


def bundle_of(meta, cast, sb):
    """bundle.json: a storyboard with its cast and the prop packs it needs, the one file an embed fetches. render.py draws from these bytes."""
    base = f"{meta['slug']}/{sb['slug']}/"
    return jdump({"what": f"A storyboard with its cast, for an embed: <sg-storyboard src=\"{SITE}/{base}bundle.json\">. The storyboard is {base}storyboard.json, unchanged.",
                  "series": meta["slug"], "packs": meta["packs"], "storyboard": sb, "cast": cast})


# ------------------------------------------------------------------ the build
def build(out):
    if not API:
        die("admin/build/api.json is missing: python3 admin/build/build.py --pin PATH/TO/SGit-AI__Website__Storyboards__API")
    versions = load_versions()
    V = versions[0]["version"]
    series = load_series()
    fmt = run_formats(series)
    renders = json.loads(RENDERS.read_text(encoding="utf-8")) if RENDERS.exists() else {"boards": {}}
    files = {}

    def put(rel, data):
        if rel in files:
            die(f"two things want to write {rel}")
        files[rel] = data.encode("utf-8") if isinstance(data, str) else data

    def put_page(rel, title, body, desc, md_body, **kw):
        put(rel, page(rel, title, body, desc, V, **kw))
        twin = kw.get("twin") or Path(rel).with_suffix(".md").name
        put(str(Path(rel).parent / twin) if "/" in rel else twin, md_twin(title, f"{SITE}/{rel}".removesuffix("index.html"), md_body, desc))

    catalogue = []
    total_panels = sum(len(b["sb"]["scenes"]) for s in series for b in s["boards"])
    for s in series:
        meta, cast = s["meta"], s["cast"]
        S = meta["slug"]
        names = {c["id"]: c["name"] for c in cast["characters"]}
        put(f"{S}/cast.json", s["cast_raw"])
        by_slug = {b["sb"]["slug"]: b for b in s["boards"]}
        origin = meta["origin"]
        origin_tree = f"https://github.com/{origin['repo']}/blob/{origin['commit']}/"
        for b in s["boards"]:
            sb, slug = b["sb"], b["sb"]["slug"]
            key = f"{S}/{slug}"
            base = f"{S}/{slug}/"
            f = fmt[key]
            bundle_bytes = bundle_of(meta, cast, sb)
            put(base + "storyboard.json", b["raw"])
            put(base + "bundle.json", bundle_bytes)
            put(base + "graph.json", jdump(f["graph"]))
            # the renders are committed; the build checks they were drawn from these bytes by the pinned release
            stamp = hashlib.sha256(bundle_bytes).hexdigest()
            r = renders["boards"].get(key)
            if not r or r.get("bundle_sha256") != stamp or r.get("api") != API["release"]:
                die(f"{key}: thumb.jpg and og.jpg are stale or missing (the storyboard, its cast or the pinned API changed): python3 admin/build/render.py")
            n = len(sb["scenes"])
            tries = "".join(f'<a class="btn{" ink" if i == 0 else ""}" href="{esc(h if h.startswith("http") else origin["site"] + "/" + h)}">{esc(l)} &rarr;</a>'
                            for i, (l, h) in enumerate(sb.get("try_it", [])))
            qs = sb.get("quote_source")
            src_line = (f' Every quote and Guide line was checked word for word against <a href="{origin_tree}{esc(qs)}">{esc(qs)}</a> by the origin site\'s build.' if qs else "")
            rows = "".join(f'<li><a href="#scene-{i}">{i}</a>. {esc(fmt[key]["texts"][i - 1][:160])}'
                           f' <span class="small dim">({esc(sc.get("kind", "scene"))}{"; " + esc(sc.get("source")) if sc.get("source") else ""})</span></li>'
                           for i, sc in enumerate(sb["scenes"], 1))
            embed = (f'<script src="{API_BASE}embed.js" defer></script>\n'
                     f'<sg-storyboard src="{SITE}/{base}bundle.json" view="deck"></sg-storyboard>')
            body = f"""<p class="kicker small dim">{esc(meta["title"])} &middot; {esc(sb.get("shelf") or next(sh["title"] for sh in meta["shelves"] if slug in sh["boards"]))} &middot; board {b["n"]}</p>
<h1>{esc(sb["title"])}</h1>
<p class="lede">{esc(sb.get("subtitle", ""))}</p>
<p class="small dim"><span class="pill {esc(sb.get("status", ""))}">{esc(sb.get("status", ""))}</span> {n} panels &middot; {esc(sb.get("by", ""))}{" &middot; book " + esc(sb["book_version"]) if sb.get("book_version") else ""}. {esc(sb.get("rule", ""))}</p>
{f'<div class="try">{tries}</div>' if tries else ""}
<div class="sb-viewer">{sb_tools(views=True)}
<div class="sb-deck" hidden><div class="sb-track"></div>
<div class="sb-bar"><button type="button" class="sb-prev" aria-label="Previous panel">&larr;</button><span class="sb-count"></span><button type="button" class="sb-next" aria-label="Next panel">&rarr;</button><button type="button" class="sb-replay" title="Play this panel (p)">&#9654; Play</button><button type="button" class="sb-notes-toggle" title="Notes (n)">Notes</button><button type="button" class="sb-full" title="Full screen (f)">Full screen</button></div>
<div class="sb-notes"></div></div>
<div class="sb-grid" hidden></div>
<div class="sb-script" hidden></div>
<script type="application/json" class="sb-data">{payload({"storyboard": sb, "cast": cast})}</script></div>

<h2 id="formats">Take it with you</h2>
<p class="small dim">The same storyboard in every shape it comes in. The data and its derived files are on this site; the pictures are drawn in your browser, now, by the same code as the deck (<code>export.js</code>, {API["release"]}), from the <span class="which">current panel</span>.</p>
<div class="formats">
<a href="storyboard.json"><b>storyboard.json</b><span>the data, as {esc(origin["site"].removeprefix("https://"))} wrote it</span></a>
<a href="bundle.json"><b>bundle.json</b><span>the data with its cast, for an embed</span></a>
<a href="index.md"><b>index.md</b><span>the script, as markdown</span></a>
<a href="graph.json"><b>graph.json</b><span>a semantic graph: {len(f["graph"]["nodes"])} nodes, {len(f["graph"]["edges"])} edges</span></a>
<a href="thumb.jpg"><b>thumb.jpg</b><span>the cover, 480 wide</span></a>
<a href="og.jpg"><b>og.jpg</b><span>the cover, 1200 wide</span></a>
</div>
<div class="formats exports">
<button type="button" data-export="svg"><b>SVG</b><span>this panel, sharp at any size</span></button>
<button type="button" data-export="animated"><b>Animated SVG</b><span>this panel, drawing itself</span></button>
<button type="button" data-export="png"><b>PNG</b><span>this panel, 1600&times;1000</span></button>
<button type="button" data-export="jpg"><b>JPEG</b><span>this panel, 1600&times;1000</span></button>
<button type="button" data-export="sheet"><b>Every panel, one SVG</b><span>a contact sheet, four per row</span></button>
</div>

<h2 id="embed">Put it on your page</h2>
<p class="small dim">Two lines, from any site. The script is pinned to an immutable release of the kit, so the embed draws exactly this, for as long as the page exists. <a href="../../embed/index.html">How embedding works</a>.</p>
<div class="embed-code"><pre><code id="embed-snippet">{esc(embed)}</code></pre><button type="button" class="btn" data-copy="#embed-snippet">Copy</button></div>

<h2 id="panels">The panels</h2>
<ol class="small">{rows}</ol>
<p class="small dim">Imported unchanged from <a href="{origin_tree}{esc(origin["path"] + b["file"])}">{esc(origin["repo"])}/{esc(origin["path"] + b["file"])}</a> at commit <code>{origin["commit"][:8]}</code> ({origin["date"]}).{src_line} The cast is <a href="../cast.json">cast.json</a>.</p>
"""
            put_page(base + "index.html", sb["title"], body, sb.get("subtitle", ""), f["md"],
                     crumbs=((meta["title"], f"{S}/index.html"), (sb["title"], None)),
                     scripts=kit_scripts(meta["packs"], export=True), og=f"{SITE}/{base}og.jpg", current="Storyboards")
            # the twin of a storyboard's page is the script itself, not a copy of the page
            files[base + "index.md"] = f["md"].encode("utf-8")
            catalogue.append({"series": S, "slug": slug, "title": sb["title"], "subtitle": sb.get("subtitle", ""), "status": sb.get("status", ""),
                              "panels": n, "cast": f["stats"]["cast"], "page": f"{SITE}/{base}",
                              "formats": {k: f"{SITE}/{base}{v}" for k, v in [("json", "storyboard.json"), ("bundle", "bundle.json"), ("markdown", "index.md"),
                                                                             ("graph", "graph.json"), ("thumbnail", "thumb.jpg"), ("og", "og.jpg")]},
                              "embed": embed, "origin": f"{origin_tree}{origin['path']}{b['file']}"})

        # ---- the series: the comic shelf (gen-z-developers.sgit.ai's, drawn live by the kit's shelf())
        stance = meta.get("stance", {})

        def faces_of(sb, k=4):
            count = {}
            for sc in sb["scenes"]:
                for c in sc.get("cast", []):
                    count[c["who"]] = count.get(c["who"], 0) + 1
            return [w for w, _ in sorted(count.items(), key=lambda x: (-x[1], x[0]))[:k]]

        def faces_html(sb, cls="sbx-face"):
            return "".join(f'<svg class="{cls}" data-who="{esc(w)}" role="img" aria-label="{esc(names[w])}"><title>{esc(names[w])}</title></svg>' for w in faces_of(sb))

        def thumb(slug, i, cls="sbx-thumb"):
            return f'<svg class="{cls}" data-board="{esc(slug)}" data-scene="{i}" viewBox="0 0 1600 1000" role="img" aria-label="Panel {i + 1}"></svg>'

        def card(slug):
            b = by_slug[slug]
            sb = b["sb"]
            href = f"{slug}/index.html"
            strip = "".join(thumb(slug, i) for i in range(1, min(4, len(sb["scenes"]))))
            return (f'<article class="sbx-card"><a class="sbx-cover" href="{href}" aria-label="{esc(sb["title"])}: open the deck">{thumb(slug, 0)}'
                    f'<span class="sbx-tag">{b["n"]}</span></a>'
                    f'<a class="sbx-strip" href="{href}?view=grid" aria-label="{esc(sb["title"])}: every panel">{strip}</a>'
                    f'<div class="sbx-body"><h3><a href="{href}">{esc(sb["title"])}</a></h3><p>{esc(sb.get("subtitle", ""))}</p>'
                    f'<div class="sbx-meta"><span class="sbx-faces">{faces_html(sb)}</span><span>{len(sb["scenes"])} panels</span>'
                    f'<span class="sbx-status sbx-{esc(sb.get("status", ""))}">{esc(sb.get("status", ""))}</span></div></div></article>')

        st = by_slug[meta["start"]]
        ssb, sn = st["sb"], len(st["sb"]["scenes"])
        shref = f"{meta['start']}/index.html"
        start = (f'<section class="sbx-start" aria-labelledby="sbx-start-h"><p class="sbx-kicker">Start here</p><div class="sbx-start-grid">'
                 f'<div><a class="sbx-cover sbx-big" href="{shref}" aria-label="{esc(ssb["title"])}: open the deck">{thumb(ssb["slug"], 0)}</a>'
                 f'<div class="sbx-start-strip">{"".join(thumb(ssb["slug"], i) for i in range(1, min(4, sn)))}'
                 f'<a class="sbx-more" href="{shref}?view=grid">+{max(0, sn - 4)} more</a></div></div>'
                 f'<div class="sbx-start-text"><span class="sbx-tag sbx-tag-big">{st["n"]}</span>'
                 f'<h2 id="sbx-start-h">{esc(ssb["title"])}</h2><p>{esc(ssb.get("subtitle", ""))}</p>'
                 f'<div class="sbx-meta"><span class="sbx-faces">{faces_html(ssb, "sbx-face sbx-face-big")}</span><span>{sn} panels &middot; {esc(ssb.get("status", ""))}</span></div>'
                 f'<div class="sbx-actions"><a class="sbx-btn sbx-btn-go" href="{shref}?view=deck">&#9654; Play the deck</a>'
                 f'<a class="sbx-btn" href="{shref}?view=grid">See all {sn}</a><a class="sbx-btn" href="{shref}?view=script">Read the script</a></div>'
                 f'</div></div></section>')
        shelf_html = "".join(
            f'<section class="sbx-shelf" aria-labelledby="sbx-shelf-{k}"><div class="sbx-head"><h2 id="sbx-shelf-{k}">{esc(sh["title"])}</h2><p>{esc(sh.get("note", ""))}</p></div>'
            f'<div class="sbx-cards">{"".join(card(slug) for slug in sh["boards"])}</div></section>'
            for k, sh in enumerate(meta["shelves"], 1))
        cast_html = "".join(
            f'<figure class="sbx-person"><div class="sbx-bubble">&ldquo;{esc(c.get("line", ""))}&rdquo;</div>'
            f'<svg class="sbx-figure" data-who="{esc(c["id"])}" data-pose="{stance.get(c["id"], ("stand", "happy"))[0]}" data-mood="{stance.get(c["id"], ("stand", "happy"))[1]}" role="img" aria-label="{esc(c["name"])}"></svg>'
            f'<figcaption><b>{esc(c["name"])}</b><span>{esc(c.get("role", ""))}</span>'
            f'<details><summary>More</summary><dl><dt>Stands for</dt><dd>{esc(c.get("stands_for", ""))}</dd><dt>Personality</dt><dd>{esc(c.get("personality", ""))}</dd>'
            f'<dt>Wants</dt><dd>{esc(c.get("wants", ""))}</dd><dt>Fears</dt><dd>{esc(c.get("fears", ""))}</dd></dl></details></figcaption></figure>'
            for c in cast["characters"])
        stotal = sum(len(b["sb"]["scenes"]) for b in s["boards"])
        lineup_names = "".join(f"<span>{esc(c['name'])}</span>" for c in cast["characters"])
        data = {"cast": cast, "boards": {b["sb"]["slug"]: {"title": b["sb"]["title"], "scenes": b["sb"]["scenes"][:4]} for b in s["boards"]},
                "stance": {k: list(v) for k, v in stance.items()}}
        body = f"""<div class="sbx">
<section class="sbx-hero" aria-labelledby="sbx-h1">
<p class="sbx-count">{len(s["boards"])} storyboards &middot; {stotal} panels &middot; {len(cast["characters"])} characters &middot; all drawn from data</p>
<h1 id="sbx-h1">{esc(meta["title"])}</h1>
<svg class="sbx-underline" aria-hidden="true" viewBox="0 0 620 22" preserveAspectRatio="none"><path d="M4 14 Q 160 4 310 12 T 616 8"></path></svg>
<p class="sbx-lede">{esc(meta["blurb"])}</p>
<div class="sbx-actions"><a class="sbx-btn sbx-btn-ink" href="{shref}">Start with {esc(ssb["title"])} &rarr;</a><a class="sbx-btn sbx-btn-marker" href="all.html">Every panel on one page</a><a class="sbx-btn sbx-btn-line" href="#cast">Meet the cast</a></div>
<svg class="sbx-lineup" role="img" aria-label="The cast in a row: {esc(", ".join(names.values()))}"></svg>
<div class="sbx-names" style="--n:{len(cast["characters"])}">{lineup_names}</div>
</section>
{start}
{shelf_html}
<section class="sbx-cast" id="cast" aria-labelledby="sbx-cast-h"><div class="sbx-head"><h2 id="sbx-cast-h">The cast</h2><p>{esc(cast.get("what", ""))}</p><a href="model-sheet.html">The model sheet: every mood and pose &rarr;</a></div>
<div class="sbx-people">{cast_html}</div></section>
<p class="small dim">From <a href="{origin["site"]}/storyboards/index.html">{esc(origin["site"].removeprefix("https://"))}</a>, imported unchanged at commit <a href="https://github.com/{origin["repo"]}/tree/{origin["commit"]}/{origin["path"]}"><code>{origin["commit"][:8]}</code></a> ({origin["date"]}). {esc(meta.get("quotes", ""))}</p>
<script type="application/json" class="sb-data">{payload(data)}</script>
</div>
"""
        smd = [f"{meta['blurb']}", "", f"Imported from {origin['site']} at commit {origin['commit'][:8]} ({origin['date']}).", ""]
        for sh in meta["shelves"]:
            smd += [f"## {sh['title']}", "", sh.get("note", ""), ""]
            smd += [f"- [{by_slug[x]['sb']['title']}]({x}/index.md): {by_slug[x]['sb'].get('subtitle', '')} ({len(by_slug[x]['sb']['scenes'])} panels, {by_slug[x]['sb'].get('status', '')})" for x in sh["boards"]]
            smd.append("")
        smd += ["## The cast", ""] + [f"- **{c['name']}** ({c.get('kind', 'human')}): {c.get('role', '')}" for c in cast["characters"]]
        put_page(f"{S}/index.html", meta["title"], body, meta["tagline"] + " " + meta["blurb"], "\n".join(smd),
                 crumbs=((meta["title"], None),), scripts=kit_scripts(meta["packs"]), og=f"{SITE}/{S}/{meta['start']}/og.jpg", current="Storyboards")
        # every panel of the series on one page
        data = {"boards": [{"href": f"{b['sb']['slug']}/index.html", "storyboard": b["sb"]} for b in s["boards"]], "cast": cast}
        body = f"""<h1>Every panel</h1>
<p class="lede">All {len(s["boards"])} storyboards of {esc(meta["title"])}, {stotal} panels, on one page, in order: to see the series as a flow rather than one panel at a time. A click on a panel plays it; its number opens it in that storyboard's deck.</p>
<div class="sb-contact" data-view="grid">{sb_tools(views=False)}<script type="application/json" class="sb-data">{payload(data)}</script></div>
"""
        put_page(f"{S}/all.html", f"Every panel: {meta['title']}", body, f"All {stotal} panels of {meta['title']} on one page.",
                 "\n".join(f"- [{b['sb']['title']}]({b['sb']['slug']}/index.md), {len(b['sb']['scenes'])} panels" for b in s["boards"]),
                 crumbs=((meta["title"], f"{S}/index.html"), ("Every panel", None)), scripts=kit_scripts(meta["packs"]), current="Storyboards")
        body = f"""<h1>The model sheet</h1>
<p class="lede">Every character of {esc(meta["title"])} in every mood and every pose, side by side, the way animators check a character is on model: a face that reads wrong here reads wrong in every panel it is in.</p>
<div class="sb-sheet"><script type="application/json" class="sb-data">{payload({"cast": cast})}</script></div>
"""
        put_page(f"{S}/model-sheet.html", f"The model sheet: {meta['title']}", body, f"Every character of {meta['title']} in every mood and pose.",
                 "\n".join(f"- **{c['name']}**: {c.get('role', '')}" for c in cast["characters"]),
                 crumbs=((meta["title"], f"{S}/index.html"), ("The model sheet", None)), scripts=kit_scripts(meta["packs"]), current="Storyboards")

    # ---- articles
    articles = []
    for f in sorted((CONTENT / "articles").glob("*.md")):
        m, body_md = front_matter(f.read_text(encoding="utf-8"))
        for k in ("title", "date", "by", "summary"):
            if not m.get(k):
                die(f"content/articles/{f.name}: front matter needs {k}")
        slug = f.stem.split("__", 1)[-1]
        articles.append((m, slug, body_md))
    articles.sort(key=lambda a: (a[0]["date"], a[1]), reverse=True)
    for m, slug, body_md in articles:
        body = f"""<article class="article"><h1>{esc(m["title"])}</h1>
<p class="lede">{esc(m["summary"])}</p>
<p class="byline">{esc(m["by"])} &middot; {esc(m["date"])}{" &middot; site " + esc(m["version"]) if m.get("version") else ""}</p>
{md_render(body_md)}
</article>"""
        put_page(f"articles/{slug}.html", m["title"], body, m["summary"], body_md, crumbs=(("Articles", "articles/index.html"), (m["title"], None)), current="Articles", narrow=True)
    body = '<h1>Articles</h1><p class="lede">How storyboards.sgit.ai came to be, how it is built, and what a storyboard is for.</p><ul class="list">' + "".join(
        f'<li><a href="{slug}.html">{esc(m["title"])}</a> <span class="small dim">{esc(m["date"])} &middot; {esc(m["by"])}</span><p>{esc(m["summary"])}</p></li>' for m, slug, _ in articles) + "</ul>"
    put_page("articles/index.html", "Articles", body, "Articles about storyboards.sgit.ai.",
             "\n".join(f"- [{m['title']}]({slug}.md) ({m['date']}): {m['summary']}" for m, slug, _ in articles), crumbs=(("Articles", None),), current="Articles", narrow=True)

    # ---- pages written as markdown: content/pages/<path>.md -> <path>.html (index.md -> index.html in its folder)
    for f in sorted((CONTENT / "pages").rglob("*.md")):
        m, body_md = front_matter(f.read_text(encoding="utf-8"))
        rel = f.relative_to(CONTENT / "pages").with_suffix(".html").as_posix()
        body_md = body_md.replace("{{API_BASE}}", API_BASE).replace("{{API_RELEASE}}", API["release"]).replace("{{SITE}}", SITE)
        body = f'<article class="article"><h1>{esc(m["title"])}</h1><p class="lede">{esc(m.get("summary", ""))}</p>{md_render(body_md)}</article>'
        crumbs = ((m["title"], None),)
        put_page(rel, m["title"], body, m.get("summary", ""), body_md, crumbs=crumbs, current=m.get("nav"), narrow=True)

    # ---- the brief, in full: briefs/*.md, newest first, each its own page
    briefs = []
    for f in sorted((ROOT / "briefs").glob("*.md"), reverse=True):
        m, body_md = front_matter(f.read_text(encoding="utf-8"))
        briefs.append((m, f.stem, body_md))
        body = f'<article class="article"><h1>{esc(m["title"])}</h1><p class="byline">{esc(m.get("status", ""))} &middot; {esc(m.get("date", ""))} &middot; {esc(m.get("by", ""))}</p>{md_render(body_md)}</article>'
        put_page(f"brief/{f.stem}.html", m["title"], body, m.get("summary", m["title"]), body_md, crumbs=(("The brief", "brief/index.html"), (m["title"], None)), current="The brief", narrow=True)
    body = ('<h1>The brief</h1><p class="lede">The words this site was built from, published in full and never edited afterwards. '
            f'Where a brief turned out to be wrong, the correction is in <a href="{REPO}/blob/dev/BRIEF-CORRECTIONS.md">BRIEF-CORRECTIONS.md</a>, not in the brief.</p><ul class="list">' + "".join(
                f'<li><a href="{stem}.html">{esc(m["title"])}</a> <span class="small dim">{esc(m.get("date", ""))} &middot; {esc(m.get("status", ""))}</span><p>{esc(m.get("summary", ""))}</p></li>' for m, stem, _ in briefs) + "</ul>")
    put_page("brief/index.html", "The brief", body, "The brief storyboards.sgit.ai was built from, in full.",
             "\n".join(f"- [{m['title']}]({stem}.md) ({m.get('date', '')}, {m.get('status', '')})" for m, stem, _ in briefs), crumbs=(("The brief", None),), current="The brief", narrow=True)

    # ---- the agent behaviour policy: a top-level page from policies/abp.json, and the data itself beside it
    abp = json.loads((ROOT / "policies/abp.json").read_text(encoding="utf-8"))
    problems = ABP.check(abp)
    if problems:
        die("policies/abp.json: " + "; ".join(problems))
    abp_md = ABP.markdown(abp)
    put_page("abp/index.html", "Agent behaviour policy", f'<article class="article"><h1>Agent behaviour policy</h1><p class="lede">The agents that work on {HOST}, what they can do, what they are asked to do, and what stands in the way of each rule.</p>{md_render(abp_md)}</article>',
             f"The agents that work on {HOST}, what they can do, what they are asked to do, and what stands in the way of each rule.", abp_md, crumbs=(("Agent behaviour policy", None),), current="Behaviour policy")
    put("abp/abp.json", (ROOT / "policies/abp.json").read_bytes())

    # ---- release history
    rows = "".join(f'<tr><td class="ver">{esc(r["version"])}</td><td>{esc(r["date"])}</td><td>{esc(r["what"])}</td></tr>' for r in versions)
    body = (f'<h1>Release history</h1><p class="lede">One row per push to dev, newest first. The site is at {V}; it draws every panel with '
            f'<a href="https://api.storyboards.sgit.ai/">api.storyboards.sgit.ai</a> {API["release"]}, pinned in <code>admin/build/api.json</code>.</p>'
            f'<table><thead><tr><th>Version</th><th>Date</th><th>What changed, and why</th></tr></thead><tbody>{rows}</tbody></table>')
    put_page("admin/versions.html", "Release history", body, "Every release of storyboards.sgit.ai.",
             "| Version | Date | What changed |\n|---|---|---|\n" + "\n".join(f"| {r['version']} | {r['date']} | {r['what']} |" for r in versions),
             crumbs=(("Release history", None),))

    # ---- home
    start = series[0]["meta"]
    hero_board = next(b for b in series[0]["boards"] if b["sb"]["slug"] == start["start"])
    cards = []
    for s in series:
        meta = s["meta"]
        S = meta["slug"]
        by_slug = {b["sb"]["slug"]: b for b in s["boards"]}
        shelves = "".join(
            f'<p class="shelf-title">{esc(sh["title"])}</p><p class="shelf-note">{esc(sh.get("note", ""))}</p><div class="cards">' + "".join(
                f'<article class="card"><img src="{S}/{x}/thumb.jpg" alt="The cover of {esc(by_slug[x]["sb"]["title"])}" width="480" height="300" loading="lazy">'
                f'<div class="body"><h3><a href="{S}/{x}/index.html">{esc(by_slug[x]["sb"]["title"])}</a></h3><p>{esc(by_slug[x]["sb"].get("subtitle", ""))}</p>'
                f'<div class="meta"><span>{len(by_slug[x]["sb"]["scenes"])} panels</span><span class="pill {esc(by_slug[x]["sb"].get("status", ""))}">{esc(by_slug[x]["sb"].get("status", ""))}</span></div></div></article>'
                for x in sh["boards"]) + "</div>" for sh in meta["shelves"])
        cards.append(f'<section class="series" id="{S}"><div class="series-head"><div><h2><a href="{S}/index.html">{esc(meta["title"])}</a></h2><p>{esc(meta["blurb"])}</p></div>'
                     f'<div class="actions"><a class="btn" href="{S}/index.html">The shelf &rarr;</a><a class="btn" href="{S}/all.html">Every panel</a><a class="btn" href="{S}/model-sheet.html">The model sheet</a></div></div>{shelves}</section>')
    nboards = sum(len(s["boards"]) for s in series)
    nchars = sum(len(s["cast"]["characters"]) for s in series)
    latest = "".join(f'<li><a href="articles/{slug}.html">{esc(m["title"])}</a> <span class="small dim">{esc(m["date"])}</span><p>{esc(m["summary"])}</p></li>' for m, slug, _ in articles[:4])
    body = f"""<section class="hero" aria-labelledby="h1">
<div>
<p class="count">{nboards} storyboards &middot; {total_panels} panels &middot; {len(series)} series &middot; {nchars} characters &middot; all drawn from data</p>
<h1 id="h1">Storyboards, drawn from data</h1>
<svg class="underline" aria-hidden="true" viewBox="0 0 620 22" preserveAspectRatio="none"><path d="M4 14 Q 160 4 310 12 T 616 8"></path></svg>
<p class="lede">A storyboard is a short strip of panels: who is there, what they say, the evidence, the punchline. Here each one is a JSON file, and the panels are drawn by code in your browser, so a panel is corrected by changing a line. Read them, take them in seven shapes, or put one on your own page with two lines.</p>
<div class="actions"><a class="btn ink" href="{start["slug"]}/{start["start"]}/index.html">&#9654; Play {esc(hero_board["sb"]["title"])}</a><a class="btn marker" href="#series">Every storyboard</a><a class="btn" href="embed/index.html">Embed one</a></div>
</div>
<div class="hero-panel"><sg-storyboard src="{start["slug"]}/{start["start"]}/bundle.json" view="panel" panel="1"><img src="{start["slug"]}/{start["start"]}/thumb.jpg" alt="The cover of {esc(hero_board["sb"]["title"])}" width="480" height="300"></sg-storyboard></div>
</section>
<div class="features">
<div class="feature"><b>Data, not pictures</b><span>Each storyboard is one JSON file and its cast another. An unknown character, pose, mood or prop stops the build.</span></div>
<div class="feature"><b>Seven shapes</b><span>The deck, the JSON, the markdown script, a semantic graph, SVG, animated SVG and PNG or JPEG, all from the same data. <a href="formats/index.html">The formats</a>.</span></div>
<div class="feature"><b>Embed anywhere</b><span>One script tag from <a href="https://api.storyboards.sgit.ai/">api.storyboards.sgit.ai</a>, one element. <a href="embed/index.html">How</a>.</span></div>
<div class="feature"><b>Every version a folder</b><span>The kit is served at <code>/v0/v0.1/v0.1.0/</code>, never changed once published, with a hash for every file. <a href="articles/every-version-is-a-folder.html">Why</a>.</span></div>
</div>
<h2 id="series">Every storyboard</h2>
{"".join(cards)}
<h2 id="articles">Articles</h2>
<ul class="list">{latest}</ul>
"""
    hmd = ["Storyboards drawn from data: every storyboard here is a JSON file, drawn by code in the reader's browser.", ""]
    for s in series:
        hmd += [f"## {s['meta']['title']}", "", s["meta"]["blurb"], ""] + [f"- [{b['sb']['title']}]({s['meta']['slug']}/{b['sb']['slug']}/index.md): {b['sb'].get('subtitle', '')}" for b in s["boards"]] + [""]
    hmd += ["## Articles", ""] + [f"- [{m['title']}](articles/{slug}.md): {m['summary']}" for m, slug, _ in articles]
    put_page("index.html", "Storyboards, drawn from data", body,
             f"{nboards} storyboards, {total_panels} panels, drawn from data by code: read them, take them as JSON, markdown, a graph, SVG or PNG, or embed one.",
             "\n".join(hmd), scripts=api_tag("embed.js", " defer"), og=f"{SITE}/{start['slug']}/{start['start']}/og.jpg", current="Storyboards")

    # ---- 404
    put("404.html", page("404.html", "Not here", '<h1>Not here</h1><p class="lede">There is no page at this address. <a href="/index.html">Every storyboard is on the home page</a>.</p>',
                         "Not found.", V, twin="/index.md").replace("<head>", '<head>\n<meta name="robots" content="noindex">').replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/'))

    # ---- machine-readable: catalogue.json, llms.txt, sitemap.xml, robots.txt, CNAME
    put("catalogue.json", jdump({"what": "Every storyboard on storyboards.sgit.ai, with every format it comes in and the embed snippet. Generated by admin/build/build.py.",
                                 "site": SITE, "version": V, "api": {"release": API["release"], "base": API_BASE},
                                 "series": [{"slug": s["meta"]["slug"], "title": s["meta"]["title"], "cast": f"{SITE}/{s['meta']['slug']}/cast.json",
                                             "packs": s["meta"]["packs"], "origin": s["meta"]["origin"]} for s in series],
                                 "storyboards": catalogue}))
    llms = [f"# {HOST}", "", f"> Storyboards drawn from data: {nboards} storyboards, {total_panels} panels, {len(series)} series. Each storyboard is a JSON file "
            f"drawn by code (api.storyboards.sgit.ai {API['release']}); each comes as JSON, a bundle with its cast, a markdown script, a semantic graph and images. Site {V}.", "",
            "Every page has a markdown twin (replace .html with .md; a storyboard's twin is its script, index.md). The full index of storyboards and formats is "
            f"{SITE}/catalogue.json.", "", "## Series", ""]
    for s in series:
        llms += [f"### {s['meta']['title']}", "", s["meta"]["blurb"], ""]
        llms += [f"- [{b['sb']['title']}]({SITE}/{s['meta']['slug']}/{b['sb']['slug']}/index.md): {b['sb'].get('subtitle', '')}" for b in s["boards"]] + [""]
    llms += ["## Pages", ""] + [f"- [{label}]({SITE}/{Path(href).with_suffix('.md').as_posix()})" for label, href in NAV[1:] if not href.startswith("https://")] + [""]
    llms += ["## Articles", ""] + [f"- [{m['title']}]({SITE}/articles/{slug}.md): {m['summary']}" for m, slug, _ in articles] + [""]
    llms += ["## Agent behaviour policy", "", f"- [The agents, their grant, mandate and rules]({SITE}/abp/index.md); data: {SITE}/abp/abp.json", ""]
    llms += ["## The API", "", f"- [api.storyboards.sgit.ai](https://api.storyboards.sgit.ai/llms.txt): the kit that draws every panel, in immutable versioned folders; this site pins {API_BASE}", ""]
    put("llms.txt", "\n".join(llms))
    urls = sorted(r for r in files if r.endswith(".html") and r != "404.html")
    put("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"<url><loc>{SITE}/{u.removesuffix('index.html')}</loc></url>\n" for u in urls) + "</urlset>\n")
    put("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    put("CNAME", HOST + "\n")
    put(".nojekyll", "")
    for a in ("site.css", "site.js"):
        put(f"assets/{a}", (ROOT / "admin/assets" / a).read_bytes())
    put("og.jpg", (OUT / start["slug"] / start["start"] / "og.jpg").read_bytes() if (OUT / start["slug"] / start["start"] / "og.jpg").exists() else b"")

    # ---- write: the renders stay, everything else is exactly what this build made
    keep = {f"{k}/{name}" for k in renders["boards"] for name in RENDERED}
    if out.exists():
        for p in sorted(out.rglob("*"), reverse=True):
            rel = p.relative_to(out).as_posix()
            if p.is_file() and rel not in files and rel not in keep:
                p.unlink()
            elif p.is_dir() and not any(p.iterdir()):
                p.rmdir()
    for rel, data in files.items():
        p = out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists() or p.read_bytes() != data:
            p.write_bytes(data)
    if out == OUT:
        print(f"build: www/ is site {V}: {len(files)} files, {nboards} storyboards, {total_panels} panels, kit {API['release']}")
    return files


def check():
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp) / "www"
        if OUT.exists():
            shutil.copytree(OUT, t)
        files = build(t)
        diffs = []
        for rel, data in files.items():
            p = OUT / rel
            if not p.exists() or p.read_bytes() != data:
                diffs.append(rel)
        renders = json.loads(RENDERS.read_text(encoding="utf-8"))
        keep = {f"{k}/{name}" for k in renders["boards"] for name in RENDERED}
        for p in OUT.rglob("*"):
            rel = p.relative_to(OUT).as_posix()
            if p.is_file() and rel not in files and rel not in keep:
                diffs.append(rel + " (not made by the build)")
        for k in renders["boards"]:
            for name in RENDERED:
                if not (OUT / k / name).exists():
                    diffs.append(f"{k}/{name} (missing render)")
        if diffs:
            die("www/ is not what the build makes (run python3 admin/build/build.py and commit):\n  " + "\n  ".join(sorted(diffs)[:30]))
    print(f"build --check: www/ is what the build makes ({len(files)} files)")


if __name__ == "__main__":
    if "--pin" in sys.argv:
        pin(sys.argv[sys.argv.index("--pin") + 1])
    elif "--check" in sys.argv:
        check()
    else:
        build(OUT)
