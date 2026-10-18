# 视频模型拼贴参考

## 用途

当项目的复杂 scene 需要交给 `doubao-seedance-1-5-pro-251215` 这类视频模型时，使用这份参考统一。模型 ID 区分大小写，禁止写成大写 `Pro`：

- 整体拼贴审美
- 旁白驱动的 editorial 结构
- 关键帧应该长什么样
- 视频模型该如何“动”这张拼贴画

这份文件综合了以下两类来源，但其棕灰犯罪纪录片配色不再作为默认风格：

- `Crime Documentary Paper Engine` 的脚本、beat、图像 prompt、通用视频 prompt、thumbnail DNA
- `VOX ANIMATIONS.txt` 里的分阶段创作引擎和 documentary editorial collage 语言

它不是让我们照搬 crime niche，而是把其中真正可迁移的 production grammar 抽出来，服务于任何 paper collage explainer。所有项目先执行 `0720-bright-paper-style.md`；只有用户明确要求档案、犯罪或去饱和配色并记录 `user_palette_override=true` 时，才允许使用本文件中的旧档案材质词。

## 总体方向

视频模型路线的目标不是做“电影感镜头”，而是做：

- 一张已经设计完成的 editorial 拼贴画面
- 由纸片、标签、地图、图章、线条、照片剪贴组成
- 在镜头锁定或几乎锁定的前提下，自行装配、落位、停驻
- 最后停成一张会呼吸的 living poster

可以把它理解为：

- `Vox` 的信息组织
- `Fern` 式纪录片旁白节奏
- 明亮手工纸艺、编辑型信息图和必要时的档案拼贴材质语言

## 核心视觉语言

### 材质

- bright fibrous, watercolor, printed, corrugated, and halftone paper
- broad chromatic paper fields
- crisp rough-cut or torn edges
- thin fibrous white separators around focal cutouts
- archival paper, old maps, tape, stamps, string, and pins only when the content requires them

### 配色

- 默认采用 `0720-bright-paper`：一个有彩主场、至少两个有彩辅助色、一个冷暖焦点色、一个深色锚点和少量纸张中性色
- 安静背景通过降低细节和边缘密度实现，不通过去饱和实现
- 米白只用于纤维、撕边、云、泡沫、标签和负空间
- tan、brown、gray 与档案桌面色默认合计不超过 20%
- 去饱和 tan/off-white/gray/ink-black 配色只属于用户明确批准的档案例外

### 构图法则

- 每个 beat 或每张关键帧，尽量只有一个主视觉
- 主元素约占 70% 视觉重心
- 辅助元素最多 2-3 个
- 留出负空间
- 不为“好看”而堆叠碎屑，所有胶带、印章、标签都必须服务叙事

### 文字法则

- 默认不加字
- 只有日期、姓名、金额、地点、年份这类信息必须可视化时，才允许一个短标签
- 单个标签最多 1-4 个词
- 避免长句文字直接进图

### 连续性法则

如果一个人物、地点、道具跨多个 beat 重复出现：

- 外观描述保持一致
- 服装、姿态、轮廓、标志性道具不要每帧乱变
- 让整支片子看起来像同一个世界，而不是一堆彼此无关的图

## 适合视频模型路线的 scene

优先切到 `seedance-first-last` 的情况：

- 元素很多，且要同时动
- 画面是一个完整的大拼贴 tableau，不适合拆成前中后景独立 rig
- 运动是“整体画面中的多个局部联动”
- scene 更像“证据墙”“新闻封面场”“地图追踪场”“档案桌面场”

典型类型：

- conspiracy evidence board
- clean evidence wall
- document forensics desk
- archival timeline
- annotated data viz
- mixed-media data collage
- chromatic editorial paper tableau
- Vox mixed-media editorial poster scene

## 可复用风格家族

从 PDF 第 7 页那张 `VOX VISUAL STYLES` 表里，最适合我们当前 skill 的，不是所有卡片，而是这几类：

