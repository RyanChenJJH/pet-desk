# pet-forge & work_space 全局 Agent 协作规范与架构约束

> **重要说明**：本文档为本项目最高优先级全局规范。任何 AI Agent 在启动、分析或执行任务前，**必须完整阅读并严格遵守**本规范的所有条款。

---

## 1. 项目定位与生态架构

本工程致力于打造高品质桌面宠物动画并无缝对接桌面端运行时。三者职责划分如下：

1. **`pet-forge` (根级动画工坊)**：
   - 动画母版设计、骨骼绑定契约、动作节奏库与调参工具链。
   - 提供标准 conventions、routes、scripts 与预设体系。
2. **`work_space/` (个人专属定制动画开发区)**：
   - 每个独立角色拥有专属根目录（如 `R1_doraemon/`, `R2_clock/`）。
   - 承载角色的参考图、矢量母版、调参页面、导出产物及最终的主题发布包。
3. **`clawd-on-desk` (桌面宠物运行时)**：
   - 位于本地 `E:\Work2\AI_Work\tool\clawd-on-desk\clawd-on-desk`。
   - 通过 `theme.json` 与 `assets/` 目录加载并驱动桌宠状态机（包含光标跟随、漫步、多会话并发状态及拖拽反应）。

---

## 2. 全 SVG 路线核心技术硬约束（Iron Rules）

本项目所有交付动画资产必须严格遵循**全 SVG 路线**：

1. **自包含与纯净沙箱**：
   - **严禁 `<script>` 标签**：Clawd-on-desk 安全沙箱加载外部主题时会自动清洗并剔除所有脚本。
   - **严禁外部资源**：严禁引用外部 `<link>` 样式表、外部网络图片或自定义网络字体。
   - **内联样式**：所有动画逻辑必须完全使用自包含的 `<style>` 标签与 CSS `@keyframes` 编写。
2. **Clawd 光标跟随契约 (Eye-Tracking Rig)**：
   - 在启用了眼球跟随的状态（如 `idle-follow.svg`）中，必须保留以下 3 个标准元素 ID：
     - `#eyes-js`：接收光标移动偏转（通常 `maxOffset: 2~3px`）。
     - `#body-js`：接收轻微身体角度跟随倾斜。
     - `#shadow-js`：接收地面投影的缩放与平移拉伸。
   - 必须统一坐标系原点与变换基准点（`transform-origin`）。
3. **循环动画首尾关键帧 100% 闭环**：
   - 循环动画（如 `idle`, `roam`, `working`, `thinking`, `sleeping`）的 `@keyframes` `0%` 与 `100%` 关键帧的 `transform`、`opacity` 与几何属性必须严格一致，严禁任何瞬跳断层。
4. **漫步方向约定**：
   - 漫步动画（`roam.svg`）中的角色造型必须统一**面朝右侧 (Facing Right)**。Clawd-on-desk 向左巡逻时会在运行时自动进行水平镜像翻转。

### 2.1 桌宠标准固定尺寸规范（Fixed Size Baseline）
为保证所有角色在桌面端具有统一、舒适的视觉比例，避免“过大遮挡屏幕”或“过小细节丢失”，全局严格约定以下**固定尺寸基线**：

1. **统一画布视口（Canvas ViewBox）**：
   - 采用标准居中视口：`viewBox="-25 -25 50 50"` 或 `-20 -25 50 50"`（统一逻辑空间 50×50，脚底接触线 `baselineY = 18`）。
2. **可视包围盒尺寸（contentBox）**：
   - 角色主体可视宽度：`width: 22 ~ 26`（占视口 44%~52%）。
   - 角色主体可视高度：`height: 24 ~ 28`（占视口 48%~56%）。
3. **桌面窗口占比硬性红线（visibleHeightRatio）**：
   - **固定标准区间：`0.38 ~ 0.44`**（严禁超过 `0.48`，默认基准推荐 `0.40 ~ 0.42`）。
   - `visibleHeightRatio` 过大（如 >0.50）会导致桌面宠物异常庞大遮挡用户工作区。
   - `baselineBottomRatio: 0.05`（确保角色稳定贴合在窗口底部）。

