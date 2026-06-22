# 存量代码治理 Skills

> 本目录提供 2 个可直接使用的 skill，覆盖存量代码两大场景：**模块等价重构** 与 **存量模块新增功能**。二者均优先依赖 `understand-anything` 做代码理解，遵循「先文档、后代码、确认门、反漂移」治理原则。

## 选型：用哪个 Skill？

| 你的目标 | 选用 | 核心差异 |
|----------|------|----------|
| 改善结构/解耦/还债，**不改变**对外行为 | `module-refactor` | 行为等价、旁路实现、v1/vn 并存、双确认门 |
| 在现有模块上**加新能力**，允许增量行为 | `refactor-feature-addition` | 最小改动、REQ 拆解、三向追溯、四件套确认 |

**不要混用**：等价重构与新增功能不应在同一 PR 里捆绑；若两者都需要，先拆任务、分版本目录。

---

## Skills 一览

| Skill | 目录 | 适用场景 | 铁律摘要 | 默认产出路径 |
|-------|------|----------|----------|--------------|
| `module-refactor` | `module-refactor/` | 独立/链路模块重构、legacy 治理、技术债偿还 | 行为等价；禁止原地重写；三文档 + 双确认门前禁止写代码 | `refactor/{模块名}/{version}/` |
| `refactor-feature-addition` | `refactor-feature-addition/` | 老模块加功能、存量扩展、legacy 增能力 | 最小改动；三向追溯互验 + 研发确认前禁止写代码 | `feature/{模块名}/{version}/` |

CLI manifest 见 [`manifests/skills/`](../manifests/skills/)（`quick.module-refactor`）。

---

## 目录结构

```text
stock-project-governance/
├── README.md
├── module-refactor/
│   ├── SKILL.md
│   └── references/
│       ├── understand-install.md
│       ├── understand-call-chain.md
│       ├── call-graph-output.md
│       ├── pre-refactor-issues.md
│       ├── solid-cohesion-performance.md
│       ├── testcases-rd-qa.md
│       ├── verify-and-drift.md
│       ├── qa-regression-impact.md
│       └── refactor-report-template.md
└── refactor-feature-addition/
    ├── SKILL.md
    └── references/
        ├── understand-install.md
        ├── understand-call-chain.md
        ├── 三向追溯矩阵.md
        ├── 技术方案-overlay.md
        ├── 实施计划模板.md
        ├── testcases-rd-qa.md
        ├── verify-and-drift.md
        └── 影响范围模板.md          # 按需加载
```

---

## Skill 1：`module-refactor` — 模块等价重构

### 适用场景

- 独立模块或链路模块的结构治理
- legacy 模块解耦、分层、去技术债
- 需要旁路实现与快速回滚的 vn 重构

### 工作流（11 步）

```text
Step 0   understand-anything 就绪 + 范围约定          ⛔
Step 1   书面化模块逻辑（职责、不变量、契约）         ⚠️
Step 2   调用图谱 + 影响范围 + Mermaid               ⚠️
Step 2.5 现状问题与风险清单（架构/安全/编码/性能）   ⚠️
Step 3   落盘三文档（技术方案 + 重构计划 + 测试用例）⚠️
Step 4   研发确认（第一道门）                        ⛔
Step 5–6 旁路实现 + 迁移 + 切片内等价自检
Step 6.5 研发视角用例 → 项目单元测试                 ⚠️
Step 7   单测全量通过                                ⛔
Step 7.5 验证 + 反漂移 → 验证报告.md                 ⛔
Step 8   /understand --update + QA回归影响评估.md    ⚠️
Step 9   研发二次确认                                ⛔
Step 10  重构报告.md                                 ⚠️
```

### 交付物

| 文件 | 说明 |
|------|------|
| `技术方案.md` | 含范围卡片、Issue→切片、目标结构 |
| `重构计划.md` | 切片、文件/符号、回滚点 |
| `测试用例.md` | **研发视角** + **QA 视角** 两章 |
| `验证报告.md` | 文档↔代码、入口级行为等价 |
| `QA回归影响评估.md` | 重构后实际影响 vs 计划 |
| `重构报告.md` | 终版归档 |

### 核心约束

- 不改变对外可观测行为、错误语义、时序与并发承诺
- 禁止在旧业务路径上原地重写；新路径旁路实现，旧路径默认冻结
- 禁止顺手改与重构无关的代码
- 方案 / 用例 / 实现禁止静默漂移；不一致先修文档

### references 说明

| 文件 | 加载时机 |
|------|----------|
| `understand-install.md` | 无图谱时 |
| `understand-call-chain.md` | Step 0 建链 |
| `call-graph-output.md` | Step 2 输出调用图 |
| `pre-refactor-issues.md` | Step 2.5 问题清单 |
| `solid-cohesion-performance.md` | Step 3 方案设计 |
| `testcases-rd-qa.md` | Step 3 双视角用例 |
| `verify-and-drift.md` | Step 7.5 反漂移 |
| `qa-regression-impact.md` | Step 8 QA 评估 |
| `refactor-report-template.md` | Step 10 报告 |

