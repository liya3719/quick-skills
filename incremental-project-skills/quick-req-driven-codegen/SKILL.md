---
name: quick-req-driven-codegen
description: "REQ-and-spec-driven implementation: PRD + tech solution (master + sub-designs per 附录 F), overall architecture blueprint, task split per sub-design, then code from decomposition, contracts, and design-token JSON. Actions: 整体架构设计, 架构图, 子方案分任务, 排期与依赖, implement, wire API, pixel-match UI from tokens, incremental appendix-D. Objects: PRD, REQ-xxx, master tech-solution Markdown, sub-design files, testcase doc, token JSON (W3C/design-tokens, Style Dictionary, team schema). Stacks: Vue 3, React, Tailwind, SCSS, Less, TypeScript, JavaScript. Phrases: 按拆解开发, 按子方案开发, 总方案子方案, 对照技术方案写代码, 用 token JSON 还原样式, trace to REQ, no invented product rules. Use when delivery must follow PRD plus master/sub specs plus tokens—not screenshot guesswork or ad-hoc module boundaries."
argument-hint: "[stack] e.g. Vue3+Tailwind+TS | React+SCSS+TS | 写明 UI 框架、样式方案、语言"
---

# Req Tech Design Codegen

**语言**：交付说明、映射表、OPEN 项默认使用**中文**；保留 REQ-xxx、TC-xxx、OPEN-xxx、API 路径与代码标识符为原样英文。

IRON LAW：**禁止在拆解文档、技术方案与测试用例未覆盖之处「发明」业务规则、接口字段、错误语义或状态迁移。** **整体架构与子任务划分须与 PRD、总方案、附录 F 子方案索引及各子方案一致**；跨模块职责与集成点无方案依据时，标 **OPEN** 或「工程补充」并说明理由，禁止静默新增模块或契约。**样式与主题以团队提供的 design token JSON 为真源**，禁止仅凭主观配色替换 token。若 token 与 REQ/方案冲突，**不得静默折中**——列出冲突与建议并在继续前取得用户确认（或记入 OPEN-xxx）。

## Workflow

复制下列清单并在完成时勾选：

```
REQ 驱动实现进度：

- [ ] 步骤 1：输入清点 ⛔ BLOCKING
  - [ ] 1.1 **PRD** 路径与版本（或声明「以拆解稿为产品真源」并给拆解版本）
  - [ ] 1.2 拆解文档路径、版本；本批 **REQ-xxx** 列表
  - [ ] 1.3 **总方案**路径、版本；文内 **附录 F 子方案索引**是否与磁盘子方案文件一致
  - [ ] 1.4 各 **子方案**路径列表（`{功能描述}-版本.md`）；覆盖 REQ 子集无遗漏、无冲突
  - [ ] 1.5 设计稿：**design token JSON** 路径（或粘贴）、格式说明（若多文件则说明主次）
  - [ ] 1.6 **技术栈（必问）**：UI 框架、样式方案、语言
  - [ ] 1.7（可选）测试用例文档路径；需对齐的 TC-xxx
  - [ ] 1.8 OPEN/BLOCKED：列出并确认假设或显式延后
- [ ] 步骤 2：整体架构设计 ⚠️ REQUIRED（多子方案或用户要求架构蓝图时；否则核对总方案已有架构图并勾选「已对齐 PRD/拆解」）
  - [ ] 2.1 加载 `references/architecture-and-task-split.md`
  - [ ] 2.2 在 PRD+总方案+附录 F 约束下产出或核对**一页架构视图**（上下文、分层/模块边界、跨模块集成点、REQ 映射）
  - [ ] 2.3 **确认门**：存在子方案冲突、依赖环或与代码仓结构重大差异时，用户确认后再冻结
- [ ] 步骤 3：子任务拆分与开发顺序 ⚠️ REQUIRED（多子方案时；单子方案可「单任务包」略写但须含 REQ 列表）
  - [ ] 3.1 默认 **一子方案 → 一开发任务包**；标注依赖顺序与可并行项
  - [ ] 3.2 每任务包：**对应子方案文件**、REQ-xxx、建议验证点（TC 或自测）
  - [ ] 3.3 确认门：任务顺序或并行策略与用户预期不一致时，先对齐再编码
- [ ] 步骤 4：契约、token 与栈实践对齐 ⚠️ REQUIRED
  - [ ] 4.1 从方案抽取：挂载点、模块边界、接口与错误码
  - [ ] 4.2 加载 references/design-tokens-json.md，解析 token JSON：语义分组、引用关系、暗色/品牌变体
  - [ ] 4.3 按下方「渐进加载表」**仅加载与本次栈匹配的 references**（勿同时打开 Vue 与 React 全文）
  - [ ] 4.4 建立「token 名 → theme/变量」映射草稿；缺失 token 记 OPEN
- [ ] 步骤 5：实现计划
  - [ ] 5.1 **按任务包**列文件级变更；先类型/契约与 theme 接入，再 UI 与集成
  - [ ] 5.2 若方案附录 D 式增量：只允许触及附录声明的范围
- [ ] 步骤 6：编码与追溯
  - [ ] 6.1 关键行为以 REQ 注释或团队约定方式锚点（与「工程补充」区分）
  - [ ] 6.2 UI 使用映射后的 token；禁止硬编码与 JSON 冲突的色值/间距（除非 OPEN 已批准）
- [ ] 步骤 7：确认门 ⚠️ REQUIRED
  - [ ] 大范围删除/替换、或与 REQ 冲突的 token 取舍 — 须用户确认后再写定稿
- [ ] 步骤 8：交付说明
  - [ ] 8.1 变更文件列表；**架构/任务包摘要**（若步骤 2–3 已执行）；REQ→实现映射；TC 覆盖或缺口；OPEN；token 文件版本摘要；**本次栈（框架+样式+语言）**
```

