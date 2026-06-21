# eMachination CAD Patent Prompt-Rig SRS v0.1

**Status:** Final draft for implementation planning  
**Target baseline code shape:** `emac-coding-prompt-rig_SMALL_NO_IMAGES_20260617_203259`  
**Target product family:** eMachination Prompt-Rig sibling product  
**Working product name:** eMachination CAD Patent Prompt-Rig  
**Primary implementation intent:** Keep the existing Prompt-Rig runtime/layout behavior, replace the prompt library with CAD / patent drawing prompts, and preserve placeholder image stubs so new artwork can be inserted later.

---

## 1. Purpose

The eMachination CAD Patent Prompt-Rig is a local-first prompt board for roughing in mechanical parts, cleaning up design concepts, creating CAD-ready instructions, preparing patent-style drawing prompts, generating cross-section / hatching guidance, creating flowchart and system-diagram prompts, and assembling drawing packets for invention documentation.

The product is not CAD software. It is not a patent attorney. It is the operator prompt layer between rough invention material and structured CAD / patent drawing work.

```text
rough-in idea / sketch / CAD screenshot / invention note
        ↓
prompt-board workflow
        ↓
cleaned mechanical concept / CAD instructions / patent drawing instructions
        ↓
Fusion / Inventor / SolidWorks / illustrator / patent packet
```

---

## 2. Baseline code posture

The implementation should be code-shaped like the uploaded small Prompt-Rig package:

```text
emac-coding-prompt-rig_SMALL_NO_IMAGES_20260617_203259
```

That means:

- preserve the existing Windows AutoHotkey v2 runtime model;
- preserve the existing launcher structure;
- preserve Prompt Forge / Prompt Coach behavior where it already exists;
- preserve editable Markdown prompt files;
- preserve `prompts/index.ini` as the prompt routing table;
- preserve the same primary / secondary / tertiary board model;
- preserve 8 button slots per board;
- preserve no-image packaging posture with `.txt` image stubs;
- preserve Linux source/runtime support, but do not make Linux perfection block the Windows prompt-board product.

The main work is content replacement and small product-identity configuration, not a rewrite.

---

## 3. Scope

### 3.1 In scope

- CAD / patent drawing prompt library.
- Rough-in part development prompts.
- Mechanical drawing cleanup prompts.
- CAD application prompts for Autodesk Fusion, Autodesk Inventor, and SolidWorks.
- Patent drawing prompts for utility patent figures, cross-sections, hatching, reference numerals, and drawing review.
- Patent-style flowchart, system diagram, and figure-to-spec mapping prompts.
- Final figure packet / release review prompts.
- Same board layout behavior as the existing Prompt-Rig runtime.
- README / START_HERE / prompt catalog documentation updates.
- Tests validating prompt index paths, prompt loading, profile/board layout, and expected prompt-file existence.

### 3.2 Out of scope

- Direct CAD API automation.
- Automatic generation of `.f3d`, `.ipt`, `.sldprt`, `.dwg`, `.dxf`, or `.step` files.
- Formal patent legal advice.
- Patentability opinions.
- Claim drafting as legal representation.
- Guaranteeing USPTO acceptance.
- Replacing a CAD drafter, patent illustrator, attorney, or agent.
- Universal Linux terminal-buffer capture.
- New branding image generation in this implementation slice.

---

## 4. Standards posture

The product may help the user prepare patent drawing instructions, but it must speak carefully:

- It may say “possible drawing issue,” “review risk,” “drawing-prep checklist item,” or “needs professional review.”
- It must not say “USPTO compliant” as a final legal conclusion.
- It should cite or refer to formal drawing rules where relevant.
- It should keep source facts separate from assumptions.

Baseline standards references to account for in prompts and documentation:

- 37 CFR § 1.84 is the core U.S. patent drawing standards rule.
- Drawing sheets and margins are a common formal-review issue.
- Hatching should use regularly spaced oblique parallel lines and should not interfere with reference characters or lead lines.
- Flow sheets and diagrams can be treated as drawings when they are part of the patent disclosure.
- Patent disclosure support matters; figures and written description should not drift apart.

Reference URLs:

- https://www.law.cornell.edu/cfr/text/37/1.84
- https://www.uspto.gov/web/offices/pac/mpep/s507.html
- https://www.uspto.gov/web/offices/pac/mpep/s1825.html
- https://www.uspto.gov/web/offices/pac/mpep/s608.html

---

## 5. Product identity

### 5.1 Recommended repository / folder names

Recommended sibling repo:

```text
emac-cad-patent-prompt-rig
```

Recommended installed folder:

```text
eMachinationCADPatentPromptRig
```

Recommended package name:

```text
emachination_cad_patent_prompt_rig_full_windows_linux_portable.zip
```

### 5.2 Runtime title

```text
eMachination CAD Patent
Prompt-Rig
```

### 5.3 Image assets

The first implementation may keep image stub files from the no-image package. New CAD / patent branding images can be inserted later.

Required behavior:

- Do not fail if image files are represented by `.txt` stubs.
- Do not delete the branding/image paths.
- Keep image path locations stable so real images can be dropped in later.

---

## 6. Users / actors

| Actor | Need |
|---|---|
| Inventor | Convert rough part ideas into structured drawing/CAD prompts. |
| CAD operator | Turn rough concepts into CAD modeling instructions. |
| Patent illustrator | Receive clean figure instructions, reference numerals, section views, and drawing packets. |
| Engineer / builder | Review manufacturability, dimensions, holes, slots, clearances, and feature layout. |
| Patent drafter / attorney reviewer | Review figure consistency, terminology, and written-description support. |
| AI-assisted operator | Use repeatable prompt slots instead of rebuilding long prompts manually. |

---

## 7. Core workflow

The board must support this flow:

