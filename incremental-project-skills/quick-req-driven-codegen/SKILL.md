---
name: quick-req-driven-codegen
description: "REQ 驱动编码：编码前必读 docs/ 下需求拆解(docs/prd)与技术方案(docs/design)、design/ 下设计数据(Figma/MasterGo/token)；三类物料须齐套且研发确认后方可编码；写代码前落盘执行计划(每 block 含目标文件/组件/字段/交互/证据)，缺落点 blocked；禁凭截图写 UI；稳定分层 types→api→state→leaf→page→route→tracking；结束后架构对齐报告，关键项 pass 才编译，missing 最多回流 5 轮否则 blocked。Actions: 执行计划, 架构对齐, 分层实现, token JSON, 子方案分任务, 物料门禁, 研发确认. Objects: REQ-xxx, docs/prd, docs/design, design/, 总方案/子方案, AGENTS.md. Stacks: Vue3, React, ZRN, TS. Triggers: 按拆解开发, 按方案写代码, 执行计划, 架构对齐报告, 禁止截图 UI, 分层实现, 研发确认, 物料齐套."
argument-hint: "[stack] e.g. Vue3+Tailwind+TS | React+ZRN+TS | 写明 UI 框架、样式方案、语言"
---

# Req Tech Design Codegen

**语言**：交付说明、映射表、OPEN 项默认使用**中文**；保留 REQ-xxx、TC-xxx、OPEN-xxx、API 路径与代码标识符为原样英文。

IRON LAW：**编码前须从 `docs/` 读取需求拆解与技术方案、从 `design/` 读取设计数据；三类物料须齐套且均经研发确认，否则整单 blocked。** **禁止在拆解、方案、测试用例、设计数据、项目规则未覆盖处发明业务规则、接口字段、UI 或交互。** **写代码前须有落盘的《执行计划》，且每个 ready block 具备目标文件、目标组件、数据字段、交互与证据；缺落点只能标 blocked，禁止硬写。** **禁止凭截图/主观目测写 UI**——须 `design/` 可解析 metadata 或已批准的 OPEN。**实现须按稳定层顺序**：types → api → state → leaf → page → route → tracking。**编译验证前须《架构对齐报告》关键项全部 pass**；missing 最多回流 5 轮，仍缺则 **blocked**。

## Workflow

