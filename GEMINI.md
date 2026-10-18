# Motion-Doc Studio (Gemini CLI context)

Motion-Doc Studio is installed. When the user asks for a motion-graphics, explainer, documentary or "VOX-style"
video, a reel, a remake/restyle, or sound design for a motion video:

0. New project or a raw idea → activate `motion-director` first (intake, research, production prompt; `START.md`).
1. Activate the skill `motion-doc-studio` (`skills/motion-doc-studio/SKILL.md`). It is canonical. For sound, activate
   `motion-sound-layer` (`skills/motion-sound-layer/SKILL.md` + its verbatim `PROMPT.md`).
2. Locate the studio root with `bash skills/motion-doc-studio/scripts/studio.sh` (inside the extension:
   `${extensionPath}`). Every path in the skills (`rules/`, `workflow/`, `engine/`, `tools/`, `vendor/`) is relative to it.
3. Follow `AGENTS.md` for the read order and operating mode. Talk to the user in their language.
