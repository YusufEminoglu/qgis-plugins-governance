"""Geophilo QGIS plugin dashboard.

Downloads, releases and reach of the Geophilo plugins on the QGIS Plugin Hub,
built only from data the Hub publishes:

* plugins.xml            - every plugin's version, total downloads, dates, links
* plugins_history.json   - one snapshot per run (this script appends it), which
                           turns cumulative totals into downloads per day/week
* Hub Metabase (public)  - downloads per country, recorded since 2024-05-30

Nothing is estimated or simulated: a figure the Hub does not provide is shown
as unavailable. Plugins are identified by their Hub package name, which never
changes, so display-name changes do not break the history.
"""
from __future__ import annotations

import base64
import html
import json
import math
import os
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
HISTORY = os.path.join(HERE, "plugins_history.json")
GEOJSON = os.path.join(HERE, "world_map.geojson")
ICON_DIR = os.path.join(HERE, "assets", "plugin_icons")
PLUGINS_ROOT = os.path.abspath(os.path.join(HERE, ".."))
HUB_XML = "https://plugins.qgis.org/plugins/plugins.xml?qgis=4.0"
METABASE = ("https://plugins.qgis.org/metabase/api/public/dashboard/"
            "2c2d25b4-5288-43da-8247-8122a2395476/dashcard/28/card/26/json")
COUNTRY_SINCE = "2024-05-30"  # the Hub started recording downloads per country
AUTHORS = ("geophilo", "yusuf eminoglu", "yusuf eminoğlu")
NOW = datetime.now(timezone.utc)
TODAY = NOW.date()

# Hub display names used before the 2026-10 rename -> package name, so the
# snapshots taken under the old names join the same series.
LEGACY_NAMES = {
    "3D OSM Model": "osm_3d_model", "OSM Quick 3D": "osm_quick_3d",
    "02CadGis Universal CAD/GIS Importer": "zero2cadgis", "PlanX CAD Toolset": "planX_CAD_arac_Seti",
    "02viz - Geospatial Visualization Studio": "zero2viz", "PlanX": "planx",
    "PlanX 3D City Viewer": "planx_3d_city", "02-Multimap: Sync-up Multimaps": "zero2multimap",
    "EasyFillet": "EasyFillet", "PlanX GeoStats Lab": "planx_geostats",
    "PlanX: Urban Resilience": "planx_urban_resilience",
    "PlanX Settlement Planning Toolset": "planx_yerlesim_plani_arac_seti",
    "PlanX Suitability Lab": "planx_suitability_lab",
    "PlanX Uygulama İmar Planı (Master Plan) Toolset": "planx_uip_arac_seti",
    "ParcelFlux": "parcelflux", "PlanX Urban Procedural 3D": "planx_urban_procedural_3d",
    "PlanX DataCube Lab": "planx_datacube", "02Urban Portrait - City as a Face": "zero2urbanportrait",
    "02GeoQuest - Playable Map Studio": "zero2geoquest", "02truesize - Map Truth Lab": "zero2truesize",
    "02Agent OSM Downloader": "zero2agent_osm_downloader", "Parametric Process": "parametric_process",
    "02Agent Smart Modeler": "zero2smartmodeler", "02CartoLab": "zero2cartolab",
    "QGIS 2.5D Styling": "qgis_25d_styling",
    "02Route 3D - Multi-Criteria 3D Mobility Studio": "zero2route3d",
    "Qgis Advanced Map Tips&Actions": "qgis_maptips", "02 Geo3D Analyzer": "zero2geospatial3d",
    "PlanX MPYY Studio": "planx_mpyy_studio", "PLN3113 NİP ve Kentsel Analiz Stüdyosu": "pln3113_nip",
}

SUITES = (("planx", "PlanX suite"), ("zero2", "02 suite"), ("", "Standalone"))


def suite_of(package):
    p = package.lower()
    if p.startswith("planx"):
        return "PlanX suite"
    if p.startswith("zero2"):
        return "02 suite"
    return "Standalone"


def get(url, data=None, timeout=60, tries=3):
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers={
                "User-Agent": "Mozilla/5.0 (geophilo dashboard)",
                "Content-Type": "application/json"} if data else {"User-Agent": "Mozilla/5.0 (geophilo dashboard)"},
                method="POST" if data else "GET")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except Exception as exc:  # retried; the caller decides what a failure means
            last = exc
            time.sleep(2 * (attempt + 1))
    raise last


