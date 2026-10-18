#!/usr/bin/env python3
from pathlib import Path
import json

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"

def load(name):
    return json.loads((SCHEMAS / name).read_text())
def registry():
    resources = []
    for path in SCHEMAS.glob("*.schema.json"):
        schema = json.loads(path.read_text())
        uri = schema.get("$id", f"https://vox-motion-graphics.local/schemas/{path.name}")
        resources.append((uri, Resource.from_contents(schema)))
    return Registry().with_resources(resources)


REGISTRY = registry()


def validator(name):
    schema = load(name)
    return Draft202012Validator(schema, registry=REGISTRY)


def assert_valid(schema_name, obj):
    validator(schema_name).validate(obj)


def assert_invalid(schema_name, obj):
    errors = list(validator(schema_name).iter_errors(obj))
    assert errors, f"expected {schema_name} to reject object"


def storyboard():
    return {
        "projectId": "p",
        "preview": {"path": "storyboard/index.html", "mode": "playable"},
        "status": "frozen",
        "freezeEvidence": {
            "reviewer": "independent-critic",
            "reviewRef": "review-01",
            "independent": True,
        },
        "scenes": [
            {
                "id": "S1",
                "beatIds": ["B1"],
                "visualThesis": "One route becomes the bottleneck for the whole system",
                "focalPoint": "flow through the narrow gate",
                "dominantRelationship": "many inputs depend on one constrained route",
                "constructionFamily": "constraint",
                "assetIds": ["route"],
                "states": [
                    {
                        "id": "anchor",
                        "purpose": "establish flow",
                        "focalElement": "moving inputs",
                        "meaningfulChange": "inputs enter the shared route",
                        "assetIds": ["route"],
                    },
                    {
                        "id": "payoff",
                        "purpose": "show consequence",
                        "focalElement": "blocked gate",
                        "meaningfulChange": "flow queues and depletes downstream",
                        "assetIds": ["route"],
                    },
                ],
                "transitionIntent": "follow the last output into the next system",
            }
        ],
    }


