# kd7dgf-OpenGD77-codeplug

**Multi-radio DMR codeplug generator for Western Washington/Oregon**

Generate customized DMR codeplugs for three radio variants from a variety of online sources using
[dzcb (DMR Zone Channel Builder)](https://github.com/mycodeplug/dzcb).

This project extends the upstream [example-codeplug](https://github.com/mycodeplug/example-codeplug) to support simultaneous generation of multiple radio formats with radio-specific optimizations.

## Supported Radios

This project generates codeplugs for three radio variants:

### AT-D578UV_III_Plus
- **Output Format**: Anytone CPS (Windows-only import)
- **CPS Version**: 1.11
- **Features**: Analog, Digital DMR repeaters, GMRS, simplex
- **Status**: ✅ Fully supported (CPS import only, dmrconfig not supported upstream)

### AT-D878UV_II_Plus
- **Output Formats**: Anytone CPS + dmrconfig
- **CPS Version**: 1.21 (Anytone), OpenRTX (dmrconfig)
- **Features**: Analog, Digital DMR repeaters, GMRS, simplex, advanced features
- **Status**: ✅ Fully supported (dual-format output)

### OpenGD77
- **Output Formats**: dmrconfig (recommended) + GB3GF CSV (experimental)
- **Import Tools**: 
  - [dmrconfig](https://github.com/OpenRTX/dmrconfig) (Linux/Mac, fully supported)
  - GB3GF CSV: ⚠️ **Currently incompatible** - Format mismatch with OpenGD77's native CSV import. See [PR #93](https://github.com/mycodeplug/dzcb/pull/93) for upstream fix in progress.
- **Features**: Analog, Digital DMR repeaters, GMRS, simplex, GPS coordinates (in progress)
- **Status**: ✅ dmrconfig fully supported | ⏳ GB3GF CSV format pending upstream fix

## Data Sources

**Active Sources:**
- **PNWDigital**: Live repeater network (https://pnwdigital.net)
- **SeattleDMR**: Live repeater network (https://seattledmr.org)
- **Local K7ABD Files**: Manual zone/channel definitions

**Disabled Sources:**
- **Repeaterbook Proximity**: Disabled due to upstream issue with CSV header generation (see Known Issues)

## Editing

Create / edit codeplug source files under [`/input`](/input).

This project uses **multiple subdirectories** under `/input` to generate **simultaneous codeplugs for three radios**:
- `input/AT-D578UV_III_Plus/` → Anytone CPS format only
- `input/AT-D878UV_II_Plus/` → Anytone CPS + dmrconfig formats
- `input/OpenGD77/` → dmrconfig + GB3GF formats

Each subdirectory contains:
- [`generate.py`](./input/AT-D878UV_II_Plus/generate.py): Python script that builds the codeplug using dzcb API
- [`k7abd/`](./input/AT-D878UV_II_Plus/k7abd/): Zone/channel definitions in K7ABD CSV format
- [`order.csv`](./input/AT-D878UV_II_Plus/order.csv): Preferred zone/channel/contact order
- [`exclude.csv`](./input/AT-D878UV_II_Plus/exclude.csv): Zone/channel/contact exclusions
- [`replacements.csv`](./input/AT-D878UV_II_Plus/replacements.csv): Object name replacements (regex)
- [`scanlists.json`](./input/AT-D878UV_II_Plus/scanlists.json): Additional scanlists
- Radio-specific config template (e.g., `d878uv-default.conf` for dmrconfig)

### See [dzcb README.md](https://github.com/mycodeplug/dzcb#dzcb) for more information on input file formats.

## Generating

### Local Build

```bash
# Install dependencies
pip install tox

# Build all three radio variants
tox

# Or run directly
python3 input/generate_all.py
```

Generated codepl ugs will be in `OUTPUT/` subdirectories organized by radio:
- `OUTPUT/AT-D578UV_III_Plus/anytone/` → Anytone CPS files
- `OUTPUT/AT-D878UV_II_Plus/anytone/` → Anytone CPS files
- `OUTPUT/AT-D878UV_II_Plus/dmrconfig/` → dmrconfig .conf file
- `OUTPUT/OpenGD77/dmrconfig/` → dmrconfig .conf file
- `OUTPUT/OpenGD77/gb3gf/` → GB3GF CSV files

### GitHub Actions

* [Fork this repo](../../fork)
  * In the newly forked repo, click the ["Actions" tab](../../actions) and
    enable Github Actions for your fork.
* Customize codeplug input files in [`/input`](./input/) for each radio variant:
  * Update zone/channel definitions in `k7abd/` subdirectories
  * Adjust `order.csv`, `exclude.csv`, `replacements.csv` as needed
  * Modify radio-specific config templates (`.conf` or `.json` files) with your Radio ID/Name
  * Update `scanlists.json` for custom scan lists
* Github [`codeplugs` workflow](.github/workflows/codeplugs.yml)
  will automatically build all three radio codepl ugs when you push to main
* When a [Release](../../releases) is published, the generated
  codepl ugs will be hosted publicly with stable URLs

### Requirements (Local Build)

* Linux, macOS, or Windows
* Python 3.8 or later
* [tox](https://tox.readthedocs.io/en/latest/)

See [dzcb WALKTHROUGH](https://github.com/mycodeplug/dzcb/blob/main/doc/WALKTHROUGH.md) for step-by-step instructions.

## Known Issues

### Repeaterbook Proximity (Re-enabled)

Previously, the upstream dzcb 0.3.10 had a bug where Analog CSV files generated from Repeaterbook proximity searches were missing the required "Zone" column header, causing `KeyError: 'Zone'` during parsing.

**Status**: ✅ **Fixed** - The root cause was UTF-8 Byte Order Mark (BOM) in K7ABD CSV files. After removing the BOM, repeaterbook proximity has been re-enabled.

**Current Configuration**: All three radios now include repeaterbook data from Washington and Oregon within 50-mile radius of defined proximity points (Seattle, Tacoma).

### OpenGD77 GB3GF CSV Format

OpenGD77 now has native CSV import support built into the CPS, but the current dzcb GB3GF output format is **incompatible** with OpenGD77's import expectations.

**Status**: A fix for the CSV format and GPS coordinate support is in progress at [PR #93](https://github.com/mycodeplug/dzcb/pull/93).

**Workarounds**: 
1. Use the **dmrconfig output** for OpenGD77 on Linux/Mac (fully supported, recommended)
2. Copy/paste rows from the GB3GF CSV files directly into OpenGD77 CPS as a manual workaround until the format is fixed

### AT-D578UV dmrconfig Support

The upstream dmrconfig tool doesn't recognize the AT-D578UV radio model.

**Workaround**: AT-D578UV codepl ugs are generated in Anytone CPS format only. Import through Windows CPS software.

## Best Practices

### Editing CSV Files

⚠️ **Important**: Always use **UTF-8 encoding WITHOUT BOM** when saving CSV files:

- **VS Code**: File → Save with Encoding → UTF-8
- **Excel**: Save As → CSV UTF-8
- **LibreOffice**: Tools → Options → Load/Save → Default file format

Editors like Notepad++ and Sublime Text add a UTF-8 BOM by default, which breaks dzcb's CSV parsing.

### Zone and Channel Naming

- Zone names **must be unique** across all CSV files
- Channel names **can be identical** in different zones
- Keep names under 20 characters for compatibility with all radio models

### Testing

Before pushing to production:

```bash
# Build locally
python3 input/generate_all.py

# Check for errors in logs
tail -20 OUTPUT/*/dzcb.*.log

# Verify all three radios produced output
ls OUTPUT/AT-D578UV_III_Plus/anytone/
ls OUTPUT/AT-D878UV_II_Plus/anytone/
ls OUTPUT/AT-D878UV_II_Plus/dmrconfig/
ls OUTPUT/OpenGD77/dmrconfig/
ls OUTPUT/OpenGD77/gb3gf/
```

Then import into CPS/dmrconfig or GB3GF tool to validate.

### Manual

#### Requirements

* linux, macOS, windows
* python 3.6+ (python 3.8 recommended)
* [tox](https://tox.readthedocs.io/en/latest/)

#### Build

To output to a specific directory, set the `OUTPUT` environment variable.

```
pip install tox
tox
```

To run the `generate.sh` shell scripts

```
tox -e shell
```
