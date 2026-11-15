"""In-memory upstream for the egress sandbox tests."""

import asyncio

import httpx
import pytest

from backend.dlp.pii import redact
from models.chat import ChatRequest
from services.audit import audit_prompt


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


@pytest.fixture
def sandbox_forward(mock_upstream):
    """Wire the real detector to the in-memory provider for sandbox tests."""
    client, _ = mock_upstream

    def forward(payload: dict) -> httpx.Response | None:
        request = ChatRequest.model_validate(payload)
        audit = asyncio.run(audit_prompt(request))
        if not audit.allowed:
            return None

        messages = []
        for message in request.messages:
            masked, _ = redact(message.content)
            messages.append({"role": message.role, "content": masked})

        # Limit the sandbox payload to the test model and masked messages.
        return client.post("/chat", json={"model": "sandbox-only", "messages": messages})

    return forward
