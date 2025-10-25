"""Test to validate GitHub Actions versions are up-to-date."""
import re
import yaml
from pathlib import Path


def test_github_actions_not_deprecated():
    """Ensure GitHub Actions use non-deprecated versions."""
    workflow_dir = Path(__file__).parent.parent / ".github" / "workflows"
    
    deprecated_actions = {
        "actions/upload-artifact@v3": "actions/upload-artifact@v4",
        "actions/upload-artifact@v2": "actions/upload-artifact@v4",
        "actions/cache@v3": "actions/cache@v4",
        "actions/cache@v2": "actions/cache@v4",
        "actions/create-release@v1": "softprops/action-gh-release@v2",
    }
    
    issues = []
    for workflow_file in workflow_dir.glob("*.yml"):
        content = workflow_file.read_text()
        for deprecated, recommended in deprecated_actions.items():
            if deprecated in content:
                issues.append(
                    f"Deprecated action '{deprecated}' found in {workflow_file.name}. "
                    f"Use '{recommended}' instead."
                )
    
    assert not issues, "\n".join(issues)
