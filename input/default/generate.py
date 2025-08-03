#!/usr/bin/env python3

# This generates the same codeplug as generate.sh
# using python code.

from pathlib import Path
import os

from dzcb.recipe import CodeplugRecipe
from datetime import datetime

# Get today's date in YYYY-MM-DD format
today_date = datetime.today().strftime('%Y-%m-%d')
cp_dir = today_date
output = Path(os.environ.get("OUTPUT") or (cp_dir / ".." / ".." / "OUTPUT"))

CodeplugRecipe(
    source_pnwdigital=True,
    source_seattledmr=True,
    source_default_k7abd=True,
    source_k7abd=[(cp_dir / "k7abd")],
    source_repeaterbook_proximity=cp_dir / "prox.csv",
    repeaterbook_states=["washington", "oregon"],
    repeaterbook_name_format='{Callsign} {Nearest City} {Landmark}',
    scanlists_json=cp_dir / "scanlists.json",
    exclude=cp_dir / "exclude.csv",
    order=cp_dir / "order.csv",
    replacements=cp_dir / "replacements.csv",
    output_anytone=False,
    output_dmrconfig=[(cp_dir / "gd77-default.conf")],
    output_farnsworth=False,
    output_gb3gf=True
).generate(output / cp_dir.name)
