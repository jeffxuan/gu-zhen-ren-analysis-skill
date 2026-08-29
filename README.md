# Strategic Fantasy Writing

[English](README.md) | [简体中文](README.zh-CN.md)

A Codex skill for strategic narrative analysis, original progression-fantasy design, outline stress testing, and story-grounded classical-style Chinese poetry.

The project began as a high-level structural study of a user-supplied *Gu Zhen Ren* EPUB. It contains no novel text, model weights, or training corpus. It does not imitate the source's author, prose, or poetry.

本项目可以用中文分析策略型长篇叙事、设计原创人物与势力、检查剧情因果，并根据原创人物弧线生成古风叙事诗。

## Capabilities

- Analyze decisions through objectives, resources, rules, information, trade-offs, and persistent consequences.
- Design original settings, factions, conflict chains, and 12-chapter opening arcs.
- Score outlines with a 20-point narrative stress test.
- Generate character- and scene-specific original 古风叙事诗.
- Build a local SQLite index from a separately obtained `chinese-poetry` checkout.
- Retrieve relevant classical references and check draft poems for line length and suspicious phrase overlap.

## Install

```bash
git clone https://github.com/jeffxuan/strategic-fantasy-writing.git \
  ~/.codex/skills/strategic-fantasy-writing
```

Restart Codex after installation.

## Quick Use

```text
Use $strategic-fantasy-writing to analyze this original chapter.
Explain objectives, constraints, information gaps, costs, and persistent consequences,
then score it with the narrative stress test.
```

```text
Use $strategic-fantasy-writing to write an original seven-character, four-line
classical-style Chinese poem for this character.
Character arc: ...
Turning point: ...
Scene placement: chapter ending
Required image: 残灯
Avoid: 剑、血、天命
```

## Optional Poetry Index

The repository does not redistribute the external poetry corpus. Obtain it separately, review its data provenance, then build a local index:

```bash
git clone https://github.com/chinese-poetry/chinese-poetry.git /path/to/chinese-poetry
python3 scripts/build_poetry_index.py \
  --source /path/to/chinese-poetry \
  --output /path/to/poetry.sqlite
```

Search references and check a draft:

```bash
python3 scripts/retrieve_poems.py \
  --index /path/to/poetry.sqlite \
  --query '少年 远行 春光 酒' \
  --top-k 5

python3 scripts/check_poem.py \
  --index /path/to/poetry.sqlite \
  --text $'第一句\n第二句\n第三句\n第四句' \
  --expected-chars 7
```

See `references/DATA-MANIFEST.md` before corpus use and `references/CLASSICAL-POETRY-MODULE.md` for the complete workflow.

## Boundaries

- This is a knowledge-and-tool skill, not a pretrained poetry model.
- It does not provide continuation or imitation of a specific modern author or work.
- Source-grounded claims beyond the included provenance anchors require user-supplied source text.
- The `chinese-poetry` repository is MIT-licensed at the repository level, while its README says the underlying data came from the internet. Review data rights before training or redistribution.
- Fictional strategy analysis must not become real-world operational advice for deception, coercion, violence, or illegal conduct.

## Project Layout

```text
SKILL.md                    Skill entrypoint and task router
agents/openai.yaml          Codex UI metadata
references/                Mode-specific guidance and provenance
scripts/                   Poetry indexing, retrieval, and checking tools
tests/                     Deterministic tool tests
```

## License

New documentation and code in this repository use the [MIT License](LICENSE). External works and datasets remain subject to their own rights and licenses.
