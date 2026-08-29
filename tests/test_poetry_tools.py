#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from build_poetry_index import build_index  # noqa: E402
from check_poem import analyze_poem  # noqa: E402
from poetry_common import search_works  # noqa: E402


class PoetryToolsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        collection = self.root / "全唐诗"
        collection.mkdir()
        records = [
            {
                "author": "测试者",
                "title": "潮港",
                "paragraphs": [
                    "暮港收残照，孤灯候远舟。",
                    "潮回空渡口，雁去满城秋。",
                ],
            },
            {
                "author": "测试者",
                "title": "山炉",
                "paragraphs": [
                    "石径通云舍，寒炉守旧书。",
                    "晨钟催客起，松影过前除。",
                ],
            },
        ]
        (collection / "sample.json").write_text(
            json.dumps(records, ensure_ascii=False), encoding="utf-8"
        )
        self.index = self.root / "poetry.sqlite"
        self.summary = build_index(self.root, self.index)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_build_and_retrieve(self) -> None:
        self.assertEqual(self.summary["records_written"], 2)
        results = search_works(self.index, "孤灯 远舟", limit=2)
        self.assertTrue(results)
        self.assertEqual(results[0]["title"], "潮港")

    def test_checker_finds_exact_phrase(self) -> None:
        result = analyze_poem(
            "暮港收残照\n新灯照客衣\n潮声催夜渡\n雁影过桥西",
            expected_chars=5,
            index_path=self.index,
        )
        self.assertTrue(result["strict_form_pass"])
        self.assertFalse(result["originality_check_pass"])
        self.assertEqual(result["suspicious_corpus_matches"][0]["overlap"], "暮港收残照")

    def test_checker_reports_line_length(self) -> None:
        result = analyze_poem("短句\n此句恰好五字吗", expected_chars=5)
        self.assertFalse(result["strict_form_pass"])
        self.assertFalse(result["corpus_check_ran"])


if __name__ == "__main__":
    unittest.main()
