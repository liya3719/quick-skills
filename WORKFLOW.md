# AI 研发流水线

本文描述从 **PRD → 需求拆解 → 技术方案 → 编码实现 → 测试用例** 的固定顺序、产物位置与版本约定，便于在新仓库复用同一套 Cursor Skills，而不绑定具体业务名称。

## 1. 技能与顺序（不可跳步）

| 顺序 | 阶段 | Cursor Skill（本仓库路径） | 产出物（典型） |
|------|------|---------------------------|----------------|
| 1 | 需求拆解 | `.cursor/skills/requirement-decomposition/` | 拆解文档（REQ-xxx）、`docs/prd/_snapshots/` PRD 快照 |
| 2 | 技术方案 | `.cursor/skills/rd-tech-solution/` | `docs/design/*-tech-solution-v*.md`（新文件升版，不覆盖旧版） |
| 3 | 编码实现 | `.cursor/skills/req-tech-design-codegen/` | 代码、REQ→实现映射、design token JSON 引用说明 |
| 4 | 测试用例 | `.cursor/skills/requirement-testcase-trace/` | `docs/testcases/*-testcases-v*.md`（需求变更则新文件） |

**依赖关系**：阶段 2 依赖阶段 1 的稳定 REQ；阶段 3 依赖阶段 1 + 2（契约与挂载点）；阶段 4 依赖阶段 1，并应与阶段 3 交付物可对齐（TC ↔ 代码/手测路径）。

触发方式：在对话中说明阶段与引用路径（例如「按 `/rd-tech-solution` 写方案」），或依赖各 Skill `description` 中的关键词由模型自动选用。

## 2. 目录约定

| 路径 | 用途 |
|------|------|
| `docs/prd/_snapshots/` | 原始 PRD 不可变快照（每次变更新增文件） |
| `docs/prd/` | 拆解文档：`{需求名}-v{x.y}.md` |
| `docs/design/` | 技术方案：`{需求名}-tech-solution-v{x.y}.md` |
| `docs/testcases/` | 测试用例：`{需求名}-testcases-v{x.y}.md` |
| 设计 token（任选） | 如 `design-tokens/` 或仓库约定目录，存放 **JSON** 真源 |

细则与拆解版本规则见：`docs/prd/README.md` 与 `requirement-decomposition/references/versioning.md`。

## 3. 版本与追溯合同

1. **拆解 ↔ 方案 ↔ 用例**：文档头或 `CHANGELOG` 中写明**上游 PRD 快照**、**本文件版本**；升版时 **新建文件**，禁止在历史终稿上静默整体替换为新版内容（各 Skill IRON LAW 已约束）。
2. **代码实现基线**：在拆解文档或团队约定处标明**分支 / tag / 工单**，使「运行中的代码」对应哪一版 REQ 可查。
3. **编码阶段**：以 **REQ + 技术方案 + design token JSON** 为准；token 与 REQ/方案冲突时列 OPEN 或确认，不私自定业务规则（见 `req-tech-design-codegen`）。

## 4. 迁移到新仓库的步骤

1. 复制（或 submodule）本仓库中的四个 Skill 目录至新仓库 `.cursor/skills/` 下同名路径。
2. 复制本文 `docs/WORKFLOW.md` 与 `docs/prd/README.md`（或合并为项目自己的一页「研发文档约定」）。
3. 在新仓库创建上表中的 `docs/prd/_snapshots/` 等空目录骨架。
4. 用 **一条小型需求** 跑通 1→4 全链路，校验文件命名与升版习惯，再推广到正式需求。

## 5. 自检

- [ ] 新成员仅依赖本文 + 各 Skill，能说出四阶段顺序与**禁止覆盖旧拆解/旧方案/旧用例**的边界。
- [ ] 任意一次迭代能在文档中查到：**REQ 列表、方案版本、用例版本、token 文件标识**。
- [ ] 需求变更后，PRD 快照、拆解、方案、用例中至少**新增文件**可追溯，而非单文件无版本改写。

---

**文档版本**：v1.0 | **维护**：与四条 Cursor Skill 同步修订；Skill 行为以各 `SKILL.md` 为准，本文只描述流程与落盘约定。
