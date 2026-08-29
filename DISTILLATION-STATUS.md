# Distillation Status

## Completed: Third-pass framework

`SKILL.md` is a neutral, reusable analysis skill built from the supplied EPUB's observable structural patterns. It is suitable for:

- studying why a progression-fantasy plot moves;
- annotating scenes by incentives, resources, institutions, and information;
- outlining an original story with comparable strategic depth but a distinct setting, cast, and prose.

It now also includes decision canvases for individual actors, institutions, factions, and conditional alliances; a source-independent workflow for producing original outlines; a 20-point quality rubric for testing those outlines; and an original classical-style poetry module that uses the `chinese-poetry` repository as a form-and-imagery reference. The repository is MIT-licensed, while the underlying corpus should still receive source and rights review before any model-training use. It is not suitable for author imitation, continuation, or model fine-tuning.

## Not yet claimed

- Exhaustive summaries of all 2,365 chapters.
- A definitive chronology or character encyclopedia.
- Claims about the author's intent, values, or real-world advice.
- GPU-trained weights or a LoRA.

## Recommended second pass

1. Divide the 2,365 chapters into narrative arcs by setting, institution, and dominant conflict.
2. For each arc, create a short source-grounded card: objective, bottleneck, information edge, reversal, persistent cost.
3. Compare cards to identify repeated mechanisms and exceptions.
4. Add a `references/arc-cards.md` file and revise `SKILL.md` only when an inference has evidence from multiple arcs.
5. Run five test prompts: scene analysis, outline critique, resource-conflict design, institutional-response design, and misuse/boundary test.

## GPU note

An RTX 4090 is optional for step 2 only if a local language model is used to draft annotations in batches. It is not required for the actual distillation: the quality bottleneck is source traceability and human review, not GPU compute.

No GPU workload or model training is included in this release.
