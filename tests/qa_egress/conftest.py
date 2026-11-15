"""In-memory upstream for the egress sandbox tests."""

import httpx
import pytest


@pytest.fixture
def mock_upstream():
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"status": "ok"})

    with httpx.Client(
        transport=httpx.MockTransport(handle),
        base_url="https://upstream.invalid",
        trust_env=False,
    ) as client:
        yield client, requests
