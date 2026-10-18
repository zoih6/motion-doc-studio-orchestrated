# 提示词模板

## 用途

这份文件提供四类提示词模板：

- beat 级图片 prompt
- Seedance 首尾帧图片 prompt
- 视频模型 prompt
- thumbnail prompt

这些模板服务于 `paper-collage-video` 的复杂 scene 路线，不要求逐字照抄，但建议保留其中的约束逻辑。

当前只支持 `vox-mixed-media`。以下所有模板都必须使用 Vox 编辑型 mixed-media 视觉语法。

所有模板默认执行 `0720-bright-paper-style.md`。除非用户明确锁定其他配色，必须先完成每场 `color_script`，再把其中的 `prompt_palette_sentence` 和全部 `negative_palette_terms` 逐字放进背景、元素和视频提示词。不要把“安静背景”翻译成全米黄、棕灰、低饱和或褪色怀旧。

## 从内容到提示词的最小流程

建议始终先做这一步，再写 prompt：

```yaml
raw_input: 用户给的一段故事 / 口播 / 需求
extract:
  scene_goal: 这个 scene 到底要说明什么
  hero_subject: 谁或什么占主要视觉重心
  supports: 最多 2-3 个辅助元素
  fixed_scaffold: 哪些背景结构从头到尾都不变
  motion_order: 谁先进场，谁后进场，谁一直锚定
  hold_state: 最后停在哪个信息点上
route:
  simple: remotion
  dense: seedance-first-last
```

不要一上来就把原文整段塞给模型。先抽成这几个字段，图像和视频结果会稳定很多。

## 1. Beat 图片 prompt 模板

### 目标

把一个 narration beat 转成一张自洽的 editorial collage still。

### 必守规则

- 一个主元素
- 最多 2-3 个辅助元素
- 保持负空间
- 默认不加字
- 只有日期、金额、人名、地点需要强调时，才加一个 1-4 词标签

### 模板

```text
Create a Vox-style editorial mixed-media paper collage for this beat:
[describe the beat's core idea, not the literal sentence]

Hero element:
[one dominant subject carrying most of the visual weight]

Supporting elements:
- [supporting element 1]
- [supporting element 2]
- [optional supporting element 3]

Background:
[one broad chromatic paper field plus one quiet structural band; use archival surfaces only when the content truly requires them]

Optional label:
[only if a date, number, place, or name truly matters, 1-4 words max]

Style:
Vox-style editorial mixed-media collage, bright tactile paper cutouts with rough fibrous white borders, broad chromatic color fields, crisp halftone and paper grain, hand-drawn marker annotations, abstract maps and data shapes, one controlled focal accent, clear warm-cool and light-dark separation, matte flat lighting, soft cutout shadows, non-photorealistic, no live-action

Palette lock:
[copy color_script.prompt_palette_sentence verbatim]

Negative palette:
[copy every color_script.negative_palette_terms phrase verbatim]

Rules:
every element must appear physically hand-cut and layered from real paper, with visible cutout edges, halftone print texture, and soft shadow separation between layers. The composition stays clean, minimal, and editorial with generous negative space. Not digital illustration, not cartoon, not 3D render, not glossy, no gradients, no clutter, no watermark, no logos, no text beyond the specified label. [Gate 1 aspect ratio and canvas], ultra-detailed.
```

### 示例

#### 输入 beat

```text
他把赎金和四个降落伞要到了手里。
```

#### 提取结果

```yaml
scene_goal: show the negotiation has become physical evidence
hero_subject: ransom note pinned over stacked cash
supports:
  - folded parachute pack
  - red-circled typed demand line
background: archival desk + clipped airline form
label: "$200,000"
```

#### 图片 prompt 示例

