# Motion-Doc Studio

حزمة Skills وأدوات لإنتاج فيديوهات الموشن جرافيك، تبدأ من فكرة المستخدم ثم تمر بالاستلام، البحث، التخطيط، التنفيذ، الفحص، والتسليم.

## الرابط الذي ترسله للوكيل

انسخ هذا الرابط وأرسله كما هو لأي وكيل برمجي:

```text
https://raw.githubusercontent.com/zoih6/motion-doc-studio-orchestrated/main/START.md
```

وقل له: «اقرأ الرابط ونفّذ التعليمات حرفيًا. لا تبدأ الإنتاج قبل أسئلة الـ intake». هذا الرابط هو نقطة التشغيل الرسمية، وليس رابط README.

للتثبيت فقط استخدم:

```text
https://raw.githubusercontent.com/zoih6/motion-doc-studio-orchestrated/main/INSTALL.md
```

أو عبر الطرفية:

```bash
curl -fsSL https://raw.githubusercontent.com/zoih6/motion-doc-studio-orchestrated/main/install.sh | bash
```

## البنية الفعلية

يبدأ كل وكيل من `AGENTS.md` ثم يقرأ `skills/motion-system-orchestrator/SKILL.md`. هذه هي طبقة التوجيه التي تمنع الدوران، وتحدد بوابة الأسئلة، والبحث، وتحليل DNA، وتخطيط الأصول، والتنفيذ، والـ QA، والاستئناف. بعدها تُستدعى المهارة المتخصصة: `motion-director`، أو `motion-doc-studio`، أو `motion-sound-layer`.

ملفات `.claude-plugin/` و`.codex-plugin/` و`.agents/plugins/` هي manifests للتكامل مع Plugins، و`gemini-extension.json` يعرّف امتداد Gemini. أداة `install.sh` تثبت الـ orchestrator والمهارات الثلاث الأخرى، وتضع نسخة الاستوديو في `~/.motion-doc-studio-orchestrated`.

المجلد `resources/integrations/` يحتوي snapshots غير معدلة من Paper Collage وVox Motion وRemotion Skills. أما قواعد الدمج نفسها ففي `skills/motion-system-orchestrator/` و`workflow/`.

## تحقق سريع

```bash
python3 tools/preflight_system.py --json
python3 tools/validate_system.py
```

لا تُحفظ مفاتيح GitHub أو الأسرار داخل هذا المستودع.
