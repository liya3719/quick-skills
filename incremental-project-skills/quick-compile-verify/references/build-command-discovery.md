# 构建命令发现

## 何时加载

步骤 1，执行任何 shell 命令**之前**必读。

## 发现顺序

1. **`AGENTS.md` / `AGENT.md` / `CLAUDE.md`**（仓库根或子包）— 项目约定优先
2. **根 `package.json` scripts** — `lint` / `eslint` / `typecheck` / `check` / `build` / `dev` 勿混淆
3. **变更所在 workspace 的 `package.json`**（monorepo：`pnpm-workspace.yaml` / `lerna.json` / `nx.json`）
4. **CI 配置** — `.github/workflows/*.yml`、`Jenkinsfile`、`.gitlab-ci.yml` 中的 install + check + build 段
5. **框架约定**（无 script 时推断，须在报告中标注「推断」）：

| 栈 | 常见 lint | 常见 typecheck | 常见 build |
|----|-----------|----------------|------------|
| Vue3 + Vite | `eslint .` / `npm run lint` | `vue-tsc --noEmit` | `vite build` |
| React + Vite | 同上 | `tsc --noEmit` | `vite build` |
| Next.js | `next lint` | `tsc --noEmit` | `next build` |
| Rspack/Webpack | `eslint` | `tsc --noEmit` | `rspack build` / `webpack` |

## Monorepo

- 在**变更文件所属 package** 下执行脚本；根脚本若仅为 `turbo run build` 则用根命令
- filter 示例：`pnpm --filter <pkg> lint`、`nx run <project>:build`

## 验证命令表模板

```markdown
| 阶段 | 命令 | cwd | 来源 |
|------|------|-----|------|
| lint | | | |
| typecheck | | | |
| web build | | | |
```

## 禁止

- 未 Read `package.json` 就执行 `npm run build`
- 把 `dev` / `start` 当 build 验证
- 忽略 engines/node 版本要求
