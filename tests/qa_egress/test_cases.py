"""Validate synthetic inputs and check the sandbox egress payload."""

import asyncio
import json
from pathlib import Path
from unittest.mock import AsyncMock

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


FORWARD_CASES = [case for case in CASES if case["expected_action"] == "forward"]


@pytest.mark.parametrize("case", FORWARD_CASES, ids=[case["id"] for case in FORWARD_CASES])
def test_allowed_request_reaches_upstream_with_expected_body(
    case, sandbox_forward, mock_upstream, sandbox_token
):
    _, requests = mock_upstream
    extra_email = "excluded-field@example.invalid"

    response = sandbox_forward(
        {
            "model": "sandbox-only",
            "messages": case["messages"],
            "extra": {"contact": extra_email},
        },
        token=sandbox_token,
    )

    assert response is not None
    assert response.status_code == 200
    assert len(requests) == 1
    body = requests[0].content
    assert extra_email.encode("utf-8") not in body
    assert json.loads(body) == {
        "model": "sandbox-only",
        "messages": [
            {"role": message["role"], "content": masked}
            for message, masked in zip(
                case["messages"], case["expected_contents"], strict=True
            )
        ],
    }


def test_blocked_request_never_reaches_upstream(
    sandbox_forward, mock_upstream, sandbox_token
):
    case = next(case for case in CASES if case["id"] == "block-sentinel")
    _, requests = mock_upstream

    response = sandbox_forward(
        {"model": "sandbox-only", "messages": case["messages"]},
        token=sandbox_token,
    )

    assert response is None
    assert len(requests) == 0


def test_unauthenticated_request_never_reaches_upstream(sandbox_forward, mock_upstream):
    case = next(case for case in CASES if case["id"] == "mask-email")
    _, requests = mock_upstream
    policy = AsyncMock(side_effect=AssertionError("Policy ran before authentication"))

    response = sandbox_forward(
        {"model": "sandbox-only", "messages": case["messages"]}, policy=policy
    )

    assert response is None
    policy.assert_not_called()
    assert not requests


def test_policy_error_never_reaches_upstream(
    sandbox_forward, mock_upstream, sandbox_token
):
    case = next(case for case in CASES if case["id"] == "mask-email")
    _, requests = mock_upstream
    policy = AsyncMock(side_effect=RuntimeError("Synthetic policy failure"))

    with pytest.raises(RuntimeError, match="Synthetic policy failure"):
        sandbox_forward(
            {"model": "sandbox-only", "messages": case["messages"]},
            token=sandbox_token,
            policy=policy,
        )

    policy.assert_awaited_once()
    assert not requests
