# Resume Builder Template

A lightweight LaTeX resume starter for creating targeted, one-page technical resumes.

This repository is designed to be forked or copied by anyone who wants a clean resume workflow:

- Start from a polished LaTeX template.
- Add job descriptions and new achievements as plain text notes.
- Keep private resume drafts, cover letters, and personal data out of Git.
- Optionally fetch public GitHub project summaries to help choose resume projects.

## Quick Start

1. Install a LaTeX compiler. The easiest option is [Tectonic](https://tectonic-typesetting.github.io/).
2. Copy the template:

   ```sh
   cp templates/resume.tex resume.tex
   ```

3. Replace the placeholder text in `resume.tex` with your own details.
4. Compile the resume:

   ```sh
   tectonic resume.tex
   ```

The compiled PDF will be created next to `resume.tex`.

## Suggested Workflow

Use these folders as a lightweight workspace:

- `job_description/` - paste target job descriptions here.
- `newinfo/` - add new projects, achievements, skills, and certifications.
- `data/` - store public, non-sensitive project notes.
- `examples/` - keep sample resumes or anonymized examples.

Before publishing your fork, run:

```sh
git status --ignored
```

Make sure only generic template files are tracked.

## Optional: Fetch GitHub Project Notes

You can generate Markdown notes from your public GitHub repositories:

```sh
python3 scripts/evaluate_github.py your-github-username --output-dir data/github
```

The script only reads public repository metadata and README files.

## Privacy Checklist

Before pushing changes, check for:

- Real phone numbers, email addresses, home addresses, student IDs, or government IDs.
- Private certificate links.
- Cover letters for specific companies.
- Old resume drafts.
- AI memory dumps or raw notes that mention personal history.

## License

MIT License. Use it freely for your own resume.
