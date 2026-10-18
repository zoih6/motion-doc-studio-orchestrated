# paper-collage-video

面向 Codex 的纸艺拼贴视频 Skill。它把故事、口播稿、音频或制作需求拆成可验收的分镜，并通过 `remotion-code` 或 `video-model` 两条路线制作 Vox mixed-media 风格的视频。

[![示例视频预览](docs/media/frame-001.png)](docs/media/final.mp4)

点击预览图可查看仓库中的 [示例成片](docs/media/final.mp4)。示例图片、视频与项目文档来自 `0720-remake/project` 的实际产出。

## 核心能力

- 把故事、旁白或需求拆成 beat、Scene、时长和出现顺序
- 通过 Gate 0 检查环境、插件、脚本、密钥和依赖
- 通过 Gate 1 锁定制作模式、画幅和音频方案
- 默认采用明亮、清晰、多彩的 `vox-mixed-media` 视觉语言
- `remotion-code`：Imagegen 生成独立栅格素材，Remotion 只负责分层、排版和动画
- `video-model`：Imagegen 生成首帧，并基于首帧编辑尾帧，再由 Seedance 生成视频
- 使用 Edge TTS 生成普通话男声配音和 SRT，并按 SRT 拆 Scene
- 对资产来源、构图、碰撞、画面重复、首尾帧连续性和最终输出执行机器校验
- Remotion 项目复用共享依赖和浏览器缓存，不再为每个项目重复安装依赖或下载 Headless Chrome

## 两条制作路线

### Remotion Code

适合元素可拆分、需要精确控制排版和运动的 Scene。

- 每个 Scene 使用独立背景和 4-8 个经过批准的栅格素材
- 至少 3 个非背景元素具有独立时间和运动
- 所有新增可见图片素材由 Imagegen 生成
- 禁止 SVG、内联 SVG、Canvas、Pillow 或 CSS 绘制主要视觉资产
- Remotion 负责入场、内容动作、遮挡、视差、停驻和镜头组织
- 元素按旁白首次出现或因果顺序进入画面

### Video Model

适合元素很多、多个对象需要复杂独立运动，或更适合整张拼贴画面运动的 Scene。

- 默认模型：`doubao-seedance-1-5-pro-251215`
- 每个 Scene 按内容自动分配 `4-12s`
- 首帧是唯一的空镜或近空镜背景母版
- 尾帧必须由 Imagegen 编辑准确的首帧生成，禁止单独文生图
- 首帧必须先通过 Gate 1 画幅与目标画布检查，才能生成尾帧
- 首尾帧保持相同画布、裁切、镜头、背景几何和固定物体
- 只有声明在 `change_regions` 中的新增元素可以变化
- 图片以本地 Base64 提交，无需公网图床
- 提交前自动执行关键帧来源、尺寸、比例、哈希和背景连续性校验

## 安装

```bash
git clone https://github.com/Cliff007007/paper-collage-video.git \
  ~/.codex/skills/paper-collage-video

cd ~/.codex/skills/paper-collage-video
cp .env.example .env
```

在本地 `.env` 中填写火山引擎 Ark API Key：

```bash
ARK_API_KEY=your_private_key_here
```

## 使用流程

调用 Skill 时，用户通常只需要提供以下任一种输入：

- 一个故事
- 一段口播稿
- 一个内容音频文件
- 一段视频制作需求

Skill 会先执行 Gate，不应直接生成项目：

1. `Gate 0`：检查 `.env`、Ark Key、Imagegen、Remotion、Node、npm、FFmpeg、Pillow、Edge TTS 和内部校验脚本。
2. `Gate 1`：让用户选择 `remotion-code / video-model`、`16:9 / 9:16`；没有源音频时选择是否生成配音。
3. `Voiceover Gate`：需要配音时，使用 `zh-CN-YunjianNeural` 生成 MP3 和 SRT。
4. 根据音频、SRT 或内容自动确定总时长，并按语义拆 Scene。
5. 锁定脚本、视觉隐喻、构图蓝图、资产清单和运动契约。
6. 生成资产、实现动画、执行 Gate、渲染和验收。

运行环境自检：

