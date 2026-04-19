#!/usr/bin/env python
"""Lightweight test server to verify /api/topics endpoint works."""

import asyncio
from aiohttp import web
from moshi.topics import get_topics_list


async def handle_topics(request):
    """Return list of available conversation topics."""
    return web.json_response(get_topics_list())


async def main():
    app = web.Application()
    app.router.add_get("/api/topics", handle_topics)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", 8998)
    await site.start()

    print("✅ Lightweight test server started on http://localhost:8998")
    print("   - Try: curl http://localhost:8998/api/topics")
    print("   - Press Ctrl+C to stop\n")

    try:
        await asyncio.sleep(3600)  # Run for 1 hour
    except KeyboardInterrupt:
        print("\n✅ Shutting down")
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
