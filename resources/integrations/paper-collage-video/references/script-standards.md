# 脚本创作标准

## 用途

这份标准用于把用户给的故事、口播稿、需求描述，整理成适合 paper collage explainer 的 narration。

目标不是写“文学化旁白”，而是写：

- calm
- precise
- documentary
- 可拆成 beat
- 可直接转成分镜和图像 prompt

## House Rule

- 默认不要使用 em dash
- 优先使用逗号、冒号、括号、短横线或正常断句

## 标题标准

标题要是 declarative 或 interrogative，不要 clickbait。

推荐形状：

- `How [event] Unfolded`
- `The Hunt for [target]`
- `The [adjective] Story of [subject]`
- `Why [place] [did X]`
- `[Event] Explained`
- `The Man/Woman Who [impossible act]`
- `What Really Happened to [subject]`

每个标题至少带一个具体钩子：

- 日期
- 人名
- 地点
- 数字

## 时长换算

默认按 `2.5 words per second` 估算。

- `30s` 约 `75` 词
- `1 min` 约 `150` 词
- `2 min` 约 `300` 词
- `3 min` 约 `450` 词
- `5 min` 约 `750` 词

允许误差控制在 `5%` 内。

如果用户提供真实音频，优先按音频时长，而不是估词数。

## 开头标准

冷开场优先在前 `3-4` 句内完成，约 `30-40` 词。

必须尽量包含：

- 一个明确日期
- 一个具体地点
- 一个小而具体的动作

不要：

- “想象一下”
- 空泛提问
- 长铺垫

理想感觉是：故事直接在一个时刻里发生了。

## 语气与节奏

- 平静、精确、克制
- 多用短 declarative 句
- 每一小段允许一条稍长的解释句调节节奏
- 不要对观众喊话
- 不要过度情绪化
- 张力来自事实排列，而不是形容词堆砌

## 连接词系统

优先使用时间和因果连接，让句子彼此推动：

- then
- by morning
- three days later
- within the hour
- because of this
- which meant
- what nobody knew was

这样后续拆 beat 时，画面会更像因果推进，而不是并排信息点。

## 句子纪律

- 每句只表达一个主要视觉 idea
- 每句必须能被看见、被画出来、被拆成 beat
- 每句正常收于句号

如果一条句子无法被清楚可视化，就重写。

长句可以按自然逗号或从句拆成两个 beat。

## 准确性与克制

- 不编造日期、人名、金额、地点
- 有争议的细节用更安全的写法绕开
- 真实悲剧题材避免 gore、受害者特写、猎奇
- 紧张感放在对象、地点、文件、天气、时间、后果上

## 结尾钩子

结尾最后一行优先控制在 `12` 词以内，最好停在：

- 一个名词
- 一个名字
- 一个日期
- 一个简短 declarative

可复用的结尾模式：

1. `未解之物`
   例：落在仍未找到的东西上。
2. `跳到后来的日期`
   例：用一个更晚的年份重新打开事件。
3. `缺失的一块`
   例：点出调查者始终没拿到的那一项。
4. `安静的矛盾`
   例：一句事实，反过来推翻前面的理解。
5. `代价线`
   例：平静说出人或钱的代价。

## Beat 拆分标准

默认每个 beat：

- `2-3` 秒
- 大约 `5-8` 个词
- 一个视觉 idea

数量参考：

- `30s`：`12-15` beats
- `1 min`：`22-30` beats
- `2 min`：`45-60` beats
- `3 min`：`70-90` beats
- `5 min`：`115-150` beats

时间码计算可以按累计词数除以 `2.5`。

## Beat 到 scene 的归并

不是每个 beat 都要单独做一个 scene。

归并原则：

- 如果多个 beat 属于一个稳定视觉想法，可以放到同一 scene
- 如果旁白突然切到新人物、新地点、新证据、新图表，再切 scene
- 如果 scene 内元素过多、运动过多，再标记为 `seedance`

## 适配当前 skill 的落地规则

在 `paper-collage-video` 里，脚本整理后的结果至少要能支持：

- `beat list`
- `scene list`
- `storyboard`
- `motion_intent`
- `route hint`

也就是脚本不是终点，而是后续素材、关键帧、视频 prompt 的上游结构。

## 内容提取示例

下面这个例子，展示如何把用户原始需求抽成当前 skill 真正需要的上游结构。

### 用户原始输入

```text
我想做一个 35 秒左右的拼贴解说视频，讲 1971 年一个男子劫持飞机后跳伞失踪，最后一直没找到。风格偏档案、调查、地图、证据墙，旁白是平静纪录片口吻，横版，要带配乐但不要把旁白烘进去。
```

### 提取后的生产信息

```yaml
topic: 1971 hijacking disappearance case
format: vo-sequence
aspect_ratio: 16:9
audio_mode: full-mix
total_duration_rule: user-specified
total_duration_seconds: 35
scene_duration_policy: auto-by-content
style_family:
  - vox mixed-media editorial collage
  - archival desk
  - evidence wall
  - map tracking
tone:
  - calm
  - precise
  - documentary
required_visuals:
  - hijacker note
  - airplane / boarding context
  - cash bundle
  - parachute
  - search map
  - evidence-board relationship view
likely_scene_routes:
  - scene_01: remotion
  - scene_02: remotion
  - scene_03: seedance
  - scene_04: remotion
ending_hook: the missing parachute / the object never found
```

### 为什么这样提取

- 用户说“故事”，我们要补成 `scene list`
- 用户说“平静纪录片口吻”，我们要补成脚本语气约束
- 用户说“地图、证据墙”，我们要补成可执行的视觉家族
- 用户说“35 秒左右”，我们要补成可拆 beat 的目标时长
- 用户没有说 scene route，我们要先代判哪些 scene 适合 `remotion`，哪些该升级到 `seedance`

## 内容优化示例

### 原始口语化描述

```text
这个男的劫机以后拿了钱就跳伞跑了，警方找了很久也没找到，所以这个案子后来特别传奇。
```

### 优化后的纪录片旁白

```text
On November 24, 1971, a man boarded a Northwest Orient flight with a black briefcase.
By the time the plane landed in Seattle, he had demanded $200,000 and four parachutes.
That night, somewhere over the Pacific Northwest, he jumped into the dark and disappeared.
Search crews found scraps, rumors, and one small trail of cash.
They never found the parachute that should have told the whole story.
```

### 为什么这个版本更适合当前 skill

- 开头前两句就交代日期、地点语境和动作
- 每句都是一个清楚的视觉 idea
- 句长适合继续拆成 beat
- 最后落在“没找到的物件”，天然适合作为结尾钩子

## Beat 拆分示例

基于上面的优化版本，可以继续拆成：

```yaml
- beat: 01
  line: "On November 24, 1971"
  visual: date strip + ticket counter context
  route_hint: remotion
- beat: 02
  line: "a man boarded a Northwest Orient flight"
  visual: halftone cutout of man + aircraft label
  route_hint: remotion
- beat: 03
  line: "he demanded $200,000 and four parachutes"
  visual: ransom note + cash + parachute evidence tableau
  route_hint: seedance
- beat: 04
  line: "he jumped into the dark and disappeared"
  visual: night plane door + falling silhouette over map void
  route_hint: remotion
- beat: 05
  line: "They never found the parachute"
  visual: evidence board ending on missing object
  route_hint: seedance
```

这个示例的关键不是题材本身，而是：脚本必须天然长成可以继续推到 `beat -> scene -> prompt -> motion_intent` 的结构。