# --------------------------------------------------------------------------- Hub
def fetch_plugins():
    root = ET.fromstring(get(HUB_XML))
    plugins = []
    for el in root.findall("pyqgis_plugin"):
        author = (el.findtext("author_name") or "").strip()
        if not any(a in author.lower() for a in AUTHORS):
            continue
        url = el.findtext("download_url") or ""
        package = url.split("/plugins/")[1].split("/")[0] if "/plugins/" in url else el.attrib.get("name", "")
        plugins.append({
            "package": package,
            "name": el.attrib.get("name", package),
            "version": el.attrib.get("version", ""),
            "downloads": int(el.findtext("downloads") or 0),
            "created": (el.findtext("create_date") or "")[:10],
            "updated": (el.findtext("update_date") or "")[:10],
            "qgis_min": el.findtext("qgis_minimum_version") or "",
            "qgis_max": el.findtext("qgis_maximum_version") or "",
            "experimental": (el.findtext("experimental") or "").lower() in ("true", "yes", "1"),
            "homepage": el.findtext("homepage") or "",
            "repository": el.findtext("repository") or "",
            "suite": suite_of(package),
        })
    if not plugins:
        raise SystemExit("No Geophilo plugins in plugins.xml - refusing to publish an empty dashboard.")
    return sorted(plugins, key=lambda p: -p["downloads"])


# ----------------------------------------------------------------------- history
def load_history():
    if not os.path.exists(HISTORY):
        return []
    with open(HISTORY, encoding="utf-8") as fh:
        history = json.load(fh)
    for snap in history:  # re-key snapshots taken under old display names
        snap["plugins"] = {LEGACY_NAMES.get(k, k): v for k, v in snap.get("plugins", {}).items()}
    return history


def add_snapshot(history, plugins):
    snap = {
        "timestamp": NOW.isoformat(),
        "date_str": NOW.strftime("%b %d, %Y %H:%M UTC"),
        "total_downloads": sum(p["downloads"] for p in plugins),
        "plugins": {p["package"]: {"downloads": p["downloads"], "version": p["version"], "name": p["name"]}
                    for p in plugins},
    }
    if history and history[-1]["timestamp"][:10] == NOW.date().isoformat():
        history[-1] = snap  # one snapshot per day; the latest run of the day wins
    else:
        history.append(snap)
    with open(HISTORY, "w", encoding="utf-8") as fh:
        json.dump(history, fh, ensure_ascii=False, indent=1)
    return history


def daily_series(history, packages, days):
    """Cumulative downloads per package for each of the last `days` days (forward-filled).

    A day before the plugin's first snapshot is None."""
    by_day = {}
    for snap in history:
        d = datetime.fromisoformat(snap["timestamp"].replace("Z", "+00:00")).date()
        by_day[d] = snap["plugins"]  # last snapshot of the day wins
    start = TODAY - timedelta(days=days)
    ordered = sorted(by_day)
    out = {p: [] for p in packages}
    last = {p: None for p in packages}
    idx = 0
    for i in range(days + 1):
        d = start + timedelta(days=i)
        while idx < len(ordered) and ordered[idx] <= d:
            for p in packages:
                rec = by_day[ordered[idx]].get(p)
                if rec is not None:
                    last[p] = rec.get("downloads")
            idx += 1
        for p in packages:
            out[p].append(last[p])
    return [start + timedelta(days=i) for i in range(days + 1)], out


def increments(series):
    inc = []
    for a, b in zip(series, series[1:]):
        inc.append(max(0, b - a) if a is not None and b is not None else 0)
    return inc


def release_events(history, names):
    events, last = [], {}
    for snap in history:
        d = snap["timestamp"][:10]
        for pkg, rec in snap["plugins"].items():
            v = rec.get("version")
            if pkg in last and v and last[pkg] != v and pkg in names:
                events.append({"date": d, "package": pkg, "name": names[pkg], "from": last[pkg], "to": v})
            if v:
                last[pkg] = v
    return events