```text
1. Rough-in concept
2. Improve part shape
3. Clean drawing image prompt
4. Normalize dimensions
5. Convert to CAD steps
6. Convert to patent figure plan
7. Check hatching / section / numerals
8. Assemble figure packet
```

The product should preserve design intent, not preserve ugly geometry. Rough, crooked, or ambiguous lines can be cleaned into horizontal/vertical/square mechanical geometry when the prompt explicitly asks for cleanup.

---

## 8. Runtime model

### 8.1 Profiles

The target prompt library uses six profiles:

```text
rough_in_part_development
mechanical_drawing_cleanup
cad_application_assist
patent_drawing_standards
patent_flowcharts_system_diagrams
figure_packet_release_review
```

User-facing profile names:

```text
Rough-In / Part Development
Mechanical Drawing Cleanup
CAD Application Assist
Patent Drawing Standards
Patent Flowcharts / System Diagrams
Figure Packet / Release Review
```

### 8.2 Boards

Keep the base runtime board IDs:

```text
primary
secondary
tertiary
```

The visible board label may remain `Primary`, `Secondary`, and `Tertiary` unless the runtime is later extended to support profile-specific board display names.

### 8.3 Slots

Each board has eight prompt slots.

Designed target shape:

```text
6 profiles × 3 boards × 8 slots
```

### 8.4 Hotkeys

Preserve the existing behavior from the base Prompt-Rig code:

| Control | Required action |
|---|---|
| ScrollLock | Open board |
| Shift + ScrollLock | Open tertiary board |
| Pause / Break | Cycle boards |
| Ctrl + Pause / Break | Cycle boards |
| NumLock | Cycle profiles |
| Ctrl + ScrollLock | Close board |
| Ctrl + Alt + ScrollLock | Exit runtime |
| Esc | Close board while focused |
| F5 | Reload prompt index/files while focused |

---

## 9. Prompt file scaffold

Each prompt Markdown file should keep the standard Prompt-Rig scaffold:

```markdown
# <Slot Title>

**Profile:** <Profile Display Name>  
**Board:** <Board Display Name>  
**Slot:** <Slot Number>  
**Runtime key:** `<profile_id>.<board_id>.<slot>`

## Prompt

You are helping with **<profile area>** work. Use this prompt slot for **<slot purpose>**.

### Goal

<One bounded goal.>

### Use when

<When the operator should use this prompt.>

### Source material

Use the current chat context and any material I paste after this prompt. If required context is missing, ask for the smallest missing piece rather than inventing details.

### Rules

- Stay focused on this slot's job.
- Separate observed facts from assumptions.
- Do not invent final dimensions unless they are clearly labeled assumptions.

### Output format

Return the result using these sections:

1. <Section>
2. <Section>
3. <Section>
4. <Section>

### Final instruction

Be practical, specific, and bounded. If a decision is not supported by the provided context, label it as an assumption instead of pretending it is known.
```

---

## 10. Profile and board catalog

## Profile 1 — Rough-In / Part Development

### Purpose

Help the user take an early mechanical idea and rough it into a more believable, buildable part.

This profile is not limited to hand drawings. It can work from rough sketches, CAD screenshots, invention notes, crude geometry, partial dimensions, or bad first-pass AI images.

### Board 1A — Primary: Rough-In Intake

| Slot | Label | Runtime key | Prompt file |
|---|---|---|---|
| 1 | Analyze Concept | `rough_in_part_development.primary.01` | `prompts/rough_in_part_development/primary/01_analyze_concept.md` |
| 2 | Extract Geometry | `rough_in_part_development.primary.02` | `prompts/rough_in_part_development/primary/02_extract_geometry.md` |
| 3 | Extract Dimensions | `rough_in_part_development.primary.03` | `prompts/rough_in_part_development/primary/03_extract_dimensions.md` |
| 4 | Missing Dimensions | `rough_in_part_development.primary.04` | `prompts/rough_in_part_development/primary/04_missing_dimensions.md` |
| 5 | Likely Function | `rough_in_part_development.primary.05` | `prompts/rough_in_part_development/primary/05_likely_function.md` |
| 6 | Manufacturability | `rough_in_part_development.primary.06` | `prompts/rough_in_part_development/primary/06_manufacturability.md` |
| 7 | Clarify Fast | `rough_in_part_development.primary.07` | `prompts/rough_in_part_development/primary/07_clarify_fast.md` |
| 8 | Rough-In Summary | `rough_in_part_development.primary.08` | `prompts/rough_in_part_development/primary/08_rough_in_summary.md` |

### Board 1B — Secondary: Part Improvement

| Slot | Label | Runtime key | Prompt file |
|---|---|---|---|
| 1 | Buildable Geometry | `rough_in_part_development.secondary.01` | `prompts/rough_in_part_development/secondary/01_buildable_geometry.md` |
| 2 | Square Layout | `rough_in_part_development.secondary.02` | `prompts/rough_in_part_development/secondary/02_square_layout.md` |
| 3 | Better Proportions | `rough_in_part_development.secondary.03` | `prompts/rough_in_part_development/secondary/03_better_proportions.md` |
| 4 | Hole Slot Placement | `rough_in_part_development.secondary.04` | `prompts/rough_in_part_development/secondary/04_hole_slot_placement.md` |
| 5 | Fillet Radius Plan | `rough_in_part_development.secondary.05` | `prompts/rough_in_part_development/secondary/05_fillet_radius_plan.md` |
| 6 | Thickness Material | `rough_in_part_development.secondary.06` | `prompts/rough_in_part_development/secondary/06_thickness_material.md` |
| 7 | Weak Feature Review | `rough_in_part_development.secondary.07` | `prompts/rough_in_part_development/secondary/07_weak_feature_review.md` |
| 8 | Improved Concept | `rough_in_part_development.secondary.08` | `prompts/rough_in_part_development/secondary/08_improved_concept.md` |

