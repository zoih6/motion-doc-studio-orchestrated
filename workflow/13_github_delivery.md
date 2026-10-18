# 13 — Safe GitHub Delivery

## مبدأ النسخ

هذه النسخة تُدار كمستودع مستقل. كل مرحلة مهمة تُحفظ في commit، وكل تغيير كبير في فرع أو tag واضح.

## الأسرار

لا تكتب PAT أو `GH_TOKEN` في الملفات أو prompts أو logs أو Git. استخدم اعتماد GitHub الموجود في البيئة أو مدير أسرار النظام. لا تحذف اعتمادًا موجودًا تلقائيًا؛ لا تغيّر إعداداته إلا بطلب صريح. «الاحتفاظ» يعني تركه في مخزن الاعتماد، لا نسخه إلى المشروع.

افحص قبل commit:

```bash
git diff --check
git status --short
grep -RInE 'gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+|AKIA[0-9A-Z]{16}' --exclude-dir=.git . || true
```

إذا ظهر secret، أوقف الرفع، أزله من التاريخ/الملف، واطلب تدويره عند الحاجة.

## دورة الرفع

```bash
git add -A
git diff --cached --check
git commit -m "stage: describe completed stage"
git push -u origin main
```

أنشئ المستودع الجديد خاصًا افتراضيًا باستخدام `gh repo create ... --private`، ولا ترفع ملفات الفيديو الكبيرة إلى Git؛ استخدم GitHub Release أو تخزينًا خارجيًا بعد التحقق.

## سجل التسليم

احفظ `docs/PROGRESS.md` و`docs/decision-log.md` و`docs/source-manifest.md`. اذكر commit، الملفات الرئيسية، الفحوصات، وماذا يفعل الوكيل لاحقًا. لا تدّعِ أن الرفع تم قبل فحص `git status` و`gh repo view`.