# --------------------------------------------------------------------- countries
ISO3_TO_ISO2 = {
    'ABW': 'AW', 'AFG': 'AF', 'AGO': 'AO', 'AIA': 'AI', 'ALA': 'AX', 'ALB': 'AL', 'AND': 'AD', 'ARE': 'AE',
    'ARG': 'AR', 'ARM': 'AM', 'ASM': 'AS', 'ATA': 'AQ', 'ATF': 'TF', 'ATG': 'AG', 'AUS': 'AU', 'AUT': 'AT',
    'AZE': 'AZ', 'BDI': 'BI', 'BEL': 'BE', 'BEN': 'BJ', 'BES': 'BQ', 'BFA': 'BF', 'BGD': 'BD', 'BGR': 'BG',
    'BHR': 'BH', 'BHS': 'BS', 'BIH': 'BA', 'BLM': 'BL', 'BLR': 'BY', 'BLZ': 'BZ', 'BMU': 'BM', 'BOL': 'BO',
    'BRA': 'BR', 'BRB': 'BB', 'BRN': 'BN', 'BTN': 'BT', 'BVT': 'BV', 'BWA': 'BW', 'CAF': 'CF', 'CAN': 'CA',
    'CCK': 'CC', 'CHE': 'CH', 'CHL': 'CL', 'CHN': 'CN', 'CIV': 'CI', 'CMR': 'CM', 'COD': 'CD', 'COG': 'CG',
    'COK': 'CK', 'COL': 'CO', 'COM': 'KM', 'CPV': 'CV', 'CRI': 'CR', 'CUB': 'CU', 'CUW': 'CW', 'CXR': 'CX',
    'CYM': 'KY', 'CYP': 'CY', 'CZE': 'CZ', 'DEU': 'DE', 'DJI': 'DJ', 'DMA': 'DM', 'DNK': 'DK', 'DOM': 'DO',
    'DZA': 'DZ', 'ECU': 'EC', 'EGY': 'EG', 'ERI': 'ER', 'ESH': 'EH', 'ESP': 'ES', 'EST': 'EE', 'ETH': 'ET',
    'FIN': 'FI', 'FJI': 'FJ', 'FLK': 'FK', 'FRA': 'FR', 'FRO': 'FO', 'FSM': 'FM', 'GAB': 'GA', 'GBR': 'GB',
    'GEO': 'GE', 'GGY': 'GG', 'GHA': 'GH', 'GIB': 'GI', 'GIN': 'GN', 'GLP': 'GP', 'GMB': 'GM', 'GNB': 'GW',
    'GNQ': 'GQ', 'GRC': 'GR', 'GRD': 'GD', 'GRL': 'GL', 'GTM': 'GT', 'GUF': 'GF', 'GUM': 'GU', 'GUY': 'GY',
    'HKG': 'HK', 'HMD': 'HM', 'HND': 'HN', 'HRV': 'HR', 'HTI': 'HT', 'HUN': 'HU', 'IDN': 'ID', 'IMN': 'IM',
    'IND': 'IN', 'IOT': 'IO', 'IRL': 'IE', 'IRN': 'IR', 'IRQ': 'IQ', 'ISL': 'IS', 'ISR': 'IL', 'ITA': 'IT',
    'JAM': 'JM', 'JEY': 'JE', 'JOR': 'JO', 'JPN': 'JP', 'KAZ': 'KZ', 'KEN': 'KE', 'KGZ': 'KG', 'KHM': 'KH',
    'KIR': 'KI', 'KNA': 'KN', 'KOR': 'KR', 'KWT': 'KW', 'LAO': 'LA', 'LBN': 'LB', 'LBR': 'LR', 'LBY': 'LY',
    'LCA': 'LC', 'LIE': 'LI', 'LKA': 'LK', 'LSO': 'LS', 'LTU': 'LT', 'LUX': 'LU', 'LVA': 'LV', 'MAC': 'MO',
    'MAF': 'MF', 'MAR': 'MA', 'MCO': 'MC', 'MDA': 'MD', 'MDG': 'MG', 'MDV': 'MV', 'MEX': 'MX', 'MHL': 'MH',
    'MKD': 'MK', 'MLI': 'ML', 'MLT': 'MT', 'MMR': 'MM', 'MNE': 'ME', 'MNG': 'MN', 'MNP': 'MP', 'MOZ': 'MZ',
    'MRT': 'MR', 'MSR': 'MS', 'MTQ': 'MQ', 'MUS': 'MU', 'MWI': 'MW', 'MYS': 'MY', 'MYT': 'YT', 'NAM': 'NA',
    'NCL': 'NC', 'NER': 'NE', 'NFK': 'NF', 'NGA': 'NG', 'NIC': 'NI', 'NIU': 'NU', 'NLD': 'NL', 'NOR': 'NO',
    'NPL': 'NP', 'NRU': 'NR', 'NZL': 'NZ', 'OMN': 'OM', 'PAK': 'PK', 'PAN': 'PA', 'PCN': 'PN', 'PER': 'PE',
    'PHL': 'PH', 'PLW': 'PW', 'PNG': 'PG', 'POL': 'PL', 'PRI': 'PR', 'PRK': 'KP', 'PRT': 'PT', 'PRY': 'PY',
    'PSE': 'PS', 'PYF': 'PF', 'QAT': 'QA', 'REU': 'RE', 'ROU': 'RO', 'RUS': 'RU', 'RWA': 'RW', 'SAU': 'SA',
    'SDN': 'SD', 'SEN': 'SN', 'SGP': 'SG', 'SGS': 'GS', 'SHN': 'SH', 'SJM': 'SJ', 'SLB': 'SB', 'SLE': 'SL',
    'SLV': 'SV', 'SMR': 'SM', 'SOM': 'SO', 'SPM': 'PM', 'SRB': 'RS', 'SSD': 'SS', 'STP': 'ST', 'SUR': 'SR',
    'SVK': 'SK', 'SVN': 'SI', 'SWE': 'SE', 'SWZ': 'SZ', 'SXM': 'SX', 'SYC': 'SC', 'SYR': 'SY', 'TCA': 'TC',
    'TCD': 'TD', 'TGO': 'TG', 'THA': 'TH', 'TJK': 'TJ', 'TKL': 'TK', 'TKM': 'TM', 'TLS': 'TL', 'TON': 'TO',
    'TTO': 'TT', 'TUN': 'TN', 'TUR': 'TR', 'TUV': 'TV', 'TWN': 'TW', 'TZA': 'TZ', 'UGA': 'UG', 'UKR': 'UA',
    'UMI': 'UM', 'URY': 'UY', 'USA': 'US', 'UZB': 'UZ', 'VAT': 'VA', 'VCT': 'VC', 'VEN': 'VE', 'VGB': 'VG',
    'VIR': 'VI', 'VNM': 'VN', 'VUT': 'VU', 'WLF': 'WF', 'WSM': 'WS', 'YEM': 'YE', 'ZAF': 'ZA', 'ZMB': 'ZM',
    'ZWE': 'ZW',
}


