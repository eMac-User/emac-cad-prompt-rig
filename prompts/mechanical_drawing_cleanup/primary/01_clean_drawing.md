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
