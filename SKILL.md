---
name: hybrid-ppt-builder
description: Create, convert, or revise academic and industrial formal-report PowerPoint decks using a hybrid editable-layer strategy. Use for PPT/PPTX generation, slide redesign, manuscript-to-deck work, background-preserving conversions, reference background image style matching, SVG-to-PowerPoint decisions, editable foreground reconstruction, preview validation, package/object inspection, thesis/defense-style decks, technical project reports, engineering summaries, industrial operation reports, training reports, and internal technical reviews.
---

# Hybrid PPT Builder

## Scope

Use this skill for academic and industrial formal report decks: research presentations, thesis/defense-style decks, technical project reports, engineering summaries, industrial operation reports, training reports, and internal technical reviews.

Enterprise internal event reports, growth-sharing talks, onboarding reflections, and training summaries are in scope when the desired result should feel like a formal internal report rather than an event poster or casual talk deck.

Do not optimize for marketing decks, sales decks, landing-page style presentations, casual event slides, pitch decks, or highly decorative business templates. If event-like source content is ambiguous, infer a restrained formal-report direction unless the user requests a more casual or decorative style.

## Top-level Modes and Rules

Use one of these modes deliberately:

- **Default editable PPTX mode (preferred):** create a final `.pptx` with stable background layers and PowerPoint-native foreground text, shapes, tables, charts, and layout objects.
- **Source reconstruction mode:** rebuild selected existing slides, screenshots, PDF pages, or flattened slides into editable foreground layers while preserving or recreating the background.
- **Manuscript-to-deck mode:** convert a script, article, markdown document, report, or speech draft into a formal report deck.
- **Reference visual system mode:** use a provided background or reference image either directly as a master background or as a style reference for a new clean background system.
- **Background asset mode:** create or edit a raster background asset only when the deck needs it. Use the `imagegen` skill for AI-generated raster backgrounds; use deterministic local drawing when that is sufficient.
- **Visual-only draft mode:** use full-slide PNG/JPEG output only for quick previews or when the user explicitly accepts low editability. Do not treat it as the default final deliverable.

Rules:

- Default to editable PPTX mode. Do not silently downgrade to full-slide screenshots, flattened SVG, image-only tables, non-editable foreground images, or a final deck without preview validation.
- Ask before delivering a low-editability final deck unless the user explicitly requested a visual-only draft, one-shot output, or no confirmation.
- Keep all slide-specific claims, labels, conclusions, data, and reading logic in editable foreground objects.
- Use visual approval gates for a new or materially changed deck-wide visual system unless the user explicitly asks to skip confirmations.
- Do not require approval for the slide outline unless the user explicitly asks for content planning. The gates are for visual execution and readability.
- Do not use `imagegen` just because a background exists. Preserve a suitable source background or construct a deterministic background when that is more controlled.
- If a required source file, data table, brand asset, or reference image is missing and cannot be inferred safely, ask for it. Otherwise proceed with conservative assumptions.

## Decision Tree

Classify each request with these exact task slugs:

- `create-formal-deck`: create a new formal report deck from structured content or a brief.
- `manuscript-to-deck`: condense a long script, article, report, markdown file, or speech draft into slides.
- `rebuild-existing-slides`: remake existing slides so foreground content becomes editable.
- `preserve-background-conversion`: keep the original background unchanged and reconstruct editable foreground content.
- `reference-background-match`: use a provided background or image as the visual source.
- `narrow-slide-edit`: make a scoped edit to selected slides while preserving the current visual system.
- `svg-to-ppt-evaluation`: decide whether SVG should remain source, be inserted, be converted, or be rebuilt as native shapes.
- `visual-sample`: produce background candidates or a small approved sample before full deck generation.

For every task, answer four questions before implementation:

1. **Task type:** which slug above applies, and what pages or sections are in scope?
2. **Visual system:** preserve source background, use provided image directly, derive a new style from a reference, generate a new raster background, or construct a deterministic background?
3. **Editability contract:** which objects must be PowerPoint-native, which can be stable SVG/images, and which low-editability parts were explicitly accepted?
4. **Approval strategy:** use Gate 1, Gate 2, both, or skip because the user explicitly requested one-shot/fast/no-confirmation output?

## Input Role Classification

Label every input before using it:

- `source deck`: PPT/PPTX/PDF/slides to inspect, preserve, convert, or rebuild.
- `target slide range`: pages or sections that should change.
- `content manuscript`: source text, report, markdown, transcript, or outline to condense into slides.
- `data source`: spreadsheet, table, chart values, metrics, or labels that must remain accurate.
- `background reference`: image intended as a direct reusable slide background.
- `style reference`: image or deck used only for colors, motifs, line weights, page furniture, and density.
- `brand asset`: logo, font, color, icon set, or required corporate identity material.
- `editable target`: objects, text, charts, or diagrams the user expects to edit later.

