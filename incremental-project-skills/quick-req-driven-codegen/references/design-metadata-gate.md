# 设计稿 metadata 门禁

## 何时加载

步骤 3（`design/` 设计数据质量检查）**必读**；缺关键产物时 **⛔ BLOCKING**，禁止进入 UI 编码。

**前置**：步骤 2 已通过 `input-materials-gate.md`（含 `design/` 研发确认）。

## 必查产物（均在 `design/` 下）

| 用途 | 文件 | 最低要求 | 缺失时 |
|------|------|----------|--------|
| **布局结构** | `*.json` | 可解析节点树（id/name/children/layout/constraints） | `BLOCKED-STRUCT`；禁止写 leaf/page |
| **视觉基准** | `*.png` | 与 JSON 同页/同状态的终稿截图 | `BLOCKED-VISUAL`；禁止宣称 UI 还原 |
| **样式 token** | `tokens.json` 或 JSON 内变量 | 色值/字号/间距可映射 | 样式层 `missing`，禁硬编码 |
| **清单** | `manifest.md`（可选） | JSON↔PNG 配对表 | 须在执行计划 block 证据列手动配对 |

JSON 与 PNG **须成对**（同页面或同组件状态）；文件名或 manifest 可互指。

## 检查清单

- [ ] 每个 UI block 已绑定 `design/*.json` + 配对 `design/*.png`
- [ ] JSON 节点 id → 执行计划 block / 目标组件可映射
- [ ] PNG 与 JSON 为同一设计稿版本（manifest 或研发确认版本一致）
- [ ] 交互态（hover/disabled/loading）在 JSON variants 或 PRD REQ 有依据

## 禁止

- 仅有 PNG、无 JSON → **写 leaf/page**（结构不明）
- 仅有 JSON、无 PNG → **宣称视觉还原完成**
- 聊天截图/飞书图片替代 `design/*.png`
- 跳过本门禁直接实现 leaf / page

## 降级（须用户书面确认）

- 仅逻辑层、无 UI：执行计划标 `UI-N/A` + REQ 引用
- 临时 mock UI：OPEN-xxx + 确认门；不得冒充终稿

## 下游

leaf/page 编码细则 → `ui-view-layer-implementation.md`
