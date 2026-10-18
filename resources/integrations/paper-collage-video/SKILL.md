---
name: paper-collage-video
description: 以代码优先的工作流构建或逆向拆解纸艺拼贴和 Vox 风格的编辑型视频。适用于 Codex 需要分析参考拼贴动画、提取其风格与节奏结构、制作分镜和主资产总表、规划或生成自带撕边效果的透明 PNG 剪贴素材、搭建基于 Remotion 的项目骨架、组装单个短场景或旁白驱动的多场景序列、应用视差或分步式运动、使用红色描边的剪贴分层、将道具拆成前后层形成夹心纵深，或在渲染前加入克制的音乐、旁白与音效的场景。
---

# 纸艺拼贴视频

## 概览

将参考片段或新的拼贴概念整理成可重复执行的短动画制作流程。优先采用代码驱动的组装方式、可复用的剪贴素材、清晰的质量关卡，以及克制稀疏的音频设计。

用户通常不需要先提供技术参数，默认把以下任一输入当作起点：

- 一个故事
- 一段口播稿或逐句旁白
- 一段“我想做什么”的需求描述

收到这类输入后，先依次通过 `Gate 0` 和 `Gate 1`。如果 Gate 1 选择生成配音，再通过 `Voiceover Gate`。这些 Gate 未通过前，不得拆节拍、生成视觉素材或编写动画。

## 选择模式

这套 skill 里有两层“模式”，不要混用：

- 用户弹窗里的 `mode`
  是制作方式选择：
  `remotion-code` 或 `video-model`
- 内部工作流里的 `content shape`
  是内容组织形态：
  `single-scene` 或 `vo-sequence`
- `scene route`
  是场景级执行路线：
  简单 scene 走 `Remotion cutout`，复杂 scene 走 `Seedance 1.5 Pro first+last`

默认视频模型固定为 `doubao-seedance-1-5-pro-251215`。这是区分大小写的规范模型 ID，所有配置、场景文件和 API 请求都必须复用该值。当单个 scene 同时包含大量元素、多个元素都需要复杂独立运动、或者更适合作为“一整张会动的拼贴画面”处理时，优先切到 Seedance 首尾帧路线。

先阅读 [references/workflow.md](references/workflow.md)。当项目是旁白驱动、按场景组织或偏编辑解说时，再阅读 [references/vox-broll-sequence.md](references/vox-broll-sequence.md)。所有 `vox-mixed-media` 项目必须阅读并执行 [references/0720-bright-paper-style.md](references/0720-bright-paper-style.md)；当使用 `remotion-code` 时，必须再阅读并执行 [references/vox-motion-contract.md](references/vox-motion-contract.md)。
当你需要决定某个节拍应该构建成哪类场景模块时，阅读 [references/scene-archetypes.md](references/scene-archetypes.md)。
当项目明确以视频模型驱动复杂 scene，或你需要统一脚本、关键帧和视频提示词的语言时，阅读 [references/video-model-collage-reference.md](references/video-model-collage-reference.md)、[references/seedance-motion-contract.md](references/seedance-motion-contract.md)、[references/script-standards.md](references/script-standards.md) 和 [references/prompt-recipes.md](references/prompt-recipes.md)。
当项目明确想把 `vox-motion-graphics.skill` 里的 Mixed Media 风格迁入当前 skill 时，阅读 [references/vox-style-migration.md](references/vox-style-migration.md)。
当需要理解 Edge TTS 直连、远程 HTTP 服务方案或未来切换后端时，阅读 [references/edge-tts-voiceover.md](references/edge-tts-voiceover.md)。
当你需要稳定复用这套 skill，而不是靠临场判断时，额外阅读 [references/output-contract.md](references/output-contract.md) 和 [references/golden-example.md](references/golden-example.md)。

## 每次调用先自检

每次调用都先过 `Gate 0`，再进入任何内容分析或生成。

`Gate 0` 是环境与能力自检。未通过前，不得进入分镜、出图、动画或视频生成。

至少检查以下前置：

- skill 目录 `.env` 是否明确包含非空的 `ARK_API_KEY`
- `imagegen` skill 是否可用
- Remotion skill/plugin、Node 和 npm 是否可用
- Edge TTS 是可选能力；只有 Gate 1 选择 `generate-voiceover` 后才将其升级为必需能力
- 当前工具清单是否包含 `show_select_popup` 这类 Tool Call / Function Calling 弹窗；如果没有，记录为文本选择模式，不把它当作允许自动默认的理由
- 是否知道 Seedance 复杂 scene 固定只用 2 张图：首帧空镜和尾帧停驻图
- scene 时长是否适合 `Seedance 1.5 Pro` 的 `4-12s` 区间
- 是否确认图片直接走本地 `base64` 提交，不需要公网图床

固定把 skill 目录下的本地配置文件作为 Gate 0 的配置源：

- `~/.codex/skills/paper-collage-video/.env`