### Board 1C — Tertiary: Feature Breakdown

| Slot | Label | Runtime key | Prompt file |
|---|---|---|---|
| 1 | CAD Features | `rough_in_part_development.tertiary.01` | `prompts/rough_in_part_development/tertiary/01_cad_features.md` |
| 2 | Base Body | `rough_in_part_development.tertiary.02` | `prompts/rough_in_part_development/tertiary/02_base_body.md` |
| 3 | Cuts Slots Pockets | `rough_in_part_development.tertiary.03` | `prompts/rough_in_part_development/tertiary/03_cuts_slots_pockets.md` |
| 4 | Holes Countersinks | `rough_in_part_development.tertiary.04` | `prompts/rough_in_part_development/tertiary/04_holes_countersinks.md` |
| 5 | Ribs Tabs Brackets | `rough_in_part_development.tertiary.05` | `prompts/rough_in_part_development/tertiary/05_ribs_tabs_brackets.md` |
| 6 | Datum Strategy | `rough_in_part_development.tertiary.06` | `prompts/rough_in_part_development/tertiary/06_datum_strategy.md` |
| 7 | Feature Tree | `rough_in_part_development.tertiary.07` | `prompts/rough_in_part_development/tertiary/07_feature_tree.md` |
| 8 | Drafter Brief | `rough_in_part_development.tertiary.08` | `prompts/rough_in_part_development/tertiary/08_drafter_brief.md` |

---

## Profile 2 — Mechanical Drawing Cleanup

### Purpose

Turn ugly rough drawings, AI mechanical concepts, or loose design sketches into clean mechanical drawing prompts and image-generation prompts.

This is where the board asks for cleaner vertical and horizontal lines, orthographic layout, consistent line weight, dimension readability, and part geometry that looks like an actual object that could be made.

### Board 2A — Primary: Clean Mechanical Image Prompt

| Slot | Label | Runtime key | Prompt file |
|---|---|---|---|
| 1 | Clean Drawing | `mechanical_drawing_cleanup.primary.01` | `prompts/mechanical_drawing_cleanup/primary/01_clean_drawing.md` |
| 2 | Front View | `mechanical_drawing_cleanup.primary.02` | `prompts/mechanical_drawing_cleanup/primary/02_front_view.md` |
| 3 | Top Side Views | `mechanical_drawing_cleanup.primary.03` | `prompts/mechanical_drawing_cleanup/primary/03_top_side_views.md` |
| 4 | Detail View | `mechanical_drawing_cleanup.primary.04` | `prompts/mechanical_drawing_cleanup/primary/04_detail_view.md` |
| 5 | B/W Line Art | `mechanical_drawing_cleanup.primary.05` | `prompts/mechanical_drawing_cleanup/primary/05_bw_line_art.md` |
| 6 | Patent Line Art | `mechanical_drawing_cleanup.primary.06` | `prompts/mechanical_drawing_cleanup/primary/06_patent_line_art.md` |
| 7 | CAD Trace Ref | `mechanical_drawing_cleanup.primary.07` | `prompts/mechanical_drawing_cleanup/primary/07_cad_trace_ref.md` |
| 8 | Final Image Prompt | `mechanical_drawing_cleanup.primary.08` | `prompts/mechanical_drawing_cleanup/primary/08_final_image_prompt.md` |

### Board 2B — Secondary: Dimension Cleanup

| Slot | Label | Runtime key | Prompt file |
|---|---|---|---|
| 1 | Normalize Dims | `mechanical_drawing_cleanup.secondary.01` | `prompts/mechanical_drawing_cleanup/secondary/01_normalize_dims.md` |
| 2 | Dimension Table | `mechanical_drawing_cleanup.secondary.02` | `prompts/mechanical_drawing_cleanup/secondary/02_dimension_table.md` |
| 3 | Dim Conflicts | `mechanical_drawing_cleanup.secondary.03` | `prompts/mechanical_drawing_cleanup/secondary/03_dim_conflicts.md` |
| 4 | Missing Callouts | `mechanical_drawing_cleanup.secondary.04` | `prompts/mechanical_drawing_cleanup/secondary/04_missing_callouts.md` |
| 5 | Datum Edges | `mechanical_drawing_cleanup.secondary.05` | `prompts/mechanical_drawing_cleanup/secondary/05_datum_edges.md` |
| 6 | Hole Centers | `mechanical_drawing_cleanup.secondary.06` | `prompts/mechanical_drawing_cleanup/secondary/06_hole_centers.md` |
| 7 | Radii Fillets | `mechanical_drawing_cleanup.secondary.07` | `prompts/mechanical_drawing_cleanup/secondary/07_radii_fillets.md` |
| 8 | Corrected Dim Plan | `mechanical_drawing_cleanup.secondary.08` | `prompts/mechanical_drawing_cleanup/secondary/08_corrected_dim_plan.md` |

### Board 2C — Tertiary: Drawing Quality Review

| Slot | Label | Runtime key | Prompt file |
|---|---|---|---|
| 1 | Crooked Lines | `mechanical_drawing_cleanup.tertiary.01` | `prompts/mechanical_drawing_cleanup/tertiary/01_crooked_lines.md` |
| 2 | Holes Slots | `mechanical_drawing_cleanup.tertiary.02` | `prompts/mechanical_drawing_cleanup/tertiary/02_holes_slots.md` |
| 3 | Over Dimensioned | `mechanical_drawing_cleanup.tertiary.03` | `prompts/mechanical_drawing_cleanup/tertiary/03_over_dimensioned.md` |
| 4 | Under Dimensioned | `mechanical_drawing_cleanup.tertiary.04` | `prompts/mechanical_drawing_cleanup/tertiary/04_under_dimensioned.md` |
| 5 | Silhouette Clarity | `mechanical_drawing_cleanup.tertiary.05` | `prompts/mechanical_drawing_cleanup/tertiary/05_silhouette_clarity.md` |
| 6 | Line Labels | `mechanical_drawing_cleanup.tertiary.06` | `prompts/mechanical_drawing_cleanup/tertiary/06_line_labels.md` |
| 7 | CAD Feasibility | `mechanical_drawing_cleanup.tertiary.07` | `prompts/mechanical_drawing_cleanup/tertiary/07_cad_feasibility.md` |
| 8 | Cleanup Checklist | `mechanical_drawing_cleanup.tertiary.08` | `prompts/mechanical_drawing_cleanup/tertiary/08_cleanup_checklist.md` |