```text
Create a Vox-style editorial mixed-media paper collage for this beat:
the hijacker's demands become tangible evidence on an archival desk

Hero element:
a typed ransom note pinned over stacked bundles of cash

Supporting elements:
- one folded parachute pack placed to the side
- a red circled demand line on the note
- a clipped airline form peeking from below

Background:
a deep ocean-blue paper desk field with a limited warm-cork strip and faint sky-blue airline paperwork; archival brown remains below 20% of the frame

Optional label:
$200,000

Style:
Vox-style editorial mixed-media collage, bright tactile halftone cutouts with rough fibrous white borders, broad chromatic paper fields, crisp paper grain, marker annotations, marigold focal accent, deep navy anchor, matte flat lighting, soft layered shadows, non-photorealistic, no live-action

Palette lock:
deep ocean blue is the dominant field, sky blue and leaf green are support colors, marigold orange is the focal accent, and deep navy is the dark anchor

Negative palette:
no sepia wash, no all-beige palette, no muddy brown-gray cast, no desaturated vintage filter, no monochrome kraft-paper scene, no faded low-contrast look

Rules:
one dominant hero object, clean editorial composition, generous negative space, no decorative clutter, no extra text, not digital illustration, not 3D, [Gate 1 aspect ratio and canvas]
```

## 2. Seedance 首尾帧图片 prompt 模板

### 目标

先用 `imagegen` 生成一张首帧母版，再以该首帧为编辑目标生成尾帧，最后交给 Seedance。禁止分别文生图两张 still。

### 分工

- `first-frame`：使用 `generate`，生成空镜或近空镜，保留场景底板和全部固定结构
- `last-frame`：使用 `edit`，将首帧作为唯一 `referenced_image_paths` 输入，只添加最终停驻画面新增的元素

如果坚持使用真正的空首帧，不要只依赖尾帧去约束中段运动。还要补上：

- `allowed objects`
- `forbidden objects`
- `rigidity rule`
- `scale rule`
- `entry order`

否则模型很容易在中段发明“相关但不对”的过渡物。

### 首帧 generate 模板

```text
Create a full-frame Vox-style editorial mixed-media collage still for a Seedance first+last scene.

Scene goal:
[what the whole scene is trying to communicate]

This specific still moment:
first-frame empty plate

Hero subject:
[main subject]

Supporting subjects:
- [support 1]
- [support 2]
- [support 3 if truly needed]

Background and surface logic:
[one broad chromatic paper field plus a relevant map / evidence wall / desk / timeline structure; archival brown surfaces stay limited unless the user overrides the palette]

Composition rule:
the frame should already look like a finished editorial poster, with clear depth, readable silhouettes, and enough negative space to keep the scene legible.

Style:
Vox-style editorial mixed-media collage, bright tactile cut-paper with rough fibrous white borders, broad chromatic fields, crisp halftone and paper grain, restrained marker annotations and data shapes, one controlled focal accent, deep chromatic anchor, matte lighting, soft layered shadows, non-photorealistic, no live-action

Palette lock:
[copy color_script.prompt_palette_sentence verbatim]

Negative palette:
[copy every color_script.negative_palette_terms phrase verbatim]

Future edit rule:
this exact image will be the edit target for the last frame. Keep every fixed background surface complete and reserve the declared change regions for future additions.

Avoid:
overcrowding, cinematic perspective distortion, glossy lighting, smooth digital painting, 3D rendering, long text blocks, decorative clutter
```

### 尾帧 edit 模板

在调用内置 `image_gen` 前，先用 `view_image` 查看本地
`first-frame.png`，然后把该本地路径作为唯一
`referenced_image_paths`。使用编辑语义，不得调用空输入的生成语义。

```text
Edit the provided first-frame image. This image is the immutable background
master for a Seedance first+last scene.

Change only these approved regions:
- [region id, x/y/width/height percentages]: add [exact entering object]
- [region id, x/y/width/height percentages]: add [exact entering object]

Additions:
- [exact rigid foreground object 1]
- [exact rigid foreground object 2]
- [exact draw-on path or accent, if any]

Hard invariants outside the approved regions:
preserve the exact canvas, crop, camera, perspective, background geometry,
horizon, map or architecture contours, paper tears, edge positions, texture,
grain, color, lighting, and every fixed object. Do not repaint, restyle,
regenerate, extend, simplify, or move the background. Do not add decorative
scraps outside the approved regions.

Palette lock:
[copy color_script.prompt_palette_sentence verbatim]

Negative palette:
[copy every color_script.negative_palette_terms phrase verbatim]

Output:
the same first-frame canvas with only the approved foreground additions. No
background redesign, no recrop, no camera change, no global style transfer.
```

