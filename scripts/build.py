"""Build and check standalone Orca bot prompts from the pack sources."""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
OUTPUT = ROOT / "dist"
MODULES = (
    "spec-delivery",
    "pr-review-docs",
    "repo-maintenance",
    "security-dependencies",
    "release-environments",
    "infrastructure-operations",
)
GROUPS = {
    "review-maintenance": ("pr-review-docs", "repo-maintenance", "security-dependencies"),
    "release-operations": ("release-environments", "infrastructure-operations"),
}
ROLES = (*MODULES, *GROUPS)
SAFE_DEFAULTS = {"enabled": False, "results_to": "chat", "runs_in": "new"}
CRON_FIELD = re.compile(r"\*|([0-9]+)(?:-([0-9]+))?")
CRON_BOUNDS = ((0, 59), (0, 23), (1, 31), (1, 12), (0, 6))


def valid_cron(expression):
    fields = expression.split()
    if len(fields) != len(CRON_BOUNDS):
        return False
    for field, (minimum, maximum) in zip(fields, CRON_BOUNDS):
        match = CRON_FIELD.fullmatch(field)
        if not match:
            return False
        start, end = match.groups()
        if start is not None and not minimum <= int(start) <= int(end or start) <= maximum:
            return False
    return True


def load_routines():
    manifest = json.loads((TEMPLATES / "routines.json").read_text(encoding="utf-8"))
    if manifest["version"] != 1 or manifest["defaults"] != SAFE_DEFAULTS:
        raise ValueError("Unsupported routine version or unsafe defaults")

    routines_by_role = {role: [] for role in MODULES}
    seen = set()
    for routine in manifest["routines"]:
        role, routine_id = routine["bot"], routine["id"]
        if role not in routines_by_role or routine_id in seen:
            raise ValueError(f"Unknown role or repeated routine ID: {role}/{routine_id}")
        if routine["tier"] not in {"recommended", "opt-in"} or not routine["prompt"].strip():
            raise ValueError(f"Invalid routine: {routine_id}")
        trigger = routine["trigger"]
        if set(trigger) == {"cron"}:
            if not valid_cron(trigger["cron"]):
                raise ValueError(f"Invalid cron expression: {routine_id}")
        elif set(trigger) != {"source", "event"} or routine["tier"] != "opt-in":
            raise ValueError(f"Invalid event configuration: {routine_id}")
        routines_by_role[role].append(routine)
        seen.add(routine_id)
    for role, modules in GROUPS.items():
        routines_by_role[role] = [
            routine for module in modules for routine in routines_by_role[module]
        ]
    return routines_by_role


def render_routine(routine):
    trigger = routine["trigger"]
    if "cron" in trigger:
        when = f'Cron `{trigger["cron"]}` in the confirmed timezone.'
    else:
        when = f'Event `{trigger["source"]}.{trigger["event"]}` with a confirmed scope.'
    return (
        f'### {routine["name"]}\n\n'
        f'`{routine["id"]}` · {routine["tier"]}. {when}\n\n'
        f'{routine["prompt"]}\n'
    )


def render_role(role):
    role_text = (TEMPLATES / f"{role}.md").read_text(encoding="utf-8").strip()
    if role in GROUPS:
        sections = [role_text]
        for module in GROUPS[role]:
            sections.append(re.sub(r"^(?=#+ )", "#", render_role(module), flags=re.MULTILINE))
        return "\n\n".join(sections)
    if "## First-run questions" not in role_text or "Onboarding dry run:" not in role_text:
        raise ValueError(f"Template {role} requires an interview and dry run")
    return role_text


def build(check):
    common = (TEMPLATES / "common.md").read_text(encoding="utf-8").strip()
    routines_by_role = load_routines()
    if not check:
        OUTPUT.mkdir(exist_ok=True)
    stale = []
    for role, routines in routines_by_role.items():
        role_text = render_role(role)
        if role in GROUPS:
            sections = []
            for module in GROUPS[role]:
                title = render_role(module).splitlines()[0].removeprefix("# ")
                recipes = "\n".join(
                    "#" + render_routine(routine)
                    for routine in routines_by_role[module]
                )
                sections.append(f"### {title}\n\n{recipes}")
            routine_text = "\n".join(sections)
        else:
            routine_text = "\n".join(render_routine(routine) for routine in routines)
        contents = (
            f"{role_text}\n\n{common}\n\n"
            "## Optional Orca routines\n\n"
            "Start with an interview. Confirm the profile before any setup write. "
            "Register approved routines paused, in a fresh run, with results in this chat "
            "unless an explicit destination was approved. If a matching routine "
            "already exists, review it instead of registering another.\n\n"
            f"{routine_text}"
        )
        target = OUTPUT / f"{role}.md"
        if check:
            if not target.is_file() or target.read_bytes() != contents.encode("utf-8"):
                stale.append(target.name)
        else:
            target.write_bytes(contents.encode("utf-8"))
    if stale:
        print(f"Rebuild stale templates: {', '.join(stale)}", file=sys.stderr)
        return 1
    print(f"{'Checked' if check else 'Built'} {len(ROLES)} standalone templates.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check generated files without writing")
    raise SystemExit(build(parser.parse_args().check))
