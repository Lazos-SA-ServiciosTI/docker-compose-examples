#!/usr/bin/env python3
"""Find and optionally apply the newest stable official WordPress PHP-FPM tag."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen


REGISTRY = "https://registry-1.docker.io"
AUTH = "https://auth.docker.io/token"
TAG_PATTERN = re.compile(r"^php(?P<major>\d+)\.(?P<minor>\d+)-fpm$")
IMAGE_LINE = re.compile(
    r"^(?P<prefix>\s*image:\s*wordpress:)(?P<tag>[^\s#]+)(?P<suffix>\s*(?:#.*)?)$",
    re.MULTILINE,
)


def request_json(url: str, token: str | None = None) -> tuple[dict, object]:
    headers = {"Accept": "application/json", "User-Agent": "docker-compose-examples"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=30) as response:
        return json.load(response), response.headers


def registry_token() -> str:
    query = urlencode(
        {"service": "registry.docker.io", "scope": "repository:library/wordpress:pull"}
    )
    payload, _ = request_json(f"{AUTH}?{query}")
    return payload.get("token") or payload["access_token"]


def wordpress_tags() -> set[str]:
    token = registry_token()
    url = f"{REGISTRY}/v2/library/wordpress/tags/list?n=1000"
    tags: set[str] = set()

    while url:
        payload, headers = request_json(url, token)
        tags.update(payload.get("tags") or [])
        link = headers.get("Link", "")
        next_link = re.search(r'<([^>]+)>\s*;\s*rel="next"', link)
        url = urljoin(url, next_link.group(1)) if next_link else ""

    return tags


def example_files() -> list[Path]:
    files: list[Path] = []
    for path in sorted(Path(".").glob("wordpress-*/docker-compose.yml")):
        if IMAGE_LINE.search(path.read_text(encoding="utf-8")):
            files.append(path)
    if not files:
        raise RuntimeError("No WordPress example Compose files were found.")
    return files


def current_tags(files: list[Path]) -> set[str]:
    result: set[str] = set()
    for path in files:
        matches = IMAGE_LINE.findall(path.read_text(encoding="utf-8"))
        if len(matches) != 1:
            raise RuntimeError(f"Expected one wordpress image declaration in {path}.")
        result.add(matches[0][1])
    if len(result) != 1:
        raise RuntimeError("WordPress examples do not all use the same image tag.")
    return result


def version(tag: str) -> tuple[int, int] | None:
    match = TAG_PATTERN.fullmatch(tag)
    if not match:
        return None
    return int(match.group("major")), int(match.group("minor"))


def newest_candidate(current: str, available: set[str]) -> str:
    current_version = version(current)
    if current_version is None:
        raise RuntimeError(f"Current WordPress tag does not match php<major>.<minor>-fpm: {current}")

    candidates = [
        (parsed, tag)
        for tag in available
        if (parsed := version(tag)) is not None and parsed > current_version
    ]
    return max(candidates, default=((0, 0), ""))[1]


def apply_tag(files: list[Path], old_tag: str, new_tag: str) -> None:
    for path in files:
        contents = path.read_text(encoding="utf-8")
        updated, count = IMAGE_LINE.subn(
            lambda match: f"{match.group('prefix')}{new_tag}{match.group('suffix')}",
            contents,
        )
        if count != 1 or old_tag not in contents:
            raise RuntimeError(f"Could not safely update the WordPress image in {path}.")
        path.write_text(updated, encoding="utf-8")


def main() -> int:
    try:
        files = example_files()
        old_tag = next(iter(current_tags(files)))
        if len(sys.argv) == 3 and sys.argv[1] == "--update":
            new_tag = sys.argv[2]
            if version(new_tag) is None or version(new_tag) <= version(old_tag):
                raise RuntimeError(f"Refusing non-newer or unsupported tag: {new_tag}")
            apply_tag(files, old_tag, new_tag)
            return 0
        if len(sys.argv) != 1:
            raise RuntimeError("Usage: check_wordpress_php_tag.py [--update TAG]")

        candidate = newest_candidate(old_tag, wordpress_tags())
        print(f"tag={candidate}")
        return 0
    except (HTTPError, URLError, KeyError, RuntimeError, TimeoutError, json.JSONDecodeError) as error:
        print(f"WordPress tag check failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
