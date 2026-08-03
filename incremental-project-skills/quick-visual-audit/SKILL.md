---
name: quick-visual-audit
description: "UI 视觉审计：审计前从 design/ 定位配对 *.json(结构数值)+*.png(视觉基准)，数据确认通过后对比 codegen 实现；校验布局、间距、字号、颜色、状态、资源、响应式与多端；输出 VA 偏差清单回流 quick-req-driven-codegen。Actions: 视觉审计, UI验收, 设计还原, 走查UI, 对比设计稿, design json, design png, 偏差清单. Objects: design/*.json, design/*.png, 执行计划, 架构对齐报告, REQ-xxx. Stacks: Vue3, React, ZRN, Tailwind. Triggers: 视觉审计, UI对稿, 检查还原度, design目录, 间距字号颜色不对, 组件状态缺失."
argument-hint: "[--scope block|page|all] [--platform web|native|all] [--reflux-rounds N] 默认 all+web；reflux-rounds 默认 3（与 codegen 回流上限对齐）"
---

# UI 视觉审计

**语言**：偏差清单、报告默认**中文**；保留 JSON 节点 id、token 名、组件符号、REQ-xxx 为原样。

IRON LAW：**审计前须从 `design/` 定位与 block 配对的 `*.json` + `*.png`，完成数据确认后方可开始分维度审计。** **JSON 为结构与数值真源；PNG 为视觉还原基准；禁止聊天截图或未落盘 `design/` 文件。** **禁止在本 skill 内直接改 UI 代码**——只产出 VA-xxx 偏差清单，由 **`quick-req-driven-codegen`** 修复。**无配对设计数据且未标 UI-N/A 时，禁止输出 pass。** **每条偏差须可追溯到 JSON 字段/token 名或 PNG 基准差异 + 代码位置。**

Red Flags（出现则回到步骤 0）：

- 未确认 `design/` 数据就开始审计
- 仅有 JSON 无 PNG、或仅有 PNG 无 JSON 却做 pass 结论
- 偏差项无「设计值 vs 实现值」双列
- 把编译错误、接口逻辑问题混入视觉偏差
- 未读执行计划 block 映射就全仓扫样式
- 本 skill 内擅自改 `.vue`/`.tsx` 样式
- 无偏差却标 pass（未覆盖任一 ready UI block）

## Workflow

```
视觉审计进度：

- [ ] 步骤 0：前置与范围 ⛔ BLOCKING
  - [ ] 0.1 执行计划 + 架构对齐报告路径；ready UI block 列表
  - [ ] 0.2 scope：block / page / all；platform：web / native / all
  - [ ] 0.3 reflux-rounds 上限（默认 3，与 codegen 对齐）
  - [ ] 0.4 UI-N/A 是否已用户确认（是则整单 N/A，跳过）
- [ ] 步骤 1：design/ 设计数据确认 ⛔ BLOCKING
  - [ ] 加载 `references/design-source-gate.md`
  - [ ] 从 `design/` 定位每个 block 配对的 `*.json` + `*.png`
  - [ ] 校验 JSON 可解析、PNG 与 JSON 同稿面；异常 → blocked，禁止审计
- [ ] 步骤 2：建立对账映射 ⛔ BLOCKING
  - [ ] 加载 `references/metadata-to-code-mapping.md`
  - [ ] block / JSON 节点 id → 组件文件 / 选择器；绑定 PNG 路径
  - [ ] 缺映射 → OPEN 或 blocked，不臆造节点
- [ ] 步骤 3：分维度审计 ⚠️ REQUIRED
  - [ ] 加载 `references/audit-dimensions.md`
  - [ ] 数值：JSON/token；观感：PNG 基准；布局→间距→字号→颜色→状态→资源→响应式→多端
- [ ] 步骤 4：偏差分级 ⛔ BLOCKING
  - [ ] 加载 `references/deviation-severity.md`
  - [ ] 每条标 P0/P1/P2；P0 须 codegen 回流
- [ ] 步骤 5：落盘偏差清单 ⚠️ REQUIRED
  - [ ] 加载 `references/deviation-list-template.md`
  - [ ] 默认：`docs/ai/visual-audit/{需求名}-视觉偏差清单-v{x.y}.md`
- [ ] 步骤 6：回流 codegen ⛔ BLOCKING（存在 P0/P1 且未达 reflux 上限）
  - [ ] 将 VA-xxx 清单交给 `quick-req-driven-codegen` 按 block 修复
  - [ ] 修复后重跑本 skill；更新清单「回流记录」
  - [ ] 达上限仍 P0 → blocked，交产品/设计 OPEN
- [ ] 步骤 7：门禁结论
  - [ ] pass → 可进入 `quick-compile-verify`
  - [ ] blocked → 禁止宣称 UI 验收通过
```