- `cutout collage`
  适合人物、物件、象征性 subject
- `mixed-media data collage`
  适合“人物 + 图表 + 走势”混合信息 scene
- `annotated data viz`
  适合红线、圈注、解释型图表
- `archival timeline`
  适合年份跳跃、事件推进、before/after
- `conspiracy evidence board`
  适合证据关系、线索串联、调查感
- `clean evidence wall`
  适合极简证据展示，负空间更强
- `document forensics`
  适合文本、档案、页眉、批注、highlight
- `bright layered paper tableau`
  适合信息密度较高但仍保持清晰色彩层级的 editorial 拼贴
- `Vox mixed-media editorial`
  适合整个项目的总 aesthetic，尤其适合 thumbnail 和 hero scene

这些不是要逐张模仿，而是告诉我们：复杂 scene 应优先落在“明亮纸艺、数据、地图、比较、路径、必要时的档案证据”这组视觉家族里，而不是跑去 cinematic concept art 或统一棕灰的犯罪纪录片模板。

## 视频模型镜头规则

### 默认镜头语法

- 镜头锁定
- 不推拉摇移
- 不重新构图
- 不中途变焦
- 不切镜
- 不替换对象
- 不让元素 morph

如果没有明确理由，不要把视频模型当作 cinematic camera tool。

### 默认时间结构

一个 8-10 秒的拼贴视频，优先按这个逻辑组织：

1. `0-70%`：build-on assembly
2. `70-100%`：living poster hold

也就是：

- 先从空背景或少量基础底板开始
- 元素按叙事顺序，从后到前进场
- 到后半段时，画面已经长成最终 last frame
- 最后只保留很轻的生命感

当 `first-frame` 明确要保持空镜或近空镜时，不要只写“从空画面装配到最终画面”。
还要同时锁死：

- 唯一允许进场的前景物件白名单
- 明确禁止的替代物和额外碎片
- 每个前景物件都是 `rigid flat paper cutout`
- 物件保持与尾帧一致的轮廓家族和近似最终比例
- 明确的串行进场顺序

否则模型很容易在中段发明“语义相关但风格不对”的过渡元素，比如奶瓶、鸡蛋、购物袋、漂浮纸卡。

关键帧本身也必须锁死：先生成唯一的 `first-frame.png` 背景母版，再以该文件作为内置 `image_gen` 编辑模式的唯一 `referenced_image_paths` 输入，只在声明的 `change_regions` 内增加尾帧元素。不得分别文生图首尾帧，也不得把 “same background” 当成图生图的替代品。

### 进场动作

允许的动作更像真实纸片被摆上去：

- slide in with paper drag
- stamp settle
- tape press
- pin drop
- string draw
- underline draw-on
- label slide-in

每个元素落位后，原则上就不要大幅乱动。

当 scene 中有少量但关键的道具时，优先写成“刚性对象编排”而不是“主题联想”：

- 不要写 `grocery elements`
- 改写成 `one flat milk carton cutout`
- 不要写 `fuel symbol`
- 改写成 `one flat gas nozzle cutout`
- 不要写 `rent paperwork`
- 改写成 `one flat rent invoice slip`

对视频模型来说，`grocery` 是语义域，不是稳定物件。只写语义域，就等于把中段过渡形态交给模型自由发挥。

### 停驻阶段

最后停驻时，只保留非常轻的微动作：

- 纸角轻微翘动
- 阴影轻微呼吸
- halftone 轻微闪动
- string tension 微颤
- 印章墨迹轻微发亮

不能出现：

- 位置大改
- 元素缩放
- 大幅旋转
- 新元素继续进场

如果 scene 已经出现过一次“中段发明额外物件”的漂移，下次重试时优先这样收紧：

- 保持空首帧不变
- 增加 `allowed objects`
- 增加 `forbidden objects`
- 明确禁止 `morphing`、`substitution`、`detached fragments`
- 让 hero object 先落位，再让 supporting objects 近最终尺寸进场

