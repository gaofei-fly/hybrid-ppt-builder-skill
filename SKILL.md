---
name: hybrid-ppt-builder
description: Create, convert, or revise PowerPoint decks using a hybrid editable-layer strategy. Use when Codex works on PPT/PPTX generation, slide redesign, background-preserving conversions, SVG-to-PowerPoint decisions, editable foreground reconstruction, preview validation, or user requests such as "make this PPT editable", "keep the background unchanged", "convert pages to SVG/PPT shapes", or "generate a professional presentation".
---

# Hybrid PPT Builder

## Core Strategy

Build decks by object type, not by whole-slide shortcuts:

- **Stable complex backgrounds**: keep as PNG/JPEG slide backgrounds when they are not meant to be edited.
- **Important foreground content**: create PowerPoint-native text boxes, lines, rectangles, tables, charts, timelines, callouts, and layout containers.
- **Complex foreground graphics that are rarely edited**: use SVG modules for icons, technical symbols, decorative marks, and complex illustrations.
- **Editable data visuals**: use native PowerPoint charts/tables when values or labels may change.
- **Visual-only drafts**: use full-slide PNG only for fast previews, never as the final editable deliverable unless the user explicitly accepts non-editability.

For this user, the default best balance is: **PNG background + PowerPoint-native text/layout + SVG icons or complex decorative modules**.

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

2. **Inspect the source**
   - Open or parse the deck when possible.
   - Identify background elements versus foreground content.
   - Check existing scripts, assets, fonts, and prior output files.
   - Avoid hard-coded dependency paths unless already verified in the current environment.

3. **Choose object-level implementation**
   - Background: image layer.
   - Page title, core message, bullets, labels: native text boxes.
   - Cards, grids, timeline lines, arrows, badges: native shapes.
   - Icons and complex but stable drawings: SVG modules.
   - Charts/tables expected to be edited: native chart/table objects.

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

6. **Report clearly**
   - Provide the output file path.
   - State whether the result is editable and what kind of editability it has.
   - State how editability was verified, including object counts or media checks when relevant.
   - Mention any remaining manual review point.

## Quality Preferences

- Use restrained professional report styling, especially for enterprise or industrial topics.
- Prefer light backgrounds and blue accents unless the source design requires otherwise.
- Avoid heavy shadows, crowded cards, gratuitous gradients, and marketing-page composition.
- Preserve user-requested structure and background; do not restyle unrelated pages during a narrow conversion.
- Make slide text short enough to fit and support it with speaker notes or source narrative when available.

## Reference

For reusable Chinese prompt templates and phase-by-phase wording, read `references/prompt-templates.md` when the user asks for a prompt, reusable workflow, or a reminder of the preferred PPT production process.
