# JavaScript + UI 实现

加载时机：用户声明 **JavaScript**（无 TS）时。

## 原则

- **契约**：用 JSDoc 为 props、API 载荷、`@typedef` 标注枚举与 REQ 一致字段；避免「口头约定」。
- **Token**：集中 `tokens.js` 或从 JSON `import`，组件只读对象键；不写散落的色值。
- **常量**：错误码、状态字符串用 `Object.freeze` 或 `as const` 等价模式（若环境支持）避免拼写漂移。
- **与 TS 混编仓库**：不破坏现有 `.ts` 契约；新文件若必须 JS，在边界处类型由 JSDoc 或相邻 `.d.ts` 补全（团队已有约定为准）。

## 自检

- [ ] 关键 REQ 字段在 JSDoc 或常量中与方案一致
- [ ] 无「猜」接口形状而不查方案
