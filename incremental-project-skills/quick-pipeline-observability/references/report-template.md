# 流水线观测报告模板

> **何时加载**：生成或审阅 `docs/ai/metrics/{需求名}-metrics-v{x.y}.md`。

脚本可自动填「自动扫描」节；「人工抽检」由确认门后补全。

```markdown
# 流水线观测 — {需求名} v{x.y}

| 字段 | 内容 |
|------|------|
| run_id | |
| scanned_at | |
| status | ok / partial / blocked |
| 拆解 | path + 版本 |
| 方案 | path + 版本 |
| 用例 | path + 版本 |
| 架构对齐 | path |
| 视觉 / 编译 / 审查 | path 或 N/A |

## 1. 红灯与缺口

- **red_lights**：…
- **gaps**：…

## 2. 自动扫描（L1/L2）

### 拆解
| 指标 | 值 |
|------|-----|
| req_count | |
| open_count | |
| testability_rate | |
| open_density | |
| three_view_complete_rate | |

### 方案
| 指标 | 值 |
|------|-----|
| req_coverage | |
| change_consistency | |
| drift_events | |
| orphan_anchor_rate | |

### 实现（架构对齐）
| 指标 | 值 |
|------|-----|
| first_pass_rate | |
| p0_req_first_cover | |
| reflow_rounds | |
| unapproved_delta_count | |
| blocked | |

### 用例
| 指标 | 值 |
|------|-----|
| req_coverage | |
| func_layer_rate | |
| three_layer_complete_rate | |
| orphan_rate | |
| leaf_table_consistency | |
| completeness_score | |

### 视觉 / 编译 / 审查
| 指标 | 值 |
|------|-----|
| visual.p0_count / p1_count | |
| compile.first_fail_categories | |
| review.open_p0_findings | |

## 3. 人工抽检（L3）

| 指标 | 值 |
|------|-----|
| capability_loss_rate | （待填） |
| atomicity_pass_rate | （待填） |

抽检明细见 `references/rubric-semantic.md` 表。

## 4. 结论

- [ ] L1 红灯已解释或已清零
- [ ] 未用单一「合理性分」替代门禁
- [ ] JSON 已落盘且版本未覆盖旧文件

**一句话**：…
```
