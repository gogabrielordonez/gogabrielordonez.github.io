#!/usr/bin/env python3
# spec: 001-site-fixes-for-gabrielordonez-com
# spec: 002-age-proofing
"""Checks for specs/001-site-fixes-for-gabrielordonez-com, one per task.

Written from spec.md before the pages were changed, so a tick has something
to answer to. Each check is one function, `check_T###`, whose docstring names
the requirements it proves and whose body is the whole assertion.

    python3 tests/check_site.py          # fails for ticked tasks whose check fails
    python3 tests/check_site.py --all    # every task must pass (T012, the finish line)

Coquivacoa runs the default mode after every OpenCode session. A task ticked
in tasks.md whose check fails turns the run red, so a tick is a claim the
files have to back. Unticked tasks print as pending. Standard library only.
"""

from __future__ import annotations

import difflib
import json
import re
import struct
import subprocess
import sys
import unicodedata
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

    Done when: SC-03 SC-12.

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
    others = [n for n in ("index.htm", "index.md", "home.html", "default.html") if (ROOT / n).exists()]
    if others:
        problems.append(f"{others} could answer / instead of index.html")
    if p.refresh:
        problems.append("index.html redirects with meta refresh")
    return problems


def check_T002() -> list[str]:
    """FR-02 FR-04: index.html declares exactly one canonical, the site root.

    Done when: SC-02 SC-04.
    """
    c = Page("index.html").canonical
    return [] if c == [SITE] else [f"index.html canonical is {c or 'missing'}, not [{SITE}]"]


def check_T003() -> list[str]:
    """FR-01 FR-07: index.html og:title equals its <title>.

    Done when: SC-01 SC-07.
    """
    p = Page("index.html")
    got = p.meta.get("og:title")
    if got is None:
        return ["index.html has no og:title"]
    return [] if got == p.title else [f"og:title {got!r} is not <title> {p.title!r}"]


def check_T004() -> list[str]:
    """FR-01 FR-07: index.html og:description equals its meta description.

    Done when: SC-01 SC-07.
    """
    p = Page("index.html")
    got, want = p.meta.get("og:description"), p.meta.get("description")
    if got is None:
        return ["index.html has no og:description"]
    return [] if got == want else [f"og:description {got!r} is not the meta description {want!r}"]


def check_T005() -> list[str]:
    """FR-01: og-image.jpg is a 1200x630 JPEG card showing the name, rendered

    Done when: SC-01.
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
    """FR-01 FR-07: index.html og:image is the shared image URL.

    Done when: SC-01 SC-07.
    """
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

    Done when: SC-09.

    og:title equals its <title>, og:description its meta description, og:image
    the shared image -- see open_graph() directly above.
    """
    return open_graph("blog.html")


def check_T008() -> list[str]:
    """FR-10: rag-project.html carries og:title, og:description and og:image,

    Done when: SC-10.
    each equal to its <title>, its meta description and the shared image."""
    return open_graph("rag-project.html")


def check_T009() -> list[str]:
    """FR-11: blog/rag-latency.html carries og:title, og:description and

    Done when: SC-11.
    og:image, each equal to its <title>, its meta description and the shared image."""
    return open_graph("blog/rag-latency.html")


