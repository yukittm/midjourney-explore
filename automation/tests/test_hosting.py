import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from igpub.hosting import GitHubPagesHost, build_host  # noqa: E402


class TestGitHubPagesHost(unittest.TestCase):
    def test_url_for_strips_slashes(self):
        h = GitHubPagesHost("https://yukittm.github.io/midjourney-explore/")
        self.assertEqual(
            h.url_for("/automation/assets/x/01.jpg"),
            "https://yukittm.github.io/midjourney-explore/automation/assets/x/01.jpg",
        )

    def test_build_host_github_pages(self):
        h = build_host({"host": {"kind": "github_pages", "pages_base": "https://u.github.io/r"}})
        self.assertEqual(h.url_for("a.jpg"), "https://u.github.io/r/a.jpg")

    def test_build_host_requires_base(self):
        with self.assertRaises(ValueError):
            build_host({"host": {"kind": "github_pages"}})

    def test_build_host_unknown_kind(self):
        with self.assertRaises(ValueError):
            build_host({"host": {"kind": "nope"}})

    def test_build_host_defaults_to_github_pages(self):
        h = build_host({"host": {"pages_base": "https://u.github.io/r"}})
        self.assertIsInstance(h, GitHubPagesHost)


if __name__ == "__main__":
    unittest.main()
