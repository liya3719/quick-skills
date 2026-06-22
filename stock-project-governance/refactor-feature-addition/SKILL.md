---
name: refactor-feature-addition
description: "存量模块/项目上新增功能：先 understand-anything 理解调用链与影响范围，再需求拆解→技术方案→实施计划→研发+QA双视角测试用例，三文档互验防漂移，研发确认后最小改动实现，单测全绿+上下游回归+终版反漂移校对。Actions: 加功能、扩展、挂能力、补需求、需求拆解、出方案、写计划、写用例、画调用链、评估影响、三向追溯、最小改动、补中文注释、跑单测、回归上下游、反漂移。对象: 老模块、legacy、存量代码、现有模块。Triggers: 老模块加功能、存量扩展、加 feature、新增能力、legacy 增能力、先理解再方案、不要顺手重构、最小改动、先方案后代码、REQ追溯。禁止: 未确认写代码、顺手重构无关逻辑、无单测合入、三文档漂移、无图谱证据编造调用链。"
---

IRON LAW：**图谱/理解未完成、三件套（需求拆解 + 技术方案 + 测试用例）未互验通过、研发未书面确认前，0 行业务实现代码；确认后仍须最小改动，禁止顺带改无关文件。**

# refactor-feature-addition — 存量模块新增功能

## 交付物路径 `{artifactRoot}`

默认：**项目根** `feature/{模块名}/{version}/`（Step 0 可与用户改约定，须写入范围卡片）。

| 文件 | 阶段 | 说明 |
|------|------|------|
| `需求拆解.md` | Step 2 | REQ-xxx 原子需求；可与 `docs/prd/` 对齐 |
| `技术方案.md` | Step 3 | 含存量理解、新功能设计、REQ 追溯 |
| `实施计划.md` | Step 4 | 切片、文件/符号、顺序、回滚点 |
| `测试用例.md` | Step 5 | **研发视角** + **QA 视角** 两章 |
| `验证报告.md` | Step 7.5 | 终版代码 ↔ 三文档反漂移 |

升版**新建** `{version}` 目录或递增文件名，禁止无说明覆盖旧版。

**渐进加载**：`understand-install.md` · `understand-call-chain.md` · `三向追溯矩阵.md` · `技术方案-overlay.md` · `实施计划模板.md` · `testcases-rd-qa.md` · `verify-and-drift.md` · `影响范围模板.md`（按需）

---

## Workflow

```text
Feature Addition Progress:

- [ ] Step 0: understand-anything 就绪 + 范围约定 ⛔ BLOCKING
- [ ] Step 1: 存量模块理解（职责、调用链、影响范围）⚠️ REQUIRED
- [ ] Step 2: 新功能需求拆解（REQ-xxx）⚠️ REQUIRED
- [ ] Step 3: 技术方案落盘 ⚠️ REQUIRED
- [ ] Step 4: 实施计划落盘 ⚠️ REQUIRED
- [ ] Step 5: 测试用例（研发 + QA 双视角）⚠️ REQUIRED
- [ ] Step 5.5: 三向追溯互验 ⛔ BLOCKING
- [ ] Step 6: 研发确认（第一道门）⛔ BLOCKING
- [ ] Step 7: 最小改动实现 + 中文注释 + 单元测试 ⚠️ REQUIRED
- [ ] Step 8: 单测全量通过 ⛔ BLOCKING
- [ ] Step 9: 上下游回归（测试用例 RG 条）⚠️ REQUIRED
- [ ] Step 7.5: 终版反漂移 → 验证报告.md ⛔ BLOCKING
```

---

## Step 0：understand-anything 就绪 ⛔ BLOCKING

### 0.1 范围与路径

- 问：目标模块物理边界（路径/包名）？
- 问：新功能挂载点候选与**不应受影响**的路径？
- 问：`{artifactRoot}` 用默认还是自定义（如 `docs/design/` + `docs/testcase/`）？

### 0.2 检查 understand-anything（Claude Code / Cursor 优先）

1. 检查 `.understand-anything/knowledge-graph.json`
2. **无** → 加载 `references/understand-install.md`，按环境安装并执行 `/understand`（或等价命令）
3. **陈旧**（`meta.json` 的 `lastAnalyzedAt` 早于目标文件变更）→ `/understand --update`
4. 加载 `references/understand-call-chain.md` → 主路径 + Mermaid，写入 `{artifactRoot}/技术方案.md` → **`## 范围卡片`**

**无插件环境**：在回复中列出已读关键路径/文件与仍不确定项；调用链每条边须附 **文件:符号** 证据；**禁止**无证据编造 node id。范围卡片标注 **「图谱来源：手工 Read + 静态分析」**。

---

## Step 1：存量模块理解 ⚠️ REQUIRED

加载 `references/技术方案-overlay.md`，写入《技术方案》§1–§2，须含：

- 一段话复述原模块职责、不变量、对外契约
- 上下游调用链（Mermaid + 文字）；范围大时加载 `references/影响范围模板.md`
- **不应受影响的路径**（显式列出）

**未能复述职责与不变量前，禁止进入 Step 2 定稿。**

执行前自问（写入技术方案或回复摘要）：

- 不做新能力时，原有主路径的输入/输出/错误语义是否应保持不变？
- 新能力的最小挂载点是哪一处？为何不是改既有大分支？
- 必须回归的上下游路径有哪些？

---

## Step 2：新功能需求拆解 ⚠️ REQUIRED

**已安装 `quick-requirement-decomposition`**：按该 skill 工作流产出 REQ-xxx 拆解稿；落盘 `{artifactRoot}/需求拆解.md` 或 `docs/prd/{需求名}-v{x.y}.md`（团队约定为准，须在范围卡片注明）。

