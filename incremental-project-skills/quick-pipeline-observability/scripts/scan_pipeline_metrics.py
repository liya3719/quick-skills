#!/usr/bin/env python3
"""Scan incremental-project skill artifacts and emit metrics JSON + MD (read-only)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set

REQ_RE = re.compile(r"\bREQ-(\d+)\b", re.IGNORECASE)
OPEN_RE = re.compile(r"\bOPEN-(\d+)\b", re.IGNORECASE)
TC_RE = re.compile(r"\bTC-[A-Z]?-?\d+\b", re.IGNORECASE)
# Normalize TC ids later


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_text(path: Optional[Path]) -> str:
    if path is None or not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def unique_reqs(text: str) -> Set[str]:
    return {f"REQ-{m.group(1).zfill(3)}" if len(m.group(1)) <= 3 else f"REQ-{m.group(1)}"
            for m in REQ_RE.finditer(text)}


def unique_opens(text: str) -> Set[str]:
    return {f"OPEN-{m.group(1)}" for m in OPEN_RE.finditer(text)}


def unique_tcs(text: str) -> Set[str]:
    return {m.group(0).upper().replace("TC-", "TC-") for m in TC_RE.finditer(text)}


def find_latest(root: Path, patterns: Iterable[str], name_hint: Optional[str] = None) -> Optional[Path]:
    candidates: List[Path] = []
    for pattern in patterns:
        candidates.extend(root.glob(pattern))
    files = [p for p in candidates if p.is_file()]
    if name_hint:
        hinted = [p for p in files if name_hint in p.name]
        if hinted:
            files = hinted
    if not files:
        return None
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0]


def section_after_heading(text: str, keywords: List[str], max_chars: int = 12000) -> str:
    lines = text.splitlines()
    start = None
    start_level = 2
    for i, line in enumerate(lines):
        if not line.lstrip().startswith("#"):
            continue
        low = line.lower()
        if any(k.lower() in low for k in keywords):
            start = i
            start_level = len(line) - len(line.lstrip("#"))
            break
    if start is None:
        for i, line in enumerate(lines):
            if any(k.lower() in line.lower() for k in keywords):
                start = i
                start_level = 2
                break
    if start is None:
        return ""
    end = len(lines)
    for j in range(start + 1, len(lines)):
        line = lines[j]
        if line.lstrip().startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            if level <= start_level:
                end = j
                break
    chunk = "\n".join(lines[start:end])
    return chunk[:max_chars]


def parse_md_tables(text: str) -> List[List[List[str]]]:
    """Return list of tables; each table is list of rows; each row list of cells."""
    tables: List[List[List[str]]] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("|") and "|" in line[1:]:
            rows: List[List[str]] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                raw = lines[i].strip()
                if re.match(r"^\|[\s\-:|]+\|$", raw):
                    i += 1
                    continue
                cells = [c.strip() for c in raw.strip("|").split("|")]
                rows.append(cells)
                i += 1
            if rows:
                tables.append(rows)
            continue
        i += 1
    return tables


def rate(num: float, den: float) -> Optional[float]:
    if den <= 0:
        return None
    return round(num / den, 4)


def scan_decomp(text: str, gaps: List[str]) -> Dict[str, Any]:
    if not text:
        gaps.append("missing decomp document")
        return {}
    reqs = unique_reqs(text)
    opens = unique_opens(text)
    # Heuristic: REQ block with BLOCKED and no GWT-like acceptance nearby counts as untestable
    untestable = 0
    for req in reqs:
        # find a window around first mention
        m = re.search(re.escape(req), text, re.IGNORECASE)
        if not m:
            continue
        window = text[max(0, m.start() - 50) : m.start() + 800]
        if re.search(r"BLOCKED", window) and not re.search(
            r"(Given|When|Then|验收|主路径)", window, re.IGNORECASE
        ):
            untestable += 1
    testable = max(0, len(reqs) - untestable)

    matrix = section_after_heading(text, ["追溯矩阵", "三视图", "§6", "6. "])
    three_view_rate: Optional[float] = None
    if matrix:
        tables = parse_md_tables(matrix)
        if tables:
            rows = tables[0][1:] if len(tables[0]) > 1 else tables[0]
            ok = 0
            total = 0
            for row in rows:
                if not row or not any(REQ_RE.search(c) for c in row):
                    continue
                total += 1
                joined = " ".join(row)
                # treat empty cells as incomplete unless N/A
                emptyish = sum(1 for c in row[1:] if not c.strip())
                if emptyish == 0 or re.search(r"N/A|不适用", joined, re.IGNORECASE):
                    ok += 1
            three_view_rate = rate(ok, total) if total else None
        else:
            gaps.append("decomp three-view matrix table not parsed")
    else:
        gaps.append("decomp three-view / trace matrix section not found")

    return {
        "req_count": len(reqs),
        "open_count": len(opens),
        "reqs": sorted(reqs),
        "testability_rate": rate(testable, len(reqs)),
        "open_density": rate(len(opens), len(reqs)),
        "three_view_complete_rate": three_view_rate,
    }


def scan_solution(text: str, decomp_reqs: Set[str], decomp_text: str, gaps: List[str]) -> Dict[str, Any]:
    if not text:
        gaps.append("missing solution document")
        return {}
    appendix_a = section_after_heading(text, ["附录 A", "附录A", "需求追溯"])
    appendix_d = section_after_heading(text, ["附录 D", "附录D", "本版变更"])
    change_decomp = section_after_heading(decomp_text, ["9.2", "REQ 级变更", "变更明细", "版本与变更"])

    a_reqs = unique_reqs(appendix_a) if appendix_a else unique_reqs(text)
    d_reqs = unique_reqs(appendix_d) if appendix_d else set()
    s92 = unique_reqs(change_decomp) if change_decomp else set()

    if not appendix_a:
        gaps.append("solution appendix A / req trace section weak; used full-doc REQ set")

    coverage = rate(len(a_reqs & decomp_reqs), len(decomp_reqs)) if decomp_reqs else None
    if s92 or d_reqs:
        change_consistency = len(d_reqs.symmetric_difference(s92))
    else:
        change_consistency = 0

    only_sol = a_reqs - decomp_reqs if decomp_reqs else set()
    only_decomp = decomp_reqs - a_reqs if decomp_reqs else set()
    drift_events = len(only_sol) + len(only_decomp)

    # orphan anchor heuristic: lines with 接口/错误码 without REQ or 工程补充
    orphan_lines = 0
    candidate_lines = 0
    for line in text.splitlines():
        if not re.search(r"接口|错误码|error\s*code|API", line, re.IGNORECASE):
            continue
        if line.strip().startswith("#"):
            continue
        candidate_lines += 1
        if not REQ_RE.search(line) and "工程补充" not in line:
            orphan_lines += 1

    return {
        "req_in_appendix_a": len(a_reqs),
        "req_coverage": coverage,
        "change_consistency": change_consistency,
        "drift_events": drift_events,
        "orphan_anchor_rate": rate(orphan_lines, candidate_lines),
        "reqs_only_in_solution": sorted(only_sol),
        "reqs_only_in_decomp": sorted(only_decomp),
    }


def scan_codegen(text: str, gaps: List[str]) -> Dict[str, Any]:
    if not text:
        gaps.append("missing architecture alignment report")
        return {}

    blocked = bool(re.search(r"整单\s*`?blocked`?|status\s*[:=]\s*blocked", text, re.IGNORECASE))

    # status counts from tables
    pass_n = missing_n = blocked_n = 0
    for table in parse_md_tables(text):
        header = [c.lower() for c in table[0]] if table else []
        status_idx = None
        for i, h in enumerate(header):
            if "状态" in h or "status" in h:
                status_idx = i
                break
        for row in table[1:]:
            cell = " ".join(row).lower() if status_idx is None else (row[status_idx].lower() if status_idx < len(row) else "")
            if re.search(r"\bpass\b|通过", cell):
                pass_n += 1
            elif re.search(r"\bmissing\b|缺失", cell):
                missing_n += 1
            elif re.search(r"\bblocked\b|阻塞", cell):
                blocked_n += 1

    critical_total = pass_n + missing_n + blocked_n
    critical_pass = pass_n

    reflow = section_after_heading(text, ["回流记录", "回流"])
    rounds = 0
    if reflow:
        nums = []
        for m in re.finditer(
            r"轮次\s*[:=]?\s*(\d+)|第\s*(\d+)\s*轮|round\s*[:=]?\s*(\d+)",
            reflow,
            re.IGNORECASE,
        ):
            g = m.group(1) or m.group(2) or m.group(3)
            if g:
                nums.append(int(g))
        rounds = max(nums) if nums else 0
    else:
        gaps.append("codegen reflow section not found; first_pass_rate uses current critical stats")

    first_pass_rate = rate(critical_pass, critical_total) if critical_total else None

    # P0 cover: rows mentioning P0 and pass
    p0_reqs = set()
    p0_pass = set()
    for m in re.finditer(r"(REQ-\d+)[^\n]{0,80}P0|P0[^\n]{0,80}(REQ-\d+)", text, re.IGNORECASE):
        rid = m.group(1) or m.group(2)
        if rid:
            p0_reqs.add(rid.upper())
    for m in re.finditer(r"(REQ-\d+)[^\n]{0,120}\bpass\b|\bpass\b[^\n]{0,120}(REQ-\d+)", text, re.IGNORECASE):
        rid = (m.group(1) or m.group(2) or "").upper()
        if rid in p0_reqs:
            p0_pass.add(rid)

    delta = section_after_heading(text, ["偏差", "§8", "8. "])
    unapproved = 0
    if delta:
        for line in delta.splitlines():
            if re.search(r"VA-|偏差|DELTA|未批准", line) or (line.strip().startswith("|") and REQ_RE.search(line)):
                if re.match(r"^\|?\s*-+\s*", line.strip()):
                    continue
                if line.strip().startswith("|") and "偏差" in line and "---" not in line:
                    # skip header-ish
                    cells = [c.strip() for c in line.strip("|").split("|")]
                    if cells and cells[0] in ("偏差", "项", "ID", "编号"):
                        continue
                    unapproved += 1
        # count list items
        unapproved += len(re.findall(r"^\s*[-*]\s+\S+", delta, re.MULTILINE))
        if unapproved == 0 and len(delta.strip()) > 80:
            gaps.append("deviation section present but row count uncertain")

    return {
        "critical_pass": critical_pass,
        "critical_total": critical_total,
        "first_pass_rate": first_pass_rate,
        "p0_req_first_cover": rate(len(p0_pass), len(p0_reqs)) if p0_reqs else None,
        "reflow_rounds": rounds,
        "unapproved_delta_count": unapproved,
        "blocked": blocked or (rounds >= 5 and missing_n > 0),
    }


def scan_testcase(text: str, decomp_reqs: Set[str], gaps: List[str]) -> Dict[str, Any]:
    if not text:
        gaps.append("missing testcase document")
        return {}
    tcs = unique_tcs(text)
    # orphan: TC lines without REQ nearby — approximate via table rows
    orphan = 0
    func_by_req: Dict[str, int] = {r: 0 for r in decomp_reqs}
    three_ok = 0
    three_total = 0

    tables = parse_md_tables(text)
    tc_rows = 0
    for table in tables:
        header = [c.lower() for c in table[0]] if table else []
        if not any("req" in h or "追溯" in h or "层级" in h or "用例" in h for h in header):
            continue
        for row in table[1:]:
            joined = " ".join(row)
            if not TC_RE.search(joined) and not any("tc-" in c.lower() for c in row):
                continue
            tc_rows += 1
            reqs_in_row = unique_reqs(joined)
            if not reqs_in_row:
                orphan += 1
            layer = joined
            is_func = bool(re.search(r"功能", layer)) and not re.search(r"异常|边界", layer[:20])
            # simpler: cell containing 功能
            for r in reqs_in_row:
                key = r if r in func_by_req else r
                if key not in func_by_req:
                    func_by_req[key] = 0
                if re.search(r"功能", joined):
                    func_by_req[key] += 1

    if tc_rows == 0:
        # fallback orphan: TCs in text vs REQ co-occurrence windows
        for tc in tcs:
            m = re.search(re.escape(tc), text, re.IGNORECASE)
            if not m:
                continue
            window = text[max(0, m.start() - 100) : m.start() + 200]
            if not REQ_RE.search(window):
                orphan += 1
        gaps.append("testcase main table weak; orphan heuristic used")

    covered = sum(1 for r, n in func_by_req.items() if n >= 1) if decomp_reqs else 0
    func_ok = sum(1 for r, n in func_by_req.items() if n >= 2) if decomp_reqs else 0
    req_coverage = rate(covered, len(decomp_reqs)) if decomp_reqs else None
    func_layer_rate = rate(func_ok, len(decomp_reqs)) if decomp_reqs else None

    # three-layer: look for 异常 and 边界 mentions per REQ
    for req in decomp_reqs:
        three_total += 1
        # windows of all mentions
        if re.search(rf"{re.escape(req)}[\s\S]{{0,2000}}异常", text) and re.search(
            rf"{re.escape(req)}[\s\S]{{0,2000}}边界", text
        ):
            three_ok += 1
        elif re.search(rf"{re.escape(req)}[\s\S]{{0,800}}N/A", text):
            three_ok += 1

    three_rate = rate(three_ok, three_total) if three_total else None

    # leaf consistency: count TC- in flowchart blocks vs table
    flow_tcs = set()
    for block in re.findall(r"```(?:mermaid)?\s*([\s\S]*?)```", text):
        if "flowchart" in block or "graph" in block:
            flow_tcs |= unique_tcs(block)
    if flow_tcs and tcs:
        leaf_consistency: Any = flow_tcs == tcs or len(flow_tcs) == len(tcs)
    elif not re.search(r"flowchart", text):
        leaf_consistency = "unsupported"
    else:
        leaf_consistency = "unsupported"
        gaps.append("testcase flowchart TC set incomplete")

    parts = [req_coverage, func_layer_rate, three_rate]
    completeness = None
    if all(p is not None for p in parts):
        completeness = round(0.4 * parts[0] + 0.3 * parts[1] + 0.3 * parts[2], 4)  # type: ignore

    tc_count = len(tcs) if tcs else tc_rows
    orphan_rate = rate(orphan, tc_count) if tc_count else None

    return {
        "tc_count": tc_count,
        "req_coverage": req_coverage,
        "func_layer_rate": func_layer_rate,
        "three_layer_complete_rate": three_rate,
        "orphan_rate": orphan_rate,
        "leaf_table_consistency": leaf_consistency,
        "completeness_score": completeness,
    }


def scan_visual(text: str, gaps: List[str]) -> Dict[str, Any]:
    if not text:
        return {}
    p0 = len(re.findall(r"\bP0\b", text))
    p1 = len(re.findall(r"\bP1\b", text))
    # avoid double-counting headers: prefer VA- rows
    va_p0 = len(re.findall(r"VA-\d+[^\n]*P0|\|?\s*P0\s*\|", text))
    va_p1 = len(re.findall(r"VA-\d+[^\n]*P1|\|?\s*P1\s*\|", text))
    return {
        "p0_count": va_p0 or p0,
        "p1_count": va_p1 or p1,
    }


def scan_compile(text: str, gaps: List[str]) -> Dict[str, Any]:
    if not text:
        return {}
    cats = []
    for label in ("lint", "tsc", "typecheck", "build", "bundle"):
        if re.search(label, text, re.IGNORECASE) and re.search(
            rf"{label}[^\n]{{0,40}}(fail|失败|error)", text, re.IGNORECASE
        ):
            cats.append(label)
    return {"first_fail_categories": cats or None}


def scan_review(text: str, gaps: List[str]) -> Dict[str, Any]:
    if not text:
        return {}
    open_p0 = len(re.findall(r"P0[^\n]{0,40}(未关闭|open|待修复)", text, re.IGNORECASE))
    open_p0 += len(re.findall(r"(未关闭|open)[^\n]{0,40}P0", text, re.IGNORECASE))
    return {"open_p0_findings": open_p0}


def collect_red_lights(auto: Dict[str, Any]) -> List[str]:
    red: List[str] = []
    sol = auto.get("solution") or {}
    if sol.get("change_consistency") not in (None, 0):
        red.append("solution.change_consistency!=0")
    if sol.get("drift_events") not in (None, 0):
        red.append("solution.drift_events!=0")
    tc = auto.get("testcase") or {}
    if tc.get("orphan_rate") not in (None, 0):
        red.append("testcase.orphan_rate!=0")
    vis = auto.get("visual") or {}
    if vis.get("p0_count") not in (None, 0):
        red.append("visual.p0_count!=0")
    cg = auto.get("codegen") or {}
    if cg.get("blocked") is True:
        red.append("codegen.blocked")
    return red


def render_md(data: Dict[str, Any]) -> str:
    auto = data.get("auto") or {}
    sources = data.get("sources") or {}
    versions = data.get("versions") or {}

    def block(title: str, obj: Dict[str, Any]) -> str:
        if not obj:
            return f"### {title}\n\n（无数据）\n"
        lines = [f"### {title}", "", "| 指标 | 值 |", "|------|-----|"]
        for k, v in obj.items():
            if k in ("reqs", "reqs_only_in_solution", "reqs_only_in_decomp"):
                continue
            lines.append(f"| {k} | {v} |")
        return "\n".join(lines) + "\n"

    parts = [
        f"# 流水线观测 — {data.get('requirement_name')} v{data.get('metrics_version')}",
        "",
        "| 字段 | 内容 |",
        "|------|------|",
        f"| run_id | {data.get('run_id')} |",
        f"| scanned_at | {data.get('scanned_at')} |",
        f"| status | {data.get('status')} |",
        f"| 拆解 | {sources.get('decomp')} / {versions.get('decomp')} |",
        f"| 方案 | {sources.get('solution')} / {versions.get('solution')} |",
        f"| 用例 | {sources.get('testcase')} / {versions.get('testcase')} |",
        f"| 架构对齐 | {sources.get('alignment')} |",
        f"| 视觉 | {sources.get('visual')} |",
        f"| 编译 | {sources.get('compile')} |",
        f"| 审查 | {sources.get('review')} |",
        "",
        "## 1. 红灯与缺口",
        "",
        f"- **red_lights**：{', '.join(data.get('red_lights') or []) or '（无）'}",
        f"- **gaps**：{', '.join(data.get('gaps') or []) or '（无）'}",
        "",
        "## 2. 自动扫描（L1/L2）",
        "",
        block("拆解", auto.get("decomp") or {}),
        block("方案", auto.get("solution") or {}),
        block("实现（架构对齐）", auto.get("codegen") or {}),
        block("用例", auto.get("testcase") or {}),
        block("视觉", auto.get("visual") or {}),
        block("编译", auto.get("compile") or {}),
        block("审查", auto.get("review") or {}),
        "## 3. 人工抽检（L3）",
        "",
        "| 指标 | 值 |",
        "|------|-----|",
        f"| capability_loss_rate | {(data.get('human') or {}).get('capability_loss_rate')} |",
        f"| atomicity_pass_rate | {(data.get('human') or {}).get('atomicity_pass_rate')} |",
        "",
        "抽检明细按 `references/rubric-semantic.md` 填写。",
        "",
        "## 4. 结论",
        "",
        "- [ ] L1 红灯已解释或已清零",
        "- [ ] 未用单一「合理性分」替代门禁",
        "- [ ] JSON 已落盘且版本未覆盖旧文件",
        "",
        "**一句话**：（待填）",
        "",
    ]
    return "\n".join(parts)


def resolve_sources(root: Path, name: str, args: argparse.Namespace) -> Dict[str, Optional[Path]]:
    return {
        "decomp": Path(args.decomp) if args.decomp else find_latest(root, ["docs/prd/**/*.md", "docs/ai/requirements/**/*.md"], name),
        "solution": Path(args.solution) if args.solution else find_latest(root, ["docs/design/**/*.md", "docs/ai/solution/**/*.md"], name),
        "testcase": Path(args.testcase) if args.testcase else find_latest(root, ["docs/testcase/**/*.md"], name),
        "alignment": Path(args.alignment) if args.alignment else find_latest(
            root, ["docs/ai/codegen/**/*架构对齐*", "docs/ai/codegen/**/*alignment*"], name
        ),
        "visual": Path(args.visual) if args.visual else find_latest(
            root, ["docs/ai/visual-audit/**/*.md"], name
        ),
        "compile": Path(args.compile) if args.compile else find_latest(
            root, ["docs/ai/compile-verify/**/*.md"], name
        ),
        "review": Path(args.review) if args.review else find_latest(
            root, ["docs/ai/review/**/*.md"], name
        ),
    }


def guess_version(path: Optional[Path]) -> Optional[str]:
    if not path:
        return None
    m = re.search(r"v(\d+\.\d+(?:\.\d+)?)", path.name, re.IGNORECASE)
    return m.group(0) if m else None


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Scan pipeline artifacts → metrics JSON/MD")
    parser.add_argument("--root", required=True, help="Project root")
    parser.add_argument("--name", required=True, help="Requirement name hint")
    parser.add_argument("--version", default="0.1", help="Metrics version x.y")
    parser.add_argument("--strict", action="store_true", help="Hard red lights → status=blocked")
    parser.add_argument("--decomp", default=None)
    parser.add_argument("--solution", default=None)
    parser.add_argument("--testcase", default=None)
    parser.add_argument("--alignment", default=None)
    parser.add_argument("--visual", default=None)
    parser.add_argument("--compile", default=None)
    parser.add_argument("--review", default=None)
    parser.add_argument("--out-dir", default=None, help="Default: <root>/docs/ai/metrics")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"root not found: {root}", file=sys.stderr)
        return 2

    sources = resolve_sources(root, args.name, args)
    gaps: List[str] = []
    decomp_text = read_text(sources["decomp"])
    solution_text = read_text(sources["solution"])
    testcase_text = read_text(sources["testcase"])
    alignment_text = read_text(sources["alignment"])
    visual_text = read_text(sources["visual"])
    compile_text = read_text(sources["compile"])
    review_text = read_text(sources["review"])

    decomp = scan_decomp(decomp_text, gaps)
    decomp_reqs = set(decomp.get("reqs") or unique_reqs(decomp_text))
    solution = scan_solution(solution_text, decomp_reqs, decomp_text, gaps)
    codegen = scan_codegen(alignment_text, gaps)
    testcase = scan_testcase(testcase_text, decomp_reqs, gaps)
    visual = scan_visual(visual_text, gaps)
    compile_m = scan_compile(compile_text, gaps)
    review = scan_review(review_text, gaps)

    # strip helper lists from exported decomp if desired — keep reqs for debug but schema allows
    auto = {
        "decomp": {k: v for k, v in decomp.items() if k != "reqs"},
        "solution": {k: v for k, v in solution.items() if not k.startswith("reqs_")},
        "codegen": codegen,
        "testcase": testcase,
        "visual": visual,
        "compile": compile_m,
        "review": review,
    }
    # keep drift detail in solution extras inside gaps if large
    if solution.get("reqs_only_in_solution") or solution.get("reqs_only_in_decomp"):
        gaps.append(
            "drift detail: only_sol=%s only_decomp=%s"
            % (solution.get("reqs_only_in_solution"), solution.get("reqs_only_in_decomp"))
        )

    red = collect_red_lights(auto)
    status = "ok"
    if gaps and (not decomp_text and not solution_text):
        status = "partial"
    elif gaps:
        status = "partial"
    if args.strict and red:
        status = "blocked"
    elif red and status == "ok":
        status = "partial"

    ver = args.version.lstrip("v")
    out_dir = Path(args.out_dir) if args.out_dir else root / "docs" / "ai" / "metrics"
    out_dir.mkdir(parents=True, exist_ok=True)
    base = f"{args.name}-metrics-v{ver}"
    json_path = out_dir / f"{base}.json"
    md_path = out_dir / f"{base}.md"
    if json_path.exists() or md_path.exists():
        print(f"refusing to overwrite existing metrics: {json_path}", file=sys.stderr)
        return 3

    data = {
        "schema_version": "1.0",
        "run_id": f"{args.name}-v{ver}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "scanned_at": utc_now(),
        "requirement_name": args.name,
        "metrics_version": ver,
        "root": str(root),
        "sources": {k: (str(v) if v else None) for k, v in sources.items()},
        "versions": {
            "decomp": guess_version(sources["decomp"]),
            "solution": guess_version(sources["solution"]),
            "codegen": guess_version(sources["alignment"]),
            "testcase": guess_version(sources["testcase"]),
        },
        "auto": auto,
        "human": {
            "capability_loss_rate": None,
            "atomicity_pass_rate": None,
            "atomicity_sample": None,
            "rubric_samples": None,
            "notes": None,
        },
        "red_lights": red,
        "gaps": gaps,
        "status": status,
    }

    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_md(data), encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    print(f"status={status} red_lights={len(red)} gaps={len(gaps)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