---

## Profile 3 — CAD Application Assist

### Purpose

Convert the cleaned part concept into application-specific CAD instructions.

### Board 3A — Primary: Autodesk Fusion

| Slot | Label | Runtime key | Prompt file |
|---|---|---|---|
| 1 | Fusion Model Steps | `cad_application_assist.primary.01` | `prompts/cad_application_assist/primary/01_fusion_model_steps.md` |
| 2 | Fusion Constraints | `cad_application_assist.primary.02` | `prompts/cad_application_assist/primary/02_fusion_constraints.md` |
| 3 | Fusion Extrude Cut | `cad_application_assist.primary.03` | `prompts/cad_application_assist/primary/03_fusion_extrude_cut.md` |
| 4 | Fusion Holes Fillets | `cad_application_assist.primary.04` | `prompts/cad_application_assist/primary/04_fusion_holes_fillets.md` |
| 5 | Fusion Drawings | `cad_application_assist.primary.05` | `prompts/cad_application_assist/primary/05_fusion_drawings.md` |
| 6 | Fusion Components | `cad_application_assist.primary.06` | `prompts/cad_application_assist/primary/06_fusion_components.md` |
| 7 | Fusion Troubleshoot | `cad_application_assist.primary.07` | `prompts/cad_application_assist/primary/07_fusion_troubleshoot.md` |
| 8 | Fusion Handoff | `cad_application_assist.primary.08` | `prompts/cad_application_assist/primary/08_fusion_handoff.md` |

### Board 3B — Secondary: Autodesk Inventor

| Slot | Label | Runtime key | Prompt file |
|---|---|---|---|
| 1 | Inventor Part Steps | `cad_application_assist.secondary.01` | `prompts/cad_application_assist/secondary/01_inventor_part_steps.md` |
| 2 | Inventor Constraints | `cad_application_assist.secondary.02` | `prompts/cad_application_assist/secondary/02_inventor_constraints.md` |
| 3 | Inventor Features | `cad_application_assist.secondary.03` | `prompts/cad_application_assist/secondary/03_inventor_features.md` |
| 4 | Inventor Holes Fillets | `cad_application_assist.secondary.04` | `prompts/cad_application_assist/secondary/04_inventor_holes_fillets.md` |
| 5 | Inventor Drawing Sheet | `cad_application_assist.secondary.05` | `prompts/cad_application_assist/secondary/05_inventor_drawing_sheet.md` |
| 6 | Inventor Assembly BOM | `cad_application_assist.secondary.06` | `prompts/cad_application_assist/secondary/06_inventor_assembly_bom.md` |
| 7 | Inventor Troubleshoot | `cad_application_assist.secondary.07` | `prompts/cad_application_assist/secondary/07_inventor_troubleshoot.md` |
| 8 | Inventor Handoff | `cad_application_assist.secondary.08` | `prompts/cad_application_assist/secondary/08_inventor_handoff.md` |

### Board 3C — Tertiary: SolidWorks

| Slot | Label | Runtime key | Prompt file |
|---|---|---|---|
| 1 | SolidWorks Model | `cad_application_assist.tertiary.01` | `prompts/cad_application_assist/tertiary/01_solidworks_model.md` |
| 2 | SolidWorks Relations | `cad_application_assist.tertiary.02` | `prompts/cad_application_assist/tertiary/02_solidworks_relations.md` |
| 3 | SolidWorks Feature Tree | `cad_application_assist.tertiary.03` | `prompts/cad_application_assist/tertiary/03_solidworks_feature_tree.md` |
| 4 | SolidWorks Holes Fillets | `cad_application_assist.tertiary.04` | `prompts/cad_application_assist/tertiary/04_solidworks_holes_fillets.md` |
| 5 | SolidWorks Drawings | `cad_application_assist.tertiary.05` | `prompts/cad_application_assist/tertiary/05_solidworks_drawings.md` |
| 6 | SolidWorks Assembly BOM | `cad_application_assist.tertiary.06` | `prompts/cad_application_assist/tertiary/06_solidworks_assembly_bom.md` |
| 7 | SolidWorks Troubleshoot | `cad_application_assist.tertiary.07` | `prompts/cad_application_assist/tertiary/07_solidworks_troubleshoot.md` |
| 8 | SolidWorks Handoff | `cad_application_assist.tertiary.08` | `prompts/cad_application_assist/tertiary/08_solidworks_handoff.md` |

---

## Profile 4 — Patent Drawing Standards

### Purpose

Turn cleaned mechanical concepts into patent-style drawing instructions.

### Board 4A — Primary: Utility Patent Figures

