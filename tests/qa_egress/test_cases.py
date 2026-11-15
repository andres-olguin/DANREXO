"""Validate synthetic inputs and check the sandbox egress payload."""

import asyncio
import json
from pathlib import Path

import pytest

from backend.dlp.pii import redact
from models.chat import ChatRequest
from services.audit import audit_prompt


CASES = json.loads(Path(__file__).with_name("cases.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("case", CASES, ids=[case["id"] for case in CASES])
def test_synthetic_case_matches_existing_components(case):
    request = ChatRequest.model_validate(
        {"model": "sandbox-only", "messages": case["messages"]}
    )

    audit = asyncio.run(audit_prompt(request))
    assert audit.allowed is (case["expected_action"] == "forward")
    if audit.allowed:
        assert [redact(message.content)[0] for message in request.messages] == (
            case["expected_contents"]
        )


def test_allowed_request_reaches_upstream_with_masked_email(
    sandbox_forward, mock_upstream
):
    case = next(case for case in CASES if case["id"] == "mask-email")
    _, requests = mock_upstream
    raw_email = case["messages"][-1]["content"].split()[-1]

    response = sandbox_forward(
        {
            "model": "sandbox-only",
            "messages": case["messages"],
            "extra": {"contact": raw_email},
        }
    )

    assert response is not None
    assert response.status_code == 200
    assert len(requests) == 1
    body = requests[0].content
    assert raw_email.encode("utf-8") not in body
    assert json.loads(body) == {
        "model": "sandbox-only",
        "messages": [
            {"role": message["role"], "content": masked}
            for message, masked in zip(
                case["messages"], case["expected_contents"], strict=True
            )
        ],
    }
