# 审计维度

## 何时加载

步骤 3。

**前置**：`design/*.json` + 配对 `*.png` 已在步骤 1 确认。

## 双真源分工

| 真源 | 审计用途 |
|------|----------|
| `design/*.json` + token | 结构、数值（px/token/色值/状态 variants） |
| `design/*.png` | 整体视觉还原：元素有无、对齐、比例、留白、视觉权重 |

数值型偏差**必须**有 JSON/token 双列；PNG 可触发「观感偏差」项并引用 PNG 路径。

## 维度清单

对每条映射行逐项自问；有 metadata 字段则**必须**对比。

### 1. 布局 Layout

- 宽/高、min/max、flex 方向、align/justify、position
- 子节点顺序与 JSON `children` 一致否
- 设计：`absoluteBoundingBox`、`layoutMode`、`constraints`
- PNG：整体区块划分与 JSON 树是否一致

### 2. 间距 Spacing

- padding、margin、gap、itemSpacing
- 设计值 vs 代码：token 名或 px/rem；禁止只写「偏小」

### 3. 字号与字重 Typography

- fontSize、lineHeight、letterSpacing、fontFamily、fontWeight
- 是否用语义 token（如 `text-body-md`）而非裸 px

### 4. 颜色 Color

- 文本/背景/边框/图标色；渐变、透明度
- 对照 token JSON 语义名；硬编码 `#hex` 与 token 不一致 → 偏差

### 5. 组件状态 States

- default / hover / active / focus / disabled / loading / error / empty
- JSON variant、`componentProperties` 或方案交互节有定义则必查
- PNG 须为对应状态稿（多状态各有 PNG 时逐张对照）

### 6. 资源 Assets

- 图标、插图、图片 URL、SVG、Lottie
- 尺寸、倍图、命名与 metadata `exportSettings` / 资源 id

### 7. 响应式 Responsive

- 断点宽度、列数、隐藏/折叠规则
- metadata 多 frame（Desktop/Tablet/Mobile）或方案声明的 breakpoint

### 8. 多端差异 Multi-platform

- Web vs ZRN/RN vs Harmony 稿面差异
- 各端独立 `design/{端}/*.json` + `*.png` 或方案「端差异表」
- 仅一端有稿却实现另一端 → OPEN 或 P1

### 9. 视觉还原 Visual fidelity（PNG）

- 对照 `design/*.png`：关键元素是否缺失、错位、比例失调
- 须写清：PNG 路径、可见差异描述、关联 JSON 节点（若有）
- 纯观感项可标 P1；结构级错误（整区缺失）标 P0

## 提取实现值的方法

1. Read 组件 SFC/TSX 与关联样式（scoped/css module/tailwind）
2. 追 token：变量定义文件、`tailwind.config`、`theme` 对象
3. PNG 辅助验证已列 VA 项的整体观感；**不得**用聊天截图代替 `design/*.png`

## 禁止

- 跳过步骤 1 数据确认直接审计
- 把业务文案错字当 P0 视觉（归功能/文案 OPEN）
