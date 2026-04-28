#!/usr/bin/env python3
"""
Post-process VCarve G-code for Laguna IQ Turner rotary output.

Modes:
- minimal: Replace Y axis words with A axis words on motion lines.
- proposed: minimal mode plus a few header/comment normalizations that
  mirror intent from the proposed .pp file.
"""

from __future__ import annotations

import argparse
import difflib
import pathlib
import re
import sys
from dataclasses import dataclass


MOTION_CODE_RE = re.compile(r"\bG(?:0|00|1|01|2|02|3|03)\b", re.IGNORECASE)
AXIS_Y_WORD_RE = re.compile(r"(?<![A-Z0-9_])Y(?=[+\-]?(?:\d|\.\d))", re.IGNORECASE)


@dataclass
class TransformResult:
    lines: list[str]
    changed_count: int


def split_code_and_comment(line: str) -> tuple[str, str]:
    """
    Split into (code, comment) at the first true comment marker.
    Supports ';' comments and full parenthesis comments.
    """
    semicolon_idx = line.find(";")
    paren_idx = line.find("(")

    # If line starts with '(', treat whole line as comment.
    if line.lstrip().startswith("("):
        return "", line

    indices = [i for i in (semicolon_idx, paren_idx) if i >= 0]
    if not indices:
        return line, ""
    split_idx = min(indices)
    return line[:split_idx], line[split_idx:]


def transform_motion_code(code: str) -> str:
    if not MOTION_CODE_RE.search(code):
        return code
    return AXIS_Y_WORD_RE.sub("A", code)


def transform_comment_for_proposed(comment: str) -> str:
    comment = comment.replace(
        "X Values are wrapped around the Y axis",
        "Y axis wrapped around cylinder - output as A",
    )
    comment = comment.replace(
        "X Values are output as X",
        "Rotary axis along X",
    )
    return comment


def transform_line(line: str, mode: str) -> str:
    code, comment = split_code_and_comment(line)
    code_out = transform_motion_code(code)

    if mode == "proposed":
        comment = transform_comment_for_proposed(comment)

    return f"{code_out}{comment}"


def transform_lines(lines: list[str], mode: str) -> TransformResult:
    out: list[str] = []
    changed = 0
    for line in lines:
        updated = transform_line(line, mode)
        if updated != line:
            changed += 1
        out.append(updated)
    return TransformResult(lines=out, changed_count=changed)


def make_default_output_path(input_path: pathlib.Path, mode: str) -> pathlib.Path:
    return input_path.with_name(f"{input_path.stem}_{mode}_converted{input_path.suffix}")


def print_unified_diff(before: list[str], after: list[str], src: str, dst: str) -> None:
    diff_lines = difflib.unified_diff(
        before,
        after,
        fromfile=src,
        tofile=dst,
        lineterm="",
    )
    for line in diff_lines:
        print(line)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Post-process VCarve G-code for Laguna IQ Turner rotary output."
    )
    parser.add_argument("input", type=pathlib.Path, help="Input G-code file path")
    parser.add_argument(
        "-o",
        "--output",
        type=pathlib.Path,
        default=None,
        help="Output path (default: <input>_<mode>_converted.<ext>)",
    )
    parser.add_argument(
        "--mode",
        choices=("minimal", "proposed"),
        default="minimal",
        help="Transformation mode (default: minimal)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write output file; print summary (and optional diff).",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="Print unified diff of proposed changes.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    input_path: pathlib.Path = args.input
    if not input_path.exists() or not input_path.is_file():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        return 1

    output_path: pathlib.Path = args.output or make_default_output_path(input_path, args.mode)

    original_text = input_path.read_text(encoding="utf-8", errors="replace")
    original_lines = original_text.splitlines(keepends=True)

    result = transform_lines(original_lines, args.mode)
    transformed_text = "".join(result.lines)

    if args.diff:
        print_unified_diff(
            before=original_lines,
            after=result.lines,
            src=str(input_path),
            dst=str(output_path),
        )

    if args.dry_run:
        print(f"Mode: {args.mode}")
        print(f"Input: {input_path}")
        print(f"Output (not written): {output_path}")
        print(f"Changed lines: {result.changed_count}")
        return 0

    output_path.write_text(transformed_text, encoding="utf-8")
    print(f"Wrote: {output_path}")
    print(f"Changed lines: {result.changed_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
