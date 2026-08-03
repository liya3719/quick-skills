# 评测方法

> **何时加载**：制定观测节奏、做 skill 回归或复盘归因时。

## 1. 结构扫描（默认、每需求）

**时机**：需求交付或 flow 末步。

**步骤**：

1. 定位本迭代产物路径（见 SKILL 步骤 1）。
2. 运行：

```bash
python scripts/scan_pipeline_metrics.py \
  --root <项目根> \
  --name <需求名> \
  --version 0.1
```

3. 阅读生成的 JSON/`gaps`；L1 红灯须解释后方可宣称「可合入观测通过」。
4. 禁止修改上游文档「凑指标」。

**统计含义**：单次关单采样；无埋点平台（见 `metric-dictionary.md`「无平台统计约定」）。

---

## 2. 多需求 / 周期汇总

```bash
python scripts/scan_metrics_rollup.py \
  --root <项目根> \
  --glob 'docs/ai/metrics/**/*-metrics-v*.json' \
  --period week
```

输出 `_rollup-YYYY-WW.md`（及可选 JSON）：需求数、L1 红灯率、`first_pass_rate` 均值、`orphan_rate` 均值、`human` 已填比例。

---

## 3. 黄金集（skill 仓回归）

本期**先定规范**，fixtures 可后补。

**包内容**（每个 case）：

- 迷你 PRD 快照
- 期望 REQ 清单（含必须 OPEN 的项）
- 可选：期望附录对齐、期望 TC 层数

**跑法**：用固定输入跑拆解→方案→（可选）用例/codegen 计划 → 再跑 observability；对比期望集合差。

**通过标准**：能力点覆盖差 ≤ 约定阈值；`change_consistency==0`；无 orphan TC。

---

## 4. 语义抽检（L3）

加载 `rubric-semantic.md`。

- **抽样**：本迭代 REQ 的 10%～20%（至少 3 条，不足则全抽）。
- **记录**：写入 metrics JSON 的 `human` 段与报告「人工抽检」表。
- **禁止**：用 LLM 自评单一「合理性分」替代 checklist；不得作为唯一合入门禁。

---

## 5. 后验归因（两周复盘）

联调 / 线上 / QA 问题打**唯一主因标签**：

| 标签 | 含义 |
|------|------|
| `decomp_loss` | 拆解未覆盖或验收不可测 |
| `solution_drift` | 方案相对拆解漂移或发明 |
| `impl_gap` | 实现对齐报告缺口 / 回流不足 |
| `testcase_wrong` | 用例错或不可执行 |
| `design_data` | design/ metadata 或缺确认 |
| `other` | 其它（须一句说明） |

落盘建议：`docs/ai/metrics/_postmortem-YYYY-WW.md` 表格（日期、问题摘要、标签、关联 REQ）。两周看标签分布，指导改 skill 或确认门，而非加埋点。

---

## 6. 升版对比

同一 `{需求名}` 保留 `metrics-v0.1`、`v0.2`…：

- 自动：diff `auto.*` 数值
- 人工：确认 L3 是否随整改改善

禁止在旧 metrics 文件上覆盖写新采样。