必须具备这个环境变量：

```bash
ARK_API_KEY=...
```

Gate 0 必须运行下面的机器检查，并检查退出码；不得只阅读 `.env` 文件是否存在：

```bash
python3 ~/.codex/skills/paper-collage-video/scripts/preflight.py
```

退出码非 0 时立即停下并向用户报告缺项。不得创建项目骨架，也不得以进程环境中的同名变量代替 skill 目录 `.env` 的配置。

不要把密钥写进项目文档或提交进仓库。脚手架只应记录变量名，不要记录真实值。
如果未来把这个 skill 同步到 GitHub，确保 `.env` 已被 `.gitignore` 排除。

## 开始时先补选项

通过 `Gate 0` 后，再进入 `Gate 1`。

`Gate 1` 是用户选择锁定。未完成前，不得开始 beat 拆分、scene 规划、资产生成或任何实现步骤。

当用户开始调用这个 skill 时，不要直接开做，先完成以下字段锁定；只有明确标为用户选项的字段才弹窗：

- `mode`：`remotion-code` 或 `video-model`
- `style_family`：固定锁定为 `vox-mixed-media`，不再弹出风格选择
- `aspect_ratio`：`16:9 / 9:16`
- `total_duration_rule`：不是用户选项，按以下优先级自动锁定：内容音频实测时长 -> 新生成配音实测时长 -> 用户在原始需求中明确给出的整片时长 -> 根据内容长度与旁白节奏自动估算。
- `scene_duration_policy`：不是用户选项。`video-model` 固定为 `auto-by-content`，先按语义拆 Scene，再依据各 Scene 的内容窗口、动作组数量和停驻需求，在 `4-12s` 内自动确定请求时长；需要超过 `12s` 的内容必须继续拆 Scene。`remotion-code` 记为 `not-applicable`。
- `audio_mode`
  如果用户提供了内容音频，就使用该内容音频。
  如果用户没有提供内容音频，必须弹出：`生成中文男声配音 / 不需要音频`。
  用户选择生成配音时锁定为 `generate-voiceover`，固定使用 Edge 在线 TTS 与 `zh-CN-YunjianNeural`。
  用户选择不需要音频时锁定为 `no-audio`。

优先规则：

- 如果宿主支持 Tool Call / Function Calling 弹窗，必须调用结构化弹窗工具让用户选择，不要改成自然语言提问
- 如果不支持弹窗，用简短文本选项提问并等待用户回复
- 如果用户明确说“你自己定”或“按默认来”，才允许回退到默认值

如果宿主支持函数调用，使用 `show_select_popup` 这类工具契约，而不是输出普通文本选项。具体 schema、回传格式和状态管理规则，阅读 [references/popup-tool-contract.md](references/popup-tool-contract.md)。

`Gate 1` 通过条件：

- `mode` 已锁定
- `style_family=vox-mixed-media` 已自动锁定
- `aspect_ratio` 已锁定
- `total_duration_rule` 与整片时长来源已按规则自动锁定
- `scene_duration_policy` 已由制作模式自动锁定
- `audio_mode` 已锁定或由 source audio presence 自动锁定
- `generate-voiceover` 时，`total_duration_rule=follow-generated-voiceover` 已锁定，具体秒数允许在 Voiceover Gate 后写入

如果以上任一项仍未锁定，流程必须停在选择阶段。

## 缺省决策规则

只有 `mode`、`aspect_ratio` 和无源音频时的 `audio_mode` 需要用户明确授权默认值。`total_duration_rule` 与 `scene_duration_policy` 始终按上面的自动规则锁定，不需要也不得请求默认授权。

对需要用户决定的字段，只有在以下情况下，才使用默认值继续推进：

- 用户明确授权“你自己定”

弹窗不可用不构成默认授权。此时必须改用文本选项并停在 Gate 1 等待回复。

默认值与自动值如下：

- `mode`：默认 `remotion-code`
- `style_family`：默认 `vox-mixed-media`
- `aspect_ratio`：默认 `16:9`
- `content shape`：单一镜头需求默认 `single-scene`；存在明确旁白、故事线或多段叙述时默认 `vo-sequence`
- `orientation`：`16:9` 归为 `horizontal`，`9:16` 归为 `vertical`
- `audio_mode`：有内容音频时 `use-source-audio`；无内容音频且用户授权默认值时 `no-audio`
- `total_duration_rule`
  有内容音频时固定跟随音频；生成配音时固定跟随生成音频；无音频时按内容估算整片时长。
- `scene_duration_policy`
  `video-model` 默认 `auto-by-content`，由每个 Scene 的实际内容自动分配 `4-12s`；不把默认值解释为整片 5 秒。
- `scene route`：默认先判 `remotion-cutout`，只有命中复杂 scene 判定矩阵时才升级到 `seedance-first-last`

如果用户后来明确补充整片时长，可覆盖 `estimated-from-content`；`scene_duration_policy` 仍由制作模式自动决定，不接受固定 5 秒或 10 秒的覆盖值。

