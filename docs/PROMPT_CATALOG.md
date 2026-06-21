# Prompt Catalog — eMachination CAD Patent Prompt-Rig

The active prompt index contains the CAD / mechanical / patent drawing prompt library. Each prompt file is editable Markdown and is routed by `prompts/index.ini`.

## Rough-In Parts

Help take an early mechanical idea and rough it into a more believable, buildable part.

### Rough-In Intake (`primary`)

| Slot | Label | Runtime key | Path |
| --- | --- | --- | --- |
| 01 | Analyze Concept | `rough_in_part_development.primary.01` | `prompts/rough_in_part_development/primary/01_analyze_concept.md` |
| 02 | Extract Geometry | `rough_in_part_development.primary.02` | `prompts/rough_in_part_development/primary/02_extract_geometry.md` |
| 03 | Extract Dimensions | `rough_in_part_development.primary.03` | `prompts/rough_in_part_development/primary/03_extract_dimensions.md` |
| 04 | Missing Dimensions | `rough_in_part_development.primary.04` | `prompts/rough_in_part_development/primary/04_missing_dimensions.md` |
| 05 | Likely Function | `rough_in_part_development.primary.05` | `prompts/rough_in_part_development/primary/05_likely_function.md` |
| 06 | Manufacturability | `rough_in_part_development.primary.06` | `prompts/rough_in_part_development/primary/06_manufacturability.md` |
| 07 | Clarify Fast | `rough_in_part_development.primary.07` | `prompts/rough_in_part_development/primary/07_clarify_fast.md` |
| 08 | Rough-In Summary | `rough_in_part_development.primary.08` | `prompts/rough_in_part_development/primary/08_rough_in_summary.md` |

### Part Improvement (`secondary`)

| Slot | Label | Runtime key | Path |
| --- | --- | --- | --- |
| 01 | Buildable Geometry | `rough_in_part_development.secondary.01` | `prompts/rough_in_part_development/secondary/01_buildable_geometry.md` |
| 02 | Square Layout | `rough_in_part_development.secondary.02` | `prompts/rough_in_part_development/secondary/02_square_layout.md` |
| 03 | Better Proportions | `rough_in_part_development.secondary.03` | `prompts/rough_in_part_development/secondary/03_better_proportions.md` |
| 04 | Hole Slot Placement | `rough_in_part_development.secondary.04` | `prompts/rough_in_part_development/secondary/04_hole_slot_placement.md` |
| 05 | Fillet Radius Plan | `rough_in_part_development.secondary.05` | `prompts/rough_in_part_development/secondary/05_fillet_radius_plan.md` |
| 06 | Thickness Material | `rough_in_part_development.secondary.06` | `prompts/rough_in_part_development/secondary/06_thickness_material.md` |
| 07 | Weak Feature Review | `rough_in_part_development.secondary.07` | `prompts/rough_in_part_development/secondary/07_weak_feature_review.md` |
| 08 | Improved Concept | `rough_in_part_development.secondary.08` | `prompts/rough_in_part_development/secondary/08_improved_concept.md` |

### Feature Breakdown (`tertiary`)

| Slot | Label | Runtime key | Path |
| --- | --- | --- | --- |
| 01 | CAD Features | `rough_in_part_development.tertiary.01` | `prompts/rough_in_part_development/tertiary/01_cad_features.md` |
| 02 | Base Body | `rough_in_part_development.tertiary.02` | `prompts/rough_in_part_development/tertiary/02_base_body.md` |
| 03 | Cuts Slots Pockets | `rough_in_part_development.tertiary.03` | `prompts/rough_in_part_development/tertiary/03_cuts_slots_pockets.md` |
| 04 | Holes Countersinks | `rough_in_part_development.tertiary.04` | `prompts/rough_in_part_development/tertiary/04_holes_countersinks.md` |
| 05 | Ribs Tabs Brackets | `rough_in_part_development.tertiary.05` | `prompts/rough_in_part_development/tertiary/05_ribs_tabs_brackets.md` |
| 06 | Datum Strategy | `rough_in_part_development.tertiary.06` | `prompts/rough_in_part_development/tertiary/06_datum_strategy.md` |
| 07 | Feature Tree | `rough_in_part_development.tertiary.07` | `prompts/rough_in_part_development/tertiary/07_feature_tree.md` |
| 08 | Drafter Brief | `rough_in_part_development.tertiary.08` | `prompts/rough_in_part_development/tertiary/08_drafter_brief.md` |

