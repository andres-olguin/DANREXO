"""Check that the sandbox observes the JSON received by the fake provider."""

import json


def test_mock_upstream_records_requests(mock_upstream):
    client, requests = mock_upstream
    payload = {"messages": [{"role": "user", "content": "Mensaje ficticio: ñ"}]}

    assert len(requests) == 0
    response = client.post("/chat", json=payload)
    assert response.json() == {"status": "ok"}
    assert len(requests) == 1
    assert json.loads(requests[0].content) == payload
