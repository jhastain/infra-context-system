#!/usr/bin/env python3
"""Check this context tree against its own conventions.

The original system enforced every rule in CONTRIBUTING.md by human PR review and
nothing else, which is exactly why several files had drifted from the template.
A convention nothing checks is a convention nothing follows.

    python bin/e2e.py

Exit code 0 only if every check passed.
"""
from __future__ import annotations

import re
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PASS: list[tuple[str, str]] = []
FAIL: list[tuple[str, str, str]] = []
SKIP: list[tuple[str, str]] = []

FENCE = re.compile(r"^\s*```")
H2 = re.compile(r"^##\s+(.*\S)\s*$")
H1 = re.compile(r"^#\s+(.*\S)\s*$")
REVIEWED = re.compile(r"^##\s+Last Reviewed:\s*(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

# The pattern template, in order. A pattern file may omit sections it does not
# need, but may not reorder them: an agent skims by position.
PATTERN_ORDER = [
    "When to Use",
    "Standard Structure",
    "Configuration",
    "Code Patterns",
    "Infrastructure (Terraform/Terragrunt)",
    "Pipeline Integration",
    "Local Development",
    "Checklist",
    "Related Patterns",
]

HOLISTIC = {
    "patterns/ado-pipeline.md",
    "patterns/bash.md",
    "patterns/cloud-function.md",
    "patterns/dotnet-service.md",
    "patterns/powershell.md",
}


# Binary files cannot be grepped, so each one listed here has been opened
# and looked at. Adding a path to this list asserts that someone did.
REVIEWED_BINARIES = [
]

class _Skip(Exception):
    pass


def check(name):
    def wrap(fn):
        try:
            detail = fn()
        except _Skip as exc:
            SKIP.append((name, str(exc)))
        except Exception as exc:  # noqa: BLE001 - the harness reports, never crashes
            FAIL.append((name, f"{type(exc).__name__}: {exc}", traceback.format_exc()))
        else:
            PASS.append((name, detail or ""))
        return fn
    return wrap


def md_files() -> list[Path]:
    return sorted(
        p for p in ROOT.rglob("*.md")
        if ".git" not in p.parts and p.name != "CONTRIBUTING.md"
    )


def headings(text: str) -> list[str]:
    out, in_fence = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = H2.match(line)
        if m:
            out.append(m.group(1))
    return out


# --------------------------------------------------------------------------
# Structure
# --------------------------------------------------------------------------

@check("every markdown file has exactly one H1")
def _single_h1():
    bad = []
    for p in md_files():
        in_fence = False
        n = 0
        for line in p.read_text(encoding="utf-8").splitlines():
            if FENCE.match(line):
                in_fence = not in_fence
                continue
            if not in_fence and H1.match(line):
                n += 1
        if n != 1:
            bad.append(f"{p.relative_to(ROOT)} has {n}")
    assert not bad, f"files without exactly one H1: {bad}"
    return f"{len(md_files())} files"


@check("every file carries a Last Reviewed date")
def _reviewed():
    missing = [
        str(p.relative_to(ROOT)) for p in md_files()
        # The L3 template keeps a YYYY-MM-DD placeholder until it is filled in.
        if p.name not in {"README.md", "standards-template.md"}
        and not REVIEWED.search(p.read_text(encoding="utf-8"))
    ]
    assert not missing, (
        f"an undated fact is indistinguishable from a current one: {missing}"
    )
    return f"{len(md_files()) - 1} dated files"


@check("Last Reviewed is the final section in every file")
def _reviewed_last():
    bad = []
    for p in md_files():
        if p.name in {"README.md", "standards-template.md"}:
            continue
        hs = headings(p.read_text(encoding="utf-8"))
        if not hs or not hs[-1].startswith("Last Reviewed"):
            bad.append(f"{p.relative_to(ROOT)} ends with {hs[-1] if hs else 'no H2'!r}")
    assert not bad, f"Last Reviewed must be last: {bad}"
    return "all files end with Last Reviewed"


@check("every directory with more than one file has an index")
def _indexes():
    missing = []
    for d in sorted({p.parent for p in md_files()}):
        if d == ROOT:
            continue
        files = [p for p in d.glob("*.md")]
        if len(files) > 1 and not (d / "_index.md").exists():
            # A directory of sibling patterns is indexed by patterns/_index.md.
            if d.is_relative_to(ROOT / "patterns"):
                continue
            missing.append(str(d.relative_to(ROOT)))
    assert not missing, f"directories needing an _index.md: {missing}"
    return "indexes present where required"


# --------------------------------------------------------------------------
# The pattern template
# --------------------------------------------------------------------------

@check("decomposed pattern files follow the template order")
def _pattern_order():
    bad = []
    checked = 0
    for p in sorted((ROOT / "patterns").rglob("*.md")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.endswith("_index.md") or rel in HOLISTIC:
            continue
        checked += 1
        hs = [h for h in headings(p.read_text(encoding="utf-8"))
              if not h.startswith("Last Reviewed")]
        known = [h for h in hs if h in PATTERN_ORDER]
        positions = [PATTERN_ORDER.index(h) for h in known]
        if positions != sorted(positions):
            bad.append(f"{rel}: {known}")
        if known and known[0] != "When to Use":
            bad.append(f"{rel}: starts with {known[0]!r}, not 'When to Use'")
    assert not bad, "pattern sections out of template order:\n  " + "\n  ".join(bad)
    return f"{checked} decomposed patterns in order"


@check("every decomposed pattern states when to use it")
def _when_to_use():
    missing = []
    for p in sorted((ROOT / "patterns").rglob("*.md")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.endswith("_index.md") or rel in HOLISTIC:
            continue
        if "When to Use" not in headings(p.read_text(encoding="utf-8")):
            missing.append(rel)
    assert not missing, (
        f"without scope, an agent applies a pattern where it does not belong: {missing}"
    )
    return "all decomposed patterns scoped"


# --------------------------------------------------------------------------
# Links and the tree
# --------------------------------------------------------------------------

@check("every relative link resolves")
def _links():
    broken = []
    for p in md_files():
        for target in LINK.findall(p.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            path = (p.parent / target.split("#")[0]).resolve()
            if not path.exists():
                broken.append(f"{p.relative_to(ROOT)} -> {target}")
    assert not broken, "broken relative links:\n  " + "\n  ".join(sorted(set(broken)))
    return "no broken relative links"


@check("the README tree matches what is on disk")
def _readme_tree():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for d in ("domains/", "systems/", "patterns/", "templates/", "examples/"):
        assert d in readme, f"README does not mention {d}"
    # The counts the README claims must be true.
    for directory, pattern in (("domains", r"domains/\s+(\d+) files"),
                               ("systems", r"systems/\s+(\d+) files"),
                               ("patterns", r"patterns/\s+(\d+) files")):
        m = re.search(pattern, readme)
        if not m:
            continue
        claimed = int(m.group(1))
        actual = len(list((ROOT / directory).rglob("*.md")))
        assert claimed == actual, (
            f"README says {directory}/ has {claimed} files; it has {actual}"
        )
    return "tree and counts match"


# --------------------------------------------------------------------------
# Routing
# --------------------------------------------------------------------------

@check("every routing-table target exists")
def _routing_targets():
    text = (ROOT / "system-overview.md").read_text(encoding="utf-8")
    targets = re.findall(r"`((?:patterns|domains|systems)/[A-Za-z0-9_./-]+\.md)`", text)
    assert targets, "no routing targets found in system-overview.md"
    missing = sorted({t for t in targets if not (ROOT / t).exists()})
    assert not missing, (
        f"the routing table points at files that do not exist, so the agent silently "
        f"loads nothing: {missing}"
    )
    return f"{len(set(targets))} distinct targets, all present"


@check("every pattern is reachable from the routing table or an index")
def _reachable():
    overview = (ROOT / "system-overview.md").read_text(encoding="utf-8")
    index = (ROOT / "patterns" / "_index.md").read_text(encoding="utf-8")
    unreachable = []
    for p in sorted((ROOT / "patterns").rglob("*.md")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.endswith("_index.md"):
            continue
        if rel in overview or p.stem in index:
            continue
        unreachable.append(rel)
    assert not unreachable, (
        f"a pattern nothing routes to will never be loaded: {unreachable}"
    )
    return "every pattern is routed to or indexed"


# --------------------------------------------------------------------------
# Publication hygiene
# --------------------------------------------------------------------------


@check("the skeleton is empty on purpose, and says so")
def _skeleton_marked():
    unmarked = []
    for p in md_files():
        if p.name == "README.md":
            continue
        text = p.read_text(encoding="utf-8")
        if "Skeleton" not in text and "<!--" not in text:
            unmarked.append(str(p.relative_to(ROOT)))
    assert not unmarked, (
        f"a file with neither a skeleton note nor guidance comments reads as real "
        f"content that happens to be blank: {unmarked}"
    )
    return f"{len(md_files()) - 1} files marked or commented"


# --------------------------------------------------------------------------
# Not covered here
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Pre-publication leak gate (shared; see bin/leakcheck.py)
# --------------------------------------------------------------------------

@check("no employer identifiers in the working tree")
def _leak_tree():
    sys.path.insert(0, str(ROOT / "bin"))
    import leakcheck

    hits = leakcheck.scan_tree(ROOT, self_path=Path(leakcheck.__file__))
    assert not hits, "\n  " + "\n  ".join(hits[:12])
    return "clean, lockfiles included"


@check("no employer identifiers anywhere in git history")
def _leak_history():
    sys.path.insert(0, str(ROOT / "bin"))
    import leakcheck

    if not (ROOT / ".git").exists():
        raise _Skip("not a git repository")
    hits = leakcheck.scan_history(ROOT)
    assert not hits, (
        "a fresh history is only clean if nothing was committed and then removed:\n  "
        + "\n  ".join(hits[:12])
    )
    return "clean across all commits"


@check("every binary file has been reviewed by eye")
def _binaries():
    sys.path.insert(0, str(ROOT / "bin"))
    import leakcheck

    found = set(leakcheck.binaries(ROOT))
    allowed = set(REVIEWED_BINARIES)
    unreviewed = sorted(found - allowed)
    stale = sorted(allowed - found)
    assert not unreviewed, (
        f"these cannot be grepped and are not on the reviewed list, so nobody has "
        f"confirmed what they show: {unreviewed}"
    )
    assert not stale, f"REVIEWED_BINARIES lists files that no longer exist: {stale}"
    return f"{len(found)} binaries, all reviewed"


UNCOVERED = [
    ("Whether the content is correct", "there is no content; that is the point of a skeleton"),
    ("The routing eval itself", "examples/cross-layer-test-prompt.md needs an agent and a tool loop"),
    ("Token-budget claims", "measuring them needs a tokenizer and real filled-in content"),
    ("Wiki links", "they point at an internal wiki that does not exist here"),
    ("Staleness policy", "every file is stamped 1970-01-01 so a freshness check flags them all"),
]


def main() -> int:
    for name, reason in UNCOVERED:
        SKIP.append((name, reason))

    width = max(len(n) for n, *_ in PASS + FAIL + SKIP)
    for name, detail in PASS:
        print(f"PASS  {name:<{width}}  {detail}")
    for name, reason in SKIP:
        print(f"SKIP  {name:<{width}}  {reason}")
    for name, msg, tb in FAIL:
        print(f"FAIL  {name:<{width}}  {msg}")
        print("".join("        " + line for line in tb.splitlines(keepends=True)))

    print(f"\n{len(PASS)} passed, {len(FAIL)} failed, {len(SKIP)} skipped")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