## Voiceover Gate

仅当 `audio_mode=generate-voiceover` 时执行，位置固定在 Gate 1 之后、beat/Scene 拆分之前。

1. 将用户输入固化为最终中文口播稿。输入本身已经是口播稿时只做必要的标点和口语流畅度调整；故事或需求描述需要改写时，按 [references/script-standards.md](references/script-standards.md) 生成最终旁白。
2. 将最终旁白保存为项目内 UTF-8 文本，例如 `00_brief/narration.txt`。在 TTS 后不得再修改文字；如需修改，必须重新生成 MP3 和 SRT。
3. 运行配音能力检查：

```bash
python3 ~/.codex/skills/paper-collage-video/scripts/preflight.py --require-edge-tts
```

4. 检查通过后生成配音：

```bash
python3 ~/.codex/skills/paper-collage-video/scripts/generate_edge_voiceover.py \
  --project [project-root] \
  --text-file [project-root]/00_brief/narration.txt
```

固定输出：

- `04_audio/voiceover.mp3`
- `04_audio/voiceover.srt`
- `04_audio/voiceover-metadata.json`

固定声音为 Edge 在线 TTS 的普通话中国男性 `zh-CN-YunjianNeural`，不弹出声音选择。

5. 读取 SRT cue，按内容语义把相邻 cue 合并成 Scene，并保存 `01_storyboard/srt-scene-plan.json`：

```json
{
  "timeline_source": "srt",
  "scenes": [
    {
      "scene_slug": "scene-01-example",
      "cue_start": 1,
      "cue_end": 4,
      "scene_goal": "这一段画面要表达的唯一信息"
    }
  ]
}
```

所有 cue 必须按原顺序连续归属，且恰好出现一次。Scene 可以合并多个相邻 cue，但不能跨过未归属 cue、重复 cue 或把一个 cue 拆开。

Voiceover Gate 只有同时满足以下条件才通过：

- MP3、SRT 和 metadata 三个文件都存在且非空
- metadata 的 `voice` 为 `zh-CN-YunjianNeural`
- metadata 含实测 `duration_seconds`
- `total_duration_seconds` 被该实测值覆盖，`duration_source=generated-voiceover`
- 后续 beat 时间窗来自 SRT，不再按文本行平均分时
- `srt-scene-plan.json` 已覆盖全部 SRT cue，且每个 Scene 有明确的 `scene_goal`

Edge TTS 或网络调用失败时立即停止，不得退回估算时长、无声模式或其他声音继续制作。

成片音频规则：

- `remotion-code`：脚手架把配音复制到 `07_remotion/public/audio/`，主序列使用 Remotion `Audio` 层加载
- `video-model`：所有 Seedance Scene 保持 `generate_audio=false`；Scene 按 SRT 时间轴拼接完成后运行：

```bash
python3 ~/.codex/skills/paper-collage-video/scripts/mux_voiceover.py \
  --video [assembled-silent-video.mp4] \
  --audio [project-root]/04_audio/voiceover.mp3 \
  --output [project-root]/05_render/final-with-voiceover.mp4
```

视频模型拼接画面短于配音时必须回到 Scene 时长规划修正，不得裁掉旁白。

## 固定输出契约

这个 skill 不接受“差不多有这些内容”的松散输出。每次正式执行都要尽量收敛到固定结构。

最低要求：

- `input intake summary`
- `beat list`
- `scene list`
- `storyboard`
- `route decision`
- `motion_intent`
- 复杂 scene 时补 `SEEDANCE_SCENE.json`

字段级格式、命名和验收规则，统一以 [references/output-contract.md](references/output-contract.md) 为准。

## 初始化项目

当工作区里还没有可用的制作骨架时，运行 `scripts/bootstrap_collage_video.py`。

只有 Gate 0、Gate 1 以及所需的 Voiceover Gate 已通过，才允许运行脚手架。脚手架的 `--production-mode`、`--style-family`、`--aspect-ratio`、`--duration`、`--duration-source`、`--audio-mode` 和 `--gate1-source` 都必须来自已锁定结果；其中 `--duration` 始终表示整片总时长。`--scene-duration-policy` 由脚手架根据 `production-mode` 自动写入，不是 Gate 1 用户输入。生成配音时还必须传入 `--source-audio-file`、`--subtitle-file`、`--voiceover-metadata-file` 和 `--srt-scene-plan-file`，禁止临时猜值补齐命令。

注意：

- 这里脚手架命令里的 `--mode`，指的是内部内容组织形态，也就是 `single-scene / vo-sequence`
- 它不等于用户弹窗里选择的制作方式 `remotion-code / video-model`

示例：

