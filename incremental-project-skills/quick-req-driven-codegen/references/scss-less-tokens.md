# SCSS / Less + Design Token

加载时机：用户声明 **SCSS** 或 **Less**（或「预处理器 + 变量」）时。

## 原则

- **变量层**：由 token JSON（或构建生成）得到 `$color-text-primary` / `@spacing-md` 等**语义变量**；组件文件只引用变量名，不写裸 `#`/`px` 除非 OPEN。
- **SCSS**：优先 `@use`/`@forward` 控制作用域，避免全局 `@import` 污染；变量集中 `abstracts/_tokens.scss` 或构建产物。
- **Less**：同样集中 token 映射文件；注意与 Ant Design 等主题的变量名冲突时按项目约定加前缀。
- **`:root` 与预处理器**：若运行时用 CSS 变量换主题，由构建或脚本从 JSON 写入 `:root`，SCSS/Less 组件内用 `var(--x)` 对齐同一套名。
- **嵌套**：勿为还原一屏 UI 嵌套过深；与设计稿区块对应即可。

## CSS Modules（无预处理器时）

- 在模块内用 `composes` 或仅 `class` + **来自 `:root` 的 var**，仍遵守「无魔法数」；映射规则同 token JSON。

## 自检

- [ ] 搜索组件样式：裸色值/裸像素是否仅在允许的 OPEN 条目中
- [ ] 主题切换若存在，变量集与 JSON mode 一致
