# 指标字典

> **何时加载**：扫描前 / 填写 human 段 / 解读报告时。

## 无平台统计约定

- **数据源**：仓库内 Markdown/JSON 产物（拆解、方案、架构对齐、用例、VA、CR）。
- **单次采样**：`scan_pipeline_metrics.py` → `docs/ai/metrics/{需求名}-metrics-v{x.y}.json`
- **升版对比**：禁止覆盖旧 metrics；diff 两版 JSON 或 git history。
- **多需求汇总**：`scan_metrics_rollup.py` → `_rollup-YYYY-WW.md`（+ 可选 `_rollup.json`）。
- **不做**：埋点 SDK、实时大盘、服务端上报。

解析失败时该指标为 `null`，run `status` 为 `partial`，并写入 `gaps[]`。

## 指标分层

| 层 | 含义 | 采集 |
|----|------|------|
| L1 | 结构完备 | 自动扫描 |
| L2 | 过程健康 | 自动扫描（回流、OPEN、blocked） |
| L3 | 语义质量 | 人工 rubric → `human` |

---

## 需求拆解 `decomp.*`

| 键 | 层 | 公式 / 操作定义 | 红灯建议 |
|----|----|-----------------|----------|
| `req_count` | L1 | 拆解稿中唯一 `REQ-\d+` 条数 | — |
| `open_count` | L1 | 唯一 `OPEN-\d+` 条数 | — |
| `testability_rate` | L1 | 有验收线索（非纯 BLOCKED）的 REQ / `req_count`；分母 0 → `null` | &lt; 0.8 |
| `open_density` | L2 | `open_count / req_count` | &gt; 0.5 |
| `three_view_complete_rate` | L1 | §6 三视图矩阵中「齐全或显式 N/A」行 / 矩阵行数；无矩阵 → `null` | &lt; 1.0 |
| `capability_loss_rate` | L3 | 评审能力点未落入任一 REQ 的比例（见 rubric） | &gt; 0.1 |
| `atomicity_pass_rate` | L3 | 抽检原子性合格条数 / 抽检条数 | &lt; 0.8 |

**口语「丢失率」** → 优先用 `capability_loss_rate`（L3）；后验可用复盘归因「拆解丢失」计数。

**口语「合理性」** → 不用单一分数；用 `atomicity_pass_rate` + rubric 分项 0/1。

---

## 技术方案 `solution.*`

| 键 | 层 | 公式 / 操作定义 | 红灯建议 |
|----|----|-----------------|----------|
| `req_in_appendix_a` | L1 | 附录 A（或标题含「需求追溯」）中出现的 REQ 集合大小 | — |
| `req_coverage` | L1 | `|附录A ∩ 拆解REQ| / |拆解REQ|`；无方案 → `null` | &lt; 1.0 |
| `change_consistency` | L1 | `|附录D REQ △ 拆解§9.2 REQ|`（对称差大小）；首版无变更节可记 0 | ≠ 0 |
| `orphan_anchor_rate` | L1/L2 | 启发式：方案中接口/错误码行既无 REQ 又无「工程补充」的占比；不可解析 → `null` | &gt; 0 |
| `drift_events` | L1 | `(方案多出的 REQ 数) + (拆解有方案无的 REQ 数)`；另加人工「同 REQ 验收改写未升版」计入 human | ≠ 0 |

**口语「是否漂移」** → `change_consistency` + `drift_events` +（抽检）验收改写。

---

## 代码实现 `codegen.*`

扫描目标：`docs/ai/codegen/*架构对齐*`（别名：架构对齐报告、回流记录）。

| 键 | 层 | 公式 / 操作定义 | 红灯建议 |
|----|----|-----------------|----------|
| `critical_pass` / `critical_total` | L1 | 报告中关键项 pass 数 / 关键项总数（表格状态列） | — |
| `first_pass_rate` | L2 | **回流 round0**（首轮、首次）关键项 pass / 关键项；无回流记录则用当前关键项比例并标 `gaps` | &lt; 0.8 |
| `p0_req_first_cover` | L2 | 至少 1 个 block=`pass` 的 P0 REQ / P0 REQ 总数；无 P0 标注 → `null` | &lt; 1.0 |
| `reflow_rounds` | L2 | 「回流记录」中最大轮次；无则 0 | ≥ 5 或仍 blocked |
| `unapproved_delta_count` | L1 | §8 偏差表非空行数（或「偏差」节下列表项） | ≠ 0 |
| `blocked` | L2 | 报告宣称整单 blocked 或关键项未全 pass 且轮次≥5 | true |

**口语「首次实现完整度」** → `first_pass_rate`（辅看 `reflow_rounds`）。

---

## 测试用例 `testcase.*`

| 键 | 层 | 公式 / 操作定义 | 红灯建议 |
|----|----|-----------------|----------|
| `tc_count` | L1 | 主表或全文唯一 `TC-` 编号数 | — |
| `req_coverage` | L1 | 至少绑定 1 条功能层 TC 的 REQ / 范围内 REQ | &lt; 1.0 |
| `func_layer_达标率` / `func_layer_rate` | L1 | 功能 TC≥2（或文档写明收窄）的 REQ / REQ | &lt; 0.9 |
| `three_layer_complete_rate` | L1 | 有异常+边界派生或显式 N/A 的功能锚点比例 | &lt; 0.8 |
| `orphan_rate` | L1 | 无 `REQ-` 绑定的 TC / `tc_count` | ≠ 0 |
| `leaf_table_consistency` | L1 | flowchart 叶子中 TC 数 == 主表 TC 数；无法解析 → `"unsupported"` | false |
| `completeness_score` | 合成 | `0.4*req_coverage + 0.3*func_layer_rate + 0.3*three_layer_complete_rate`（缺项则 `null`） | &lt; 0.85 |

**口语「测试用例完成度」** → `completeness_score`。

---

## 视觉 / 编译 / 审查

| 键 | 层 | 定义 | 红灯 |
|----|----|------|------|
| `visual.p0_count` / `p1_count` | L1 | 偏差清单中 P0/P1 条数 | p0 ≠ 0 |
| `compile.first_fail_categories` | L2 | 首跑失败类别列表（lint/tsc/build…）；无报告 → `null` | — |
| `review.open_p0_findings` | L1 | 未关闭 P0/高危 finding 数；无报告 → `null` | ≠ 0 |

---

## 可扫描标题别名（脚本匹配）

| 产物节 | 接受标题（含则匹配） |
|--------|----------------------|
| 三视图矩阵 | `追溯矩阵`、`三视图`、`§6` |
| 三向矩阵 | `三向追溯`、`三向矩阵` |
| §9.2 变更 | `9.2`、`REQ 级变更`、`变更明细` |
| 附录 A | `附录 A`、`需求追溯` |
| 附录 D | `附录 D`、`本版变更` |
| 回流 | `回流记录`、`回流` |
| 偏差 | `偏差`、`§8` |
| 关键项 | `关键项`、`分块对齐` |
