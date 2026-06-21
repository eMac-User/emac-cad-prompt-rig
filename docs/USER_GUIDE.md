# User Guide — eMachination CAD Patent Prompt-Rig

## Daily Workflow

1. Start the board with `launchers\Start eMachination CAD Patent Prompt-Rig.bat`.
2. Press `ScrollLock` to open the board.
3. Press `NumLock` to cycle profiles.
4. Press `Pause / Break` to cycle boards.
5. Click a prompt slot to copy/use the matching Markdown prompt body.
6. Press `F5` while focused after editing prompt files.

## Recommended Flow

```text
rough idea / sketch / CAD screenshot / invention note
        ↓
Rough-In / Part Development
        ↓
Mechanical Drawing Cleanup
        ↓
CAD Application Assist
        ↓
Patent Drawing Standards or Flowcharts / System Diagrams
        ↓
Figure Packet / Release Review
```

## Patent Wording Posture

The prompts help prepare drawing instructions and review-risk lists. They should not be treated as legal advice, legal compliance conclusions, patentability opinions, or a substitute for an attorney, patent agent, CAD drafter, or patent illustrator.

## Editable Prompt Files

All prompt bodies live under `prompts/`. The routing table is `prompts/index.ini`. Keep each `path=` value pointed at an existing Markdown file.