def fetch_countries(plugins):
    """Downloads per country summed over the plugins; (dict, number of plugins answered)."""
    totals, answered = {}, 0
    for p in plugins:
        params = [{"id": "193f985e", "type": "string/=", "value": p["package"]},
                  {"id": "ce07c624", "type": "date/all-options", "value": f"{COUNTRY_SINCE}~{TODAY.isoformat()}"}]
        try:
            rows = json.loads(get(METABASE, data=json.dumps({"parameters": params}).encode(), timeout=30))
        except Exception as exc:
            print(f"  countries: {p['package']} unavailable ({exc})")
            continue
        if not isinstance(rows, list):
            continue
        answered += 1
        for r in rows:
            iso, n = r.get("Country Code"), int(r.get("Sum of Download Count") or 0)
            if iso and n > 0:
                totals[iso] = totals.get(iso, 0) + n
    return totals, answered


def world_paths():
    """Equirectangular SVG paths for each country; (paths, iso2 -> name)."""
    if not os.path.exists(GEOJSON):
        return [], {}
    with open(GEOJSON, encoding="utf-8") as fh:
        gj = json.load(fh)
    W, H = 960.0, 470.0

    def proj(lon, lat):
        lat = max(-58.0, min(83.0, lat))
        return round((lon + 180.0) * W / 360.0, 1), round((83.0 - lat) * H / 141.0, 1)

    paths, names = [], {}
    for feat in gj.get("features", []):
        props, geom = feat.get("properties", {}), feat.get("geometry") or {}
        iso3, name = props.get("iso", ""), props.get("name", "")
        if not iso3 or name == "Antarctica":
            continue
        iso2 = ISO3_TO_ISO2.get(iso3, iso3[:2])
        names[iso2] = name
        polys = [geom["coordinates"]] if geom.get("type") == "Polygon" else geom.get("coordinates", [])
        parts = []
        for poly in polys:
            for ring in poly:
                pts, prev = [], None
                for lon, lat, *_ in ring:
                    pt = proj(lon, lat)
                    if prev is None or math.hypot(pt[0] - prev[0], pt[1] - prev[1]) >= 0.35:
                        pts.append(pt)
                        prev = pt
                if len(pts) >= 3:
                    parts.append("M" + "L".join(f"{x},{y}" for x, y in pts) + "Z")
        if parts:
            paths.append((iso2, name, " ".join(parts)))
    return paths, names


# ------------------------------------------------------------------------- icons
def icon_for(p):
    slugs = [p["package"], p["package"].lower(), p["package"].lower().replace("_", "-"),
             p["repository"].rstrip("/").split("/")[-1].lower() if p["repository"] else ""]
    for slug in filter(None, slugs):
        for ext, mime in ((".png", "image/png"), (".svg", "image/svg+xml")):
            path = os.path.join(ICON_DIR, slug + ext)
            if os.path.exists(path):
                with open(path, "rb") as fh:
                    return f"data:{mime};base64,{base64.b64encode(fh.read()).decode('ascii')}"
    local = os.path.join(PLUGINS_ROOT, p["package"], "icons", "icon.png")
    if os.path.exists(local):
        with open(local, "rb") as fh:
            return "data:image/png;base64," + base64.b64encode(fh.read()).decode("ascii")
    return ""


