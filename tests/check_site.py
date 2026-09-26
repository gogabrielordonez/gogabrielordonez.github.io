#!/usr/bin/env python3
# spec: 001-site-fixes-for-gabrielordonez-com
"""Checks for specs/001-site-fixes-for-gabrielordonez-com, one per task.

Written from spec.md before the pages were changed, so a tick has something
to answer to. Each check is one function, `check_T###`, whose docstring names
the requirements it proves and whose body is the whole assertion.

    python3 tests/check_site.py          # fails for ticked tasks whose check fails
    python3 tests/check_site.py --all    # every task must pass (T012, the finish line)
    python3 tests/check_site.py --live   # also fetch the FR-05 URLs over HTTP

Coquivacoa runs the default mode after every OpenCode session. A task ticked
in tasks.md whose check fails turns the run red, so a tick is a claim the
files have to back. Unticked tasks print as pending. Standard library only.
"""

from __future__ import annotations

import json
import re
import struct
import subprocess
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS = ROOT / "specs" / "001-site-fixes-for-gabrielordonez-com" / "tasks.md"
SITE = "https://gabrielordonez.com/"
OG_IMAGE = SITE + "og-image.jpg"


class Page(HTMLParser):
    """What a page declares in its markup: title, meta, canonical, JSON-LD."""

    def __init__(self, rel: str):
        super().__init__()
        self.rel = rel
        self.title = ""
        self.meta: dict[str, str] = {}
        self.canonical: list[str] = []
        self.refresh = False
        self.ld: list[str] = []
        self._in_title = self._in_ld = False
        self._buf = ""
        self.feed((ROOT / rel).read_text(encoding="utf-8"))
        self.title = " ".join(self.title.split())

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            if (a.get("http-equiv") or "").lower() == "refresh":
                self.refresh = True
            key = a.get("property") or a.get("name")
            if key and a.get("content") is not None:
                self.meta[key.lower()] = " ".join(a["content"].split())
        elif tag == "link" and "canonical" in (a.get("rel") or "").lower().split():
            self.canonical.append(a.get("href") or "")
        elif tag == "script" and (a.get("type") or "").lower() == "application/ld+json":
            self._in_ld, self._buf = True, ""

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._in_ld:
            self._in_ld = False
            self.ld.append(self._buf)

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_ld:
            self._buf += data


def check_T001() -> list[str]:
    """FR-03 FR-12: the homepage meta description is 150-160 characters.

    `/` and `/index.html` are one file on GitHub Pages, so FR-12's "identical
    to the homepage" holds only while no other file answers `/`: no second
    index page and no redirect.
    """
    p, problems = Page("index.html"), []
    d = p.meta.get("description", "")
    if not d:
        problems.append("index.html has no meta description")
    elif not 150 <= len(d) <= 160:
        problems.append(f"index.html meta description is {len(d)} characters, not 150-160")
    others = [n for n in ("index.htm", "home.html", "default.html") if (ROOT / n).exists()]
    if others:
        problems.append(f"{others} could answer / instead of index.html")
    if p.refresh:
        problems.append("index.html redirects with meta refresh")
    return problems


def check_T002() -> list[str]:
    """FR-02 FR-04: index.html declares exactly one canonical, the site root."""
    c = Page("index.html").canonical
    return [] if c == [SITE] else [f"index.html canonical is {c or 'missing'}, not [{SITE}]"]


def check_T003() -> list[str]:
    """FR-01 FR-07: index.html og:title equals its <title>."""
    p = Page("index.html")
    got = p.meta.get("og:title")
    if got is None:
        return ["index.html has no og:title"]
    return [] if got == p.title else [f"og:title {got!r} is not <title> {p.title!r}"]


def check_T004() -> list[str]:
    """FR-01 FR-07: index.html og:description equals its meta description."""
    p = Page("index.html")
    got, want = p.meta.get("og:description"), p.meta.get("description")
    if got is None:
        return ["index.html has no og:description"]
    return [] if got == want else [f"og:description {got!r} is not the meta description {want!r}"]


def check_T005() -> list[str]:
    """FR-01: og-image.jpg is a 1200x630 JPEG card showing the name, rendered
    from og-image.html.

    A card is a picture of words. The first one made was a flat dark
    rectangle that passed a size-only check; a blank card is not a preview.
    So the card has a source a person can read (og-image.html, naming
    "Gabriel Ordonez"), and the JPEG must carry enough detail to be more
    than one colour: a flat 1200x630 JPEG is about 12 KB, a card with text
    about 40 KB. The size is read from the JPEG's own frame header.
    """
    src, f, problems = ROOT / "og-image.html", ROOT / "og-image.jpg", []
    if not src.exists():
        problems.append("og-image.html, the card's source, does not exist")
    else:
        card = src.read_text(encoding="utf-8").replace("&amp;", "&")
        home_title = Page("index.html").title
        tagline = home_title.split("|", 1)[-1].strip() if "|" in home_title else home_title
        for want in ("Gabriel Ordonez", tagline, "gabrielordonez.com"):
            if want not in card:
                problems.append(f"og-image.html does not carry {want!r}")
    if not f.exists():
        return problems + ["og-image.jpg does not exist at the repository root"]
    data = f.read_bytes()
    if data[:2] != b"\xff\xd8":
        return problems + ["og-image.jpg is not a JPEG"]
    if len(data) < 25_000:
        problems.append(f"og-image.jpg is {len(data)} bytes: too little detail to be a card with text")
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        if data[i + 1] in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", data[i + 5 : i + 9])
            if (w, h) != (1200, 630):
                problems.append(f"og-image.jpg is {w}x{h}, not 1200x630")
            return problems
        i += 2 + struct.unpack(">H", data[i + 2 : i + 4])[0]
    return problems + ["og-image.jpg has no frame header"]


