# Clean Drawing (Un-Dim)

**Profile:** Rough-In Parts  
**Board:** Primary — rough-in image workflow  
**Slot:** 2  
**Runtime key:** `rough_in_part_development.primary.02`

## Prompt

You are helping with **Rough-In Parts** work. Use this prompt slot for **creating an undimensioned CAD trace master**.

### Goal

Create a practical, bounded result that turns a rough sketch, rough invention concept, or cleaned mechanical drawing into a pure black-and-white closed-contour trace image for drafting import or extrusion workflows.

### Use when

Use this when I want the final image to be geometry-only so I can trace it, vectorize it, import it into a drafting program, or feed it into my own contour/extrusion pipeline.

### Source material

Use the current chat context and any image, drawing, cleaned reference, CAD screenshot, AI-generated concept image, or notes I provide after this prompt. If required context is missing, ask for the smallest missing piece rather than inventing details.

### Rules

- Identify the visible part outline, cutouts, holes, slots, and rounded features.
- Use dimensions only as internal proportion guides.
- Do not draw any dimensions, numbers, arrows, labels, notes, callouts, title blocks, grids, construction lines, or text.
- Straighten lines that should be horizontal or vertical.
- Make corners square unless the source clearly shows a radius, chamfer, or fillet.
- Make circular holes true circles.
- Make the final linework clean, closed, and traceable.
- Remove sketch noise, shadows, smudges, paper texture, and background clutter.
- Preserve design intent, not ugly geometry.

### Output format

Return the result using these sections:

1. Observed geometry
2. Preserved dimensions
3. Cleanup instructions
4. CAD drafter notes

### Final instruction

Be practical, specific, and bounded. When you assemble the final image prompt, make it request a clean undimensioned closed-contour CAD trace master in black line art on a pure white background, with crisp straight edges, true circular holes, consistent line weight, no text of any kind, no shading, no perspective, and no decorative styling.

### Workflow intent

This is **Step 2** of the rough-in image workflow:

- Upload the same sketch or the cleaned reference + this prompt
- Get an **undimensioned CAD trace master**
- Use the result as the clean import / trace / extrude target
