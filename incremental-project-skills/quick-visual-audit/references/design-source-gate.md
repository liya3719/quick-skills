# design/ 设计数据确认门禁

## 何时加载

步骤 1 **必读**；数据未确认 → **⛔ BLOCKING**，禁止进入对账映射与分维度审计。

## 定位配对文件

从项目根 **`design/`** 目录，按执行计划 block 的「结构 JSON」「视觉 PNG」列（或证据列）定位：

| 文件 | 用途 | 典型路径 |
|------|------|----------|
| `*.json` | 节点树、布局数值、token 字段 | `design/{需求名}/*.json` |
| `*.png` | 终稿视觉基准 | `design/{需求名}/*.png` |

**配对规则**：同页面/同组件状态；文件名互指或 `manifest.md` 登记。与 codegen `design-metadata-gate.md` 一致。

## 数据确认清单 ⛔

对每个待审计 UI block，逐项确认后勾选：

- [ ] `design/*.json` 已 Read；可解析（非空、合法 JSON、含节点树）
- [ ] 配对 `design/*.png` 已 Read；与 JSON 为同一稿面/状态
- [ ] JSON 节点 id 与执行计划 block 证据可对应
- [ ] PNG 与 JSON 版本一致（manifest 或研发确认版本）
- [ ] token 字段（色值/字号/间距）在 JSON 或独立 `tokens.json` 可提取
- [ ] 明显损坏（0 字节、截断图、JSON 缺 children）→ 标 `BLOCKED-DATA`

**全部待审计 block 通过** → 进入步骤 2；任一 blocked → 整单暂停，列 OPEN，不产出 pass。

## 禁止

- 未定位 `design/` 文件就开始审计
- 仅有 JSON 无 PNG 或仅有 PNG 无 JSON（缺一则 blocked）
- 聊天截图/飞书图片替代 `design/*.png`
- 数据明显异常却标 pass

## 与 codegen 对齐

执行计划 block 表应已含「结构 JSON」「视觉 PNG」列；缺失时从对齐报告 §1/§3 或 `design/manifest.md` 补全，补不齐 → blocked-映射。