## Mechanical Drawing Cleanup

Turn rough drawings, AI mechanical concepts, or loose design sketches into clean mechanical drawing prompts and image-generation prompts.

### Clean Mechanical Image Prompt (`primary`)

| Slot | Label | Runtime key | Path |
| --- | --- | --- | --- |
| 01 | Clean Drawing | `mechanical_drawing_cleanup.primary.01` | `prompts/mechanical_drawing_cleanup/primary/01_clean_drawing.md` |
| 02 | Front View | `mechanical_drawing_cleanup.primary.02` | `prompts/mechanical_drawing_cleanup/primary/02_front_view.md` |
| 03 | Top Side Views | `mechanical_drawing_cleanup.primary.03` | `prompts/mechanical_drawing_cleanup/primary/03_top_side_views.md` |
| 04 | Detail View | `mechanical_drawing_cleanup.primary.04` | `prompts/mechanical_drawing_cleanup/primary/04_detail_view.md` |
| 05 | B/W Line Art | `mechanical_drawing_cleanup.primary.05` | `prompts/mechanical_drawing_cleanup/primary/05_bw_line_art.md` |
| 06 | Patent Line Art | `mechanical_drawing_cleanup.primary.06` | `prompts/mechanical_drawing_cleanup/primary/06_patent_line_art.md` |
| 07 | CAD Trace Ref | `mechanical_drawing_cleanup.primary.07` | `prompts/mechanical_drawing_cleanup/primary/07_cad_trace_ref.md` |
| 08 | Final Image Prompt | `mechanical_drawing_cleanup.primary.08` | `prompts/mechanical_drawing_cleanup/primary/08_final_image_prompt.md` |

### Dimension Cleanup (`secondary`)

| Slot | Label | Runtime key | Path |
| --- | --- | --- | --- |
| 01 | Normalize Dims | `mechanical_drawing_cleanup.secondary.01` | `prompts/mechanical_drawing_cleanup/secondary/01_normalize_dims.md` |
| 02 | Dimension Table | `mechanical_drawing_cleanup.secondary.02` | `prompts/mechanical_drawing_cleanup/secondary/02_dimension_table.md` |
| 03 | Dim Conflicts | `mechanical_drawing_cleanup.secondary.03` | `prompts/mechanical_drawing_cleanup/secondary/03_dim_conflicts.md` |
| 04 | Missing Callouts | `mechanical_drawing_cleanup.secondary.04` | `prompts/mechanical_drawing_cleanup/secondary/04_missing_callouts.md` |
| 05 | Datum Edges | `mechanical_drawing_cleanup.secondary.05` | `prompts/mechanical_drawing_cleanup/secondary/05_datum_edges.md` |
| 06 | Hole Centers | `mechanical_drawing_cleanup.secondary.06` | `prompts/mechanical_drawing_cleanup/secondary/06_hole_centers.md` |
| 07 | Radii Fillets | `mechanical_drawing_cleanup.secondary.07` | `prompts/mechanical_drawing_cleanup/secondary/07_radii_fillets.md` |
| 08 | Corrected Dim Plan | `mechanical_drawing_cleanup.secondary.08` | `prompts/mechanical_drawing_cleanup/secondary/08_corrected_dim_plan.md` |

### Drawing Quality Review (`tertiary`)