如果首帧已经包含坐标轴、地图、卡片、表格或证据板底面，把它列为 fixed object，不得在 prompt 里再次要求它进场。曲线、路线、红线和下划线必须作为附着在 fixed surface 上的 draw-on path：只允许笔尖沿指定方向增长，已绘制部分保留，不得整卡替换、翻页显现、离开所属区域或变形成另一条线。完整字段和数据图示例见 `seedance-motion-contract.md`。

## 推荐的声音观

如果视频模型输出带音频，默认倾向：

- 无旁白
- 无音乐
- 只有纸张 ASMR 和轻环境音

如：

- paper slide
- cardstock tap
- tape press
- stamp thud
- pin click
- room tone

旁白与音乐更适合后期独立叠加。

## 与现有 skill 的关系

这份参考补充的是“视频模型优先”的 scene 语法，不替代现有文档：

- 分层代码与可编辑 motion：继续看 `remotion-build.md`
- 多 scene editorial 组织：继续看 `vox-broll-sequence.md`
- 基础材质和纸艺规则：继续看 `style-guide.md`

如果 scene 简单，还是优先 `Remotion cutout`。
如果 scene 复杂，再用这里这套视频模型 grammar。

## 从原始内容里提取什么

参考前面那两份文案时，真正值得保留的不是 crime 题材本身，而是这套提取顺序：

1. 先抓一个可以冷开场的具体时刻
2. 再抓一个可以被“看见”的主动作
3. 再决定主视觉对象是谁
4. 再决定这个信息更像 cutout 组装，还是更像一整张会动的拼贴海报

换成当前 skill 的字段，就是：

```yaml
hook_moment:
  date:
  place:
  action:
scene_goal:
hero_subject:
supporting_subjects:
fixed_background_logic:
assembly_order:
final_hold_message:
route_hint:
```

如果这几个字段提不出来，说明原始内容还太松，不能直接进视频生成。

## 内容提取示例

### 原始需求

```text
做一个拼贴画风格 scene，讲劫机者拿到赎金和降落伞后消失，最后警方只剩下一堆互相对不上的线索。画面想要像证据板和地图调查墙。
```

### 提取结果

```yaml
hook_moment:
  date: November 24, 1971
  place: Pacific Northwest air route
  action: the man disappears after the jump
scene_goal: turn the disappearance into a final evidence-board tableau
hero_subject: hijacker note pinned near center
supporting_subjects:
  - cash bundles
  - parachute evidence card
  - regional map with red string path
fixed_background_logic:
  - corkboard
  - archival map scraps
  - date strip
assembly_order:
  - note
  - cash
  - parachute card
  - string
  - pins and stamps
final_hold_message: the case ends on the missing parachute
route_hint: seedance-first-last
```

## 从故事到首尾帧的优化示例

### 不够好的写法

```text
一个很复杂的证据墙，很多线索飞进来，最后形成一个调查结果。
```

这个写法的问题：

- 没说谁是主元素
- 没说哪些背景从头到尾固定
- 没说最终停驻的信息点
- 容易让模型乱加元素、乱改构图

### 更适合首尾帧路线的写法

```yaml
first_frame:
  generation_mode: imagegen-generate
  purpose: reserve a readable empty center for evidence assembly
  include:
    - corkboard background
    - archival map scraps already pinned down
    - date strip in upper left
    - two empty tape corners for future photos
  exclude:
    - hijacker note
    - cash
    - parachute evidence card
    - red string

last_frame:
  generation_mode: imagegen-edit
  edit_target: exact first-frame.png bytes
  referenced_image_paths: [first-frame.png]
  preserve_outside_change_regions: true
  purpose: resolve into a finished Vox editorial tableau
  include:
    - hijacker note at center
    - cash bundles lower left
    - parachute evidence card right side
    - red string across map
    - two brass pins and one red stamp accent
  hold_message:
    - the missing parachute remains the unanswered clue
```

