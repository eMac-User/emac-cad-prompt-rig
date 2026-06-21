# Clean Drawing (Dim)

**Profile:** Rough-In Parts  
**Board:** Primary — rough-in image workflow  
**Slot:** 1  
**Runtime key:** `rough_in_part_development.primary.01`

## Prompt

You are helping with **Rough-In Parts** work. Use this prompt slot for **creating a cleaned mechanical drawing with dimensions still visible**.

### Goal

Create a practical, bounded result that turns a rough sketch, rough invention concept, or messy part image into a cleaner dimensioned mechanical drawing reference.

### Use when

Use this when I have an early rough-in part sketch and I want a cleaner black-and-white drawing that still shows the useful dimensions and unresolved notes from the source.

### Source material

Use the current chat context and any image, drawing, CAD screenshot, AI-generated concept image, or notes I provide after this prompt. If required context is missing, ask for the smallest missing piece rather than inventing details.

### Rules

- Identify the visible part outline, cutouts, holes, slots, radii, and dimension notes.
- Preserve intended dimensions where visible.
- Do not invent final manufacturing dimensions unless clearly labeled as assumptions.
- Straighten lines that should be horizontal or vertical.
- Make corners square unless the source clearly shows a radius, chamfer, or fillet.
- Make circular holes clean and centered only when the source supports that placement.
- Convert rough or uneven lines into clean black-and-white mechanical linework.
- Remove sketch noise, shadows, smudges, and background clutter.
- Add only the useful dimension callouts from the source.
- Flag missing or unclear dimensions instead of hiding them.
- Preserve design intent, not ugly geometry.

### Output format

Return the result using these sections:

1. Observed geometry
2. Preserved dimensions
3. Assumptions
4. Missing dimensions
5. Clean mechanical drawing image prompt
6. CAD drafter notes

### Final instruction

Be practical, specific, and bounded. When you assemble the final image prompt, make it request a crisp black-and-white orthographic front view with readable dimensions, straightened geometry, true circular holes, white background, consistent line weight, and no decorative styling, no photorealism, and no perspective.

### Workflow intent

This is **Step 1** of the rough-in image workflow:

- Upload sketch + this prompt
- Get a **dimensioned cleanup reference**
- Use the result as a visual cleanup sheet, not as final CAD truth
