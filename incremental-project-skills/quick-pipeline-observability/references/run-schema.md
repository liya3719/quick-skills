# Metrics Run Schema

> **何时加载**：实现/修改扫描脚本、手工补 `human`、对接 rollup 时。

## 落盘路径

| 产物 | 路径 |
|------|------|
| 单需求 JSON | `docs/ai/metrics/{需求名}-metrics-v{x.y}.json` |
| 单需求报告 | `docs/ai/metrics/{需求名}-metrics-v{x.y}.md` |
| 周期汇总 | `docs/ai/metrics/_rollup-YYYY-WW.md`（可选 `_rollup-YYYY-WW.json`） |

版本号与 metrics 文件名一致；**禁止覆盖**已有版本文件。

## JSON 结构

```json
{
  "schema_version": "1.0",
  "run_id": "string",
  "scanned_at": "ISO-8601",
  "requirement_name": "string",
  "metrics_version": "0.1",
  "root": "绝对或相对项目根",
  "sources": {
    "decomp": "path|null",
    "solution": "path|null",
    "testcase": "path|null",
    "alignment": "path|null",
    "visual": "path|null",
    "compile": "path|null",
    "review": "path|null"
  },
  "versions": {
    "decomp": "string|null",
    "solution": "string|null",
    "codegen": "string|null",
    "testcase": "string|null"
  },
  "auto": {
    "decomp": {},
    "solution": {},
    "codegen": {},
    "testcase": {},
    "visual": {},
    "compile": {},
    "review": {}
  },
  "human": {
    "capability_loss_rate": null,
    "atomicity_pass_rate": null,
    "atomicity_sample": null,
    "rubric_samples": null,
    "notes": null
  },
  "red_lights": ["string"],
  "gaps": ["string"],
  "status": "ok|partial|blocked"
}
```

## `status` 判定

| 值 | 条件 |
|----|------|
| `ok` | 至少解析到拆解或方案之一；无 L1 硬红灯（见下）；`gaps` 可为空 |
| `partial` | 关键产物缺失或多项指标 `null`，但仍写出已算部分 |
| `blocked` | `codegen.blocked==true`，或存在未解释的硬红灯且确认门未放行（脚本默认：硬红灯 → 仍写文件，`status=partial`，由人在报告中改述；若 `--strict` 则硬红灯 → `blocked`） |

### 硬红灯（写入 `red_lights`）

- `solution.change_consistency` 存在且 ≠ 0
- `testcase.orphan_rate` 存在且 ≠ 0
- `visual.p0_count` 存在且 ≠ 0
- `codegen.blocked` == true
- `solution.drift_events` 存在且 ≠ 0（仅自动部分）

## `auto` 子对象键名

与 `metric-dictionary.md` 一致。比率类用 `0..1` 浮点；计数用整数；无法解析用 `null`；`leaf_table_consistency` 可为 `true`/`false`/`"unsupported"`。

## `human` 填写

扫描脚本写出时全部为 `null`。人工或 Agent 按 `rubric-semantic.md` 回填后**可新建更高 metrics 版本**或就地编辑（团队约定二选一；推荐新建 patch 版本如 `v0.1.1` 仅含 human 更新并在 notes 说明）。
