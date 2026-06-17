# quick-skills

> AI Coding Skill 集合 —— 让增量项目快速落地，让存量项目持续进化。

---

## 背景与定位

在前端工程实践中，团队同时面临两类挑战：

1. **增量项目**：新需求从 PRD 到上线，需要在短周期内完成需求拆解、技术方案、编码、测试与审查，AI 可以贯穿全流程提效。
2. **存量项目**：已有项目在长期维护中积累了技术债务，需要借助 AI 辅助完成重构、治理、性能优化与规范对齐。

**quick-skills** 将这两类场景沉淀为可复用的 AI Skill，统一管理、按需组合，形成"需求驱动、全链路可追溯"的 AI Coding 工作流。

---

## 仓库结构

```
quick-skills/
├── incremental-project-skills/   # 增量项目 Skill 本体（SKILL.md，可独立插拔）
├── stock-project-governance/     # 存量项目 Skill 本体
├── manifests/                    # quick-cli 编排层（可选，见 manifests/README.md）
│   └── skills/                   # CLI 注册用 manifest，不随 skill 安装进项目
├── flows/                        # 多 skill 流程编排（quick-cli）
├── install-targets.json          # 多平台安装映射与 preset 定义（quick-cli）
└── docs/                         # 示例文档目录结构
```

### 双模式使用

| 模式 | 你需要什么 | 说明 |
|------|-----------|------|
| **可插拔 Skill** | 任意 `*/SKILL.md` 目录 | 复制到 `.cursor/skills` 或 `.claude/skills`，在 IDE 中直接触发，无需 quick-cli |
| **quick-cli 绑定** | 上表 + `manifests/` + `flows/` + `install-targets.json` | `quick init` / `quick skill:install` 安装 preset，`quick ai:start` 跑全流程 |

Skill 目录内 **不再放置** `skill.json`；CLI 元数据集中在 `manifests/skills/`，避免 Skill 本体看起来像 quick-cli 子模块。

### Skill 目录一览

```
incremental-project-skills/
├── quick-requirement-decomposition/    # 产品需求拆解
├── quick-tech-solution/                # 研发技术方案
├── quick-req-driven-codegen/           # REQ 驱动代码生成
├── quick-requirement-testcase-trace/   # 需求追溯测试用例
└── quick-arch-security-code-review/    # 架构与安全代码审查

stock-project-governance/
├── refactor-module/                    # 独立 / 链路模块重构
└── refactor-feature-addition/          # 存量模块新增功能

docs/                                   # 项目文档示例（PRD、方案、测试用例）
├── prd/
├── design/
└── testcase/
```

---

## 增量项目 Skill

覆盖新项目从立项到上线的五个核心阶段，每个 Skill 消费上游产物作为唯一真源，禁止跨 Skill 发明业务规则。

| 阶段 | Skill | 核心能力 |
|------|-------|---------|
| 📋 需求 | [`quick-requirement-decomposition`](./incremental-project-skills/quick-requirement-decomposition/SKILL.md) | 将 PRD 拆解为带 REQ-xxx 编号的原子需求，输出大模型 / 研发 / QA 三视图与追溯矩阵 |
| 📐 设计 | [`quick-tech-solution`](./incremental-project-skills/quick-tech-solution/SKILL.md) | 基于拆解稿输出可实施、可回溯的技术方案；支持子方案拆分与版本管理 |
| 💻 实现 | [`quick-req-driven-codegen`](./incremental-project-skills/quick-req-driven-codegen/SKILL.md) | 以 PRD + 技术方案 + design token JSON 为真源驱动编码，禁止发明产品逻辑 |
| 🧪 测试 | [`quick-requirement-testcase-trace`](./incremental-project-skills/quick-requirement-testcase-trace/SKILL.md) | 生成功能 / 异常 / 边界三层用例，输出至 **`docs/testcase/`**，每条 TC 追溯到 REQ-xxx |
| 🔍 审查 | [`quick-arch-security-code-review`](./incremental-project-skills/quick-arch-security-code-review/SKILL.md) | 覆盖 SOLID、XSS/CORS/SQLi、鉴权越权、死代码、性能热路径的深度审查 |

### 协作流程

```
PRD / 产品输入
      │
      ▼
需求拆解 (quick-requirement-decomposition)      → 输出 REQ-xxx 拆解稿
      │
      ▼
技术方案 (quick-tech-solution)                   → 消费拆解稿，输出总方案 + 子方案
      │
      ├───────────────────────────────────┐
      ▼                                   ▼
代码生成                              测试用例 → docs/testcase/
(quick-req-driven-codegen)            (quick-requirement-testcase-trace)
      │
      ▼
代码审查 (quick-arch-security-code-review)       → PR / 合并前深度审查
```

---

## CLI 集成清单

