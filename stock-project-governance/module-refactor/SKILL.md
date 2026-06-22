---
name: module-refactor
description: "通用模块级等价重构 skill：先用 understand-anything 理解调用链与模块职责，再评估影响范围与现状问题（架构/安全/编码），落盘技术方案、重构计划、双视角测试用例（研发契约 + QA 功能影响），经研发书面确认后旁路实现、单元测试、验证与反漂移、图谱更新与 QA 回归评估，最后输出重构报告。触发：模块重构、refactor module、重构这个模块、understand、understand-anything、调用链、影响范围、范围卡片、现状问题、技术债、技术方案、重构计划、测试用例、研发用例、QA回归、行为等价、SOLID、解耦、单测、验证改对了、反漂移、重构报告。Actions: 分析模块、建图谱、写方案、写计划、写用例、确认后改代码、回归测试、验证、出报告。"
license: MIT
metadata:
  version: "2.0"
---

# 模块级重构

**IRON LAW：在理解原代码基础上保持功能逻辑等价——不改变对外可观测行为、错误语义、时序与并发承诺。禁止在旧业务路径上原地重写；禁止顺手改无关代码。**未完成 Step 0（图谱就绪 + 范围冻结 + 交付物路径约定）**前禁止实现类编辑**；**《技术方案》《重构计划》《测试用例》落盘且 Step 4 研发确认前禁止写业务代码**；**单测全部通过且 Step 7.5 验证通过前禁止终版报告**；**方案/用例/实现禁止静默漂移**。

## 交付物路径 `{artifactRoot}`

默认：**项目根** `refactor/{模块名}/{version}/`（Step 0.1 可与用户改约定，须写入范围卡片）。

| 文件 | 阶段 |
|------|------|
| `技术方案.md` | Step 3 前定稿 |
| `重构计划.md` | Step 3 前定稿 |
| `测试用例.md`（研发 + QA 两章） | Step 3 前定稿 |
| `验证报告.md` | Step 7.5 |
| `QA回归影响评估.md` | Step 8 |
| `重构报告.md` | Step 10 |

升版**新建** `{version}` 目录，禁止无说明覆盖。

**渐进加载**：`understand-install.md` · `understand-call-chain.md` · `call-graph-output.md` · `pre-refactor-issues.md` · `solid-cohesion-performance.md` · `testcases-rd-qa.md` · `verify-and-drift.md` · `qa-regression-impact.md` · `refactor-report-template.md`

---

## Workflow

```text
Module Refactor Progress:

- [ ] Step 0: 范围 + understand-anything 就绪 ⛔ BLOCKING
- [ ] Step 1: 理解并书面化模块逻辑 ⚠️ REQUIRED
- [ ] Step 2: 调用图谱 + 影响范围 ⚠️ REQUIRED
- [ ] Step 2b: Mermaid 图 ⚠️ REQUIRED
- [ ] Step 2.5: 现状问题与风险清单 ⚠️ REQUIRED
- [ ] Step 3: 落盘三文档（含双视角测试用例）⚠️ REQUIRED
- [ ] Step 4: 研发确认（第一道门）⛔ BLOCKING
- [ ] Step 5: 旁路实现 ⚠️ REQUIRED
- [ ] Step 6: 迁移 + 切片内等价自检
- [ ] Step 6.5: 研发视角用例 → 项目单元测试 ⚠️ REQUIRED
- [ ] Step 7: 单测回归（全部通过）⛔ BLOCKING
- [ ] Step 7.5: 验证 + 反漂移 → 验证报告.md ⛔ BLOCKING
- [ ] Step 8: /understand --update + QA回归影响评估 ⚠️ REQUIRED
- [ ] Step 9: 研发二次确认 ⛔ BLOCKING
- [ ] Step 10: 重构报告.md ⚠️ REQUIRED
```

---

## Step 0：范围 + understand-anything ⛔ BLOCKING

### 0.1 范围与路径

- 问：目标模块物理边界（路径/包名）？
- 问：哪些**对外入口**须在行为等价集合内？
- 问：完成标准（测试、指标）？
- 问：`{artifactRoot}` 用默认还是自定义？

### 0.2 图谱与范围卡片 ⚠️ REQUIRED

