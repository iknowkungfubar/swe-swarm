"""
Utility functions for agents.
"""

from pathlib import Path


def load_agent_prompt(role: str) -> str | None:
    """Load agent prompt from markdown file based on role."""
    # Map role to filename
    filename_map = {
        "product_manager": "product_manager.md",
        "principal_engineer": "principal_engineer.md",
        "senior_engineer": "senior_engineer.md",
        "qa": "qa.md",
        "sre": "sre.md",
        "ux": "ux.md",
        "security": "security.md",
        "tpm": "tpm.md",
    }

    filename = filename_map.get(role)
    if not filename:
        return None

    prompt_path = Path(__file__).parent / filename
    if prompt_path.exists():
        return prompt_path.read_text()
    else:
        return None