## 渐进加载表（步骤 4.3）

**架构与子任务**：凡执行步骤 2–3 时，先读 **`references/architecture-and-task-split.md`**（可与步骤 2.1 合并为一次加载）。

必选：**design-tokens-json.md**（凡涉及从 JSON 还原样式）。

| 用户声明 | 额外加载（仅选匹配行） |
|----------|-------------------------|
| UI：**Vue 3** | `references/vue3-ui-tokens.md` |
| UI：**React** | `references/react-ui-tokens.md` |
| 样式：**Tailwind**（含 Uno 等同类工具类方案时亦先读此篇再按项目调整） | `references/tailwind-design-tokens.md` |
| 样式：**SCSS 或 Less** | `references/scss-less-tokens.md` |
| 语言：**TypeScript** | `references/typescript-ui.md` |
| 语言：**JavaScript** | `references/javascript-ui.md` |

**CSS Modules / 纯 CSS**（且无 Tailwind）：读 `scss-less-tokens.md` 中的「变量与 `:root`」思路，组件内仍只消费语义名映射，不写魔法数。

若栈为组合（如 Vue3+SCSS+TS）：加载 **design-tokens-json + vue3-ui-tokens + scss-less-tokens + typescript-ui**。

## 步骤 1：输入清点 ⛔ BLOCKING

自问：

- **PRD / 拆解 / 总方案 / 子方案**版本是否一致？附录 F 与磁盘文件是否一致？
- 本迭代要交付的 **REQ 列表**是否与技术方案及子方案附录 A 子集一致？
- **技术方案**是否给出足够契约（接口形状、错误、状态）用于写代码？
- **Token JSON** 是否与当前页面/主题一致？是否为导出快照（可复现）？
- **技术栈**是否已明确（框架 + 样式 + 语言）？若用户未说明，**先提问再编码**。

缺少任一项时，先补齐或记入 OPEN，不「猜」需求。

## 步骤 2–3：架构与子任务（摘要）

细则与确认门见 **`references/architecture-and-task-split.md`**。要点：**不重复**总方案已冻结且仍有效的架构；子任务顺序服从 **子方案依赖与 REQ 数据流**。

## 步骤 4：契约与 design token JSON ⚠️ REQUIRED

开始写 UI 或主题前：**加载 references/design-tokens-json.md**，并按其中规则解析用户提供的 token JSON；再按「渐进加载表」加载栈相关 reference。

Ask：

- JSON 顶层是单文件多集合，还是多文件按主题拆分？
- 颜色与间距是否引用别名链？未解析到的引用是否阻塞渲染？

## 步骤 5：实现策略

- **契约优先**：类型、HTTP/IPC 负载形状、错误码与方案一致。
- **Token 优先于肉眼**：样式从 JSON 映射；若需 `rgba` 兜底，说明对应 token 名与原因。
- **栈一致**：遵循本次已加载的 framework/style/lang 参考中的约束，不混用另一框架的惯例。
- **增量**：只改附录或用户指定的 REQ 范围；禁止顺带大范围重构。
- **任务包驱动**：按步骤 3 的任务包逐个完成，避免跨包「顺手」改公共契约而不走确认门。

## 步骤 7：确认门 ⚠️ REQUIRED

在以下情况**暂停并向用户确认**后再提交最终 diff：

- 删除或大量替换已有公开 API / 路由 / 事件名。
- Token 与文案/交互在 REQ 中存在歧义，需产品侧拍板。
- 为实现布局必须在工程里写死与 token JSON 不一致的数值。

## Anti-Patterns

- 同时加载 Vue 与 React 两篇 reference「以防万一」。
- 只用「看起来像」的色值与间距，**不读 token JSON**。
- 把技术方案当参考，**省略方案中已写的错误处理与边界**。
- 用「相关需求」代替 **REQ-xxx** 锚点。
- 需求或方案已升版，却仍按旧对话记忆实现。
- **在 token 与 REQ 冲突时自判**而不列出确认项或 OPEN。
- **跳过架构与子任务对齐**，直接按子方案分别编码导致跨模块契约漂移。
- **重写与总方案矛盾的「新架构」**，或未核对附录 F 就拆任务。

## Pre-Delivery Checklist

- [ ] 每个已实现的 REQ 有可追溯锚点（注释或映射表）
- [ ] 多子方案交付时：架构视图与任务包表已产出或与已有总方案对齐并注明
- [ ] 未引用 token JSON 的样式硬编码：已清零或已记入 OPEN 并说明
- [ ] 接口与错误行为与方案一致，或已标「工程补充」
- [ ] 无占位：TODO/FIXME/TBD 留在宣称完成的逻辑路径上（OPEN 列表除外）
- [ ] 测试用例对齐：已给的 TC 有对应说明或缺口显性标出
- [ ] 交付含：文件列表、REQ→代码、token 文件标识、OPEN、**本次栈（框架+样式+语言）**

## 与相邻技能的关系

- **quick-requirement-decomposition**：消费 REQ 与版本规则，不在此技能内改写拆解稿。
- **quick-tech-solution**：总方案、子方案命名、附录 F、追溯矩阵以方案为准；冲突时回到方案或 OPEN。
- **quick-requirement-testcase-trace**：实现结果应对齐 TC 或说明 BLOCKED，不替代人工执行测试。
