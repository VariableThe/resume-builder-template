# Resume Format Template

Use `templates/resume.tex` as the canonical resume structure.

The template is intentionally generic and public-safe. Replace placeholders with your own contact details, education, skills, experience, projects, certifications, and leadership entries.

Recommended build command:

```sh
python3 scripts/build.py --template
```

(Direct compile also works: `tectonic templates/resume.tex`.)

## Photo header pattern

The header is photo-aware via a `\ifhasphoto` flag, fed by `\tryphoto`
probes in priority order (`assets/photo.jpg` wins). With a photo, the
header is a contact minipage plus a ~3.0cm headshot minipage; without one,
it collapses to `center`. Aditya's current resume
(`latestresume/`) uses this pattern. Flip `\photoleftfalse` to
`\photolefttrue` to move the photo top-left.