1. 检查 `.understand-anything/knowledge-graph.json`
2. 无 → `references/understand-install.md`，安装并 **`/understand`**
3. 陈旧 → **`/understand --update`**
4. `references/understand-call-chain.md` → 主路径 + Mermaid
5. 写入 `{artifactRoot}/技术方案.md` → **`## 范围卡片`**

---

## Step 1：模块逻辑 ⚠️ REQUIRED

写入《技术方案》或独立说明，含：一句话职责、词汇表、不变量、对外契约、非显式行为。**未能复述前禁止 Step 3 定稿。**

---

## Step 2 / 2b：图谱与影响范围 ⚠️ REQUIRED

`references/call-graph-output.md`：入口、向下/横向图、边表+锚点、影响范围（直接/间接/观测）、风险热点、Mermaid。

---

## Step 2.5：现状问题 ⚠️ REQUIRED

`references/pre-refactor-issues.md`：架构、编码、安全、性能等；P0/P1 须证据；Issue ID 对表。

---

## Step 3：三文档落盘 ⚠️ REQUIRED

`references/solid-cohesion-performance.md` + `references/testcases-rd-qa.md`。**只写文档，不改业务代码。**

- **技术方案**：范围卡片、逻辑摘要、Issue→切片、目标结构、安全/质量/性能可验证结论
- **重构计划**：切片、文件/符号、回滚点
- **测试用例**：**研发视角** + **QA 视角**（QA 不写实现细节）

---

## Step 4：研发确认 ⛔ BLOCKING

展示范围卡片、图谱、问题清单、三文档、切片与回滚、单测标准、QA R0/R1。**明确书面确认前禁止 Step 5。**

---

## Step 5–6：实现与迁移

- 新路径实现；旧路径默认冻结
- 每片：等价入口与证据
- 新增/修改**对外 API**：按**项目规范**补文档注释

---

## Step 6.5：单元测试 ⚠️ REQUIRED

- 来源：`测试用例.md` **研发视角**
- 输出：**项目约定**的测试目录与框架
- 标题含用例 ID；隔离外部依赖

---

## Step 7：单测回归 ⛔ BLOCKING

Step 4 认可范围；**全部通过**；输出回归摘要（命令、通过/失败/跳过）。禁止删断言/skip 修失败。

---

## Step 7.5：验证与反漂移 ⛔ BLOCKING

`references/verify-and-drift.md` → 落盘 **`{artifactRoot}/验证报告.md`**

- 文档↔代码、入口级行为等价、差异表、计划外变更
- 问：哪条 RD 用例 + 哪个入口证明等价？说不清则停手。

---

## Step 8：图谱 + QA 评估 ⚠️ REQUIRED

1. **`/understand --update`**（有代码变更时**必须**）
2. `references/qa-regression-impact.md` → **`QA回归影响评估.md`**
3. 与测试用例 QA 章对读；计划外标 R0

---

## Step 9：研发二次确认 ⛔ BLOCKING

确认：切片完成、单测与验证报告、QA 评估、defer 已记录。**未确认禁止 Step 10。**

---

## Step 10：重构报告 ⚠️ REQUIRED

`references/refactor-report-template.md` → **`{artifactRoot}/重构报告.md`**

---

## Anti-Patterns

- 无图谱/证据编造调用链
- 跳过 Step 4 或 Step 9 写代码或出终版报告
- 测试用例缺 QA 视角，或 QA 写类名/方法名
- 未做 Step 7.5 就宣称改对
- 合入前未 `--update` 就定稿 QA 评估
- 方案/用例/实现漂移未修订
- 交付物只存在于对话

---

## Pre-Delivery Checklist

- [ ] Step 0：`{artifactRoot}` 约定清晰；范围卡片含锚点 + Mermaid
- [ ] Step 2.5 有证据；与方案 Issue ID 一致
- [ ] 三文档已落盘；Step 4 已确认
- [ ] 测试用例含研发 + QA 两章
- [ ] 旁路实现；旧路径未经确认未大改
- [ ] 单测与研发用例可追溯；Step 7 全过
- [ ] `验证报告.md` 已落盘
- [ ] Step 8：`--update` + `QA回归影响评估.md`
- [ ] Step 9 确认；`重构报告.md` 完整
- [ ] 无未申报无关 diff
