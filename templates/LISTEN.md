# LISTEN: ear check for <film> (5 timecodes)

The agent cannot hear. Everything below comes from `qa.py` measurements, not from listening.
Please listen to these 5 moments (headphones, then a phone speaker) and answer yes/no.

| # | Timecode | Cue(s) | What the checks show | Ask the ear |
|---|---|---|---|---|
| 1 | 00:00.0 | hero `<id>` | sync 0.0 fr · audible +X dB · body +X dB | Does the hit feel like it lands *on* the motion? Too loud? |
| 2 | 00:00.0 | `<id>` (warn) | <qa warning text> | Does this feel early/late? |
| 3 | 00:00.0 | densest moment | N sounds in 1 s · music −X LU | Can you still separate every sound? Is anything harsh? |
| 4 | 00:00.0 | VO + music | voice clearance X LU | Is every word clear over the music? |
| 5 | 00:00.0 | hero `<id>` + stop_before | dead stop 0.4 s before | Does the silence feel intentional, not like a glitch? |

QA summary: `<pass> pass · <warn> warn · <FAIL> FAIL`, integrated `<I>` LUFS (target `<T>`), true peak `<TP>` dBTP,
`<n>` fix rounds. Sounds: `docs/CREDITS.md`. Music: `<title, author, licence>`.
