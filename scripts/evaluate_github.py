#!/usr/bin/env python3
"""Fetch public GitHub repository notes for resume project selection."""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path


def fetch_json(url: str) -> object:
    request = urllib.request.Request(url, headers={"User-Agent": "resume-builder-template"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_text(url: str, timeout: int = 10) -> str | None:
    request = urllib.request.Request(url, headers={"User-Agent": "resume-builder-template"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read().decode("utf-8", errors="ignore")
    except urllib.error.URLError:
        return None


def get_readme_api(username: str, repo_name: str) -> str | None:
    """Fetch README via the GitHub API (single call, base64 payload).

    Preferred over raw.githubusercontent.com, which can hang. Returns None
    when the repo has no readable README.
    """
    import base64

    url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "resume-builder-template", "Accept": "application/vnd.github.raw"},
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.read().decode("utf-8", errors="ignore")[:20000]
    except urllib.error.URLError:
        pass
    # Fallback: JSON envelope variant.
    request = urllib.request.Request(url, headers={"User-Agent": "resume-builder-template"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
        content = payload.get("content", "")
        if content:
            return base64.b64decode(content).decode("utf-8", errors="ignore")[:20000]
    except (urllib.error.URLError, ValueError, KeyError):
        return None
    return None


def get_readme(username: str, repo_name: str, default_branch: str) -> str:
    api_readme = get_readme_api(username, repo_name)
    if api_readme:
        return api_readme

    candidates = [
        f"https://raw.githubusercontent.com/{username}/{repo_name}/{default_branch}/README.md",
        f"https://raw.githubusercontent.com/{username}/{repo_name}/master/README.md",
    ]

    for url in candidates:
        content = fetch_text(url)
        if content:
            return content

    return "No README found or accessible."


def write_repo_note(output_dir: Path, username: str, repo: dict[str, object]) -> None:
    name = str(repo["name"])
    default_branch = str(repo.get("default_branch") or "main")
    readme = get_readme(username, name, default_branch)

    content = "\n".join(
        [
            f"# {name}",
            "",
            f"**URL:** {repo.get('html_url', '')}",
            f"**Language:** {repo.get('language') or 'Unknown'}",
            f"**Stars:** {repo.get('stargazers_count', 0)}",
            f"**Description:** {repo.get('description') or 'No description provided.'}",
            "",
            "## README",
            "",
            readme,
        ]
    )

    (output_dir / f"{name}.md").write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("username", help="GitHub username to inspect")
    parser.add_argument("--output-dir", default="data/github", help="Directory for generated Markdown notes")
    parser.add_argument("--include-forks", action="store_true", help="Include forked repositories")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    repos_url = f"https://api.github.com/users/{args.username}/repos?per_page=100&sort=updated"
    repos = fetch_json(repos_url)
    if not isinstance(repos, list):
        raise SystemExit("GitHub returned an unexpected response.")

    written = 0
    for repo in repos:
        if not isinstance(repo, dict):
            continue
        if repo.get("fork") and not args.include_forks:
            continue
        if not repo.get("description") and not repo.get("stargazers_count"):
            continue

        write_repo_note(output_dir, args.username, repo)
        written += 1
        time.sleep(0.2)

    print(f"Wrote {written} repository notes to {output_dir}")


if __name__ == "__main__":
    main()
