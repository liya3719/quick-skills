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
| `docs/ai/codegen/` | 执行计划、架构对齐报告 |
| `docs/ai/visual-audit/` | 视觉偏差清单（VA-xxx） |
| `docs/ai/compile-verify/` | 编译验证报告 |
| `docs/ai/review/` | 架构与安全审查报告 |
| `.quick/skills-lock.json` | 安装记录（供 `quick skill:update` 使用） |

默认安装的 7 个 skill：

| 顺序 | 目录名 | 职责 |
|------|--------|------|
| 1 | `quick-requirement-decomposition` | 产品需求拆解（REQ-xxx） |
| 2 | `quick-tech-solution` | 研发技术方案 |
| 3 | `quick-req-driven-codegen` | REQ 驱动代码生成 |
| 4 | `quick-visual-audit` | UI 视觉审计（metadata 对账，VA 偏差清单） |
| 5 | `quick-compile-verify` | 编译验证（lint / tsc / build / 多平台 bundle） |
| 6 | `quick-requirement-testcase-trace` | 需求追溯测试用例（可选） |
| 7 | `quick-arch-security-code-review` | 架构与安全代码审查 |

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
⑤ 视觉审计 → docs/ai/visual-audit/  （有 UI 时；VA 清单回流 ③ 修复）
      │
      ▼
⑥ 编译验证 → docs/ai/compile-verify/
      │
      ▼