```bash
python3 ~/.codex/skills/paper-collage-video/scripts/bootstrap_collage_video.py \
  --output ./collage-boat-remake \
  --mode single-scene \
  --production-mode remotion-code \
  --scene "A dollar-bill boat carries pilgrims across a torn-paper ocean at sunrise" \
  --duration 10 \
  --duration-source user \
  --style-family vox-mixed-media \
  --aspect-ratio 16:9 \
  --audio-mode no-audio \
  --gate1-source user-selection \
  --reference-url "https://example.com/reference.mp4"
```

如果是 Vox 风格序列：

```bash
python3 ~/.codex/skills/paper-collage-video/scripts/bootstrap_collage_video.py \
  --output ./empire-downfall-remake \
  --mode vo-sequence \
  --production-mode video-model \
  --scene "A paper-textured explainer about imperial decline and the exit from the dollar" \
  --duration 47.3 \
  --duration-source user \
  --fps 30 \
  --video-model "doubao-seedance-1-5-pro-251215" \
  --animation-strategy auto \
  --scene-complexity auto \
  --aspect-ratio 16:9 \
  --style-family vox-mixed-media \
  --audio-mode no-audio \
  --gate1-source user-selection \
  --narration-file ./narration.txt \
  --scene-count 7
```

生成以下产物：

- `project-config.json`，包含时序、引擎、风格规则，以及默认节拍数据或旁白驱动的节拍数据
- `00_brief/`, `01_storyboard/`, `02_assets/`, `03_animation/`, `04_audio/`, `05_render/`
- `00_brief/self-check.md`，用于第一次运行前检查 Seedance 前置
- `03_animation/scene-routing.md`，标明哪些 scene 该留在 Remotion，哪些该切 Seedance
- `03_animation/seedance-runbook.md`，记录 Seedance 执行命令
- 适配所选模式的 `prompts/01-04`
- 在 `video-model + single-scene` 模式下：`03_animation/SEEDANCE_SCENE.json`
- 在 `video-model + vo-sequence` 模式下：每个场景文件夹各自一份 `SEEDANCE_SCENE.json`
- 在 `remotion-code` 模式下：每场一份版本化 `ASSETS.json`、四份最小必需素材提示词，以及自动生成的 `07_remotion/`
- 生成配音时：`04_audio/voiceover.mp3`、`04_audio/voiceover.srt` 和 `04_audio/voiceover-metadata.json`
- 生成配音的序列项目：`01_storyboard/srt-scene-plan.json`

传入 `--kit-path /path/to/practice-kit`，可将现有练习包中的 `assets/` 和 `audio/` 复制到 `source-kit/`。
选择 `--production-mode remotion-code` 后必须自动生成 `07_remotion/`，不再依赖调用方记住 `--with-remotion-template`。

## 执行工作流

### 1. Analyze before generating

从参考视频片段或静帧开始。在编写动画代码或生成新的剪贴素材之前，先产出一份主资产总表和逐节拍分镜板。

在 `vo-sequence` 模式中，把旁白当作主时间线，并在决定各场景时长之前，先把节拍组映射到具体场景。

如果用户只给故事或需求描述，先补齐并确认这些选择：

- 制作方式：`remotion-code / video-model`
- 风格体系：固定使用 `vox-mixed-media`
- 比例：`16:9 / 9:16`
- 如果有内容音频：整片总时长固定跟随该音频
- 如果没有内容音频：先询问 `生成中文男声配音 / 不需要音频`
- 选择生成配音：总时长固定跟随生成后的 MP3，使用 SRT 时间窗拆分 Scene，不再询问总时长
- 选择不需要音频：若用户原始需求未明确整片时长，则自动按内容长度和旁白节奏估算，不再询问时长
- 如果制作方式是 `video-model`：自动锁定 `scene_duration_policy=auto-by-content`，不弹出单 Scene 时长选项

然后再把内容拆成：

- beat list
- scene list
- storyboard
- 每个 scene 的 `motion_intent`
- 每个 scene 的制作说明必须继承 Gate 1 的全局模式；`remotion-code` 项目全部使用 Remotion，`video-model` 项目全部使用 Seedance，不得在执行中静默切换引擎

存在 `voiceover.srt` 时，beat 与 Scene 的时间边界必须来自 SRT cue。可以把多个相邻 cue 合并成一个语义 Scene，但不得用平均字数重新计算时间，不得把一个 cue 任意截断，也不得让 Scene 脱离对应口播区间。

视频模型的时长规划顺序固定为：先确定整片时间轴 -> 按语义拆 Scene -> 为每个 Scene 分配内容窗口 -> 写入该 Scene 的 Seedance 请求时长。不得先套用统一单 Scene 时长，再把整段长内容塞进单个 Scene。

每个 Seedance Scene 必须满足：

