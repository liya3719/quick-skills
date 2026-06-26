# 错误分流与修复

## 何时加载

步骤 4；任一步骤失败时必读。

## 分流决策树

```
报错
 ├─ 环境/工具链（Node 版本、pnpm store、磁盘、权限、SDK 未装）→ env-blocked → OPEN
 ├─ 契约/方案冲突（字段与 quick-tech-solution 不一致且无法推断）→ decision-blocked → OPEN
 ├─ 需改根配置或团队 lint 豁免 → decision-blocked → 用户确认
 └─ 其余 → auto-fix → 改代码 → 重跑
```

## auto-fix 典型模式

| 现象 | 定位 | 修复原则 |
|------|------|----------|
| Cannot find module | tsconfig paths、alias、相对路径、index 导出 | 对齐项目 alias；补 export |
| Type X not assignable to Y | 调用处 vs 类型定义、API 响应 DTO | 对齐 types.ts / 方案字段 |
| Property foo does not exist | 重命名遗漏、可选链 | 全局搜符号，改引用非删类型 |
| ESLint import/order | 规则可 auto-fix | `eslint --fix` 限定文件 |
| Unused vars | 真未使用 vs 应用未接完 | 删 import；或接回业务（对齐执行计划） |
| Peer dependency | package.json | 确认后安装，报告记录 |

## 修复纪律

1. **最小 diff**：优先改变报错文件及直接依赖的类型/导出
2. **读报错栈顶**：TS 报错的第一个非 node_modules 位置
3. **对照执行计划 / 对齐报告**：字段名以方案与 types 为准，不发明字段
4. **每轮一条主因**：避免一轮改十处无记录
5. **禁止**默认 `@ts-ignore`；仅临时且 OPEN 说明时可提议，须用户确认

## fix-rounds

- 默认上限 **3** 轮（`$ARGUMENTS --fix-rounds N`）
- 同一错误签名连续 2 轮未变：换思路（查 tsconfig、查 monorepo 边界、查是否改错包）
- 用尽仍失败 → 报告 **blocked**，附未解错误列表与已尝试修复

## OPEN 模板

```markdown
### OPEN-BV-001 [env-blocked | decision-blocked]
- **现象**：
- **证据**：（log 摘要 + 命令）
- **需要研发**：（装 SDK / 确认字段 / 批准改 eslint 等）
- **阻塞步骤**：lint | typecheck | build | ios | android | harmony
```

## 禁止

- 删除功能代码「先过编译」
- 升级 major 依赖未经确认
- 把 env-blocked 当 auto-fix 反复重试同一命令
