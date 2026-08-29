#!/usr/bin/env python3
"""Check verse length, repetition, and suspicious overlap with a local corpus."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

from poetry_common import normalize_text, search_works


def split_lines(text: str) -> list[str]:
    lines = [line.strip().lstrip("> ") for line in text.splitlines() if line.strip()]
    if len(lines) <= 1:
        lines = [part.strip() for part in re.split(r"[。！？；]", text) if part.strip()]
    return lines


def repeated_ngrams(lines: list[str], size: int = 4) -> list[dict[str, object]]:
    locations: dict[str, set[int]] = defaultdict(set)
    for line_number, line in enumerate(lines, start=1):
        normalized = normalize_text(line)
        for index in range(len(normalized) - size + 1):
            locations[normalized[index : index + size]].add(line_number)
    return [
        {"phrase": phrase, "lines": sorted(line_numbers)}
        for phrase, line_numbers in sorted(locations.items())
        if len(line_numbers) > 1
    ]


def suspicious_matches(
    lines: list[str],
    index_path: Path | None,
    minimum_match: int = 5,
) -> list[dict[str, object]]:
    if index_path is None:
        return []

    flags: list[dict[str, object]] = []
    seen: set[tuple[int, int]] = set()
    for line_number, line in enumerate(lines, start=1):
        normalized_line = normalize_text(line)
        if not normalized_line:
            continue
        for candidate in search_works(index_path, line, limit=12):
            candidate_text = normalize_text(str(candidate["text"]))
            matcher = SequenceMatcher(None, normalized_line, candidate_text, autojunk=False)
            longest = matcher.find_longest_match()
            overlap = normalized_line[longest.a : longest.a + longest.size]
            coverage = longest.size / len(normalized_line)
            key = (line_number, int(candidate["id"]))
            if key in seen or (longest.size < minimum_match and coverage < 0.75):
                continue
            seen.add(key)
            flags.append(
                {
                    "line": line_number,
                    "overlap": overlap,
                    "overlap_chars": longest.size,
                    "line_coverage": round(coverage, 3),
                    "title": candidate["title"],
                    "author": candidate["author"],
                    "source_file": candidate["source_file"],
                }
            )
    return flags


def analyze_poem(
    text: str,
    expected_chars: int | None = None,
    index_path: Path | None = None,
    minimum_match: int = 5,
) -> dict[str, object]:
    lines = split_lines(text)
    lengths = [len(normalize_text(line)) for line in lines]
    length_issues = []
    if expected_chars is not None:
        length_issues = [
            {"line": index, "actual": length, "expected": expected_chars}
            for index, length in enumerate(lengths, start=1)
            if length != expected_chars
        ]

    overlap_flags = suspicious_matches(lines, index_path, minimum_match)
    return {
        "line_count": len(lines),
        "line_lengths": lengths,
        "line_endings": [normalize_text(line)[-1:] for line in lines],
        "length_issues": length_issues,
        "repeated_phrases": repeated_ngrams(lines),
        "corpus_check_ran": index_path is not None,
        "suspicious_corpus_matches": overlap_flags,
        "strict_form_pass": not length_issues,
        "originality_check_pass": not overlap_flags,
        "rhyme_note": "Line endings are reported for review; historical rhyme is not automatically validated.",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Poem text; separate lines with newlines")
    source.add_argument("--file", type=Path, help="UTF-8 text file containing the poem")
    parser.add_argument("--index", type=Path, help="Optional SQLite corpus index")
    parser.add_argument("--expected-chars", type=int, choices=(5, 7), help="Expected characters per line")
    parser.add_argument("--minimum-match", type=int, default=5, help="Flag corpus overlaps of this length")
    parser.add_argument("--strict", action="store_true", help="Exit nonzero when checks fail")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    text = args.text if args.text is not None else args.file.read_text(encoding="utf-8")
    result = analyze_poem(text, args.expected_chars, args.index, args.minimum_match)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.strict and (not result["strict_form_pass"] or not result["originality_check_pass"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
