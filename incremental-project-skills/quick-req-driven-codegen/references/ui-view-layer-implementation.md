# UI 视图层实现（leaf / page）

## 何时加载

步骤 7 进入 **leaf / page** 层之前**必读**；结构未明确 → **⛔ BLOCKING**，禁止写视图代码。

## 三源分工 ⛔

| 维度 | 真源 | 路径 | 用途 |
|------|------|------|------|
| **布局结构** | 设计 JSON | `design/*.json` | 节点树、层级、约束、间距/token 字段 |
| **视觉还原** | 设计 PNG | `design/*.png` | 终稿视觉基准（对齐、比例、观感） |
| **交互行为** | 需求拆解 + 设计结构 | `docs/prd/` + JSON 可点击/状态节点 | 事件、跳转、校验、态切换 |

**禁止**：聊天截图、飞书图片、未落盘 `design/` 的文件替代上表真源。

## 1. 结构理解（JSON）⛔

进入 leaf/page 编码前，对每个 UI block：

1. **Read** 对应 `design/*.json`（Figma/MasterGo 导出均可）
2. 产出**页面结构摘要**（可写入执行计划 block 备注或对齐报告 §3）：
   - 根容器 → 区域划分（header / body / footer 等）
   - 子组件层级（children 顺序与嵌套）
   - 关键节点 id / name → 目标组件映射
   - layoutMode、constraints、padding、itemSpacing 等布局字段
3. **结构摘要未完成或 JSON 与 block 无法对应** → block 标 `blocked`，禁止编码

自问：能否画出与本 block 一致的组件树？不能 → 先补结构，不写样式。

## 2. 视觉还原（PNG）⛔

- 每个 UI block 须绑定至少一张 **`design/*.png`**（页面级或组件级，文件名与 JSON/manifest 对应）
- leaf/page 实现时**以 PNG 为视觉基准**：对齐方式、元素相对位置、留白比例、视觉权重
- 数值（色值、字号、间距）优先取自 JSON/token；PNG 用于**校验观感**与补全 JSON 未导出的视觉细节
- 无配对 PNG → UI block **blocked**（除非用户确认 OPEN + 仅逻辑层）

## 3. 交互推理（PRD + 设计结构）⚠️

交互不得凭空发明；须**深度推理**并落盘到 block「交互」列：

| 输入 | 推理内容 |
|------|----------|
| `docs/prd/` REQ | 用户目标、主路径、异常/边界、校验规则 |
| JSON 结构 | 按钮/链接/输入框/Tab/Modal 等可交互节点；variants（default/disabled/loading） |
| 技术方案 | 接口触发时机、错误展示、路由跳转 |

**最低交付**（每个 UI block 的「交互」列）：

- 触发元素（JSON 节点 id + 组件名）
- 事件与行为（click / submit / scroll / …）
- 状态变化（loading / empty / error / disabled）
- REQ 锚点（REQ-xxx § 或段落）

推理无法闭合（如 PRD 与 JSON 矛盾）→ 标 OPEN，**不得标 ready**。

## 与七层顺序的关系

- **types / api / state**：不依赖本 reference
- **leaf / page**：必须先完成 §1 结构摘要 + §3 交互列；编码中持续对照 §2 PNG
- **route / tracking**：在 page 就绪后按方案补全

## 禁止

- 未读 `design/*.json` 就写 leaf/page
- 无 `design/*.png` 基准却宣称 UI 还原完成
- 交互仅写「点击跳转」而无 REQ/节点 id 锚点
- 用聊天截图代替 `design/*.png`
- JSON 与 PNG 明显不是同一页面/状态却强行配对

## 降级（须用户书面确认）

- JSON 缺字段但 PNG + token 可还原布局 → OPEN 记录缺失字段，可编码并待 visual-audit 补差
- 纯展示、无交互节点 → 交互列写「无交互 / REQ-xxx 只读展示」
