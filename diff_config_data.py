#!/usr/bin/env python3
"""
diff_config_data.py — Compare two sets of decoded config tables and generate change reports.

Produces both a human-readable markdown changelog and machine-readable JSON diffs
for each changed table. Uses the first column (index 0) as the record ID for
matching records between versions.

Usage:
  python3 diff_config_data.py data/tables uploads/20260301/tables --output diffs/20260301

Output:
  diffs/20260301/changelog.md        — Markdown summary
  diffs/20260301/summary.json        — Machine-readable overview
  diffs/20260301/tables/Unit.diff.json  — Per-table diffs (only changed tables)
"""

import argparse
import json
import os
import sys
from datetime import datetime

# Tables that are most relevant for combat reverse engineering
COMBAT_TABLES = {
    "Attribute", "Buff", "Skill", "Skilleffcet", "Skill_level", "Unit",
    "Equipment", "Equipment_attr", "Level", "Angel", "Angel_skill", "Angel_star",
    "Artifact", "Artifact_level", "Fate_level", "Fly_level", "Jobs_wakeup",
    "Mount", "Pet", "Petlevel", "Relic", "Season_ship", "Ship", "Spirit",
    "Client_global", "Back_talent", "Badge",
}


def load_tables(directory):
    """Load all JSON table files from a directory, returning {name: records}."""
    tables = {}
    if not os.path.isdir(directory):
        return tables
    for fname in os.listdir(directory):
        if fname.endswith(".json") and fname != "_index.json":
            name = fname[:-5]  # strip .json
            path = os.path.join(directory, fname)
            with open(path) as f:
                tables[name] = json.load(f)
    return tables


def get_record_id(record):
    """Extract the primary key from a record (first field, typically 'id')."""
    val = None
    if isinstance(record, dict):
        # Named fields — use 'id' if available, else first key
        if "id" in record:
            val = record["id"]
        else:
            keys = list(record.keys())
            if keys:
                val = record[keys[0]]
    elif isinstance(record, list):
        # Positional array — first element is the ID
        if record:
            val = record[0]
    # Ensure hashable (lists can't be dict keys)
    if isinstance(val, list):
        val = tuple(val)
    return val


def diff_records(old_record, new_record):
    """Compare two records, returning dict of changed fields."""
    changes = {}
    if isinstance(old_record, dict) and isinstance(new_record, dict):
        all_keys = set(old_record.keys()) | set(new_record.keys())
        for key in all_keys:
            if key.startswith("_"):
                continue
            old_val = old_record.get(key)
            new_val = new_record.get(key)
            if old_val != new_val:
                changes[key] = {"old": old_val, "new": new_val}
    elif isinstance(old_record, list) and isinstance(new_record, list):
        max_len = max(len(old_record), len(new_record))
        for i in range(max_len):
            old_val = old_record[i] if i < len(old_record) else None
            new_val = new_record[i] if i < len(new_record) else None
            if old_val != new_val:
                changes[f"[{i}]"] = {"old": old_val, "new": new_val}
    else:
        if old_record != new_record:
            changes["_value"] = {"old": old_record, "new": new_record}
    return changes


def diff_table(old_records, new_records):
    """Diff two lists of records, returning added/removed/modified."""
    old_by_id = {}
    for r in old_records:
        rid = get_record_id(r)
        if rid is not None:
            old_by_id[rid] = r

    new_by_id = {}
    for r in new_records:
        rid = get_record_id(r)
        if rid is not None:
            new_by_id[rid] = r

    old_ids = set(old_by_id.keys())
    new_ids = set(new_by_id.keys())

    added = [new_by_id[rid] for rid in sorted(new_ids - old_ids)]
    removed = [old_by_id[rid] for rid in sorted(old_ids - new_ids)]

    modified = []
    for rid in sorted(old_ids & new_ids):
        changes = diff_records(old_by_id[rid], new_by_id[rid])
        if changes:
            modified.append({"id": rid, "changes": changes})

    return {
        "added": added,
        "removed": removed,
        "modified": modified,
    }


