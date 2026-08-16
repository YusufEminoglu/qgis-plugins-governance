#!/usr/bin/env python3
"""Copy each plugin's main icon into assets/plugin_icons/, keyed by GitHub repo slug.

generate_dashboard.py resolves a plugin's icon at generation time by lowercasing its
`repository` URL's last path segment and looking for <slug>.png / <slug>.svg under
assets/plugin_icons/. Because the dashboard regenerates on GitHub's Ubuntu runner
(where only this repo is checked out — no sibling plugin dirs), the icons must live
*inside* this repo. This script refreshes them from the sibling plugin directories
in the local monorepo.

Run locally whenever a plugin icon changes:
    py -3 refresh_plugin_icons.py
"""
import shutil
import sys
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

# Scatter nodes render at ~24-28 px, so downscale PNGs to 64 px (retina-crisp) to keep
# the inlined HTML small — some plugin icons ship at 512 or 1024 px and would otherwise
# add megabytes. SVG icons are copied verbatim (vector, already tiny).
MAX_PX = 64

HERE = Path(__file__).resolve().parent
MONOREPO = HERE.parent
DEST = HERE / "assets" / "plugin_icons"

# live GitHub repo slug (lowercased) -> source icon path relative to the monorepo root.
# The slug is what `repository` in the QGIS plugin XML gives; SmartModeler's live repo is
# `planx-smartmodeler` while its monorepo dir is `zero2smartmodeler` — mapped explicitly.
ICONS = {
    "osm_3d_model": "osm_3d_model/icons/icon.png",
    "osm_quick_3d": "osm_quick_3d/icons/icon.png",
    "zero2cadgis": "zero2cadgis/icons/icon.png",
    "planx-cad": "planX_CAD_arac_Seti/icons/icon.png",
    "zero2viz": "zero2viz/icons/icon.png",
    "planx": "planx/icons/icon.png",
    "planx_3d_city": "planx_3d_city/icons/icon_main.svg",
    "zero2multimap": "zero2multimap/icons/icon.png",
    "easyfillet": "EasyFillet/icon.svg",
    "planx_geostats": "planx_geostats/icons/icon.png",
    "planx_urban_resilience": "planx_urban_resilience/icons/plugin.svg",
    "planx_cartolab": "planx_cartolab/icons/icon.png",
    "planx-settlement": "planx_yerlesim_plani_arac_seti/icons/icon_main.svg",
    "planx_suitability_lab": "planx_suitability_lab/icons/icon.png",
    "planx-uip": "planx_uip_arac_seti/icon.svg",
    "parcelflux": "parcelflux/icons/parcelflux.png",
    "planx_urban_procedural_3d": "planx_urban_procedural_3d/icons/icon.png",
    "planx_datacube": "planx_datacube/icons/icon.png",
    "zero2urbanportrait": "zero2urbanportrait/icons/icon.png",
    "zero2geoquest": "zero2geoquest/icons/icon.png",
    "zero2truesize": "zero2truesize/icons/icon.png",
    "02agent-osm-downloader": "zero2agent_osm_downloader/icons/icon.png",
    "parametric_process": "parametric_process/icons/icon.png",
    "planx-smartmodeler": "zero2smartmodeler/icons/icon.png",
}


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    ok = 0
    for slug, rel in ICONS.items():
        src = MONOREPO / rel
        if not src.exists():
            print(f"MISSING  {slug}: {src}")
            continue
        ext = src.suffix  # .png / .svg
        dst = DEST / (slug + ext)
        if ext == ".png":
            with Image.open(src) as im:
                im = im.convert("RGBA")
                im.thumbnail((MAX_PX, MAX_PX), Image.LANCZOS)
                im.save(dst, format="PNG", optimize=True)
        else:
            shutil.copyfile(src, dst)
        print(f"OK       {slug}{ext}  <-  {rel}  ({dst.stat().st_size} bytes)")
        ok += 1
    print(f"\n{ok}/{len(ICONS)} icons copied to {DEST}")
    return 0 if ok == len(ICONS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