| Slot | Label | Runtime key | Path |
| --- | --- | --- | --- |
| 01 | Crooked Lines | `mechanical_drawing_cleanup.tertiary.01` | `prompts/mechanical_drawing_cleanup/tertiary/01_crooked_lines.md` |
| 02 | Holes Slots | `mechanical_drawing_cleanup.tertiary.02` | `prompts/mechanical_drawing_cleanup/tertiary/02_holes_slots.md` |
| 03 | Over Dimensioned | `mechanical_drawing_cleanup.tertiary.03` | `prompts/mechanical_drawing_cleanup/tertiary/03_over_dimensioned.md` |
| 04 | Under Dimensioned | `mechanical_drawing_cleanup.tertiary.04` | `prompts/mechanical_drawing_cleanup/tertiary/04_under_dimensioned.md` |
| 05 | Silhouette Clarity | `mechanical_drawing_cleanup.tertiary.05` | `prompts/mechanical_drawing_cleanup/tertiary/05_silhouette_clarity.md` |
| 06 | Line Labels | `mechanical_drawing_cleanup.tertiary.06` | `prompts/mechanical_drawing_cleanup/tertiary/06_line_labels.md` |
| 07 | CAD Feasibility | `mechanical_drawing_cleanup.tertiary.07` | `prompts/mechanical_drawing_cleanup/tertiary/07_cad_feasibility.md` |
| 08 | Cleanup Checklist | `mechanical_drawing_cleanup.tertiary.08` | `prompts/mechanical_drawing_cleanup/tertiary/08_cleanup_checklist.md` |

## CAD Application Assist

Convert a cleaned part concept into application-specific CAD instructions.

### Autodesk Fusion (`primary`)

| Slot | Label | Runtime key | Path |
| --- | --- | --- | --- |
| 01 | Fusion Model Steps | `cad_application_assist.primary.01` | `prompts/cad_application_assist/primary/01_fusion_model_steps.md` |
| 02 | Fusion Constraints | `cad_application_assist.primary.02` | `prompts/cad_application_assist/primary/02_fusion_constraints.md` |
| 03 | Fusion Extrude Cut | `cad_application_assist.primary.03` | `prompts/cad_application_assist/primary/03_fusion_extrude_cut.md` |
| 04 | Fusion Holes Fillets | `cad_application_assist.primary.04` | `prompts/cad_application_assist/primary/04_fusion_holes_fillets.md` |
| 05 | Fusion Drawings | `cad_application_assist.primary.05` | `prompts/cad_application_assist/primary/05_fusion_drawings.md` |
| 06 | Fusion Components | `cad_application_assist.primary.06` | `prompts/cad_application_assist/primary/06_fusion_components.md` |
| 07 | Fusion Troubleshoot | `cad_application_assist.primary.07` | `prompts/cad_application_assist/primary/07_fusion_troubleshoot.md` |
| 08 | Fusion Handoff | `cad_application_assist.primary.08` | `prompts/cad_application_assist/primary/08_fusion_handoff.md` |

### Autodesk Inventor (`secondary`)

| Slot | Label | Runtime key | Path |
| --- | --- | --- | --- |
| 01 | Inventor Part Steps | `cad_application_assist.secondary.01` | `prompts/cad_application_assist/secondary/01_inventor_part_steps.md` |
| 02 | Inventor Constraints | `cad_application_assist.secondary.02` | `prompts/cad_application_assist/secondary/02_inventor_constraints.md` |
| 03 | Inventor Features | `cad_application_assist.secondary.03` | `prompts/cad_application_assist/secondary/03_inventor_features.md` |
| 04 | Inventor Holes Fillets | `cad_application_assist.secondary.04` | `prompts/cad_application_assist/secondary/04_inventor_holes_fillets.md` |
| 05 | Inventor Drawing Sheet | `cad_application_assist.secondary.05` | `prompts/cad_application_assist/secondary/05_inventor_drawing_sheet.md` |
| 06 | Inventor Assembly BOM | `cad_application_assist.secondary.06` | `prompts/cad_application_assist/secondary/06_inventor_assembly_bom.md` |
| 07 | Inventor Troubleshoot | `cad_application_assist.secondary.07` | `prompts/cad_application_assist/secondary/07_inventor_troubleshoot.md` |
| 08 | Inventor Handoff | `cad_application_assist.secondary.08` | `prompts/cad_application_assist/secondary/08_inventor_handoff.md` |

