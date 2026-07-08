# 设计稿 metadata 门禁

## 何时加载

步骤 3（`design/` 设计数据质量检查）**必读**；缺关键产物时 **⛔ BLOCKING**，禁止进入 UI 编码。

**前置**：步骤 2 已通过 `input-materials-gate.md`（含 `design/` 研发确认）。

## 必查产物（均在 `design/` 下）

| 来源 | 最低要求 | 典型路径 | 缺失时 |
|------|----------|----------|--------|
| **Figma** | 可解析 metadata（节点树 + token/变量表） | `design/{需求名}/figma.json` 或团队约定 | 标 `BLOCKED-DESIGN`；禁止凭截图写 UI |
| **MasterGo** | 可解析 metadata（DSL / 导出 JSON） | `design/{需求名}/mastergo.json` 或团队约定 | 同上 |
| **design token JSON** | 语义 token 可映射到组件 | `design/{需求名}/tokens.json` 或 `design/token/` | 样式层标 `missing`，不得硬编码替代 |

## 检查清单

- [ ] 设计稿 metadata 文件路径已写入执行计划 / 对齐报告
- [ ] 页面/组件与方案「设计分块」可对应（节点 id 或 layer 名 → block id）
- [ ] 颜色/间距/字体来自 token 或 metadata 字段，非截图目测
- [ ] 交互态（hover/disabled/loading）在 metadata 或方案中有依据

## 禁止

- 仅有 PNG/JPG/聊天截图、无 metadata → **写 UI 代码**
- 用「看起来差不多」补全未在 metadata/token 出现的样式
- 跳过本门禁直接实现 leaf components / page container

## 降级（须用户书面确认）

- 仅逻辑层、无 UI：可跳过 UI metadata，但须在执行计划标 `UI-N/A` 并引用 REQ
- 临时 mock UI：须 OPEN-xxx + 确认门；不得冒充终稿