⑦ 架构与安全审查 → docs/ai/review/
```

**原则**：后一步消费上一步产物作为真源，不要跨 skill 发明业务规则。

**依赖关系**：

| 阶段 | Skill | 依赖 |
|------|-------|------|
| ① | 需求拆解 | PRD / 快照 |
| ② | 技术方案 | ① 稳定 REQ |
| ③ | 代码生成 | ① + ② + metadata + token JSON |
| ④ | 测试用例（可选） | ①（可与 ③ 并行；升版须方案研发确认） |
| ⑤ | 视觉审计 | ③ UI 实现 + metadata（**UI-N/A 可跳过**） |
| ⑥ | 编译验证 | ③ 架构对齐 pass + ⑤ pass 或 UI-N/A |
| ⑦ | 代码审查 | ⑥ 编译 pass |

**回流约定**：视觉 P0/P1 → 回流 ③ 修复（≤3 轮）；架构对齐 missing → 回流 ③（≤5 轮）；编译 auto-fix → 在 ⑥ 内修复（≤3 轮）。

**PRD 变更时**：须先完成增量拆解（新建 `docs/prd/` 版本），再升版方案与用例；不可跳过 diff 直接改旧文件。见下文 §「PRD 变更后的增量拆解」。

---

## 2.1 PRD 变更后的增量拆解

适用：产品定稿变更、验收口径调整、范围增删——**已有** `_snapshots` 快照与上一版拆解 / 方案 / 用例时。

### 原则

1. **快照只追加**：新 PRD 先存 `docs/prd/_snapshots/{需求名}-prd-v{N}-{日期}.md`，**不覆盖**旧快照。
2. **拆解对照 diff**：新拆解**新建** `docs/prd/{需求名}-v{x.y}.md`，在 §9 写 PRD diff 摘要与 **§9.2 REQ 级变更**（新增 / 修改 / 废弃）。
3. **方案对齐 §9.2**：新建 `docs/design/` 方案版本，**附录 D** 与拆解 §9.2 **REQ 列表一致**；未变模块可写「同 v1.0 §x.y」。
4. **研发确认后用例**：方案文档头须有 `研发确认：…` 后，才将 `docs/testcase/` 新用例标为终稿；基线用例只读，**仅对变更 REQ** 增改废 TC。
5. **三向互验**：拆解 §11、方案附录 G、用例矩阵中同一 REQ 须可互相检索；见 skill `references/three-way-traceability.md`。

### 逐步操作（Cursor / Claude Code）

| 步 | 在 IDE 中对 Agent 说（示例） | 落盘 |
|----|------------------------------|------|
| 0 | 「当前 PRD 相对 `_snapshots/…-prd-v1-….md` 有变更，请先存新快照。」 | `docs/prd/_snapshots/` 新文件 |
| 1 | 「按 **quick-requirement-decomposition** 做增量拆解：基线快照 …，继承 `需求名-v0.1.md`，产出 **v0.2**，含 PRD diff 与 §9.2 REQ 变更。」 | `docs/prd/需求名-v0.2.md` |
| 2 | 「按 **quick-tech-solution** 基于 v0.2 拆解写 **tech-solution-v1.1**，附录 D 对齐 §9.2，保留 v1.0。」 | `docs/design/…-v1.1.md` |
| 3 | 「请研发确认 v1.1 附录 D 与变更设计；确认后写入方案文档头。」 | 方案头 `研发确认：…` |
| 4 | 「**quick-requirement-testcase-trace** 升版：基线 `…-testcases-v1.0.md`，新建 v1.1，变更对照对齐 §9.2 + 附录 D。」 | `docs/testcase/…-v1.1.md` |
| 5 | 「核对三向矩阵：变更 REQ 在拆解、方案、用例中锚点与 TC 是否一致。」 | 更新 §11 / 附录 G |

### REQ 编号约定（变更时）

| 变更类型 | REQ 处理 |
|----------|----------|
| 新能力 | 新编号 `REQ-0xx` |
| 口径 / 范围变更 | **保留**原编号，§9.2 标「修改」 |
| 能力下线 | 标「废弃」，写明替代 REQ 或从哪版起不实现 |
| 仅措辞润色、验收不变 | 可不升 REQ；在 §9.1 摘要一句带过 |

### 禁止

- 在 `需求名-v0.1.md` 正文里直接改成 v0.2 内容而不新建文件
- 方案附录 D 与拆解 §9.2 REQ 列表不一致
- 方案未「研发确认」就发布用例终稿
- 三向矩阵对变更 REQ 标 `OK` 但方案或用例仍引用旧拆解版本

Skill 细则：`incremental-project-skills/quick-requirement-decomposition/references/prd-diff-incremental.md`、`quick-tech-solution/references/incremental-on-req-change.md`。

---

## 2.2 编码 → 视觉 → 编译（③⑤⑥）

适用：方案研发确认后进入实现；**有 UI 的 REQ 须走视觉审计**，纯逻辑迭代可标 UI-N/A 跳过 ⑤。

| 步 | 在 IDE 中对 Agent 说（示例） | 落盘 |
|----|------------------------------|------|
| 1 | 「按 **quick-req-driven-codegen**：必读拆解、方案、Figma/MasterGo metadata、token JSON、AGENTS.md；先写执行计划再分层实现。」 | `docs/ai/codegen/{需求名}-执行计划-v{x.y}.md` |
| 2 | 「实现完成后输出架构对齐报告，关键项 pass 后再进入视觉/编译。」 | `docs/ai/codegen/{需求名}-架构对齐报告-v{x.y}.md` |
| 3 | 「按 **quick-visual-audit** 对比 metadata：布局、间距、字号、颜色、状态、资源、响应式、多端。」 | `docs/ai/visual-audit/{需求名}-视觉偏差清单-v{x.y}.md` |
| 4 | 「存在 VA P0/P1：按偏差清单回流 **quick-req-driven-codegen** 精准修复 UI，修复后复审计（≤3 轮）。」 | 更新偏差清单「回流记录」 |
| 5 | 「视觉 pass 或 UI-N/A。按 **quick-compile-verify** 跑 lint → typecheck → build；含 Native 时验 bundle。」 | `docs/ai/compile-verify/{需求名}-编译验证报告-v{x.y}.md` |
| 6 | 「编译 pass 后按 **quick-arch-security-code-review** 做合并前审查。」 | `docs/ai/review/` |

### 禁止

- 无架构对齐报告就跑编译或宣称可合入
- 无 metadata 凭截图做视觉 pass
- 视觉 P0 未解进入编译验证
- 在本 skill 视觉审计阶段直接改 UI（应产出 VA 清单交 codegen）

---

## 3. Cursor 怎么用

1. 用 Cursor 打开本项目（确保能读到 `.cursor/skills/`）。
2. 将 PRD 放入 `docs/prd/`（建议快照放在 `docs/prd/_snapshots/`）。
3. 在 Agent 对话中引用 skill，例如：

> 按 **quick-requirement-decomposition** 拆解 `docs/prd/` 下的 PRD，输出 REQ-xxx 拆解稿。

4. 完成一步后，再进入下一步 skill。

**PRD 已变更、需增量拆解时**（已有 v0.1 与 `_snapshots`）：

> 基线 PRD 快照：`docs/prd/_snapshots/需求名-prd-v1-20260401.md`。请先存当前 PRD 为新快照，再按 **quick-requirement-decomposition** 对照 diff，**新建** `docs/prd/需求名-v0.2.md`（禁止覆盖 v0.1），含 §9.2 REQ 变更与 §11 三向矩阵。

后续按 §2.1 升版方案 → 研发确认 → 升版用例。

**首次实现或变更 REQ 已纳入方案后**（§2.2）：

> 按 **quick-req-driven-codegen** 实现 REQ-00x：方案见 `docs/design/…-v1.1.md`，metadata 见 `{路径}`，token JSON 见 `{路径}`。

> 架构对齐 pass。按 **quick-visual-audit** 审计 UI，输出 VA 偏差清单；有 P0/P1 则按清单回流 codegen 修复。

> 视觉 pass。按 **quick-compile-verify** 执行 lint、tsc、build（scope: web|all）。

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
| 执行计划 | `docs/ai/codegen/` | `{需求名}-执行计划-v{x.y}.md` |
| 架构对齐报告 | `docs/ai/codegen/` | `{需求名}-架构对齐报告-v{x.y}.md` |
| 视觉偏差清单 | `docs/ai/visual-audit/` | `{需求名}-视觉偏差清单-v{x.y}.md` |
| 编译验证报告 | `docs/ai/compile-verify/` | `{需求名}-编译验证报告-v{x.y}.md` |
| 测试用例 | `docs/testcase/` | `{需求名}-testcases-v{x.y}.md` |
| 审查报告 | `docs/ai/review/` | 按 skill 约定 |

**版本与追溯**：

1. 拆解 ↔ 方案 ↔ 用例：文档头写明上游 PRD 快照与本文件版本；升版时 **新建文件**，禁止静默覆盖旧版。
2. **PRD 变更链**：快照 diff → 拆解 §9.2 → 方案附录 D →（研发确认）→ 用例变更对照区；三文档 REQ 编号以**最新拆解**为准。
3. **三向矩阵**：拆解 §11 / 方案附录 G / 用例追溯矩阵互验；变更 REQ 须含可检索锚点与 TC，未就绪标 `待方案` / `待用例`。
4. 编码阶段：以 **REQ + 技术方案 + design metadata + token JSON** 为准；冲突时列 OPEN 或确认，不私自定业务规则。
5. 视觉阶段：以 **metadata / token 数值** 为准，产出 VA-xxx 回流 codegen；禁止截图目测 pass。
6. 编译阶段：以项目 **package.json / AGENTS.md** 脚本为准；可 auto-fix 的错误在 compile-verify 内修完重跑。
7. 各 skill 的 `SKILL.md` 中有更细约定，以 skill 正文为准。

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
A：执行 `quick skill:install --skills quick.requirement-decomposition,quick.tech-solution`（按需组合，编码后建议至少含 `quick.visual-audit` 与 `quick.compile-verify`）。

**Q：纯后端 / 无 UI 迭代要跑视觉审计吗？**  
A：不必。在执行计划与对齐报告中标 **UI-N/A**（须用户确认），跳过 ⑤ 直接进入 ⑥。

**Q：PRD 变了，要重做全流程吗？**  
A：不必。保留旧版文件，按 §2.1 做**增量拆解**（对照 `_snapshots` diff → 新建拆解 v0.x → 新建方案 v1.x → 研发确认 → 新建用例 v1.x）。未变更 REQ 的方案节可引用上一版，未变更 REQ 的 TC 可引用基线编号。

**Q：如何确认三文档没漂移？**  
A：对 §9.2 中每个变更 REQ，在拆解 §11、方案附录 G、用例矩阵中检查：同一 REQ 编号、方案锚点可 `Ctrl+F`、TC 编号存在且与变更类型一致。

**文档版本**：v2.2 | 与 quick-cli `ai-coding-full-flow` preset（7 skill）同步；含 PRD 增量拆解与编码→视觉→编译链路；Skill 行为以各 `SKILL.md` 为准。
