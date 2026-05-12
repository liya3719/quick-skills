# TypeScript + UI 实现

加载时机：用户声明 **TypeScript** 时（与框架无关）。

## 原则

- **契约与类型**：接口请求/响应、路由参数、与方案一致的枚举与字面量联合类型；不把 `any` 当作「方案未写清」的替身——缺类型应 OPEN 或「工程补充」注释。
- **Token 与类型**：theme、token 映射用 `as const` + `satisfies`（或等价）保证键与 JSON 导出同步；大对象可从生成文件 `import type`。
- **组件 Props**：`interface`/`type` 显性列出可选与默认；与 REQ 字段同名的 prop 不私自改语义。
- **窄化**：从方案中的状态机、错误码做 `switch` exhaustiveness check（`never` 分支）避免漏分支。

## 自检

- [ ] 对外导出或 API 层无未解释的 `any`（或已注明原因）
- [ ] 与 REQ 相关的字面量可与方案 Ctrl+F 对上
