"""Keep synthetic identifiers and tokens out of sandbox logs and output."""

import logging

import pytest


def test_allowed_and_blocked_requests_leave_no_raw_data_in_evidence(
    sandbox_forward, sandbox_tokens, mock_upstream, caplog, capfd
):
    allowed_email = "allowed-evidence@example.invalid"
    blocked_email = "blocked-evidence@example.invalid"
    _, requests = mock_upstream

    with caplog.at_level(logging.DEBUG):
        allowed = sandbox_forward(
            {
                "model": "sandbox-only",
                "messages": [{"role": "user", "content": f"Correo: {allowed_email}"}],
            },
            token=sandbox_tokens["A"],
        )
        blocked = sandbox_forward(
            {
                "model": "sandbox-only",
                "messages": [
                    {"role": "user", "content": f"PROMPT_BLOCK_TEST {blocked_email}"}
                ],
            },
            token=sandbox_tokens["B"],
        )

    captured = capfd.readouterr()
    evidence = caplog.text + captured.out + captured.err
    for secret in (allowed_email, blocked_email, *sandbox_tokens.values()):
        if secret in evidence:
            pytest.fail("Sandbox evidence contains an unmasked identifier or token", pytrace=False)

    assert allowed is not None
    assert allowed.status_code == 200
    assert blocked is None
    assert len(requests) == 1
