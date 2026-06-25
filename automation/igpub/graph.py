"""Meta Graph API client for IG content publishing (image / carousel).

Network calls go through an injected `session`, so the module imports without `requests` and the
publish flow is unit-testable with a fake transport. The access token is sent as a POST/GET param
and is NEVER logged (errors surface only Meta's message).
"""
from __future__ import annotations

from typing import Any, Optional

GRAPH = "https://graph.facebook.com"


class GraphError(RuntimeError):
    pass


class GraphClient:
    def __init__(self, ig_user_id: str, token: str, graph_version: str = "v21.0",
                 session: Optional[Any] = None) -> None:
        self.ig_user_id = ig_user_id
        self._token = token
        self.base = f"{GRAPH}/{graph_version}"
        self._session = session

    @property
    def session(self):
        if self._session is None:
            import requests  # lazy — not needed when a session is injected (tests)
            self._session = requests.Session()
        return self._session

    def _post(self, path: str, params: dict) -> dict:
        r = self.session.post(f"{self.base}/{path}", data={**params, "access_token": self._token})
        return self._json(r)

    def _get(self, path: str, params: dict) -> dict:
        r = self.session.get(f"{self.base}/{path}", params={**params, "access_token": self._token})
        return self._json(r)

    @staticmethod
    def _json(r) -> dict:
        try:
            data = r.json()
        except Exception:  # noqa: BLE001
            raise GraphError(f"non-JSON response (HTTP {getattr(r, 'status_code', '?')})")
        if isinstance(data, dict) and data.get("error"):
            err = data["error"]  # never echo the token; surface Meta's message + code only
            raise GraphError(f"Graph error: {err.get('message')} (code {err.get('code')})")
        return data

    # --- containers ---
    def create_image_container(self, image_url: str, caption: str) -> str:
        return self._post(f"{self.ig_user_id}/media",
                          {"image_url": image_url, "caption": caption})["id"]

    def create_carousel_child(self, image_url: str) -> str:
        return self._post(f"{self.ig_user_id}/media",
                          {"image_url": image_url, "is_carousel_item": "true"})["id"]

    def create_carousel(self, child_ids: list[str], caption: str) -> str:
        return self._post(f"{self.ig_user_id}/media",
                          {"media_type": "CAROUSEL", "children": ",".join(child_ids),
                           "caption": caption})["id"]

    def container_status(self, container_id: str) -> str:
        return self._get(container_id, {"fields": "status_code"}).get("status_code", "")

    def publish(self, container_id: str) -> str:
        return self._post(f"{self.ig_user_id}/media_publish", {"creation_id": container_id})["id"]

    def permalink(self, media_id: str) -> str:
        return self._get(media_id, {"fields": "permalink"}).get("permalink", "")

    def publishing_limit(self) -> int:
        data = self._get(f"{self.ig_user_id}/content_publishing_limit", {"fields": "quota_usage"})
        rows = data.get("data") or [{}]
        return int(rows[0].get("quota_usage", 0) or 0)
