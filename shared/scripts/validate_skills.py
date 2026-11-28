"""
Validate VizArc skill packages across Claude Code, Google Antigravity, and OpenAI Codex.
Checks YAML frontmatter rules, platform-specific metadata constraints, and relative file references.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

PLATFORM_TARGETS = {
    "claude": REPO_ROOT / ".claude" / "skills" / "vizarc" / "SKILL.md",
    "antigravity": REPO_ROOT / ".agent" / "skills" / "vizarc" / "SKILL.md",
    "codex": REPO_ROOT / ".agents" / "skills" / "vizarc" / "SKILL.md",
}

ALLOWED_STANDARD_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}

CLAUDE_EXTENSION_FIELDS = {
    "argument-hint",
    "disable-model-invocation",
    "when_to_use",
}


def parse_frontmatter(text: str) -> Tuple[Dict[str, str], str]:
    """Minimal dependency-free YAML frontmatter parser for SKILL.md validation."""
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        raise ValueError("Missing opening YAML frontmatter delimiter '---'.")
    lines = text.splitlines()
    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        raise ValueError("Missing closing YAML frontmatter delimiter '---'.")

    meta: Dict[str, str] = {}
    current_key = None
    for line in lines[1:end_idx]:
        if not line.strip() or line.strip().startswith("#"):
            continue
        if line.startswith((" ", "\t")) and current_key:
            meta[current_key] = (meta[current_key] + " " + line.strip()).strip()
            continue
        if ":" not in line:
            raise ValueError(f"Malformed frontmatter line: {line!r}")
        key, val = line.split(":", 1)
        current_key = key.strip()
        meta[current_key] = val.strip().strip('"').strip("'")

    body = "\n".join(lines[end_idx + 1 :])
    return meta, body


def validate_skill(platform: str, skill_path: Path) -> List[str]:
    """Validate one platform SKILL.md and return a list of errors."""
    errors: List[str] = []
    if not skill_path.exists():
        return [f"Missing file: {skill_path}"]

    text = skill_path.read_text(encoding="utf-8")
    try:
        meta, body = parse_frontmatter(text)
    except ValueError as exc:
        return [str(exc)]

    name = meta.get("name", "")
    desc = meta.get("description", "")

    if not name:
        errors.append("Missing required 'name' field.")
    elif not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append(f"Invalid skill name '{name}' (must be lowercase alphanumeric with single hyphens, <=64 chars).")
    elif name != skill_path.parent.name:
        errors.append(f"Skill name '{name}' must match parent directory '{skill_path.parent.name}'.")

    if not desc:
        errors.append("Missing required 'description' field.")
    elif len(desc) > 1024:
        errors.append(f"Description exceeds 1024 chars ({len(desc)}).")

    compat = meta.get("compatibility", "")
    if len(compat) > 500:
        errors.append(f"Compatibility exceeds 500 chars ({len(compat)}).")

    allowed_keys = set(ALLOWED_STANDARD_FIELDS)
    if platform == "claude":
        allowed_keys |= CLAUDE_EXTENSION_FIELDS

    for key in meta:
        if key not in allowed_keys:
            errors.append(f"Incompatible or unknown frontmatter field '{key}' for platform '{platform}'.")

    if platform in ("antigravity", "codex") and "allowed-tools" in meta:
        if "Bash(" in meta["allowed-tools"]:
            errors.append(f"Claude-specific 'Bash(...)' syntax found in allowed-tools for '{platform}'.")

    # Verify markdown relative links resolve on disk
    for match in re.finditer(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)", body):
        rel_target = match.group(1).strip()
        if rel_target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (skill_path.parent / rel_target).resolve()
        if not resolved.exists():
            errors.append(f"Broken relative reference '{rel_target}' (resolved to {resolved}).")

    return errors


def validate_claude_plugin() -> List[str]:
    """Validate .claude-plugin/plugin.json references."""
    manifest = REPO_ROOT / ".claude-plugin" / "plugin.json"
    if not manifest.exists():
        return [f"Missing Claude plugin manifest: {manifest}"]
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON in plugin.json: {exc}"]

    errors: List[str] = []
    skills = data.get("skills", [])
    if isinstance(skills, str):
        skills = [skills]
    for entry in skills:
        if not entry.startswith("./"):
            errors.append(f"plugin.json skill path '{entry}' must start with './'.")
        target = (REPO_ROOT / entry).resolve()
        if not (target / "SKILL.md").exists():
            errors.append(f"plugin.json skill target missing SKILL.md: {target}")
    return errors


def main() -> int:
    has_failures = False
    print("VizArc Cross-Platform Skill Validator")
    print("=" * 42)

    for platform, path in PLATFORM_TARGETS.items():
        errs = validate_skill(platform, path)
        rel = path.relative_to(REPO_ROOT)
        if errs:
            has_failures = True
            print(f"[FAIL] {platform:<12} ({rel})")
            for err in errs:
                print(f"       - {err}")
        else:
            print(f"[PASS] {platform:<12} ({rel})")

    plugin_errs = validate_claude_plugin()
    if plugin_errs:
        has_failures = True
        print("[FAIL] claude-plugin (.claude-plugin/plugin.json)")
        for err in plugin_errs:
            print(f"       - {err}")
    else:
        print("[PASS] claude-plugin (.claude-plugin/plugin.json)")

    return 1 if has_failures else 0


if __name__ == "__main__":
    sys.exit(main())