- 请求时长为整数 `4-12s`
- `auto-by-content` 下，单一简单视觉动作通常取 `4-6s`，包含多个依次出现元素或复杂图表绘制时通常取 `7-10s`，需要充分停驻但动作预算仍合格时最多 `12s`
- Scene 请求时长必须服从旁白对齐、动作完整性和最终停驻需求，不得为了整齐而统一为同一时长
- 预计超过 `12s`、超过该时长动作组预算、或包含两个独立叙事结果时，必须继续拆 Scene
- 整片总时长等于各 Scene 内容窗口之和，或由源音频时间轴决定；不得等于单个 Scene 的请求时长

### 2. Match the style at the asset stage

先执行不可逆的路线分支，不得把两条路线串行执行：

- `production_mode=video-model` / `route=seedance-first-last`：每个 Scene 只允许生成 `first-frame.png` 和 `last-frame.png` 两张全画幅图片。禁止创建 `ASSETS.json`、Composition Blueprint、独立 background/hero/support 素材、contact sheet、`07_remotion` 或 Remotion 模板；不得先做 cutout pack 再切换到 Seedance。
- `production_mode=remotion-code` / `route=remotion-cutout`：进入下述分层资产、Composition Blueprint、碰撞规划和 Remotion 编排流程。

Gate 1 的 `aspect_ratio` 是所有关键帧画布的唯一来源。脚手架将其动态转换为画布契约：`16:9 -> 1536x864 horizontal`，`9:16 -> 864x1536 vertical`。不得在模板、提示词或代码中固定写死 `16:9`。首帧提示词必须包含 Gate 1 画幅、方向和目标画布；生成后立即运行 `validate_seedance_first_frame.py`，通过后才能编辑尾帧。

把拼贴质感直接写进每个图像提示词里，而不是打算留到后期统一处理。Remotion 独立素材应明确要求撕裂边缘、可见白色纤维、纸张颗粒和透明背景上的细白贴纸边框；Seedance 关键帧则使用 Gate 1 全画幅画布，不要求透明背景。
所有新增图片素材默认通过 `imagegen` skill 产出，除非用户已经提供现成素材，或明确要求改用别的图像生成方式。执行前必须阅读 [references/asset-provenance-contract.md](references/asset-provenance-contract.md)。PNG 文件本身不代表已调用 imagegen；必须保留逐资产 prompt、imagegen 原始输出、工具结果回执和匹配哈希。
在 `remotion-code` 模式里，`Remotion` 只负责动画编排、分层、时间控制和镜头组织；不得用代码直接画 SVG 图表、报纸版面、气泡、计数器卡、结尾 punchline 卡或其他主要可见素材图。凡是会被观众当成主视觉内容阅读的可见素材，必须先通过 `imagegen` / Imagen 生成或由用户提供，再交给 Remotion 动起来。

如果 `image_gen` 工具不可用或调用失败，停止在 Asset gate 并报告阻塞；禁止自动降级为 Pillow、ImageDraw、Canvas、SVG、CSS、OpenCV、Cairo、Matplotlib、Sharp 或 ImageMagick 绘图。不得创建 `generate_assets.py` 一类本地可见资产生成器。唯一允许的本地处理是对既有 imagegen / 用户素材做抠图、裁切、边缘清理或颜色修正，不得新增可见内容。

在任何 Remotion Studio 预览或渲染前，必须运行项目内的资产校验：

```bash
python3 tools/validate_collage_project.py --project .
```

校验失败时不得启动 Studio 或渲染。禁止项包括任何 `.svg` 文件、TS/TSX 中的内联 `<svg>` / SVG data URI、Pillow/Canvas 等程序化可见资产生成器、缺失 imagegen 来源记录、缺失的分层位图资产、未批准资产，以及用一张完整 scene 图替代分层资产。

当用户希望模仿、改造或扩展同一套视觉外观时，阅读 [references/style-guide.md](references/style-guide.md)。

对于编辑型序列，还要保持统一锁定的视觉语法：

- 共享纸张质感、配色和标注语法，但每个 scene 默认生成符合该分镜内容的独立背景
- 小而精的配色体系，并带一个标志性强调色
- 中景剪贴层，搭配错位的轮廓描边
- 能够锁定每个镜头结构的前景锚点或文字系统

如果 `style_family=vox-mixed-media` 且当前 Scene 为 `remotion-cutout`，再额外应用这些规则：

