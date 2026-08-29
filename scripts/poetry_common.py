#!/usr/bin/env python3
"""Shared text normalization and SQLite search helpers."""

from __future__ import annotations

import sqlite3
import unicodedata
from pathlib import Path


def normalize_text(text: str) -> str:
    """Keep letters and numbers while removing punctuation and whitespace."""
    return "".join(
        char
        for char in text
        if not unicodedata.category(char).startswith(("P", "Z", "C"))
    )


def search_tokens(text: str) -> list[str]:
    normalized = normalize_text(text)
    bigrams = [normalized[index : index + 2] for index in range(len(normalized) - 1)]
    return list(dict.fromkeys(bigrams + list(normalized)))


def build_search_terms(*values: str) -> str:
    tokens: list[str] = []
    for value in values:
        tokens.extend(search_tokens(value))
    return " ".join(dict.fromkeys(tokens))


def make_fts_query(text: str, max_terms: int = 32) -> str:
    tokens = search_tokens(text)
    if not tokens:
        return ""
    bigrams = [token for token in tokens if len(token) == 2]
    selected = (bigrams or tokens)[:max_terms]
    return " OR ".join(f'"{token.replace(chr(34), chr(34) * 2)}"' for token in selected)


def connect_index(index_path: Path | str) -> sqlite3.Connection:
    path = Path(index_path)
    if not path.is_file():
        raise FileNotFoundError(f"Poetry index not found: {path}")
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def search_works(
    index_path: Path | str,
    query: str,
    limit: int = 8,
) -> list[dict[str, object]]:
    fts_query = make_fts_query(query)
    if not fts_query:
        return []

    with connect_index(index_path) as connection:
        rows = connection.execute(
            """
            SELECT
                w.id,
                w.source_file,
                w.source_kind,
                w.title,
                w.author,
                w.form,
                w.text,
                bm25(works_fts) AS score
            FROM works_fts
            JOIN works AS w ON w.id = works_fts.work_id
            WHERE works_fts MATCH ?
            ORDER BY score
            LIMIT ?
            """,
            (fts_query, limit),
        ).fetchall()
    return [dict(row) for row in rows]