def check_T010() -> list[str]:
    """FR-06: index.html JSON-LD has a Person and a WebSite, each with

    Done when: SC-06.
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
    "genai-search-project.html",
    "llm-eval-project.html",
]


def check_T011() -> list[str]:
    """FR-05: every listed page exists, has a <title>, and is tracked by git.

    Done when: SC-05.

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

    Done when: SC-08.

    The finish line: it fails while any other check fails, so it cannot be
    ticked before the work it certifies is done.
    """
    return [f"{tid} fails" for tid, f in CHECKS.items() if tid not in ("T012", "T013") and f()]




def live() -> list[str] | None:
    """The published pages, fetched: each must answer 200 with a page that
    has a <title>. None only when nothing on the internet answers -- that is
    this machine offline, not the site failing. If another host answers and
    the site does not, the site is down, and that is a failure."""
    problems, errors = [], []
    for rel in [""] + FR05_PAGES:
        # Named, not Python's default: Cloudflare in front of the site
        # refuses "Python-urllib" (403) while every crawler that renders a
        # preview -- Google, LinkedIn, X, Facebook, Slack -- gets 200.
        req = urllib.request.Request(SITE + rel, headers={"User-Agent": "gabrielordonez-site-check/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                body = r.read(200_000).decode("utf-8", "replace")
                if r.status != 200:
                    problems.append(f"{SITE + rel} answered {r.status}")
                elif not re.search(r"<title>\s*\S", body, re.I):
                    problems.append(f"{SITE + rel} answered 200 with no page")
        except urllib.error.HTTPError as e:
            problems.append(f"{SITE + rel} answered {e.code}")
        except Exception as e:  # noqa: BLE001 -- no answer from this URL
            errors.append(f"{SITE + rel} did not answer: {e}")
    if errors and not problems and len(errors) == len(FR05_PAGES) + 1:
        # Nothing on the site answered. Offline, or the site is down?
        try:
            urllib.request.urlopen(urllib.request.Request(
                "https://www.github.com/", headers={"User-Agent": "gabrielordonez-site-check/1.0"}), timeout=10)
        except Exception:  # noqa: BLE001
            return None
    return problems + errors


def check_T013() -> list[str] | None:
    """FR-05: every published FR-05 URL answers HTTP 200.

    Done when: SC-05.
    Fetched on every run, with a named client. Offline it returns None: the
    check did not run, which is not the same as the site failing.
    """
    return live()


CHECKS = {name[len("check_"):]: f for name, f in sorted(globals().items()) if name.startswith("check_T")}


# --- spec 002-age-proofing: checks on index.html, one per success criterion ---
# Named age_*, not check_T###, so they stay out of CHECKS and spec 001's
# finish line (T012) is not turned red by them.

TASKS2 = ROOT / "specs" / "002-age-proofing" / "tasks.md"
BASELINE = "8e70efe"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
YEAR = re.compile(r"\b\d{4}\b")


class Node:
    def __init__(self, tag: str, start: int):
        self.tag, self.start, self.end = tag, start, start
        self.kids: list = []

    @property
    def text(self) -> str:
        parts = [k if isinstance(k, str) else k.text for k in self.kids]
        return unicodedata.normalize("NFC", " ".join(" ".join(parts).split()))


class Tree(HTMLParser):
    """index.html as nested elements, each knowing its first and last line."""

    def __init__(self, source: str):
        super().__init__()
        self.root = Node("#root", 1)
        self.stack = [self.root]
        self.feed(source)
        self.close()
        self.root.end = source.count("\n") + 1

    def handle_starttag(self, tag, attrs):
        n = Node(tag, self.getpos()[0])
        self.stack[-1].kids.append(n)
        if tag not in VOID:
            self.stack.append(n)

    def handle_endtag(self, tag):
        if any(n.tag == tag for n in self.stack[1:]):
            while True:
                n = self.stack.pop()
                n.end = self.getpos()[0]
                if n.tag == tag:
                    break

    def handle_data(self, data):
        self.stack[-1].kids.append(data)


def path_to(node: Node, needle: str) -> list[Node]:
    """Root-to-deepest chain of elements whose text contains `needle`."""
    chain = [node]
    while True:
        nxt = next((k for k in chain[-1].kids if isinstance(k, Node) and re.search(needle, k.text)), None)
        if nxt is None:
            return chain if re.search(needle, node.text) else []
        chain.append(nxt)


def grow(chain: list[Node], stop) -> Node:
    """The largest element on the chain that `stop` does not reject."""
    best = chain[-1]
    for anc in reversed(chain[:-1]):
        if anc.tag in ("body", "html", "#root") or stop(anc.text):
            break
        best = anc
    return best


def education_entry(root: Node, inst: str, other: str) -> Node | None:
    chain = path_to(root, re.escape(inst))
    return grow(chain, lambda t: other in t or "Bachelor" in t) if chain else None


def earlier_item(root: Node) -> Node | None:
    """The item headed 'Earlier Career': grown until it would take in a dated item."""
    chain = path_to(root, r"Earlier Career")
    return grow(chain, lambda t: re.search(r"\b(19|20)\d\d\b", t)) if chain else None


def old_item(root: Node) -> Node | None:
    """The baseline's '2003 – 2013' item: grown until it would take in another year."""
    rng = r"2003\s*[–-]\s*2013"
    chain = path_to(root, rng)
    return grow(chain, lambda t: re.search(r"\b(19|20)\d\d\b", re.sub(rng, "", t))) if chain else None