### 当首帧为空时，追加这段

```text
Allowed moving foreground objects only:
- [object 1]
- [object 2]
- [object 3]

Forbidden:
- [wrong substitute 1]
- [wrong substitute 2]
- [wrong substitute 3]
- any new prop not visible in the last frame
- detached floating label fragments
- extra paper scraps behaving like separate props

Rigidity rule:
every foreground prop must behave like one rigid flat paper cutout, preserving the same silhouette family and near-final scale as the last frame. No morphing, no substitution, no split-apart assembly.

Assembly order:
[object A] first, [object B] second, [object C] third, [labels/tags] last.
```

### `first-frame` 示例

```text
Edit the provided first-frame image to create the Seedance last-frame final hold. Use the exact local first-frame file as the sole edit target and reference input.

Scene goal:
an evidence-board scene that builds the mystery of a hijacker who vanished after a ransom jump

This specific still moment:
first-frame empty plate

Hero subject:
none yet; hold the central board space open for later assembly

Supporting subjects:
- a corkboard base with aged map scraps already pinned down
- two empty evidence-photo corners made from masking tape
- a faint typewriter date strip reading NOV 24 1971

Background and surface logic:
aged corkboard, archival map paper, scattered newsprint scraps, subtle pin holes

Composition rule:
the frame should already look like a clean finished background plate with a clear center area reserved for future evidence pieces

Style:
Vox-style editorial mixed-media collage, archival cutouts only where needed with rough white borders, broad flat color fields, restrained red marker accents, halftone and paper grain, matte lighting, soft layered shadows, non-photorealistic, no live-action

Continuity rule:
reserve the same map region and board layout that will remain in the last frame

Avoid:
overcrowding, glossy lighting, digital painting, long text blocks
```

### `last-frame` 示例

```text
Create a full-frame Vox-style editorial mixed-media collage still for a Seedance first+last scene.

Scene goal:
an evidence-board scene that resolves into the final mystery tableau

This specific still moment:
last-frame final hold

Hero subject:
a black-and-white halftone cutout of the hijacker note pinned near center

Supporting subjects:
- bundles of ransom cash
- one parachute pack card
- a small northwest map with a red string path

Change only:
- the central evidence cluster region reserved in the first frame
- the small northwest-map route region reserved in the first frame

Background and surface logic:
preserve the exact corkboard and archival map plate pixels, crop, tape positions, map contours, torn edges, and texture from the first frame outside those regions

Composition rule:
the frame should already look like a finished editorial poster, with the note as the visual anchor and the other pieces supporting it without clutter

Style:
Vox-style editorial mixed-media collage, rough white cutout borders, flat color zones, restrained red route lines and pins only when narratively required, halftone cutouts, visible paper grain, matte lighting, soft layered shadows, non-photorealistic, no live-action

Continuity rule:
do not redraw or reinterpret the board. Change only the approved regions and preserve all protected background pixels

Avoid:
new background redesign, cinematic perspective distortion, clutter, long text
```

## 3. 视频模型 prompt 模板

### 目标

让视频模型把关键帧当成最终完成画面，先装配，再停驻。

### 默认适用场景

- 证据板
- 地图追踪
- 档案桌面
- 报纸封面
- 混合数据拼贴
- 新闻拼贴 tableau

### 模板

