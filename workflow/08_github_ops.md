# 08 · GitHub ops, progress doc, resilience, cleanup

## Token handling
- Write the user's PAT to `/tmp/.ghtok` (outside the repo), use it via `tools/gh.sh` or
  `git -c http.extraheader="Authorization: Basic $(printf 'x-access-token:%s' "$(cat /tmp/.ghtok)" | base64 -w0)" push origin HEAD:<branch>`.
- Never commit it, never put it in remote URLs that get saved (`git remote set-url` back to the clean URL
  after a tokenised clone). Delete it at the end and advise the user to revoke tokens pasted in chat.

## Repo conventions
- `main` = latest approved; a branch per major style iteration (`v2`, `v3`) until approved.
- Releases: `segments` (samples + part previews), `vX.Y` (finals + poster + contact).
- Commit messages say what changed for the viewer ("S5–S9 rebuilt with real Ottoman specimens").

## docs/PROGRESS.md (keep current — it is your memory across resets/sessions)
- Resume-from-zero commands (clone, setup, VO decode, sfx, stills, render).
- Part table: name · frames · time · status · release asset.
- Open issues / next steps / critique notes. User's standing instructions.

## Reset resilience
- Push before ending every turn and before any long job.
- If the environment is empty at the start of a turn: re-write the token, clone, `tools/setup.sh`,
  regenerate tmp audio, read PROGRESS.md, check `git log` and the releases to see what was already done
  (you may have done more than your notes say).

## Cleanup (users care a lot)
- Render scratch lives in `/var/tmp/…`; after upload delete chunks, silent parts, previews, downloads.
- Keep only what the user asked for in their workspace (e.g. the final 720p for viewing).
- Delete raw generations once processed assets are pushed. Delete the token file at the end.
