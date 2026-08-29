#!/usr/bin/env python3
"""Retrieve classical-poetry references from a local SQLite index."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from poetry_common import search_works


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, required=True, help="SQLite index path")
    parser.add_argument("--query", required=True, help="Images, emotions, or scene terms")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results")
    parser.add_argument("--max-chars", type=int, default=180, help="Maximum excerpt length")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = search_works(args.index, args.query, max(1, args.top_k))
    prepared = []
    for result in results:
        text = str(result.pop("text"))
        result["excerpt"] = text[: args.max_chars]
        prepared.append(result)

    if args.json:
        print(json.dumps(prepared, ensure_ascii=False, indent=2))
        return

    if not prepared:
        print("No matching references found.")
        return

    for position, result in enumerate(prepared, start=1):
        heading = f"{position}. {result['title']} — {result['author']}"
        if result.get("form"):
            heading += f" ({result['form']})"
        print(heading)
        print(f"   source: {result['source_file']}")
        print(f"   excerpt: {result['excerpt'].replace(chr(10), ' / ')}")


if __name__ == "__main__":
    main()
