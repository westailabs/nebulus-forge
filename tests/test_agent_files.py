"""Generated projects use AGENTS.md + CLAUDE.md stub + .gemini/settings.json."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from forge.models import Strategy
from forge.pipeline import generate

PROFILES = Path(__file__).resolve().parents[1] / "profiles"

VARIABLES = {
    "base": {"project_name": "demo", "description": "Demo project"},
    "fullstack": {"project_name": "demo", "description": "Demo project"},
    "monorepo": {"project_name": "eco", "org_name": "Acme"},
}


@pytest.mark.parametrize("profile", sorted(VARIABLES))
def test_agent_instruction_files(tmp_path: Path, profile: str) -> None:
    target = tmp_path / profile
    target.mkdir()
    generate(
        profile,
        target,
        VARIABLES[profile],
        Strategy.CREATE,
        PROFILES,
        dry_run=False,
    )

    agents = (target / "AGENTS.md").read_text(encoding="utf-8")
    assert agents.startswith("# AGENTS.md")
    assert "agents.md" in agents

    assert (target / "CLAUDE.md").read_text(encoding="utf-8") == "@AGENTS.md\n"

    settings = json.loads((target / ".gemini" / "settings.json").read_text())
    assert settings == {"context": {"fileName": "AGENTS.md"}}

    assert not (target / "GEMINI.md").exists()