```
REQ 驱动实现进度：

- [ ] 步骤 1：输入物料清点 ⛔ BLOCKING
  - [ ] 1.1 **需求拆解**（`docs/prd/`）：路径、版本、REQ-xxx 列表、研发确认记录
  - [ ] 1.2 **技术方案**（`docs/design/`）：总方案 + 子方案；设计分块可识别；研发确认记录
  - [ ] 1.3 **设计数据**（`design/`）：Figma / MasterGo / token JSON / manifest（非截图）
  - [ ] 1.4 **项目规则**：`AGENTS.md` / `AGENT.md` / `CLAUDE.md`（存在则必读）
  - [ ] 1.5 design token JSON 路径（UI 相关 REQ 时，通常在 `design/`）
  - [ ] 1.6 **技术栈**：UI 框架、样式方案、语言（未说明则先问）
  - [ ] 1.7（可选）测试用例路径；TC-xxx
  - [ ] 1.8 OPEN/BLOCKED 与假设
- [ ] 步骤 2：物料齐套与研发确认门禁 ⛔ BLOCKING
  - [ ] 加载 `references/input-materials-gate.md`
  - [ ] 三类物料版本对齐、结构完整（整齐）
  - [ ] 拆解 / 方案 / 设计数据均有研发确认；无记录 → 确认门，禁止编码
- [ ] 步骤 3：设计数据质量门禁 ⛔ BLOCKING
  - [ ] 加载 `references/design-metadata-gate.md`
  - [ ] UI 相关 REQ 无 `design/` 可解析数据 → 流程 blocked，禁止写 UI
- [ ] 步骤 4：架构与子任务 ⚠️ REQUIRED（多子方案时）
  - [ ] 加载 `references/architecture-and-task-split.md`；核对 PRD/方案/附录 F
- [ ] 步骤 5：执行计划 ⛔ BLOCKING（真正写代码前）
  - [ ] 加载 `references/execution-plan.md`
  - [ ] 按方案设计分块填 block 表；每 block：目标文件、组件、数据字段、交互、证据
  - [ ] 缺落点 → block 标 blocked；**不得对 blocked block 编码**
  - [ ] 确认门：存在 blocked 且未缩小范围 → 停止
- [ ] 步骤 6：契约与 token ⚠️ REQUIRED
  - [ ] 从方案抽挂载点、接口、错误码
  - [ ] 加载 `references/design-tokens-json.md` + 渐进加载表（栈相关）
- [ ] 步骤 7：分层实现 ⛔ BLOCKING
  - [ ] 加载 `references/implementation-layer-order.md`
  - [ ] 顺序：types.ts → api.ts → state/hooks → leaf → page → route/web → tracking/logging
  - [ ] 仅实现执行计划中 status=ready 的 block
- [ ] 步骤 8：编码追溯与确认门 ⚠️ REQUIRED
  - [ ] REQ 锚点；token 映射；大范围删除/契约冲突须用户确认
- [ ] 步骤 9：架构对齐报告 ⛔ BLOCKING
  - [ ] 加载 `references/architecture-alignment-report.md` 并落盘
  - [ ] 覆盖：文件、分块、接口字段、路由平台、ZRN UI/样式、埋点、偏差、待验证项
- [ ] 步骤 10：对齐门禁 → 视觉审计（UI）⚠️ REQUIRED
  - [ ] 关键项全部 pass → 有 ready UI block 时触发 **`quick-visual-audit`**
  - [ ] 消费 VA-xxx 偏差清单 → 本 skill 精准修复 UI（≤3 轮）→ 复审计
  - [ ] UI-N/A 或无 UI block → 跳过，记录 N/A
  - [ ] missing（非 UI）→ 回流补全（≤5 轮），更新报告
  - [ ] 5 轮仍 missing 或 blocked 未解 → 整单 blocked
- [ ] 步骤 11：编译验证 ⛔ BLOCKING
  - [ ] 视觉 pass 或 N/A 后 → **`quick-compile-verify`**
- [ ] 步骤 12：交付说明
```

## 步骤 1：输入物料清点 ⛔ BLOCKING

**三类物料 + 项目规则**（UI 无关迭代可 1.3 标 UI-N/A + OPEN，须用户确认）：

| 物料 | 目录 | 来源 |
|------|------|------|
| 需求拆解 | `docs/prd/` | `quick-requirement-decomposition` |
| 技术方案 | `docs/design/` | `quick-tech-solution` |
| 设计数据 | **`design/`** | Figma / MasterGo 导出、token JSON、manifest |
| 项目规则 | 仓库根 | `AGENTS.md` / `AGENT.md` / `CLAUDE.md` |

**禁止混淆** `docs/design/`（技术方案）与 `design/`（设计数据）。

自问：三类路径是否已 Read？版本是否与 REQ/方案一致？**未 Read 禁止步骤 5 之后任何业务代码编辑。**

## 步骤 2–5：门禁与执行计划

- **步骤 2**：`input-materials-gate.md` — 齐套 + 研发确认；无确认 → blocked
- **步骤 3**：`design-metadata-gate.md` — `design/` 无可用 metadata 则 UI 层 blocked
- **步骤 5**：`execution-plan.md` — 方案每个设计分块 → 一行 block；**无证据不得标 ready**

默认执行计划路径：`docs/ai/codegen/{需求名}-执行计划-v{x.y}.md`

## 步骤 6–7：契约、token、分层顺序

步骤 6 沿用 design token 与栈 reference（见下表）。

步骤 7 **稳定顺序**（`implementation-layer-order.md`）：

1. `types.ts` — 类型与 DTO  
2. `api.ts` — 请求与错误映射  
3. hooks / state — 状态与数据流  
4. leaf components — 子组件  
5. page container — 页面容器  
6. route / Web 注册 — 路由与平台  
7. tracking / logging — 埋点与日志  