### SolidWorks (`tertiary`)

| Slot | Label | Runtime key | Path |
| --- | --- | --- | --- |
| 01 | SolidWorks Model | `cad_application_assist.tertiary.01` | `prompts/cad_application_assist/tertiary/01_solidworks_model.md` |
| 02 | SolidWorks Relations | `cad_application_assist.tertiary.02` | `prompts/cad_application_assist/tertiary/02_solidworks_relations.md` |
| 03 | SolidWorks Feature Tree | `cad_application_assist.tertiary.03` | `prompts/cad_application_assist/tertiary/03_solidworks_feature_tree.md` |
| 04 | SolidWorks Holes Fillets | `cad_application_assist.tertiary.04` | `prompts/cad_application_assist/tertiary/04_solidworks_holes_fillets.md` |
| 05 | SolidWorks Drawings | `cad_application_assist.tertiary.05` | `prompts/cad_application_assist/tertiary/05_solidworks_drawings.md` |
| 06 | SolidWorks Assembly BOM | `cad_application_assist.tertiary.06` | `prompts/cad_application_assist/tertiary/06_solidworks_assembly_bom.md` |
| 07 | SolidWorks Troubleshoot | `cad_application_assist.tertiary.07` | `prompts/cad_application_assist/tertiary/07_solidworks_troubleshoot.md` |
| 08 | SolidWorks Handoff | `cad_application_assist.tertiary.08` | `prompts/cad_application_assist/tertiary/08_solidworks_handoff.md` |

## Patent Drawing Standards

Turn cleaned mechanical concepts into patent-style drawing instructions without claiming legal compliance.

### Utility Patent Figures (`primary`)

| Slot | Label | Runtime key | Path |
| --- | --- | --- | --- |
| 01 | Figure List | `patent_drawing_standards.primary.01` | `prompts/patent_drawing_standards/primary/01_figure_list.md` |
| 02 | Mechanical To Patent | `patent_drawing_standards.primary.02` | `prompts/patent_drawing_standards/primary/02_mechanical_to_patent.md` |
| 03 | Reference Numerals | `patent_drawing_standards.primary.03` | `prompts/patent_drawing_standards/primary/03_reference_numerals.md` |
| 04 | View Plan | `patent_drawing_standards.primary.04` | `prompts/patent_drawing_standards/primary/04_view_plan.md` |
| 05 | Exploded View | `patent_drawing_standards.primary.05` | `prompts/patent_drawing_standards/primary/05_exploded_view.md` |
| 06 | Detail View | `patent_drawing_standards.primary.06` | `prompts/patent_drawing_standards/primary/06_detail_view.md` |
| 07 | Figure Descriptions | `patent_drawing_standards.primary.07` | `prompts/patent_drawing_standards/primary/07_figure_descriptions.md` |
| 08 | Illustrator Brief | `patent_drawing_standards.primary.08` | `prompts/patent_drawing_standards/primary/08_illustrator_brief.md` |

### Cross-Sections / Hatching (`secondary`)

