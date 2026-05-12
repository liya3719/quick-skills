# Design Token JSON（设计稿真源）

加载时机：**步骤 2** 开始解析样式、主题或任何与颜色/字体/间距/圆角相关的实现前。

## 定位

本仓库约定：**界面相关视觉规格以团队提供的 design token **JSON** 为真源**，不以截图估算为主。模型必须读取实际 JSON 内容（或用户粘贴片段），建立到代码的映射。

## 支持的常见形态（其一即可）

团队可选用以下任一类约定；若与用户说明不一致，**以用户本次提供的格式说明为准**。

1. **W3C Design Tokens Format**（`$type` / `$value` / `$extensions`）
2. **Style Dictionary** 源 JSON / 平台输出前的中间表示
3. **Figma Variables / Tokens Studio 等导出 JSON**（常为嵌套对象 + `value`、`type`）
4. **自研 schema**：须在对话中说明顶层键名（如 `color`、`spacing`、`font`）与引用语法

## 解析规则

1. **区分 token 与字面量**  
   - 若值为引用（如 `{color.primary}`、`{some.alias}`），**必须**沿引用链解析到最终字面量或标为 OPEN（断链）。  
   - 禁止未解析引用就直接写死近似色值冒充「来自 token」。

2. **语义命名优先于数值**  
   - 代码侧优先使用与设计侧一致的语义名（如 `color.text.primary`）映射到变量；避免在组件内散落 `#rrggbb`。

3. **多主题 / 暗色**  
   - 若 JSON 含多套主题或 `mode`：实现时与 REQ/方案一致；若文档未指定用哪套，**STOP → 确认或 OPEN**。

4. **与 REQ 冲突时**  
   - **REQ 与方案优先于纯视觉**（例如无障碍对比度、必填校验样式若方案有明确规定）。  
   - 若 token 导致与 REQ 明显矛盾：列出冲突点，不私自改业务规则。

5. **缺失 token**  
   - 某布局在稿面需要但 JSON 无对应项：记 **OPEN-xxx**，可用临时常量但须在交付说明中列出「待设计补 token」与占位名。

## 到代码的落点

**不要在此篇展开框架细节。** 由 `SKILL.md` 的「渐进加载表」选择：`tailwind-design-tokens.md`、`scss-less-tokens.md`、`vue3-ui-tokens.md`、`react-ui-tokens.md`、`typescript-ui.md`、`javascript-ui.md`。

共性：单一映射出口（`:root` / theme 对象 / 预处理器变量），组件只消费语义名。

## 自检

- [ ] 本功能用到的色、字重、字号、间距、圆角、阴影均能追溯到 JSON 中的路径或别名链  
- [ ] 交付说明里写了本次使用的 **token 文件标识**（路径、commit、或导出日期）
