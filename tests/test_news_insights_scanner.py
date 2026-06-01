import json
import os
import unittest
from unittest import mock
from urllib.parse import parse_qs, urlparse

from news_insights_scanner.classify_items import classify_item
from news_insights_scanner.ingest import ingest_x_api
from news_insights_scanner.models import CandidatePost
from news_insights_scanner.pipeline import _build_item


class NewsInsightsScannerTests(unittest.TestCase):
    def test_funding_and_partnership_post_is_an_announcement(self):
        post = CandidatePost(
            post_id="1",
            post_url="https://x.com/project/status/1",
            author_handle="project",
            posted_at="2026-06-01T00:00:00Z",
            text="Project raised $25M Series A and announced a new partnership with a protocol.",
            captured_at="2026-06-01T00:00:00Z",
        )

        self.assertEqual(classify_item(post), "Announcement")

    def test_source_link_alone_does_not_verify_item(self):
        post = CandidatePost(
            post_id="2",
            post_url="https://x.com/project/status/2",
            author_handle="project",
            posted_at="2026-06-01T00:00:00Z",
            text="Protocol revenue reached $1 million this month as users grew 40%.",
            captured_at="2026-06-01T00:00:00Z",
            urls=[{"url": "https://project.example/blog/revenue", "source_kind": "primary"}],
        )

        item = _build_item("run-1", post)

        self.assertEqual(item["verification_status"], "needs_verification")
        self.assertEqual(item["confidence"], "medium")
        self.assertIn("Needs manual verification", item["notes"])

    def test_explicit_source_verified_metadata_can_verify_item(self):
        post = CandidatePost(
            post_id="3",
            post_url="https://x.com/project/status/3",
            author_handle="project",
            posted_at="2026-06-01T00:00:00Z",
            text="Protocol revenue reached $1 million this month as users grew 40%.",
            captured_at="2026-06-01T00:00:00Z",
            urls=[{"url": "https://project.example/blog/revenue", "source_kind": "primary"}],
            metadata={"source_verified": True},
        )

        item = _build_item("run-1", post)

        self.assertEqual(item["verification_status"], "verified")
        self.assertEqual(item["confidence"], "high")

    def test_x_api_ingestion_follows_pagination_token(self):
        payloads = [
            {
                "data": [
                    {
                        "id": "101",
                        "author_id": "u1",
                        "created_at": "2026-06-01T00:00:00Z",
                        "text": "Project announced a launch.",
                    }
                ],
                "includes": {"users": [{"id": "u1", "username": "project"}]},
                "meta": {"next_token": "NEXT"},
            },
            {
                "data": [
                    {
                        "id": "102",
                        "author_id": "u2",
                        "created_at": "2026-06-01T00:01:00Z",
                        "text": "Project fees reached $10M.",
                    }
                ],
                "includes": {"users": [{"id": "u2", "username": "project2"}]},
                "meta": {},
            },
        ]
        calls = []

        class Response:
            def __init__(self, payload):
                self.payload = payload

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self):
                return json.dumps(self.payload).encode("utf-8")

        def fake_urlopen(request, timeout):
            calls.append(request.full_url)
            return Response(payloads[len(calls) - 1])

        with mock.patch.dict(os.environ, {"X_BEARER_TOKEN": "token"}):
            with mock.patch("news_insights_scanner.ingest.urllib.request.urlopen", side_effect=fake_urlopen):
                result = ingest_x_api(source_list_id="list-1", max_results=2)

        self.assertEqual(len(result.posts), 2)
        self.assertEqual(len(calls), 2)
        first_query = parse_qs(urlparse(calls[0]).query)
        second_query = parse_qs(urlparse(calls[1]).query)
        self.assertNotIn("pagination_token", first_query)
        self.assertEqual(second_query["pagination_token"], ["NEXT"])


if __name__ == "__main__":
    unittest.main()