| Slot | Label | Runtime key | Prompt file |
|---|---|---|---|
| 1 | Figure List | `patent_drawing_standards.primary.01` | `prompts/patent_drawing_standards/primary/01_figure_list.md` |
| 2 | Mechanical To Patent | `patent_drawing_standards.primary.02` | `prompts/patent_drawing_standards/primary/02_mechanical_to_patent.md` |
| 3 | Reference Numerals | `patent_drawing_standards.primary.03` | `prompts/patent_drawing_standards/primary/03_reference_numerals.md` |
| 4 | View Plan | `patent_drawing_standards.primary.04` | `prompts/patent_drawing_standards/primary/04_view_plan.md` |
| 5 | Exploded View | `patent_drawing_standards.primary.05` | `prompts/patent_drawing_standards/primary/05_exploded_view.md` |
| 6 | Detail View | `patent_drawing_standards.primary.06` | `prompts/patent_drawing_standards/primary/06_detail_view.md` |
| 7 | Figure Descriptions | `patent_drawing_standards.primary.07` | `prompts/patent_drawing_standards/primary/07_figure_descriptions.md` |
| 8 | Illustrator Brief | `patent_drawing_standards.primary.08` | `prompts/patent_drawing_standards/primary/08_illustrator_brief.md` |

### Board 4B — Secondary: Cross-Sections / Hatching

| Slot | Label | Runtime key | Prompt file |
|---|---|---|---|
| 1 | Section Cut | `patent_drawing_standards.secondary.01` | `prompts/patent_drawing_standards/secondary/01_section_cut.md` |
| 2 | Section View | `patent_drawing_standards.secondary.02` | `prompts/patent_drawing_standards/secondary/02_section_view.md` |
| 3 | Hatching Plan | `patent_drawing_standards.secondary.03` | `prompts/patent_drawing_standards/secondary/03_hatching_plan.md` |
| 4 | Material Distinction | `patent_drawing_standards.secondary.04` | `prompts/patent_drawing_standards/secondary/04_material_distinction.md` |
| 5 | Avoid Label Interference | `patent_drawing_standards.secondary.05` | `prompts/patent_drawing_standards/secondary/05_avoid_label_interference.md` |
| 6 | Section Numerals | `patent_drawing_standards.secondary.06` | `prompts/patent_drawing_standards/secondary/06_section_numerals.md` |
| 7 | Section Clarity | `patent_drawing_standards.secondary.07` | `prompts/patent_drawing_standards/secondary/07_section_clarity.md` |
| 8 | Final Section Prompt | `patent_drawing_standards.secondary.08` | `prompts/patent_drawing_standards/secondary/08_final_section_prompt.md` |

### Board 4C — Tertiary: Patent Drawing Review

| Slot | Label | Runtime key | Prompt file |
|---|---|---|---|
| 1 | Line Clarity | `patent_drawing_standards.tertiary.01` | `prompts/patent_drawing_standards/tertiary/01_line_clarity.md` |
| 2 | Numeral Check | `patent_drawing_standards.tertiary.02` | `prompts/patent_drawing_standards/tertiary/02_numeral_check.md` |
| 3 | Figure Labels | `patent_drawing_standards.tertiary.03` | `prompts/patent_drawing_standards/tertiary/03_figure_labels.md` |
| 4 | Missing Views | `patent_drawing_standards.tertiary.04` | `prompts/patent_drawing_standards/tertiary/04_missing_views.md` |
| 5 | Sheet Margin Risk | `patent_drawing_standards.tertiary.05` | `prompts/patent_drawing_standards/tertiary/05_sheet_margin_risk.md` |
| 6 | Figure Spec Flow | `patent_drawing_standards.tertiary.06` | `prompts/patent_drawing_standards/tertiary/06_figure_spec_flow.md` |
| 7 | Crowding Review | `patent_drawing_standards.tertiary.07` | `prompts/patent_drawing_standards/tertiary/07_crowding_review.md` |
| 8 | Objection Risk List | `patent_drawing_standards.tertiary.08` | `prompts/patent_drawing_standards/tertiary/08_objection_risk_list.md` |

---

## Profile 5 — Patent Flowcharts / System Diagrams

### Purpose

Create patent-style process diagrams, system diagrams, architecture diagrams, and method flowcharts.

### Board 5A — Primary: Flowcharts

| Slot | Label | Runtime key | Prompt file |
|---|---|---|---|
| 1 | Method Flowchart | `patent_flowcharts_system_diagrams.primary.01` | `prompts/patent_flowcharts_system_diagrams/primary/01_method_flowchart.md` |
| 2 | Numbered Steps | `patent_flowcharts_system_diagrams.primary.02` | `prompts/patent_flowcharts_system_diagrams/primary/02_numbered_steps.md` |
| 3 | Decision Blocks | `patent_flowcharts_system_diagrams.primary.03` | `prompts/patent_flowcharts_system_diagrams/primary/03_decision_blocks.md` |
| 4 | Alternate Paths | `patent_flowcharts_system_diagrams.primary.04` | `prompts/patent_flowcharts_system_diagrams/primary/04_alternate_paths.md` |
| 5 | Simplify Flowchart | `patent_flowcharts_system_diagrams.primary.05` | `prompts/patent_flowcharts_system_diagrams/primary/05_simplify_flowchart.md` |
| 6 | Flow Numerals | `patent_flowcharts_system_diagrams.primary.06` | `prompts/patent_flowcharts_system_diagrams/primary/06_flow_numerals.md` |
| 7 | Figure Caption | `patent_flowcharts_system_diagrams.primary.07` | `prompts/patent_flowcharts_system_diagrams/primary/07_figure_caption.md` |
| 8 | Final Flow Prompt | `patent_flowcharts_system_diagrams.primary.08` | `prompts/patent_flowcharts_system_diagrams/primary/08_final_flow_prompt.md` |

### Board 5B — Secondary: System Diagrams