def index_html() -> str:
    return (ROOT / "index.html").read_text(encoding="utf-8")


def age_SC001() -> list[str]:
    """FR-001 SC-001: neither the Barcelona nor the Canada West Education entry
    in index.html carries a four-digit year; both still name degree and institution."""
    root, problems = Tree(index_html()).root, []
    for inst, other, degree in (
        ("University of Barcelona", "University Canada West", r"\bM\.?S\.?c?\b|Master"),
        ("University Canada West", "University of Barcelona", r"\bMBA\b|Master of Business"),
    ):
        e = education_entry(root, inst, other)
        if e is None:
            problems.append(f"index.html has no Education entry naming {inst}")
            continue
        if not re.search(degree, e.text):
            problems.append(f"the {inst} entry no longer names its degree: {e.text!r}")
        if YEAR.search(e.text):
            problems.append(f"the {inst} entry still carries a year: {e.text!r}")
    return problems


def age_SC002() -> list[str]:
    """FR-002 FR-003 FR-005 SC-002: index.html has no 2003; an undated item headed
    Earlier Career names Ericsson, MSI Americas, Telefónica and both resume roles;
    the leftover developer comment is gone."""
    src, problems = index_html(), []
    if "2003" in src:
        problems.append("index.html still contains 2003")
    for part in ("Nokia/Ericsson/MSI", "Grouped for brevity", "I'll include Nokia"):
        if part in src:
            problems.append(f"part of the leftover developer comment ({part!r}) is still in index.html")
    if any("Nokia" in c for c in re.findall(r"<!--.*?-->", src, re.S)):
        problems.append("an HTML comment naming Nokia is still in index.html")
    root = Tree(src).root
    item = earlier_item(root)
    if item is None:
        return problems + ["index.html has no item headed Earlier Career"]
    if not any(isinstance(k, str) and k.strip() == "Earlier Career" for n in [item, *_walk(item)] for k in n.kids):
        problems.append("no element of the item has Earlier Career as its whole heading text")
    t = item.text.replace("&amp;", "&")
    if YEAR.search(t):
        problems.append(f"the Earlier Career item carries a year: {t!r}")
    for want in ("Ericsson", "MSI Americas", "Telefónica", "Solutions Architect & Project Lead", "RF Engineering"):
        if unicodedata.normalize("NFC", want) not in t:
            problems.append(f"the Earlier Career item does not name {want!r}")
    return problems


def _walk(node: Node):
    for k in node.kids:
        if isinstance(k, Node):
            yield k
            yield from _walk(k)