## 步骤 0：前置与范围 ⛔ BLOCKING

自问：

- 哪些 block 为 **ready** 且含 UI？（执行计划表）
- 本次 **UI-N/A** 已用户确认？（是则跳过步骤 1–6，标 N/A）
- 多端：Web only / 含 ZRN·RN / 含 Harmony 独立稿？

## 步骤 1：design/ 设计数据确认 ⛔ BLOCKING

加载 `references/design-source-gate.md`。

**数据确认通过前禁止步骤 3 及之后任何审计动作。**

## 步骤 2：对账映射

加载 `references/metadata-to-code-mapping.md`。

**映射表**（审计前必填）：

| block id | REQ | JSON 路径 + 节点 id | PNG 路径 | 组件/文件 | 平台 |
|----------|-----|---------------------|----------|-----------|------|

无法建立映射的 block → **blocked-映射**，不得对该 block 标 pass。

## 步骤 3：分维度审计

加载 `references/audit-dimensions.md`。

对每个已映射 block：**数值**取自 `design/*.json`/token；**观感**对照配对 `design/*.png`。

**禁止**用聊天截图；禁止「看起来差不多」而无双列数值。

## 步骤 4–7

偏差分级、清单落盘、回流 codegen、门禁结论——见上文 workflow 与对应 reference。

## 确认门 ⚠️ REQUIRED

- 容差放宽（如间距 ±4px → ±8px）→ 须用户或设计确认
- 建议改 `design/*.json`/token 真源而非代码 → 标 OPEN，不擅自改 JSON
- 用户只要报告、不要回流 → 步骤 6 仅交付清单

## Anti-Patterns

- 跳过步骤 1 设计数据确认
- 聊天截图代替 `design/*.png`
- 仅有 JSON 或仅有 PNG 却全量 pass
- 在本 skill 内直接改样式过审计
- 把 lint/TS 报错写进偏差清单
- 无「设计值 vs 实现值」的模糊描述
- 未映射 block 标 pass

## Pre-Delivery Checklist

- [ ] 每个 UI block 的 `design/*.json` + `*.png` 已确认且已 Read
- [ ] 映射表覆盖所有待审计 ready UI block
- [ ] 每条 VA-xxx 含双列（JSON/token 或 PNG 基准 vs 实现）+ 代码位置
- [ ] P0/P1 与 codegen 回流动作明确
- [ ] 《视觉偏差清单》已落盘
- [ ] 未在本 skill 内改 UI 代码
- [ ] blocked 时未宣称 pass

## 与相邻技能的关系

- **quick-req-driven-codegen**：上游实现（JSON 定结构、PNG 定视觉）；下游按 VA-xxx 修复。
- **quick-compile-verify**：视觉 pass 后执行；编译问题不在此 skill 处理。
- **quick-tech-solution**：交互/状态以方案为准；与 JSON/PNG 冲突标 OPEN。
- **quick-pipeline-observability**：下游统计 VA P0/P1；偏差清单须含可扫描的 P0/P1 标记。
