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
    # 1. planx_mpyy_studio
    "planx_mpyy_studio": "planx_mpyy_studio/icons/icon.png",
    "planx-mpyy-studio": "planx_mpyy_studio/icons/icon.png",
    # 2. EasyFillet
    "easyfillet": "EasyFillet/icons/icon.png",
    # 3. osm_3d_model
    "osm_3d_model": "osm_3d_model/icons/icon.png",
    "osm-3d-model": "osm_3d_model/icons/icon.png",
    # 4. osm_quick_3d
    "osm_quick_3d": "osm_quick_3d/icons/icon.png",
    "osm-quick-3d": "osm_quick_3d/icons/icon.png",
    # 5. parametric_process
    "parametric_process": "parametric_process/icons/icon.png",
    "parametric-process": "parametric_process/icons/icon.png",
    # 6. parcelflux
    "parcelflux": "parcelflux/icons/icon.png",
    # 7. planx
    "planx": "planx/icons/icon.png",
    # 8. planx_3d_city
    "planx_3d_city": "planx_3d_city/icons/icon.png",
    "planx-3d-city": "planx_3d_city/icons/icon.png",
    # 9. planX_CAD_arac_Seti
    "planx-cad": "planX_CAD_arac_Seti/icons/icon.png",
    "planx_cad_arac_seti": "planX_CAD_arac_Seti/icons/icon.png",
    "planx_cad": "planX_CAD_arac_Seti/icons/icon.png",
    # 10. planx_datacube
    "planx_datacube": "planx_datacube/icons/icon.png",
    "planx-datacube": "planx_datacube/icons/icon.png",
    # 11. planx_geostats
    "planx_geostats": "planx_geostats/icons/icon.png",
    "planx-geostats": "planx_geostats/icons/icon.png",
    # 12. zero2smartmodeler
    "planx-smartmodeler": "zero2smartmodeler/icons/icon.png",
    "02agent-smart-modeler": "zero2smartmodeler/icons/icon.png",
    "zero2agent-smartmodeler": "zero2smartmodeler/icons/icon.png",
    "zero2smartmodeler": "zero2smartmodeler/icons/icon.png",
    "zero2smartmodeler_icon": "zero2smartmodeler/icons/icon.png",
    # 13. planx_suitability_lab
    "planx_suitability_lab": "planx_suitability_lab/icons/icon.png",
    "planx-suitability-lab": "planx_suitability_lab/icons/icon.png",
    # 14. planx_uip_arac_seti
    "planx-uip": "planx_uip_arac_seti/icon.svg",
    "planx_uip_arac_seti": "planx_uip_arac_seti/icon.svg",
    # 15. planx_urban_procedural_3d
    "planx_urban_procedural_3d": "planx_urban_procedural_3d/icons/icon.png",
    "planx-urban-procedural-3d": "planx_urban_procedural_3d/icons/icon.png",
    # 16. planx_urban_resilience
    "planx_urban_resilience": "planx_urban_resilience/icons/icon.png",
    "planx-urban-resilience": "planx_urban_resilience/icons/icon.png",
    # 17. planx_yerlesim_plani_arac_seti
    "planx-settlement": "planx_yerlesim_plani_arac_seti/icons/icon_main.svg",
    "planx_yerlesim_plani_arac_seti": "planx_yerlesim_plani_arac_seti/icons/icon_main.svg",
    # 18. zero2agent_osm_downloader
    "02agent-osm-downloader": "zero2agent_osm_downloader/icons/icon.png",
    "zero2agent-osm-downloader": "zero2agent_osm_downloader/icons/icon.png",
    "zero2agent_osm_downloader": "zero2agent_osm_downloader/icons/icon.png",
    # 19. zero2cadgis
    "zero2cadgis": "zero2cadgis/icons/icon.png",
    # 20. zero2cartolab
    "planx_cartolab": "zero2cartolab/icons/icon.png",
    "zero2cartolab": "zero2cartolab/icons/icon.png",
    "02cartolab": "zero2cartolab/icons/icon.png",
    "02-cartolab": "zero2cartolab/icons/icon.png",
    # 21. zero2geoquest
    "zero2geoquest": "zero2geoquest/icons/icon.png",
    # 22. zero2multimap
    "zero2multimap": "zero2multimap/icons/icon.png",
    "02multimap": "zero2multimap/icons/icon.png",
    # 23. zero2truesize
    "zero2truesize": "zero2truesize/icons/icon.png",
    "02truesize": "zero2truesize/icons/icon.png",
    # 24. zero2urbanportrait
    "zero2urbanportrait": "zero2urbanportrait/icons/icon.png",
    # 25. zero2viz
    "zero2viz": "zero2viz/icons/icon.png",
    "02viz": "zero2viz/icons/icon.png",
    # 26. qgis_25d_styling
    "qgis_25d_styling": "qgis_25d_styling/icons/icon.png",
    "qgis-25d-styling": "qgis_25d_styling/icons/icon.png",
    # 27. zero2route3d
    "zero2route3d": "zero2route3d/icons/icon.png",
    "02route3d": "zero2route3d/icons/icon.png",
    "02route-3d": "zero2route3d/icons/icon.png",
    "02-route-3d": "zero2route3d/icons/icon.png",
    # 28. qgis_maptips
    "qgis_maptips": "qgis_maptips/icons/icon.png",
    "qgis-maptips": "qgis_maptips/icons/icon.png",
    # 29. pln3113_nip
    "pln3113_nip": "pln3113_nip/icons/icon.png",
    "pln3113-nip": "pln3113_nip/icons/icon.png",
    "tire_nip": "pln3113_nip/icons/icon.png",
    "tire-nip": "pln3113_nip/icons/icon.png",
    # 30. zero2geospatial3d
    "zero2geospatial3d": "zero2geospatial3d/icons/icon.png",
    "02geospatial3d": "zero2geospatial3d/icons/icon.png",
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
