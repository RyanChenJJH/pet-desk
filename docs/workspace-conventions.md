# work_space 多动画与桌面宠物管理规范

> 本文档定义在 `work_space` 目录下创建、制作、存储个人定制桌宠动画的标准目录结构与通用工作流。后续创建其他角色（如皮卡丘、蜡笔小新、自定义吉祥物等）时，统一沿用此规范。

---

## 1. 目录架构规范

在 `work_space` 根目录下，每个独立角色均拥有一个以英文字符命名的专有文件夹：

```text
work_space/
├── docs/                                  # 【全局文档库】存储各角色的设计方案、执行计划与全局规范
│   ├── workspace-conventions.md           # 本规范文件
│   ├── R1-doraemon-scheme.md              # 机器猫 R1 设计与技术方案
│   ├── R1-doraemon-plan.md                # 机器猫 R1 实施执行计划
│   ├── R2-doraemon-scheme.md              # 机器猫 R2 高级交互与道具方案
│   └── R2-doraemon-plan.md                # 机器猫 R2 实施执行计划
│
├── doraemon/                              # 【机器猫】专属工程目录
│   ├── 00_reference/                      # 原始参考图、配色板、透明PNG素材
│   ├── 01_master/                         # 分层矢量母版 (SVG Master / Library)
│   ├── 02_forge/                          # 制作过程页面、参数调试工具、单文件预览
│   ├── 03_export/                         # 导出产物归档 (符合规范的静态或动画产物)
│   ├── theme/                             # 【Clawd-on-desk 主题包】
│   │   ├── theme.json                     # 主题配置文件
│   │   └── assets/                        # 最终交付的动画文件 (.svg / .gif / .apng)
│   └── install-to-clawd.ps1               # 一键同步安装到 Clawd 本地用户主题目录的脚本
│
└── <next_character>/                      # 【新角色目录：如 pikachu, shinchan 等】完全复用上述结构
```

---

## 2. 子目录职责划分

| 目录名 | 职责与内容要求 |
|---|---|
| `00_reference/` | 存放角色的第一手视觉素材，包含官方立绘、表情参考、配色表、去背景后的高精透明 PNG。严禁将带杂乱背景或棋盘格的截图作为矢量化输入。 |
| `01_master/` | 存放**分层矢量母版**（如 `doraemon-master.svg`）与零件库（如 `gadgets-library.svg`）。母版负责锁定角色识别锚点、统一坐标系（如 `viewBox="-20 -25 50 50"`）、提供标准的部件 ID 契约。母版不包含具体动画关键帧，确保后续制作各动作时部件造型高度一致。 |
| `02_forge/` | 动画制作过程沙盒。存放 `.svg.html` 调参页、HTML 预览对比页。此处的调试文件可以包含调试脚本与控制面板，但交付文件必须沉淀回纯净自包含文件。 |
| `03_export/` | 交付前归档。存放锁定的原始纯净 SVG/APNG 产物。 |
| `theme/` | **对标 Clawd-on-desk 运行时**的主题根目录。直接包含 `theme.json` 与 `assets/` 目录，可直接被 Clawd 加载或打包发布。 |

---

## 3. 技术契约与硬性规则

1. **自包含与安全沙箱**：
   - 外部主题由 Clawd-on-desk 的沙箱加载，SVG 内的 `<script>` 标签会被清理剥离。
   - 所有动画逻辑必须完全使用内联 CSS `@keyframes` 编写，严禁依赖外链脚本、外部字体或外部图片。
2. **眼球光标跟随契约**：
   - 若在 `theme.json` 中开启 `eyeTracking: { enabled: true, states: ["idle"] }`，则 `idle` 状态引用的 SVG 文件必须暴露以下元素：
     - `#eyes-js`：接收光标移动产生的偏移（建议 `maxOffset: 2~3px`）。
     - `#body-js`：接收微幅身体倾斜偏移。
     - `#shadow-js`：接收投影拉伸变形。
3. **循环动画闭环**：
   - A 类循环状态（如 `idle`, `thinking`, `working`, `roam`），其 `@keyframes` 的 `0%` 与 `100%` 关键帧必须完全一致，严禁出现瞬跳断层。
4. **漫步方向约定**：
   - `roam.svg` 必须画风朝右（Facing Right）。Clawd-on-desk 运行时向左漫步时会自动进行水平镜像翻转。

---

## 4. 新角色开启指引（5 步走）

当未来需要创建新角色（例如 `pikachu`）时：
1. **建立目录**：复制目录结构模板创建 `work_space/pikachu/`。
2. **素材拓扑盘点**：在 `00_reference/` 放入参考图，按 `pet-forge` 规范盘点主体轮廓、眼睛、四肢与支撑关系。
3. **建立分层母版**：在 `01_master/` 绘制 `pikachu-master.svg`，定好坐标系与标准颜色。
4. **磨制 Hero 待机**：制作 `idle-follow.svg`，在浏览器持续观察 30 秒以上循环效果。
5. **扩展与装配**：制作核心动作，配置 `theme/theme.json` 并运行验证脚本 `validate-theme.js`。
