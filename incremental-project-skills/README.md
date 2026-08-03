# 新项目

> 本目录收录新项目从立项到上线全流程的 AI Skill，覆盖需求拆解 → 技术方案 → 代码实现 → 视觉审计 → 编译验证 → 测试用例 → 代码审查。

---

## Skill 全景

| 阶段 | 目录 | Skill 名称 | 核心能力 |
|------|------|-----------|---------|
| 📋 需求 | [`quick-requirement-decomposition`](./quick-requirement-decomposition/SKILL.md) | 产品需求拆解 | 将 PRD 拆解为带 REQ-xxx 编号的原子需求，输出大模型 / 研发 / QA 三视图与追溯矩阵 |
| 📐 设计 | [`quick-tech-solution`](./quick-tech-solution/SKILL.md) | 研发技术方案 | 基于拆解稿输出可实施、可回溯的技术方案；支持子方案拆分、版本管理与附录追溯 |
| 💻 实现 | [`quick-req-driven-codegen`](./quick-req-driven-codegen/SKILL.md) | REQ 驱动代码生成 | 以 PRD + 技术方案 + design token JSON 为真源驱动编码，禁止发明产品逻辑 |
| 👁 视觉 | [`quick-visual-audit`](./quick-visual-audit/SKILL.md) | UI 视觉审计 | 对比 metadata/token 校验布局、间距、字号、颜色、状态、资源、响应式与多端；VA 清单回流 codegen |
| 🔧 验证 | [`quick-compile-verify`](./quick-compile-verify/SKILL.md) | 编译验证 | lint / tsc / build / 多平台 bundle；失败定位修复 |
| 🧪 测试 | [`quick-requirement-testcase-trace`](./quick-requirement-testcase-trace/SKILL.md) | 需求追溯测试用例 | 生成功能 / 异常 / 边界三层用例，输出至 **`docs/testcase/`**，每条 TC 追溯到 REQ-xxx |
| 🔍 审查 | [`quick-arch-security-code-review`](./quick-arch-security-code-review/SKILL.md) | 架构与安全代码审查 | 覆盖 SOLID、XSS/CORS/SQLi、鉴权越权、死代码、性能热路径的深度 Code Review |
| 📊 观测 | [`quick-pipeline-observability`](./quick-pipeline-observability/SKILL.md) | 流水线观测 | 只读扫描各阶段产物，产出 `docs/ai/metrics` 指标 JSON/报告与 rollup；无埋点平台 |

---

## Skill 协作关系

```
PRD / 产品输入
      │
      ▼
quick-requirement-decomposition   ← 输出 REQ-xxx 拆解稿（真源）
      │
      ▼
quick-tech-solution               ← 消费拆解稿，输出总方案 + 子方案（附录 F）
      │
      ├──────────────────────────────────────────┐
      ▼                                          ▼
quick-req-driven-codegen     quick-requirement-testcase-trace
（按方案 + token 驱动实现）    （按 REQ 生成三层测试用例）
      │
      ▼
quick-visual-audit                ← metadata 对账，VA 偏差清单回流 codegen
      │
      ▼
quick-compile-verify              ← lint / tsc / build / bundle
      │
      ▼
quick-arch-security-code-review   ← PR / 合并前，对产出代码做架构与安全审查
      │
      ▼
quick-pipeline-observability      ← 只读扫描上述产物 → docs/ai/metrics（可选末步）
```

> **关键约定**：每个 Skill 消费上游产物作为**唯一真源**，禁止跨 Skill 发明业务规则或接口字段。观测 skill **不改写**上游产物。

---

## IRON LAW（跨 Skill 通用）

1. **禁止发明** — 每条实现承诺、接口字段、错误码必须能对应到 REQ-xxx 或标注「工程补充」
2. **禁止覆盖** — PRD 变更或方案升版时，须新建版本文件，旧版保留可查
3. **禁止静默删除** — 未经用户明确确认，不得删除代码或旧文件
4. **追溯优先** — 需求 → 方案 → 代码 → 用例，全链路可回溯

---

## CLI Manifest 集成

Skill 本体目录只需 `SKILL.md`（及可选 `references/`）。与 quick-cli 集成时，在仓库根 [`manifests/skills/`](../manifests/skills/) 增加同名 manifest，并在 [`install-targets.json`](../install-targets.json) 登记 `sourceDir`。

- manifest 与 `SKILL.md` **分目录存放**，安装进项目时不会复制 manifest
- `name` 使用 `quick.<skill-name>` 命名空间
- `sourceDir` 指向本目录下的 skill 子目录
- `entry` 通常为 `SKILL.md`
- `inputs` 声明上游产物别名，例如 `prd`、`requirements_doc`、`solution_doc`
- `outputs` 声明真实产物文件路径，例如 `docs/ai/codegen/codegen-plan.v1.md`

全流程编排定义在仓库根目录的 `flows/*/flow.json`：

- `quick.vue-ai-full-flow`：Vue 模板默认流程
- `quick.ai-full-flow`：通用模板流程

注意：`flow.json` 的步骤 `outputs` 使用逻辑别名，不直接写文件路径；CLI 需要再映射到各 skill 的真实产物。

---

## 如何新增 Skill

1. 在本目录下新建子目录，命名以 `quick-` 开头，使用 `kebab-case`，力求见名知意
2. 子目录内包含 `SKILL.md`（主 Skill 文件）及可选的 `references/` 参考资料目录
3. 在本文件的「Skill 全景」表格与「Skill 协作关系」图中补充对应条目
