"""Check that interleaved synthetic clients keep their own request and response."""

import json

import httpx
import pytest


def echo_received_message(request):
    body = json.loads(request.content)
    return httpx.Response(200, json={"received": body["messages"][0]["content"]})


@pytest.mark.parametrize("mock_upstream", [echo_received_message], indirect=True)
def test_interleaved_clients_get_their_own_responses(
    sandbox_forward, sandbox_tokens, mock_upstream
):
    _, requests = mock_upstream
    first_a = sandbox_forward(
        {
            "model": "sandbox-only",
            "messages": [{"role": "user", "content": "A-1: alpha@example.invalid"}],
        },
        token=sandbox_tokens["A"],
    )
    response_b = sandbox_forward(
        {
            "model": "sandbox-only",
            "messages": [{"role": "user", "content": "B-1: bravo@example.invalid"}],
        },
        token=sandbox_tokens["B"],
    )
    second_a = sandbox_forward(
        {
            "model": "sandbox-only",
            "messages": [{"role": "user", "content": "A-2: alpha@example.invalid"}],
        },
        token=sandbox_tokens["A"],
    )

    expected = ["A-1: [[EMAIL]]", "B-1: [[EMAIL]]", "A-2: [[EMAIL]]"]
    assert [json.loads(request.content) for request in requests] == [
        {"model": "sandbox-only", "messages": [{"role": "user", "content": content}]}
        for content in expected
    ]
    for response, content in zip((first_a, response_b, second_a), expected, strict=True):
        assert response is not None
        assert response.status_code == 200
        assert response.json() == {"received": content}
