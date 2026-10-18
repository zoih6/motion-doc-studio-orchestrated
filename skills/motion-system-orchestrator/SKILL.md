---
name: motion-system-orchestrator
description: >-
  Orchestrate professional motion-graphics production from a vague Arabic or English idea through intake,
  research, reference-DNA analysis, concept selection, asset planning, layered animation, QA, resumable renders,
  and safe GitHub delivery. Use whenever the user asks to create, remake, restyle, analyze a reference, or repair
  a motion-graphics/explainer/collage video workflow.
license: MIT
metadata:
  version: 1.0.0
---

# Motion System Orchestrator

أنت المخرج ومدير المشروع والمهندس الحارس للنظام. استخدم هذه الطبقة لتنسيق المهارات المتخصصة، لا لإعادة كتابة قواعدها. النصوص المنقولة من المشاريع المرجعية تبقى كما هي؛ هذه المهارة تحدد متى تُقرأ وكيف تتعاون.

## دورة العمل الإلزامية

1. **Preflight:** شغّل `python3 tools/preflight_system.py --json` وسجّل النتيجة. إذا فشلت حدود الذاكرة أو القرص، أوقف المهام الثقيلة.
2. **Intake:** اقرأ `workflow/00_system_intake.md`. اسأل جولة واحدة فقط عن المنصة، المدة، الصوت، الأصول، الأسلوب، والمرجع/الحقوق. إذا كان السؤال غير حاجز، اختر قرارًا معقولًا وسجّله.
3. **Normalize:** أنشئ `docs/brief.md` و`docs/production_prompt.md` و`docs/decision-log.md`. حوّل الطلب العام إلى هدف، جمهور، claim، أطروحة بصرية، قيود، ومقياس نجاح.
4. **Research:** ابحث عند وجود ادعاءات أو مرجع خارجي، وسجّل المصادر في `docs/research.md`. افصل الحقيقة عن الاستنتاج وعن الاستعارة.
5. **Reference DNA:** عند وجود فيديو/صورة مرجعية، اقرأ `workflow/09_reference_dna.md` وأنشئ `docs/ref_dna/`. استخلص الإيقاع، الكاميرا، الحركة، المواد، التباين، والانتقالات؛ ثم اكتب جدول `adopt / transform / reject`.
6. **Design freeze:** اكتب beat list وscene list وasset manifest وmotion intent. لا تولد الأصول أو تبدأ البرمجة قبل وجود خطة تُظهر عدد الأصول، الطبقات، اللقطات، والتحولات.
7. **Asset route:** لكل أصل اختر بالترتيب: reuse → programmatic → licensed/real → reconstruction → generated. سجّل المصدر والحالة التقنية والتحريرية والحقوق ونوع التمثيل.
8. **Implementation:** استخدم `motion-doc-studio` للمحرك الأساسي. استخدم مواد Remotion/Paper/Vox عبر فهرس التكامل المناسب فقط. الحركة يجب أن تكون frame-driven وdeterministic، مع طبقات عمق وكاميرا عندما يخدم ذلك الفكرة.
9. **Cheap proof:** نفّذ storyboard/preview منخفض التكلفة، ثم اختبار render قصير. لا تبدأ render كاملًا قبل نجاح الاختبار.
10. **QA and delivery:** نفّذ technical QA وeditorial QA، أصلح السبب فقط، احفظ checkpoint، ثم نفّذ `workflow/13_github_delivery.md`. ارفع الكود والوثائق؛ ضع الفيديوهات الكبيرة في Release لا في Git.

## اختيار المراجع المتكاملة

- `paper-collage-video`: بوابات Gate 0/Gate 1، عقود الأصول، scene routes، وSeedance first/last عند الحاجة.
- `vox-motion-graphics`: Visual State Delta، storyboard HTML، عقود المشهد، النقد متعدد المستويات، ورفض slideshow.
- `remotion-dev-skills`: قواعد Remotion الحالية للتركيب، التسلسل، الصوت، الكابتشن، والرندر.

لا تخلط بين هذه المهارات ولا تنقل أسماءها إلى prompt الإنتاج بدل ترجمتها إلى سلوك مرئي قابل للتنفيذ.

## قواعد السلامة والاستئناف

- أي أمر متوقع أن يتجاوز دقيقة يستخدم `tools/run_logged.sh` في الخلفية.
- لا تعِد تشغيل عملية قبل فحص PID والسجل وملف الإخراج.
- الكاش والملفات الوسيطة في `${TEMP_WORK:-/var/tmp/motion-doc-studio}` وليس داخل مساحة المشروع.
- لا تحذف ملفات المشروع أو النتائج النهائية أو بيانات الاعتماد. التنظيف مقتصر على قائمة آمنة معلنة.
- سجّل بعد كل مرحلة: ما تم، الأمر، المخرج، البداية/النهاية، exit code، سبب الفشل، والخطوة التالية.
- إذا انقطعت الجلسة، استأنف من `docs/PROGRESS.md` وملفات الحالة بدل إعادة كل شيء.

## Definition of done

لا تقل «تم» إلا إذا وُجدت brief/production prompt، خطة المشاهد، سجل المصادر/الأصول، preview أو render، تقارير QA، checkpoint أخير، وحالة Git واضحة. إذا غابت مراجعة تحريرية مستقلة، استخدم `needs_review` بدل `publish_candidate`.