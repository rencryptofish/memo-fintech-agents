#!/usr/bin/env python3
"""
Governance refresh checks for this research repo.

Modes:
  - weekly: source-health + citation due dates + metadata schema checks
  - monthly: regulatory/rails tracker freshness checks
  - quarterly: TAM harmonization freshness checks
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TODAY = dt.date.today()


REQUIRED_METADATA_COLUMNS = {
    "source_id",
    "source_url",
    "source_capture_method",
    "last_verified_utc",
    "confidence",
    "status",
}


def parse_date(value: str) -> dt.date | None:
    value = (value or "").strip()
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S"):
        try:
            return dt.datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def read_header(path: Path) -> set[str]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        row = next(reader, [])
    return set(row)


def extract_last_verified(path: Path) -> dt.date | None:
    text = path.read_text(encoding="utf-8")
    patterns = [
        r"Last verified:\s*(\d{4}-\d{2}-\d{2})",
        r"Last updated:\s*(\d{4}-\d{2}-\d{2})",
        r"Effective date:\s*(\d{4}-\d{2}-\d{2})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            date_val = parse_date(match.group(1))
            if date_val:
                return date_val
    return None


def check_weekly() -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []

    matrix_path = ROOT / "research" / "memo-citation-backfill-matrix.csv"
    if not matrix_path.exists():
        failures.append("Missing research/memo-citation-backfill-matrix.csv")
    else:
        with matrix_path.open("r", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                due = parse_date(row.get("next_refresh_date", ""))
                claim_id = row.get("claim_id", "unknown")
                if due and due <= TODAY:
                    failures.append(
                        f"Citation refresh overdue: {claim_id} (next_refresh_date={due.isoformat()})"
                    )

    x402_path = ROOT / "data" / "x402_kpi_canonical.csv"
    if not x402_path.exists():
        failures.append("Missing data/x402_kpi_canonical.csv")
    else:
        last_dates: list[dt.date] = []
        with x402_path.open("r", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                d = parse_date(row.get("last_verified_utc", ""))
                if d:
                    last_dates.append(d)
        if not last_dates:
            failures.append("x402 KPI canonical file has no parseable last_verified_utc values")
        else:
            age_days = (TODAY - max(last_dates)).days
            if age_days > 7:
                failures.append(
                    f"x402 KPI canonical data is stale ({age_days} days old; SLA=7 days)"
                )

    governed_csvs = [
        "data/fintech_geographic_opportunity_metrics.csv",
        "data/fintech_failure_risk_kpis.csv",
        "data/fintech_value_creation_vs_destruction_cases.csv",
        "data/fintech_funding_stage_year_category_estimated.csv",
        "data/fintech_stage_breakdown_by_year_category_wide_estimated.csv",
        "data/fintech_stage_totals_by_year_estimated.csv",
        "data/fintech_category_maturity_late_stage_share_estimated.csv",
    ]
    for rel in governed_csvs:
        path = ROOT / rel
        if not path.exists():
            failures.append(f"Missing governed dataset: {rel}")
            continue
        header = read_header(path)
        missing = sorted(REQUIRED_METADATA_COLUMNS - header)
        if missing:
            failures.append(f"{rel} missing metadata columns: {', '.join(missing)}")

    tracker_path = ROOT / "research" / "milestone-status-tracker.csv"
    if not tracker_path.exists():
        failures.append("Missing research/milestone-status-tracker.csv")
    else:
        header = read_header(tracker_path)
        expected = {"milestone_id", "status", "target_window", "milestone"}
        missing = sorted(expected - header)
        if missing:
            failures.append(
                f"research/milestone-status-tracker.csv missing columns: {', '.join(missing)}"
            )

    return failures, warnings


def check_monthly() -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []

    targets = [
        ("research/regulatory-tracker-us-2026.md", 35),
        ("research/rails-metrics-pack-2026Q1.md", 35),
        ("research/public-private-kpi-refresh-2026Q1.md", 35),
        ("research/source-registry.md", 35),
    ]
    for rel, max_age in targets:
        path = ROOT / rel
        if not path.exists():
            failures.append(f"Missing monthly tracker: {rel}")
            continue
        d = extract_last_verified(path)
        if not d:
            warnings.append(f"No parseable last verified date in {rel}")
            continue
        age_days = (TODAY - d).days
        if age_days > max_age:
            failures.append(f"{rel} is stale ({age_days} days old; SLA={max_age} days)")

    return failures, warnings


def check_quarterly() -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []

    targets = [
        ("research/market-size-harmonization-2026Q1.md", 95),
        ("research/source-governance-policy.md", 120),
    ]
    for rel, max_age in targets:
        path = ROOT / rel
        if not path.exists():
            failures.append(f"Missing quarterly tracker: {rel}")
            continue
        d = extract_last_verified(path)
        if not d:
            warnings.append(f"No parseable date in {rel}")
            continue
        age_days = (TODAY - d).days
        if age_days > max_age:
            failures.append(f"{rel} is stale ({age_days} days old; SLA={max_age} days)")

    return failures, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["weekly", "monthly", "quarterly"],
        required=True,
        help="Refresh cadence mode to validate",
    )
    args = parser.parse_args()

    if args.mode == "weekly":
        failures, warnings = check_weekly()
    elif args.mode == "monthly":
        failures, warnings = check_monthly()
    else:
        failures, warnings = check_quarterly()

    print(f"[{args.mode}] governance refresh check")
    print(f"date={TODAY.isoformat()}")
    print(f"warnings={len(warnings)} failures={len(failures)}")

    for msg in warnings:
        print(f"WARN: {msg}")
    for msg in failures:
        print(f"FAIL: {msg}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
