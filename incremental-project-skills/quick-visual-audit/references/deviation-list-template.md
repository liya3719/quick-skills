# 视觉偏差清单模板

## 何时加载

步骤 4 落盘时。

## 默认路径

`docs/ai/visual-audit/{需求名}-视觉偏差清单-v{x.y}.md`

## 模板

```markdown
# 视觉偏差清单 — {需求名} v{x.y}

## 1. 元数据
- 执行计划：
- 对齐报告：
- design JSON：（各 block 路径）
- design PNG：（各 block 路径）
- token JSON：（如有）
- scope / platform：
- 回流轮次：n / 上限 N
- 数据确认：步骤 1 pass / blocked

## 2. 映射表
| block | REQ | JSON 路径+节点 | PNG 路径 | 文件/组件 | 平台 |
|-------|-----|----------------|----------|-----------|------|

## 3. 偏差明细
| ID | block | 维度 | 严重度 | 设计值 | 实现值 | 代码位置 | 建议修复（codegen） |
|----|-------|------|--------|--------|--------|----------|---------------------|
| VA-001 | B-01 | spacing | P1 | gap: 16 / spacing-md | gap: 8px | src/.../Foo.vue:42 | 改用 var(--spacing-md) |

## 4. 汇总
- P0：n  P1：n  P2：n  OPEN：n

## 5. 回流记录
| 轮次 | 交给 codegen 的 VA | 修复摘要 | 复审计结果 |

## 6. 门禁结论
- pass / fixed-pass / blocked
- 可否进入 compile-verify：是 / 否
```

## VA-xxx 字段要求

- **设计值**：JSON 字段 / token 名 + 数值，或 PNG 基准描述 + 路径
- **实现值**：代码/CSS/类名 + 数值
- **建议修复**：具体到 token 名或属性，非「改好看点」

## 禁止

- 空表却结论 pass
- 建议修复含改业务逻辑/API