def main():
    schema_files = sorted(SCHEMAS.glob("*.schema.json"))
    for path in schema_files:
        Draft202012Validator.check_schema(json.loads(path.read_text()))

    assert_valid("storyboard-plan.schema.json", storyboard())
    no_freeze = storyboard()
    no_freeze.pop("freezeEvidence")
    assert_invalid("storyboard-plan.schema.json", no_freeze)
    self_frozen = storyboard()
    self_frozen["freezeEvidence"]["independent"] = False
    assert_invalid("storyboard-plan.schema.json", self_frozen)
    no_change = storyboard()
    no_change["scenes"][0]["states"][0].pop("meaningfulChange")
    assert_invalid("storyboard-plan.schema.json", no_change)

    explanation = storyboard()
    explanation["scenes"][0].update(visualJob="explanation", stateDelta={
        "before": "full flow", "operation": "one gate narrows", "after": "queue forms",
        "viewerInference": "the system depends on this bottleneck",
    })
    assert_valid("storyboard-plan.schema.json", explanation)
    malformed_delta = json.loads(json.dumps(explanation))
    malformed_delta["scenes"][0]["stateDelta"].pop("operation")
    assert_invalid("storyboard-plan.schema.json", malformed_delta)
    stillness = storyboard()
    stillness["scenes"][0]["visualJob"] = "evidence"
    assert_valid("storyboard-plan.schema.json", stillness)

    directional = storyboard()
    directional["direction"] = {
        "film": {"viewerPromise": "Understand the bottleneck", "argument": "one route constrains the system",
                 "emotionalProgression": "curiosity to concern", "conclusion": "capacity is the limit"},
        "sequences": [{"id": "Q1", "sceneIds": ["S1"], "purpose": "show the bottleneck",
                       "payoffTrajectory": "route narrows into consequence", "rhythmIntent": "hold scale",
                       "repetitionAssessment": "repeated route diagrams clarify the accumulating queue"}],
    }
    assert_valid("storyboard-plan.schema.json", directional)
    story_plan = {
        "project": {"topic": "bottlenecks", "targetPlatforms": ["web"], "targetDurationSec": 55},
        "story": {"angle": "one route changes everything", "hook": "Where does flow stop?",
                  "thesis": "capacity is the constraint", "causalSpine": ["route narrows", "queue grows"],
                  "payoff": "the route sets the limit",
                  "beats": [{"id": "B1", "purpose": "explain", "viewerQuestionIn": "where?",
                             "viewerQuestionOut": "why?", "emotion": "concern", "claimIds": []}]},
        "narration": {"text": "The route narrows.", "estimatedWordCount": 3},
        "direction": directional["direction"],
    }
    assert_valid("story-plan.schema.json", story_plan)
    directional["direction"]["sequences"][0]["sceneIds"] = []
    assert_invalid("storyboard-plan.schema.json", directional)

    packet = {
        "projectId": "p", "packetType": "ScenePacket",
        "frozenBoard": {"file": "board.html", "sha256": "a" * 64},
        "scope": {"id": "S1", "sceneIds": ["S1"]},
        "context": {"objective": "show the bottleneck", "constraints": ["keep existing typography"]},
        "artifacts": [], "evidence": [],
        "style": {"visualLanguage": "cut paper, restrained navy"},
        "timing": {"startSec": 0, "durationSec": 4, "beats": [{"id": "B1", "startSec": 0, "endSec": 4}]},
        "assets": [], "neighbors": {"next": {"sceneId": "S2", "handoff": "contrast"}},
    }
    assert_valid("implementation-packet.schema.json", packet)
    unfrozen_packet = json.loads(json.dumps(packet))
    unfrozen_packet.pop("frozenBoard")
    assert_invalid("implementation-packet.schema.json", unfrozen_packet)
    long_packet = json.loads(json.dumps(packet))
    long_packet["packetType"] = "SequencePacket"
    assert_valid("implementation-packet.schema.json", long_packet)
    long_packet["scope"]["sceneIds"] = ["S1", "S2"]
    assert_valid("implementation-packet.schema.json", long_packet)
    long_packet["packetType"] = "ScenePacket"
    assert_invalid("implementation-packet.schema.json", long_packet)
    invalid_timing = json.loads(json.dumps(packet))
    invalid_timing["timing"]["startSec"] = -1
    assert_invalid("implementation-packet.schema.json", invalid_timing)
    invalid_digest = json.loads(json.dumps(packet))
    invalid_digest["frozenBoard"]["sha256"] = "stale"
    assert_invalid("implementation-packet.schema.json", invalid_digest)
    scored = storyboard()
    scored["scenes"][0]["relationshipInvariants"] = [
        {"id": "carrier", "observable": "image stays registered as carrier departs", "proofRef": "boundary clip 00:04-00:06"}
    ]
    scored["scenes"][0]["shotScore"] = {
        "composition": "image dominates", "objectAction": "carrier departs", "camera": "locked",
        "attention": "image to departing carrier", "rhythm": "resolve then hold",
        "sound": "texture stops", "exit": "hard cut resets scale",
    }
    assert_valid("storyboard-plan.schema.json", scored)
    scored["scenes"][0]["relationshipInvariants"][0].pop("observable")
    assert_invalid("storyboard-plan.schema.json", scored)

    ready = storyboard()
    ready["status"] = "ready_for_approval"
    ready.pop("freezeEvidence")
    ready["reviewEvidence"] = {
        "reviewer": "independent-critic",
        "reviewRef": "review-ready-01",
        "independent": True,
    }
    assert_valid("storyboard-plan.schema.json", ready)
    ready.pop("reviewEvidence")
    assert_invalid("storyboard-plan.schema.json", ready)

    candidate = {
        "projectId": "p",
        "assets": [
            {
                "id": "hero",
                "sceneIds": ["S1"],
                "role": "illustrative hero",
                "origin": "generated",
                "technicalStatus": "candidate",
                "editorialStatus": "pending",
                "rightsStatus": "self_created",
                "representationType": "metaphor",
            }
        ],
    }
    assert_valid("asset-manifest.schema.json", candidate)

    accepted = json.loads(json.dumps(candidate))
    asset = accepted["assets"][0]
    asset.update(
        {
            "technicalStatus": "verified",
            "editorialStatus": "accepted",
            "file": "assets/hero.png",
            "reviewEvidence": ["storyboard-freeze-01"],
        }
    )
    assert_valid("asset-manifest.schema.json", accepted)

    not_verified = json.loads(json.dumps(accepted))
    not_verified["assets"][0]["technicalStatus"] = "available"
    assert_invalid("asset-manifest.schema.json", not_verified)

    rights = json.loads(json.dumps(accepted))
    rights["assets"][0]["rightsStatus"] = "verified"
    assert_invalid("asset-manifest.schema.json", rights)

    evidence = json.loads(json.dumps(accepted))
    evidence["assets"][0]["representationType"] = "evidence"
    assert_invalid("asset-manifest.schema.json", evidence)
    evidence["assets"][0].update(claimIds=["C1"], sourceUri="https://archive.example/source")
    assert_invalid("asset-manifest.schema.json", evidence)
    evidence["assets"][0]["origin"] = "programmatic"
    assert_valid("asset-manifest.schema.json", evidence)
    evidence["assets"][0]["origin"] = "sourced"
    assert_valid("asset-manifest.schema.json", evidence)
    evidence["assets"][0].update(origin="reconstructed", representationType="reconstruction")
    assert_valid("asset-manifest.schema.json", evidence)

    timing = {
        "fps": 30,
        "alignmentSource": "voiceover-alignment.json",
        "compositionDurationSec": 12,
        "voiceoverEndSec": 11.5,
        "captionEndSec": 11.5,
        "finalHold": {
            "startSec": 11.5,
            "endSec": 12,
            "intentional": True,
            "reviewed": True,
            "reason": "let the thesis land",
        },
        "scenes": [
            {
                "sceneId": "S1",
                "sceneStartSec": 0,
                "sceneDurationSec": 12,
                "microbeats": [
                    {
                        "offsetSec": 0,
                        "event": "establish flow",
                        "motionRole": "primary",
                        "storyboardStateId": "anchor",
                    }
                ],
            }
        ],
    }
    assert_valid("frame-scene-spec.schema.json", timing)
    timing["scenes"][0]["microbeats"][0]["semanticTiming"] = {
        "phrase": "flow stops", "orientationStartSec": 0, "triggerSec": 2,
        "actionCompleteSec": 3, "readableStartSec": 3.2, "readableEndSec": 5,
        "transitionStartSec": 4.5, "transitionEndSec": 6,
    }
    timing["scenes"][0]["sfxEvents"] = [{
        "offsetSec": 2, "visualEvent": "gate closes", "sfx": "planned impact",
        "disposition": "omitted", "decisionReason": "silence makes the stop perceptible",
    }]
    assert_valid("frame-scene-spec.schema.json", timing)
    timing["scenes"][0]["sfxEvents"][0].pop("decisionReason")
    assert_invalid("frame-scene-spec.schema.json", timing)

    editorial = {
        "critic": "critic-agent",
        "independent": True,
        "renderRefs": ["contact-sheet.png"],
        "overallStatus": "publish_candidate",
        "sceneFindings": [
            {
                "sceneId": "S1",
                "status": "approve",
                "checks": {
                    "thesisClear": True,
                    "hierarchyClear": True,
                    "visualJobSatisfied": True,
                    "pacingResolved": True,
                    "continuityResolved": True,
                    "assetFit": True,
                },
                "viewingSizeEvidence": [{"widthPx": 360, "heightPx": 640, "size": "portrait player", "distance": "arm's length",
                                         "observation": "label reads", "proofRef": "phone-frame.png", "proofSha256": "a" * 64}],
                "findings": [],
            }
        ],
        "scopeFindings": [{"scopeType": "film", "scopeId": "film", "status": "approve", "finding": "argument resolves"}],
    }
    assert_valid("editorial-qa-report.schema.json", editorial)
    for status in ("approve", "publish_candidate"):
        approved = json.loads(json.dumps(editorial))
        approved["overallStatus"] = status
        assert_valid("editorial-qa-report.schema.json", approved)
        approved.pop("scopeFindings")
        assert_invalid("editorial-qa-report.schema.json", approved)
        approved["scopeFindings"] = []
        assert_invalid("editorial-qa-report.schema.json", approved)
    for status in ("revise", "redesign", "needs_review"):
        incomplete = json.loads(json.dumps(editorial))
        incomplete["overallStatus"] = status
        incomplete.pop("scopeFindings")
        assert_valid("editorial-qa-report.schema.json", incomplete)
        incomplete["scopeFindings"] = []
        assert_valid("editorial-qa-report.schema.json", incomplete)
    self_approved = json.loads(json.dumps(editorial))
    self_approved["independent"] = False
    assert_invalid("editorial-qa-report.schema.json", self_approved)
    unresolved_editorial = json.loads(json.dumps(editorial))
    unresolved_editorial["sceneFindings"][0]["checks"]["hierarchyClear"] = False
    assert_invalid("editorial-qa-report.schema.json", unresolved_editorial)

    technical = {
        "runId": "qa-01",
        "overallStatus": "pass",
        "checks": [{"id": "render", "status": "pass", "evidence": "render exited 0"}],
    }
    assert_valid("technical-qa-report.schema.json", technical)
    false_pass = json.loads(json.dumps(technical))
    false_pass["checks"][0]["status"] = "fail"
    assert_invalid("technical-qa-report.schema.json", false_pass)
    editorial.update(reviewContext="critic-session", boardSha256="a" * 64, masterSha256="b" * 64, blockers=[])
    assert_valid("editorial-qa-report.schema.json", editorial)
    editorial["blockers"] = ["unresolved label"]
    assert_invalid("editorial-qa-report.schema.json", editorial)
    technical["blockers"] = ["decode failure"]
    assert_invalid("technical-qa-report.schema.json", technical)
    receipt = {
        "producerContext": "director-session",
        "board": {"file": "board.html", "sha256": "a" * 64},
        "master": {"file": "master.mp4", "sha256": "b" * 64},
        "reviews": {name: {"file": f"{name}.json", "sha256": "c" * 64}
                    for name in ("design", "editorial", "technical")},
    }
    assert_valid("review-receipt.schema.json", receipt)
    receipt["reviews"]["editorial"]["sha256"] = "approval"
    assert_invalid("review-receipt.schema.json", receipt)

    reference = {
        "referenceId": "ref1",
        "scenes": [
            {
                "id": "S1",
                "semanticJob": "reveal",
                "constructionFamily": "portal",
                "visualThesis": "frame becomes world",
                "mechanism": "weld-detach",
            }
        ],
        "findings": [
            {
                "finding": "few assets, high choreography",
                "classification": "creator_dna",
                "confidence": "high",
                "evidenceSceneIds": ["S1"],
            }
        ],
    }
    assert_valid("reference-analysis.schema.json", reference)

    tune = {
        "projectId": "p",
        "scenes": [
            {
                "sceneId": "S1",
                "parameters": [
                    {
                        "name": "heroScale",
                        "type": "number",
                        "currentValue": 1.0,
                        "min": 0.5,
                        "max": 2.0,
                        "step": 0.05,
                        "allowedValues": None,
                        "semanticRole": "focal hierarchy",
                        "repairPriority": "high",
                        "studioExposed": True,
                    }
                ],
            }
        ],
    }
    assert_valid("tunable-parameter-manifest.schema.json", tune)

    patch = {
        "critic": "vision-critic",
        "renderId": "r1",
        "changes": [
            {
                "sceneId": "S1",
                "parameter": "heroScale",
                "oldValue": 1.0,
                "newValue": 1.15,
                "reason": "hero too weak",
                "expectedEffect": "stronger focal hierarchy",
                "confidence": "high",
            }
        ],
        "requiresRedesign": False,
        "redesignReason": None,
    }
    assert_valid("parameter-patch.schema.json", patch)

    print(f"OK: {len(schema_files)} schemas + behavioral guardrails")


if __name__ == "__main__":
    main()
