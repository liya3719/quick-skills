# Metadata → 代码映射

## 何时加载

步骤 2，分维度审计**之前**必读。

**前置**：步骤 1 已确认 `design/*.json` + `*.png` 配对无误。

## 映射来源（优先级）

1. **执行计划** block 表：结构 JSON、视觉 PNG、目标文件、目标组件
2. **架构对齐报告** §2 文件清单、§3 分块对齐
3. **`design/*.json`**：节点 `id` / `name` / `children`
4. **方案设计分块** 与页面路由对应

## JSON 常见字段（`design/*.json`）

| 字段 | 用途 |
|------|------|
| `id` / `nodeId` | 与 block 证据对齐 |
| `absoluteBoundingBox` | 布局位置、尺寸 |
| `layoutMode` / constraints | Flex/对齐 |
| `padding*` / `itemSpacing` | 间距 |
| `style.fontSize` / `fontName` | 字号字体 |
| `fills` / `strokes` | 颜色 |
| `componentProperties` / variants | 状态 |
| `children` | 层级结构 |

## PNG 角色

- 映射表 **PNG 路径** 列：与 JSON 同 block 绑定
- 审计时作整体观感对照（元素有无、对齐、留白比例）
- 数值争议以 JSON/token 为准；PNG 补 JSON 未导出的视觉细节

## 映射表填写规则

- 一 block 至少一行；须同时填 JSON 路径+节点 id 与 PNG 路径
- **platform** 列：web / ios / android / harmony / shared
- JSON 节点不存在 → `blocked-映射`；PNG 缺失 → 同 blocked

## 代码侧定位

- Vue：`.vue` + `<template>` 根元素 / `class` / `:deep`
- React：组件文件 + `className` / styled / CSS module
- Token：CSS 变量、`theme.*`、Tailwind 类

## 禁止

- 无 block 证据的全仓 grep 当审计完成
- 用聊天截图图层名猜测节点 id
- JSON 与 PNG 未配对却建映射