**未安装**：按 `references/三向追溯矩阵.md` 中 REQ 字段要求，在 `{artifactRoot}/需求拆解.md` 手写原子需求：

- 每条 REQ 仅含一条能力或规则；编号 REQ-001、REQ-002、…
- 每条 REQ 须有三视图摘要：大模型意图、研发边界/触点、QA 验收线索
- 未知项列 OPEN-xxx，不得用模糊措辞掩盖

**确认门**：呈现 REQ 条数、OPEN 条数、范围与非目标；用户确认或明确缩小范围后再继续。

---

## Step 3：技术方案 ⚠️ REQUIRED

加载 `references/技术方案-overlay.md`（**无论是否安装增量 skill 均必读**）。

**已安装 `quick-tech-solution`**：正文按该 skill 的 `document-outline.md` 撰写，并**追加 overlay 必含章节**（范围卡片、§1–§2、§5、§8、附录 A）；落盘 `{artifactRoot}/技术方案.md` 或 `docs/design/{需求名}-tech-solution-v{x.y}.md`。

**未安装**：以 overlay 为最低结构；每条设计承诺锚定 REQ-xxx 或显式「工程补充」。

**只写文档，不改业务代码。**

---

## Step 4：实施计划 ⚠️ REQUIRED

按 `references/实施计划模板.md` 落盘 `{artifactRoot}/实施计划.md`：

- 按 REQ 或挂载点切分实现切片（顺序、依赖）
- 每片对应文件/符号、预估改动类型、回滚点
- 与《技术方案》§5「最小改动证据」预对齐

---

## Step 5：测试用例（研发 + QA 双视角）⚠️ REQUIRED

加载 `references/testcases-rd-qa.md`（含落盘骨架与两章规则；**唯一用例 reference**）。

**已安装 `quick-requirement-testcase-trace`**：QA 视角按该 skill 三层结构 + flowchart；研发视角仍按 `testcases-rd-qa.md`；可与 `docs/testcase/` 交叉引用（范围卡片注明）。

回归用例（RG 条）须覆盖 Step 1 列出的上下游与「不应受影响」路径。

---

## Step 5.5：三向追溯互验 ⛔ BLOCKING

加载 `references/三向追溯矩阵.md`，建矩阵并逐项核对：

- 每个 REQ 在《技术方案》有设计锚点
- 每个 REQ 在《测试用例》有 TC（或 BLOCKED+OPEN）
- 每个 TC 能回溯 REQ 与技术方案章节
- 《实施计划》切片覆盖全部 REQ，无 orphan 设计

**矩阵有空行或 orphan → 先补文档，禁止进入 Step 6。**

---

## Step 6：研发确认 ⛔ BLOCKING

**停止**，输出：

> 四件套已生成（需求拆解、技术方案、实施计划、测试用例），路径：…  
> 三向追溯矩阵：REQ {n} 条，TC {m} 条，OPEN {k} 条  
> 是否确认开始写代码？(yes / no)

收到明确 `yes`（或等价肯定）前，不得修改实现代码（含「先改一行」）。

---

## Step 7–9：实现与验证

### Step 7：实现 ⚠️ REQUIRED

- 仅改《实施计划》与「最小改动证据」列出的文件；额外改动须先更新三文档并告知用户
- 新增/修改的 API、类、函数补齐**中文注释**
- 单元测试来源：《测试用例》**研发视角**；标题含用例 ID

### Step 8：单测全量通过 ⛔ BLOCKING

粘贴命令与摘要输出；**禁止**删断言 / skip 修失败。

### Step 9：上下游回归 ⚠️ REQUIRED

执行《测试用例》中 RG 条及 QA 视角 R0 场景；记录通过/失败。

### Step 7.5：终版反漂移 ⛔ BLOCKING

加载 `references/verify-and-drift.md` → 落盘 **`{artifactRoot}/验证报告.md`**：

- 终版代码 ↔ 需求拆解 ↔ 技术方案 ↔ 测试用例 四方对读
- **不一致先改文档并简述原因**，再更新验证报告
- 有代码变更时执行 `/understand --update`（若图谱可用）

---

## Red Flags（停下并说明）

- 无图谱且无手工证据时编造调用链
- 无法复述职责、不变量、契约即写代码
- REQ 在三文档间无法一一对齐
- 测试用例缺 QA 视角，或 QA 章写实现细节
- 无关文件改动或大范围无关格式化
- 改判断顺序/默认值/错误语义未进文档与用例
- 单测未全过即推合入
- 终版代码与三文档不一致且未修订

## 反模式

- 跳过 Step 5.5 或 Step 6 直接写代码
- 先实现再倒补 REQ / 测试对齐代码
- 大范围重构 + 新功能同一 PR
- 手工主流程代替单测全绿
- 三文档只存在于对话、未落盘
- 插新分支不补注释、不落测试映射

## 交付前自检

- [ ] `{artifactRoot}` 含需求拆解、技术方案、实施计划、测试用例、验证报告
- [ ] 三向追溯矩阵无 orphan REQ/TC
- [ ] 「最小改动证据」与 diff 一致
- [ ] 测试用例含研发 + QA 两章
- [ ] 新增或修改的 API/类/函数有中文注释
- [ ] 单测命令与结果已附，全量通过
- [ ] RG 回归已执行并记录
- [ ] 无无关改动（含无关依赖升级）
- [ ] 终版代码 ↔ 三文档一致（或文档已修订并说明原因）
