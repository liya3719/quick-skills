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
├── incremental-project-skills/   # 增量项目 —— 从立项到上线的全流程 Skill
│   ├── quick-requirement-decomposition/    # 产品需求拆解
│   ├── quick-tech-solution/                # 研发技术方案
│   ├── quick-req-driven-codegen/           # REQ 驱动代码生成
│   ├── quick-requirement-testcase-trace/   # 需求追溯测试用例
│   └── quick-arch-security-code-review/    # 架构与安全代码审查
├── stock-project-governance/     # 存量项目 —— 重构、治理与持续优化 Skill
└── docs/                         # 项目文档（PRD、技术方案等）
```

---

## 增量项目 Skill

覆盖新项目从立项到上线的五个核心阶段，每个 Skill 消费上游产物作为唯一真源，禁止跨 Skill 发明业务规则。

| 阶段 | Skill | 核心能力 |
|------|-------|---------|
| 📋 需求 | [`quick-requirement-decomposition`](./incremental-project-skills/quick-requirement-decomposition/SKILL.md) | 将 PRD 拆解为带 REQ-xxx 编号的原子需求，输出大模型 / 研发 / QA 三视图与追溯矩阵 |
| 📐 设计 | [`quick-tech-solution`](./incremental-project-skills/quick-tech-solution/SKILL.md) | 基于拆解稿输出可实施、可回溯的技术方案；支持子方案拆分与版本管理 |
| 💻 实现 | [`quick-req-driven-codegen`](./incremental-project-skills/quick-req-driven-codegen/SKILL.md) | 以 PRD + 技术方案 + design token JSON 为真源驱动编码，禁止发明产品逻辑 |
| 🧪 测试 | [`quick-requirement-testcase-trace`](./incremental-project-skills/quick-requirement-testcase-trace/SKILL.md) | 生成功能 / 异常 / 边界三层用例，每条 TC 追溯到 REQ-xxx |
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
代码生成                              测试用例
(quick-req-driven-codegen)            (quick-requirement-testcase-trace)
      │
      ▼
代码审查 (quick-arch-security-code-review)       → PR / 合并前深度审查
```

---

## 存量项目 Skill

面向已有项目的持续优化场景，帮助团队降低维护成本、提升代码质量、加速新成员上手。

| 分类 | 说明 |
|------|------|
| 代码重构 | 组件拆分、逻辑解耦、类型补全 |
| 依赖治理 | 依赖升级、废弃包替换、包体积优化 |
| 性能优化 | 页面性能分析、懒加载、缓存策略 |
| 新员工入职 | 项目概览、本地运行、常见问题 FAQ |
| 规范对齐 | 存量代码迁移至新规范的操作指引 |
| 测试补全 | 单测覆盖率提升、E2E 测试引入 |

> 详见 [`stock-project-governance/README.md`](./stock-project-governance/README.md)

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

1. 在 `stock-project-governance/` 对应分类下新建子目录，命名使用 `kebab-case`
2. 每个 Skill 包含 `README.md` 说明文档 + 示例代码 / 操作步骤
3. 在 [`stock-project-governance/README.md`](./stock-project-governance/README.md) 的内容分类表格中补充条目

---

## License

MIT
