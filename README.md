# LLM Hallucination Evaluation Lab

Deterministic QA checks for source-grounded LLM answers. This project detects claims that are not supported by supplied evidence, measures citation coverage, and distinguishes a grounded response from a deliberately hallucinated one.

## Why this matters

An answer can sound fluent yet invent policy dates, numbers, or capabilities. The evaluator makes this failure observable before release by checking atomic claims against an approved context.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python -m src.evaluate --sample grounded
python -m src.evaluate --sample hallucinated
```

## Method

1. Split output into explicit claims.
2. Normalize each claim and look for support in the approved source passages.
3. Check whether every supported claim has a `[source-id]` citation.
4. Report unsupported claims, missing citations, and a groundedness score.

## Limitations

This is a transparent lexical baseline, intentionally easy to audit. Production systems should add semantic entailment, human review for ambiguous cases, adversarial prompts, and domain-specific policy rules.
