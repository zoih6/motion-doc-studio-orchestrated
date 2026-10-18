# Plugin Structure

هذه هي البنية التي يجب أن يراها الوكيل والمنصة:

```text
AGENTS.md                         # نقطة الدخول العامة
START.md                          # الرابط الذي يرسله المستخدم للوكيل
INSTALL.md                        # تعليمات التثبيت
install.sh                        # مثبت عام
.claude-plugin/plugin.json       # Claude plugin manifest
.claude-plugin/marketplace.json  # Claude marketplace entry
.codex-plugin/plugin.json        # Codex plugin manifest
.agents/plugins/marketplace.json # Agent marketplace entry
gemini-extension.json            # Gemini extension metadata
skills/
  motion-system-orchestrator/SKILL.md  # الراوتر والبوابات
  motion-director/SKILL.md             # intake والتطوير الإبداعي
  motion-doc-studio/SKILL.md            # التنفيذ الأساسي
  motion-sound-layer/SKILL.md           # الصوت والـ QA
workflow/                         # إجراءات التشغيل المرحلية
tools/                            # فحص البيئة والرندر والاستئناف
resources/integrations/            # snapshots مرجعية غير معدلة
```

الـ Plugin لا يعتمد على README لتشغيل الوكيل. `START.md` هو رابط التشغيل، و`AGENTS.md` هو عقد القراءة داخل المستودع، وملفات manifests هي ما تستخدمه أدوات الـ Plugin.
