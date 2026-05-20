---
name: hybrid-ppt-builder
description: Create, convert, or revise academic and industrial formal-report PowerPoint decks using a hybrid editable-layer strategy. Use for PPT/PPTX generation, slide redesign, background-preserving conversions, reference background image style matching, SVG-to-PowerPoint decisions, editable foreground reconstruction, preview validation, thesis/defense-style decks, technical project reports, engineering summaries, industrial operation reports, training reports, and internal technical reviews.
---

# Hybrid PPT Builder

## Scope

This skill is for academic and industrial formal report decks: research presentations, thesis/defense-style decks, technical project reports, engineering summaries, industrial operation reports, training reports, and internal technical reviews.

Do not optimize for marketing decks, sales decks, landing-page style presentations, casual event slides, pitch decks, or highly decorative business templates.

## Core Strategy

Build decks by object type, not by whole-slide shortcuts:

- **Stable complex backgrounds**: keep as PNG/JPEG slide backgrounds when they are not meant to be edited.
- **Important foreground content**: create PowerPoint-native text boxes, lines, rectangles, tables, charts, timelines, callouts, and layout containers.
- **Complex foreground graphics that are rarely edited**: use SVG modules for icons, technical symbols, decorative marks, and complex illustrations.
- **Editable data visuals**: use native PowerPoint charts/tables when values or labels may change.
- **Visual-only drafts**: use full-slide PNG only for fast previews, never as the final editable deliverable unless the user explicitly accepts non-editability.

For this skill's formal-report scope, the default best balance is: **stable PNG/JPEG master background + PowerPoint-native text/layout + SVG icons or complex decorative modules**.

## Formal Report Background / Foreground Contract

For academic and industrial formal report decks, define the background/foreground contract before building or redesigning.

### Background Layer

The background layer provides formal report identity, domain atmosphere, spatial structure, and visual continuity. It may be a stable PNG/JPEG master background when it is decorative and not meant to change slide by slide.

A valid formal-report background is not just sparse decoration. It should include a coherent visual system:

- a restrained light canvas;
- consistent page furniture such as header line, footer area, page number, or section marker;
- subtle academic or industrial domain cues, such as equipment line art, architectural structure, lab/engineering grid, data texture, process geometry, or technical drawing traces;
- clear content zones where foreground text, charts, tables, and diagrams can sit without interference.

Default for this skill:

- Use one unified master background unless the source deck or user explicitly requires preserved backgrounds or variants.
- Keep the background light, low-contrast, and formal.
- Place stronger background detail near edges, corners, headers, footers, or intentionally empty zones.
- Keep main reading areas clean.
- Do not let background graphics cross small text, charts, tables, or dense diagrams.
- Do not treat a few lines, dots, or isolated shapes as a complete background system.

### Foreground Layer

The foreground layer carries all slide-specific meaning and must remain editable.

Foreground includes:

- slide titles, subtitles, section labels, and page numbers when they change per slide;
- key claims, bullet points, conclusions, quotes, and speaker-facing structure;
- charts, tables, timelines, process diagrams, arrows, cards, callouts, labels, and data annotations;
- all case-specific, research-specific, or project-specific logic.

Implement foreground with:

- PowerPoint-native text boxes for important text;
- native shapes for cards, lines, arrows, diagrams, timelines, and labels;
- native tables/charts when values or labels may need editing;
- SVG only for stable supporting graphics, unless PowerPoint conversion is validated and usable.

Do not put core slide logic, editable labels, key claims, data, or conclusions only inside a background image, full-slide screenshot, or non-editable SVG.

## Reference Background Image Mode

When the user provides a background image, first decide whether it should be used directly as a master background or treated only as a style reference.

1. **Use as master background**
   - Use when the image is already suitable as a formal-report slide background.
   - It should be 16:9 or safely croppable to 16:9.
   - It should have clean title, body, chart, table, and diagram zones.
   - It should not contain slide-specific claims, dense text, editable labels, or foreground logic.
   - Insert it as a stable background layer and build all slide-specific content as editable foreground objects.

2. **Use as style reference**
   - Use when the image has useful visual style but is not suitable as a direct slide background.
   - Extract the visual system: colors, contrast, motifs, page furniture, line weights, card style, and safe content zones.
   - Generate or construct a clean 16:9 formal-report background inspired by that style.
   - Use the `imagegen` skill when an AI-generated or edited raster background asset is needed; otherwise create deterministic raster/vector-style background assets locally.
   - Do not copy slide-specific text or logic from the reference image into the background.

