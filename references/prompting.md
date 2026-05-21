# Prompting and Deck Construction Guidance

Use this reference when a task needs prompt shaping, visual direction, content condensation, or formal-report style decisions.

## Prompt Contract

For deck work, structure the working spec in this order:

```text
Task slug: <create-formal-deck | manuscript-to-deck | rebuild-existing-slides | ...>
Input roles: <source deck, manuscript, data source, style reference, ...>
Audience and setting: <defense, technical review, internal report, training, ...>
Primary goal: <what the deck must communicate>
Visual system: <preserve source, direct background, style reference, generated background, deterministic background>
Editability contract: <native text/shapes/charts; stable SVG/images; explicitly accepted low-editability items>
Output artifacts: <pptx, previews, contact sheet, SVG sources, notes>
Validation: <PowerPoint export, LibreOffice fallback, package inspection, object counts>
Constraints: <must keep, must avoid, brand rules, fonts, language>
```

Keep the spec short. Add only details that materially improve the deck.

## Content Condensation

- Preserve source meaning, terminology, and evidence.
- Convert prose into slide claims, short bullets, tables, timelines, process diagrams, or comparison cards.
- Put supporting explanation in speaker notes when requested or useful.
- Do not invent metrics, organizations, claims, or conclusions.
- Do not overfit a manuscript into dense paragraphs. Formal report slides need readable structure, not transcript replicas.

## Formal Report Style

Use restrained, information-first styling:

- light canvas, blue or blue-gray accents, and modest contrast;
- consistent header/footer/page markers;
- technical cues such as grids, line drawings, process geometry, data textures, or equipment traces;
- clean content zones for dense text, diagrams, charts, and tables;
- small but legible typography, with clear hierarchy and stable spacing.

Avoid:

- marketing hero layouts;
- oversized decorative cards;
- heavy shadows and glossy gradients;
- ornate event-poster composition;
- backgrounds that cross reading zones;
- one-note palettes that make every element a variation of the same hue.

## Editability Invariants

Repeat these invariants in generation or revision prompts when editability matters:

- Keep titles, key claims, labels, page numbers, table text, chart labels, and conclusions as PowerPoint-native text.
- Build cards, dividers, process lines, arrows, timelines, and badges as native shapes.
- Use SVG only for stable symbols, technical motifs, icon modules, or decorative line art.
- Do not flatten the slide foreground into one picture.
- Do not put required slide-specific content into the background image.

## Chinese Deck Handling

- Prefer `Microsoft YaHei` for Chinese text unless the source deck requires another available font.
- Check exported previews for garbled text, overflow, cramped line spacing, and text that becomes too small.
- Keep slide titles compact and body bullets short.
- Avoid mixing too many Chinese font families in one deck.

## Background Prompting

When a raster background asset is needed, use the `imagegen` skill and keep the prompt background-only:

```text
Use case: productivity-visual
Asset type: 16:9 formal report PPT master background
Primary request: create a restrained academic/industrial report background
Scene/backdrop: light technical canvas with subtle domain cues and clean reading zones
Composition/framing: 16:9 slide background, stronger detail near edges/header/footer, empty body zones
Style/medium: polished formal report background, not a marketing hero image
Constraints: no slide-specific claims, no dense text, no logos unless provided, no foreground labels, no watermark
Avoid: text crossing body zones, heavy shadows, saturated gradients, decorative clutter
```

After generating or selecting the asset, run Gate 1 before using it across the deck unless the user explicitly skipped confirmations.
