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

## 安装（Claude Code / 支持插件的环境）

```bash
/plugin marketplace add Lum1104/Understand-Anything
/plugin install understand-anything
```

首次 `/understand` 需 **Node.js ≥ 22**、**pnpm ≥ 10**（插件会构建 `@understand-anything/core`）。

## 无插件环境（降级）

1. 说明无法自动建图，请用户安装 understand-anything 或提供已有 `.understand-anything/`
2. 在《技术方案》范围卡片标注 **「图谱来源：手工 Read + 静态分析」**
3. 调用链每条边须附 **文件:符号** 证据；**禁止**无证据编造 node id
4. 仍须完成理解、图谱、落盘与验证步骤

## 常用命令

| 命令 | 用途 |
|------|------|
| `/understand` | 建图 → `.understand-anything/knowledge-graph.json` |
| `/understand --update` | 增量刷新（重构合入后**必须**） |
| `/understand --full` | 强制全量重建 |
| `/understand-chat "<描述>"` | 图谱问答；结果仍须落盘 |
| `/understand-domain` | 业务域图谱（辅助 QA 功能点命名） |

## 禁止

- 无图谱且无手工证据时伪造 `function:...` node id
- 安装/建图失败仍跳过 Step 0 进入实现
