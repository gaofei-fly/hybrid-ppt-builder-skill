# Hybrid PPT Builder 重构过程报告

日期：2026-05-21

## 目标

本次重构目标是把 `imagegen` skill 中已经验证有效的工程化经验迁移到 `hybrid-ppt-builder`：

- 明确默认路径和 fallback 边界；
- 避免静默降级为低可编辑性 PPT；
- 把输入角色、任务模式、产物路径、审批门和验证动作写成可执行流程；
- 将详细提示词经验从主 `SKILL.md` 拆到引用文档；
- 增加一个可运行的 PPTX 包检查脚本，让“可编辑性”有最小结构证据。

## 子代理分工

子代理 A 负责学习 `imagegen` 的优秀经验。结论是：最值得迁移的不是图片提示词本身，而是“顶层模式、默认优先级、fallback 确认、输入角色标注、产物保存、验证闭环、最终报告”的完整控制策略。

子代理 B 负责梳理 `hybrid-ppt-builder` 现状。结论是：已安装版本比工作区版本更新，现有技能已有正式报告方向、背景/前景契约和 Gate 机制，但缺少硬模式边界、可执行验证脚本、工具能力边界、产物策略和同步后的引用模板。

## 重构前主要问题

1. Source of truth 不清：工作区 `SKILL.md` 落后于已安装技能版本。
2. 规则偏叙述：背景/前景原则多次出现，但没有足够清晰的顶层模式和降级规则。
3. Gate 机制不够完整：已有背景候选和样张确认，但缺少默认跳过条件、迭代规则和最终报告要求。
4. 可编辑性验证不够可执行：没有脚本支撑对象数量、媒体数量和原生文本检查。
5. 引用模板滞后：中文模板没有覆盖参考背景判定、稿件转 PPT、Gate 1/Gate 2、SVG 可编辑性和交付审查。
6. 工具边界不够硬：`python-pptx`、PowerPoint COM、LibreOffice、PPTX 包检查、`imagegen` 的能力范围没有明确分层。

## 迁移自 imagegen 的关键经验

- **顶层模式固定化**：新增默认可编辑 PPTX、源重建、稿件转 deck、参考视觉系统、背景资产、视觉草稿六种模式。
- **默认路径优先**：默认交付可编辑 PPTX，不默认交付整页图片或低编辑性方案。
- **fallback 必须显式**：不能静默降级为整页截图、不可编辑 SVG、截图式表格或无预览交付。
- **输入角色标注**：把 source deck、content manuscript、data source、background reference、style reference、brand asset、editable target 等角色写入流程。
- **产物路径策略**：明确最终 PPTX、预览图、联系表、背景资产、SVG 模块和临时文件的默认位置。
- **验证闭环量化**：新增 `scripts/inspect_pptx.py`，检查 slide count、16:9、native objects、pictures、graphic frames、charts、tables、native text runs 和启发式 warning。
- **报告格式固定**：最终必须报告路径、页数、任务 slug、模式、Gate 使用/跳过、可编辑性和验证方法。

## 文件变更

### `SKILL.md`

重写为更硬的执行规范，核心新增内容：

- `Top-level Modes and Rules`
- `Decision Tree`
- `Input Role Classification`
- `Approval and Iteration Rules`
- `SVG and Tool Capability Boundaries`
- `Output and Artifact Policy`
- 更具体的 validation/reporting 要求
- 新 reference map

### `references/prompting.md`

新增提示词和构建原则文档，覆盖：

- 工作 spec 结构；
- 稿件压缩原则；
- 正式报告视觉风格；
- 可编辑性不变量；
- 中文字体和预览检查；
- 用 `imagegen` 生成背景时的背景专用 prompt。

### `references/sample-prompts.md`

新增中文可复制模板，覆盖：

- 总控 prompt；
- 现有 PPT 重制；
- 稿件转正式汇报；
- 参考背景图判定；
- Gate 1 背景候选确认；
- Gate 2 视觉样张确认；
- SVG 可编辑性确认；
- 交付前审查。

### `references/prompt-templates.md`

保留兼容入口，同时更新旧模板，使其与新规则一致：

- 增加背景/前景契约；
- 增加 Gate 1/Gate 2；
- 增加原生文本检查；
- 增加任务模式和审批门报告要求。

### `scripts/inspect_pptx.py`

新增无外部依赖的 PPTX 包检查脚本。它用于补齐 PowerPoint 预览之外的结构证据，尤其适合检查是否存在“背景图 + 整页前景图”冒充可编辑内容的风险。

### `agents/openai.yaml`

更新 UI 描述和默认 prompt，使其反映新的“稳定背景 + 原生前景 + 预览导出 + 对象级验证”定位。

## 验证结果

已完成以下验证：

```text
python C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
结果：Skill is valid!
```

```text
python -m py_compile .\scripts\inspect_pptx.py
结果：通过
```

```text
python .\scripts\inspect_pptx.py --help
结果：帮助输出正常
```

使用 `python-pptx` 生成了一个临时 16:9 PPTX 样例，并执行：

```text
python .\scripts\inspect_pptx.py .\tmp\hybrid-ppt-builder\inspect-sample.pptx --expect-slides 1 --min-native-objects 2 --require-native-text
```

检查结果显示：

- Slides: 1
- 16:9: True
- Media files: 0
- native_objects: 2
- native_text_runs: 1
- warnings: 无

验证中发现 `python-pptx` 生成的 EMU 尺寸会有微小舍入误差，因此把 16:9 判断从严格整数相等改成容差判断，避免误报。

## 相比重构前的提升

重构前，技能已经知道“背景稳定、前景可编辑”的方向，但执行时仍容易出现自由发挥过大、低编辑性降级不明显、验证证据不足的问题。

重构后，技能具备了更完整的工程控制面：

- 有明确模式和 task slug；
- 有输入角色表；
- 有低编辑性降级拦截；
- 有 Gate 使用和跳过规则；
- 有产物路径策略；
- 有工具能力边界；
- 有结构化可编辑性检查脚本；
- 有同步后的中文模板和 prompt 原则；
- 有固定最终报告字段。

这使它从“会做正式报告 PPT 的经验文档”升级为“能约束另一个 Codex 稳定执行正式报告 PPT 工作流的技能”。
