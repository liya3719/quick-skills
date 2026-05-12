# Vue 3 + Design Token

加载时机：用户声明 **Vue 3**（或兼容 API 的同类栈）且实现含 token 还原的 UI 时。

## 原则

- **单文件组件（SFC）**：结构、逻辑、 scoped 样式同文件；与 token 相关的**语义变量**优先放在 `assets/styles/tokens` 或通过构建注入，避免在多个 `.vue` 里复制同一 `#hex`。
- **主题与 Token**：全局 token 用 CSS 自定义属性（`:root` / `html[data-theme]`）或 Pinia/插件暴露只读 theme 对象；子组件只读不写散列魔法值。
- **Scoped 与变量**：需要覆盖时用 `:deep()` 谨慎穿透；与设计 token 冲突时优先改 token 源，不在 scoped 里堆任意像素凑数。
- **Props / Emit**：对外契约与 REQ、方案一致；不在组件层发明业务状态名。
- **Composables**：跨页面共享的布局与主题逻辑进 `composables/`，不在每个页面重复解析 JSON。

## 自检

- [ ] 颜色/间距/圆角来自 token 映射，未在 template 内联与 JSON 冲突的 style
- [ ] 多主题与 REQ 一致时，切换入口与 token 集对应同一套文档说明
