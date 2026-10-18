#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import io
import hashlib
import json
import struct
import sys
import tempfile
import unittest
import zlib
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_project", ROOT / "tools" / "validate_project.py")
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


def png(path: Path, color_type: int) -> None:
    channels = 4 if color_type == 6 else 3
    raw = b"\x00" + (b"\xff" * channels)

    def chunk(name: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + name + data + struct.pack(">I", zlib.crc32(name + data) & 0xFFFFFFFF)

    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, color_type, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )


def base_manifest(asset_file: str = "hero.png") -> dict:
    return {
        "composition": {"durationSec": 12.0, "toleranceSec": 0.05},
        "voiceover": {"endSec": 11.5},
        "captions": [{"id": "C1", "startSec": 0.0, "endSec": 11.5}],
        "scenes": [{"id": "S1", "startSec": 0.0, "durationSec": 12.0}],
        "finalHold": {
            "startSec": 11.5,
            "endSec": 12.0,
            "intentional": True,
            "reviewed": True,
            "reason": "Let the thesis land",
        },
        "assets": [
            {
                "id": "hero",
                "sceneIds": ["S1"],
                "role": "hero subject",
                "file": asset_file,
                "origin": "generated",
                "technicalStatus": "verified",
                "editorialStatus": "accepted",
                "rightsStatus": "self_created",
                "representationType": "metaphor",
                "requirements": {"requiresAlpha": True},
                "reviewEvidence": ["asset critic review"],
            }
        ],
        "storyboard": {
            "status": "frozen",
            "freezeEvidence": {
                "reviewer": "external-critic",
                "reviewRef": "review-1",
                "independent": True,
            },
            "scenes": [
                {
                    "id": "S1",
                    "beatIds": ["B1"],
                    "visualThesis": "The hero visibly changes state",
                    "focalPoint": "hero",
                    "dominantRelationship": "the before state transforms into the payoff",
                    "constructionFamily": "transformation",
                    "assetIds": ["hero"],
                    "states": [
                        {
                            "id": "anchor",
                            "purpose": "establish",
                            "focalElement": "hero",
                            "intentionalHoldReason": "make the starting state readable",
                        },
                        {
                            "id": "payoff",
                            "purpose": "resolve",
                            "focalElement": "hero",
                            "meaningfulChange": "the hero completes its transformation",
                        },
                    ],
                    "transitionIntent": "carry the transformed hero into the next scene",
                }
            ],
        },
        "implementation": {"scenes": [{"id": "S1", "stateIds": ["anchor", "payoff"]}]},
    }


def codes(findings) -> set[str]:
    return {finding.code for finding in findings}


class ValidateProjectTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        png(self.root / "hero.png", 6)
        self.manifest_path = self.root / "project-manifest.json"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def validate(self, manifest: dict):
        return VALIDATOR.validate_manifest(manifest, self.manifest_path)

    def test_complete_manifest_passes(self) -> None:
        self.assertEqual(self.validate(base_manifest()), [])

    def test_non_narrated_project_does_not_invent_a_dead_tail(self) -> None:
        manifest = base_manifest()
        manifest.pop("voiceover")
        manifest["captions"] = []
        manifest.pop("finalHold")
        self.assertEqual(self.validate(manifest), [])

    def test_timing_bounds_and_undeclared_tail_are_reported(self) -> None:
        manifest = base_manifest()
        manifest["composition"]["durationSec"] = 10.0
        manifest["voiceover"]["endSec"] = 10.5
        manifest["captions"][0]["endSec"] = 10.7
        manifest["scenes"][0]["durationSec"] = 11.0
        manifest.pop("finalHold")
        result = codes(self.validate(manifest))
        self.assertTrue(
            {"VOICEOVER_OUT_OF_BOUNDS", "CAPTION_OUT_OF_BOUNDS", "SCENE_OUT_OF_BOUNDS"}.issubset(result)
        )

        tail = base_manifest()
        tail["voiceover"]["endSec"] = 9.0
        tail["captions"][0]["endSec"] = 9.0
        tail.pop("finalHold")
        self.assertIn("UNDECLARED_FINAL_HOLD", codes(self.validate(tail)))

    def test_final_hold_must_be_explicit_reviewed_and_cover_the_tail(self) -> None:
        manifest = base_manifest()
        manifest["finalHold"] = {
            "startSec": 11.8,
            "endSec": 11.9,
            "intentional": False,
            "reviewed": False,
            "reason": "",
        }
        result = codes(self.validate(manifest))
        self.assertTrue(
            {
                "HOLD_GAP",
                "HOLD_END_MISMATCH",
                "HOLD_NOT_INTENTIONAL",
                "HOLD_NOT_REVIEWED",
                "MISSING_HOLD_REASON",
            }.issubset(result)
        )

    def test_asset_status_file_rights_and_alpha_checks(self) -> None:
        manifest = base_manifest("opaque.png")
        png(self.root / "opaque.png", 2)
        asset = manifest["assets"][0]
        asset["technicalStatus"] = "available"
        asset["rightsStatus"] = "verified"
        result = codes(self.validate(manifest))
        self.assertIn("ACCEPTED_ASSET_NOT_VERIFIED", result)
        self.assertIn("INCOMPLETE_RIGHTS_EVIDENCE", result)
        self.assertIn("ALPHA_REQUIRED", result)

        asset["technicalStatus"] = "verified"
        asset.pop("reviewEvidence")
        self.assertIn("ACCEPTED_ASSET_MISSING_REVIEW", codes(self.validate(manifest)))

        candidate = base_manifest()
        candidate["assets"] = [
            {
                "id": "candidate",
                "sceneIds": ["S1"],
                "role": "candidate hero",
                "origin": "generated",
                "technicalStatus": "candidate",
                "editorialStatus": "pending",
                "rightsStatus": "unresolved",
                "representationType": "metaphor",
            }
        ]
        candidate["storyboard"]["scenes"][0]["assetIds"] = ["candidate"]
        self.assertIn("FROZEN_ASSET_NOT_READY", codes(self.validate(candidate)))

        candidate["storyboard"]["status"] = "in_review"
        candidate["storyboard"].pop("freezeEvidence")
        self.assertEqual(self.validate(candidate), [])

    def test_verified_asset_requires_existing_file(self) -> None:
        manifest = base_manifest("missing.png")
        self.assertIn("ASSET_FILE_MISSING", codes(self.validate(manifest)))

    def test_frozen_storyboard_requires_complete_reviewed_scenes(self) -> None:
        manifest = base_manifest()
        manifest["storyboard"].pop("freezeEvidence")
        scene = manifest["storyboard"]["scenes"][0]
        scene["focalPoint"] = ""
        scene["states"] = [
            {"id": "hold", "purpose": "hold", "focalElement": "hero"},
            {"id": "hold", "purpose": "hold", "focalElement": "hero", "meaningfulChange": "moves"},
        ]
        result = codes(self.validate(manifest))
        self.assertIn("INCOMPLETE_FREEZE_EVIDENCE", result)
        self.assertIn("INCOMPLETE_FROZEN_SCENE", result)
        self.assertIn("DUPLICATE_ID", result)
        self.assertIn("INVALID_STATE_SEMANTICS", result)

        manifest = base_manifest()
        manifest["storyboard"]["freezeEvidence"]["independent"] = False
        self.assertIn("FREEZE_REVIEW_NOT_INDEPENDENT", codes(self.validate(manifest)))

    def test_storyboard_status_uses_canonical_review_values(self) -> None:
        manifest = base_manifest()
        manifest["storyboard"]["status"] = "in_review"
        manifest["storyboard"].pop("freezeEvidence")
        self.assertEqual(self.validate(manifest), [])

        ready = base_manifest()
        ready["storyboard"]["status"] = "ready_for_approval"
        ready["storyboard"].pop("freezeEvidence")
        ready["storyboard"]["reviewEvidence"] = {
            "reviewer": "external-critic",
            "reviewRef": "review-ready-1",
            "independent": True,
        }
        self.assertEqual(self.validate(ready), [])

        ready["storyboard"]["reviewEvidence"]["independent"] = False
        self.assertIn("REVIEW_NOT_INDEPENDENT", codes(self.validate(ready)))

        manifest["storyboard"]["status"] = "review"
        self.assertIn("INVALID_STORYBOARD_STATUS", codes(self.validate(manifest)))

    def test_frozen_storyboard_requires_every_planned_scene(self) -> None:
        manifest = base_manifest()
        manifest["scenes"].append({"id": "S2", "startSec": 11.5, "durationSec": 0.5})
        self.assertIn("STORYBOARD_SCENE_MISSING", codes(self.validate(manifest)))

    def test_storyboard_implementation_scene_and_state_mismatches(self) -> None:
        manifest = base_manifest()
        manifest["implementation"]["scenes"] = [
            {"id": "S1", "stateIds": ["payoff", "anchor", "extra"]},
            {"id": "S2", "stateIds": ["entry"]},
        ]
        result = codes(self.validate(manifest))
        self.assertIn("IMPLEMENTATION_SCENE_EXTRA", result)
        self.assertIn("IMPLEMENTATION_STATE_EXTRA", result)

        manifest["implementation"]["scenes"] = [{"id": "S1", "stateIds": ["payoff", "anchor"]}]
        self.assertIn("IMPLEMENTATION_STATE_ORDER_MISMATCH", codes(self.validate(manifest)))

        manifest["implementation"]["scenes"] = []
        self.assertIn("IMPLEMENTATION_SCENE_MISSING", codes(self.validate(manifest)))

    def test_cli_returns_nonzero_for_invalid_manifest_and_json_output(self) -> None:
        manifest = base_manifest()
        manifest.pop("finalHold")
        self.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(VALIDATOR.main([str(self.manifest_path), "--json"]), 1)

    def release(self, duration_sec=12.0, chaptered=False):
        manifest = base_manifest()
        manifest["composition"]["durationSec"] = duration_sec
        manifest["voiceover"]["endSec"] = duration_sec - 0.5
        manifest["captions"][0]["endSec"] = duration_sec - 0.5
        manifest["scenes"][0]["durationSec"] = duration_sec
        manifest["finalHold"].update(startSec=duration_sec - 0.5, endSec=duration_sec)
        board_scene = manifest["storyboard"]["scenes"][0]
        board_scene.update(visualJob="explanation", stateDelta={
            "before": "the system is flowing", "operation": "one route narrows",
            "after": "flow queues at the bottleneck",
            "viewerInference": "the system depends on this constrained route",
        })
        board_scene["vocabularyIds"] = ["route"]
        scene_ids = ["S1"]
        sequence_defs = [("Q1", ["S1"])]
        chapter_defs = [("C1", ["Q1"])] if chaptered else []
        if chaptered:
            scene_ids = ["S1", "S2", "S3", "S4"]
            for index, scene_id in enumerate(scene_ids[1:], start=1):
                scene = json.loads(json.dumps(board_scene))
                scene["id"] = scene_id
                scene["beatIds"] = [f"B{index + 1}"]
                scene["visualJob"] = "payoff" if index == 3 else "evidence"
                scene.pop("stateDelta", None)
                if scene["visualJob"] == "payoff":
                    scene["payoffConstruction"] = "hold on the queue after the route closes"
                manifest["storyboard"]["scenes"].append(scene)
            manifest["scenes"] = [
                {"id": scene_id, "startSec": index * duration_sec / 4, "durationSec": duration_sec / 4}
                for index, scene_id in enumerate(scene_ids)
            ]
            manifest["implementation"]["scenes"] = [
                {"id": scene_id, "stateIds": ["anchor", "payoff"]} for scene_id in scene_ids
            ]
            manifest["assets"][0]["sceneIds"] = scene_ids
            sequence_defs = [("Q1", ["S1", "S2"]), ("Q2", ["S3", "S4"])]
            chapter_defs = [("C1", ["Q1"]), ("C2", ["Q2"])]
        manifest["storyboard"]["direction"] = {
            "film": {"viewerPromise": "Understand the bottleneck", "argument": "one route constrains the system",
                     "emotionalProgression": "curiosity to concern", "conclusion": "capacity is the limit"},
            "sequences": [
                {"id": sequence_id, "sceneIds": sequence_scene_ids, "purpose": "show the bottleneck",
                 "payoffTrajectory": "narrowing route becomes accumulating queue",
                 "rhythmIntent": "hold a stable scale as density rises",
                 "repetitionAssessment": "repeated route images let the queue become legible"}
                for sequence_id, sequence_scene_ids in sequence_defs
            ],
            "vocabulary": [{"id": "route", "subjectIdentity": "shared route", "visualRole": "hero subject",
                            "viewpoint": "system overview", "representation": "metaphor", "assetIds": ["hero"]}],
        }
        if chapter_defs:
            manifest["storyboard"]["direction"]["chapters"] = [
                {"id": chapter_id, "sequenceIds": sequence_ids, "argumentTurn": "capacity becomes the story",
                 "evidenceBurden": "show the accumulated queue", "payoff": "the route is the constraint"}
                for chapter_id, sequence_ids in chapter_defs
            ]
        (self.root / "board.html").write_text("<h1>Frozen transformation</h1>")
        (self.root / "master.mp4").write_bytes(b"master fixture bytes")
        (self.root / "creation.txt").write_text("Original illustration; created for this production")
        png(self.root / "phone-frame.png", 6)
        png(self.root / "desktop-frame.png", 6)
        manifest["storyboard"]["preview"] = {"path": "board.html", "mode": "playable"}
        manifest["masterFile"] = "master.mp4"
        manifest["reviewReceipt"] = "release.json"
        manifest["assets"][0].update(sourceUri="creation.txt", rightsEvidence="creation.txt")
        receipt = {
            "producerContext": "director-session",
            "board": self.binding("board.html"),
            "master": self.binding("master.mp4"),
            "reviews": {},
        }
        for name, verdict in (("design", "approve"), ("editorial", "publish_candidate"), ("technical", "pass")):
            report = {
                "reviewContext": f"{name}-session", "overallStatus": verdict, "blockers": [],
                "boardSha256": receipt["board"]["sha256"],
            }
            if name != "design":
                report["masterSha256"] = receipt["master"]["sha256"]
            if name == "technical":
                report.update(runId="qa-1", checks=[{"id": "render", "status": "pass", "evidence": "decoded frames"}])
            else:
                scopes = [{"scopeType": "film", "scopeId": "film", "status": "approve",
                           "finding": "the argument resolves at film scale"}]
                scopes.extend({"scopeType": "sequence", "scopeId": sequence_id, "status": "approve",
                               "finding": "the sequence escalates to its local payoff"}
                              for sequence_id, _ in sequence_defs)
                scopes.extend({"scopeType": "chapter", "scopeId": chapter_id, "status": "approve",
                               "finding": "the chapter carries the capacity turn"}
                              for chapter_id, _ in chapter_defs)
                viewing_sizes = [
                    {"widthPx": 360 if duration_sec < 300 else 390,
                     "heightPx": 640 if duration_sec < 300 else 219,
                     "size": "portrait player" if duration_sec < 300 else "landscape phone player",
                     "distance": "arm's length", "observation": "the bottleneck remains legible",
                     "proofRef": "phone-frame.png", "proofSha256": self.binding("phone-frame.png")["sha256"]},
                    *([{"widthPx": 960, "heightPx": 540, "size": "desktop player",
                        "distance": "seated viewing", "observation": "the system hierarchy remains legible",
                        "proofRef": "desktop-frame.png", "proofSha256": self.binding("desktop-frame.png")["sha256"]}] if duration_sec >= 300 else []),
                ]
                report.update(
                    critic="independent-critic", independent=True, renderRefs=["board.html"],
                    sceneFindings=[{"sceneId": scene_id, "status": "approve", "findings": [],
                                    "checks": {key: True for key in (
                                        "thesisClear", "hierarchyClear", "visualJobSatisfied",
                                        "pacingResolved", "continuityResolved", "assetFit")},
                                    "viewingSizeEvidence": viewing_sizes}
                                   for scene_id in scene_ids],
                    scopeFindings=scopes,
                )
            (self.root / f"{name}.json").write_text(json.dumps(report))
            receipt["reviews"][name] = self.binding(f"{name}.json")
        (self.root / "release.json").write_text(json.dumps(receipt))
        return manifest

    def binding(self, filename):
        return {"file": filename, "sha256": hashlib.sha256((self.root / filename).read_bytes()).hexdigest()}

    def change_review(self, name, change):
        path = self.root / f"{name}.json"
        review = json.loads(path.read_text())
        change(review)
        path.write_text(json.dumps(review))
        receipt_path = self.root / "release.json"
        receipt = json.loads(receipt_path.read_text())
        receipt["reviews"][name] = self.binding(path.name)
        receipt_path.write_text(json.dumps(receipt))

    def publish(self, manifest):
        return VALIDATOR.validate_manifest(manifest, self.manifest_path, "publish")

    def test_draft_is_not_publish_and_valid_release_passes(self):
        draft = base_manifest()
        draft["storyboard"]["status"] = "draft"
        self.assertEqual(self.validate(draft), [])
        self.assertTrue({"PUBLISH_REQUIRES_FREEZE", "PUBLISH_RECEIPT_REQUIRED"} <= codes(self.publish(draft)))
        self.assertEqual(self.publish(self.release()), [])
        self.assertIn("INVALID_STAGE", codes(VALIDATOR.validate_manifest(draft, self.manifest_path, "typo")))

    def test_release_rejects_changed_artifact_or_missing_file(self):
        for filename in ("board.html", "master.mp4", "design.json", "editorial.json", "technical.json"):
            with self.subTest(filename=filename):
                manifest = self.release()
                (self.root / filename).write_bytes(b"changed after review")
                self.assertIn("STALE_ARTIFACT", codes(self.publish(manifest)))
        manifest = self.release()
        (self.root / "editorial.json").unlink()
        self.assertIn("ARTIFACT_READ_ERROR", codes(self.publish(manifest)))

    def test_release_rejects_negative_missing_or_self_review(self):
        cases = [
            ("editorial", lambda r: r.update(overallStatus="revise"), "REVIEW_NOT_APPROVED"),
            ("technical", lambda r: r.update(blockers=["decode error"]), "REVIEW_NOT_APPROVED"),
            ("design", lambda r: r.update(independent=False), "REVIEW_NOT_INDEPENDENT"),
            ("editorial", lambda r: r.update(reviewContext="director-session"), "REVIEW_NOT_INDEPENDENT"),
            ("editorial", lambda r: r.pop("reviewContext"), "MISSING_REVIEW_CONTEXT"),
            ("editorial", lambda r: r.pop("renderRefs"), "REVIEW_EVIDENCE_MISSING"),
            ("design", lambda r: r.update(renderRefs=["missing-frame.png"]), "REVIEW_EVIDENCE_MISSING"),
            ("technical", lambda r: r.update(masterSha256="0" * 64), "REVIEW_ARTIFACT_MISMATCH"),
            ("design", lambda r: r.update(boardSha256="0" * 64), "REVIEW_ARTIFACT_MISMATCH"),
            ("editorial", lambda r: r["sceneFindings"][0].update(status="revise"), "EDITORIAL_CHECKS_UNRESOLVED"),
            ("technical", lambda r: r["checks"][0].update(status="fail"), "TECHNICAL_CHECKS_UNRESOLVED"),
        ]
        for name, change, expected in cases:
            with self.subTest(expected=expected, name=name):
                manifest = self.release()
                self.change_review(name, change)
                self.assertIn(expected, codes(self.publish(manifest)))
        for receipt in ({}, [], {"board": True}):
            manifest = self.release()
            (self.root / "release.json").write_text(json.dumps(receipt))
            self.assertIn("INVALID_ARTIFACT_BINDING", codes(self.publish(manifest)))

    def test_v010_publication_envelopes_are_artifact_bound(self):
        for duration, chaptered in ((55.0, False), (300.0, False), (900.0, True)):
            with self.subTest(duration=duration):
                self.assertEqual(self.publish(self.release(duration, chaptered)), [])

    def test_publish_requires_populated_visual_vocabulary(self):
        for present, vocabulary in ((False, None), (True, []), (True, None), (True, {})):
            with self.subTest(present=present, vocabulary=vocabulary):
                manifest = self.release()
                direction = manifest["storyboard"]["direction"]
                if present:
                    direction["vocabulary"] = vocabulary
                else:
                    direction.pop("vocabulary")
                for scene in manifest["storyboard"]["scenes"]:
                    scene.pop("vocabularyIds")
                self.assertEqual(self.validate(manifest), [])
                self.assertIn("PUBLISH_REQUIRES_VOCABULARY", codes(self.publish(manifest)))

    def test_direction_partitions_and_vocabulary_bindings(self):
        manifest = self.release()
        manifest["storyboard"]["direction"]["sequences"][0]["sceneIds"] = ["missing"]
        self.assertIn("SEQUENCE_PARTITION_MISMATCH", codes(self.validate(manifest)))
        manifest = self.release()
        manifest["storyboard"]["direction"]["vocabulary"][0]["assetIds"] = ["missing"]
        self.assertIn("UNKNOWN_VOCABULARY_ASSET", codes(self.validate(manifest)))
        manifest = self.release()
        manifest["storyboard"]["scenes"][0]["vocabularyIds"] = ["unknown"]
        self.assertIn("UNKNOWN_VOCABULARY_REFERENCE", codes(self.validate(manifest)))

        manifest = self.release()
        board = manifest["storyboard"]
        second = json.loads(json.dumps(board["scenes"][0]))
        second["id"] = "S2"
        second["beatIds"] = ["B2"]
        board["scenes"].append(second)
        manifest["scenes"].append({"id": "S2", "startSec": 12, "durationSec": 4})
        manifest["composition"]["durationSec"] = 16
        manifest["voiceover"]["endSec"] = 15.5
        manifest["captions"][0]["endSec"] = 15.5
        manifest["finalHold"].update(startSec=15.5, endSec=16)
        board["status"] = "draft"
        board.pop("freezeEvidence")
        board["direction"]["sequences"][0]["sceneIds"] = ["S1", "S2"]
        board["direction"]["sequences"][0]["repetitionAssessment"] = "same family persists to make the accumulating constraint easy to compare"
        manifest.pop("implementation")
        self.assertEqual(self.validate(manifest), [])

        ordered = self.release()
        ordered["storyboard"]["status"] = "draft"
        ordered["storyboard"].pop("freezeEvidence")
        ordered["storyboard"]["scenes"].append({"id": "S2"})
        ordered["scenes"].append({"id": "S2", "startSec": 12, "durationSec": 1})
        ordered["storyboard"]["direction"]["sequences"] = [
            {"id": "Q1", "sceneIds": ["S2"], "purpose": "later", "payoffTrajectory": "later",
             "rhythmIntent": "later", "repetitionAssessment": "later"},
            {"id": "Q2", "sceneIds": ["S1"], "purpose": "earlier", "payoffTrajectory": "earlier",
             "rhythmIntent": "earlier", "repetitionAssessment": "earlier"},
        ]
        self.assertIn("SEQUENCE_PARTITION_MISMATCH", codes(self.validate(ordered)))
        ordered["storyboard"]["direction"]["chapters"] = [
            {"id": "C1", "sequenceIds": ["Q2", "Q1"], "argumentTurn": "turn", "evidenceBurden": "proof",
             "payoff": "resolution"}
        ]
        self.assertIn("CHAPTER_PARTITION_MISMATCH", codes(self.validate(ordered)))
        duplicate = self.release()
        duplicate["storyboard"]["direction"]["sequences"][0]["sceneIds"] = ["S1", "S1"]
        self.assertIn("DUPLICATE_SEQUENCE_SCENE", codes(self.validate(duplicate)))

    def test_conditional_state_delta_and_concept_search(self):
        manifest = self.release()
        scene = manifest["storyboard"]["scenes"][0]
        scene["visualJob"] = "evidence"
        scene.pop("stateDelta")
        self.assertNotIn("INCOMPLETE_STATE_DELTA", codes(self.validate(manifest)))
        scene.update(visualJob="explanation", stateDelta={"before": "flow", "after": "queue"})
        self.assertIn("INCOMPLETE_STATE_DELTA", codes(self.validate(manifest)))
        scene["stateDelta"] = {"before": "flow", "operation": "route narrows", "after": "queue",
                               "viewerInference": "the route is constrained"}
        scene["conceptSearch"] = {
            "candidates": [
                {"id": "A", "family": "diagram", "inference": "route constrains flow", "description": "narrowing path"},
                {"id": "B", "family": "spatial", "inference": "route constrains flow", "description": "crowded corridor"},
            ],
            "selectedId": "missing", "selectionReason": "better readability",
        }
        self.assertIn("INVALID_SELECTED_CONCEPT", codes(self.validate(manifest)))
        scene["conceptSearch"]["selectedId"] = "A"
        scene["conceptSearch"]["candidates"][1]["family"] = "diagram"
        self.assertIn("CONCEPT_FAMILIES_NOT_DISTINCT", codes(self.validate(manifest)))

    def test_publish_requires_independent_scope_and_viewing_size_proof(self):
        manifest = self.release(900, chaptered=True)
        self.assertEqual(self.publish(manifest), [])
        self.change_review("editorial", lambda report: report.pop("scopeFindings"))
        self.assertIn("SCOPE_REVIEWS_UNRESOLVED", codes(self.publish(manifest)))
        manifest = self.release(900, chaptered=True)
        self.change_review("editorial", lambda report: report["scopeFindings"][0].update(status="revise"))
        self.assertIn("SCOPE_REVIEWS_UNRESOLVED", codes(self.publish(manifest)))
        manifest = self.release(900, chaptered=True)
        self.change_review("editorial", lambda report: report["sceneFindings"][0]["viewingSizeEvidence"][0].update(
            proofRef="missing-frame.png"))
        self.assertIn("ARTIFACT_READ_ERROR", codes(self.publish(manifest)))

    def test_malformed_direction_values_return_findings(self):
        for field in ("id", "family"):
            manifest = self.release()
            manifest["storyboard"]["scenes"][0]["conceptSearch"] = {
                "candidates": [
                    {"id": "A", "family": "diagram", "inference": "capacity limits flow", "description": "narrowing route"},
                    {"id": "B", "family": "accumulation", "inference": "capacity limits flow", "description": "growing queue", field: []},
                ],
                "selectedId": "A", "selectionReason": "the stable route makes the limit visible",
            }
            self.assertIn("INCOMPLETE_CONCEPT", codes(self.validate(manifest)))
        manifest = self.release()
        manifest["storyboard"]["scenes"][0].update(visualJob="evidence", stateDelta={"before": "source"})
        self.assertIn("INCOMPLETE_STATE_DELTA", codes(self.validate(manifest)))
        manifest = self.release()
        manifest["storyboard"]["scenes"][0]["visualJob"] = []
        self.assertIn("PUBLISH_REQUIRES_VISUAL_JOB", codes(self.publish(manifest)))
        manifest = self.release()
        manifest["storyboard"]["scenes"][0]["vocabularyIds"] = [{}]
        self.assertIn("UNKNOWN_VOCABULARY_REFERENCE", codes(self.validate(manifest)))
        manifest = self.release()
        manifest["storyboard"]["direction"]["vocabulary"][0]["assetIds"] = [{}]
        self.assertIn("INVALID_VOCABULARY_ASSETS", codes(self.validate(manifest)))
        manifest = self.release()
        self.change_review("editorial", lambda report: report["scopeFindings"][0].update(scopeType=[]))
        self.assertIn("SCOPE_REVIEWS_UNRESOLVED", codes(self.publish(manifest)))
        manifest = self.release()
        manifest["storyboard"]["direction"]["vocabulary"][0]["representation"] = "authentic-looking"
        self.assertIn("INVALID_VOCABULARY_REPRESENTATION", codes(self.validate(manifest)))
        manifest["storyboard"]["direction"]["vocabulary"][0].update(representation="metaphor", assetIds=["hero", "hero"])
        self.assertIn("DUPLICATE_VOCABULARY_ASSET", codes(self.validate(manifest)))

    def test_vocabulary_only_assets_obey_publication_lifecycle(self):
        manifest = self.release()
        for scene in manifest["storyboard"]["scenes"]:
            scene["assetIds"] = []
            for state in scene["states"]:
                state.pop("assetIds", None)
        asset = manifest["assets"][0]
        asset["sceneIds"] = []
        asset["role"] = "recurring route detail"
        self.assertEqual(self.publish(manifest), [])
        asset.update(technicalStatus="candidate", editorialStatus="pending")
        self.assertIn("PUBLISH_ASSET_NOT_READY", codes(self.publish(manifest)))
        asset.update(technicalStatus="verified", editorialStatus="accepted", rightsStatus="unresolved")
        self.assertIn("PUBLISH_RIGHTS_UNRESOLVED", codes(self.publish(manifest)))
        asset["rightsStatus"] = "self_created"
        asset.pop("sourceUri")
        self.assertIn("PUBLISH_PROVENANCE_MISSING", codes(self.publish(manifest)))

    def test_viewing_proof_identity_is_bound_to_review(self):
        manifest = self.release()
        self.assertEqual(self.publish(manifest), [])
        (self.root / "phone-frame.png").write_bytes(b"changed after independent review")
        self.assertIn("STALE_ARTIFACT", codes(self.publish(manifest)))
        manifest = self.release()
        self.change_review("editorial", lambda report: report["sceneFindings"][0]["viewingSizeEvidence"][0].pop("proofSha256"))
        self.assertIn("INVALID_ARTIFACT_BINDING", codes(self.publish(manifest)))

    def test_used_asset_release_rights_and_provenance(self):
        for status in ("unresolved", "needs_review"):
            manifest = self.release()
            manifest["assets"][0]["rightsStatus"] = status
            self.assertEqual(self.validate(manifest), [])
            self.assertIn("PUBLISH_RIGHTS_UNRESOLVED", codes(self.publish(manifest)))
        manifest = self.release()
        manifest["assets"][0].pop("sourceUri")
        self.assertIn("PUBLISH_PROVENANCE_MISSING", codes(self.publish(manifest)))
        manifest = self.release()
        manifest["implementation"]["scenes"][0]["assetIds"] = ["missing"]
        self.assertIn("UNKNOWN_ASSET_REFERENCE", codes(self.publish(manifest)))
        manifest = self.release()
        manifest["assets"].append({"id": "unused", "origin": "sourced", "technicalStatus": "candidate",
                                   "editorialStatus": "pending", "rightsStatus": "unresolved",
                                   "representationType": "literal", "sceneIds": []})
        self.assertEqual(self.publish(manifest), [])

    def test_evidence_requires_honest_origin_and_supported_claim(self):
        manifest = base_manifest()
        asset = manifest["assets"][0]
        asset.update(representationType="evidence", sourceUri="https://archive.example/item", claimIds=["claim"])
        manifest["claimSet"] = {
            "sources": [{"id": "source", "title": "Archive", "url": "https://archive.example/item"}],
            "claims": [{"id": "claim", "claim": "The product existed", "status": "verified", "sourceRefs": ["source"]}],
        }
        for origin in ("generated", "reconstructed"):
            asset["origin"] = origin
            self.assertIn("COUNTERFEIT_EVIDENCE", codes(self.validate(manifest)))
        for origin in ("sourced", "programmatic", "reused"):
            asset["origin"] = origin
            self.assertEqual(self.validate(manifest), [])
        manifest["claimSet"]["claims"][0]["sourceRefs"] = ["missing"]
        self.assertIn("UNSUPPORTED_EVIDENCE_CLAIM", codes(self.validate(manifest)))
        asset.update(origin="reconstructed", representationType="reconstruction")
        self.assertEqual(self.validate(manifest), [])
        asset.update(representationType="evidence")
        asset.pop("claimIds")
        self.assertIn("INCOMPLETE_EVIDENCE", codes(self.validate(manifest)))

    def test_semantic_windows_and_cue_disposition(self):
        manifest = base_manifest()
        timing = {"phrase": "the transformation resolves", "orientationStartSec": 0, "triggerSec": 2,
                  "actionCompleteSec": 4, "readableStartSec": 4.2, "readableEndSec": 6,
                  "transitionStartSec": 5.5, "transitionEndSec": 7}
        manifest["scenes"][0]["microbeats"] = [{"semanticTiming": timing}]
        manifest["scenes"][0]["sfxEvents"] = [{"disposition": "omitted", "decisionReason": "deliberate silence"}]
        self.assertEqual(self.validate(manifest), [])
        for field, value, code in (("actionCompleteSec", 8, "INVALID_SEMANTIC_ORDER"),
                                   ("readableEndSec", 4.2, "INVALID_SEMANTIC_ORDER"),
                                   ("transitionEndSec", 13, "INVALID_SEMANTIC_TIMING"),
                                   ("triggerSec", float("nan"), "INVALID_SEMANTIC_TIMING")):
            old = timing[field]
            timing[field] = value
            self.assertIn(code, codes(self.validate(manifest)))
            timing[field] = old
        manifest["scenes"][0]["sfxEvents"][0].pop("decisionReason")
        self.assertIn("INVALID_CUE_DISPOSITION", codes(self.validate(manifest)))

    def test_readability_can_overlap_action_and_transition(self):
        manifest = base_manifest()
        manifest["scenes"][0]["microbeats"] = [{"semanticTiming": {
            "phrase": "the comparison remains readable while moving",
            "orientationStartSec": 0, "triggerSec": 1, "actionCompleteSec": 5,
            "readableStartSec": 3, "readableEndSec": 6,
            "transitionStartSec": 5.5, "transitionEndSec": 7,
        }}]
        self.assertEqual(self.validate(manifest), [])

    def test_cli_publish_is_explicit(self):
        manifest = self.release()
        self.manifest_path.write_text(json.dumps(manifest))
        with redirect_stdout(io.StringIO()):
            self.assertEqual(VALIDATOR.main([str(self.manifest_path), "--stage", "publish", "--json"]), 0)
        manifest["assets"][0]["rightsStatus"] = "unresolved"
        self.manifest_path.write_text(json.dumps(manifest))
        with redirect_stdout(io.StringIO()):
            self.assertEqual(VALIDATOR.main([str(self.manifest_path)]), 0)
            self.assertEqual(VALIDATOR.main([str(self.manifest_path), "--stage", "publish"]), 1)

    def test_defining_promises_need_observable_proof_and_complete_score(self):
        manifest = base_manifest()
        scene = manifest["storyboard"]["scenes"][0]
        scene["relationshipInvariants"] = [{"id": "match", "observable": "carrier stays registered",
                                           "proofRef": "boundary.mp4 at 2-3s"}]
        scene["shotScore"] = {"composition": "carrier dominates", "objectAction": "carrier releases image",
                              "camera": "locked", "attention": "image", "rhythm": "resolve and hold",
                              "sound": "silence", "exit": "hard cut"}
        self.assertEqual(self.validate(manifest), [])
        scene["relationshipInvariants"][0].pop("proofRef")
        scene["shotScore"].pop("camera")
        self.assertTrue({"INCOMPLETE_RELATIONSHIP_INVARIANT", "INCOMPLETE_SHOT_SCORE"} <= codes(self.validate(manifest)))

    def test_first_party_documentary_evidence_can_publish(self):
        manifest = self.release()
        asset = manifest["assets"][0]
        asset.update(origin="reused", representationType="evidence", claimIds=["C1"])
        manifest["claimSet"] = {
            "sources": [{"id": "source", "title": "First-party record", "url": "creation.txt"}],
            "claims": [{"id": "C1", "claim": "This object was photographed", "status": "verified", "sourceRefs": ["source"]}],
        }
        self.assertEqual(self.publish(manifest), [])


if __name__ == "__main__":
    unittest.main()
