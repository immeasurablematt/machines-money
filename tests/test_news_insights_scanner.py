import json
import os
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock
from urllib.parse import parse_qs, urlparse

from news_insights_scanner.classify_items import classify_item
from news_insights_scanner.ingest import ingest_manual, ingest_x_api
from news_insights_scanner.models import CandidatePost, ScannerConfig
from news_insights_scanner.pipeline import _build_item, _filter_lookback, run_scanner
from news_insights_scanner.score_items import _timeliness


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

    def test_report_with_numbers_is_a_deep_dive_before_metric(self):
        post = CandidatePost(
            post_id="1b",
            post_url="https://x.com/project/status/1b",
            author_handle="project",
            posted_at="2026-06-01T00:00:00Z",
            text="New report breaks down 10 trends in tokenized private credit.",
            captured_at="2026-06-01T00:00:00Z",
        )

        self.assertEqual(classify_item(post), "Deep Dive/Article")

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

    def test_x_api_ingestion_returns_partial_posts_after_malformed_later_page(self):
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
            [],
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

        self.assertEqual([post.post_id for post in result.posts], ["101"])
        self.assertEqual(result.verification_status, "manual_review_needed")
        self.assertIn("Returned 1 post(s) fetched before the failure", result.warnings[0])

    def test_x_api_ingestion_handles_non_object_payload(self):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self):
                return json.dumps([]).encode("utf-8")

        with mock.patch.dict(os.environ, {"X_BEARER_TOKEN": "token"}):
            with mock.patch("news_insights_scanner.ingest.urllib.request.urlopen", return_value=Response()):
                result = ingest_x_api(source_list_id="list-1", max_results=1)

        self.assertEqual(result.verification_status, "manual_review_needed")
        self.assertEqual(result.posts, [])
        self.assertIn("Expected a JSON object response from X API", result.warnings[0])

    def test_x_api_ingestion_handles_explicit_null_objects(self):
        payload = {
            "data": [
                {
                    "id": "301",
                    "author_id": "u1",
                    "created_at": "2026-06-01T00:00:00Z",
                    "text": "Project announced a launch.",
                    "entities": None,
                }
            ],
            "includes": None,
            "meta": None,
        }

        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self):
                return json.dumps(payload).encode("utf-8")

        with mock.patch.dict(os.environ, {"X_BEARER_TOKEN": "token"}):
            with mock.patch("news_insights_scanner.ingest.urllib.request.urlopen", return_value=Response()):
                result = ingest_x_api(source_list_id="list-1", max_results=1)

        self.assertEqual(result.verification_status, "needs_verification")
        self.assertEqual(len(result.posts), 1)
        self.assertEqual(result.posts[0].post_id, "301")
        self.assertEqual(result.posts[0].author_handle, "")
        self.assertEqual(result.posts[0].urls, [])
        self.assertEqual(result.warnings, [])

    def test_manual_json_non_object_falls_back_to_line_parsing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "posts.json"
            input_path.write_text('["https://x.com/project/status/1 adoption stat"]', encoding="utf-8")

            result = ingest_manual(str(input_path))

        self.assertEqual(len(result.posts), 1)
        self.assertEqual(result.posts[0].post_id, "manual-0001")
        self.assertEqual(result.posts[0].post_url, "https://x.com/project/status/1")

    def test_timeliness_treats_naive_datetime_as_utc(self):
        class FixedDatetime(datetime):
            @classmethod
            def now(cls, tz=None):
                value = cls(2026, 6, 3, 0, 30, tzinfo=timezone.utc)
                return value if tz is None else value.astimezone(tz)

        with mock.patch("news_insights_scanner.score_items.datetime", FixedDatetime):
            self.assertEqual(_timeliness("2026-06-01T00:00:00"), 4)

    def test_filter_lookback_treats_naive_datetime_as_utc(self):
        class FixedDatetime(datetime):
            @classmethod
            def now(cls, tz=None):
                value = cls(2026, 6, 3, 0, 30, tzinfo=timezone.utc)
                return value if tz is None else value.astimezone(tz)

        post = CandidatePost(
            post_id="naive",
            post_url="https://x.com/project/status/naive",
            author_handle="project",
            posted_at="2026-06-01T00:00:00",
            text="Project announced a launch.",
            captured_at="2026-06-03T00:30:00Z",
        )

        with mock.patch("news_insights_scanner.pipeline.datetime", FixedDatetime):
            self.assertEqual(_filter_lookback([post], lookback_hours=48), [])

    def test_x_api_ingestion_loads_bearer_token_from_dotenv(self):
        payload = {
            "data": [
                {
                    "id": "201",
                    "author_id": "u1",
                    "created_at": "2026-06-01T00:00:00Z",
                    "text": "Project announced a launch.",
                }
            ],
            "includes": {"users": [{"id": "u1", "username": "project"}]},
            "meta": {},
        }
        captured_auth_headers = []

        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self):
                return json.dumps(payload).encode("utf-8")

        def fake_urlopen(request, timeout):
            captured_auth_headers.append(request.headers.get("Authorization"))
            return Response()

        original_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            env_path = Path(tmpdir) / ".env"
            env_path.write_text('X_BEARER_TOKEN="dotenv-token"\n', encoding="utf-8")
            os.chdir(tmpdir)
            try:
                with mock.patch.dict(os.environ, {}, clear=True):
                    with mock.patch("news_insights_scanner.ingest.urllib.request.urlopen", side_effect=fake_urlopen):
                        result = ingest_x_api(source_list_id="list-1", max_results=1)
            finally:
                os.chdir(original_cwd)

        self.assertEqual(len(result.posts), 1)
        self.assertEqual(captured_auth_headers, ["Bearer dotenv-token"])

    def test_scanner_selects_top_items_instead_of_cataloging_every_post(self):
        manual_payload = {
            "posts": [
                {
                    "post_id": "announcement",
                    "posted_at": "2026-06-01T17:00:00Z",
                    "text": "Maple announced a new institutional lending integration for tokenized credit.",
                    "urls": ["https://maple.finance/blog/integration"],
                },
                {
                    "post_id": "metric",
                    "posted_at": "2026-06-01T16:00:00Z",
                    "text": "Protocol revenue reached $2M over the past 30 days.",
                    "urls": ["https://project.example/revenue"],
                },
                {
                    "post_id": "retweet",
                    "posted_at": "2026-06-01T15:00:00Z",
                    "text": "RT @someone: crazy work keep cooking",
                    "urls": ["https://x.com/someone/status/1"],
                },
                {
                    "post_id": "promo",
                    "posted_at": "2026-06-01T14:00:00Z",
                    "text": "Full episode with our founder is live now.",
                    "urls": ["https://x.com/project/status/2"],
                },
                {
                    "post_id": "report",
                    "posted_at": "2026-06-01T13:00:00Z",
                    "text": "New research report breaks down tokenized real-world asset market structure.",
                    "urls": ["https://project.example/report"],
                },
            ]
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.json"
            output_dir = Path(tmpdir) / "out"
            input_path.write_text(json.dumps(manual_payload), encoding="utf-8")
            run_scanner(
                ScannerConfig(
                    ingestion="manual",
                    input_path=str(input_path),
                    output_dir=str(output_dir),
                    top_n=2,
                    lookback_hours=24 * 365,
                )
            )
            payload = json.loads((output_dir / "digest.json").read_text())
            markdown = (output_dir / "digest.md").read_text()

        selected_ids = {item["post_id"] for item in payload["items"]}
        self.assertEqual(payload["selection_audit"]["reviewed_tweet_count"], 5)
        self.assertEqual(payload["selection_audit"]["selected_count"], 2)
        self.assertEqual(len(payload["items"]), 2)
        self.assertIn("announcement", selected_ids)
        self.assertIn("metric", selected_ids)
        self.assertNotIn("retweet", selected_ids)
        self.assertIn("Reviewed 5 tweets", markdown)
        self.assertIn("Items selected for Ian: `2`", markdown)


if __name__ == "__main__":
    unittest.main()
