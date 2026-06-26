# Metadata → 代码映射

## 何时加载

步骤 1，分维度审计**之前**必读。

## 映射来源（优先级）

1. **执行计划** block 表：目标文件、目标组件、证据（metadata 节点 id）
2. **架构对齐报告** §2 文件清单、§3 分块对齐
3. **metadata 自身**：Figma `id` / `name`；MasterGo layer 路径
4. **方案设计分块** 与页面路由对应

## Figma metadata 常见字段

| metadata | 用途 |
|----------|------|
| `id` / `nodeId` | 与 block 证据对齐 |
| `absoluteBoundingBox` | 布局位置、尺寸 |
| `layoutMode` / constraints | Flex/对齐 |
| `padding*` / `itemSpacing` | 间距 |
| `style.fontSize` / `fontName` | 字号字体 |
| `fills` / `strokes` | 颜色 |
| `componentProperties` / variants | 状态（default/disabled/…） |
| `children` | 层级结构 |

## MasterGo / DSL

- 读团队约定 JSON 路径；layer `id`、`style`、`children` 与上表等价映射
- token 引用字段（如 `$color.primary`）→ 对照 design token JSON

## 映射表填写规则

- 一 block 至少一行；一组件可多节点（容器+子 leaf）
- **platform** 列：web / ios / android / harmony / shared
- 节点在 metadata 不存在 → block 标 `blocked-映射`，VA 不生成臆造项

## 代码侧定位

- Vue：`.vue` + `<template>` 根元素 / `class` / `:deep` 目标
- React：组件文件 + `className` / styled / CSS module 键
- Token：CSS 变量名、`theme.*` 键、Tailwind 类与 `tailwind.config` 映射

## 禁止

- 无 block 证据的「全项目 grep 颜色」当审计完成
- 用截图图层名猜测节点 id
