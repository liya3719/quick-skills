# Tailwind（及同类工具类方案）+ Design Token

加载时机：用户声明 **Tailwind** 或「工具类优先」且 token 需进 `tailwind.config.*` / `@theme` 时。

## 原则

- **单一真源**：从 design token JSON 派生 `theme.extend`（颜色、间距、字体、圆角、阴影）；禁止在 class 里长期依赖任意值 `[#hex]`、`[13px]`，除非 OPEN 已记录且对应缺失的 token。
- **命名**：`extend` 的键尽量与 JSON 语义路径一致（或团队映射表），便于对照设计与代码。
- **暗色 / 多主题**：用 `dark:`、`data-theme` 或 CSS 变量 + `tailwind` 引用变量，与 token JSON 的 mode 对齐；未在 REQ 中指定的主题切换方式 → 确认或 OPEN。
- **`@apply`**：仅适合小组件基类或在 `@layer components` 中封装；避免超长 `@apply` 链复制整张稿面。
- **与 JS**：若用 TS 维护 token 常量，再喂给 Tailwind 配置，避免两处手写两套数值。

## 自检

- [ ] `tailwind.config` 中可见与本次 JSON 导出对应的语义项
- [ ] 抽查页面：无「与 token 表毫无同名关系」的任意值类名堆砌