- 优先使用 flat bold color fields，而不是总是档案纸底
- 优先使用 hand-drawn circles、underlines、arrows、redaction blocks
- 允许 abstract data graphics、flat maps、scale-comparison motifs
- 动效可更 snappy，但仍保持 editorial clarity，不要变成影视镜头
- 除非是极短标签或道具型字样，尽量不要把真实可读长文本直接画进素材图
- 每个 Remotion scene 至少交付 1 个独立背景和 3 个独立可运动叙事素材；默认总资产数为 4-8 个
- 每个 scene 在资产生成前必须先写 `visual_metaphor`、`composition` 和 `motion_rhythm`；先把抽象观点映射成一个可运动的具体机制，再决定素材清单
- 不得默认使用“中央主体 + 左右辅助 + 底部长条”；底部长条不是必选资产，只能在内容确实需要地面、堆积、结果带或遮挡时使用
- 相邻 scene 禁止复用同一布局原型；4 个以上 scene 的序列至少使用 3 种布局原型和 3 种运动节奏
- `module_type` / `layout_archetype` 必须由真实锚点、阅读路径、纵深和动作兑现，不能只写在文档里却继续调用同一固定排版
- 在任何背景或元素出图前，必须先完成 `background_contract` 与 `collision_plan`：背景禁止主体、元素保留区、静态落位框、动作终点框、安全间距、允许遮挡对和运动扫掠路径全部锁定
- 在任何出图前必须完成每场 `color_script`：有彩主色、至少两种有彩辅助色、焦点色、深色锚点、纸张中性色、颜色面积预算、主体/背景对比和相邻 Scene 换色策略全部锁定
- 默认执行 `0720-bright-paper` 色彩方向：安静背景是低细节而不是低饱和；米白只做留白与撕边，褐灰只做少量结构材质，禁止默认生成全米黄、灰绿、棕褐或褪色怀旧画面
- 每场默认至少出现 3 种有意义的有彩色，并建立冷暖对撞和深中浅层级；主体必须在缩略图下凭轮廓和局部色彩对比从背景中分离，不能只依赖阴影
- 背景与全部独立素材 prompt 必须逐字复制已批准的 `prompt_palette_sentence` 和 `negative_palette_terms`，防止不同批次素材发生色漂
- 背景只能承担低显著度舞台作用；如果店铺、人物、车辆、图表或其他主体会作为独立素材进入，背景禁止再出现同类高细节对象抢占该落位区
- 背景必须先单独生成并审查；确认保留区清空、无重复主体、不会争夺焦点后，才允许生成前景元素
- 未声明的元素两两重叠默认不得超过较小落位框的 8%；有意遮挡必须记录对象对、最大重叠比例和叙事理由

仅对 `remotion-cutout` Scene，在第一次调用 imagegen 之前必须运行：

```bash
python3 tools/validate_composition_blueprint.py --project .
```

退出码非 0 时停在 Composition blueprint gate。不得先生成背景试错，更不得批量生成元素后再调整位置。
- 禁止跨 scene 复用同一背景，除非用户明确要求连续空间并记录 `background_sharing_authorized: true`
- 禁止把多个需要单独运动的角色、道具或因果元素合并成一个 hero PNG
- 非背景 PNG 在进入 Remotion 前必须裁去透明留白，只保留 3-5% 安全边距；不得用带大面积透明边缘的 imagegen 原图直接编排
- 为每个元素写明 `content_kind`、`sizing_mode`、按 alpha 可见边界计算的实际占屏尺寸、锚点、`appearance_order`、`appearance_reason`、入场区间、内容动作、停驻方式和退场方式
- 入场运动与内容动作必须分开；文案包含退避、追击、合围、替代、击败、上升或下降时，必须填写独立 `action_motion`，不得用轻微漂浮代替叙事动作
- `appearance_order` 必须严格服从内容中的首次出现或因果顺序；标注元素必须在被标注对象之后出现
- 内容顺序、构图占比和逐元素运动核对完成前，不得把 `content_order_locked`、`composition_locked`、`motion_plan_locked` 设为 `true`

### 3. Build the scene as layered code

把镜头视为一组具有纵深关系、可循环运算的图层堆栈，而不是一个充满关键帧的时间线。背景运动应保持顺滑，把分步式或海报化的运动留给角色和主道具。

在搭建或调优动画实现时，阅读 [references/remotion-build.md](references/remotion-build.md)。

在 `vo-sequence` 模式下，把场景组件构建成模块，再按旁白时间线组装进总控的 `Series` 中。

在写组件之前，先锁定每个 scene 的 `ASSETS.json`。其中必须包含 scene 独立背景、至少 3 个独立可运动素材、内容隐喻、布局原型、阅读路径、主体画面占比和完整运动字段；不得强制每场都有 `foreground_anchor`。`vox-mixed-media` 的 Remotion 组件必须直接读取自己的 manifest，不能在组件里另写一套顺序和尺寸；可以使用通用 `VoxManifestScene`，也可以为径向、路径、堆叠、替换等隐喻写 Scene 专属 choreography。禁止所有 Scene 仅做同一通用模板的薄包装而没有真实布局和运动差异。尺寸范围、跨 Scene 构图去重、Vox 入场节奏及内容顺序映射以 [references/vox-motion-contract.md](references/vox-motion-contract.md) 为准。

当 scene 足够简单时，继续用 `Remotion`：

- 少量剪贴元素
- 可拆开的前中后景
- 适合视差、分步停顿、标签、计数器、alpha plate 的运动

当 scene 足够复杂时，切到 `Seedance 1.5 Pro`：

