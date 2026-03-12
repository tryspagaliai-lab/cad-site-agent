# Roman Gardens Example

This example runs the full CAD site agent pipeline on `roman_gardens_gapclosed.dxf`.

## Prerequisites

- Python 3.10 with all project deps installed (see root README)
- DXF source file at `E:\roman_gardens_gapclosed.dxf` (or update path in run.bat/run.sh)

## Run

**Windows:**
```
run.bat
```

**Linux/macOS:**
```
bash run.sh
```

## Expected Output

See `expected_output.md` for the pipeline summary statistics from a reference run.

## Output Files

| File | Description |
|------|-------------|
| `roman_gardens.dxf` | Routed non-region features (linework, markings, symbols, text) |
| `roman_gardens.hatches.dxf` | Closed-region HATCH entities |
| `roman_gardens.hatch_candidates.json` | Candidate metadata (confidence, material, etc.) |
| `roman_gardens.process.json` | Full pipeline summary |
