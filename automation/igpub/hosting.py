"""Image hosting adapters — turn a repo-relative image path into the PUBLIC JPEG URL the
Graph API fetches. The backend is swappable (GitHub Pages now; R2/Cloudinary/tunnel later) so
the host stays a config choice, never a core change."""
from __future__ import annotations

from typing import Protocol


class ImageHost(Protocol):
    def url_for(self, repo_relative_path: str) -> str: ...


class GitHubPagesHost:
    """Serves images committed to the repo via GitHub Pages.

    The 'upload' is just committing the JPEG under automation/assets/; the public URL is derived
    from its repo path — no API, no credentials, no expiry.
    """

    def __init__(self, pages_base: str) -> None:
        # e.g. https://timbankrupt.github.io/midjourney-explore
        self.pages_base = pages_base.rstrip("/")

    def url_for(self, repo_relative_path: str) -> str:
        return f"{self.pages_base}/{repo_relative_path.lstrip('/')}"


def build_host(config: dict) -> ImageHost:
    host_cfg = (config or {}).get("host", {}) or {}
    kind = host_cfg.get("kind", "github_pages")
    if kind == "github_pages":
        base = host_cfg.get("pages_base", "")
        if not base:
            raise ValueError(
                "host.pages_base is required for github_pages "
                "(e.g. https://<user>.github.io/<repo>)"
            )
        return GitHubPagesHost(base)
    raise ValueError(f"unknown host kind: {kind!r}")