def age_SC003() -> list[str]:
    """FR-004 FR-005 SC-003: outside the Barcelona and Canada West Education entries,
    the Earlier Career item and the removed comment, index.html equals index.html at
    8e70efe (blank lines and trailing spaces aside)."""
    shown = subprocess.run(
        ["git", "show", f"{BASELINE}:index.html"], cwd=ROOT, capture_output=True, text=True, check=False
    )
    if shown.returncode:
        return [f"cannot read index.html at {BASELINE}: {shown.stderr.strip()}"]
    base_src = shown.stdout
    base_root = Tree(base_src).root
    lines = base_src.splitlines()
    allowed: set[int] = set()  # 1-based baseline lines
    problems = []
    for inst, other in (("University of Barcelona", "University Canada West"), ("University Canada West", "University of Barcelona")):
        e = education_entry(base_root, inst, other)
        if e:
            allowed |= set(range(e.start, e.end + 1))
        else:
            problems.append(f"baseline has no Education entry naming {inst}")
    old = old_item(base_root)
    if old:
        allowed |= set(range(old.start, old.end + 1))
    else:
        problems.append("baseline has no 2003 – 2013 item")
    hit = next((i for i, l in enumerate(lines, 1) if "I'll include Nokia" in l), None)
    if hit:
        a = max(i for i in range(1, hit + 1) if "<!--" in lines[i - 1])
        b = min(i for i in range(hit, len(lines) + 1) if "-->" in lines[i - 1])
        # FR-005 is the whole run of comments, e.g. a one-line comment right above
        # the multi-line one: take every directly preceding one-line comment too.
        while a > 1 and (not lines[a - 2].strip() or re.fullmatch(r"\s*<!--.*-->\s*", lines[a - 2])):
            a -= 1
        allowed |= set(range(a, b + 1))
    else:
        problems.append("baseline has no leftover developer comment")
    if problems:
        return problems

    def kept(src_lines):
        return [(n, l.rstrip()) for n, l in enumerate(src_lines, 1) if l.strip()]

    base, now = kept(lines), kept(index_html().splitlines())
    sm = difflib.SequenceMatcher(None, [t for _, t in base], [t for _, t in now], autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        if i1 == i2:  # pure insertion: must sit beside an allowed line
            near = {base[i1 - 1][0]} if i1 else set()
            near |= {base[i1][0]} if i1 < len(base) else set()
            if not near & allowed:
                problems.append(f"lines added outside the allowed places after baseline line {sorted(near)}: {now[j1][1].strip()[:80]!r}")
        else:
            bad = [n for n, _ in base[i1:i2] if n not in allowed]
            if bad:
                problems.append(f"baseline line {bad[0]} changed outside the allowed places: {lines[bad[0] - 1].strip()[:80]!r}")
    return problems


AGE_CHECKS = {"SC-001": age_SC001, "SC-002": age_SC002, "SC-003": age_SC003}


def age_ticked() -> bool:
    """Spec 002's T002 (the edit) is ticked: from then the checks are a claim to back."""
    try:
        return bool(re.search(r"^\s*- \[[xX]\] T002\b", TASKS2.read_text(encoding="utf-8"), re.M))
    except OSError:
        return False


def ticked() -> set[str]:
    text = TASKS.read_text(encoding="utf-8")
    return set(re.findall(r"^\s*- \[[xX]\] (T\d+)\b", text, re.M))


def main(argv: list[str]) -> int:
    every, done, failed = "--all" in argv, ticked(), 0
    for tid, check in CHECKS.items():
        frs = (check.__doc__ or "").split(":")[0]
        problems = check()
        if problems is None:
            # Could not run (offline). No result line: not run is not red.
            print(f"not run  {tid} {frs}: the network could not be reached")
            continue
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
    claimed = every or age_ticked()
    for sid, check in AGE_CHECKS.items():
        problems = check()
        print(f"test {sid} ... {'ok' if not problems else 'FAILED'}")
        if not problems:
            print(f"PASS     {sid}")
        elif claimed:
            failed += 1
            print(f"FAIL     {sid} (spec 002): " + "; ".join(problems))
        else:
            print(f"pending  {sid} (spec 002): " + "; ".join(problems))
    unknown = sorted(done - set(CHECKS))
    if unknown:
        failed += 1
        print(f"FAIL     ticked with no check: {', '.join(unknown)}")
    print(f"{'red' if failed else 'green'}: {failed} failing, {len(done)} ticked of {len(CHECKS)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
