---
name: quick-arch-security-code-review
description: "面向架构、安全与性能的深度代码审查，默认中文输出。覆盖 SOLID 与分层边界、XSS 与 CORS 与 SQL 注入、身份认证与鉴权与越权、敏感信息与私钥进日志、不安全反序列化、竞态与 TOCTOU、错误处理与边界与空值、算法与 I/O 与热路径性能。死代码以统一可检索标注列出，须经研发明确确认后由本人或研发删除，审查方不擅自删线。触发：代码审查、code review、CR、PR 审查、合并前检查、走查、安全审计、渗透前自查、质量分析、查死代码、性能问题、架构合理性。Actions: review, audit, inspect, scan, 检查, 审计, 走读, 评审。"
argument-hint: "[--focus all|arch|security|quality|perf|dead-code] [--in-repo-annotate yes|no] 无参则全维度；annotate 表示是否在代码中加 DEAD 注释，须用户明确同意"
---

# 架构与安全代码审查

IRON LAW：**未**得用户或研发**明确确认**前，**不得**从仓库**删除**任何代码，**不得**将「死代码」物理移除；**不得**擅自向生产分支**推送**安全修复。审查产出以**报告与可选注释标注**为主。

Red Flags（出现则回到「确认范围与权限」再往下）：

- 准备用「应删未用」**直接**删 import/函数/文件
- 在无流量与业务上下文时，声称某分支「**绝对**不可达」
- 把**猜测**写成**已证实**的安全漏洞
- 用户**未**要求时**修改**远程/共享分支

---

## Workflow

```
架构与安全代码审查 进度:

- [ ] Step 0: 确认范围与模式 ⛔ BLOCKING
- [ ] Step 1: 通读范围与数据流
- [ ] Step 2: 架构与 SOLID → references/solid-architecture.md
- [ ] Step 3: 安全风险 → references/security-risks.md
- [ ] Step 4: 代码质量（错误/边界）→ references/code-quality.md
- [ ] Step 5: 性能 → references/performance.md
- [ ] Step 6: 死代码（疑似）与染色 → references/dead-code-marking.md
- [ ] Step 7: 按模板汇总 ⚠️ REQUIRED → references/review-output-template.md
- [ ] Step 8: 用户确认后行动（改代码/不改编译）⚠️ REQUIRED
```

**`$ARGUMENTS` / focus**：`--focus arch|security|quality|perf|dead-code` 时，**可跳过**非选中维度的长清单，但摘要中须注明「本次未覆盖：…」。`all` 或缺省为全维度。

---

## Step 0: 确认范围与模式 ⛔ BLOCKING

在读取代码前，向用户**确认**或从上下文**推断**并**复述**：

- **范围**：单文件、目录、diff、整 PR、或分支对比？
- **技术栈**（影响 XSS/SQL/反序列化/并发模型等检查项的权重）
- **是否在库中打「死代码」注释**（`--in-repo-annotate`）：**默认否**；**仅**在用户明确说「可改仓库加标注」时启用
- 若有「仅出意见/可改代码」偏好，**遵守**

---

## Step 1: 通读范围与数据流

问：**外部**输入从何处进入？**敏感**写操作、**钱/库存/权限**变更在何路径？  
用 3～6 句话概括数据流，再进各专项；避免一上来抠命名。

---

## Step 2: 架构与 SOLID

加载 `references/solid-architecture.md`，按**提问清单**在报告「架构」类下列出发现。  
**禁止**只写「违反 SRP」而无**可改**的拆分建议或**至少一个**具体问题（例如多职责证据）。

---

## Step 3: 安全风险

加载 `references/security-risks.md`。  
对 XSS/CORS/SQLi、鉴权与越权、日志与私钥、反序列化、竞态：**每类**至少**自问**表格中的**对应句**；有代码证据再写进报告，无证据进「需确认」。

---

## Step 4: 代码质量

加载 `references/code-quality.md`，覆盖**错误处理**与**边界**两类；区分「**风格**」与「**会崩/会错**」问题。

---

## Step 5: 性能

加载 `references/performance.md`。先标出**热路径/大数据量**再谈优化；**无**基准或复杂度对比时，严重度**上限 P2** 并标「需 profiling」。

---

## Step 6: 死代码（疑似）与「染色」

加载 `references/dead-code-marking.md`。

- 在报告中**单独**一节列「**疑似**死代码」，每条：**位置、依据、置信度（低/中/高）**。
- **仅**在用户允许 `--in-repo-annotate` 时，在**本地/分支**用文档中的**统一注释**标注；**不得**在未经确认时**删除**。
- 高置信度时仍写「须研发确认后删除」。

---

## Step 7: 汇总

加载 `references/review-output-template.md`，按**严重度**排序，**P0 安全**与**可立即越权/注入**最前。每条含：位置、类别、问题、**一条**可执行建议。

---

## Step 8: 用户确认后行动 ⚠️ REQUIRED

- **只读报告**：不修改文件。
- **需改代码**（如加 DEAD 注释、修漏洞）：**复述**将改哪些文件，**等待**用户明确「可以改」或「发 PR 草稿」再动手。
- **删代码**：**仅**在用户**逐条**或整段确认「可删」后执行，且**优先**由用户自行在版本库中删除。

---

## Anti-Patterns

- 以「未使用」为由**直接** `git rm` 或大片删除。
- 把 `eslint` 能报的**当**成深度架构结论。
- 不区分 **Back-end / 前端** 的安全模型，混用 CORS 与「接口鉴权」的叙述。
- 在报告中堆砌术语而无**file:line** 或**符号**位置。
- **自动**为「修复安全」在共享分支**强推**或覆盖他人提交。

---

## Pre-Delivery Checklist

- [ ] 已说明 scope 与本次 `--focus` 未覆盖的维度
- [ ] 每条**实质**问题含**位置**（`path:line` 或符号）
- [ ] 安全项区分「**已**从代码**证实**」与「**需**业务/运行确认」
- [ ] 无「建议重构」**单独**成条而无具体问题
- [ ] 死代码**未**在未经授权时删除；若打了注释，**未**用非统一标签
- [ ] 无占位 `TODO`/`FIXME` 在交付报告主体中冒充结论
- [ ] IRON LAW：无擅自删线与未授权的自动修复
