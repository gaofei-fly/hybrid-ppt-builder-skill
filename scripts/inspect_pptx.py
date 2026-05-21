#!/usr/bin/env python3
"""Inspect a PPTX package for editable-layer evidence."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
}


def slide_sort_key(path: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", path)
    return int(match.group(1)) if match else 0


def text_content(root: ET.Element) -> list[str]:
    values: list[str] = []
    for node in root.findall(".//a:t", NS):
        if node.text and node.text.strip():
            values.append(node.text.strip())
    return values


def presentation_size(zf: zipfile.ZipFile) -> dict[str, int] | None:
    try:
        root = ET.fromstring(zf.read("ppt/presentation.xml"))
    except (KeyError, ET.ParseError):
        return None
    size = root.find(".//p:sldSz", NS)
    if size is None:
        return None
    return {
        "cx": int(size.attrib.get("cx", "0")),
        "cy": int(size.attrib.get("cy", "0")),
    }


def is_16_9_size(size: dict[str, int] | None) -> bool:
    if not size or not size["cx"] or not size["cy"]:
        return False
    return abs((size["cx"] / size["cy"]) - (16 / 9)) < 0.001


def inspect_slide(zf: zipfile.ZipFile, path: str) -> dict[str, object]:
    root = ET.fromstring(zf.read(path))
    texts = text_content(root)
    shapes = root.findall(".//p:sp", NS)
    pictures = root.findall(".//p:pic", NS)
    graphic_frames = root.findall(".//p:graphicFrame", NS)
    groups = root.findall(".//p:grpSp", NS)
    text_shapes = [
        shape for shape in shapes if shape.find(".//p:txBody", NS) is not None
    ]

    chart_frames = 0
    table_frames = 0
    for frame in graphic_frames:
        if frame.find(".//c:chart", NS) is not None:
            chart_frames += 1
        if frame.find(".//a:tbl", NS) is not None:
            table_frames += 1

    native_objects = len(shapes) + len(graphic_frames) + len(groups)
    warnings: list[str] = []
    if not texts:
        warnings.append("no native text found")
    if len(pictures) >= 2 and native_objects <= 3:
        warnings.append("possible flattened foreground: many pictures and few native objects")
    if native_objects <= 1 and len(pictures) >= 1:
        warnings.append("low editability evidence: picture-only or near picture-only slide")

    return {
        "slide": slide_sort_key(path),
        "path": path,
        "native_objects": native_objects,
        "shapes": len(shapes),
        "text_shapes": len(text_shapes),
        "pictures": len(pictures),
        "graphic_frames": len(graphic_frames),
        "groups": len(groups),
        "charts": chart_frames,
        "tables": table_frames,
        "native_text_runs": len(texts),
        "native_text_preview": " ".join(texts)[:240],
        "warnings": warnings,
    }


def inspect_pptx(path: Path) -> dict[str, object]:
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        slide_paths = sorted(
            [
                name
                for name in names
                if re.match(r"ppt/slides/slide\d+\.xml$", name)
            ],
            key=slide_sort_key,
        )
        slides = [inspect_slide(zf, slide_path) for slide_path in slide_paths]
        media = [name for name in names if name.startswith("ppt/media/")]
        embedded = [name for name in names if name.startswith("ppt/embeddings/")]
        size = presentation_size(zf)

    warnings = [
        f"slide {slide['slide']}: {warning}"
        for slide in slides
        for warning in slide["warnings"]
    ]
    return {
        "file": str(path),
        "slide_count": len(slides),
        "slide_size_emu": size,
        "is_16_9": is_16_9_size(size),
        "media_count": len(media),
        "embedded_count": len(embedded),
        "slides": slides,
        "warnings": warnings,
    }


def print_table(report: dict[str, object]) -> None:
    print(f"File: {report['file']}")
    print(f"Slides: {report['slide_count']}")
    print(f"16:9: {report['is_16_9']}")
    print(f"Media files: {report['media_count']}")
    print(f"Embedded files: {report['embedded_count']}")
    print()
    header = (
        "slide native_objects shapes text_shapes pictures "
        "graphic_frames charts tables native_text_runs warnings"
    )
    print(header)
    for slide in report["slides"]:
        print(
            f"{slide['slide']} "
            f"{slide['native_objects']} "
            f"{slide['shapes']} "
            f"{slide['text_shapes']} "
            f"{slide['pictures']} "
            f"{slide['graphic_frames']} "
            f"{slide['charts']} "
            f"{slide['tables']} "
            f"{slide['native_text_runs']} "
            f"{'; '.join(slide['warnings'])}"
        )
    if report["warnings"]:
        print()
        print("Warnings:")
        for warning in report["warnings"]:
            print(f"- {warning}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Inspect PPTX slides for native objects, pictures, media, and text."
    )
    parser.add_argument("pptx", type=Path, help="PPTX file to inspect")
    parser.add_argument("--json", action="store_true", help="print JSON report")
    parser.add_argument("--expect-slides", type=int, help="expected slide count")
    parser.add_argument(
        "--min-native-objects",
        type=int,
        default=0,
        help="fail if any slide has fewer native objects than this value",
    )
    parser.add_argument(
        "--require-native-text",
        action="store_true",
        help="fail if any slide has no native text runs",
    )
    parser.add_argument(
        "--fail-on-warning",
        action="store_true",
        help="return nonzero when heuristic warnings are present",
    )
    args = parser.parse_args(argv)

    if not args.pptx.exists():
        print(f"error: file not found: {args.pptx}", file=sys.stderr)
        return 2

    try:
        report = inspect_pptx(args.pptx)
    except zipfile.BadZipFile:
        print(f"error: not a valid zip/PPTX file: {args.pptx}", file=sys.stderr)
        return 2
    except ET.ParseError as exc:
        print(f"error: failed to parse PPTX XML: {exc}", file=sys.stderr)
        return 2

    failures: list[str] = []
    if args.expect_slides is not None and report["slide_count"] != args.expect_slides:
        failures.append(
            f"expected {args.expect_slides} slides, found {report['slide_count']}"
        )
    if args.min_native_objects:
        for slide in report["slides"]:
            if slide["native_objects"] < args.min_native_objects:
                failures.append(
                    f"slide {slide['slide']} has {slide['native_objects']} "
                    f"native objects, below {args.min_native_objects}"
                )
    if args.require_native_text:
        for slide in report["slides"]:
            if slide["native_text_runs"] == 0:
                failures.append(f"slide {slide['slide']} has no native text")
    if args.fail_on_warning:
        failures.extend(report["warnings"])

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_table(report)

    if failures:
        print()
        print("Failures:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
