# Copilot Instructions for kd7dgf-OpenGD77-codeplug

## Project Overview

This is a **multi-radio DMR codeplug generator** based on the upstream [dzcb](https://github.com/mycodeplug/dzcb) (DMR Zone Channel Builder) project. It generates customized radio programming files for three Anytone/OpenGD77 radio variants from multiple data sources.

- **Upstream Project**: https://github.com/mycodeplug/dzcb
- **Example Project**: https://github.com/mycodeplug/example-codeplug
- **Technology**: Python 3.8+, dzcb ~0.3.9, GitHub Actions
- **Purpose**: Build ham radio DMR codeplugs for Western Washington/Oregon area

## Project Architecture

```
kd7dgf-OpenGD77-codeplug/
├── README.md                           # Main documentation
├── .github/
│   ├── copilot-instructions.md        # This file
│   └── workflows/
│       └── codeplugs.yml              # GitHub Actions build workflow
├── input/                              # Radio variant subdirectories
│   ├── AT-D578UV_III_Plus/            # Anytone 578 (CPS 1.11) - Anytone output only
│   │   ├── generate.py                # Python codeplug generator
│   │   ├── d578uv-default.conf        # CPS template (for reference)
│   │   ├── k7abd/                     # Zone/Channel definitions (K7ABD format)
│   │   ├── exclude.csv                # Channels/zones to exclude
│   │   ├── order.csv                  # Channel/zone ordering
│   │   ├── replacements.csv           # Name replacements (regex)
│   │   ├── scanlists.json             # Custom scanlists
│   │   └── prox.csv                   # Repeaterbook proximity search (disabled)
│   ├── AT-D878UV_II_Plus/             # Anytone 878 (CPS 1.21) - Anytone + dmrconfig
│   │   ├── generate.py                # Python codeplug generator
│   │   ├── d878uv-default.conf        # dmrconfig template
│   │   ├── k7abd/                     # Zone/Channel definitions (K7ABD format)
│   │   ├── exclude.csv                # Channels/zones to exclude
│   │   ├── order.csv                  # Channel/zone ordering
│   │   ├── replacements.csv           # Name replacements (regex)
│   │   ├── scanlists.json             # Custom scanlists
│   │   └── prox.csv                   # Repeaterbook proximity search (disabled)
│   └── OpenGD77/                      # OpenGD77 radio - Farnsworth (editcp) output
│       ├── generate.py                # Python codeplug generator
│       ├── gd77-default.conf          # dmrconfig template (reference only)
│       ├── k7abd/                     # Zone/Channel definitions (K7ABD format)
│       ├── exclude.csv                # Channels/zones to exclude
│       ├── order.csv                  # Channel/zone ordering
│       ├── replacements.csv           # Name replacements (regex)
│       ├── scanlists.json             # Custom scanlists
│       └── prox.csv                   # Repeaterbook proximity search (disabled)
├── OUTPUT/                             # Build output (generated)
│   ├── AT-D578UV_III_Plus/
│   │   └── anytone/                   # Anytone CPS CSV files
│   ├── AT-D878UV_II_Plus/
│   │   ├── anytone/                   # Anytone CPS CSV files
│   │   └── dmrconfig/                 # dmrconfig .conf files
│   └── OpenGD77/
│       └── editcp/                    # Farnsworth JSON files
└── tox.ini                             # Test/build configuration
```

## Core Concepts

### Data Flow

```
dzcb.CodeplugRecipe() 
  ├── Input Sources:
  │   ├── Local K7ABD CSV files (zones, channels, talkgroups)
  │   ├── PNWDigital network (live repeater data)
  │   ├── SeattleDMR network (live repeater data)
  │   └── Repeaterbook Proximity (disabled - see Known Issues)
  │
  ├── Processing:
  │   ├── Merge zones from all sources
  │   ├── Apply exclude.csv filters
  │   ├── Apply order.csv sorting
  │   ├── Apply replacements.csv (regex name transforms)
  │   └── Apply scanlists.json customizations
  │
  └── Output Formats:
      ├── Anytone CPS (CSV files for Windows CPS software)
      ├── dmrconfig (OpenRTX format for AT-D878UV)
      └── Farnsworth/editcp (JSON for editcp tool - OpenGD77)
```

### K7ABD Format

The input CSV files follow the **K7ABD format** (named after the original anytone-config-builder):

- **Analog__ZoneName.csv**: Analog channels (GMRS, simplex, business, etc)
  - Columns: Zone, Channel Name, Bandwidth, Power, RX Freq, TX Freq, CTCSS Decode, CTCSS Encode, TX Prohibit
  - Example: `Analog__GMRS_FRS_Channels.csv`, `Analog__Ham_Simplex_Channels.csv`

- **Digital-Repeaters__ZoneName.csv**: Digital repeaters with static talkgroup assignments
  - Format: Zone Name, Comment, Power, RX Freq, TX Freq, Color Code, talkgroup1, talkgroup2, ...

- **Talkgroups__ZoneName.csv**: DMR talkgroup definitions
  - No header row
  - Format: talkgroup_name,talkgroup_number (suffix with "P" for private calls)

## Customizations from Upstream

### Multi-Radio Support

**Upstream**: example-codeplug uses a single `default/` directory for one codeplug variant.

**Customization**: We generate multiple radio variants simultaneously:
- `input/AT-D578UV_III_Plus/` → Anytone CPS format only
- `input/AT-D878UV_II_Plus/` → Anytone CPS + dmrconfig formats
- `input/OpenGD77/` → Farnsworth/editcp format

Each `generate.py` in each subdirectory is independently executed by `input/generate_all.py`.

### Output Format Selection

**Customization**: Different radios output different formats:
- AT-D578UV: `output_anytone=True`, `output_dmrconfig=False` (not supported upstream)
- AT-D878UV: `output_anytone=True`, `output_dmrconfig=True` (fully supported)
- OpenGD77: `output_farnsworth=True`, `output_anytone=False`

### Repeaterbook Proximity (Disabled)

**Upstream**: dzcb supports `--repeaterbook-proximity-csv` for live repeater data within distance of points of interest.

**Issue**: dzcb 0.3.10 has a bug where `zones_to_k7abd()` generates Analog CSV files without proper Zone column headers, causing `KeyError: 'Zone'`.

**Customization**: Set `source_repeaterbook_proximity=None` in all `generate.py` files to disable this feature until upstream fixes the issue.

**Impact**: Users still get PNWDigital and SeattleDMR live data; repeaterbook proximity-based dynamic zones are unavailable.

## Development Workflow

### Local Build

```bash
# Install dependencies
pip install tox

# Build all three radio variants
tox

# Or manually:
python3 input/generate_all.py
```

**Output**: `OUTPUT/{AT-D578UV_III_Plus,AT-D878UV_II_Plus,OpenGD77}/`

### GitHub Actions

**Workflow**: `.github/workflows/codeplugs.yml`
- Triggered on: every push to main, and on manual workflow_dispatch
- Runs: Python 3.8, tox, dzcb ~0.3.9
- Outputs: Artifacts in GitHub Actions

### Adding a New Radio Variant

1. Create `input/NewRadio/` directory
2. Copy configuration files from an existing variant
3. Create `input/NewRadio/generate.py` with appropriate `CodeplugRecipe()` parameters
4. Add radio-specific k7abd CSV files to `input/NewRadio/k7abd/`
5. Update README.md to document the new variant

## Configuration File Reference

### generate.py (CodeplugRecipe Parameters)

```python
CodeplugRecipe(
    # Data Sources (live or local)
    source_pnwdigital=True,              # Include live PNWDigital repeaters
    source_seattledmr=True,              # Include live SeattleDMR repeaters
    source_default_k7abd=False,          # Include dzcb default simplex/unlicensed
    source_k7abd=[(cp_dir / "k7abd")],   # Local K7ABD CSV files
    source_repeaterbook_proximity=None,  # Disabled due to upstream bug
    
    # Repeaterbook Configuration (if re-enabling)
    repeaterbook_states=["washington", "oregon"],
    repeaterbook_name_format='{Callsign} {Nearest City} {Landmark}',
    
    # Customization Files
    scanlists_json=cp_dir / "scanlists.json",
    exclude=cp_dir / "exclude.csv",
    order=cp_dir / "order.csv",
    replacements=cp_dir / "replacements.csv",
    
    # Output Formats (radio-specific)
    output_anytone=True,                 # Generate Anytone CPS format
    output_dmrconfig=False,              # Generate dmrconfig format (radio-dependent)
    output_farnsworth=False,             # Generate Farnsworth/editcp JSON
    output_gb3gf=False                   # Generate GB3GF format
).generate(output / cp_dir.name)
```

### exclude.csv (Channel/Zone Exclusion)

Format: One column named "zone" and/or "channel"

```csv
zone,channel
Simplex Test,
,Test Channel Only
```

Excludes all channels in "Simplex Test" zone and "Test Channel Only" channel across all zones.

### order.csv (Channel/Zone Ordering)

Format: "zone,channel" columns (one entry per line)

```csv
zone,channel
Ham Repeaters,
Ham Simplex,2m Call
Analog Simplex,
```

Specifies the order zones/channels appear in the final codeplug.

### replacements.csv (Regex Name Transforms)

Format: "object_pattern,object_repl" columns

```csv
zone_pattern,zone_repl
channel_pattern,channel_repl
Channel Name (Test),Channel Name
```

Applied in order; later replacements can affect earlier ones.

### scanlists.json (Custom Scanlists)

Format: JSON dict mapping scanlist name to array of channel names

```json
{
  "Local Repeaters": ["PNWDigital 441.1", "SeattleDMR 441.1"],
  "Emergency Net": ["PNWDigital 6", "SeattleDMR 1"]
}
```

## K7ABD CSV Format Details

### Zone/Channel Name Uniqueness

⚠️ **CRITICAL**: Zone names must be globally unique across all CSV files, but **channel names CAN be identical in different zones**.

**Example (valid)**:
```
Analog__GMRS_FRS_Channels.csv: Zone="GMRS", Channel="Ch 01"
Analog__Ham_Simplex_Channels.csv: Zone="Ham Simplex", Channel="Ch 01"
```

### Avoiding UTF-8 BOM Issues

**Issue**: Some editors add a UTF-8 Byte Order Mark (BOM) at the start of files, causing dzcb to not recognize column headers.

**Solution**: Always save CSV files with UTF-8 encoding **without BOM**.

- **VS Code**: File → Save with Encoding → UTF-8 (NOT UTF-8 with BOM)
- **Excel**: Save As → CSV UTF-8 (uses correct encoding)
- **Command line**: `sed -i '1s/^\xEF\xBB\xBF//' filename.csv`

## Known Issues and Limitations

### 1. Repeaterbook Proximity Disabled

**Status**: ⚠️ Upstream bug

**Issue**: dzcb 0.3.10 `zones_to_k7abd()` generates Analog CSV files without Zone column headers.

**Symptoms**: `KeyError: 'Zone'` during codeplug generation

**Workaround**: Repeaterbook data disabled; use PNWDigital/SeattleDMR instead

**Resolution Path**: 
- Monitor dzcb releases for fix in >= 0.3.11
- Test and re-enable when upstream resolves

### 2. AT-D578UV dmrconfig Not Supported

**Status**: ℹ️ Upstream limitation

**Issue**: dmrconfig doesn't recognize Anytone AT-D578UV model

**Workaround**: Generates Anytone CPS format only (still functional)

**Resolution Path**: 
- File issue with OpenRTX/dmrconfig if AT-D578UV support is needed
- Until then, users must import via Anytone CPS software (Windows)

### 3. GitHub Actions Cache Key

**Current**: `dzcb-cache-YYYYMMDD-AM` (once per morning)

**Note**: Cache keys use UTC time zone; adjust if time-based keying causes issues

## Common Workflow Tasks

### Update Live Data Sources

Simply push to main—GitHub Actions fetches latest PNWDigital and SeattleDMR automatically.

```bash
git add .
git commit -m "Update custom channels"
git push origin main
```

### Add New Analog Channels

1. Create or edit `input/RadioVariant/k7abd/Analog__NewZone.csv`
2. Follow K7ABD format with headers and UTF-8 encoding (no BOM)
3. Update `input/RadioVariant/order.csv` if ordering matters
4. Commit and push

### Filter Out Problematic Channels

Edit `input/RadioVariant/exclude.csv`:

```csv
zone,channel
Problem Zone,
,Problematic Channel Name
```

### Change Channel Name Format

Use `input/RadioVariant/replacements.csv` with regex:

```csv
channel_pattern,channel_repl
^SeattleDMR (.*),$,SeattleDMR\1 (TG)
^PNWDigital (.*),$,PNW\1
```

## Testing and Validation

### Local Validation

```bash
# Build locally
python3 input/generate_all.py

# Verify output files
ls -lh OUTPUT/*/anytone/
ls -lh OUTPUT/*/dmrconfig/
ls -lh OUTPUT/*/editcp/
```

### GitHub Actions Validation

Check workflow runs: https://github.com/AlwaysLearningTech/kd7dgf-OpenGD77-codeplug/actions

**Success indicators**:
- ✅ All three `generate.py` files complete without errors
- ✅ Output artifacts created for each radio variant
- ✅ No `KeyError: 'Zone'` or encoding-related errors

### CPS Import Testing

Before using generated files:

1. **Anytone CPS**: Import CSV files through official CPS software
2. **dmrconfig**: Load .conf file and validate radio settings
3. **editcp**: Open JSON and verify zones/channels in GUI

## Upstream Methodology

### dzcb Design Philosophy

1. **Source Data Separation**: Zones/channels from multiple sources combined cleanly
2. **Format Agnostic**: Input once, output multiple radio formats
3. **Reproducible**: Same input always produces same output
4. **Extensible**: Python API allows custom processing before output

### Example Project Pattern

The upstream [example-codeplug](https://github.com/mycodeplug/example-codeplug) uses:

- Single `input/default/` directory with one `generate.py`
- Focuses on demonstrating dzcb capabilities
- Serves as template for users creating their own codeplugs

### Our Deviation

We extend this pattern to support:

- Multiple radio variants in parallel
- Different output formats per radio
- Persistent GitHub Actions workflow
- Western Washington/Oregon focus with local customizations

## Documentation

- **README.md**: User-facing build and customization guide
- **This file**: Copilot development guidelines and best practices
- **dzcb docs**: https://github.com/mycodeplug/dzcb (for format details)
- **WALKTHROUGH.md**: https://github.com/mycodeplug/dzcb/blob/main/doc/WALKTHROUGH.md (upstream guide)

## Best Practices

### Code Guidelines

- Use Python CodeplugRecipe API in `generate.py` (not bash scripts)
- Keep K7ABD CSV files in consistent naming: `Analog__ZoneName.csv`, `Digital-Repeaters__ZoneName.csv`
- Test locally with `python3 input/generate_all.py` before pushing
- Verify no UTF-8 BOM in CSV files: `file input/*/k7abd/*.csv`

### CSV Editing

- **Recommended editors**: VS Code, Excel, LibreOffice Calc
- **Avoid**: Notepad++, Sublime (often add BOM by default)
- **Always**: Specify UTF-8 without BOM in save dialogs

### Commit Messages

Follow standard format:

```
Short description (50 chars or less)

Detailed explanation if needed. Reference which radio(s) affected.

Examples:
- "Update W7ACS frequencies for AT-D878UV and AT-D578UV"
- "Fix UTF-8 BOM in W7ACS_20250917.csv"
- "Add new analog zone: Western Washington GMRS"
```

### Version Pinning

Current: `dzcb ~= 0.3.9` (allows 0.3.x updates, not 0.4+)

Update only after testing locally and on GitHub Actions. Check release notes at https://github.com/mycodeplug/dzcb/releases.

## Critical Files Reference

| File | Purpose | Radio(s) |
|------|---------|----------|
| `input/*/generate.py` | Codeplug generation script | All |
| `input/*/k7abd/*.csv` | Zone/channel definitions | All |
| `input/*/exclude.csv` | Channel/zone filters | All |
| `input/*/order.csv` | Channel/zone ordering | All |
| `input/*/replacements.csv` | Name replacements (regex) | All |
| `input/*/scanlists.json` | Custom scanlists | All |
| `input/AT-D878UV_II_Plus/d878uv-default.conf` | dmrconfig template | 878 only |
| `.github/workflows/codeplugs.yml` | GitHub Actions build | All |

## Quick Reference Commands

```bash
# Local build
python3 input/generate_all.py

# Verify CSV encoding (no BOM)
file input/*/k7abd/*.csv

# Find non-UTF8 files
find input -name "*.csv" -exec file {} \; | grep -v UTF-8

# Check git status before push
git status

# View GitHub Actions
git log --oneline | head -5
```

## When to Update Documentation

Update this file (`copilot-instructions.md`) when:
- Adding new radio variants
- Changing data sources or output formats
- Discovering new upstream issues
- Modifying build workflow

Update `README.md` when:
- Users need step-by-step customization instructions
- Adding new end-user features

---

**Questions?** Refer to upstream dzcb documentation: https://github.com/mycodeplug/dzcb