| Slot | Label | Runtime key | Path |
| --- | --- | --- | --- |
| 01 | Section Cut | `patent_drawing_standards.secondary.01` | `prompts/patent_drawing_standards/secondary/01_section_cut.md` |
| 02 | Section View | `patent_drawing_standards.secondary.02` | `prompts/patent_drawing_standards/secondary/02_section_view.md` |
| 03 | Hatching Plan | `patent_drawing_standards.secondary.03` | `prompts/patent_drawing_standards/secondary/03_hatching_plan.md` |
| 04 | Material Distinction | `patent_drawing_standards.secondary.04` | `prompts/patent_drawing_standards/secondary/04_material_distinction.md` |
| 05 | Avoid Label Interference | `patent_drawing_standards.secondary.05` | `prompts/patent_drawing_standards/secondary/05_avoid_label_interference.md` |
| 06 | Section Numerals | `patent_drawing_standards.secondary.06` | `prompts/patent_drawing_standards/secondary/06_section_numerals.md` |
| 07 | Section Clarity | `patent_drawing_standards.secondary.07` | `prompts/patent_drawing_standards/secondary/07_section_clarity.md` |
| 08 | Final Section Prompt | `patent_drawing_standards.secondary.08` | `prompts/patent_drawing_standards/secondary/08_final_section_prompt.md` |

### Patent Drawing Review (`tertiary`)

| Slot | Label | Runtime key | Path |
| --- | --- | --- | --- |
| 01 | Line Clarity | `patent_drawing_standards.tertiary.01` | `prompts/patent_drawing_standards/tertiary/01_line_clarity.md` |
| 02 | Numeral Check | `patent_drawing_standards.tertiary.02` | `prompts/patent_drawing_standards/tertiary/02_numeral_check.md` |
| 03 | Figure Labels | `patent_drawing_standards.tertiary.03` | `prompts/patent_drawing_standards/tertiary/03_figure_labels.md` |
| 04 | Missing Views | `patent_drawing_standards.tertiary.04` | `prompts/patent_drawing_standards/tertiary/04_missing_views.md` |
| 05 | Sheet Margin Risk | `patent_drawing_standards.tertiary.05` | `prompts/patent_drawing_standards/tertiary/05_sheet_margin_risk.md` |
| 06 | Figure Spec Flow | `patent_drawing_standards.tertiary.06` | `prompts/patent_drawing_standards/tertiary/06_figure_spec_flow.md` |
| 07 | Crowding Review | `patent_drawing_standards.tertiary.07` | `prompts/patent_drawing_standards/tertiary/07_crowding_review.md` |
| 08 | Objection Risk List | `patent_drawing_standards.tertiary.08` | `prompts/patent_drawing_standards/tertiary/08_objection_risk_list.md` |

## Patent Flowcharts / System Diagrams

Create patent-style process diagrams, system diagrams, architecture diagrams, and method flowcharts.

### Flowcharts (`primary`)

| Slot | Label | Runtime key | Path |
| --- | --- | --- | --- |
| 01 | Method Flowchart | `patent_flowcharts_system_diagrams.primary.01` | `prompts/patent_flowcharts_system_diagrams/primary/01_method_flowchart.md` |
| 02 | Numbered Steps | `patent_flowcharts_system_diagrams.primary.02` | `prompts/patent_flowcharts_system_diagrams/primary/02_numbered_steps.md` |
| 03 | Decision Blocks | `patent_flowcharts_system_diagrams.primary.03` | `prompts/patent_flowcharts_system_diagrams/primary/03_decision_blocks.md` |
| 04 | Alternate Paths | `patent_flowcharts_system_diagrams.primary.04` | `prompts/patent_flowcharts_system_diagrams/primary/04_alternate_paths.md` |
| 05 | Simplify Flowchart | `patent_flowcharts_system_diagrams.primary.05` | `prompts/patent_flowcharts_system_diagrams/primary/05_simplify_flowchart.md` |
| 06 | Flow Numerals | `patent_flowcharts_system_diagrams.primary.06` | `prompts/patent_flowcharts_system_diagrams/primary/06_flow_numerals.md` |
| 07 | Figure Caption | `patent_flowcharts_system_diagrams.primary.07` | `prompts/patent_flowcharts_system_diagrams/primary/07_figure_caption.md` |
| 08 | Final Flow Prompt | `patent_flowcharts_system_diagrams.primary.08` | `prompts/patent_flowcharts_system_diagrams/primary/08_final_flow_prompt.md` |

