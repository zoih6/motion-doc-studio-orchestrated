#!/usr/bin/env python3
"""Validate deterministic v0.10 motion-project contracts.
The validator checks timing, asset, storyboard direction, implementation, and
publication evidence without scoring aesthetics. Paths resolve from the manifest.

Manifest shape (all times are seconds):

{
  "composition": {"durationSec": 12.0, "toleranceSec": 0.05},
  "voiceover": {"endSec": 11.5},
  "captions": [{"id": "C1", "startSec": 0.0, "endSec": 2.2}],
  "scenes": [{"id": "S1", "startSec": 0.0, "durationSec": 12.0}],
  "finalHold": {
    "startSec": 11.5,
    "endSec": 12.0,
    "intentional": true,
    "reviewed": true,
    "reason": "Let the thesis land"
  },
  "assets": [{
    "id": "hero",
    "sceneIds": ["S1"],
    "role": "hero subject",
    "file": "assets/hero.png",
    "origin": "generated",
    "technicalStatus": "verified",
    "editorialStatus": "accepted",
    "rightsStatus": "self_created",
    "representationType": "metaphor",
    "requirements": {"requiresAlpha": true},
    "reviewEvidence": ["asset critic review"]
  }],
  "storyboard": {
    "status": "frozen",
    "freezeEvidence": {
      "reviewer": "external-critic",
      "reviewRef": "review-2026-09-17",
      "independent": true
    },
    "scenes": [{
      "id": "S1",
      "beatIds": ["B1"],
      "visualThesis": "The hero visibly changes state",
      "focalPoint": "hero",
      "dominantRelationship": "the before state transforms into the payoff",
      "constructionFamily": "transformation",
      "assetIds": ["hero"],
      "states": [
        {"id": "anchor", "purpose": "establish", "focalElement": "hero",
         "intentionalHoldReason": "make the starting state readable"},
        {"id": "payoff", "purpose": "resolve", "focalElement": "hero",
         "meaningfulChange": "the hero completes its transformation"}
      ],
      "transitionIntent": "carry the transformed hero into the next scene"
    }]
  },
  "implementation": {
    "scenes": [{"id": "S1", "stateIds": ["anchor", "payoff"]}]
  }
}

Paths are resolved relative to the manifest. Alpha inspection is dependency-free
and currently supports PNG. A positive tail after narration/captions is accepted
only when an explicit reviewed finalHold covers it. There are no built-in
aesthetic, stillness, safe-zone, or duration-preference thresholds.

Draft preserves legacy manifests. v0.10 publish requires film direction and ordered
sequence/optional chapter partitions; sequence purpose, payoff trajectory, rhythm
intent, and repetition assessment; and scene visualJob contracts. Explanatory scenes
require stateDelta; other visual jobs may hold without fictional change.
Publication additionally requires independent artifact-bound design and editorial
reviews covering every scene and film/sequence/chapter scope. Per-scene
viewingSizeEvidence records widthPx, heightPx, distance, observation, proofRef,
and proofSha256; local proof bytes are hash-bound inside the review report.
Critics must confirm the proof depicts the reviewed board/master. All evidence
paths resolve from the manifest directory.
The validator never imposes visual diversity quotas or aesthetic thresholds.
  manifest.masterFile = mastered output file
  manifest.reviewReceipt = receipt JSON file
Receipt: {"producerContext": "...", "board": {"file": "...", "sha256": "..."},
          "master": {"file": "...", "sha256": "..."},
          "reviews": {"design": {"file": "...", "sha256": "..."},
                      "editorial": {"file": "...", "sha256": "..."},
                      "technical": {"file": "...", "sha256": "..."}}}
All paths, including receipt paths, are relative to the project manifest.
Reviews use editorial/technical QA report fields plus reviewContext, boardSha256,
blockers (empty for approval), and masterSha256 for final reviews. Design uses
overallStatus=approve; final editorial uses publish_candidate; technical uses
pass. Independent design/editorial reviewContext must differ from producerContext.
The actual review files and board/master bytes are hashed; hashes identify
revisions, not quality or reviewer honesty. Keep the board snapshot self-contained
(or a bundled archive) so its digest includes its defining content.

Evidence assets require sourceUri and claimIds resolving through manifest.claimSet
(the existing claim-set shape) to verified claims with retrievable source URLs or
local files. Generated/reconstructed assets cannot claim representationType=evidence.
Publish checks used assets from board/state/implementation assetIds, used
direction vocabulary bindings, and ledger sceneIds;
resolved rights also require sourceUri and rightsEvidence, including creation
records for self-created work. Unused candidates need not have resolved rights.

Optional scenes[].microbeats[].semanticTiming uses scene-local seconds:
phrase, orientationStartSec <= triggerSec <= actionCompleteSec <= transitionEndSec;
readableStartSec < readableEndSec <= transitionEndSec, with transitionStartSec <= transitionEndSec.
Transition overlap is allowed; all times must fit the scene. Optional sfxEvents
disposition is implemented/replaced/omitted; replacement/omission needs decisionReason.
Storyboard relationshipInvariants contain id, observable, proofRef; these index
review evidence, not a machine assertion that a relationship is visible.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import json
import struct
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


ORIGINS = {"generated", "sourced", "programmatic", "reused", "reconstructed"}
TECHNICAL_STATUSES = {"candidate", "available", "verified"}
EDITORIAL_STATUSES = {"pending", "accepted", "rejected"}
RIGHTS_STATUSES = {"unresolved", "needs_review", "verified", "self_created"}
STORYBOARD_STATUSES = {"draft", "in_review", "ready_for_approval", "frozen"}


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    message: str
    severity: str = "error"


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _object(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _add(findings: list[Finding], code: str, path: str, message: str) -> None:
    findings.append(Finding(code=code, path=path, message=message))


def _unique_ids(
    items: list[Any], collection_path: str, findings: list[Finding]
) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(items):
        item_path = f"{collection_path}[{index}]"
        if not isinstance(raw, dict):
            _add(findings, "INVALID_ITEM", item_path, "must be an object")
            continue
        item_id = raw.get("id")
        if not _nonempty_string(item_id):
            _add(findings, "MISSING_ID", f"{item_path}.id", "must be a non-empty string")
            continue
        if item_id in indexed:
            _add(findings, "DUPLICATE_ID", f"{item_path}.id", f"duplicate id {item_id!r}")
            continue
        indexed[item_id] = raw
    return indexed


def _png_has_alpha(path: Path) -> bool | None:
    """Return PNG alpha capability, or None when the file is not a valid PNG."""
    try:
        with path.open("rb") as handle:
            if handle.read(8) != b"\x89PNG\r\n\x1a\n":
                return None
            saw_ihdr = False
            color_type: int | None = None
            while True:
                raw_length = handle.read(4)
                if len(raw_length) != 4:
                    return None
                length = struct.unpack(">I", raw_length)[0]
                chunk_type = handle.read(4)
                data = handle.read(length)
                crc = handle.read(4)
                if len(chunk_type) != 4 or len(data) != length or len(crc) != 4:
                    return None
                if chunk_type == b"IHDR":
                    if length != 13:
                        return None
                    color_type = data[9]
                    saw_ihdr = True
                elif chunk_type == b"tRNS":
                    return True
                elif chunk_type == b"IEND":
                    break
            if not saw_ihdr or color_type is None:
                return None
            return color_type in {4, 6}
    except OSError:
        return None


def _validate_timing(manifest: dict[str, Any], findings: list[Finding]) -> None:
    composition = _object(manifest.get("composition"))
    duration = composition.get("durationSec")
    tolerance = composition.get("toleranceSec", 0.0)
    if not _is_number(duration) or duration <= 0:
        _add(findings, "INVALID_DURATION", "composition.durationSec", "must be greater than zero")
        return
    if not _is_number(tolerance) or tolerance < 0:
        _add(findings, "INVALID_TOLERANCE", "composition.toleranceSec", "must be zero or greater")
        tolerance = 0.0

    scenes = _list(manifest.get("scenes"))
    scene_index = _unique_ids(scenes, "scenes", findings)
    latest_scene_end = 0.0
    for scene_id, scene in scene_index.items():
        index = scenes.index(scene)
        path = f"scenes[{index}]"
        start = scene.get("startSec")
        scene_duration = scene.get("durationSec")
        if not _is_number(start) or start < 0:
            _add(findings, "INVALID_SCENE_START", f"{path}.startSec", "must be zero or greater")
            continue
        if not _is_number(scene_duration) or scene_duration <= 0:
            _add(findings, "INVALID_SCENE_DURATION", f"{path}.durationSec", "must be greater than zero")
            continue
        end = start + scene_duration
        latest_scene_end = max(latest_scene_end, end)
        if end > duration + tolerance:
            _add(
                findings,
                "SCENE_OUT_OF_BOUNDS",
                path,
                f"scene {scene_id!r} ends at {end:.3f}s after composition end {duration:.3f}s",
            )
        for index, beat in enumerate(_list(scene.get("microbeats"))):
            timing = _object(_object(beat).get("semanticTiming"))
            if "semanticTiming" not in _object(beat):
                continue
            timing_path = f"{path}.microbeats[{index}].semanticTiming"
            fields = ("orientationStartSec", "triggerSec", "actionCompleteSec",
                      "readableStartSec", "readableEndSec", "transitionEndSec")
            values = [timing.get(field) for field in fields]
            transition_start = timing.get("transitionStartSec")
            if (not _nonempty_string(timing.get("phrase"))
                    or any(not _is_number(value) or not 0 <= value <= scene_duration
                           for value in [*values, transition_start])):
                _add(findings, "INVALID_SEMANTIC_TIMING", timing_path, "requires a phrase and scene-local times within scene bounds")
            elif (not values[0] <= values[1] <= values[2] <= values[-1]
                  or not values[3] < values[4] <= values[-1]
                  or transition_start > values[-1]):
                _add(findings, "INVALID_SEMANTIC_ORDER", timing_path, "orientation, trigger, and completion must be ordered; readable and transition windows must end within the event")
        for index, cue in enumerate(_list(scene.get("sfxEvents"))):
            cue = _object(cue)
            if "disposition" not in cue:
                continue
            if (cue["disposition"] not in ("implemented", "replaced", "omitted")
                    or (cue["disposition"] != "implemented" and not _nonempty_string(cue.get("decisionReason")))):
                _add(findings, "INVALID_CUE_DISPOSITION", f"{path}.sfxEvents[{index}]", "replacement or omission requires a decisionReason")
    if scenes and latest_scene_end < duration - tolerance:
        _add(
            findings,
            "SCENES_END_EARLY",
            "scenes",
            f"latest scene ends at {latest_scene_end:.3f}s before composition end {duration:.3f}s",
        )

    voiceover = _object(manifest.get("voiceover"))
    voiceover_end = voiceover.get("endSec")
    if voiceover and (not _is_number(voiceover_end) or voiceover_end < 0):
        _add(findings, "INVALID_VOICEOVER_END", "voiceover.endSec", "must be zero or greater")
        voiceover_end = None
    if _is_number(voiceover_end) and voiceover_end > duration + tolerance:
        _add(
            findings,
            "VOICEOVER_OUT_OF_BOUNDS",
            "voiceover.endSec",
            f"voiceover ends at {voiceover_end:.3f}s after composition end {duration:.3f}s",
        )

    captions = _list(manifest.get("captions"))
    _unique_ids(captions, "captions", findings)
    latest_caption_end: float | None = None
    for index, caption in enumerate(captions):
        if not isinstance(caption, dict):
            continue
        path = f"captions[{index}]"
        start = caption.get("startSec")
        end = caption.get("endSec")
        if not _is_number(start) or start < 0:
            _add(findings, "INVALID_CAPTION_START", f"{path}.startSec", "must be zero or greater")
            continue
        if not _is_number(end) or end < start:
            _add(findings, "INVALID_CAPTION_END", f"{path}.endSec", "must be at or after startSec")
            continue
        latest_caption_end = end if latest_caption_end is None else max(latest_caption_end, end)
        if end > duration + tolerance:
            _add(
                findings,
                "CAPTION_OUT_OF_BOUNDS",
                path,
                f"caption ends at {end:.3f}s after composition end {duration:.3f}s",
            )
        if _is_number(voiceover_end) and end > voiceover_end + tolerance:
            _add(
                findings,
                "CAPTION_AFTER_VOICEOVER",
                path,
                f"caption ends at {end:.3f}s after voiceover end {voiceover_end:.3f}s",
            )

    active_end_candidates = [value for value in (voiceover_end, latest_caption_end) if _is_number(value)]
    active_end = max(active_end_candidates) if active_end_candidates else duration
    tail = duration - active_end
    hold = _object(manifest.get("finalHold"))
    if tail > tolerance and not hold:
        _add(
            findings,
            "UNDECLARED_FINAL_HOLD",
            "finalHold",
            f"composition has a {tail:.3f}s tail after narration/captions; declare and review it",
        )
    if hold:
        start = hold.get("startSec")
        end = hold.get("endSec")
        if not _is_number(start) or start < 0:
            _add(findings, "INVALID_HOLD_START", "finalHold.startSec", "must be zero or greater")
        if not _is_number(end) or (_is_number(start) and end <= start):
            _add(findings, "INVALID_HOLD_END", "finalHold.endSec", "must be after startSec")
        elif abs(end - duration) > tolerance:
            _add(
                findings,
                "HOLD_END_MISMATCH",
                "finalHold.endSec",
                "must match composition.durationSec within toleranceSec",
            )
        if _is_number(start) and start > active_end + tolerance:
            _add(
                findings,
                "HOLD_GAP",
                "finalHold.startSec",
                f"hold starts at {start:.3f}s after active content ends at {active_end:.3f}s",
            )
        if hold.get("intentional") is not True:
            _add(findings, "HOLD_NOT_INTENTIONAL", "finalHold.intentional", "must be true")
        if hold.get("reviewed") is not True:
            _add(findings, "HOLD_NOT_REVIEWED", "finalHold.reviewed", "must be true")
        if not _nonempty_string(hold.get("reason")):
            _add(findings, "MISSING_HOLD_REASON", "finalHold.reason", "must explain the editorial purpose")


def _validate_assets(
    manifest: dict[str, Any], manifest_dir: Path, findings: list[Finding]
) -> dict[str, dict[str, Any]]:
    assets = _list(manifest.get("assets"))
    asset_index = _unique_ids(assets, "assets", findings)
    for asset_id, asset in asset_index.items():
        index = assets.index(asset)
        path = f"assets[{index}]"
        origin = asset.get("origin")
        technical = asset.get("technicalStatus")
        editorial = asset.get("editorialStatus")
        rights = asset.get("rightsStatus")
        if origin not in ORIGINS:
            _add(findings, "INVALID_ASSET_ORIGIN", f"{path}.origin", f"must be one of {sorted(ORIGINS)}")
        if technical not in TECHNICAL_STATUSES:
            _add(
                findings,
                "INVALID_TECHNICAL_STATUS",
                f"{path}.technicalStatus",
                f"must be one of {sorted(TECHNICAL_STATUSES)}",
            )
        if editorial not in EDITORIAL_STATUSES:
            _add(
                findings,
                "INVALID_EDITORIAL_STATUS",
                f"{path}.editorialStatus",
                f"must be one of {sorted(EDITORIAL_STATUSES)}",
            )
        if rights not in RIGHTS_STATUSES:
            _add(
                findings,
                "INVALID_RIGHTS_STATUS",
                f"{path}.rightsStatus",
                f"must be one of {sorted(RIGHTS_STATUSES)}",
            )
        if asset.get("representationType") == "evidence":
            if origin in {"generated", "reconstructed"}:
                _add(findings, "COUNTERFEIT_EVIDENCE", path, "generated/reconstructed material must use an honest non-evidence representation")
            claim_set = _object(manifest.get("claimSet"))
            claims = {item.get("id"): item for item in _list(claim_set.get("claims"))
                      if isinstance(item, dict) and _nonempty_string(item.get("id"))}
            sources = {item.get("id"): item for item in _list(claim_set.get("sources"))
                       if isinstance(item, dict) and _nonempty_string(item.get("id"))}
            claim_ids = asset.get("claimIds")
            if (not _source_exists(asset.get("sourceUri"), manifest_dir) or not isinstance(claim_ids, list)
                    or not claim_ids or any(not _nonempty_string(item) for item in claim_ids)):
                _add(findings, "INCOMPLETE_EVIDENCE", path, "evidence needs sourceUri and supported claimIds")
            else:
                for claim_id in claim_ids:
                    claim = claims.get(claim_id, {})
                    refs = _list(claim.get("sourceRefs"))
                    if (claim.get("status") != "verified" or not _nonempty_string(claim.get("claim"))
                            or not refs or any(not _nonempty_string(ref) or ref not in sources
                                              or not _source_exists(sources[ref].get("url"), manifest_dir)
                                              for ref in refs)):
                        _add(findings, "UNSUPPORTED_EVIDENCE_CLAIM", path, f"claim {claim_id!r} needs verified text and retrievable sourceRefs")
        if editorial == "accepted":
            if technical != "verified":
                _add(
                    findings,
                    "ACCEPTED_ASSET_NOT_VERIFIED",
                    path,
                    "editorial acceptance requires technicalStatus=verified",
                )
            review_evidence = asset.get("reviewEvidence")
            if not isinstance(review_evidence, list) or not review_evidence or any(
                not _nonempty_string(item) for item in review_evidence
            ):
                _add(
                    findings,
                    "ACCEPTED_ASSET_MISSING_REVIEW",
                    f"{path}.reviewEvidence",
                    "editorial acceptance requires at least one review reference",
                )

        asset_path_value = asset.get("file")
        asset_path_field = "file"
        if not _nonempty_string(asset_path_value) and _nonempty_string(asset.get("path")):
            asset_path_value = asset.get("path")
            asset_path_field = "path"
        needs_file = technical in {"available", "verified"} or editorial == "accepted"
        resolved_path: Path | None = None
        if _nonempty_string(asset_path_value):
            resolved_path = (manifest_dir / asset_path_value).resolve()
            if not resolved_path.is_file():
                _add(
                    findings,
                    "ASSET_FILE_MISSING",
                    f"{path}.{asset_path_field}",
                    f"asset {asset_id!r} does not exist at {resolved_path}",
                )
        elif needs_file:
            _add(findings, "ASSET_FILE_REQUIRED", f"{path}.file", "available, verified, or accepted assets need a file")

        if rights == "verified":
            for field in ("sourceUri", "license", "rightsEvidence"):
                if not _nonempty_string(asset.get(field)):
                    _add(
                        findings,
                        "INCOMPLETE_RIGHTS_EVIDENCE",
                        f"{path}.{field}",
                        "rightsStatus=verified requires sourceUri, license, and rightsEvidence",
                    )

        requirements = _object(asset.get("requirements"))
        requires_alpha = requirements.get("requiresAlpha")
        if requires_alpha is None:
            requires_alpha = asset.get("requiredAlpha")
        if requires_alpha is True and resolved_path and resolved_path.is_file():
            alpha = _png_has_alpha(resolved_path)
            if alpha is None:
                _add(
                    findings,
                    "ALPHA_FORMAT_UNSUPPORTED",
                    f"{path}.{asset_path_field}",
                    "dependency-free alpha inspection currently supports valid PNG files only",
                )
            elif not alpha:
                _add(findings, "ALPHA_REQUIRED", f"{path}.{asset_path_field}", "asset does not contain an alpha channel")
    return asset_index


def _validate_direction(
    storyboard: dict[str, Any], planned_scenes: list[Any],
    asset_index: dict[str, dict[str, Any]], findings: list[Finding],
) -> None:
    direction = _object(storyboard.get("direction"))
    if not direction:
        return
    film = _object(direction.get("film"))
    if any(not _nonempty_string(film.get(field))
           for field in ("viewerPromise", "argument", "emotionalProgression", "conclusion")):
        _add(findings, "INCOMPLETE_FILM_DIRECTION", "storyboard.direction.film",
             "requires viewerPromise, argument, emotionalProgression, and conclusion")
    scene_ids = [scene.get("id") for scene in planned_scenes
                 if isinstance(scene, dict) and _nonempty_string(scene.get("id"))]
    sequences = _list(direction.get("sequences"))
    sequence_ids = _unique_ids(sequences, "storyboard.direction.sequences", findings)
    for sequence_id, sequence in sequence_ids.items():
        if any(not _nonempty_string(sequence.get(field))
               for field in ("purpose", "payoffTrajectory", "rhythmIntent", "repetitionAssessment")):
            _add(findings, "INCOMPLETE_SEQUENCE_DIRECTION",
                 f"storyboard.direction.sequences[{sequence_id}]",
                 "requires purpose, payoffTrajectory, rhythmIntent, and repetitionAssessment")
    flattened_scenes: list[str] = []
    for sequence_id, sequence in sequence_ids.items():
        ids = sequence.get("sceneIds")
        if not isinstance(ids, list) or not ids or any(not _nonempty_string(item) for item in ids):
            _add(findings, "INVALID_SEQUENCE_SCENES", f"storyboard.direction.sequences[{sequence_id}].sceneIds",
                 "must contain ordered non-empty scene ids")
            continue
        flattened_scenes.extend(ids)
    if len(flattened_scenes) != len(set(flattened_scenes)):
        _add(findings, "DUPLICATE_SEQUENCE_SCENE", "storyboard.direction.sequences",
             "each scene must occur in exactly one sequence")
    if flattened_scenes != scene_ids:
        _add(findings, "SEQUENCE_PARTITION_MISMATCH", "storyboard.direction.sequences",
             "sequence scene ids must partition all scenes in film order")

    if "chapters" in direction:
        chapter_ids = _unique_ids(_list(direction.get("chapters")), "storyboard.direction.chapters", findings)
        flattened_sequences: list[str] = []
        for chapter_id, chapter in chapter_ids.items():
            if any(not _nonempty_string(chapter.get(field))
                   for field in ("argumentTurn", "evidenceBurden", "payoff")):
                _add(findings, "INCOMPLETE_CHAPTER_DIRECTION",
                     f"storyboard.direction.chapters[{chapter_id}]",
                     "requires argumentTurn, evidenceBurden, and payoff")
            ids = chapter.get("sequenceIds")
            if not isinstance(ids, list) or not ids or any(not _nonempty_string(item) for item in ids):
                _add(findings, "INVALID_CHAPTER_SEQUENCES", f"storyboard.direction.chapters[{chapter_id}].sequenceIds",
                     "must contain ordered non-empty sequence ids")
                continue
            flattened_sequences.extend(ids)
        if len(flattened_sequences) != len(set(flattened_sequences)):
            _add(findings, "DUPLICATE_CHAPTER_SEQUENCE", "storyboard.direction.chapters",
                 "each sequence must occur in exactly one chapter")
        if flattened_sequences != list(sequence_ids):
            _add(findings, "CHAPTER_PARTITION_MISMATCH", "storyboard.direction.chapters",
                 "chapter sequence ids must partition declared sequences in order")

    vocabulary = _list(direction.get("vocabulary"))
    vocabulary_index = _unique_ids(vocabulary, "storyboard.direction.vocabulary", findings)
    used_vocabulary = {item for scene in _list(storyboard.get("scenes")) if isinstance(scene, dict)
                       for item in _list(scene.get("vocabularyIds")) if _nonempty_string(item)}
    for scene in _list(storyboard.get("scenes")):
        if isinstance(scene, dict):
            for vocabulary_id in _list(scene.get("vocabularyIds")):
                if not _nonempty_string(vocabulary_id) or vocabulary_id not in vocabulary_index:
                    _add(findings, "UNKNOWN_VOCABULARY_REFERENCE",
                         f"storyboard.scenes[{scene.get('id')}].vocabularyIds",
                         f"unknown vocabulary id {vocabulary_id!r}")
    for vocabulary_id, item in vocabulary_index.items():
        if any(not _nonempty_string(item.get(field))
               for field in ("subjectIdentity", "visualRole", "viewpoint", "representation")):
            _add(findings, "INCOMPLETE_VOCABULARY_ROLE",
                 f"storyboard.direction.vocabulary[{vocabulary_id}]",
                 "requires subjectIdentity, visualRole, viewpoint, and representation")
        if item.get("representation") not in ("literal", "evidence", "reconstruction", "metaphor", "abstract"):
            _add(findings, "INVALID_VOCABULARY_REPRESENTATION",
                 f"storyboard.direction.vocabulary[{vocabulary_id}].representation",
                 "must use an existing representation type")
        bindings = item.get("assetIds")
        if not isinstance(bindings, list):
            _add(findings, "INVALID_VOCABULARY_ASSETS",
                 f"storyboard.direction.vocabulary[{vocabulary_id}].assetIds", "must be an array of asset ids")
            continue
        valid_bindings = [value for value in bindings if _nonempty_string(value)]
        if len(valid_bindings) != len(set(valid_bindings)):
            _add(findings, "DUPLICATE_VOCABULARY_ASSET",
                 f"storyboard.direction.vocabulary[{vocabulary_id}].assetIds",
                 "asset bindings must be unique within a vocabulary role")
        if (vocabulary_id in used_vocabulary and storyboard.get("status") in {"ready_for_approval", "frozen"}
                and not bindings):
            _add(findings, "UNBOUND_USED_VOCABULARY",
                 f"storyboard.direction.vocabulary[{vocabulary_id}].assetIds",
                 "used vocabulary roles need bound assets before freeze")
        for asset_id in bindings:
            if not _nonempty_string(asset_id):
                _add(findings, "INVALID_VOCABULARY_ASSETS",
                     f"storyboard.direction.vocabulary[{vocabulary_id}].assetIds",
                     "asset ids must be non-empty strings")
                continue
            asset = asset_index.get(asset_id)
            if asset is None:
                _add(findings, "UNKNOWN_VOCABULARY_ASSET",
                     f"storyboard.direction.vocabulary[{vocabulary_id}].assetIds",
                     f"unknown asset id {asset_id!r}")


def _validate_storyboard(
    manifest: dict[str, Any],
    asset_index: dict[str, dict[str, Any]],
    findings: list[Finding],
) -> None:
    storyboard = _object(manifest.get("storyboard"))
    if not storyboard:
        return
    status = storyboard.get("status")
    if status not in STORYBOARD_STATUSES:
        _add(
            findings,
            "INVALID_STORYBOARD_STATUS",
            "storyboard.status",
            f"must be one of {sorted(STORYBOARD_STATUSES)}",
        )
    storyboard_scenes = _list(storyboard.get("scenes"))
    storyboard_index = _unique_ids(storyboard_scenes, "storyboard.scenes", findings)
    planned_index = {
        item.get("id"): item
        for item in _list(manifest.get("scenes"))
        if isinstance(item, dict) and _nonempty_string(item.get("id"))
    }
    _validate_direction(storyboard, storyboard_scenes, asset_index, findings)
    storyboard_state_ids: dict[str, list[str]] = {}
    for scene_id, scene in storyboard_index.items():
        path = f"storyboard.scenes[{scene_id}]"
        if "relationshipInvariants" in scene:
            invariants = scene["relationshipInvariants"]
            if not isinstance(invariants, list):
                _add(findings, "INVALID_RELATIONSHIP_INVARIANTS", path, "relationshipInvariants must be an array")
            else:
                indexed = _unique_ids(invariants, f"{path}.relationshipInvariants", findings)
                for invariant in indexed.values():
                    if any(not _nonempty_string(invariant.get(field)) for field in ("observable", "proofRef")):
                        _add(findings, "INCOMPLETE_RELATIONSHIP_INVARIANT", path, "each defining promise needs observable and proofRef")
        if "shotScore" in scene:
            score = _object(scene["shotScore"])
            if any(not _nonempty_string(score.get(field)) for field in
                   ("composition", "objectAction", "camera", "attention", "rhythm", "sound", "exit")):
                _add(findings, "INCOMPLETE_SHOT_SCORE", path, "shot score must resolve composition, action, camera, attention, rhythm, sound, and exit")
        visual_job = scene.get("visualJob")
        valid_jobs = ("explanation", "identification", "evidence", "chronology", "atmosphere", "emotion", "payoff")
        if visual_job is not None and visual_job not in valid_jobs:
            _add(findings, "INVALID_VISUAL_JOB", f"{path}.visualJob", f"must be one of {sorted(valid_jobs)}")
        if visual_job == "explanation" or "stateDelta" in scene:
            delta = _object(scene.get("stateDelta"))
            if any(not _nonempty_string(delta.get(field)) for field in ("before", "operation", "after", "viewerInference")):
                _add(findings, "INCOMPLETE_STATE_DELTA", f"{path}.stateDelta",
                     "stateDelta requires before, operation, after, and viewerInference")
        if visual_job == "payoff" and not _nonempty_string(scene.get("payoffConstruction")):
            _add(findings, "MISSING_PAYOFF_CONSTRUCTION", f"{path}.payoffConstruction",
                 "payoff scenes require a construction choice")
        if "conceptSearch" in scene:
            search = _object(scene["conceptSearch"])
            candidates = _list(search.get("candidates"))
            if not 2 <= len(candidates) <= 3:
                _add(findings, "INVALID_CONCEPT_COUNT", f"{path}.conceptSearch.candidates",
                     "concept search needs two or three candidates")
            if any(not _nonempty_string(_object(candidate).get(field))
                   for candidate in candidates for field in ("id", "family", "inference", "description")):
                _add(findings, "INCOMPLETE_CONCEPT", f"{path}.conceptSearch.candidates",
                     "each candidate needs id, family, inference, and description")
            ids = [_object(candidate).get("id") for candidate in candidates
                   if _nonempty_string(_object(candidate).get("id"))]
            families = [_object(candidate).get("family") for candidate in candidates
                        if _nonempty_string(_object(candidate).get("family"))]
            inferences = [_object(candidate).get("inference") for candidate in candidates
                          if _nonempty_string(_object(candidate).get("inference"))]
            if len(ids) != len(set(ids)):
                _add(findings, "DUPLICATE_CONCEPT_ID", f"{path}.conceptSearch.candidates", "candidate ids must be unique")
            if len(families) != len(set(families)):
                _add(findings, "CONCEPT_FAMILIES_NOT_DISTINCT", f"{path}.conceptSearch.candidates",
                     "candidate construction families must differ")
            if len({str(value).strip().casefold() for value in inferences}) > 1:
                _add(findings, "CONCEPT_INFERENCE_MISMATCH", f"{path}.conceptSearch.candidates",
                     "candidates must test the same viewer inference")
            if search.get("selectedId") not in ids:
                _add(findings, "INVALID_SELECTED_CONCEPT", f"{path}.conceptSearch.selectedId",
                     "selectedId must identify one candidate")
            if not _nonempty_string(search.get("selectionReason")):
                _add(findings, "MISSING_CONCEPT_REASON", f"{path}.conceptSearch.selectionReason",
                     "selection needs a reason")

    if status in {"ready_for_approval", "frozen"}:
        evidence_field = "freezeEvidence" if status == "frozen" else "reviewEvidence"
        review_evidence = _object(storyboard.get(evidence_field))
        for field in ("reviewer", "reviewRef"):
            if not _nonempty_string(review_evidence.get(field)):
                _add(
                    findings,
                    "INCOMPLETE_FREEZE_EVIDENCE" if status == "frozen" else "INCOMPLETE_REVIEW_EVIDENCE",
                    f"storyboard.{evidence_field}.{field}",
                    f"a {status} storyboard requires non-empty reviewer and reviewRef fields",
                )
        if review_evidence.get("independent") is not True:
            _add(
                findings,
                "FREEZE_REVIEW_NOT_INDEPENDENT" if status == "frozen" else "REVIEW_NOT_INDEPENDENT",
                f"storyboard.{evidence_field}.independent",
                f"a {status} storyboard requires independent editorial review",
            )
        for scene_id in sorted(set(planned_index) - set(storyboard_index)):
            _add(
                findings,
                "STORYBOARD_SCENE_MISSING",
                "storyboard.scenes",
                f"planned scene {scene_id!r} is missing from the review-ready storyboard",
            )
        for scene_id, scene in storyboard_index.items():
            index = storyboard_scenes.index(scene)
            path = f"storyboard.scenes[{index}]"
            for field in (
                "visualThesis",
                "focalPoint",
                "dominantRelationship",
                "constructionFamily",
                "transitionIntent",
            ):
                if not _nonempty_string(scene.get(field)):
                    _add(
                        findings,
                        "INCOMPLETE_FROZEN_SCENE",
                        f"{path}.{field}",
                        "must be a non-empty string before approval/freeze",
                    )
            beat_ids = scene.get("beatIds")
            if not isinstance(beat_ids, list) or not beat_ids or any(not _nonempty_string(value) for value in beat_ids):
                _add(
                    findings,
                    "INCOMPLETE_FROZEN_SCENE",
                    f"{path}.beatIds",
                    "must contain at least one non-empty beat id",
                )
            elif len(set(beat_ids)) != len(beat_ids):
                _add(
                    findings,
                    "DUPLICATE_BEAT_ID",
                    f"{path}.beatIds",
                    "beat ids must be unique within a scene",
                )

            scene_asset_ids = scene.get("assetIds")
            if not isinstance(scene_asset_ids, list):
                _add(findings, "INCOMPLETE_FROZEN_SCENE", f"{path}.assetIds", "must be an array")
                scene_asset_ids = []
            elif any(not _nonempty_string(asset_id) for asset_id in scene_asset_ids):
                _add(
                    findings,
                    "INVALID_ASSET_REFERENCE",
                    f"{path}.assetIds",
                    "asset ids must be non-empty strings",
                )
                scene_asset_ids = []
            elif len(set(scene_asset_ids)) != len(scene_asset_ids):
                _add(findings, "DUPLICATE_ASSET_REFERENCE", f"{path}.assetIds", "asset ids must be unique")
            for asset_id in scene_asset_ids:
                if asset_id not in asset_index:
                    _add(
                        findings,
                        "UNKNOWN_ASSET_REFERENCE",
                        f"{path}.assetIds",
                        f"unknown asset id {asset_id!r}",
                    )
                    continue
                asset = asset_index[asset_id]
                if asset.get("technicalStatus") != "verified" or asset.get("editorialStatus") != "accepted":
                    _add(
                        findings,
                        "FROZEN_ASSET_NOT_READY",
                        f"{path}.assetIds",
                        f"asset {asset_id!r} must be technically verified and editorially accepted before approval/freeze",
                    )

            states = scene.get("states")
            if not isinstance(states, list) or not states:
                _add(
                    findings,
                    "INCOMPLETE_FROZEN_SCENE",
                    f"{path}.states",
                    "must contain at least one state object",
                )
                states = []
            state_index = _unique_ids(states, f"{path}.states", findings)
            storyboard_state_ids[scene_id] = list(state_index)
            for state_id, state in state_index.items():
                state_position = states.index(state)
                state_path = f"{path}.states[{state_position}]"
                for field in ("purpose", "focalElement"):
                    if not _nonempty_string(state.get(field)):
                        _add(
                            findings,
                            "INCOMPLETE_STORYBOARD_STATE",
                            f"{state_path}.{field}",
                            "must be a non-empty string before approval/freeze",
                        )
                has_change = _nonempty_string(state.get("meaningfulChange"))
                has_hold = _nonempty_string(state.get("intentionalHoldReason"))
                if has_change == has_hold:
                    _add(
                        findings,
                        "INVALID_STATE_SEMANTICS",
                        state_path,
                        "state must declare exactly one of meaningfulChange or intentionalHoldReason",
                    )
                state_asset_ids = state.get("assetIds", [])
                if not isinstance(state_asset_ids, list):
                    _add(findings, "INVALID_STATE_ASSETS", f"{state_path}.assetIds", "must be an array")
                    continue
                if any(not _nonempty_string(asset_id) for asset_id in state_asset_ids):
                    _add(
                        findings,
                        "INVALID_STATE_ASSETS",
                        f"{state_path}.assetIds",
                        "asset ids must be non-empty strings",
                    )
                    continue
                for asset_id in state_asset_ids:
                    if asset_id not in asset_index:
                        _add(
                            findings,
                            "UNKNOWN_ASSET_REFERENCE",
                            f"{state_path}.assetIds",
                            f"unknown asset id {asset_id!r}",
                        )

    if status not in {"ready_for_approval", "frozen"}:
        for scene_id, scene in storyboard_index.items():
            states = _list(scene.get("states"))
            storyboard_state_ids[scene_id] = [
                state["id"]
                for state in states
                if isinstance(state, dict) and _nonempty_string(state.get("id"))
            ]

    implementation = _object(manifest.get("implementation"))
    if not implementation:
        return
    implementation_scenes = _list(implementation.get("scenes"))
    implementation_index = _unique_ids(implementation_scenes, "implementation.scenes", findings)
    for scene_id in sorted(set(storyboard_index) - set(implementation_index)):
        _add(
            findings,
            "IMPLEMENTATION_SCENE_MISSING",
            "implementation.scenes",
            f"storyboard scene {scene_id!r} is missing from implementation metadata",
        )
    for scene_id in sorted(set(implementation_index) - set(storyboard_index)):
        _add(
            findings,
            "IMPLEMENTATION_SCENE_EXTRA",
            "implementation.scenes",
            f"implementation scene {scene_id!r} is not present in the storyboard",
        )
    for scene_id in sorted(set(storyboard_index) & set(implementation_index)):
        storyboard_states = storyboard_state_ids.get(scene_id, [])
        implementation_states = _list(implementation_index[scene_id].get("stateIds"))
        missing = [state for state in storyboard_states if state not in implementation_states]
        extra = [state for state in implementation_states if state not in storyboard_states]
        if missing:
            _add(
                findings,
                "IMPLEMENTATION_STATE_MISSING",
                f"implementation.scenes[{scene_id}].stateIds",
                f"missing storyboard states: {missing}",
            )
        if extra:
            _add(
                findings,
                "IMPLEMENTATION_STATE_EXTRA",
                f"implementation.scenes[{scene_id}].stateIds",
                f"states not present in storyboard: {extra}",
            )
        if not missing and not extra and storyboard_states != implementation_states:
            _add(
                findings,
                "IMPLEMENTATION_STATE_ORDER_MISMATCH",
                f"implementation.scenes[{scene_id}].stateIds",
                "state order differs from the frozen storyboard",
            )

def _source_exists(value: Any, base: Path) -> bool:
    if not _nonempty_string(value):
        return False
    # Network retrieval and source authority remain research/editorial review work.
    from urllib.parse import urlparse
    try:
        parsed = urlparse(value)
        return (parsed.scheme in {"http", "https"} and bool(parsed.netloc)) or (base / value).is_file()
    except (ValueError, OSError):
        return False


def _bound_file(value: Any, base: Path, path: str, findings: list[Finding]) -> Path | None:
    artifact = _object(value)
    filename, digest = artifact.get("file"), artifact.get("sha256")
    if (not _nonempty_string(filename) or not isinstance(digest, str) or len(digest) != 64
            or any(char not in "0123456789abcdef" for char in digest)):
        _add(findings, "INVALID_ARTIFACT_BINDING", path, "requires file and lowercase SHA-256 digest")
        return None
    resolved = (base / filename).resolve()
    try:
        with resolved.open("rb") as handle:
            actual = hashlib.file_digest(handle, "sha256").hexdigest()
    except OSError as error:
        _add(findings, "ARTIFACT_READ_ERROR", path, str(error))
        return None
    if actual != digest:
        _add(findings, "STALE_ARTIFACT", path, "file bytes differ from reviewed SHA-256")
        return None
    return resolved


def _validate_publish(manifest: dict[str, Any], base: Path, assets: dict[str, dict[str, Any]],
                      findings: list[Finding]) -> None:
    board = _object(manifest.get("storyboard"))
    if board.get("status") != "frozen" or not _list(board.get("scenes")):
        _add(findings, "PUBLISH_REQUIRES_FREEZE", "storyboard", "publish requires a populated frozen storyboard")
    if not _object(board.get("direction")):
        _add(findings, "PUBLISH_REQUIRES_DIRECTION", "storyboard.direction",
             "v0.10 publish requires film, sequence, and vocabulary direction")
    if not _list(_object(board.get("direction")).get("vocabulary")):
        _add(findings, "PUBLISH_REQUIRES_VOCABULARY", "storyboard.direction.vocabulary",
             "v0.10 publish requires a populated visual vocabulary contract")
    for index, scene in enumerate(_list(board.get("scenes"))):
        scene = _object(scene)
        job = scene.get("visualJob")
        if job not in ("explanation", "identification", "evidence", "chronology", "atmosphere", "emotion", "payoff"):
            _add(findings, "PUBLISH_REQUIRES_VISUAL_JOB", f"storyboard.scenes[{index}].visualJob",
                 "v0.10 publish requires a declared visualJob")
        if job == "explanation" and any(not _nonempty_string(_object(scene.get("stateDelta")).get(field))
                                        for field in ("before", "operation", "after", "viewerInference")):
            _add(findings, "PUBLISH_REQUIRES_STATE_DELTA", f"storyboard.scenes[{index}].stateDelta",
                 "explanatory scenes require complete stateDelta")
        if job == "payoff" and not _nonempty_string(scene.get("payoffConstruction")):
            _add(findings, "PUBLISH_REQUIRES_PAYOFF", f"storyboard.scenes[{index}].payoffConstruction",
                 "payoff scenes require payoffConstruction")
    if not _list(_object(manifest.get("implementation")).get("scenes")):
        _add(findings, "PUBLISH_REQUIRES_IMPLEMENTATION", "implementation", "publish requires as-built scene metadata")
    used = set()
    for section in (board, _object(manifest.get("implementation"))):
        for scene in _list(section.get("scenes")):
            scene = _object(scene)
            for item in [scene, *[_object(state) for state in _list(scene.get("states"))]]:
                used.update(value for value in _list(item.get("assetIds")) if _nonempty_string(value))
    used.update(asset_id for asset_id, asset in assets.items() if _list(asset.get("sceneIds")))
    used_vocabulary = {value for scene in _list(board.get("scenes"))
                       for value in _list(_object(scene).get("vocabularyIds")) if _nonempty_string(value)}
    for role in _list(_object(board.get("direction")).get("vocabulary")):
        role = _object(role)
        if _nonempty_string(role.get("id")) and role["id"] in used_vocabulary:
            used.update(value for value in _list(role.get("assetIds")) if _nonempty_string(value))
    for asset_id in sorted(used):
        asset = assets.get(asset_id)
        if asset is None:
            _add(findings, "UNKNOWN_ASSET_REFERENCE", "assets", f"used asset {asset_id!r} is not declared")
            continue
        if asset.get("technicalStatus") != "verified" or asset.get("editorialStatus") != "accepted":
            _add(findings, "PUBLISH_ASSET_NOT_READY", f"assets.{asset_id}", "used assets must be verified and accepted")
        if asset.get("rightsStatus") not in {"verified", "self_created"}:
            _add(findings, "PUBLISH_RIGHTS_UNRESOLVED", f"assets.{asset_id}", "used asset rights must be resolved")
        if (not _source_exists(asset.get("sourceUri"), base)
                or not _nonempty_string(asset.get("rightsEvidence"))):
            _add(findings, "PUBLISH_PROVENANCE_MISSING", f"assets.{asset_id}", "used assets require sourceUri and rightsEvidence (creation records for self-created work)")
    receipt_ref = manifest.get("reviewReceipt")
    if not _nonempty_string(receipt_ref):
        _add(findings, "PUBLISH_RECEIPT_REQUIRED", "reviewReceipt", "publish requires an artifact-bound review receipt")
        return
    try:
        receipt = json.loads((base / receipt_ref).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        _add(findings, "RECEIPT_READ_ERROR", "reviewReceipt", str(error))
        return
    receipt = _object(receipt)
    producer = receipt.get("producerContext")
    if not _nonempty_string(producer):
        _add(findings, "MISSING_PRODUCER_CONTEXT", "reviewReceipt.producerContext", "requires the generating/implementation context identity")
    for name, expected in (("board", _object(board.get("preview")).get("path")),
                           ("master", manifest.get("masterFile"))):
        artifact = _object(receipt.get(name))
        _bound_file(artifact, base, f"reviewReceipt.{name}", findings)
        if (not _nonempty_string(expected) or not _nonempty_string(artifact.get("file"))
                or (base / expected).resolve() != (base / artifact["file"]).resolve()):
            _add(findings, "ARTIFACT_PATH_MISMATCH", f"reviewReceipt.{name}", "receipt must bind the manifest's frozen preview/master file")
    for name, verdict in (("design", "approve"), ("editorial", "publish_candidate"), ("technical", "pass")):
        path = f"reviewReceipt.reviews.{name}"
        review_path = _bound_file(_object(receipt.get("reviews")).get(name), base, path, findings)
        if review_path is None:
            continue
        try:
            review = _object(json.loads(review_path.read_text(encoding="utf-8")))
        except (OSError, ValueError) as error:
            _add(findings, "REVIEW_READ_ERROR", path, str(error))
            continue
        if review.get("overallStatus") != verdict or review.get("blockers") != []:
            _add(findings, "REVIEW_NOT_APPROVED", path, "requires the stage's affirmative verdict and empty blockers")
        context = review.get("reviewContext")
        if not _nonempty_string(context):
            _add(findings, "MISSING_REVIEW_CONTEXT", path, "requires reviewer context identity")
        if name != "technical" and (review.get("independent") is not True or context == producer
                                    or not _nonempty_string(review.get("critic"))):
            _add(findings, "REVIEW_NOT_INDEPENDENT", path, "design/editorial approval requires an identified independent critic context")
        for artifact in (("board",) if name == "design" else ("board", "master")):
            digest = _object(receipt.get(artifact)).get("sha256")
            if not digest or review.get(f"{artifact}Sha256") != digest:
                _add(findings, "REVIEW_ARTIFACT_MISMATCH", path, f"review does not cover current {artifact}")
        if name == "technical":
            checks = _list(review.get("checks"))
            if (not _nonempty_string(review.get("runId")) or not checks
                    or any(_object(check).get("status") not in ("pass", "not_applicable")
                           or not _nonempty_string(_object(check).get("id"))
                           or not _nonempty_string(_object(check).get("evidence")) for check in checks)):
                _add(findings, "TECHNICAL_CHECKS_UNRESOLVED", path, "technical checks need passing results and evidence")
        else:
            render_refs = review.get("renderRefs")
            if (not isinstance(render_refs, list) or not render_refs
                    or any(not _source_exists(ref, base) for ref in render_refs)):
                _add(findings, "REVIEW_EVIDENCE_MISSING", path, "design/editorial review requires existing local renderRefs or source URLs")
            scene_reviews = _list(review.get("sceneFindings"))
            required_scenes = {scene.get("id") for scene in _list(board.get("scenes"))
                               if isinstance(scene, dict) and _nonempty_string(scene.get("id"))}
            reviewed_scenes = {item.get("sceneId") for item in scene_reviews
                               if isinstance(item, dict) and _nonempty_string(item.get("sceneId"))}
            checks = ("thesisClear", "hierarchyClear", "visualJobSatisfied",
                      "pacingResolved", "continuityResolved", "assetFit")
            if (not scene_reviews or required_scenes != reviewed_scenes
                    or len(scene_reviews) != len(reviewed_scenes)
                    or any(_object(item).get("status") != "approve"
                           or any(_object(_object(item).get("checks")).get(key) is not True for key in checks)
                           for item in scene_reviews)):
                _add(findings, "EDITORIAL_CHECKS_UNRESOLVED", path, "every board scene needs affirmative editorial checks")
            if any(not (isinstance(_object(item).get("viewingSizeEvidence"), list)
                        and _object(item).get("viewingSizeEvidence"))
                   or any(type(_object(evidence).get(field)) is not int or _object(evidence).get(field) <= 0
                          for evidence in _list(_object(item).get("viewingSizeEvidence"))
                          for field in ("widthPx", "heightPx"))
                   or any(any(not _nonempty_string(_object(evidence).get(field))
                              for field in ("distance", "observation", "proofRef"))
                          or not _nonempty_string(_object(evidence).get("proofSha256"))
                          for evidence in _list(_object(item).get("viewingSizeEvidence")))
                   for item in scene_reviews):
                _add(findings, "VIEWING_SIZE_EVIDENCE_MISSING", path,
                     "each scene needs readable proof with positive widthPx/heightPx, distance, and observation")
            for item in scene_reviews:
                for index, evidence in enumerate(_list(_object(item).get("viewingSizeEvidence"))):
                    evidence = _object(evidence)
                    _bound_file({"file": evidence.get("proofRef"), "sha256": evidence.get("proofSha256")},
                                base, f"{path}.sceneFindings[{_object(item).get('sceneId')}].viewingSizeEvidence[{index}]",
                                findings)
            direction = _object(board.get("direction"))
            required_scopes = {("film", "film")}
            required_scopes.update(("sequence", item.get("id")) for item in _list(direction.get("sequences"))
                                   if isinstance(item, dict) and _nonempty_string(item.get("id")))
            required_scopes.update(("chapter", item.get("id")) for item in _list(direction.get("chapters"))
                                   if isinstance(item, dict) and _nonempty_string(item.get("id")))
            scope_reviews = _list(review.get("scopeFindings"))
            reviewed_scopes = {(item.get("scopeType"), item.get("scopeId")) for item in scope_reviews
                               if isinstance(item, dict) and _nonempty_string(item.get("scopeType"))
                               and _nonempty_string(item.get("scopeId"))}
            if (required_scopes != reviewed_scopes or len(scope_reviews) != len(reviewed_scopes)
                    or any(_object(item).get("status") != "approve"
                           or not _nonempty_string(_object(item).get("finding")) for item in scope_reviews)):
                _add(findings, "SCOPE_REVIEWS_UNRESOLVED", path,
                     "review must cover film and every declared sequence/chapter")



def validate_manifest(manifest: Any, manifest_path: Path, stage: str = "draft") -> list[Finding]:
    findings: list[Finding] = []
    if not isinstance(manifest, dict):
        return [Finding("INVALID_MANIFEST", "$", "top-level JSON value must be an object")]
    if stage not in ("draft", "publish"):
        return [Finding("INVALID_STAGE", "stage", "must be draft or publish")]
    _validate_timing(manifest, findings)
    asset_index = _validate_assets(manifest, manifest_path.parent, findings)
    _validate_storyboard(manifest, asset_index, findings)
    if stage == "publish":
        _validate_publish(manifest, manifest_path.parent, asset_index, findings)
    return findings


def _render_text(findings: Iterable[Finding], manifest_path: Path) -> str:
    rows = list(findings)
    if not rows:
        return f"OK: {manifest_path} passed deterministic project validation"
    lines = [f"FAIL: {manifest_path} has {len(rows)} validation issue(s)"]
    lines.extend(f"- {item.severity.upper()} {item.code} at {item.path}: {item.message}" for item in rows)
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate timing, assets, ordered storyboard direction, visual-job contracts, and artifact-bound publication reviews.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("manifest", type=Path, help="project-manifest JSON path")
    parser.add_argument("--json", action="store_true", help="emit machine-readable findings")
    parser.add_argument("--stage", choices=("draft", "publish"), default="draft", help="draft checks or artifact-bound publish gate (default: draft)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        finding = Finding("MANIFEST_READ_ERROR", "$", str(error))
        if args.json:
            print(json.dumps({"ok": False, "findings": [asdict(finding)]}, indent=2))
        else:
            print(f"FAIL: {finding.code}: {finding.message}", file=sys.stderr)
        return 1

    findings = validate_manifest(manifest, args.manifest.resolve(), args.stage)
    if args.json:
        print(json.dumps({"ok": not findings, "findings": [asdict(item) for item in findings]}, indent=2))
    else:
        print(_render_text(findings, args.manifest))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
