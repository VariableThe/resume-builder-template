# Resume Generation Workflow

Use this workflow when creating a targeted resume from the template.

1. Read the target job description from `job_description/`.
2. Review new achievements, skills, certifications, and project notes from `newinfo/` and `data/`.
3. Choose the most relevant experience and projects for the role.
4. Write concise bullets that emphasize action, technical depth, and measurable impact.
5. `latestresume/` holds ONLY the current resume. When it is superseded,
   move the old version to `My resumes - old/` for reference and put the
   new version in `latestresume/`. Never keep two currents side by side.
6. Optional photo: drop a headshot at `assets/photo.jpg` (`.jpeg`/`.png`
   also work). It is embedded top-right automatically; with no photo the
   header falls back to centered. Set `\photolefttrue` for top-left.
7. Build with `python3 scripts/build.py` (or `--template`, `--all`).
   PDFs land in `output/pdf/`.
8. Before committing, check that no private details, photos, old drafts, or
   generated PDFs are staged (`git status --short`; photo and PDFs are
   gitignored by default).
