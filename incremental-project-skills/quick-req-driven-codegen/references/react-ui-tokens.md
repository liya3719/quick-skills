# React + Design Token

加载时机：用户声明 **React**（或 Preact 等 JSX 栈且团队按 React 惯例）且实现含 token 还原的 UI 时。

## 原则

- **样式来源**：优先 CSS 变量（`:root`）或设计系统 `theme` 对象经 Context 下发；组件内避免 `style={{ color: '#...' }}` 除非你已在 OPEN 中说明且对齐某 token。
- **组织**：Presentational 与容器分离时，视觉仍只依赖 token/theme，不把业务字段掺进 className 拼装逻辑。
- **Hooks**：共享主题订阅用 `useContext`/`useTheme`；token JSON 的一次性解析与缓存放 hook 或模块级初始化，不在每个叶子组件重复读文件。
- **边界**：不为实现局部效果引入与方案冲突的第三方全局 CSS；若必须，记入「工程补充」与 REQ 关系。

## 自检

- [ ] 未见与 design token JSON 冲突的硬编码色值/间距（或已 OPEN）
- [ ] 无障碍与焦点环等若 REQ/方案有要求，未因「省事」省掉