```text
Transform the provided first-frame and last-frame images into a premium Vox-style editorial mixed-media animation.

Preserve the final composition of the provided last frame exactly. Do not redesign, replace, or substantially reposition elements. The first frame is the empty or near-empty starting plate. The last frame is the finished frame the animation builds toward.

Style:
Vox-style editorial mixed-media collage in motion, rough white-bordered cutouts, flat bold color fields, halftone and paper grain, marker sweeps and route-line draw-ons, rigid paper-piece motion, soft layered shadows, snappy editorial timing, subtle handcrafted settles, non-photorealistic, no live-action

Camera:
keep the camera locked unless explicitly instructed otherwise. No zoom, no pan, no tilt, no orbit, no handheld shake, no cuts, no morphing, no object replacement.

Timing structure:
0-70 percent: build-on assembly from back to front
70-100 percent: living poster hold

Assembly behavior:
start from the bare background plate or structural base with the main story elements absent. Let background scraps settle first, then the hero cutout, then supporting cutouts, then labels, tape, stamps, strings, and marker accents. Each piece lands with a tiny handcrafted settle and layered shadow.

Hold behavior:
once the final composition is reached, keep everything in place. Only allow subtle life such as slight paper-corner lift, faint shadow breathing, slight halftone shimmer, or one small string quiver.

Audio:
no narration baked in. Prefer subtle paper ASMR only: paper slide, cardstock tap, tape press, pin click, stamp thud, soft room tone.

Avoid:
CGI-smooth motion, big camera moves, clutter growth, late object swaps, dramatic reframing, heavy atmospheric effects, glossy render feel
```

### 视频 prompt 强化版

当首帧为空，而且你已经知道 scene 里哪些道具最容易被模型误解时，补上这种结构：

```text
Allowed moving foreground objects only:
- one flat [object 1] cutout
- one flat [object 2] cutout
- one flat [object 3] cutout
- [optional labels or price tags]

Forbidden:
- [common wrong substitute 1]
- [common wrong substitute 2]
- [common wrong substitute 3]
- any new prop not visible in the last frame
- detached floating cards
- detached label fragments

Object behavior rule:
every foreground prop must remain a rigid flat paper cutout. Do not morph one icon into another. Do not substitute one grocery or evidence symbol for another. Do not let any object enter at a dramatically larger scale than its final size.
```

如果你只写：

- `grocery elements`
- `fuel elements`
- `rent elements`

模型往往会把它们当成语义篮子，而不是固定物件，于是中段会自己补出奶瓶、鸡蛋、购物袋或飘散纸卡。

### 图表、路线和红线的强化结构

首帧里已经存在的坐标轴或卡片不能再写成 `the chart card drops in`。必须区分固定 surface 和新增 stroke：

```text
Fixed persistent surface:
- the [chart / map / board / document] surface and its structural marks already exist in the first frame
- keep this exact surface pixel-locked from first frame to last frame
- never drop in, flip, replace, cover, duplicate, resize, or redraw the fixed surface

Draw-on path only:
- draw one [curve / route / connection / underline] entirely inside or on its declared fixed surface
- the stroke begins at its specified final start point and grows toward its final endpoint by progressive leading-tip extension
- previously drawn stroke remains visible behind the moving tip
- each point marker appears only when the tip reaches that exact final coordinate
- no complete-path fade-in, no duplicate surface, no detached arc, and no stroke outside its declared surface

Identity separation:
- every visually similar line or accent receives a different object ID and final zone
- one path may never travel into another zone or transform into another line
```

这些约束还必须写入 `SEEDANCE_SCENE.json.motion_contract`；只放在 prose prompt 里不算通过。

### 视频 prompt 示例

```text
Transform the provided first-frame and last-frame images into a premium Vox-style editorial mixed-media animation.

Preserve the final composition of the provided last frame exactly. Do not redesign, replace, or substantially reposition elements. The first frame is the empty starting plate. The last frame is the finished evidence board.

Style:
Vox-style editorial mixed-media collage in motion, rough white-bordered cutouts, flat bold color fields, halftone and paper grain, restrained marker annotations and route lines, rigid paper-piece motion, soft layered shadows, snappy editorial timing, subtle handcrafted settles, non-photorealistic, no live-action

Camera:
keep the camera locked. No zoom, no pan, no reframing, no cuts, no morphing, no replacement of objects.

Timing structure:
0-70 percent: board assembles from back to front
70-100 percent: living poster hold

Assembly behavior:
start with the bare corkboard and map scraps already present. Let the note land first near center, then cash bundles slide in from the lower edge, then the parachute evidence card, then the red string draws across the map, then pins and stamp marks settle.

Hold behavior:
once the final composition is reached, keep all major pieces fixed. Allow only slight paper-corner lift, faint shadow breathing, and one subtle red-string quiver.

Audio:
no narration baked in. Prefer paper slide, pin click, tape press, soft room tone.

Avoid:
CGI smoothness, excessive camera motion, clutter growth, late redesign, dramatic atmosphere
```