```bash
python3 scripts/preflight.py
```

需要配音时运行严格检查：

```bash
python3 scripts/preflight.py --require-edge-tts
```

## 创建项目骨架

下面的命令只负责创建规范化项目，不会绕过 Gate 1 替用户做选择：

```bash
python3 scripts/bootstrap_collage_video.py \
  --output ./my-collage-video \
  --mode vo-sequence \
  --production-mode remotion-code \
  --scene "一段关于边际效用的 Vox 拼贴解说" \
  --duration 18 \
  --duration-source estimated \
  --aspect-ratio 16:9 \
  --style-family vox-mixed-media \
  --audio-mode no-audio \
  --gate1-source user-selection \
  --with-remotion-template
```

实际参数以脚本帮助为准：

```bash
python3 scripts/bootstrap_collage_video.py --help
```

## 配音

```bash
python3 scripts/generate_edge_voiceover.py \
  --project ./my-collage-video \
  --text-file ./my-collage-video/00_brief/narration.txt
```

固定输出：

- `04_audio/voiceover.mp3`
- `04_audio/voiceover.srt`
- `04_audio/voiceover-metadata.json`

最终视频可通过 `scripts/mux_voiceover.py` 与配音合成。

## Seedance 首尾帧

每个 Video Model Scene 必须遵循同一画布的两状态原则：

1. 使用 Imagegen 生成 `first-frame.png`。
2. 使用 `view_image` 检查首帧。
3. 调用 Imagegen 编辑模式，将首帧本地路径作为唯一 `referenced_image_paths`。
4. 只在批准的 `change_regions` 内加入尾帧元素并保存为 `last-frame.png`。
5. 在 `SEEDANCE_SCENE.json` 中填写工具回执、输入输出哈希和连续性审计。
6. 通过关键帧 Gate 后才能提交。

```bash
python3 scripts/validate_seedance_keyframes.py \
  --project ./my-collage-video \
  --scene-spec ./my-collage-video/03_animation/SEEDANCE_SCENE.json

python3 scripts/run_seedance_scene.py \
  --project ./my-collage-video \
  --scene-spec ./my-collage-video/03_animation/SEEDANCE_SCENE.json
```

`run_seedance_scene.py` 和底层提交器也会再次执行连续性 Gate，不能通过直接调用提交脚本绕过。

## 质量关卡

- `validate_composition_blueprint.py`：检查 Scene 构图、阅读路径、颜色脚本和布局多样性
- `validate_collage_project.py`：检查项目结构、资产来源、禁止 SVG、运动字段和锁定状态
- `extract_layout_audit.py`：从渲染视频抽帧，检查主体尺寸、碰撞、遮挡和安全边距
- `validate_seedance_first_frame.py`：在尾帧生成前检查首帧是否符合 Gate 1 画幅与目标画布
- `validate_seedance_keyframes.py`：检查首尾帧尺寸、比例、编辑来源、哈希和背景连续性
- `finalize_remotion_render.py`：只有人工查看联系表并提交有效审核回执后，才允许生成最终成片
- `verify_remotion_output.py`：使用 FFprobe 检查最终分辨率、帧率、时长和音轨契约

详细输出结构和验收标准见 [output-contract.md](references/output-contract.md) 与 [golden-example.md](references/golden-example.md)。

## 示例项目

仓库保留了 `0720-remake` 的项目节选：

- [项目说明](examples/0720-remake/README.md)
- [项目 Brief](examples/0720-remake/00_brief/project-brief.md)
- [分镜板](examples/0720-remake/01_storyboard/storyboard.md)
- [Scene 规划](examples/0720-remake/06_sequence/scene-plan.md)
- [项目配置](examples/0720-remake/project-config.json)

![0720 remake contact sheet](docs/media/contact-sheet.png)

![Frame 001](docs/media/frame-001.png)
![Frame 003](docs/media/frame-003.png)
![Frame 005](docs/media/frame-005.png)

## 仓库结构

```text
paper-collage-video/
├── SKILL.md
├── README.md
├── agents/
├── docs/media/
├── examples/0720-remake/
├── references/
├── scripts/
├── requirements-voiceover.txt
└── .env.example
```