- 先用 `imagegen` skill 的生成模式制作唯一背景母版 `first-frame.png`，它是带有固定背景场景的空镜或近空镜
- 把 Gate 1 的 `aspect_ratio`、方向和脚手架生成的目标画布逐字注入 `first-frame.md`；不得默认写死横版或 `16:9`
- 首帧落盘后、尾帧生成前，必须运行 `python3 tools/validate_seedance_first_frame.py --project . --scene-spec [scene-spec]`；失败时停止，先规范化或重生首帧并记录原始回执、处理方式和最终哈希
- 必须先用 `view_image` 检查首帧，再调用内置 `image_gen` 的编辑模式，并把该首帧本地路径作为唯一 `referenced_image_paths`；只在已批准的 `change_regions` 内添加元素，输出 `last-frame.png`
- `last-frame.png` 是首帧母版的增量编辑结果，不是第二次独立文生图；禁止仅靠 “same background” 文本重新生成尾帧
- 首尾帧必须保持相同画布、裁切、镜头、背景几何、固定对象、撕边和材质纹理；允许变化的只有计划中从无到有的前景元素及其局部接触阴影
- `SEEDANCE_SCENE.json` 必须填写 `keyframe_generation_contract`：首帧与尾帧的真实工具回执、输出哈希、尾帧编辑目标路径、首帧输入哈希、`referenced_image_paths` 和允许变化区域
- 提交前必须运行 `python3 ~/.codex/skills/paper-collage-video/scripts/validate_seedance_keyframes.py --project [project-root] --scene-spec [scene-spec]`；非零退出时禁止提交
- 底层图像模型配置可以记录在项目里，但默认出图入口仍然是 `imagegen` skill
- 图片直接走本地 `base64` 提交，不需要上传公网图床
- 尾帧编辑完成后禁止再裁切或缩放任一关键帧；若需规范画布，必须在尾帧调用之前完成，并让规范化后的首帧成为真实编辑源
- `motion_intent` 必须先写清楚：谁先进入、谁保持锚定、镜头是否锁定、最后如何停驻
- `SEEDANCE_SCENE.json` 必须填写结构化 `motion_contract`；把首帧已有对象列为 fixed，把进场剪贴列为 entering，把曲线、路线和下划线列为 draw-on path
- 对照真实首尾帧完成对象状态审计，并确认自然语言 prompt 与结构化契约无冲突后，才能锁定两个 motion-contract audit 字段
- 首帧已经存在且尾帧继续存在的卡片、坐标轴或底板禁止再次“drop in / place / replace”；只能动画化它上面新增的内容
- 4-5 秒 scene 最多 4 组非停驻动作，6-12 秒最多 7 组；超出时合并同类重复对象、删减动作或拆 scene
- scene spec 填好后，运行：
  `python3 ~/.codex/skills/paper-collage-video/scripts/run_seedance_scene.py --project [project-root] --scene-spec ./03_animation/SEEDANCE_SCENE.json`

不要把 Seedance 当成所有镜头的默认方案；它是复杂 scene 的升级通道。

### 4. Add sound last

在生成任何音乐之前，先提出音乐方向选项。只加入那些真正能支撑场景的声音提示。一个短拼贴片通常只需要一条音乐底和大约三个拟音点。

### 5. Enforce the gates

在当前产物通过确认前，不要推进到下一阶段。

使用以下关卡：

- Gate 0：环境与能力自检通过
- Gate 1：用户选择锁定通过
- Storyboard gate：分镜板与用户脑海中的视频一致
- Composition blueprint gate：仅对 Remotion Scene，任何图片生成前，背景保留区、元素最终框、完整动作走廊和允许遮挡必须通过
- Asset gate：仅对 Remotion Scene，动画开始前质量弱的剪贴素材必须重生成
- Motion gate：场景在 1x 正常播放速度下感觉正确
- Layout audit gate：仅对 Remotion Scene，粗剪后抽取主组装帧和最终停驻帧；缩略图下主体、隐喻和阅读路径仍清楚，且相邻 Scene 构图不重复
- Seedance first-frame canvas gate：仅对 video-model Scene，首帧必须先匹配 Gate 1 画幅与目标画布，随后才允许生成尾帧
- Audio gate：任何会让人明显“注意到这是个声音”的提示音，都应被删掉

粗剪完成后运行：

```bash
python3 ~/.codex/skills/paper-collage-video/scripts/extract_layout_audit.py \
  --project [project-root]
```

必须查看 `05_render/layout-audit/contact-sheet.jpg`。如果主体在缩略图下过小、隐喻无法一句话说清、留白没有服务后续入场或阅读、相邻 Scene 的焦点位置/阅读路径/最终轮廓重复，就返回修改 Manifest 与 Remotion 编排，不得进入最终渲染。

Remotion 执行顺序固定为：

```bash
cd 07_remotion
npm run studio
npm run render
```

`npm run studio/render` 会自动复用 `~/.codex/cache/paper-collage-video/remotion-runtime/`，不得在每个项目里重新运行 `npm install`、重新创建 Remotion 工程或单独下载 Headless Chrome。首次匹配版本只安装一次；之后项目通过共享 `node_modules` 使用同一依赖和浏览器缓存。

