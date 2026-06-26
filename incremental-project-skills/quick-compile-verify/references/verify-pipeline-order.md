# Web 验证管线顺序

## 何时加载

步骤 2。

## 标准顺序 ⛔

```
lint → typecheck → web build
```

### 1. Lint

- 目标：静态规则、import 顺序、未使用变量、hooks 规则等
- 若项目提供 `lint:fix` 且仅 style 类失败：可 fix 后重跑 lint，再进入 typecheck
- **逻辑错误**（如错误 hook 依赖）须改代码，不能仅靠 fix

### 2. Typecheck

- `tsc --noEmit` / `vue-tsc --noEmit` / 项目封装 `type-check`
- 与 build 区别：更快暴露类型错误；**须在本步清零**再 build

### 3. Web build

- 生产或 CI 等价 build（`vite build` / `next build` / `rspack build`）
- 验证：exit 0、产物目录存在（如 `dist/`、`.next/`）

## 失败时

- **停止**后续步骤
- 进入 `error-triage-and-fix.md` 修复循环
- 修复后**从失败步骤重跑**，不必从 lint 重头（若修复可能影响全局类型则从 typecheck 重跑）

## 可选步骤（项目有则跑，报告标 optional）

- `test` / `test:unit` — 单测非本 skill 必需，除非用户或 AGENTS.md 要求
- `stylelint` — 与 UI lint 分开记录

## 禁止

- build 过了就跳过 lint/typecheck
- 用 `skipLibCheck` 等改 tsconfig **全局**关检查（须 OPEN + 用户确认）
