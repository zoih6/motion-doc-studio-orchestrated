# Edge TTS Voiceover

## Current backend

The default backend is `rany2/edge-tts` running as a skill-local client. It does not run a local speech model: it connects to Microsoft Edge's online TTS service and streams back audio plus word-boundary metadata.

Fixed contract:

- provider: `edge-tts-online`
- voice: `zh-CN-YunjianNeural`
- outputs: MP3, SRT, metadata JSON
- whole-video duration: measured MP3 duration
- beat timing: SRT cue windows

This is the default because one synthesis call produces both audio and the timing data required for Scene planning.

## Existing HTTP wrapper

`travisvn/openai-edge-tts` can be self-hosted with Docker and exposes an OpenAI-compatible `/v1/audio/speech` endpoint. It is suitable when several machines need one shared TTS service, but its standard response is audio-only and its SSE mode streams audio chunks rather than the SRT artifact required by this skill.

Do not switch the skill to that endpoint unless the service is extended to return word boundaries or SRT in the same job.

## Recommended remote-service shape

If a remote HTTP backend is needed, build a thin authenticated service around `edge-tts-universal` or the Python `edge-tts` stream API. The service must preserve WordBoundary events and expose one atomic job result:

```yaml
request:
  text: string
  voice: zh-CN-YunjianNeural
  rate: +0%
response:
  audio: MP3 bytes or authenticated download URL
  subtitles: SRT text or authenticated download URL
  duration_seconds: number
  voice: zh-CN-YunjianNeural
```

Required production safeguards:

- API authentication
- request-size limit and rate limit
- timeout and retry policy
- no public unauthenticated audio URLs
- audio and SRT generated from the same synthesis stream
- response rejected if audio, SRT, duration, or fixed voice is missing

## Backend boundary

Only the synthesis adapter may change. Gate 1, Voiceover Gate, fixed voice, measured total duration, SRT cue validation, semantic Scene plan, and final audio assembly remain unchanged.
