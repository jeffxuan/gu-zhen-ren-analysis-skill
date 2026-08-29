#!/usr/bin/env python3
"""Build a local SQLite search index from chinese-poetry-style JSON files."""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from poetry_common import build_search_terms, normalize_text


DEFAULT_COLLECTIONS = ("全唐诗", "宋词", "诗经", "五代诗词")
TEXT_KEYS = ("paragraphs", "content")


def clean_text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(item.strip() for item in value if isinstance(item, str) and item.strip())
    return ""


def iter_poetry_records(node: Any) -> Iterator[dict[str, Any]]:
    if isinstance(node, list):
        for item in node:
            yield from iter_poetry_records(item)
        return
    if not isinstance(node, dict):
        return

    if any(clean_text(node.get(key)) for key in TEXT_KEYS):
        yield node
        return

    for value in node.values():
        if isinstance(value, (dict, list)):
            yield from iter_poetry_records(value)


def record_text(record: dict[str, Any]) -> str:
    for key in TEXT_KEYS:
        text = clean_text(record.get(key))
        if text:
            return text
    return ""


def record_metadata(record: dict[str, Any]) -> tuple[str, str, str]:
    title = str(record.get("title") or record.get("rhythmic") or "Untitled").strip()
    author = str(record.get("author") or record.get("poet") or "Unknown").strip()
    form_parts = [record.get("rhythmic"), record.get("chapter"), record.get("section")]
    form = " / ".join(str(part).strip() for part in form_parts if part)
    return title, author, form


def initialize_database(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        PRAGMA journal_mode = OFF;
        PRAGMA synchronous = OFF;
        CREATE TABLE works (
            id INTEGER PRIMARY KEY,
            source_file TEXT NOT NULL,
            source_kind TEXT NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            form TEXT NOT NULL,
            text TEXT NOT NULL,
            normalized TEXT NOT NULL
        );
        CREATE UNIQUE INDEX works_source_file_idx ON works(source_file);
        CREATE VIRTUAL TABLE works_fts USING fts5(
            work_id UNINDEXED,
            title,
            author,
            search_terms,
            tokenize = 'unicode61 remove_diacritics 2'
        );
        CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        """
    )


def selected_json_files(source: Path, collections: list[str]) -> Iterator[Path]:
    found_collection = False
    for collection in collections:
        collection_path = source / collection
        if not collection_path.is_dir():
            continue
        found_collection = True
        yield from sorted(collection_path.rglob("*.json"))
    if not found_collection:
        raise FileNotFoundError(
            f"None of the selected collections exist under {source}: {', '.join(collections)}"
        )


def build_index(
    source: Path,
    output: Path,
    collections: list[str] | None = None,
    force: bool = False,
) -> dict[str, int]:
    source = source.resolve()
    output = output.resolve()
    selected = collections or list(DEFAULT_COLLECTIONS)

    if not source.is_dir():
        raise FileNotFoundError(f"Corpus directory not found: {source}")
    if output.exists() and not force:
        raise FileExistsError(f"Output already exists; pass --force to replace it: {output}")

    output.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(
        prefix=f".{output.name}.", suffix=".tmp", dir=output.parent
    )
    os.close(handle)
    temporary_path = Path(temporary_name)

    files_read = 0
    records_written = 0
    files_skipped = 0

    try:
        with sqlite3.connect(temporary_path) as connection:
            initialize_database(connection)
            for json_path in selected_json_files(source, selected):
                relative_path = json_path.relative_to(source)
                try:
                    payload = json.loads(json_path.read_text(encoding="utf-8"))
                except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                    files_skipped += 1
                    continue

                files_read += 1
                source_kind = relative_path.parts[0]
                for item_index, record in enumerate(iter_poetry_records(payload)):
                    text = record_text(record)
                    normalized = normalize_text(text)
                    if len(normalized) < 4:
                        continue
                    title, author, form = record_metadata(record)
                    source_file = f"{relative_path.as_posix()}#{item_index}"
                    cursor = connection.execute(
                        """
                        INSERT INTO works(
                            source_file, source_kind, title, author, form, text, normalized
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (source_file, source_kind, title, author, form, text, normalized),
                    )
                    work_id = cursor.lastrowid
                    connection.execute(
                        """
                        INSERT INTO works_fts(work_id, title, author, search_terms)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            work_id,
                            title,
                            author,
                            build_search_terms(title, author, form, text),
                        ),
                    )
                    records_written += 1

            connection.executemany(
                "INSERT INTO metadata(key, value) VALUES (?, ?)",
                (
                    ("format_version", "1"),
                    ("collections", json.dumps(selected, ensure_ascii=False)),
                    ("records", str(records_written)),
                ),
            )
            connection.commit()

        os.replace(temporary_path, output)
    finally:
        temporary_path.unlink(missing_ok=True)

    return {
        "files_read": files_read,
        "files_skipped": files_skipped,
        "records_written": records_written,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Path to a corpus checkout")
    parser.add_argument("--output", type=Path, required=True, help="SQLite index to create")
    parser.add_argument(
        "--include",
        action="append",
        dest="collections",
        help="Top-level collection to include; repeat as needed",
    )
    parser.add_argument("--force", action="store_true", help="Replace an existing index")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = build_index(args.source, args.output, args.collections, args.force)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