### System Diagrams (`secondary`)

| Slot | Label | Runtime key | Path |
| --- | --- | --- | --- |
| 01 | Block Diagram | `patent_flowcharts_system_diagrams.secondary.01` | `prompts/patent_flowcharts_system_diagrams/secondary/01_block_diagram.md` |
| 02 | Module Diagram | `patent_flowcharts_system_diagrams.secondary.02` | `prompts/patent_flowcharts_system_diagrams/secondary/02_module_diagram.md` |
| 03 | Data Flow | `patent_flowcharts_system_diagrams.secondary.03` | `prompts/patent_flowcharts_system_diagrams/secondary/03_data_flow.md` |
| 04 | HW SW Boundary | `patent_flowcharts_system_diagrams.secondary.04` | `prompts/patent_flowcharts_system_diagrams/secondary/04_hw_sw_boundary.md` |
| 05 | Signal Control Path | `patent_flowcharts_system_diagrams.secondary.05` | `prompts/patent_flowcharts_system_diagrams/secondary/05_signal_control_path.md` |
| 06 | System Numerals | `patent_flowcharts_system_diagrams.secondary.06` | `prompts/patent_flowcharts_system_diagrams/secondary/06_system_numerals.md` |
| 07 | Architecture Caption | `patent_flowcharts_system_diagrams.secondary.07` | `prompts/patent_flowcharts_system_diagrams/secondary/07_architecture_caption.md` |
| 08 | Final System Prompt | `patent_flowcharts_system_diagrams.secondary.08` | `prompts/patent_flowcharts_system_diagrams/secondary/08_final_system_prompt.md` |

### Figure-to-Spec Mapping (`tertiary`)

| Slot | Label | Runtime key | Path |
| --- | --- | --- | --- |
| 01 | Figure To Spec | `patent_flowcharts_system_diagrams.tertiary.01` | `prompts/patent_flowcharts_system_diagrams/tertiary/01_figure_to_spec.md` |
| 02 | Numeral Map | `patent_flowcharts_system_diagrams.tertiary.02` | `prompts/patent_flowcharts_system_diagrams/tertiary/02_numeral_map.md` |
| 03 | Flow To Method Text | `patent_flowcharts_system_diagrams.tertiary.03` | `prompts/patent_flowcharts_system_diagrams/tertiary/03_flow_to_method_text.md` |
| 04 | Missing Spec Support | `patent_flowcharts_system_diagrams.tertiary.04` | `prompts/patent_flowcharts_system_diagrams/tertiary/04_missing_spec_support.md` |
| 05 | Unsupported Figure Elements | `patent_flowcharts_system_diagrams.tertiary.05` | `prompts/patent_flowcharts_system_diagrams/tertiary/05_unsupported_figure_elements.md` |
| 06 | Figure Paragraph | `patent_flowcharts_system_diagrams.tertiary.06` | `prompts/patent_flowcharts_system_diagrams/tertiary/06_figure_paragraph.md` |
| 07 | Consistency Table | `patent_flowcharts_system_diagrams.tertiary.07` | `prompts/patent_flowcharts_system_diagrams/tertiary/07_consistency_table.md` |
| 08 | Spec Mapping Packet | `patent_flowcharts_system_diagrams.tertiary.08` | `prompts/patent_flowcharts_system_diagrams/tertiary/08_spec_mapping_packet.md` |

## Figure Packet / Release Review

Assemble drawings, CAD instructions, patent figures, flowcharts, and review notes into a complete drawing packet.

### Figure Packet Builder (`primary`)