def check_T006() -> list[str]:
    """FR-01 FR-07: index.html og:image is the shared image URL."""
    got = Page("index.html").meta.get("og:image")
    return [] if got == OG_IMAGE else [f"index.html og:image is {got!r}, not {OG_IMAGE!r}"]


def open_graph(rel: str) -> list[str]:
    """FR-09 FR-10 FR-11: the page's og:title equals its <title>, og:description
    its meta description, and og:image the shared image URL.

    Shared by check_T007, check_T008 and check_T009, one page each.
    """
    p, problems = Page(rel), []
    for prop, want in (
        ("og:title", p.title),
        ("og:description", p.meta.get("description")),
        ("og:image", OG_IMAGE),
    ):
        got = p.meta.get(prop)
        if got is None:
            problems.append(f"{rel} has no {prop}")
        elif got != want:
            problems.append(f"{rel} {prop} is {got!r}, not {want!r}")
    return problems


def check_T007() -> list[str]:
    """FR-09: blog.html carries og:title, og:description and og:image.

    og:title equals its <title>, og:description its meta description, og:image
    the shared image -- see open_graph() directly above.
    """
    return open_graph("blog.html")


def check_T008() -> list[str]:
    """FR-10: rag-project.html carries og:title, og:description and og:image,
    each equal to its <title>, its meta description and the shared image."""
    return open_graph("rag-project.html")


def check_T009() -> list[str]:
    """FR-11: blog/rag-latency.html carries og:title, og:description and
    og:image, each equal to its <title>, its meta description and the shared image."""
    return open_graph("blog/rag-latency.html")


def check_T010() -> list[str]:
    """FR-06: index.html JSON-LD has a Person and a WebSite, each with
    name "Gabriel Ordonez" and url "https://gabrielordonez.com/"."""
    blocks = Page("index.html").ld
    if not blocks:
        return ["index.html has no application/ld+json script"]
    nodes: list[dict] = []
    for b in blocks:
        try:
            v = json.loads(b)
        except json.JSONDecodeError as e:
            return [f"index.html JSON-LD does not parse: {e}"]
        items = v if isinstance(v, list) else v.get("@graph", [v]) if isinstance(v, dict) else []
        nodes += [n for n in items if isinstance(n, dict)]
    problems = []
    for kind in ("Person", "WebSite"):
        n = next((n for n in nodes if n.get("@type") == kind), None)
        if n is None:
            problems.append(f"no {kind} in index.html JSON-LD")
        elif n.get("name") != "Gabriel Ordonez" or n.get("url") != SITE:
            problems.append(f"{kind} is name={n.get('name')!r} url={n.get('url')!r}")
    return problems


FR05_PAGES = [
    "index.html",
    "blog.html",
    "rag-project.html",
    "blog/rag-latency.html",
    "blog/llm-trust.html",
    "blog/ai-theory-practice.html",
    "genai-search-project.html",
    "llm-eval-project.html",
]


def check_T011() -> list[str]:
    """FR-05: every listed page exists, has a <title>, and is tracked by git.

    GitHub Pages serves what is committed: a page on disk and not in git is a
    404 on the live site however right it looks here. `--live` also fetches
    each URL.
    """
    listed = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=False
    ).stdout.split()
    tracked, problems = set(listed), []
    for rel in FR05_PAGES:
        if not (ROOT / rel).exists():
            problems.append(f"{rel} does not exist")
        elif not Page(rel).title:
            problems.append(f"{rel} has no <title>")
        elif rel not in tracked:
            problems.append(f"{rel} is not tracked by git, so GitHub Pages will not serve it")
    return problems


def check_T012() -> list[str]:
    """FR-08: every assertion in this file holds against the source.

    The finish line: it fails while any other check fails, so it cannot be
    ticked before the work it certifies is done.
    """
    return [f"{tid} fails" for tid, f in CHECKS.items() if tid != "T012" and f()]


CHECKS = {name[len("check_"):]: f for name, f in sorted(globals().items()) if name.startswith("check_T")}


def live() -> list[str]:
    problems = []
    for rel in [""] + FR05_PAGES:
        try:
            with urllib.request.urlopen(SITE + rel, timeout=15) as r:
                if r.status != 200:
                    problems.append(f"{SITE + rel} answered {r.status}")
        except Exception as e:  # noqa: BLE001 -- any failure is the finding
            problems.append(f"{SITE + rel} failed: {e}")
    return problems


def ticked() -> set[str]:
    text = TASKS.read_text(encoding="utf-8")
    return set(re.findall(r"^\s*- \[[xX]\] (T\d+)\b", text, re.M))


def main(argv: list[str]) -> int:
    every, done, failed = "--all" in argv, ticked(), 0
    for tid, check in CHECKS.items():
        frs = (check.__doc__ or "").split(":")[0]
        problems = check()
        # The one line format the harness reads for any language (099): it
        # records each result per task, so a regression on one task locks the
        # repository to that task's files.
        print(f"test {tid} ... {'ok' if not problems else 'FAILED'}")
        if not problems:
            print(f"PASS     {tid} {frs}")
        elif tid in done or every:
            failed += 1
            print(f"FAIL     {tid} {frs}: " + "; ".join(problems))
        else:
            print(f"pending  {tid} {frs}: " + "; ".join(problems))
    if "--live" in argv:
        problems = live()
        failed += bool(problems)
        print(("FAIL     live FR-05: " + "; ".join(problems)) if problems else "PASS     live FR-05")
    unknown = sorted(done - set(CHECKS))
    if unknown:
        failed += 1
        print(f"FAIL     ticked with no check: {', '.join(unknown)}")
    print(f"{'red' if failed else 'green'}: {failed} failing, {len(done)} ticked of {len(CHECKS)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