def generate_changelog(all_diffs, old_tables, new_tables, date_label):
    """Generate a markdown changelog from all table diffs."""
    lines = [
        f"# Config Data Changelog — {date_label}",
        "",
        f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        "",
    ]

    # Summary counts
    new_table_names = sorted(set(new_tables.keys()) - set(old_tables.keys()))
    removed_table_names = sorted(set(old_tables.keys()) - set(new_tables.keys()))
    changed_table_names = sorted(all_diffs.keys())

    total_added = sum(len(d["added"]) for d in all_diffs.values())
    total_removed = sum(len(d["removed"]) for d in all_diffs.values())
    total_modified = sum(len(d["modified"]) for d in all_diffs.values())

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **{len(new_table_names)}** new tables")
    lines.append(f"- **{len(removed_table_names)}** removed tables")
    lines.append(f"- **{len(changed_table_names)}** changed tables")
    lines.append(f"- **{total_added}** records added, **{total_removed}** removed, **{total_modified}** modified")
    lines.append("")

    # Combat-relevant changes (highlighted section)
    combat_changes = {k: v for k, v in all_diffs.items() if k in COMBAT_TABLES}
    if combat_changes:
        lines.append("## Combat-Relevant Changes")
        lines.append("")
        for tname in sorted(combat_changes.keys()):
            d = combat_changes[tname]
            parts = []
            if d["added"]:
                parts.append(f"+{len(d['added'])} added")
            if d["removed"]:
                parts.append(f"-{len(d['removed'])} removed")
            if d["modified"]:
                parts.append(f"~{len(d['modified'])} modified")
            lines.append(f"- **{tname}**: {', '.join(parts)}")

            # Show sample of modified records for combat tables
            for m in d["modified"][:5]:
                change_fields = list(m["changes"].keys())[:5]
                lines.append(f"  - ID {m['id']}: {', '.join(change_fields)}")
        lines.append("")

    # New tables
    if new_table_names:
        lines.append("## New Tables")
        lines.append("")
        for name in new_table_names:
            count = len(new_tables[name])
            combat = " **(combat)**" if name in COMBAT_TABLES else ""
            lines.append(f"- **{name}**: {count} records{combat}")
        lines.append("")

    # Removed tables
    if removed_table_names:
        lines.append("## Removed Tables")
        lines.append("")
        for name in removed_table_names:
            lines.append(f"- **{name}**")
        lines.append("")

    # All changed tables (non-combat)
    non_combat_changes = {k: v for k, v in all_diffs.items() if k not in COMBAT_TABLES}
    if non_combat_changes:
        lines.append("## Other Changed Tables")
        lines.append("")
        for tname in sorted(non_combat_changes.keys()):
            d = non_combat_changes[tname]
            parts = []
            if d["added"]:
                parts.append(f"+{len(d['added'])}")
            if d["removed"]:
                parts.append(f"-{len(d['removed'])}")
            if d["modified"]:
                parts.append(f"~{len(d['modified'])}")
            lines.append(f"- {tname}: {', '.join(parts)}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Compare two sets of decoded config tables")
    parser.add_argument("baseline", help="Baseline tables directory (e.g., data/tables)")
    parser.add_argument("new", help="New tables directory (e.g., /tmp/new_tables)")
    parser.add_argument("--output", default=None, help="Output directory for diff reports (default: diffs/YYYYMMDD)")
    args = parser.parse_args()

    # Determine output directory
    if args.output:
        output_dir = args.output
    else:
        date_str = datetime.now().strftime("%Y%m%d")
        output_dir = os.path.join("diffs", date_str)

    date_label = os.path.basename(output_dir)

    print(f"Baseline: {args.baseline}")
    print(f"New:      {args.new}")

    old_tables = load_tables(args.baseline)
    new_tables = load_tables(args.new)

    if not old_tables:
        print(f"WARNING: No tables found in baseline {args.baseline}")
    if not new_tables:
        print(f"ERROR: No tables found in {args.new}")
        sys.exit(1)

    print(f"Baseline: {len(old_tables)} tables, New: {len(new_tables)} tables")

    # Diff all tables that exist in both
    all_diffs = {}
    common = set(old_tables.keys()) & set(new_tables.keys())
    for tname in sorted(common):
        d = diff_table(old_tables[tname], new_tables[tname])
        if d["added"] or d["removed"] or d["modified"]:
            all_diffs[tname] = d

    new_table_names = set(new_tables.keys()) - set(old_tables.keys())
    removed_table_names = set(old_tables.keys()) - set(new_tables.keys())

    print(f"\nNew tables: {len(new_table_names)}")
    print(f"Removed tables: {len(removed_table_names)}")
    print(f"Changed tables: {len(all_diffs)}")

    # Create output
    os.makedirs(output_dir, exist_ok=True)
    tables_dir = os.path.join(output_dir, "tables")
    os.makedirs(tables_dir, exist_ok=True)

    # Write per-table diffs
    for tname, d in all_diffs.items():
        diff_data = {
            "table": tname,
            "baseline_count": len(old_tables.get(tname, [])),
            "new_count": len(new_tables.get(tname, [])),
            "combat_relevant": tname in COMBAT_TABLES,
            **d,
        }
        diff_path = os.path.join(tables_dir, f"{tname}.diff.json")
        with open(diff_path, "w") as f:
            json.dump(diff_data, f, indent=2, ensure_ascii=False)

    # Write summary.json
    summary = {
        "date": date_label,
        "baseline_tables": len(old_tables),
        "new_tables_count": len(new_tables),
        "new_tables": sorted(new_table_names),
        "removed_tables": sorted(removed_table_names),
        "changed_tables": sorted(all_diffs.keys()),
        "combat_changes": sorted(k for k in all_diffs if k in COMBAT_TABLES),
        "stats": {
            "total_added": sum(len(d["added"]) for d in all_diffs.values()),
            "total_removed": sum(len(d["removed"]) for d in all_diffs.values()),
            "total_modified": sum(len(d["modified"]) for d in all_diffs.values()),
        },
    }
    with open(os.path.join(output_dir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # Write changelog.md
    changelog = generate_changelog(all_diffs, old_tables, new_tables, date_label)
    with open(os.path.join(output_dir, "changelog.md"), "w") as f:
        f.write(changelog)

    print(f"\nOutput: {output_dir}/")
    print(f"  changelog.md — human-readable summary")
    print(f"  summary.json — machine-readable overview")
    print(f"  tables/      — {len(all_diffs)} per-table diff files")


if __name__ == "__main__":
    main()
