# Popup Tool Contract

## Purpose

Use this contract when the host application supports Tool Call / Function Calling driven popups.

For `paper-collage-video`, do not ask plain-text multiple-choice questions for:

- `mode`
- `aspect_ratio`
- `audio_mode`

When the host supports structured tool calls, the skill should request these via a popup tool such as `show_select_popup`.

## Tool schema

Recommended function definition:

```json
{
  "type": "function",
  "function": {
    "name": "show_select_popup",
    "description": "Open a popup and let the user choose one or more options.",
    "parameters": {
      "type": "object",
      "required": ["title", "options"],
      "properties": {
        "title": {
          "type": "string",
          "description": "Popup title"
        },
        "hint": {
          "type": "string",
          "description": "Short explanation shown inside the popup"
        },
        "mode": {
          "type": "string",
          "enum": ["single", "multi"]
        },
        "options": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["key", "text"],
            "properties": {
              "key": {"type": "string"},
              "text": {"type": "string"}
            }
          }
        }
      }
    }
  }
}
```

## Required behavior

If popup tool support exists:

1. The skill must emit a tool call instead of a natural-language options list.
2. The host must intercept the tool call and render the popup UI locally.
3. The host must wait for the user selection.
4. The host must return the chosen value as a tool result.
5. Only then should the skill continue.

If popup tool support does not exist:

1. Fall back to a short plain-text options list.
2. Stop and wait for the user's reply.
3. Do not pretend a popup exists.
4. Do not replace the missing popup with automatic defaults.

## Tool result format

Recommended tool result:

```json
{
  "selected": ["option_key"]
}
```

For single-select flows, return one selected key in the array.
For multi-select flows, return multiple keys in the array.

## Host flow

Recommended sequence:

1. Codex decides a user choice is required.
2. Codex emits `show_select_popup`.
3. The host intercepts the tool call instead of forwarding it back as a normal model response.
4. The host renders the popup.
5. The user selects an option.
6. The host returns:

```json
{
  "role": "tool",
  "tool_call_id": "xxx",
  "name": "show_select_popup",
  "content": "{\"selected\":[\"option_key\"]}"
}
```

7. Codex resumes from the same workflow step.

## Skill-specific popup mapping

### `mode`

Use:

- `remotion-code`
- `video-model`

### `style_family`

Do not show a popup. Lock this field automatically to the skill's only supported value: `vox-mixed-media`.

### `aspect_ratio`

Use:

- `16:9`
- `9:16`

### `total_duration_rule`

Do not show a popup for this field. Lock it automatically using this priority order:

1. source audio -> `follow-source-audio`
2. `audio_mode=generate-voiceover` -> `follow-generated-voiceover`; fill the duration after TTS succeeds
3. an explicit whole-video runtime already present in the user's brief -> `user-specified`
4. otherwise -> `estimated-from-content`; estimate from content length and narration pace

### `scene_duration_policy`

Do not show a popup for this field. Lock `video-model` to `auto-by-content` and `remotion-code` to `not-applicable`. For video-model planning, choose each Seedance request as an integer `4-12s` from the Scene's narration window, ordered events, motion complexity, and final hold. If a Scene needs more than `12s`, split it before generation.

### `audio_mode`

Rules:

- if source audio exists, use source audio
- if no source audio exists, show a required popup:
  - `生成中文男声配音（推荐）` -> `generate-voiceover`
  - `不需要音频` -> `no-audio`
- `generate-voiceover` always uses Edge online TTS voice `zh-CN-YunjianNeural`; do not show another voice popup

After `audio_mode` is locked, derive `total_duration_rule` automatically. Generated voiceover uses the measured MP3 duration as the authority.

## State handling

While waiting for popup selection:

- keep the current workflow step stable
- keep `Gate 1` in `pending` state
- do not advance scene planning
- do not generate assets yet
- resume from the exact pending decision once the tool result arrives

## Failure handling

If the host cannot parse the tool arguments:

1. do not guess silently
2. ask Codex to regenerate the tool call in valid JSON

If the user dismisses the popup:

1. either reprompt through the same tool
2. or stop and ask a short fallback text question

## Production recommendation

For production-grade Skill systems, prefer this tool-call popup flow over plain-text choice prompts because it:

- separates AI reasoning from UI rendering
- improves state management
- reduces natural-language drift
- makes multi-step Skills more reliable