| Slot | Label | Runtime key | Prompt file |
|---|---|---|---|
| 1 | Block Diagram | `patent_flowcharts_system_diagrams.secondary.01` | `prompts/patent_flowcharts_system_diagrams/secondary/01_block_diagram.md` |
| 2 | Module Diagram | `patent_flowcharts_system_diagrams.secondary.02` | `prompts/patent_flowcharts_system_diagrams/secondary/02_module_diagram.md` |
| 3 | Data Flow | `patent_flowcharts_system_diagrams.secondary.03` | `prompts/patent_flowcharts_system_diagrams/secondary/03_data_flow.md` |
| 4 | HW SW Boundary | `patent_flowcharts_system_diagrams.secondary.04` | `prompts/patent_flowcharts_system_diagrams/secondary/04_hw_sw_boundary.md` |
| 5 | Signal Control Path | `patent_flowcharts_system_diagrams.secondary.05` | `prompts/patent_flowcharts_system_diagrams/secondary/05_signal_control_path.md` |
| 6 | System Numerals | `patent_flowcharts_system_diagrams.secondary.06` | `prompts/patent_flowcharts_system_diagrams/secondary/06_system_numerals.md` |
| 7 | Architecture Caption | `patent_flowcharts_system_diagrams.secondary.07` | `prompts/patent_flowcharts_system_diagrams/secondary/07_architecture_caption.md` |
| 8 | Final System Prompt | `patent_flowcharts_system_diagrams.secondary.08` | `prompts/patent_flowcharts_system_diagrams/secondary/08_final_system_prompt.md` |

### Board 5C — Tertiary: Figure-to-Spec Mapping

| Slot | Label | Runtime key | Prompt file |
|---|---|---|---|
| 1 | Figure To Spec | `patent_flowcharts_system_diagrams.tertiary.01` | `prompts/patent_flowcharts_system_diagrams/tertiary/01_figure_to_spec.md` |
| 2 | Numeral Map | `patent_flowcharts_system_diagrams.tertiary.02` | `prompts/patent_flowcharts_system_diagrams/tertiary/02_numeral_map.md` |
| 3 | Flow To Method Text | `patent_flowcharts_system_diagrams.tertiary.03` | `prompts/patent_flowcharts_system_diagrams/tertiary/03_flow_to_method_text.md` |
| 4 | Missing Spec Support | `patent_flowcharts_system_diagrams.tertiary.04` | `prompts/patent_flowcharts_system_diagrams/tertiary/04_missing_spec_support.md` |
| 5 | Unsupported Figure Elements | `patent_flowcharts_system_diagrams.tertiary.05` | `prompts/patent_flowcharts_system_diagrams/tertiary/05_unsupported_figure_elements.md` |
| 6 | Figure Paragraph | `patent_flowcharts_system_diagrams.tertiary.06` | `prompts/patent_flowcharts_system_diagrams/tertiary/06_figure_paragraph.md` |
| 7 | Consistency Table | `patent_flowcharts_system_diagrams.tertiary.07` | `prompts/patent_flowcharts_system_diagrams/tertiary/07_consistency_table.md` |
| 8 | Spec Mapping Packet | `patent_flowcharts_system_diagrams.tertiary.08` | `prompts/patent_flowcharts_system_diagrams/tertiary/08_spec_mapping_packet.md` |

---

## Profile 6 — Figure Packet / Release Review

### Purpose

Assemble cleaned mechanical drawings, CAD instructions, patent figures, flowcharts, and review notes into a complete drawing packet.

### Board 6A — Primary: Figure Packet Builder

| Slot | Label | Runtime key | Prompt file |
|---|---|---|---|
| 1 | Figure Inventory | `figure_packet_release_review.primary.01` | `prompts/figure_packet_release_review/primary/01_figure_inventory.md` |
| 2 | Figure Order | `figure_packet_release_review.primary.02` | `prompts/figure_packet_release_review/primary/02_figure_order.md` |
| 3 | Mechanical Group | `figure_packet_release_review.primary.03` | `prompts/figure_packet_release_review/primary/03_mechanical_group.md` |
| 4 | Section Detail Group | `figure_packet_release_review.primary.04` | `prompts/figure_packet_release_review/primary/04_section_detail_group.md` |
| 5 | Flow System Group | `figure_packet_release_review.primary.05` | `prompts/figure_packet_release_review/primary/05_flow_system_group.md` |
| 6 | Drawing Task List | `figure_packet_release_review.primary.06` | `prompts/figure_packet_release_review/primary/06_drawing_task_list.md` |
| 7 | Illustrator Handoff | `figure_packet_release_review.primary.07` | `prompts/figure_packet_release_review/primary/07_illustrator_handoff.md` |
| 8 | Packet Summary | `figure_packet_release_review.primary.08` | `prompts/figure_packet_release_review/primary/08_packet_summary.md` |

### Board 6B — Secondary: Consistency QA

| Slot | Label | Runtime key | Prompt file |
|---|---|---|---|
| 1 | Numeral Consistency | `figure_packet_release_review.secondary.01` | `prompts/figure_packet_release_review/secondary/01_numeral_consistency.md` |
| 2 | Terminology Consistency | `figure_packet_release_review.secondary.02` | `prompts/figure_packet_release_review/secondary/02_terminology_consistency.md` |
| 3 | Missing Views | `figure_packet_release_review.secondary.03` | `prompts/figure_packet_release_review/secondary/03_missing_views.md` |
| 4 | Duplicate Figures | `figure_packet_release_review.secondary.04` | `prompts/figure_packet_release_review/secondary/04_duplicate_figures.md` |
| 5 | Unresolved Dimensions | `figure_packet_release_review.secondary.05` | `prompts/figure_packet_release_review/secondary/05_unresolved_dimensions.md` |
| 6 | Open Questions | `figure_packet_release_review.secondary.06` | `prompts/figure_packet_release_review/secondary/06_open_questions.md` |
| 7 | Drawing Risks | `figure_packet_release_review.secondary.07` | `prompts/figure_packet_release_review/secondary/07_drawing_risks.md` |
| 8 | QA Report | `figure_packet_release_review.secondary.08` | `prompts/figure_packet_release_review/secondary/08_qa_report.md` |