| Slot | Label | Runtime key | Path |
| --- | --- | --- | --- |
| 01 | Figure Inventory | `figure_packet_release_review.primary.01` | `prompts/figure_packet_release_review/primary/01_figure_inventory.md` |
| 02 | Figure Order | `figure_packet_release_review.primary.02` | `prompts/figure_packet_release_review/primary/02_figure_order.md` |
| 03 | Mechanical Group | `figure_packet_release_review.primary.03` | `prompts/figure_packet_release_review/primary/03_mechanical_group.md` |
| 04 | Section Detail Group | `figure_packet_release_review.primary.04` | `prompts/figure_packet_release_review/primary/04_section_detail_group.md` |
| 05 | Flow System Group | `figure_packet_release_review.primary.05` | `prompts/figure_packet_release_review/primary/05_flow_system_group.md` |
| 06 | Drawing Task List | `figure_packet_release_review.primary.06` | `prompts/figure_packet_release_review/primary/06_drawing_task_list.md` |
| 07 | Illustrator Handoff | `figure_packet_release_review.primary.07` | `prompts/figure_packet_release_review/primary/07_illustrator_handoff.md` |
| 08 | Packet Summary | `figure_packet_release_review.primary.08` | `prompts/figure_packet_release_review/primary/08_packet_summary.md` |

### Consistency QA (`secondary`)

| Slot | Label | Runtime key | Path |
| --- | --- | --- | --- |
| 01 | Numeral Consistency | `figure_packet_release_review.secondary.01` | `prompts/figure_packet_release_review/secondary/01_numeral_consistency.md` |
| 02 | Terminology Consistency | `figure_packet_release_review.secondary.02` | `prompts/figure_packet_release_review/secondary/02_terminology_consistency.md` |
| 03 | Missing Views | `figure_packet_release_review.secondary.03` | `prompts/figure_packet_release_review/secondary/03_missing_views.md` |
| 04 | Duplicate Figures | `figure_packet_release_review.secondary.04` | `prompts/figure_packet_release_review/secondary/04_duplicate_figures.md` |
| 05 | Unresolved Dimensions | `figure_packet_release_review.secondary.05` | `prompts/figure_packet_release_review/secondary/05_unresolved_dimensions.md` |
| 06 | Open Questions | `figure_packet_release_review.secondary.06` | `prompts/figure_packet_release_review/secondary/06_open_questions.md` |
| 07 | Drawing Risks | `figure_packet_release_review.secondary.07` | `prompts/figure_packet_release_review/secondary/07_drawing_risks.md` |
| 08 | QA Report | `figure_packet_release_review.secondary.08` | `prompts/figure_packet_release_review/secondary/08_qa_report.md` |

### Final Handoff (`tertiary`)

| Slot | Label | Runtime key | Path |
| --- | --- | --- | --- |
| 01 | CAD Handoff | `figure_packet_release_review.tertiary.01` | `prompts/figure_packet_release_review/tertiary/01_cad_handoff.md` |
| 02 | Patent Illustrator Handoff | `figure_packet_release_review.tertiary.02` | `prompts/figure_packet_release_review/tertiary/02_patent_illustrator_handoff.md` |
| 03 | Attorney Review Handoff | `figure_packet_release_review.tertiary.03` | `prompts/figure_packet_release_review/tertiary/03_attorney_review_handoff.md` |
| 04 | Invention Notebook Summary | `figure_packet_release_review.tertiary.04` | `prompts/figure_packet_release_review/tertiary/04_invention_notebook_summary.md` |
| 05 | Filing Support Notes | `figure_packet_release_review.tertiary.05` | `prompts/figure_packet_release_review/tertiary/05_filing_support_notes.md` |
| 06 | Final Open Questions | `figure_packet_release_review.tertiary.06` | `prompts/figure_packet_release_review/tertiary/06_final_open_questions.md` |
| 07 | Next Action Checklist | `figure_packet_release_review.tertiary.07` | `prompts/figure_packet_release_review/tertiary/07_next_action_checklist.md` |
| 08 | Final Release Packet | `figure_packet_release_review.tertiary.08` | `prompts/figure_packet_release_review/tertiary/08_final_release_packet.md` |
