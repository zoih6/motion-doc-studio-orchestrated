# Install Motion-Doc Studio Orchestrated v4

هذا الملف مخصص للوكيل البرمجي. شغّل الأوامر بنفسك، ثم اقرأ `START.md` وابدأ intake.

## التثبيت العام

```bash
curl -fsSL https://raw.githubusercontent.com/zoih6/motion-doc-studio-orchestrated/main/install.sh | bash
```

المثبت ينسخ المستودع إلى `~/.motion-doc-studio-orchestrated` ويثبت أربع Skills: `motion-system-orchestrator`، `motion-director`، `motion-doc-studio`، و`motion-sound-layer`. كما يثبت الاعتمادات عند توفر مدير الحزم. استخدم `MDS_DEPS=0` لتخطي الاعتمادات، أو `MDS_COPY=1` للنسخ بدل الروابط الرمزية.

## Claude Code

```bash
claude plugin marketplace add zoih6/motion-doc-studio-orchestrated
claude plugin install motion-doc-studio@motion-doc-studio
```

## Codex CLI

```bash
codex plugin marketplace add zoih6/motion-doc-studio-orchestrated
codex plugin add motion-doc-studio@motion-doc-studio
```

## Gemini CLI

```bash
gemini extensions install https://github.com/zoih6/motion-doc-studio-orchestrated
```

## Skills فقط

```bash
npx skills add zoih6/motion-doc-studio-orchestrated -g -y
```

## بعد التثبيت

تحقق من وجود:

```bash
ls ~/.motion-doc-studio-orchestrated/skills
# motion-system-orchestrator motion-director motion-doc-studio motion-sound-layer
node ~/.motion-doc-studio-orchestrated/tools/selftest.mjs
```

ثم اقرأ رابط التشغيل الرسمي:

```text
https://raw.githubusercontent.com/zoih6/motion-doc-studio-orchestrated/main/START.md
```
