# AI Coding 全流程说明

本文说明 **AI Coding 全流程** 的步骤顺序、各 skill 职责与产物位置。由 `quick init` 或 `quick skill:install --preset ai-coding-full-flow` 安装到项目后，配合 Cursor / Claude Code 等 IDE 使用。

远程 skill 源：[https://github.com/liya3719/quick-skills](https://github.com/liya3719/quick-skills)

## 流程总览

```
PRD / 产品输入
      │
      ▼
① 需求拆解 (quick-requirement-decomposition)
      │  → docs/ai/requirements/ 或 docs/prd/
      ▼
② 技术方案 (quick-tech-solution)
      │  → docs/design/ 或 docs/ai/solution/
      ▼
      ├──────────────────────────────┐
      ▼                              ▼
③ 代码生成                    ④ 测试用例（可选）
(quick-req-driven-codegen)     (quick-requirement-testcase-trace)
      │                              → docs/testcase/
      ▼
⑤ 架构与安全审查 (quick-arch-security-code-review)
      → docs/ai/review/
```

**依赖关系**：不可跳步。阶段 2 依赖阶段 1 的稳定 REQ；阶段 3 依赖阶段 1 + 2；阶段 4 依赖阶段 1（可选，可与 3 并行）；阶段 5 依赖阶段 3 的代码交付。

## 各步骤说明

| 顺序 | Skill 目录名 | 职责 | 典型产物 |
|------|-------------|------|---------|
| 1 | `quick-requirement-decomposition` | 将 PRD 拆解为 REQ-xxx 原子需求 | 拆解文档、PRD 快照 |
| 2 | `quick-tech-solution` | 基于拆解稿输出可实施技术方案 | `*-tech-solution-v*.md` |
| 3 | `quick-req-driven-codegen` | 以 REQ + 方案 + design token 驱动编码 | 代码、实现映射说明 |
| 4 | `quick-requirement-testcase-trace` | 生成功能/异常/边界三层用例（可选） | `docs/testcase/` |
| 5 | `quick-arch-security-code-review` | SOLID、安全、性能、死代码审查 | `docs/ai/review/` |

## 如何在 IDE 中使用

### Cursor

Skill 安装在 `.cursor/skills/<skill-dir>/`。在 Agent 对话中说明当前阶段并引用对应 skill，例如：

> 按 quick-requirement-decomposition 拆解这份 PRD，输出到 docs/prd/

### Claude Code

Skill 安装在 `.claude/skills/<skill-dir>/`。目录名与 `SKILL.md` frontmatter 的 `name` 一致，可用 slash command：

```
/quick-requirement-decomposition
/quick-tech-solution
```

## 目录约定

| 路径 | 用途 |
|------|------|
| `docs/prd/_snapshots/` | PRD 不可变快照 |
| `docs/prd/` | 需求拆解文档 |
| `docs/design/` | 技术方案 |
| `docs/testcase/` | 测试用例 |
| `docs/ai/` | AI flow 运行时产物 |
| `.ai/` | CLI 运行期状态（`runtime-state.json`、`artifact-index.json`） |

详细版本与升版规则见项目根目录 [`docs/WORKFLOW.md`](../WORKFLOW.md)（由 CLI 从 quick-skills 安装）。

## quick-cli 命令（可选）

安装 skill 后，如需 CLI 编排 flow 状态：

```bash
quick ai:start          # 启动 flow（交互选择）
quick ai:status         # 查看步骤与产物
quick ai:resume         # 恢复中断的 flow
quick flow:list         # 列出可用 flow
```

Flow ID 与模板对应关系：

| 模板 | 默认 Flow |
|------|-----------|
| Vue3Admin / Vue3Mobile | `quick.vue-ai-full-flow` |
| React / Component / Electron 等 | `quick.ai-full-flow` |

## IRON LAW（跨 Skill 通用）

1. **禁止发明**：实现须对应 REQ-xxx 或标注「工程补充」
2. **禁止覆盖**：升版时新建文件，保留旧版
3. **禁止静默删除**：未经确认不得删除代码或文档
4. **追溯优先**：需求 → 方案 → 代码 → 用例全链路可回溯

---

**文档版本**：v1.0 | 与 [quick-skills](https://github.com/liya3719/quick-skills) 增量 skill 同步维护