---

## Skill 2：`refactor-feature-addition` — 存量模块新增功能

### 适用场景

- 在老模块上挂新能力、扩展接口
- legacy 模块增量需求，要求最小变更面
- 需要先理解存量调用链与影响范围再设计

### 工作流（12 步）

```text
Step 0    understand-anything 就绪（Claude Code / Cursor 优先）⛔
Step 1    存量理解（职责、调用链、不应受影响路径）              ⚠️
Step 2    新功能需求拆解（REQ-xxx）                             ⚠️
Step 3    技术方案（+ overlay 必含章节）                        ⚠️
Step 4    实施计划（切片 / 回滚）                               ⚠️
Step 5    测试用例（研发 + QA 双视角）                          ⚠️
Step 5.5  三向追溯互验（拆解 ↔ 方案 ↔ 用例 ↔ 计划）           ⛔
Step 6    研发确认（第一道门）                                  ⛔
Step 7    最小改动实现 + 中文注释 + 单元测试                    ⚠️
Step 8    单测全量通过                                          ⛔
Step 9    上下游回归（RG 条 + QA R0）                           ⚠️
Step 7.5  终版反漂移 → 验证报告.md                               ⛔
```

### 交付物

| 文件 | 说明 |
|------|------|
| `需求拆解.md` | REQ-xxx 原子需求；可对接 `docs/prd/` |
| `技术方案.md` | 存量理解 + 新功能设计 + §5 最小改动证据 + §8 测试映射 |
| `实施计划.md` | 按 REQ/挂载点切片 |
| `测试用例.md` | 研发视角（契约/RG）+ QA 视角（功能回归） |
| `验证报告.md` | 终版代码 ↔ 四文档四方对读 |

### 与 incremental-project-skills 的协作

| 已安装 skill | 委托范围 |
|--------------|----------|
| `quick-requirement-decomposition` | Step 2 需求拆解 |
| `quick-tech-solution` | Step 3 方案正文（仍须追加 `技术方案-overlay.md` 章节） |
| `quick-requirement-testcase-trace` | Step 5 QA 三层用例 + flowchart |

未安装时，由本 skill 的 references 提供最低结构约束。

### 核心约束

- **最小改动**：能新建类/策略就不在长函数堆分支
- 禁止顺手重构、格式化或改与需求无关的文件
- 三向追溯矩阵无 orphan REQ/TC 才能进入研发确认
- 单测全绿 + RG 回归通过后，终版四方对读；不一致**先改文档**

### references 说明

| 文件 | 加载时机 |
|------|----------|
| `understand-install.md` | 无图谱时（含 Cursor / Claude Code 检测） |
| `understand-call-chain.md` | Step 0–1 调用链与影响范围 |
| `技术方案-overlay.md` | Step 1、3（存量新增专有章节） |
| `三向追溯矩阵.md` | Step 5.5 互验 |
| `实施计划模板.md` | Step 4 |
| `testcases-rd-qa.md` | Step 5（唯一用例 reference，含落盘骨架） |
| `verify-and-drift.md` | Step 7.5 |
| `影响范围模板.md` | 影响面复杂时按需 |

---

## 通用治理原则

两个 skill 共用：

1. **先理解、后动手** — `understand-anything` 优先；无图谱时手工分析并附 `文件:符号` 证据
2. **先文档、后代码** — 确认门前 0 行业务实现编辑
3. **双视角测试** — 研发视角（契约/自动化）+ QA 视角（用户可感知，不写实现细节）
4. **反漂移** — 终版代码与文档不一致时，先修订文档并记录原因
5. **SOLID** — 高内聚低耦合；禁止无关 diff
6. **升版不覆盖** — 新建 `{version}` 目录或递增文件名，保留历史可查

---

## 如何使用

### 安装

- **Cursor**：复制 skill 目录到 `.cursor/skills/`，或通过 `quick skill:install`（见 [`install-targets.json`](../install-targets.json)）
- **Claude Code**：复制到 `.claude/skills/`，或使用 slash 命令

### 典型触发语句

**模块重构**

- `重构 settlement 模块，保持行为等价，输出方案和计划后再写代码`
- `把订单履约链路做 vn 重构，要求旁路实现、支持快速回滚`
- `分析 legacy 支付模块调用链，先出现状问题清单和双视角用例`

**新增功能**

- `给现有库存模块加预占库存功能，要求最小改动，不要顺手重构`
- `在 legacy 支付模块里新增超时取消能力，先 understand 再出 REQ 和方案`
- `老模块加 feature：先需求拆解和三向追溯，确认后再写代码`

### understand-anything 前置

两个 skill 均检查 `.understand-anything/knowledge-graph.json`。首次使用：

```bash
/plugin marketplace add Lum1104/Understand-Anything   # Claude Code
/plugin install understand-anything
/understand
```

合入代码变更后执行 `/understand --update` 刷新图谱。

---

**文档版本**：v3.0 — 与 `module-refactor` v2.0、`refactor-feature-addition` v2.0 能力对齐；Skill 行为以各目录 `SKILL.md` 为准。