## 4. `motion_intent` 模板

`motion_intent` 不描述美术，要描述运动关系。

### 模板

```text
The camera remains [locked / nearly locked / with only a very slight drift]. The scene begins on [empty base / partial layout / quiet background], then [hero subject] enters first / after [supporting element], followed by [secondary motion]. [Anchored object] stays fixed throughout. Motion should feel like rigid paper pieces being placed by hand, with small stepped settles rather than smooth cinematic animation. By the final third of the shot, the composition is fully assembled and holds as a living poster, with only micro-motion in [paper corners / shadows / string / halftone texture].
```

### `motion_intent` 示例

```text
The camera remains locked. The scene begins on a quiet corkboard plate with only the map scraps and date strip already fixed in place. The typed hijacker note lands first and becomes the visual anchor. Cash bundles slide in from below, followed by the parachute evidence card from the right. The red string is drawn across the map last, and the brass pins settle after it. The map base and date strip stay anchored throughout. Motion should feel like rigid paper pieces placed by hand, with stepped settles and no cinematic smoothing. By the final third of the shot, the full board is assembled and holds as a living poster, with only slight paper-corner lift, soft shadow breathing, and one tiny string quiver.
```

## 5. Thumbnail prompt 模板

### 规则

- 一个主 subject
- 最多两个文字块
- 每个文字块最多 3 个词
- 大号 condensed all caps
- 热红和亮黄可以比正片更大声
- 必须在 `200px` 宽时还能读

### 模板

```text
Create a high-contrast Vox-style editorial mixed-media thumbnail.

Hero subject:
[one dominant person / object / place cutout]

If the subject is a real person:
add a black censor bar across the eyes.

Headline block:
[1-3 words]

Secondary stamp or label:
[optional, 1-3 words]

Highlight device:
[red marker circle / yellow highlight bar / stamp box / underline]

Background:
aged torn newsprint bleeding off frame, with hard contrast and bold red-yellow accents

Style:
black-and-white halftone cutout, rough scissor-cut edges, red offset stroke, torn paper labels, archival newspaper texture, bold condensed type, poster-scale readability

Rules:
no small details, no extra text, no logos, no watermark, [Gate 1 aspect ratio and canvas], extremely readable at thumbnail size
```

## 内容优化示例

### 原始需求

```text
做一个讲 1971 年劫机失踪案的拼贴视频，想要有档案感、地图感、证据感，最后停在一直没找到的那个东西上。
```

### 优化成 scene brief

```yaml
scene_goal: turn the case into a clear Vox mixed-media evidence explainer
ending_hook: the missing parachute
first_frame_logic:
  - corkboard and map scraps already present
  - central evidence area left empty
last_frame_logic:
  - note, cash, parachute card, and red string fully assembled
motion_order:
  - note
  - cash
  - parachute card
  - string and pins
route: seedance-first-last
```

先把需求优化成这种结构，再去写图片和视频 prompt，成功率会明显更高。

## 6. Vox Mixed-Media 专用模板

所有 scene 都优先使用这组 prompt 语法，不要默认写成证据板或档案桌面。

### Vox STYLE tokens

```text
editorial mixed-media collage, bright tactile cut-paper with rough fibrous white borders, broad chromatic fields, at least three meaningful chromatic hues, warm-cool counterpoint, deep chromatic anchor, controlled fibrous white neutral, crisp halftone and paper-grain texture separation, hand-drawn marker annotations, abstract data graphics, flat maps, non-photorealistic, no live-action, no sepia wash, no all-beige palette, no muddy brown-gray cast, no desaturated vintage filter, no monochrome kraft-paper scene, no faded low-contrast look
```

### Vox beat 图片 prompt 模板