远程仓库：**[https://github.com/liya3719/quick-skills](https://github.com/liya3719/quick-skills)**

为支持 quick-cli 发现和安装 skill，本仓库在 **编排层**（与 Skill 本体分离）提供：

| 文件 / 目录 | 作用 | 是否随 skill 安装进项目 |
|------------|------|------------------------|
| `manifests/skills/*.json` | 单个 skill 的 CLI 注册信息（入口、输入输出、适用模板） | 否 |
| `flows/*/flow.json` | 多 skill 编排顺序与产物别名 | 复制到项目 `.ai/flows/` |
| `install-targets.json` | 多平台安装映射与 `ai-coding-full-flow` preset | 否（仅 CLI 读取） |

详见 [`manifests/README.md`](./manifests/README.md)。

- `manifests/skills/*.json`：`sourceDir` 指向 Skill 本体目录，`entry` 通常为 `SKILL.md`
- `flow.json`：步骤 `outputs` 为编排层别名；真实路径见各 skill manifest 的 `outputs`
- `install-targets.json`：声明 `.cursor/skills`、`.claude/skills` 等平台目录名

### Flow 列表

| Flow ID | 适用场景 | 默认 |
|---------|---------|------|
| `quick.vue-ai-full-flow` | Vue3Admin / Vue3Mobile 增量全流程 | 是（Vue 模板） |
| `quick.ai-full-flow` | 通用增量全流程 | 否 |
| `quick.refactor-module-flow` | 存量模块重构 | 否 |
| `quick.refactor-feature-flow` | 存量模块新增功能 | 否 |

### Skill 注册范围

- **增量项目**：`incremental-project-skills/` 下 5 个 skill（manifest 在 `manifests/skills/`）
- **存量治理**：`stock-project-governance/` 下 2 个 skill（manifest 在 `manifests/skills/`）

### init 安装 preset

`quick init` 选「是」加载 AI Coding 全流程时，CLI 按 `install-targets.json` 中 `presets.ai-coding-full-flow` 安装：

- 5 个增量 skill → `.cursor/skills/` + `.claude/skills/`
- 说明文档 → `docs/WORKFLOW.md`、`docs/ai/README.md`、`docs/ai/skills-overview.md`

产物约定：
- `manifests/skills/*.json` 的 `outputs` 写真实产物文件路径，例如 `docs/ai/requirements/requirements.v1.md`
- `flow.json.steps[].outputs` 写编排层产物别名，例如 `requirements_doc`、`codegen_doc`
- 建议由 CLI 在 `.ai/artifact-index.json` 中维护别名到真实文件路径的映射

---

## 存量项目 Skill

面向已有项目的持续治理场景，强调 **行为等价、最小改动、先文档后代码**，帮助团队在不破坏既有契约的前提下完成重构与功能扩展。

| 场景 | Skill | 适用 | 核心约束 | 主要产出 |
|------|-------|------|---------|---------|
| 🛠 重构 | [`refactor-module`](./stock-project-governance/refactor-module/SKILL.md) | 独立模块重构、链路模块重构、legacy 治理、需要快速回滚的 vn 重构 | 行为等价、禁止原地重写、`v1 / vn` 并存、三件套确认前禁止写代码 | 现状与风险、调用关系图、技术方案、重构计划、测试用例、重构报告 |
| ➕ 新增 | [`refactor-feature-addition`](./stock-project-governance/refactor-feature-addition/SKILL.md) | 在存量 / legacy 模块上新增或扩展功能 | 最小改动、禁止顺手改无关代码、先做影响范围分析、双文档确认前禁止写代码 | 技术方案、测试用例、必要时补充影响范围说明 |

### 协作流程

```
存量代码 + 新需求 / 治理目标
      │
      ▼
understand-anything / /understand    ← 先做代码理解，明确职责、契约、不变量
      │
      ├──────────────────────────────┐
      ▼                              ▼
    重构场景                      新增场景
(refactor-module)         (refactor-feature-addition)
      │                              │
      ▼                              ▼
现状/调用图/方案/计划/用例        技术方案 + 测试用例 + 影响范围
      │                              │
      └──────────── 用户确认 ────────┘
                     │
                     ▼
            实施编码（v1/vn 并存 或 最小改动）
                     │
                     ▼
            全量测试 + 三方一致性校对（代码 / 方案 / 用例）
                     │
                     ▼
            归档（重构报告 / 回归记录）
```

> 详见 [`stock-project-governance/README.md`](./stock-project-governance/README.md)

### 通用治理原则

- 先理解原模块的职责、契约、影响范围，再动手
- 先文档、后代码；三件套 / 双文档未确认前禁止写代码
- 禁止顺手优化与本次任务无关的代码
- 新增或实质修改的 API、类、函数必须补充**中文注释**
- 测试通过后再归档、再推进后续流程

---

## IRON LAW（跨 Skill 通用铁律）

| # | 规则 | 说明 |
|---|------|------|
| 1 | **禁止发明** | 每条实现承诺、接口字段、错误码必须对应到 REQ-xxx 或标注「工程补充」 |
| 2 | **禁止覆盖** | PRD 变更或方案升版时须新建版本文件，旧版保留可查 |
| 3 | **禁止静默删除** | 未经用户明确确认，不得删除代码或旧文件 |
| 4 | **追溯优先** | 需求 → 方案 → 代码 → 用例，全链路可回溯 |

---

## 如何贡献

### 增量项目 Skill

1. 在 `incremental-project-skills/` 下新建子目录，命名以 `quick-` 开头，使用 `kebab-case`
2. 子目录内包含 `SKILL.md`（主文件）及可选的 `references/` 参考资料目录
3. 在 [`incremental-project-skills/README.md`](./incremental-project-skills/README.md) 的 Skill 全景表格中补充条目

### 存量项目 Skill

1. 在 `stock-project-governance/` 下新建子目录，命名使用 `kebab-case`，体现重构 / 治理意图（如 `refactor-xxx`）
2. 子目录内包含 `SKILL.md`（主 Skill 文件）及 `references/` 模板目录（如现状与风险、技术方案、测试用例、影响范围等模板）
3. 严格遵循「先文档、后代码」「行为等价 / 最小改动」原则，并补充对应的核心约束与产出物清单
4. 在 [`stock-project-governance/README.md`](./stock-project-governance/README.md) 的 Skills 列表与目录结构中补充条目

---

## License

MIT
