import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from igpub.graph import GraphClient  # noqa: E402


class FakeResp:
    def __init__(self, data):
        self._data = data
        self.status_code = 200

    def json(self):
        return self._data


class FakeSession:
    def __init__(self, data):
        self._data = data
        self.gets = []

    def get(self, url, params=None):
        self.gets.append((url, params))
        return FakeResp(self._data)

    def post(self, url, data=None):
        return FakeResp(self._data)


class TestPublishingLimit(unittest.TestCase):
    """Lock the one method that parses a real nested Meta response shape + its safe default —
    the rate-limit pre-check that gates publishing depends on it."""

    def test_parses_quota_usage(self):
        g = GraphClient("IG", "tok", session=FakeSession({"data": [{"quota_usage": 7}]}))
        self.assertEqual(g.publishing_limit(), 7)

    def test_empty_data_defaults_zero(self):
        g = GraphClient("IG", "tok", session=FakeSession({"data": []}))
        self.assertEqual(g.publishing_limit(), 0)

    def test_missing_data_defaults_zero(self):
        g = GraphClient("IG", "tok", session=FakeSession({}))
        self.assertEqual(g.publishing_limit(), 0)

    def test_token_never_in_get_params_is_caller_concern(self):
        # sanity: the limit GET carries the fields param (token is added internally, not asserted here)
        sess = FakeSession({"data": [{"quota_usage": 0}]})
        GraphClient("IG", "tok", session=sess).publishing_limit()
        self.assertTrue(sess.gets)


class TestGraphError(unittest.TestCase):
    def test_meta_error_raises(self):
        from igpub.graph import GraphError
        g = GraphClient("IG", "tok",
                        session=FakeSession({"error": {"message": "bad", "code": 100}}))
        with self.assertRaises(GraphError):
            g.publishing_limit()


if __name__ == "__main__":
    unittest.main()
