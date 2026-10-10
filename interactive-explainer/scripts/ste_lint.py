"""Lint the visible text of a rendered explainer page against the ASD-STE100 rules a machine can see."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

DESCRIPTIVE_MAX = 25

SKIP_TAGS = {"script", "style", "code", "title", "small", "head"}
SKIP_CLASSES = {"mono", "file", "eyebrow"}
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr",
             "path", "circle", "rect", "line", "marker"}
BLOCK_TAGS = {"p", "li", "td", "th", "h1", "h2", "h3", "h4", "summary", "button", "div", "text", "b", "span", "dt", "dd"}

UNAPPROVED = {
    "create": "make", "creates": "makes", "ensure": "make sure", "ensures": "makes sure",
    "verify": "make sure / examine", "verifies": "examines", "inspect": "examine",
    "get": "receive", "gets": "receives", "got": "received", "obtain": "receive",
    "launch": "start", "utilize": "use", "leverage": "use", "employ": "use",
    "display": "show", "displays": "shows", "indicate": "show", "indicates": "shows",
    "need": "necessary / must", "needs": "must have", "needed": "necessary",
    "require": "must have", "requires": "must have", "fail": "an error occurs",
    "fails": "an error occurs", "failed": "was not satisfactory", "retain": "keep",
    "revert": "put back", "proceed": "continue", "resume": "continue",
    "approximately": "about", "via": "through", "e.g.": "for example", "i.e.": "that is",
}
PHRASAL = re.compile(
    r"\b(set(?:s)? up|roll(?:s|ed)? out|check(?:s|ed)? out|carr(?:y|ies|ied) on|kick(?:s|ed)? off|"
    r"find(?:s)? out|look(?:s|ed)? up|pick(?:s|ed)? up|shut(?:s)? down|tear(?:s)? down|figure(?:s|d)? out|"
    r"spin(?:s)? up|back(?:s|ed)? up|hand(?:s|ed)? off)\b",
    re.I,
)
CONTRACTION = re.compile(r"\b\w+(?:n't|'re|'ll|'ve|'d|'m)\b|\b(?:it|that|there|what|who|here)'s\b", re.I)
ING_ALLOWED = {"string", "strings", "thing", "things", "nothing", "something", "anything", "everything",
               "during", "ring", "spring", "bring", "king", "ceiling", "morning", "evening"}


@dataclass
class Finding:
    rule: str
    detail: str
    sentence: str


@dataclass
class TextCollector(HTMLParser):
    blocks: list[str] = field(default_factory=list)
    _stack: list[bool] = field(default_factory=list)
    _buf: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__init__(convert_charrefs=True)

    def _skipping(self) -> bool:
        return any(self._stack)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._flush_if_block(tag)
        if tag in VOID_TAGS:
            return
        classes = set((dict(attrs).get("class") or "").split())
        self._stack.append(tag in SKIP_TAGS or bool(classes & SKIP_CLASSES))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._flush_if_block(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID_TAGS:
            return
        if self._stack:
            self._stack.pop()
        self._flush_if_block(tag)

    def handle_data(self, data: str) -> None:
        if not self._skipping():
            self._buf.append(data)

    def _flush_if_block(self, tag: str) -> None:
        if tag in BLOCK_TAGS or tag in SKIP_TAGS:
            text = " ".join("".join(self._buf).split())
            if text:
                self.blocks.append(text)
            self._buf = []


def sentences(block: str) -> list[str]:
    """Split one block of text into sentences on terminal punctuation."""
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"“])", block) if s.strip()]


def plain_words(sentence: str) -> list[str]:
    """Words a reader counts; tokens carrying path or code characters are names and count once."""
    return [w for w in sentence.split() if re.search(r"[A-Za-z0-9]", w)]


def lint_sentence(s: str, allowed: set[str]) -> list[Finding]:
    found: list[Finding] = []
    words = plain_words(s)
    if len(words) > DESCRIPTIVE_MAX:
        found.append(Finding("length", f"{len(words)} words (descriptive max {DESCRIPTIVE_MAX}, procedural 20)", s))
    for m in CONTRACTION.finditer(s):
        found.append(Finding("contraction", m.group(0), s))
    for m in PHRASAL.finditer(s):
        found.append(Finding("phrasal verb", m.group(0), s))
    if re.search(r"[—–]|\s--\s", s):
        found.append(Finding("dash", "em or en dash", s))
    for raw in s.split():
        if re.search(r"[-_/.:<>=@#`]", raw.strip(".,;:!?()\"“”")):
            continue
        w = raw.strip(".,;:!?()\"“”").lower()
        if w in allowed:
            continue
        if w in UNAPPROVED:
            found.append(Finding("word", f"{w} -> {UNAPPROVED[w]}", s))
        elif w.endswith("ing") and len(w) > 4 and w not in ING_ALLOWED and raw[:1].islower():
            found.append(Finding("-ing", f"{w} (allowed only as a technical noun)", s))
    return found


def main(path: str, allowed: set[str]) -> int:
    collector = TextCollector()
    collector.feed(Path(path).read_text(encoding="utf-8"))
    findings = [f for block in collector.blocks for s in sentences(block) for f in lint_sentence(s, allowed)]
    seen: set[tuple[str, str, str]] = set()
    unique = [f for f in findings if (k := (f.rule, f.detail, f.sentence)) not in seen and not seen.add(k)]
    for f in unique:
        print(f"[{f.rule}] {f.detail}\n    {f.sentence[:160]}")
    print(f"ste lint: {len(unique)} finding(s) in {path}")
    return 1 if unique else 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page", help="the rendered page, from Chrome --dump-dom")
    parser.add_argument("--allow", default="", help="comma-separated words confirmed as technical nouns or verbs")
    args = parser.parse_args()
    sys.exit(main(args.page, {w.strip().lower() for w in args.allow.split(",") if w.strip()}))
