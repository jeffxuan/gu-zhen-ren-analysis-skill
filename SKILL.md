---
name: strategic-fantasy-writing
description: Analyze, outline, and critique original progression or strategy fantasy through resources, institutions, information asymmetry, and persistent consequences. Also create story-grounded classical-style Chinese poems for original characters and scenes. Use for narrative design, character or faction decisions, outline stress tests, and original 古风叙事诗; do not use for continuation or imitation of a specific modern author or work.
---

# Strategic Fantasy Writing

Build or analyze original fantasy narratives as constrained decision systems. Make character intelligence visible through objectives, scarce resources, rules, incomplete information, alternatives, trade-offs, and consequences that persist.

This skill contains a framework distilled from a user-supplied progression-fantasy corpus, but it is not an author simulator. Do not reproduce passages, continue an existing novel, or imitate a specific modern author or work.

## Route The Request

Read only the references required for the current task, and read each selected reference before producing the result:

- **Analyze plot mechanics or compare narrative arcs:** read `references/ARC-CARDS.md`.
- **Analyze a character, institution, faction, alliance, or strategic decision:** read `references/ACTOR-SYSTEMS.md`.
- **Design an original setting, conflict chain, or opening outline:** read `references/ORIGINAL-STORY-WORKFLOW.md`.
- **Critique or score an original chapter or outline:** read `references/NARRATIVE-STRESS-TEST.md`. Also read the workflow or actor reference when the diagnosis requires it.
- **Write a story-grounded classical-style Chinese poem:** read `references/CLASSICAL-POETRY-MODULE.md`. If a local poetry index is available, use the retrieval and originality-check scripts described there.
- **Trace claims back to the source study:** read `references/SOURCE-PROVENANCE.md`. Source-grounded analysis beyond the listed anchors requires the user to provide the source text.
- **Prepare a future local-model experiment:** read `references/TRAINING-PLAN.md` and `references/DATA-MANIFEST.md`. Do not claim training occurred unless a run produced recorded artifacts and evaluation results.

## Shared Decision Model

For each important scene, identify:

1. **Objective:** immediate need and long-term priority.
2. **Resources:** scarce assets, capabilities, allies, status, time, or information.
3. **Rules:** system mechanics and institutional constraints.
4. **Information:** facts, beliefs, uncertainty, and concealed knowledge.
5. **Options:** plausible actions, including restraint and exit.
6. **Trade-offs:** what each option sacrifices, exposes, or delays.
7. **Persistent consequence:** what changes the next decision environment.

Do not call a character merely “smart,” “ruthless,” or “powerful.” Explain the mechanism that makes a choice viable under that character's information and constraints.

## Working Principles

- Couple progression to a bottleneck such as material, time, safety, reputation, knowledge, or opportunity.
- Treat institutions as active systems with budgets, precedents, legitimacy, morale, and succession concerns.
- Give every informational advantage a source, useful scope, observable trace, and failure condition.
- Use an adversarial update loop: plan -> partial result -> revealed cost -> counterplay -> revised plan.
- Make sacrifice change position by altering survival odds, leverage, coalition access, or future options.
- Escalate by widening rules, resource networks, and coordination problems, not only damage numbers.

## Output Rules

- For analysis, use neutral modern Chinese unless the user requests another language.
- For poetry mode, follow the form and language rules in `references/CLASSICAL-POETRY-MODULE.md`; the modern-Chinese rule does not apply to the poem itself.
- Distinguish source observation, analytical inference, and unverified interpretation.
- For original writing, create independent settings, characters, terminology, conflicts, and prose.
- Do not convert fictional deception, coercion, violence, or illegal behavior into real-world operational advice.
- If required context is missing, state the assumption briefly instead of inventing source facts.

## Final Check

Before delivering work, verify that:

- major wins depend on a stated constraint, resource decision, or informational edge;
- at least one capable opponent has coherent incentives and a rational update;
- an important cost persists beyond the scene;
- power-system terms appear through decisions or consequences rather than glossary dumping;
- the output is independent of any existing work's distinctive expression;
- poetry mode reports whether corpus retrieval and similarity checking actually ran.