### 2.2 深度依托 `pet-forge` 开源项目进行设计与开发
本项目动画设计与工程实现**必须深度依托并严格遵守 `pet-forge` 开源项目**（位于 `pet-forge/`）：
1. **约定体系（Conventions）**：
   - 遵循 `source-to-animation-master.md`：必须忠实提取原图特征，严禁凭空脱离参考图臆造矢量结构。概念图定义“角色是谁”，初始母版解决“像不像”，分层母版解决“能不能动”。
   - 遵循 `layered-master.md`：必须建立分层矢量母版，母版是唯一真实源（Single Source of Truth），所有状态动画均派生自母版。
   - 遵循 `head-motion-axis.md`、`body-motion-axis.md`、`limb-rig-points.md` 与 `expression-mouth-system.md` 等关节骨骼与表情轴心规范。
   - 遵循 `loop-states.md` 与 `validation-runbook.md` 闭环与验证规范。
2. **工具链与模板（Tools & Templates）**：
   - 充分参考与利用 `routes/svg/templates/hello-idle.svg.html` 调参沙盒架构。
   - 充分利用 `routes/svg/tools/png2svg/` 矢量提取逻辑与预设风格定义。

---

## 3. 文档命名与版本生命周期规范

为保证多角色长期演进的高效可维护性，方案与计划必须统一遵循以下命名与存储规则：

1. **动画代号以 `R` 开头**：
   - 每个独立动画角色拥有唯一的大写代号（例如：`R1` 代表机器猫，`R2` 代表闹钟机器人，后续新角色依序递增 `R3`, `R4`...）。
   - 角色阶段与版本递增表示为 `R{角色编号}.{版本号}`（例如 `R1.0`, `R1.1`, `R2.0`, `R2.1`）。
2. **统一中文命名与分类**：
   - **设计与技术方案**：`docs/R{角色编号}.{版本号}_{角色中文名}_设计与技术方案.md`
     - 示例：`docs/R2.0_闹钟机器人_设计与技术方案.md`
   - **实施执行计划**：`docs/R{角色编号}.{版本号}_{角色中文名}_实施执行计划.md`
     - 示例：`docs/R2.0_闹钟机器人_实施执行计划.md`
3. **统一存储目录**：
   - 所有动画方案与计划统一存放在 `work_space/docs/` 目录下，严禁随意散落在角色工作目录或根目录中。

---

## 4. 文档头部需求与背景回溯标准

为确保项目历史清晰、需求不丢失，**每个方案（Scheme）和计划（Plan）的文档头部必须包含完整的追溯信息**：

```markdown
# [角色名称] R{编号}.{版本} [方案/计划名称]

> **原始需求与背景回溯**：
> - 提出时间：[YYYY-MM-DD]
> - 业务场景：[记录用户的原始需求、意图与核心诉求描述，做到一字不漏可回溯]
> - 已拍板技术决策：[记录用户已确认的美学风格、拓扑结构、技术路线、状态范围等关键结论]
> - 对接运行时：Clawd-on-Desk (`theme.json` Schema v1)
> - 交付目标：`work_space/R{编号}_{角色拼音}/`
```

---

## 5. 角色工作目录标准架构与 Theme 结构规范

### 5.1 五级工程流水线
在 `work_space` 下，每个独立角色的专属目录结构必须严格对齐 5 级流水线：

```text
work_space/
├── docs/                                      # 全局方案与计划归档库（中文命名）
│   ├── R1.0-doraemon-scheme.md
│   ├── R2.0_闹钟机器人_设计与技术方案.md
│   └── R2.0_闹钟机器人_实施执行计划.md
│
├── cloudling/                                 # 【标准 Theme 示例库】
│   ├── theme.json                             # 标准根配置文件 (无 BOM UTF-8)
│   └── assets/                                # 纯净动画素材子目录
│
├── R2_clock/                                  # 角色工程目录（R{编号}_{角色英文/拼音}）
│   ├── 00_reference/                          # 参考素材、调色板、透明去底 PNG
│   ├── 01_master/                             # 分层矢量母版（如 clock-master.svg，无动画静态基准）
│   ├── 02_forge/                              # 调参沙盒、单文件预览页面、关键帧调优
│   ├── 03_export/                             # 导出的标准自包含 SVG 产物归档
│   ├── theme/                                 # 对标 cloudling 的运行时主题包
│   │   ├── theme.json                         # 主题配置文件（纯 UTF-8 无 BOM）
│   │   └── assets/                            # 交付给 Clawd 的最终 .svg 动画资产
│   ├── clock-robot.zip                        # 一键生成的纯净无 BOM 主题压缩包
│   └── install-to-clawd.ps1                   # 一键同步安装到 Clawd-on-desk 的脚本
```

### 5.2 Theme 目录硬性契约（严格对标 `cloudling` 示例）
每个角色工程下的 `theme/` 目录必须严格遵守以下目录与编码规约：

