---
name: quick-pipeline-observability
description: "增量 Skill 流水线观测：只读扫描拆解/方案/架构对齐/用例/VA/编译/审查产物，计算 L1/L2 指标（覆盖、漂移、首次完整度、用例完成度等），产出 docs/ai/metrics JSON+报告；支持多需求 rollup 周报；L3 语义用 rubric 抽检写入 human。无埋点平台。Actions: 观测, 指标, metrics, 扫描, rollup, 评测, 完整度, 漂移, 丢失率. Objects: docs/prd, docs/design, docs/testcase, 架构对齐报告, VA清单. Triggers: 流水线观测, 算指标, metrics, 质量看板, 交付后扫描, 周报汇总."
---

# 流水线观测（Pipeline Observability）

**语言**：说明与报告默认中文；指标键名、REQ/TC/OPEN、JSON 字段保持英文/编号原样。

IRON LAW：**观测只读**——禁止为凑指标改写上游拆解/方案/用例/对齐报告。禁止用单一「合理性分」或 LLM 自评替代 L1 红灯与既有 skill 门禁。

IRON LAW（统计）：**无埋点平台**。数据来自仓库产物扫描；单次写入 `docs/ai/metrics/{需求名}-metrics-v{x.y}.json`；升版不覆盖；跨需求用 `scan_metrics_rollup.py`。详见 `references/metric-dictionary.md`、`references/evaluation-methods.md`。

## 工作流

```
流水线观测进度：

- [ ] 步骤 1：定位本迭代产物路径 ⚠️ REQUIRED
- [ ] 步骤 2：运行扫描脚本（或等价手工填表）⚠️ REQUIRED
- [ ] 步骤 3：L3 抽检写入 human（10%～20% REQ）⚠️ REQUIRED
- [ ] 步骤 4：确认门 ⚠️ REQUIRED
- [ ] 步骤 5：落盘 JSON + MD；可选 rollup ⚠️ REQUIRED
```

## 步骤 1：定位产物

在项目根确认（缺则记入 gaps，不中断）：

| 产物 | 典型路径 |
|------|----------|
| 拆解 | `docs/prd/{需求名}-v*.md` |
| 方案 | `docs/design/**` |
| 用例 | `docs/testcase/**` |
| 架构对齐 | `docs/ai/codegen/*架构对齐*` |
| 视觉 | `docs/ai/visual-audit/**` |
| 编译 | `docs/ai/compile-verify/**` |
| 审查 | `docs/ai/review/**` |

加载 `references/metric-dictionary.md` 核对可扫描标题别名。

## 步骤 2：扫描

优先执行（路径相对本 skill 安装目录或仓库内源码路径）：

```bash
python scripts/scan_pipeline_metrics.py \
  --root <项目根> \
  --name <需求名> \
  --version <x.y>
```

可选：`--decomp` / `--solution` / `--testcase` / `--alignment` 等覆盖自动发现；`--strict` 时硬红灯 → `status=blocked`。

无 Python 时：按 `references/report-template.md` + `run-schema.md` 手工建 JSON/MD，`auto` 能算则算，否则 `null` + gaps。

## 步骤 3：人工抽检（L3）

加载 `references/rubric-semantic.md`，抽检本迭代 10%～20% REQ（至少 3 条），回填 `human.capability_loss_rate`、`human.atomicity_pass_rate`（推荐新建 patch 版本如 `v0.1.1`，见 `run-schema.md`）。

## 步骤 4：确认门

向用户展示：

- `status`、`red_lights`、`gaps`
- 关键自动指标：`solution.change_consistency`、`codegen.first_pass_rate`、`testcase.completeness_score` / `orphan_rate`、`visual.p0_count`
- L3 待填或已填结果

**禁止**：L1 红灯未解释时宣称「全链路质量优秀」或「观测通过可合入」。

## 步骤 5：落盘与汇总

- 默认：`docs/ai/metrics/{需求名}-metrics-v{x.y}.json` + `.md`
- 多需求周/月：

```bash
python scripts/scan_metrics_rollup.py --root <项目根> --period week
```

加载 `references/evaluation-methods.md` 做复盘归因（可选）。

## Anti-Patterns

- 覆盖旧 metrics 版本文件
- 改上游文档消灭 red_lights
- 无扫描、仅聊天口头「完整度 90%」
- 把 rollup 当成实时埋点大盘而自建后端

## Pre-Delivery Checklist

- [ ] 扫描已跑或等价手工 schema 齐全
- [ ] JSON/MD 落在 `docs/ai/metrics/` 且未覆盖旧版
- [ ] red_lights / gaps 已在确认门呈现
- [ ] human 段已抽检或显式推迟并写 notes
- [ ] 未修改上游产物

## 与相邻技能的关系

- 消费：`quick-requirement-decomposition`、`quick-tech-solution`、`quick-req-driven-codegen`、`quick-requirement-testcase-trace`、`quick-visual-audit`、`quick-compile-verify`、`quick-arch-security-code-review` 的落盘产物。
- 不替代各 skill 自身门禁；本 skill 提供**跨阶段可对比指标**。
