#!/usr/bin/env python3
"""Roll up multiple *-metrics-v*.json files into a weekly/monthly summary (no platform)."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


def deep_get(obj: Dict[str, Any], path: str) -> Any:
    cur: Any = obj
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def mean_of(values: List[float]) -> Optional[float]:
    vals = [v for v in values if isinstance(v, (int, float))]
    if not vals:
        return None
    return round(float(statistics.mean(vals)), 4)


def period_label(period: str, when: Optional[datetime] = None) -> str:
    when = when or datetime.now(timezone.utc)
    if period == "month":
        return when.strftime("%Y-%m")
    # ISO week
    y, w, _ = when.isocalendar()
    return f"{y}-W{w:02d}"


def load_metrics(root: Path, glob_pat: str) -> List[Dict[str, Any]]:
    files = sorted(root.glob(glob_pat))
    out: List[Dict[str, Any]] = []
    for f in files:
        if f.name.startswith("_rollup"):
            continue
        try:
            out.append(json.loads(f.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError) as e:
            print(f"skip {f}: {e}", file=sys.stderr)
    return out


def human_filled(human: Any) -> bool:
    if not isinstance(human, dict):
        return False
    return any(
        human.get(k) is not None
        for k in ("capability_loss_rate", "atomicity_pass_rate", "rubric_samples")
    )


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Roll up pipeline metrics JSON files")
    parser.add_argument("--root", required=True)
    parser.add_argument(
        "--glob",
        default="docs/ai/metrics/**/*-metrics-v*.json",
        help="Glob relative to root",
    )
    parser.add_argument("--period", choices=["week", "month"], default="week")
    parser.add_argument("--out-dir", default=None)
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    rows = load_metrics(root, args.glob)
    label = period_label(args.period)
    out_dir = Path(args.out_dir) if args.out_dir else root / "docs" / "ai" / "metrics"
    out_dir.mkdir(parents=True, exist_ok=True)

    n = len(rows)
    with_red = sum(1 for r in rows if r.get("red_lights"))
    human_n = sum(1 for r in rows if human_filled(r.get("human")))

    first_pass = [deep_get(r, "auto.codegen.first_pass_rate") for r in rows]
    orphan = [deep_get(r, "auto.testcase.orphan_rate") for r in rows]
    req_cov = [deep_get(r, "auto.testcase.req_coverage") for r in rows]
    change_bad = sum(
        1
        for r in rows
        if (deep_get(r, "auto.solution.change_consistency") or 0) not in (0, None)
    )

    summary = {
        "schema_version": "1.0",
        "period": args.period,
        "period_label": label,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_count": n,
        "metrics": {
            "requirement_runs": n,
            "l1_red_light_rate": round(with_red / n, 4) if n else None,
            "first_pass_rate_mean": mean_of(first_pass),  # type: ignore
            "orphan_rate_mean": mean_of(orphan),  # type: ignore
            "testcase_req_coverage_mean": mean_of(req_cov),  # type: ignore
            "change_consistency_nonzero_count": change_bad,
            "human_filled_rate": round(human_n / n, 4) if n else None,
        },
        "runs": [
            {
                "requirement_name": r.get("requirement_name"),
                "metrics_version": r.get("metrics_version"),
                "status": r.get("status"),
                "red_lights": r.get("red_lights") or [],
            }
            for r in rows
        ],
    }

    stem = f"_rollup-{label}"
    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"

    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    m = summary["metrics"]
    md = "\n".join(
        [
            f"# 流水线观测汇总 — {label}",
            "",
            f"- generated_at: {summary['generated_at']}",
            f"- source_count: {n}",
            f"- glob: `{args.glob}`",
            "",
            "## 汇总指标",
            "",
            "| 指标 | 值 |",
            "|------|-----|",
            f"| L1 红灯率 | {m['l1_red_light_rate']} |",
            f"| first_pass_rate 均值 | {m['first_pass_rate_mean']} |",
            f"| orphan_rate 均值 | {m['orphan_rate_mean']} |",
            f"| testcase.req_coverage 均值 | {m['testcase_req_coverage_mean']} |",
            f"| change_consistency≠0 次数 | {m['change_consistency_nonzero_count']} |",
            f"| human 已填比例 | {m['human_filled_rate']} |",
            "",
            "## 明细",
            "",
            "| 需求 | metrics 版本 | status | red_lights |",
            "|------|--------------|--------|------------|",
        ]
        + [
            f"| {r.get('requirement_name')} | {r.get('metrics_version')} | {r.get('status')} | "
            f"{', '.join(r.get('red_lights') or []) or '—'} |"
            for r in summary["runs"]
        ]
        + ["", "无埋点平台：本文件由仓库内 metrics JSON 批处理生成。", ""]
    )
    md_path.write_text(md, encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
