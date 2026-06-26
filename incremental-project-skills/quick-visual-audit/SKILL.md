---
name: quick-visual-audit
description: "UI 视觉审计：对比 quick-req-driven-codegen 产出与设计 metadata(Figma/MasterGo/token JSON)，校验布局、间距、字号、颜色、组件状态、资源、响应式与多端差异；输出可回流偏差清单(VA-xxx)供 codegen 精准修复，非截图目测。Actions: 视觉审计, UI 验收, 设计还原, 走查 UI, 对比设计稿, metadata 对账, 偏差清单, 还原度检查. Objects: Figma/MasterGo metadata, design token JSON, 执行计划 block, 架构对齐报告, REQ-xxx. Stacks: Vue3, React, ZRN, Tailwind, SCSS. Triggers: 视觉审计, UI 对稿, 检查还原度, 设计 metadata 对比, 间距字号颜色不对, 组件状态缺失, 响应式偏差, 多端 UI 差异."
argument-hint: "[--scope block|page|all] [--platform web|native|all] [--reflux-rounds N] 默认 all+web；reflux-rounds 默认 3（与 codegen 回流上限对齐）"
---

# UI 视觉审计

**语言**：偏差清单、报告默认**中文**；保留 metadata 节点 id、token 名、组件符号、REQ-xxx 为原样。

IRON LAW：**禁止凭截图、聊天图片或主观目测代替 metadata/token 数值对比。** **禁止在本 skill 内直接改 UI 代码或发明设计规格**——只产出带定位的偏差清单，由 **`quick-req-driven-codegen`** 按清单修复。**无设计 metadata 且未标 UI-N/A 时，禁止输出 pass。** **每条偏差须可追溯到 metadata 字段或 token 名 + 代码位置，否则不得列入可修复清单。**

Red Flags（出现则回到步骤 0）：

- 仅有 PNG/JPG 无 metadata 却做「通过」结论
- 偏差项无「设计值 vs 实现值」双列
- 把编译错误、接口逻辑问题混入视觉偏差
- 未读执行计划 block 映射就全仓扫样式
- 本 skill 内擅自改 `.vue`/`.tsx` 样式
- 无偏差却标 pass（未覆盖任一 ready UI block）

## Workflow

```
视觉审计进度：

- [ ] 步骤 0：前置与范围 ⛔ BLOCKING
  - [ ] 0.1 执行计划 + 架构对齐报告路径；UI block 列表
  - [ ] 0.2 设计 metadata + token JSON 路径（与 codegen 步骤 1 一致）
  - [ ] 0.3 scope：block / page / all；platform：web / native / all
  - [ ] 0.4 reflux-rounds 上限（默认 3，与 codegen 对齐）
- [ ] 步骤 1：建立对账映射 ⛔ BLOCKING
  - [ ] 加载 `references/metadata-to-code-mapping.md`
  - [ ] block / metadata 节点 id → 组件文件 / 选择器
  - [ ] 缺映射 → OPEN 或 blocked，不臆造节点
- [ ] 步骤 2：分维度审计 ⚠️ REQUIRED
  - [ ] 加载 `references/audit-dimensions.md`
  - [ ] 布局 → 间距 → 字号 → 颜色 → 状态 → 资源 → 响应式 → 多端
- [ ] 步骤 3：偏差分级 ⛔ BLOCKING
  - [ ] 加载 `references/deviation-severity.md`
  - [ ] 每条标 P0/P1/P2；P0 须 codegen 回流
- [ ] 步骤 4：落盘偏差清单 ⚠️ REQUIRED
  - [ ] 加载 `references/deviation-list-template.md`
  - [ ] 默认：`docs/ai/visual-audit/{需求名}-视觉偏差清单-v{x.y}.md`
- [ ] 步骤 5：回流 codegen ⛔ BLOCKING（存在 P0/P1 且未达 reflux 上限）
  - [ ] 将 VA-xxx 清单交给 `quick-req-driven-codegen` 按 block 修复
  - [ ] 修复后重跑本 skill；更新清单「回流记录」
  - [ ] 达上限仍 P0 → blocked，交产品/设计 OPEN
- [ ] 步骤 6：门禁结论
  - [ ] pass → 可进入 `quick-compile-verify`
  - [ ] blocked → 禁止宣称 UI 验收通过
```