```text
Create a Vox-style editorial mixed-media collage still for this beat.

Core idea:
[state the narration idea, not the literal sentence]

Hero subject:
[one dominant subject]

Supporting devices:
- [chart / map / marker circle / comparison object]
- [supporting cutout 2]
- [supporting cutout 3 if needed]

Background:
[one dominant flat color field with subtle paper grain]

Palette lock:
[copy color_script.prompt_palette_sentence verbatim]

Negative palette:
[copy every color_script.negative_palette_terms phrase verbatim]

Style:
editorial mixed-media collage, bright tactile paper cutouts with rough white fibrous borders, broad chromatic color fields, at least three meaningful chromatic hues, warm-cool counterpoint, crisp halftone and paper grain textures, hand-drawn marker annotations, abstract shapes, non-photorealistic, no live-action

Rules:
one strong visual idea, bright editorial clarity, no long readable text, no subtitles, no photorealism, no 3D render, no clutter
```

### Vox beat 图片示例

```text
Create a Vox-style editorial mixed-media collage still for this beat.

Core idea:
food waste happens before food reaches the plate

Hero subject:
a full dinner plate cutout near center

Supporting devices:
- a row of apples and bread loaves flipping downward into a torn-paper bin shape
- one thick black marker circle around the final remaining plate

Background:
a warm yellow flat paper field with halftone texture

Palette lock:
warm yellow is the dominant field, turquoise and leaf green are support colors, coral red is the focal accent, deep navy is the dark anchor, and fibrous cream is used only for cut edges and breathing room

Style:
editorial mixed-media collage, bright tactile paper cutouts with rough white fibrous borders, broad chromatic color fields, crisp halftone and paper grain textures, hand-drawn marker annotations, non-photorealistic, no live-action

Negative palette:
no sepia wash, no all-beige palette, no muddy brown-gray cast, no desaturated vintage filter, no monochrome kraft-paper scene, no faded low-contrast look

Rules:
bright editorial composition, no readable text, no 3D, no photorealism, no clutter
```

### Vox scene prompt 模板

```text
Create a Vox-style mixed-media editorial scene.

Scene goal:
[what this scene must explain]

Primary visual system:
[cutout / chart / map / compare-and-contrast / editorial page]

Hero subject:
[main cutout or shape]

Supporting devices:
- [marker circle / underline / route line / chart bar / highlight block]
- [supporting cutout]

Background:
[deep navy / warm yellow / off-white / coral field with subtle paper grain]

Palette lock:
[copy color_script.prompt_palette_sentence verbatim]

Negative palette:
[copy every color_script.negative_palette_terms phrase verbatim]

Motion intent:
snappy motion-graphics behavior, one loud action at a time, clear ease-out entrances, optional slow push-in on emphasis, no live-action camera realism

Avoid:
long readable text, cinematic realism, 3D infographic style, live-action faces, clutter
```

### Vox 视频 prompt 模板

```text
Transform this scene into a Vox-style mixed-media editorial motion-graphics animation.

Style:
archival cutouts with white paper borders, flat bold color fields, halftone and paper grain texture, hand-drawn circles and underlines, abstract charts and maps, non-photorealistic, no live-action

Motion:
snappy pop-ins, slide-ins, marker sweeps, chart growth, route-line draw-ons, one dominant emphasis action per beat, optional gentle push-in on the key point

Camera:
editorial motion-graphics camera only, no cinematic realism, no handheld, no live-action emulation

Rules:
keep the scene readable, avoid long readable text, no subtitles inside the generated image, no photorealism, no glossy 3D graphics
```

### Vox 内容优化示例

#### 原始表达

```text
食品浪费很多，而且很多是在上桌之前就浪费掉了。
```

#### 更适合 Vox mixed-media 的 beat 提取

```yaml
core_idea: most waste happens before consumption
hero_subject: dinner plate
support_devices:
  - falling food row
  - torn-paper bin shape
  - marker circle
background: warm yellow field
best_scene_type: compare-and-contrast or symbolic explainer
style_family: vox-mixed-media
```

这个版本更适合 Vox 风格，因为它不是把信息压进一张档案桌面，而是把概念转成一个立即可读的编辑型比喻。
