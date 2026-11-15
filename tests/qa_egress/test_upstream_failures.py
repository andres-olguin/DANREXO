"""Observe how the sandbox sends masked data during timeout and streaming."""

import json

import httpx
import pytest


@pytest.fixture
def chat_payload():
    return {
        "model": "sandbox-only",
        "messages": [{"role": "user", "content": "Correo: timeout@example.invalid"}],
    }


def timeout_response(request):
    raise httpx.ReadTimeout("Synthetic upstream timeout", request=request)


class SyntheticStream(httpx.SyncByteStream):
    def __iter__(self):
        yield b"data: first\n\n"
        yield b"data: second\n\n"


def streaming_response(request):
    return httpx.Response(
        200, headers={"Content-Type": "text/event-stream"}, stream=SyntheticStream()
    )


@pytest.mark.parametrize("mock_upstream", [timeout_response], indirect=True)
def test_upstream_timeout_has_one_masked_attempt(
    chat_payload, sandbox_forward, sandbox_token, mock_upstream
):
    _, requests = mock_upstream

    with pytest.raises(httpx.ReadTimeout, match="Synthetic upstream timeout"):
        sandbox_forward(chat_payload, token=sandbox_token)

    assert len(requests) == 1
    assert json.loads(requests[0].content) == {
        "model": "sandbox-only",
        "messages": [{"role": "user", "content": "Correo: [[EMAIL]]"}],
    }


@pytest.mark.parametrize("mock_upstream", [streaming_response], indirect=True)
def test_streaming_sends_masked_payload_and_yields_chunks(
    chat_payload, sandbox_forward, sandbox_token, mock_upstream
):
    _, requests = mock_upstream
    chat_payload["stream"] = True

    response = sandbox_forward(chat_payload, token=sandbox_token)
    assert response is not None
    try:
        assert response.status_code == 200
        assert not response.is_stream_consumed
        assert len(requests) == 1
        assert json.loads(requests[0].content) == {
            "model": "sandbox-only",
            "messages": [{"role": "user", "content": "Correo: [[EMAIL]]"}],
            "stream": True,
        }
        assert list(response.iter_raw()) == [b"data: first\n\n", b"data: second\n\n"]
    finally:
        response.close()
