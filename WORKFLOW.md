# AI Coding 研发流水线

本文说明 `quick init` / `quick skill:install` 安装完成后，如何在 IDE 中使用 AI Coding skill。

**CLI 只负责安装 skill 与本文档；具体执行在 Cursor / Claude Code 中完成。**

Skill 源仓库：[https://github.com/liya3719/quick-skills](https://github.com/liya3719/quick-skills)

---

## 1. 装好了什么

| 位置 | 内容 |
|------|------|
| `.cursor/skills/` | Cursor 可用的 skill（每个子目录含 `SKILL.md`） |
| `.claude/skills/` | Claude Code 可用的 skill |
| `docs/prd/` | PRD 快照、需求拆解产物 |
| `docs/design/` | 技术方案 |
| `docs/testcase/` | 测试用例 |
| `docs/ai/` | 审查报告等 AI 产物（可选） |
| `.quick/skills-lock.json` | 安装记录（供 `quick skill:update` 使用） |

默认安装的 5 个 skill：

| 顺序 | 目录名 | 职责 |
|------|--------|------|
| 1 | `quick-requirement-decomposition` | 产品需求拆解（REQ-xxx） |
| 2 | `quick-tech-solution` | 研发技术方案 |
| 3 | `quick-req-driven-codegen` | REQ 驱动代码生成 |
| 4 | `quick-requirement-testcase-trace` | 需求追溯测试用例（可选） |
| 5 | `quick-arch-security-code-review` | 架构与安全代码审查 |

---

## 2. 推荐顺序（不可跳步）

```
PRD / 产品输入
      │
      ▼
① 需求拆解 → docs/prd/
      │
      ▼
② 技术方案 → docs/design/
      │
      ├──────────────────────────────┐
      ▼                              ▼
③ 代码生成                    ④ 测试用例（可选）
      │                              → docs/testcase/
      ▼
⑤ 架构与安全审查 → docs/ai/review/
```

**原则**：后一步消费上一步产物作为真源，不要跨 skill 发明业务规则。

**依赖关系**：阶段 2 依赖阶段 1 的稳定 REQ；阶段 3 依赖阶段 1 + 2；阶段 4 依赖阶段 1（可与 3 并行）；阶段 5 依赖阶段 3 的代码交付。

---

## 3. Cursor 怎么用

1. 用 Cursor 打开本项目（确保能读到 `.cursor/skills/`）。
2. 将 PRD 放入 `docs/prd/`（建议快照放在 `docs/prd/_snapshots/`）。
3. 在 Agent 对话中引用 skill，例如：

> 按 **quick-requirement-decomposition** 拆解 `docs/prd/` 下的 PRD，输出 REQ-xxx 拆解稿。

4. 完成一步后，再进入下一步 skill。

---

## 4. Claude Code 怎么用

Skill 安装在 `.claude/skills/`。在 Claude Code 中可用 slash 命令触发，例如：

```
/quick-requirement-decomposition
```

按 skill 内 `SKILL.md` 的说明提供 PRD 路径与期望输出目录。

---

## 5. 产物与版本约定

| 阶段 | 建议目录 | 典型命名 |
|------|---------|---------|
| PRD 快照 | `docs/prd/_snapshots/` | 不可变快照，变更新增文件 |
| 需求拆解 | `docs/prd/` | `{需求名}-v{x.y}.md` |
| 技术方案 | `docs/design/` | `{需求名}-tech-solution-v{x.y}.md` |
| 测试用例 | `docs/testcase/` | `{需求名}-testcases-v{x.y}.md` |
| 审查报告 | `docs/ai/review/` | 按 skill 约定 |

**版本与追溯**：

1. 拆解 ↔ 方案 ↔ 用例：文档头写明上游 PRD 快照与本文件版本；升版时 **新建文件**，禁止静默覆盖旧版。
2. 编码阶段：以 **REQ + 技术方案 + design token JSON** 为准；冲突时列 OPEN 或确认，不私自定业务规则。
3. 各 skill 的 `SKILL.md` 中有更细约定，以 skill 正文为准。

---

## 6. 可选后续

| 命令 | 用途 |
|------|------|
| `quick add` | 接入 ESLint、Prettier、Commitlint、Husky 等工程化配置 |
| `quick build:tools` | 接入 vite / rspack / webpack 构建配置 |
| `quick skill:update` | 更新 quick-skills 并重新安装本项目 preset |
| `quick skill:list` | 查看 quick-skills 仓库中全部可安装 skill |

---

## 7. 常见问题

**Q：还需要运行 `quick ai:start` 吗？**  
A：不需要。直接在 IDE 中按上文顺序使用 skill 即可。

**Q：skill 更新了怎么办？**  
A：在项目根执行 `quick skill:update`。

**Q：只想装部分 skill？**  
A：执行 `quick skill:install --skills quick.requirement-decomposition,quick.tech-solution`。

---

**文档版本**：v2.0 | 与 quick-cli skill 安装 preset 同步；Skill 行为以各 `SKILL.md` 为准。