Do not infer visual style only from a filename or metadata. Inspect decks, images, and exports when available.

## Background / Foreground Contract

Build decks by object type, not by whole-slide shortcuts.

The default formal-report balance is: **stable PNG/JPEG master background + PowerPoint-native text/layout + SVG icons or complex decorative modules**.

Background layer:

- Carries stable identity, domain atmosphere, spatial structure, and continuity.
- May be a PNG/JPEG master background when decorative and not meant to change slide by slide.
- Should use a restrained light canvas, consistent page furniture, subtle academic or industrial cues, and clean safe zones for text/charts/tables.
- Should place stronger detail near edges, corners, headers, footers, or intentionally empty zones.
- Must not carry required slide-specific logic, dense text, conclusions, labels, or data.
- Must not interfere with small text, charts, tables, or dense diagrams.

Foreground layer:

- Carries all slide-specific meaning and must remain editable by default.
- Includes titles, subtitles, page numbers when variable, claims, bullets, quotes, charts, tables, timelines, process diagrams, arrows, cards, callouts, labels, and data annotations.
- Use PowerPoint-native text boxes for important text.
- Use native shapes for cards, lines, arrows, diagrams, timelines, labels, badges, and layout containers.
- Use native tables/charts when values or labels may need editing.
- Use SVG only for stable supporting graphics unless PowerPoint conversion is validated and useful.

## Reference Background Image Mode

When the user provides a background image, decide whether to use it directly or treat it only as a style reference.

Use it as a master background when:

- it is already suitable for a formal-report slide background;
- it is 16:9 or safely croppable to 16:9;
- it has clean title, body, chart, table, and diagram zones;
- it does not contain slide-specific claims, dense text, editable labels, or foreground logic.

Use it as a style reference when:

- the image has useful visual style but is not suitable as a direct slide background;
- it contains slide-specific content, dense text, or unsafe foreground zones;
- a cleaner 16:9 formal-report background should be generated or constructed from its colors, contrast, motifs, page furniture, line weights, and safe zones.

Match foreground styling to the chosen or generated background: sample compatible title/accent colors, line weights, card transparency, dividers, badges, and chart highlights while keeping important text readable and editable.

## Approval and Iteration Rules

Gate 1: Background Candidate Approval.

- Use when `imagegen` generates or edits a background, a provided image is used as a style reference, multiple backgrounds are available, or a new deterministic background will become the deck-wide master background.
- Show the background candidate(s) and ask whether to use it, revise it, generate a different direction, use the original image directly, or switch to deterministic local construction.
- Do not build the full deck until the background direction is confirmed, unless the user explicitly asked for one-shot/fast/no-confirmation output.

Gate 2: Visual Sample Approval.

- Use before a full deck when a new or materially changed visual system, foreground density, or typography direction is involved.
- Build a small sample, usually one cover/title slide, one dense content slide, and one diagram/card/process slide when relevant.
- Ask the user to judge background/foreground fit, typography, information density, chart/card/divider style, and whether the result feels like an academic or industrial formal report.

Iteration rule:

- After a gate or preview review, make one targeted visual change per iteration when possible: background, typography, density, palette, chart style, or layout structure. Re-check after each change.
- If gates are skipped, say why in the final report and still validate previews before delivery.

## Manuscript-to-Deck Handling

When the source is a script, article, markdown document, speech draft, or report:

- Preserve the source argument, terminology, and evidence. Do not invent new claims or reorder logic in a way that changes meaning.
- Condense prose into slide claims, short bullets, diagrams, timelines, cards, or tables.
- Keep slide text short enough to read comfortably; move supporting detail into speaker notes when useful or requested.
- Treat the slide outline as an implementation decision unless the user asks to approve content planning.
- Use Gate 2 to validate typography, density, and reading comfort before full generation when gates apply.

## SVG and Tool Capability Boundaries

Treat these as different deliverables:

1. SVG source files.
2. SVG images inserted into PowerPoint.
3. SVG that PowerPoint can convert to editable shapes.
4. PowerPoint-native editable shapes created directly.

Do not call an embedded SVG image "PowerPoint editable" unless it has been converted and validated. If editability matters, keep titles, body text, page highlights, labels, and layout structure native even when SVG is used for icons or technical symbols.

Tool boundaries:

- `python-pptx`: good for deterministic PPTX creation with native text boxes, shapes, images, tables, and basic charts. It does not validate real PowerPoint rendering.
- PowerPoint COM: preferred when available for opening, exporting previews, checking actual rendering, and testing SVG-to-shape conversion.
- LibreOffice: useful fallback for preview export, but rendering can differ from PowerPoint; report that limitation.
- PPTX package/XML inspection: useful for object counts, media counts, native text extraction, and detecting flattened foregrounds. It does not replace visual preview.
- `imagegen`: use only for raster background/assets that benefit from AI generation or editing. Follow the imagegen skill's save-path policy; never leave a deck-referenced asset only under `$CODEX_HOME/*`.

If SVG conversion is unavailable or unstable, use native PowerPoint shapes for important/editable parts and inserted SVG/images only for stable non-editable graphics.

## Output and Artifact Policy

If the user gives paths, honor them. If not, write project artifacts under the current workspace:

- final deck: `output/<descriptive-name>.pptx`;
- previews: `output/previews/<descriptive-name>/slide-XX.png`;
- contact sheet: `output/previews/<descriptive-name>-contact-sheet.png`;
- deck-specific backgrounds: `output/assets/backgrounds/`;
- SVG modules or sources: `output/assets/svg/`;
- temporary files: `tmp/hybrid-ppt-builder/`.

Do not overwrite an existing deck or asset unless the user explicitly asked for replacement. Use a descriptive versioned filename instead.

Keep final project-referenced assets inside the workspace. Temporary exports and discarded variants can be deleted after validation unless the user asks to keep them.

## Workflow

1. **Clarify or infer requirements**
   - Source file(s), input roles, target slide range, output path, language, style constraints, and whether speaker notes are needed.
   - Background/foreground contract, including preserved backgrounds, unified master background, variants, and editability expectations.
   - Approval strategy and whether the user requested one-shot/fast/no-confirmation output.

2. **Inspect inputs**
   - Open or parse decks when possible.
   - Export or view source slides/images when useful.
   - Inspect reference backgrounds for ratio, crop safety, palette, contrast, motifs, page furniture, safe zones, and risk zones.
   - Check existing scripts, assets, fonts, and prior outputs.
   - Avoid hard-coded dependency paths unless verified in the current environment.

3. **Choose object-level implementation**
   - Background: stable image layer or deterministic native/raster construction.
   - Titles, claims, bullets, labels: native text boxes.
   - Cards, grids, timelines, arrows, badges: native shapes.
   - Icons and complex stable drawings: SVG modules or images.
   - Editable data visuals: native charts/tables when practical.
   - Keep slide-specific academic/industrial logic native.

4. **Generate candidates, samples, or final deck**
   - Apply Gate 1 and Gate 2 when required.
   - Prefer `python-pptx` or PowerPoint COM for native objects.
   - Keep foreground modules separate enough to select, edit, or replace.
   - Do not flatten the full foreground into one image.

5. **Validate before final response**
   - Open the PPTX with PowerPoint when available.
   - Export slide previews and a contact sheet.
   - Check page count, 16:9 dimensions, background placement, alignment, and text readability.
   - Check editable slides contain multiple native foreground objects, not only a background plus one foreground image.
   - Inspect package media and XML when useful. Use `scripts/inspect_pptx.py` for object counts and native text evidence.
   - Verify required slide-specific terms are present as native text.
   - Verify Chinese text is not garbled and does not overlap, overflow, or become too small.
   - Verify background media is stable/decorative and does not carry required content.
   - If PowerPoint export is unavailable, use LibreOffice export or package inspection and clearly state the manual preview requirement.

6. **Report clearly**
   - Output file path, page count, task slug, mode used, and whether gates were used or skipped.
   - Editability level and what remains native versus stable image/SVG.
   - Validation method, including preview export, package/object counts, native text checks, or fallback limitations.
   - Whether a reference background was used directly or only as a style reference.
   - Remaining manual review points.

## Quality Preferences

- Use restrained academic/industrial formal report styling.
- Prefer light backgrounds, blue or blue-gray accents, and technical or engineering visual cues unless the source design requires otherwise.
- Avoid heavy shadows, crowded cards, gratuitous gradients, decorative business templates, and marketing-page composition.
- Preserve user-requested structure and backgrounds during narrow conversions.
- Make slide text short enough to fit; use speaker notes for supporting detail when available.

## Reference Map

- `references/prompting.md`: read when shaping content, visual direction, density, Chinese typography, or imagegen background prompts.
- `references/sample-prompts.md`: read when the user wants reusable prompts, Chinese workflow prompts, or copy/paste task recipes.
- `references/prompt-templates.md`: compatibility entry for older Chinese prompt-template workflows; prefer `references/sample-prompts.md` for new work.
- `scripts/inspect_pptx.py`: run when a PPTX deliverable needs package/object/native-text inspection.