这就是视频模型更容易理解的 scene 结构，因为它知道从哪开始、往哪结束、哪些元素不能乱变。

## 图片提示词示例

### 首帧示例

```text
Create a full-frame Vox-style editorial mixed-media empty plate for a Seedance first+last scene. This is the one background master that will later be edited.

Scene goal:
an evidence-board scene about a hijacker who vanished after a ransom jump

This specific still moment:
first-frame empty plate

Hero subject:
none yet; leave the center area open for evidence assembly

Supporting subjects:
- corkboard background with archival map scraps already pinned down
- a small date strip in the upper left reading NOV 24 1971
- two empty masking-tape photo corners

Background and surface logic:
aged corkboard, archival map paper, subtle newsprint scraps, visible pin holes

Composition rule:
clear center reserve, readable negative space, no clutter

Style:
Vox-style editorial mixed-media collage, rough white-bordered cutouts, flat bold color fields, halftone and paper grain, matte lighting, soft layered shadows, one restrained red accent, non-photorealistic, no live-action
```

### 尾帧示例

```text
Edit the provided first-frame image to create the final hold. The exact local first-frame file is the immutable edit target and the sole `referenced_image_paths` input.

Scene goal:
resolve the evidence-board scene into the final mystery tableau

This specific still moment:
last-frame final hold

Hero subject:
a black-and-white halftone ransom note pinned near center

Supporting subjects:
- bundled cash lower left
- one parachute evidence card on the right
- a Northwest map with a red string route

Change only:
- central evidence assembly zone: add the ransom note
- lower-left evidence zone: add the bundled cash
- right evidence zone: add the parachute card
- declared map-path zone: add the red string and pins

Background and surface logic:
preserve the exact corkboard and map pixels, crop, tape corners, paper tears, map contours, texture, grain, color, and lighting outside those declared regions

Composition rule:
the note remains dominant, the supporting evidence stays readable, and the frame already feels like a finished poster

Style:
Vox-style editorial mixed-media collage, rough white-bordered cutouts, flat color fields, restrained route lines and pins, short labels only when necessary, visible paper grain, halftone texture, matte lighting, soft layered shadows, non-photorealistic, no live-action

Hard invariant:
do not repaint, regenerate, restyle, recrop, move, extend, or simplify the background. Output the same first-frame canvas with only the approved additions.
```

## 视频提示词示例

```text
Transform the provided first-frame and last-frame images into a premium Vox-style editorial mixed-media animation.

Preserve the final composition of the provided last frame exactly. The first frame is the quiet background plate. The last frame is the completed evidence-board tableau.

Style:
Vox-style editorial mixed-media collage in motion, flat map fields, halftone cutouts with rough white borders, restrained marker route lines and pins, rigid paper-piece motion, soft layered shadows, snappy editorial cadence, non-photorealistic, no live-action

Camera:
locked camera, no pan, no zoom, no tilt, no cuts, no morphing, no object replacement

Timing structure:
0-70 percent assemble the board from back to front
70-100 percent hold as a living poster

Assembly behavior:
the note lands first and becomes the anchor, cash slides in next, the parachute card settles on the right, then the red string draws across the map and the pins lock it into place

Hold behavior:
all major objects stay fixed, only slight paper-corner lift, soft shadow breathing, and one tiny string quiver remain

Audio:
no narration baked in, only subtle paper slide, pin click, tape press, and room tone
```

## 脚本优化示例

### 原始口播

```text
他拿到钱和降落伞以后就跳下去了，后来大家一直在找他，但很多东西都对不上。
```

### 优化后的旁白

```text
That night, he left the plane with cash and four parachutes.
By morning, search teams had a map, a timeline, and almost no certainty.
The evidence kept growing.
The answer did not.
```

这个版本更适合拼贴视频模型路线，因为：

- 每句都能拆成单独视觉
- 节奏短，方便 2-3 秒一个 beat
- 最后一句天然适合做停驻钩子
- 能直接映射成“证据越来越多，但答案没有出现”的装配式画面
