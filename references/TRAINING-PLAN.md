# Future 4090 Training Plan

This document defines gates for a future local-model experiment. It does not claim that training has occurred.

## Goal

Adapt a license-compatible open model to follow structured inputs about an **original** character arc and produce concise classical-style Chinese narrative poems. The target is character relevance, controlled form, and originality, not imitation of a modern author or work.

## Gates before GPU use

1. Complete the run-specific fields in `DATA-MANIFEST.md`.
2. Select a base model whose license allows the intended local adaptation and sharing.
3. Build retrieval and checker baselines first; training must beat those baselines on a held-out set.
4. Create instruction examples that pair original character situations with independently written target poems. Do not use passages or poems from a modern novel as targets.
5. Separate train, validation, and memorization-probe sets before training.

## Suggested example schema

```json
{
  "character_stage": "少年离乡后第一次承担集体损失",
  "turning_point": "用自己的清白证据换取城门开放",
  "scene_position": "chapter_end",
  "form": "seven_char_four_lines",
  "required_images": ["残灯"],
  "avoid_terms": ["剑", "血", "天命"],
  "poem": "<independently authored target>",
  "narrative_function": "个人损失与群体获救并置"
}
```

## Evaluation

Use a held-out set and record:

- character and turning-point relevance, scored by a human rubric;
- requested line count and character-count pass rate;
- forbidden-term violation rate;
- suspicious 5+ character overlap rate against the indexed corpus;
- repeated phrase rate within each poem;
- diversity across prompts with different character arcs;
- side-by-side preference against the retrieval-plus-prompt baseline.

Strict line length is not equivalent to correct regulated verse. Historical rhyme and tonal-pattern evaluation requires a separately reviewed lexicon and validator.

## Stopping conditions

Stop the run if any of the following occurs:

- validation quality degrades for two consecutive evaluations;
- memorization or corpus-overlap rate rises materially above the baseline;
- outputs repeatedly imitate a named modern work despite the instruction boundary;
- the base-model or corpus license cannot be documented;
- GPU memory, temperature, or system stability becomes unsafe.

Record configuration, revision, metrics, and sample-review decisions for every run. Do not publish weights until license and memorization review passes.
