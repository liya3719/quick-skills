# 审计维度

## 何时加载

步骤 2。

## 维度清单

对每条映射行逐项自问；有 metadata 字段则**必须**对比。

### 1. 布局 Layout

- 宽/高、min/max、flex 方向、align/justify、position
- 子节点顺序与 metadata `children` 一致否
- 设计：`absoluteBoundingBox`、`layoutMode`、`constraints`

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
- metadata variant、`componentProperties` 或方案交互节有定义则必查

### 6. 资源 Assets

- 图标、插图、图片 URL、SVG、Lottie
- 尺寸、倍图、命名与 metadata `exportSettings` / 资源 id

### 7. 响应式 Responsive

- 断点宽度、列数、隐藏/折叠规则
- metadata 多 frame（Desktop/Tablet/Mobile）或方案声明的 breakpoint

### 8. 多端差异 Multi-platform

- Web vs ZRN/RN vs Harmony 稿面差异
- 对齐报告 §5；各端独立 metadata 或方案「端差异表」
- 仅一端有稿却实现另一端 → OPEN 或 P1

## 提取实现值的方法

1. Read 组件 SFC/TSX 与关联样式（scoped/css module/tailwind）
2. 追 token：变量定义文件、`tailwind.config`、`theme` 对象
3. 禁止凭运行截图估像素；可辅助浏览器 MCP **仅**验证已列 VA 项

## 禁止

- 跳过无 REQ 的「顺手」页面
- 把业务文案错字当 P0 视觉（归功能/文案 OPEN）
