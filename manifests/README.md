# manifests — quick-cli 编排层（可选）

本目录存放 **与 quick-cli 集成** 所需的注册元数据，与 Skill 本体（各目录下的 `SKILL.md`）分离。

## 定位

| 层级 | 路径 | 用途 |
|------|------|------|
| Skill 本体 | `incremental-project-skills/*/SKILL.md`、`stock-project-governance/*/SKILL.md` | 可插拔 AI Skill，可直接复制到 `.cursor/skills` / `.claude/skills` 使用 |
| CLI 编排层 | 本目录 `skills/*.json` + 仓库根 `flows/` + `install-targets.json` | 供 [quick-cli](https://github.com/quick-env/quick-cli) 发现 skill、编排 flow、多平台安装 |

**不使用 quick-cli 时**：只需 Skill 目录与 `SKILL.md`，无需本目录。

**使用 quick-cli 时**：CLI 读取 `manifests/skills/*.json` 注册能力，安装时仍只复制 `SKILL.md` 与 `references/`，不会把 manifest 装进项目。

## skills/*.json 字段

| 字段 | 说明 |
|------|------|
| `name` | 全局 ID，命名空间 `quick.*` |
| `sourceDir` | Skill 本体相对仓库根的路径，与 `install-targets.json` 中 `skills.*.sourceDir` 一致 |
| `entry` | 相对 `sourceDir` 的入口，通常为 `SKILL.md` |
| `inputs` / `outputs` | flow 编排用的产物别名或真实路径 |
| `applicableTemplates` | 可选，限定适用脚手架模板 |

新增 Skill 时：先写 `SKILL.md`，再在本目录增加同名 manifest，并在 `install-targets.json` 中登记 `sourceDir` 与平台目录名。
