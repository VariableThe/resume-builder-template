# Photo assets (private, gitignored)

Drop your resume photo here as one of:

- `assets/photo.jpg`
- `assets/photo.jpeg`
- `assets/photo.png`

The build (`python3 scripts/build.py`) auto-detects the first file found,
in that priority order, and embeds it top-right in the final PDF.

- If a photo is present → it appears top-right (≈2.6cm × 3.2cm, aspect-kept).
- If no photo is present → the header collapses to a clean centered layout
  with no broken image and no empty box.

Guidelines:

- Square or 3:4 portrait works best. JPG quality ~85+, ~600×750px minimum.
- Professional headshot, plain background.
- Never commit the photo: it is ignored via `.gitignore` (`/assets/photo.*`).
  Only `assets/.gitkeep` and this README are tracked.
