# Contributing Guide
## Project Roles

| Branch | Owner | Responsibilities |
|--------|--------|------------------|
| `vqa` | Abby | Implement VQA model, repo setup |
| `ui` | Person 2 | User interface + integration logic |
| `ocr` | Person 3 | OCR module + presentation materials |

---

## Branching Model

1. The **main** branch is protected and should always contain a working version.  
2. Each member works in their own feature branch:
   - `vqa`
   - `ui`
   - `ocr`
3. Before merging into `main`, create a **Pull Request (PR)**:
   - Assign at least one teammate as reviewer.
   - Include a short summary of what was added or changed.

---

## Testing Before Pushing

- Run your own module with sample data.
- Make sure your script doesn’t break `main.py`.
- Check that paths (imports) are relative to the project root.

---

## Documentation Rules

Each folder (`/vqa`, `/ocr`, `/ui`) must have a `README.md` including:
- Purpose of the module  
- Setup instructions  
- Example usage  
- Test images and results

When done, update:
- `/docs/eval.md` with evaluation results  
- `/README.md` root file if structure or dependencies change

---

## Pull Request Checklist

Before submitting a PR:
- [ ] Your module runs without errors.
- [ ] Your `README.md` is updated.
- [ ] You added or updated at least one test case.
- [ ] You merged/rebased with `main` before pushing.

---

## Milestone Deadlines

| Phase | Due Date | Description |
|--------|-----------|-------------|
| Modules (VQA, OCR, UI) | **Nov 19** | Each module working independently |
| Integration | **Nov 26** | Full pipeline functional |
| Final Repo + Demo | **Dec 1** | Presentation and submission |

---