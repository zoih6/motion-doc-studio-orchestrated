# Motion-Doc Studio — Orchestrated Agent Entry Point

هذا الملف هو نقطة الدخول الوحيدة لأي وكيل يعمل على النظام. لا تبدأ ببناء فيديو أو توليد أصل قبل المرور على `skills/motion-system-orchestrator/SKILL.md`.

## ترتيب القراءة الإلزامي

1. `skills/motion-system-orchestrator/SKILL.md` — التوجيه والبوابات وإدارة الحالة.
2. `workflow/00_system_intake.md` — أسئلة المستخدم وتثبيت القيود.
3. `workflow/12_safe_execution.md` — الذاكرة، القرص، المهام الطويلة، السجل والاستئناف.
4. `workflow/13_github_delivery.md` — اللقطات، الفروع، الرفع الآمن وعدم تسريب الأسرار.
5. المهارة المتخصصة المطلوبة فقط:
   - الإنتاج الأساسي: `skills/motion-director/` ثم `skills/motion-doc-studio/`.
   - الصوت: `skills/motion-sound-layer/`.
   - مرجع فيديو: `workflow/09_reference_dna.md`.
   - Remotion: `resources/integrations/remotion-dev-skills/`.
   - Paper collage: `resources/integrations/paper-collage-video/`.
   - Vox orchestration: `resources/integrations/vox-motion-graphics/`.

## قواعد لا تقبل التجاوز

- خطط ثم نفّذ ثم تحقق؛ لا تعمل عشوائيًا ولا تعِد المهمة لمجرد بطئها.
- ابدأ بجولة أسئلة واحدة قصيرة، ثم أعد صياغة الطلب وأظهر خطة إنتاج قبل التنفيذ المكلف.
- المراجع تعلّم القواعد البصرية والحركية، ولا تُنسخ اللقطات أو التكوينات أو النصوص حرفيًا.
- لا تستخدم صورة أو انتقالًا كحل تلقائي. لكل مشهد أطروحة بصرية وتغير حالة واضح ومسار طبقات/كاميرا.
- استخدم `tools/preflight_system.py` قبل كل مهمة ثقيلة، و`tools/run_logged.sh` لكل أمر طويل، و`tools/checkpoint.sh` بعد كل مرحلة.
- لا تضع الأسرار في الملفات أو Git أو السجلات. لا تحذف بيانات اعتماد موجودة تلقائيًا؛ اترك إدارتها للبيئة/مدير الأسرار.
- لا تدّعِ الجاهزية النهائية قبل فحوصات تقنية ومراجعة تحريرية موثقة.

المواد المرجعية المضمنة محفوظة في `resources/integrations/` مع تراخيصها وبصمات إصداراتها.