# Poetry Data Manifest

## External source

| Field | Value |
| --- | --- |
| Project | `chinese-poetry/chinese-poetry` |
| URL | `https://github.com/chinese-poetry/chinese-poetry` |
| Repository license | MIT |
| Data provenance note | The project README says data was collected from the internet. Repository licensing does not automatically resolve every underlying text or edition right. |
| Included in this repository | No |

The indexing scripts default to these poetry-focused collections when present:

- `全唐诗`
- `宋词`
- `诗经`
- `五代诗词`

They intentionally do not index every JSON file in the external repository by default because it also contains prose and other collections.

## Permitted workflow in this project

1. The user obtains the external repository separately.
2. The user or operator reviews the repository version and intended use.
3. `build_poetry_index.py` creates a local SQLite derivative for retrieval and overlap checking.
4. Generated indexes remain untracked and are excluded by `.gitignore`.
5. Retrieved works guide imagery, form, and analysis; generated output must not copy or lightly rewrite them.

## Record before training

Do not begin model adaptation until a run-specific manifest records:

```yaml
corpus_repository: https://github.com/chinese-poetry/chinese-poetry
corpus_revision: <full commit SHA>
collections: []
files_included: 0
records_after_cleaning: 0
normalization_steps: []
license_reviewed_by: <name>
license_review_date: <YYYY-MM-DD>
allowed_use: <retrieval/evaluation/training>
excluded_sources: []
base_model: <model and revision>
base_model_license: <license>
```

Capture the external revision with:

```bash
git -C /path/to/chinese-poetry rev-parse HEAD
```

## Never commit

- downloaded corpora or source books;
- SQLite indexes built from external data;
- access credentials;
- model checkpoints or optimizer state;
- generated samples containing substantial copied passages.
