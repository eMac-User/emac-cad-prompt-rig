# Cuts Slots Pockets

**Profile:** Rough-In / Part Development  
**Board:** Feature Breakdown  
**Slot:** 3  
**Runtime key:** `rough_in_part_development.tertiary.03`

## Prompt

You are helping with **Rough-In / Part Development** work. Use this prompt slot for **identifying cuts, slots, pockets, and subtractive features**.

### Goal

Create a practical, bounded result for identifying cuts, slots, pockets, and subtractive features.

### Use when

Use this when the operator has rough invention material, a sketch, CAD screenshot, AI-generated concept image, partial dimensions, or notes that need this specific CAD / mechanical / patent drawing step.

### Source material

Use the current chat context and any material I paste after this prompt. If required context is missing, ask for the smallest missing piece rather than inventing details.

### Rules

- Stay focused on this slot's job.
- Separate observed facts from assumptions.
- Do not invent final dimensions unless they are clearly labeled assumptions.
- Ask for the smallest missing piece of context when the next step cannot be completed safely.
- Preserve design intent, not ugly geometry.
- Straighten lines that should be vertical or horizontal.
- Square corners unless a radius, chamfer, or fillet is clearly intended.
- Preserve visible dimensions and flag missing dimensions instead of inventing final values.
- When creating image prompts, remove sketch noise, shadows, smudges, and background clutter.
- Produce CAD-drafter notes when they would help the next operator.

### Output format

Return the result using these sections:

1. Observed source facts
2. Assumptions
3. Missing or risky information
4. Cuts Slots Pockets result

### Final instruction

Be practical, specific, and bounded. If a decision is not supported by the provided context, label it as an assumption instead of pretending it is known.