1. **结构组织契约**：
   - `theme/` 根目录下**必须且仅直接包含**：
     - `theme.json`（核心元数据与状态机映射表）
     - `assets/` 文件夹（存放该角色所有引用的 SVG 动画资产）
   - **严禁多层嵌套**：严禁在 `theme/` 下建立多余的包装子目录（如 `theme/my-pet/theme.json`）。
   - **严禁素材外溢**：所有 `.svg` 文件必须统一收敛在 `assets/` 目录内，严禁直接散落在 `theme/` 根目录下。

2. **`theme.json` 编码硬约束（防崩溃红线）**：
   - **绝对禁止 UTF-8 BOM**：`theme.json` 必须保存为 **无 BOM 的纯 UTF-8 编码 (UTF-8 without BOM)**！若存在 `0xEF 0xBB 0xBF` 字节序标记，Clawd-on-desk 的 Node.js / Electron 导入解包时 `JSON.parse` 会直接抛出：
     `invalid theme.json: Unexpected token '', "{\ "sche"... is not valid JSON`
   - 在使用 PowerShell 或任何脚本生成/处理 `theme.json` 时，必须确保以无 BOM 方式写入或执行 BOM 自动剥离。

3. **状态机 Fallback 契约**：
   - `states` 中，`fallbackTo` 属性**仅允许在以下 7 个特定状态使用**：
     `error`, `attention`, `notification`, `sweeping`, `carrying`, `sleeping`, `roam`
   - 对于 `waking` 等其它状态，**严禁声明 `fallbackTo`**；若未绘制专属动画，应直接省略该状态（系统将默认平滑降级至 `idle`）或直接指定已有文件数组（如 `["idle-follow.svg"]`）。

4. **主题导入包 (.zip) 规范**：
   - 制作 `.zip` 导入包时，压缩包内部结构应与 `cloudling` 保持一致，即解压后顶层直接为 `theme.json` 与 `assets/`（或仅含一层以主题 ID 命名的单级文件夹），严禁将整个外部工程代码一并打包。

---

## 6. AI Agent 工作流程契约

每次响应用户关于桌宠制作或新动画的需求时，Agent 必须遵循以下阶段门禁：

1. **第 1 阶段：提问与对齐**：向用户发起明确提问，挖掘角色拓扑、艺术风格、状态需求。严禁在未经用户明确拍板前私自编写代码或创建资产。
2. **第 2 阶段：专家级推荐与拍板**：给出专业建议与方案选项（包含造型、动效节奏、状态机拆解），由用户决策确认。
3. **第 3 阶段：方案与计划文档编制**：在 `work_space/docs/` 下编写带完整需求回溯的中文命名技术方案与执行计划。
4. **第 4 阶段：严谨实施与交付**：严格按照计划通过 TDD 与无占位符原则逐步推进母版绘制、动画调试、主题打包与安装脚本编写。
5. **第 5 阶段：自动提交与远程推送（Git Discipline）**：开发实施及自动化校验完成后，Agent 必须自动将 `work_space` 下的所有变更提交并推送到远端仓库 `https://github.com/RyanChenJJH/pet-desk.git`，严禁遗漏。

---

## 7. Git 远端版本库与自动同步纪律（Git Discipline）

为确保 `work_space/` 下所有角色动画、母版、方案与执行计划的云端备份与版本安全追溯，必须严格遵守以下 Git 自动化纪律：

1. **托管范围与远端仓库绑定**：
   - 托管根目录：`work_space/`（该目录自身作为独立 Git 仓库根）。
   - 远端仓库地址：`https://github.com/RyanChenJJH/pet-desk.git`。
   - 默认主分支：`main`。
2. **每次开发完毕自动提交与推送（Auto-Commit & Auto-Push）**：
   - **硬性红线**：每次 AI Agent 完成任意功能开发、新角色动画制作（如 R1、R2、R3...）、Bug 修复、主题配置修改或文档编制后，**必须在任务结束前自动完成 Git 提交流程并推送到远端**，严禁遗漏：
     ```bash
     git add .
     git commit -m "<标准语义化提交信息>"
     git push origin main
     ```
   - **提交信息语义化规范**：
     - 新角色交付：`feat(R{编号}): 完成 {角色中文名} R{版本} 动画母版、主题制作与运行时部署`
     - 动效迭代优化：`fix/refactor(R{编号}): 优化 {角色中文名} {状态名} 关键帧动效节奏`
     - 规范与文档：`docs: 完善 {文档名称或规则说明}`
3. **推送冲突防范与重试**：
   - 推送前如遇远端有更新，应使用 `git pull --rebase origin main` 保证线性提交历史，成功后推送到远端并明确向用户汇报 Git 提交与推送结果。
