# VCarve G-code Post Fix Usage

This script post-processes VCarve output G-code so wrapped rotary motion can be output as `A` axis moves for the Laguna IQ Turner workflow.

## Script

- `Vcarve/vcarve_gcode_post_fix.py`

## Modes

- `minimal`
  - Converts `Y` axis words to `A` axis words on motion lines (`G0/G1/G2/G3`).
  - Leaves comments unchanged.
- `proposed`
  - Includes all `minimal` behavior.
  - Also normalizes specific header/comment text based on your proposed `.pp` intent.

## Recommended Workflow

1. Post from VCarve using your currently working post processor.
2. Run a dry-run diff in both modes.
3. Choose the mode that best matches your machine/controller expectation.
4. Run again without `--dry-run` to write the converted file.

## Command Examples

Preview only, no output file written:

```bash
python3 "Vcarve/vcarve_gcode_post_fix.py" "path/to/input.nc" --mode minimal --dry-run --diff
python3 "Vcarve/vcarve_gcode_post_fix.py" "path/to/input.nc" --mode proposed --dry-run --diff
```

Write converted file (auto-named):

```bash
python3 "Vcarve/vcarve_gcode_post_fix.py" "path/to/input.nc" --mode proposed
```

Write converted file to a specific path:

```bash
python3 "Vcarve/vcarve_gcode_post_fix.py" "path/to/input.nc" --mode proposed --output "path/to/output_converted.nc"
```

## Output Naming

- Default output name: `<input_stem>_<mode>_converted<input_suffix>`
- Example:
  - input: `job.nc`
  - mode: `proposed`
  - output: `job_proposed_converted.nc`

## Notes

- Input file is never modified unless you deliberately set output to the same path.
- The script rewrites code tokens, not full-line free text, to reduce accidental edits in comments or metadata.