`npm run render` 只生成 `07_remotion/out/rough.mp4`、联系表和待审 `05_render/layout-audit/review.json`。必须实际查看联系表，再把六项检查、`reviewer` 和 `status=approved` 填好；随后运行 `npm run finalize`，只有未过期的批准才能生成 `05_render/final.mp4`。

`ASSETS.json` 使用 `manifest_version=2`。旧项目先运行：

```bash
python3 ~/.codex/skills/paper-collage-video/scripts/migrate_asset_manifests.py --project [project-root]
```

迁移会保留备份并把批准状态重置为待复核，避免升级后一次抛出大量不相关错误。

## 应用核心风格规则

除非用户明确希望采用不同诠释，否则默认遵循以下规则：

- 使用有限配色，并让材质对比清晰可见
- 使用前后纵深的纸层关系，而不是扁平的拼贴贴纸感
- 优先采用视差漂移、摇摆、起伏和揭示机制，而不是频繁移动镜头
- 在角色上使用不均匀的分步停顿，以暗示人为摆放的质感
- 在编辑型序列中，所有场景共用一套锁定的视觉系统
- 共用视觉系统不等于共用同一张背景；背景环境必须随 scene 内容变化
- 当风格需要 Vox 式记号笔处理时，在透明剪贴素材后方使用错位轮廓描边
- 当角色需要显得“处在容器内部”时，把容器拆成前后两层
- 保持音频克制，并在混音中留出留白

## 产出正确的交付物

根据项目范围，交付以下部分或全部产物：

- 主资产总表
- 含时序和运动备注的分镜板
- 旁白时间线与节拍到场景的映射
- Seedance 复杂 scene 的首尾帧包
- 每个 scene 的 `motion_intent`
- 每个 Remotion scene 的独立背景、分层资产和逐元素运动契约
- 可重复生成的素材提示词包
- 动画方案或 Remotion 脚手架
- 场景组件 brief 与序列组装计划
- 标注 cue 时点和音量级别的声音地图
- 最终渲染检查清单

## 使用随附资源

- `scripts/bootstrap_collage_video.py`：生成新的项目文件夹和提示词包骨架
- `scripts/preflight.py`：每次调用时执行 Gate 0；缺少 skill-local Ark key、imagegen、Remotion 或 Node/npm 时以非零状态退出
- `scripts/validate_collage_project.py`：在 Remotion 预览和渲染前执行资产 Gate，阻止 SVG、程序化绘图、伪造 imagegen 来源、缺失分层位图和未批准资产
- `scripts/submit_seedance_video.py`：向 Seedance 提交首尾帧任务并轮询结果
- `scripts/validate_seedance_keyframes.py`：校验尾帧是否由准确首帧增量编辑而来，并检查画布、比例、来源哈希与背景连续性
- `scripts/run_seedance_scene.py`：一条命令执行提交、轮询和下载
- `references/popup-tool-contract.md`：宿主侧 `show_select_popup` 函数调用协议、回传格式与等待状态规则
- `references/workflow.md`：端到端流程、交付物和质量关卡
- `references/style-guide.md`：源风格的视觉、运动和声音拆解
- `references/remotion-build.md`：图层顺序、运动系统、道具控制和渲染交接的实现指导
- `references/vox-broll-sequence.md`：从 Empire Downfall 套件提炼出的、旁白驱动的多场景编辑语法
- `references/vox-motion-contract.md`：Vox 场景的独立背景、主体占比、资产数量、逐元素运动参数和叙事出现顺序硬规范
- `references/asset-provenance-contract.md`：imagegen 实际调用、原始输出、逐资产 prompt、回执、哈希和禁止本地绘图降级的来源规范
- `references/scene-archetypes.md`：可复用的 Vox 风格编辑型序列场景模块模式
- `references/video-model-collage-reference.md`：面向 Seedance 首尾帧路线的 Vox mixed-media 视频风格参考
- `references/edge-tts-voiceover.md`：Edge 在线 TTS、SRT 时间轴和远程服务接入边界
- `references/script-standards.md`：脚本写作、时长换算、beat 拆分、结尾钩子与旁白约束
- `references/prompt-recipes.md`：图片、关键帧视频、缩略图和 `motion_intent` 的标准提示词模板
- `references/seedance-motion-contract.md`：视频模型的固定对象、进场对象、路径绘制、动作预算和禁止变形契约
- `references/vox-style-migration.md`：从 `vox-motion-graphics.skill` 迁入的 Mixed Media 视觉语法、镜头能量与脚本节奏
- `references/output-contract.md`：输入缺省、输出 schema、分流矩阵与可验收 gate 的硬规范
- `references/golden-example.md`：一份从原始需求到 `SEEDANCE_SCENE.json` 的端到端金标准样例
