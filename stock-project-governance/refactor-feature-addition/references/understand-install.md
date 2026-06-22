# understand-anything 安装与就绪

## 何时加载

Step 0 检查项目根下 `.understand-anything/knowledge-graph.json` **不存在**时**必读**。

## 就绪检查

```bash
test -f .understand-anything/knowledge-graph.json && echo OK || echo MISSING
```

| 结果 | 动作 |
|------|------|
| `OK` | 读 `meta.json` → `lastAnalyzedAt`；若早于目标文件最近变更 → `/understand --update` |
| `MISSING` | 安装（若需要）后执行 `/understand` |

## 环境检测顺序

1. **Claude Code**（支持插件）：检查 `/plugin` 或 marketplace 是否已装 `understand-anything`
2. **Cursor**：检查项目或全局是否已配置 understand-anything（`.cursor/skills/`、`/understand` 命令可用、或已有 `.understand-anything/`）
3. **均无** → 走下方安装或降级

## 安装（Claude Code / 支持插件的环境）

```bash
/plugin marketplace add Lum1104/Understand-Anything
/plugin install understand-anything
```

首次 `/understand` 需 **Node.js ≥ 22**、**pnpm ≥ 10**（插件会构建 `@understand-anything/core`）。

## Cursor 环境

- 若团队已在 Cursor 配置 understand-anything：直接 `/understand`
- 若未配置：优先请用户安装插件或提供已有 `.understand-anything/` 目录
- 无法安装时走**降级**（见下）

## 无插件环境（降级）

1. 说明无法自动建图，请用户安装 understand-anything 或提供已有 `.understand-anything/`
2. 在《技术方案》范围卡片标注 **「图谱来源：手工 Read + 静态分析」**
3. 调用链每条边须附 **文件:符号** 证据；**禁止**无证据编造 node id
4. 仍须完成理解、落盘与验证步骤

## 常用命令

| 命令 | 用途 |
|------|------|
| `/understand` | 建图 → `.understand-anything/knowledge-graph.json` |
| `/understand --update` | 增量刷新（合入后**必须**） |
| `/understand --full` | 强制全量重建 |
| `/understand-chat "<描述>"` | 图谱问答；结果仍须落盘 |
| `/understand-domain` | 业务域图谱（辅助 QA 功能点命名） |

## 禁止

- 无图谱且无手工证据时伪造 `function:...` node id
- 安装/建图失败仍跳过 Step 0 进入实现