## 步骤 0：前置与范围 ⛔ BLOCKING

自问：

- 哪些 block 为 **ready** 且含 UI？（执行计划表）
- metadata 与 token JSON 是否已 Read？路径是否与对齐报告 §6 一致？
- 本次 **UI-N/A** 的 REQ 是否已用户确认？（是则整单标 N/A，不审计 UI）
- 多端：Web only / 含 ZRN·RN / 含 Harmony 独立稿？

## 步骤 1：对账映射

加载 `references/metadata-to-code-mapping.md`。

**映射表**（审计前必填）：

| block id | REQ | metadata 节点 id / 层名 | 组件/文件 | 平台 |
|----------|-----|---------------------------|-----------|------|

无法建立映射的 block → **blocked-映射**，不得对该 block 标 pass。

## 步骤 2：分维度审计

加载 `references/audit-dimensions.md`。

对每个已映射 block，按维度提取 **设计值**（metadata/token）与 **实现值**（代码/CSS/主题变量），记录偏差。

**禁止**用「看起来差不多」；数值型须同单位对比（px/rem/token 名）。

## 步骤 3：偏差分级

加载 `references/deviation-severity.md`。

| 级别 | 典型 |
|------|------|
| **P0** | 布局结构错误、主色/品牌色错误、关键状态缺失、错误资源 |
| **P1** | 间距/字号超容差、次要状态、响应式断点错误 |
| **P2** | 轻微视觉差、待设计补 token |

## 步骤 4：偏差清单

加载 `references/deviation-list-template.md`。

每条偏差 **VA-xxx** 须含：block、维度、设计值、实现值、代码位置、建议修复动作（供 codegen）、严重度。

## 步骤 5：回流 codegen

本 skill **不修改** UI 源码。存在 P0/P1 时：

1. 交付偏差清单路径给 **`quick-req-driven-codegen`**
2. codegen 仅改清单列出的文件/属性，更新对齐报告 §6/§8
3. 重跑本 skill；清单追加「回流记录」

**reflux-rounds**（默认 3）：与 codegen missing 回流计数对齐；用尽仍 P0 → **blocked**。

## 步骤 6：门禁

| 结果 | 条件 |
|------|------|
| **pass** | 已映射 UI block 无 P0/P1；P2 已列或 OPEN |
| **fixed-pass** | 经回流后满足 pass |
| **blocked** | 无 metadata、映射失败、reflux 用尽仍 P0、或设计 OPEN 未解 |

## 确认门 ⚠️ REQUIRED

- 容差放宽（如间距 ±4px → ±8px）→ 须用户或设计确认
- 建议改 metadata/token 真源而非代码 → 标 OPEN，不擅自改 JSON
- 用户只要报告、不要回流 → 步骤 5 仅交付清单

## Anti-Patterns

- 截图对比代替 metadata 字段
- 在本 skill 内直接改样式过审计
- 把 lint/TS 报错写进偏差清单
- 无「设计值 vs 实现值」的模糊描述（「间距偏大」）
- 忽略响应式/多端只审 desktop Web
- 未映射 block 标 pass

## Pre-Delivery Checklist

- [ ] metadata + token 路径已记录且已 Read
- [ ] 映射表覆盖所有待审计 ready UI block
- [ ] 每条 VA-xxx 含双列数值/ token 名 + 代码位置
- [ ] P0/P1 与 codegen 回流动作明确
- [ ] 《视觉偏差清单》已落盘
- [ ] 未在本 skill 内改 UI 代码
- [ ] blocked 时未宣称 pass

## 与相邻技能的关系

- **quick-req-driven-codegen**：上游实现 + 下游 UI 修复；消费本清单 VA-xxx 按 block 精准改代码。
- **quick-compile-verify**：视觉 pass 后建议再跑编译；编译问题不在此 skill 处理。
- **quick-tech-solution**：交互/状态定义以方案为准；与 metadata 冲突标 OPEN。