# ------------------------------------------------------------------------- build
def build():
    print("[1/5] plugins.xml")
    plugins = fetch_plugins()
    names = {p["package"]: p["name"] for p in plugins}
    packages = [p["package"] for p in plugins]

    print("[2/5] history")
    history = add_snapshot(load_history(), plugins)
    days, series = daily_series(history, packages, 120)
    for p in plugins:
        s = series[p["package"]]
        inc = increments(s)
        p["last30"] = sum(inc[-30:])
        p["prev30"] = sum(inc[-60:-30])
        p["last7"] = sum(inc[-7:])
        p["spark"] = inc[-30:]
        first = next((i for i, v in enumerate(s) if v is not None), None)
        p["tracked_days"] = len(s) - first - 1 if first is not None else 0
        p["icon"] = icon_for(p)
        p["hub_url"] = f"https://plugins.qgis.org/plugins/{p['package']}/"
        p["docs_url"] = f"https://geophilo.com/{p['package']}/"

    first_snap = datetime.fromisoformat(history[0]["timestamp"].replace("Z", "+00:00")).date()
    inc_all = [sum(v) for v in zip(*[increments(series[pk]) for pk in packages])]
    day_list = days[1:]  # inc_all[i] = downloads gained on day_list[i]
    weekly = []
    for w in range(12, 0, -1):
        lo = len(inc_all) - 7 * w
        if day_list[lo] <= first_snap:  # a week must start after the first snapshot
            continue
        weekly.append({"week": day_list[lo].isoformat(), "end": day_list[lo + 6].isoformat(),
                       "downloads": sum(inc_all[lo:lo + 7])})

    # A version that is current on the Hub is dated by the Hub itself: a snapshot
    # can see it days late when a run was missed.
    hub = {p["package"]: p for p in plugins}
    raw_events = release_events(history, names)
    for e in raw_events:
        cur = hub.get(e["package"])
        if cur and e["to"] == cur["version"] and cur["updated"]:
            e["date"] = min(e["date"], cur["updated"])
    events = [e for e in raw_events if date.fromisoformat(e["date"]) >= TODAY - timedelta(days=60)]
    events.sort(key=lambda e: e["date"], reverse=True)

    print("[3/5] countries")
    countries, answered = fetch_countries(plugins)
    paths, country_names = world_paths()

    print("[4/5] summary")
    total = sum(p["downloads"] for p in plugins)
    last30 = sum(p["last30"] for p in plugins)
    prev30 = sum(p["prev30"] for p in plugins)
    suites = {}
    for p in plugins:
        suites.setdefault(p["suite"], {"downloads": 0, "plugins": 0})
        suites[p["suite"]]["downloads"] += p["downloads"]
        suites[p["suite"]]["plugins"] += 1
    data = {
        "generated": NOW.strftime("%d %b %Y, %H:%M UTC"),
        "history_since": first_snap.isoformat(),
        "total": total, "last30": last30, "prev30": prev30,
        "prev30_complete": (TODAY - first_snap).days >= 60,
        "releases30": sum(1 for e in events if date.fromisoformat(e["date"]) >= TODAY - timedelta(days=30)),
        "plugins": plugins,
        "suites": [{"name": n, **suites[n]} for _, n in SUITES if n in suites],
        "weekly": weekly,
        "releases": events[:10],
        "countries": sorted(({"iso": k, "name": country_names.get(k, k), "downloads": v}
                             for k, v in countries.items()), key=lambda c: -c["downloads"]),
        "countries_answered": answered, "countries_since": COUNTRY_SINCE,
    }
    print("[5/5] page")
    page = render(data, paths)
    for name in ("index.html", "qgis_plugins_dashboard.html"):
        with open(os.path.join(HERE, name), "w", encoding="utf-8") as fh:
            fh.write(page)
    print(f"done: {len(plugins)} plugins, {total:,} downloads, {len(countries)} countries")


def render(data, paths):
    svg = "\n".join(f'<path data-iso="{iso}" data-name="{html.escape(name)}" d="{d}"/>' for iso, name, d in paths)
    with open(os.path.join(HERE, "dashboard_template.html"), encoding="utf-8") as fh:
        tpl = fh.read()
    return (tpl.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
               .replace("<!--WORLD-->", svg))


if __name__ == "__main__":
    build()
