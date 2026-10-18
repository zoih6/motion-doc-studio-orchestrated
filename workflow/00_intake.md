# 00 · Intake: the Creative Director turns a messy idea into a pro brief

> Skill: `skills/motion-director/SKILL.md` (run it first on every new project) · sub-agent: `agents/creative-director.md`
> Output: `docs/brief.md`, `docs/production_prompt.md`, `docs/research.md`, plus one user confirmation.

The user should never have to write a prompt. They send an idea in any form (one sentence, dialect, typos, a voice
note, a poem, a picture). **You** do the prompt engineering.

## Flow
```
idea (messy) → 1 understand → 2 ONE question round (options + defaults) → 3 research → 4 3 concepts → pick
            → 5 production prompt + brief → 6 short confirmation (user's language) → hand off to the pipeline
```

## 1 · Understand (silently)
| extract | how | default when missing |
|---|---|---|
| topic / intent / emotion | the verbs and adjectives the user used; the occasion | inform + warmth |
| video type | doc/explainer · kinetic text/lyrics · reel/ad · logo/intro (table in the skill) | explainer |
| platform → aspect | انستا/تيك توك/شورتس → 9:16; يوتيوب → 16:9; واتساب ستاتس → 9:16 | ask (Q2) |
| language / dialect | the user's own writing; Yemeni/Gulf/Egyptian/Levantine/MSA | same as the user's |
| assets attached | audio → VO or song? images → references or footage? | none |
| standing rules | "no slideshow", "sample first", "keep workspace clean"… | record verbatim |

## 2 · One question round
Ask at most 6 questions, each with options and a ★ recommended default. Use the agent's choice UI when available.
Skip any question the input already answers.

**Arabic template** (adapt the options to the topic; the 3 styles are *your* proposals):
1. **المدة؟** ◦ ١٥ ثانية ◦ ٣٠ ثانية ◦ ★ ٦٠ ثانية ◦ ٢–٣ دقائق ◦ أخرى
2. **مقاس الفيديو؟** ◦ ★ طولي 9:16 (ريلز/تيك توك) ◦ أفقي 16:9 (يوتيوب) ◦ مربع 1:1 ◦ 4:5
3. **الصوت/التعليق؟** ◦ عندي ملف صوتي ◦ ★ نولّد تعليقًا صوتيًا (رجالي/نسائي، باللهجة …) ◦ بدون صوت: موسيقى + نص على الشاشة ◦ تسجيل أغنية/قصيدة نزامن عليه الكلمات
4. **الصور؟** ◦ عندي صور/لقطات سأرسلها ◦ ★ نولّد صورًا بالذكاء الاصطناعي ◦ مصادر أرشيفية حقيقية ◦ موشن جرافيك وخطوط فقط بدون صور
5. **الموسيقى والمؤثرات؟** ◦ ★ مؤثرات وموسيقى حقيقية CC0 مضبوطة على الحركة ◦ عندي موسيقى ◦ بدون
6. **الأسلوب؟** ◦ (اقتراح ١: الاسم — المزاج) ◦ (اقتراح ٢) ◦ (اقتراح ٣) ◦ فاجئني

Conditional: «الصق النص/الكلمات بالضبط» (kinetic), «اسم العلامة والشعار والألوان؟» (ads), «أرفع على GitHub؟ (اسم
المستودع + رمز PAT)», «عينة أولًا؟» (default yes for > 30 s).

**English template:** Duration? · Aspect? · Voice (mine / generate ★ / none / song) · Images (mine / generate ★ /
archival / none) · Music (CC0 measured ★ / mine / none) · Style (3 proposals / surprise me).

## 3 · Research
Use web search/fetch if the agent has it; otherwise say so. Verify names, dates, numbers and quotes that will
appear on screen, and gather 3–5 visual references (describe them; never copy). For lyrics, keep the exact text and
mark the long vowels (kashida candidates) and the emotional key word (the accent colour). Write `docs/research.md`
with sources.

## 4 · Three concepts → pick one
For each: **title · logline · core visual metaphor · motion persona · style preset · hook (0–2 s) · ending beat**.
Choose by originality × fit (emotion/platform) × feasibility (assets, tools, time). The metaphor must come from the
topic's meaning, e.g. the coffee bean's journey as one travelling line that ends as steam writing «موكا».

## 5 · Production prompt (`docs/production_prompt.md`)
Structure (fill every line; be concrete: seconds, px, hex, font families, move names):
```
ROLE & BAR      You are … ; the film must look like a top-tier studio piece; QA gates in rules/qa_checklist.md
INTENT          one sentence            AUDIENCE/PLATFORM  …            EMOTION ARC  start → peak → end
TAKEAWAY        the ONE thing viewers remember
FORMAT          duration · aspect (px) · 30 fps · language/dialect · RTL
VOICE           provided file | generated (voice, dialect, pace 130–150 wpm) | none | song  + the approved script
VISUAL SYSTEM   style preset · palette (hex, ONE accent) · display + UI font · surfaces/light · asset plan (provided/generated/sourced)
MOTION GRAMMAR  persona · 6–9 signature moves (library/motion_recipes.md, library/kinetic_type_motion.md) · transition family
STRUCTURE       hook 0–2 s → beats with timecodes (new idea every 2–4 s) → payoff/CTA
ON-SCREEN TEXT  exact, proofread, per beat
SOUND           motion-sound-layer plan (families, hero moments) · music source · −14 LUFS
DELIVERABLES    final_1080p.mp4 (+720p), poster.jpg, contact.jpg, GitHub release
CONSTRAINTS     user's standing rules verbatim · banned list (rules/motion_rules.md, kinetic §10)
ASSUMPTIONS     what you decided for the user
SUCCESS         legibility ≥ 34 px · hook ≤ 2 s · ≥ 3 critique rounds · qa.py 0 FAIL · duration = audio
```

## 6 · Confirm, then hand off
A 6–10 line message in the user's language: title + logline · format · 3–5 structure bullets · style · generated vs
provided · time estimate (render: `workflow/11_render_speed.md`) · «موافق؟ أو عدّل ما تريد». Wait. Then:
- documentary / explainer / reel → `tools/new_film.sh <dir> [--aspect 9:16]` → workflow 01 → 08 (sample first);
- kinetic text / lyrics → `tools/new_film.sh <dir> --kinetic --aspect 9:16` → `library/kinetic_type_motion.md`;
- sound for any film → `skills/motion-sound-layer`.

## Reference material from the user
- Images → `docs/reference_analysis.md`: palette (hex), surfaces, light, type mood, density, what to adopt and what *not* to copy.
- Videos → `workflow/09_reference_dna.md` + `tools/video_dna.py` (example: `examples/reference_dna/kinetic_lyrics/DNA.md`).
The user wants the **style and grammar**, never a copy of the frames.
