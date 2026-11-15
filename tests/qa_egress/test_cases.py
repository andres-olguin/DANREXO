"""Validate the synthetic inputs before wiring them through the egress flow."""

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