Match foreground styling to the chosen or generated background: sample compatible title/accent colors, line weights, card transparency, dividers, badges, and chart highlights from the reference style while keeping important text readable and editable.

## SVG Policy

Treat these as different deliverables:

1. SVG source files.
2. SVG images inserted into PowerPoint.
3. SVG that PowerPoint can convert to editable shapes.
4. PowerPoint-native editable shapes created directly.

Do not call an embedded SVG image "PowerPoint editable" unless it has been converted and validated. If the user wants editability, keep titles, body text, page highlights, labels, and layout structure native even when SVG is used for icons.

Always consider convertible SVG for complex foreground graphics when the local Office version supports it, but validate first. Use a small test SVG or the actual module and check:

- the PowerPoint conversion command is available;
- converted objects remain selectable;
- key text remains editable text when text editability matters;
- object groups are usable, not an unmanageable pile of fragments;
- visual output does not change.

If conversion is unavailable or unstable, use native PowerPoint shapes for important/editable parts and SVG images only for stable non-editable graphics.

## Workflow

1. **Clarify or infer requirements**
   - Source PPT/PPTX or content source.
   - Page range.
   - Output path and naming.
   - Whether the background must remain unchanged.
   - Which foreground items must stay editable.
   - Whether SVG source files, preview PNGs, or speaker notes are needed.
   - Background/foreground contract: infer or clarify the formal-report background system, including whether to use one unified master background, preserve source backgrounds, or support explicit variants; identify which elements may be flattened and which must remain editable.
   - If a background image is provided, decide whether it is a direct master background or a style reference.

2. **Inspect the source**
   - Open or parse the deck when possible.
   - Identify background elements versus foreground content.
   - For a provided background image, inspect canvas ratio, crop safety, palette, contrast, visual motifs, page furniture, safe foreground zones, and risk zones.
   - Visually inspect the provided background image before deciding its mode; do not infer style only from filename or metadata.
   - Check existing scripts, assets, fonts, and prior output files.
   - Avoid hard-coded dependency paths unless already verified in the current environment.

3. **Choose object-level implementation**
   - Background: image layer.
   - Page title, core message, bullets, labels: native text boxes.
   - Cards, grids, timeline lines, arrows, badges: native shapes.
   - Icons and complex but stable drawings: SVG modules.
   - Charts/tables expected to be edited: native chart/table objects.
   - Keep background stable, formal, and decorative; keep slide-specific academic/industrial argument, data, labels, and logic in native foreground objects.
   - If using a reference background image, derive the foreground style from it but keep all slide-specific meaning in native foreground objects.

4. **Generate the PPTX**
   - Prefer `python-pptx` or PowerPoint COM for native shapes.
   - Use SVG files for complex icon modules and insert them as separate objects.
   - Keep foreground modules separate enough to edit or replace.
   - Do not flatten the full foreground into one image.

5. **Validate before final response**
   - Open the PPTX with PowerPoint when available.
   - Export slide previews and a contact sheet.
   - Check page count, 16:9 dimensions, background placement, and visual alignment.
   - Check that editable slides contain many foreground objects, not only a background plus one image.
   - Inspect the PPTX package media folder when useful; a truly native foreground should not appear as one full-slide foreground image.
   - Verify Chinese text is not garbled and does not overlap, overflow, or become too small.
   - Verify important foreground text and slide-specific logic are native editable objects.
   - Verify background media is stable and decorative, not carrying required content.
   - Verify exported previews show no background interference with foreground reading zones.
   - Verify the background establishes a coherent academic/industrial formal style, not merely empty ornament.
   - If a reference background image was supplied, verify the deck visually matches its formal style without embedding required content in the background.

6. **Report clearly**
   - Provide the output file path.
   - State whether the result is editable and what kind of editability it has.
   - State how editability was verified, including object counts or media checks when relevant.
   - If a background image was provided, state whether it was used directly as the master background or only as a style reference.
   - Mention any remaining manual review point.

## Quality Preferences

- Use restrained academic/industrial formal report styling.
- Prefer light backgrounds, blue or blue-gray accents, and technical/engineering visual cues unless the source design requires otherwise.
- Avoid heavy shadows, crowded cards, gratuitous gradients, and marketing-page composition.
- Preserve user-requested structure and background; do not restyle unrelated pages during a narrow conversion.
- Make slide text short enough to fit and support it with speaker notes or source narrative when available.

## Reference

For reusable Chinese prompt templates and phase-by-phase wording, read `references/prompt-templates.md` when the user asks for a prompt, reusable workflow, or a reminder of the preferred PPT production process.
