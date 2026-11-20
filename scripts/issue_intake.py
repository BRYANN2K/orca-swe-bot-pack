"""Build an issue queue from tracker snapshots and confirmed cross-tracker links."""

import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit

from pack import load_json, nonempty, require, require_object, require_text

TRACKERS = {"github", "gitlab", "linear"}
SOURCE_STATES = {"complete", "partial", "unavailable"}
ISSUE_STATES = {"open", "closed"}


def validate_ref(ref):
    require(nonempty(ref), "Issue ref must be text")
    parts = ref.split(":", 2)
    require(len(parts) == 3 and parts[0] in TRACKERS
            and all(part and not any(c.isspace() for c in part) for part in parts),
            "Issue ref must be tracker:scope:id")
    return ":".join(parts[:2])


def reconcile(snapshot):
    require_object(snapshot, {"schema_version", "sources", "issues", "work_links"}, "snapshot")
    require(type(snapshot["schema_version"]) is int and snapshot["schema_version"] == 1,
            "Unsupported issue snapshot schema_version")
    for field in ("sources", "issues", "work_links"):
        require(isinstance(snapshot[field], list), f"{field} must be a list")

    sources = {}
    for source in snapshot["sources"]:
        require_object(source, {"scope", "status"}, "source")
        require_text(source, "scope", "source")
        require(isinstance(source["status"], str) and source["status"] in SOURCE_STATES,
                "Source status must be complete, partial, or unavailable")
        scope = source["scope"]
        validate_ref(scope + ":placeholder")
        require(scope.count(":") == 1, "Source scope must be tracker:scope")
        require(scope not in sources, f"Duplicate source scope: {scope}")
        sources[scope] = source["status"]
    require(sources, "Declare at least one expected source")

    issues = {}
    for issue in snapshot["issues"]:
        require_object(issue, {"ref", "url", "title", "status"}, "issue")
        scope = validate_ref(issue["ref"])
        require(scope in sources and sources[scope] != "unavailable",
                f"Issue belongs to an unobserved source: {scope}")
        require_text(issue, "title", "issue")
        require_text(issue, "url", "issue")
        url = urlsplit(issue["url"])
        require(url.scheme in {"http", "https"} and url.hostname
                and url.username is None and url.password is None,
                "Use an HTTP(S) issue URL without credentials")
        require(isinstance(issue["status"], str) and issue["status"] in ISSUE_STATES,
                "Issue status must be open or closed")
        ref = issue["ref"]
        require(ref not in issues, f"Duplicate issue ref: {ref}")
        issues[ref] = issue

    linked_refs = set()
    work_ids = set()
    work_items = []
    for link in snapshot["work_links"]:
        require_object(link, {"id", "primary", "refs", "evidence"}, "work link")
        for key in ("id", "primary", "evidence"):
            require_text(link, key, "work link")
        work_id = link["id"]
        require(work_id not in work_ids, f"Duplicate work ID: {work_id}")
        work_ids.add(work_id)
        refs = link["refs"]
        require(isinstance(refs, list) and len(refs) >= 2, "Work link needs at least two refs")
        require(work_id in refs or (work_id.startswith("work:") and nonempty(work_id[5:])),
                "Keep an existing issue ID or choose a work: ID")
        for ref in refs:
            scope = validate_ref(ref)
            require(scope in sources, f"Work link references undeclared source: {scope}")
            require(ref not in linked_refs, f"Issue belongs to more than one work link: {ref}")
            linked_refs.add(ref)
        require(link["primary"] in refs, "Primary issue ref must be part of the work link")
        work_items.append(work_item(work_id, link["primary"], refs, issues, link["evidence"]))

    for ref, issue in issues.items():
        if ref not in linked_refs:
            work_items.append(work_item(ref, ref, [ref], issues, None))
    return {
        "coverage_complete": all(status == "complete" for status in sources.values()),
        "sources": sources,
        "work_items": sorted(work_items, key=lambda item: item["id"]),
    }


def work_item(work_id, primary, refs, issues, evidence):
    entries = [
        issues.get(ref, {"ref": ref, "status": "not-observed"}) for ref in sorted(refs)
    ]
    states = {issue["status"] for issue in entries}
    if "open" in states:
        state = "open"
    elif "not-observed" in states:
        state = "unknown"
    else:
        state = "closed"
    return {
        "id": work_id,
        "primary": primary,
        "state": state,
        "link_evidence": evidence,
        "issues": entries,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path, help="Read-only normalized tracker snapshot")
    args = parser.parse_args()
    try:
        print(json.dumps(reconcile(load_json(args.snapshot)), indent=2, ensure_ascii=False))
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
