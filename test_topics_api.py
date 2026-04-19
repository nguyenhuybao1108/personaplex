#!/usr/bin/env python
"""Simple test to verify the topics API works correctly."""

import asyncio
import json
from aiohttp import web
from moshi.topics import get_topics_list


async def handle_topics(request):
    """Return list of available conversation topics."""
    return web.json_response(get_topics_list())


async def test_topics_endpoint():
    """Test the topics endpoint."""
    print("Testing /api/topics endpoint...")

    # Create a minimal app with just the topics endpoint
    app = web.Application()
    app.router.add_get("/api/topics", handle_topics)

    # Create test client
    from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

    class TestTopicsAPI(AioHTTPTestCase):
        async def get_application(self):
            return app

        async def test_topics_endpoint(self):
            resp = await self.client.request("GET", "/api/topics")
            assert resp.status == 200
            data = await resp.json()
            assert isinstance(data, list)
            assert len(data) == 5
            assert all(
                "id" in item and "label" in item and "level" in item
                for item in data
            )
            print("✓ Topics endpoint works!")
            for topic in data:
                print(f"  - {topic['id']}: {topic['label']} ({topic['level']})")

    # Run test
    test = TestTopicsAPI()
    await test.setUpAsync()
    await test.test_topics_endpoint()
    await test.tearDownAsync()


if __name__ == "__main__":
    asyncio.run(test_topics_endpoint())