### Board 6C — Tertiary: Final Handoff

| Slot | Label | Runtime key | Prompt file |
|---|---|---|---|
| 1 | CAD Handoff | `figure_packet_release_review.tertiary.01` | `prompts/figure_packet_release_review/tertiary/01_cad_handoff.md` |
| 2 | Patent Illustrator Handoff | `figure_packet_release_review.tertiary.02` | `prompts/figure_packet_release_review/tertiary/02_patent_illustrator_handoff.md` |
| 3 | Attorney Review Handoff | `figure_packet_release_review.tertiary.03` | `prompts/figure_packet_release_review/tertiary/03_attorney_review_handoff.md` |
| 4 | Invention Notebook Summary | `figure_packet_release_review.tertiary.04` | `prompts/figure_packet_release_review/tertiary/04_invention_notebook_summary.md` |
| 5 | Filing Support Notes | `figure_packet_release_review.tertiary.05` | `prompts/figure_packet_release_review/tertiary/05_filing_support_notes.md` |
| 6 | Final Open Questions | `figure_packet_release_review.tertiary.06` | `prompts/figure_packet_release_review/tertiary/06_final_open_questions.md` |
| 7 | Next Action Checklist | `figure_packet_release_review.tertiary.07` | `prompts/figure_packet_release_review/tertiary/07_next_action_checklist.md` |
| 8 | Final Release Packet | `figure_packet_release_review.tertiary.08` | `prompts/figure_packet_release_review/tertiary/08_final_release_packet.md` |

---

## 11. Critical example prompt: Clean Drawing

This prompt must exist at:

```text
prompts/mechanical_drawing_cleanup/primary/01_clean_drawing.md
```

Required prompt body:

```markdown
# Clean Drawing

**Profile:** Mechanical Drawing Cleanup  
**Board:** Primary — clean mechanical image prompt  
**Slot:** 1  
**Runtime key:** `mechanical_drawing_cleanup.primary.01`

## Prompt

You are helping convert a rough mechanical part concept into a cleaner mechanical drawing reference.

Use the attached rough drawing, CAD screenshot, AI-generated concept image, or partial mechanical draft as source material.

### Goal

Create a cleaner mechanical drawing image prompt that preserves the design intent but improves the geometry so it looks like a buildable part.

### Use when

Use this when a part concept is visually messy, crooked, hand-drawn, incomplete, or not yet suitable for CAD tracing or patent-style drawing work.

### Source material

Use the current chat context and any image, drawing, CAD screenshot, or notes I provide after this prompt. If required context is missing, ask for the smallest missing piece rather than inventing details.

### Rules

- Identify the visible part outline, cutouts, holes, slots, radii, and dimension notes.
- Preserve intended dimensions where visible.
- Do not invent final manufacturing dimensions unless clearly labeled as assumptions.
- Straighten lines that should be horizontal or vertical.
- Make corners square unless the source clearly shows a radius or fillet.
- Make circular holes clean and centered only when the source supports that placement.
- Convert rough or uneven lines into clean black-and-white mechanical linework.
- Remove sketch noise, shadows, smudges, and background clutter.
- Add only minimal dimension callouts from the source.
- Flag missing dimensions instead of hiding them.
- Preserve design intent, not ugly geometry.

### Output format

Return the result using these sections:

1. Observed geometry
2. Preserved dimensions
3. Assumptions
4. Missing dimensions
5. Clean mechanical drawing image prompt
6. CAD drafter notes

### Final image prompt requirements

The final image prompt must request:

- black-and-white mechanical drawing
- orthographic front view unless another view is requested
- clean vertical and horizontal edges
- consistent line weight
- white background
- readable dimensions
- no decorative styling
- no photorealistic rendering
- no perspective view unless requested
- no shading except optional light section hatching when requested
```

---

## 12. Implementation file targets

### 12.1 Preserve from baseline

Preserve these directories and behaviors from the baseline package:

```text
launchers/
setup/
src/
tools/
tests/
docs/assets/brand/*.txt
prompts/index.ini structure
Prompt Forge / Prompt Coach behavior
```

### 12.2 Replace / generate

Replace the coding prompt library with the CAD / patent prompt library:

```text
prompts/rough_in_part_development/
prompts/mechanical_drawing_cleanup/
prompts/cad_application_assist/
prompts/patent_drawing_standards/
prompts/patent_flowcharts_system_diagrams/
prompts/figure_packet_release_review/
prompts/index.ini
prompt_library_manifest.json
```

### 12.3 Update product metadata

Update these files as needed:

```text
README.md
START_HERE.md
docs/PROMPT_CATALOG.md
docs/USER_GUIDE.md
docs/ROADMAP.md
docs/visual-guide.md
package/board_package.ini
src/eMachination_Coding_Prompt_Rig.ahk
src/linux/hotkey_board_runtime.py if product metadata is duplicated there
tests/test_prompt_rig_windows_package.py
tests/test_linux_hotkey_board.py
```

Minimum AutoHotkey changes:

```ahk
APP_NAME := "eMachination CAD Patent Prompt-Rig"
APP_TITLE_LINE_1 := "eMachination CAD Patent"
APP_TITLE_LINE_2 := "Prompt-Rig"

profiles := [
    Map("id", "rough_in_part_development", "name", "Rough-In / Part Development"),
    Map("id", "mechanical_drawing_cleanup", "name", "Mechanical Drawing Cleanup"),
    Map("id", "cad_application_assist", "name", "CAD Application Assist"),
    Map("id", "patent_drawing_standards", "name", "Patent Drawing Standards"),
    Map("id", "patent_flowcharts_system_diagrams", "name", "Patent Flowcharts / System Diagrams"),
    Map("id", "figure_packet_release_review", "name", "Figure Packet / Release Review")
]
```