## 渐进加载表

| 用户声明 | 加载 |
|----------|------|
| 物料与研发确认 | `input-materials-gate.md` |
| 架构与子任务 | `architecture-and-task-split.md` |
| 执行计划 | `execution-plan.md` |
| 设计数据门禁 | `design-metadata-gate.md` |
| 分层顺序 | `implementation-layer-order.md` |
| 对齐报告 | `architecture-alignment-report.md` |
| 视觉回流 | 消费 `quick-visual-audit` 的 VA-xxx 清单，仅改清单列明 UI 项 |
| UI 样式 | **必选** `design-tokens-json.md` |
| Vue 3 | `vue3-ui-tokens.md` |
| React | `react-ui-tokens.md` |
| Tailwind | `tailwind-design-tokens.md` |
| SCSS/Less | `scss-less-tokens.md` |
| TypeScript / JS | `typescript-ui.md` / `javascript-ui.md` |

## 步骤 9–11：对齐、视觉审计与编译门禁

落盘：`docs/ai/codegen/{需求名}-架构对齐报告-v{x.y}.md`

**关键项 pass** 后：

1. **UI block 存在** → **`quick-visual-audit`** → VA 清单回流本 skill 修复（≤3 轮）→ 视觉 pass
2. → **`quick-compile-verify`**

| 结果 | 动作 |
|------|------|
| pass | 进入视觉审计（有 UI）或 compile-verify（UI-N/A） |
| missing | 回流补代码/文档，更新报告（**≤5 轮**） |
| 5 轮后仍 missing | **blocked** |
| VA P0 未解（视觉） | blocked，禁止 compile-verify |
| blocked block 被实现 | 门禁失败 |

## 确认门 ⚠️ REQUIRED

- 拆解 / 方案 / 设计数据**缺研发确认**却要编码
- 执行计划存在 blocked block 且用户未同意缩小范围
- 无 `design/` 设计数据却要交付 UI
- 删除/替换公开 API、路由、事件名
- token 与 REQ 冲突需产品拍板
- 对齐报告关键项未 pass 却要合入

## Anti-Patterns

- 跳过步骤 1–2 直接写代码
- 混淆 `docs/design/` 与 `design/`
- 物料未齐套或未研发确认却编码
- 无执行计划或 block 缺「证据」却编码
- 凭截图/聊天图片写 UI
- 跳层实现（先 page 后 types/api）
- 无架构对齐报告就跑编译或 merge
- missing 超过 5 轮仍标 pass
- 同时加载 Vue 与 React reference「以防万一」
- 发明方案未写的错误处理与边界

## Pre-Delivery Checklist

- [ ] `docs/prd/`、`docs/design/`、`design/` 路径已记录且已 Read
- [ ] 三类物料均有研发确认记录或当次用户确认
- [ ] 《执行计划》已落盘；ready block 字段完整
- [ ] 实现顺序符合七层；无 blocked block 被静默实现
- [ ] 《架构对齐报告》已落盘；关键项 pass 或已 blocked 并说明
- [ ] 编译验证在视觉 pass 或 UI-N/A **之后**执行
- [ ] 每 REQ 有追溯锚点；token 无未批准硬编码
- [ ] 交付含：文件列表、REQ→代码、执行计划与报告路径、OPEN、**本次栈**

## 与相邻技能的关系

- **quick-requirement-decomposition**：消费 `docs/prd/` REQ 与版本规则，不在此技能内改写拆解稿。
- **quick-tech-solution**：消费 `docs/design/` 总方案、子方案、附录 F；执行计划 block 须回溯方案章节；**须方案研发确认后再编码**。
- **quick-requirement-testcase-trace**：实现应对齐 TC 或说明 BLOCKED；对齐报告「待验证项」可引用 TC。
- **quick-visual-audit**：步骤 10 UI 验收；产出 VA 偏差清单，本 skill 按清单回流修复。
- **quick-compile-verify**：步骤 11；视觉 pass 或 UI-N/A 后执行。