If a low-risk first pass is preferred, keep the AHK file name unchanged and only change internal product strings. A later rename pass can rename the file.

---

## 13. Functional requirements

| ID | Requirement |
|---|---|
| FR-001 | The app shall start from the existing Windows launcher structure. |
| FR-002 | The app shall load prompt labels and file paths from `prompts/index.ini`. |
| FR-003 | The app shall support the six CAD / patent profiles listed in this SRS. |
| FR-004 | Each profile shall expose primary, secondary, and tertiary boards. |
| FR-005 | Each board shall expose eight prompt buttons. |
| FR-006 | Prompt buttons shall copy/paste/send the correct Markdown prompt body for the active profile, board, and slot. |
| FR-007 | Pause / Break shall cycle boards. |
| FR-008 | Ctrl + Pause / Break shall cycle boards. |
| FR-009 | NumLock shall cycle profiles. |
| FR-010 | F5 shall reload changed prompt files while the board is focused. |
| FR-011 | Prompt Forge shall remain available if present in the baseline runtime. |
| FR-012 | Prompt Coach shall remain available if present in the baseline runtime. |
| FR-013 | Image files may remain as `.txt` stubs until the user inserts final images. |
| FR-014 | The prompt catalog shall document the CAD / patent profiles, boards, and slots. |
| FR-015 | The Linux compiler/runtime path shall not be deleted, but Linux limitations may remain documented. |
| FR-016 | The app shall not claim to satisfy legal or patent-office requirements or provide legal advice. |

---

## 14. Non-functional requirements

| ID | Requirement |
|---|---|
| NFR-001 | The runtime should remain local-first. |
| NFR-002 | Prompt files should remain plain Markdown. |
| NFR-003 | Prompt index format should stay simple and hand-editable. |
| NFR-004 | The product should tolerate missing real images when `.txt` stubs are present. |
| NFR-005 | The Windows runtime should remain the primary release target. |
| NFR-006 | Linux support should be pragmatic and documented, not overpromised. |
| NFR-007 | Prompts should separate observations, assumptions, missing data, and final instructions. |
| NFR-008 | The product should avoid legal certainty language. |
| NFR-009 | The prompt library should be understandable without reading source code. |
| NFR-010 | The product should be packageable with the same small/no-image posture as the baseline zip. |

---

## 15. Acceptance criteria

### 15.1 Prompt library acceptance

- `prompts/index.ini` contains all target runtime keys from the profile catalog.
- Every `path=` entry in `prompts/index.ini` points to an existing `.md` file.
- Every prompt file uses the standard Prompt-Rig scaffold.
- The clean drawing prompt exists and includes the preserve-intent-not-ugly-geometry rule.
- No coding implementation prompts remain as active board prompts unless intentionally archived outside the active index.

### 15.2 Windows runtime acceptance

- Start launcher opens the CAD Patent Prompt-Rig.
- ScrollLock opens the board.
- Pause / Break cycles boards.
- Ctrl + Pause / Break cycles boards.
- NumLock cycles through the six profiles.
- Prompt buttons copy the active prompt after profile and board switching.
- F5 reloads edited prompt files.
- Prompt Forge opens and can operate against the new prompt library if the baseline supports it.

### 15.3 Package acceptance

- Package can be built with no real images inserted.
- Image stubs are preserved.
- README and START_HERE describe the CAD / patent purpose.
- Prompt catalog documents all active profiles/boards/slots.
- Tests validate index integrity and active prompt paths.

### 15.4 Linux acceptance

- Linux source/runtime files remain included.
- Linux board spec compiler can compile the new prompt index.
- Linux docs state limitations plainly.
- Linux terminal-buffer perfection is not required for this product slice.

---

## 16. Recommended targeted tests

### 16.1 Prompt index/path test

Validate:

- every INI section has `label` and `path`;
- every path exists;
- every path ends in `.md`;
- active profiles match the six target profiles;
- active boards match `primary`, `secondary`, `tertiary`;
- slots are numbered `01` through `08` per profile/board.

### 16.2 Windows package test

Validate:

- launcher files exist;
- AHK runtime file exists;
- prompt index exists;
- Prompt Forge asset paths tolerate `.txt` stubs;
- required package files exist.

### 16.3 Runtime smoke test

Manual Windows smoke:

1. Start app.
2. Open board.
3. Cycle profiles with NumLock.
4. Cycle boards with Pause / Break.
5. Press at least one prompt slot after switching.
6. Confirm copied prompt text matches active profile/board/slot.
7. Open Prompt Forge.
8. Press F5 after editing one prompt.
9. Confirm changed prompt reloads.

---

## 17. Open questions

1. Should the repo be renamed to `emac-cad-patent-prompt-rig`, or should the first implementation stay inside the existing coding Prompt-Rig codebase as a branch/variant?
2. Should the AHK runtime file be renamed now, or should only product strings and prompt content change in the first slice?
3. Should board labels remain Primary / Secondary / Tertiary, or should the runtime support per-profile board display names?
4. Should the final product include both CAD/patent prompts and the old coding prompts, or should this be a pure CAD/patent prompt board?
5. Should Autodesk Fusion, Inventor, and SolidWorks each remain one board, or should they eventually become separate profiles?
6. Should design patent drawing prompts be added in v0.2, separate from utility patent drawings?
7. Should the product include separate prompts for AI image generation tools versus CAD drafter handoffs?
8. Should a future slice generate example cleaned mechanical drawing images from rough-in inputs?

---

## 18. Design lock

The design lock for v0.1 is:

```text
Same Prompt-Rig runtime shape.
New CAD / patent prompt library.
No real image assets required yet.
Six profiles.
Three boards per profile.
Eight slots per board.
Windows release remains primary.
Linux source remains included but pragmatic.
Prompt Forge stays if it already exists.
The board preserves design intent, not ugly geometry.
```

