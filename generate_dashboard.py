"""
QGIS Plugin Portfolio Analytics, Forensic Governance & Geospatial Intelligence Studio
Author: Yusuf Eminoğlu
License: MIT
Description: Enterprise-grade analytics, econometric growth models, forensic rating abuse
surveillance, interactive vector SVG choropleth mapping, and multi-channel executive storytelling
for 24 QGIS plugins across urban analytics, spatial statistics, CAD, and 3D GIS.
"""

import urllib.request
import xml.etree.ElementTree as ET
import json
import os
import sys
import math
import hashlib
import base64
from collections import Counter
from datetime import datetime, timezone, timedelta

# Configure standard output for UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Reference date & target projection dates
reference_date = datetime.now(timezone.utc)
target_date = datetime(2027, 1, 1, tzinfo=timezone.utc)

url = "https://plugins.qgis.org/plugins/plugins.xml?qgis=4.0"
print(f"[1/5] Connecting to live QGIS repository XML: {url}")

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=25) as response:
        xml_data = response.read()

    print("[2/5] Repository XML received. Parsing metadata and telemetry...")
    root = ET.fromstring(xml_data)
    yusuf_plugins = []

    def get_category(name):
        name_lower = name.lower()
        if "planx" in name_lower:
            return "PlanX Suite"
        elif name_lower.startswith("02") or "zero2" in name_lower:
            return "02 Suite"
        else:
            return "Standalone Plugins"

    # ------------------------------------------------------------------
    # Real per-country download data (Metabase public API).
    # The QGIS plugin site records per-country download stats in a Metabase
    # dashboard (recording started 2024-05-30). We fetch real counts here
    # instead of the old synthetic distribution over 16 hardcoded countries.
    # ------------------------------------------------------------------
    _MB_DASH = "2c2d25b4-5288-43da-8247-8122a2395476"
    _MB_BASE = f"https://plugins.qgis.org/metabase/api/public/dashboard/{_MB_DASH}"

    def _iso2_to_flag(iso2):
        if not iso2 or len(iso2) != 2:
            return ""
        return "".join(chr(0x1F1E6 + (ord(c.upper()) - ord("A"))) for c in iso2)

    _ISO2_REGION = {
        'AD': 'Western Europe', 'AE': 'Eastern Europe & Middle East', 'AF': 'Asia-Pacific', 'AG': 'Latin America', 'AI': 'Latin America',
        'AL': 'Western Europe', 'AM': 'Eastern Europe & Middle East', 'AO': 'Africa', 'AR': 'Latin America', 'AS': 'Asia-Pacific',
        'AT': 'Western Europe', 'AU': 'Asia-Pacific', 'AW': 'Latin America', 'AX': 'Western Europe', 'AZ': 'Eastern Europe & Middle East',
        'BA': 'Western Europe', 'BB': 'Latin America', 'BD': 'Asia-Pacific', 'BE': 'Western Europe', 'BF': 'Africa',
        'BG': 'Eastern Europe & Middle East', 'BH': 'Eastern Europe & Middle East', 'BI': 'Africa', 'BJ': 'Africa', 'BL': 'Latin America',
        'BM': 'North America', 'BN': 'Asia-Pacific', 'BO': 'Latin America', 'BQ': 'Latin America', 'BR': 'Latin America',
        'BS': 'Latin America', 'BT': 'Asia-Pacific', 'BV': 'Latin America', 'BW': 'Africa', 'BY': 'Eastern Europe & Middle East',
        'BZ': 'Latin America', 'CA': 'North America', 'CC': 'Asia-Pacific', 'CD': 'Africa', 'CF': 'Africa',
        'CG': 'Africa', 'CH': 'Western Europe', 'CI': 'Africa', 'CK': 'Asia-Pacific', 'CL': 'Latin America',
        'CM': 'Africa', 'CN': 'Asia-Pacific', 'CO': 'Latin America', 'CR': 'Latin America', 'CU': 'Latin America',
        'CV': 'Africa', 'CW': 'Latin America', 'CX': 'Asia-Pacific', 'CY': 'Eastern Europe & Middle East', 'CZ': 'Eastern Europe & Middle East',
        'DE': 'Western Europe', 'DJ': 'Africa', 'DK': 'Western Europe', 'DM': 'Latin America', 'DO': 'Latin America',
        'DZ': 'Africa', 'EC': 'Latin America', 'EE': 'Western Europe', 'EG': 'Africa', 'EH': 'Africa',
        'ER': 'Africa', 'ES': 'Western Europe', 'ET': 'Africa', 'FI': 'Western Europe', 'FJ': 'Asia-Pacific',
        'FK': 'Latin America', 'FM': 'Asia-Pacific', 'FO': 'Western Europe', 'FR': 'Western Europe', 'GA': 'Africa',
        'GB': 'Western Europe', 'GD': 'Latin America', 'GE': 'Eastern Europe & Middle East', 'GF': 'Latin America', 'GG': 'Western Europe',
        'GH': 'Africa', 'GI': 'Western Europe', 'GL': 'North America', 'GM': 'Africa', 'GN': 'Africa',
        'GP': 'Latin America', 'GQ': 'Africa', 'GR': 'Western Europe', 'GS': 'Latin America', 'GT': 'Latin America',
        'GU': 'Asia-Pacific', 'GW': 'Africa', 'GY': 'Latin America', 'HK': 'Asia-Pacific', 'HM': 'Asia-Pacific',
        'HN': 'Latin America', 'HR': 'Western Europe', 'HT': 'Latin America', 'HU': 'Eastern Europe & Middle East', 'ID': 'Asia-Pacific',
        'IE': 'Western Europe', 'IL': 'Eastern Europe & Middle East', 'IM': 'Western Europe', 'IN': 'Asia-Pacific', 'IO': 'Africa',
        'IQ': 'Eastern Europe & Middle East', 'IR': 'Asia-Pacific', 'IS': 'Western Europe', 'IT': 'Western Europe', 'JE': 'Western Europe',
        'JM': 'Latin America', 'JO': 'Eastern Europe & Middle East', 'JP': 'Asia-Pacific', 'KE': 'Africa', 'KG': 'Asia-Pacific',
        'KH': 'Asia-Pacific', 'KI': 'Asia-Pacific', 'KM': 'Africa', 'KN': 'Latin America', 'KP': 'Asia-Pacific',
        'KR': 'Asia-Pacific', 'KW': 'Eastern Europe & Middle East', 'KY': 'Latin America', 'KZ': 'Asia-Pacific', 'LA': 'Asia-Pacific',
        'LB': 'Eastern Europe & Middle East', 'LC': 'Latin America', 'LI': 'Western Europe', 'LK': 'Asia-Pacific', 'LR': 'Africa',
        'LS': 'Africa', 'LT': 'Western Europe', 'LU': 'Western Europe', 'LV': 'Western Europe', 'LY': 'Africa',
        'MA': 'Africa', 'MC': 'Western Europe', 'MD': 'Eastern Europe & Middle East', 'ME': 'Western Europe', 'MF': 'Latin America',
        'MG': 'Africa', 'MH': 'Asia-Pacific', 'MK': 'Western Europe', 'ML': 'Africa', 'MM': 'Asia-Pacific',
        'MN': 'Asia-Pacific', 'MO': 'Asia-Pacific', 'MP': 'Asia-Pacific', 'MQ': 'Latin America', 'MR': 'Africa',
        'MS': 'Latin America', 'MT': 'Western Europe', 'MU': 'Africa', 'MV': 'Asia-Pacific', 'MW': 'Africa',
        'MX': 'Latin America', 'MY': 'Asia-Pacific', 'MZ': 'Africa', 'NA': 'Africa', 'NC': 'Asia-Pacific',
        'NE': 'Africa', 'NF': 'Asia-Pacific', 'NG': 'Africa', 'NI': 'Latin America', 'NL': 'Western Europe',
        'NO': 'Western Europe', 'NP': 'Asia-Pacific', 'NR': 'Asia-Pacific', 'NU': 'Asia-Pacific', 'NZ': 'Asia-Pacific',
        'OM': 'Eastern Europe & Middle East', 'PA': 'Latin America', 'PE': 'Latin America', 'PF': 'Asia-Pacific', 'PG': 'Asia-Pacific',
        'PH': 'Asia-Pacific', 'PK': 'Asia-Pacific', 'PL': 'Eastern Europe & Middle East', 'PM': 'North America', 'PN': 'Asia-Pacific',
        'PR': 'Latin America', 'PS': 'Eastern Europe & Middle East', 'PT': 'Western Europe', 'PW': 'Asia-Pacific', 'PY': 'Latin America',
        'QA': 'Eastern Europe & Middle East', 'RE': 'Africa', 'RO': 'Eastern Europe & Middle East', 'RS': 'Western Europe', 'RU': 'Eastern Europe & Middle East',
        'RW': 'Africa', 'SA': 'Eastern Europe & Middle East', 'SB': 'Asia-Pacific', 'SC': 'Africa', 'SD': 'Africa',
        'SE': 'Western Europe', 'SG': 'Asia-Pacific', 'SH': 'Africa', 'SI': 'Western Europe', 'SJ': 'Western Europe',
        'SK': 'Eastern Europe & Middle East', 'SL': 'Africa', 'SM': 'Western Europe', 'SN': 'Africa', 'SO': 'Africa',
        'SR': 'Latin America', 'SS': 'Africa', 'ST': 'Africa', 'SV': 'Latin America', 'SX': 'Latin America',
        'SY': 'Eastern Europe & Middle East', 'SZ': 'Africa', 'TC': 'Latin America', 'TD': 'Africa', 'TF': 'Africa',
        'TG': 'Africa', 'TH': 'Asia-Pacific', 'TJ': 'Asia-Pacific', 'TK': 'Asia-Pacific', 'TL': 'Asia-Pacific',
        'TM': 'Asia-Pacific', 'TN': 'Africa', 'TO': 'Asia-Pacific', 'TR': 'Eastern Europe & Middle East', 'TT': 'Latin America',
        'TV': 'Asia-Pacific', 'TZ': 'Africa', 'UA': 'Eastern Europe & Middle East', 'UG': 'Africa', 'UM': 'Asia-Pacific',
        'US': 'North America', 'UY': 'Latin America', 'UZ': 'Asia-Pacific', 'VA': 'Western Europe', 'VC': 'Latin America',
        'VE': 'Latin America', 'VG': 'Latin America', 'VI': 'Latin America', 'VN': 'Asia-Pacific', 'VU': 'Asia-Pacific',
        'WF': 'Asia-Pacific', 'WS': 'Asia-Pacific', 'YE': 'Eastern Europe & Middle East', 'YT': 'Africa', 'ZA': 'Africa',
        'ZM': 'Africa', 'ZW': 'Africa',
    }

    # ISO3 -> ISO2 for the countries whose 3-letter code does not simply start
    # with their 2-letter code (CHN->CN, TUR->TR, SWZ->SZ, ...). Fallback: iso3[:2].
    _ISO3_TO_ISO2 = {
        'ABW': 'AW', 'AFG': 'AF', 'AGO': 'AO', 'AIA': 'AI', 'ALA': 'AX', 'ALB': 'AL',
        'AND': 'AD', 'ARE': 'AE', 'ARG': 'AR', 'ARM': 'AM', 'ASM': 'AS', 'ATA': 'AQ',
        'ATF': 'TF', 'ATG': 'AG', 'AUS': 'AU', 'AUT': 'AT', 'AZE': 'AZ', 'BDI': 'BI',
        'BEL': 'BE', 'BEN': 'BJ', 'BES': 'BQ', 'BFA': 'BF', 'BGD': 'BD', 'BGR': 'BG',
        'BHR': 'BH', 'BHS': 'BS', 'BIH': 'BA', 'BLM': 'BL', 'BLR': 'BY', 'BLZ': 'BZ',
        'BMU': 'BM', 'BOL': 'BO', 'BRA': 'BR', 'BRB': 'BB', 'BRN': 'BN', 'BTN': 'BT',
        'BVT': 'BV', 'BWA': 'BW', 'CAF': 'CF', 'CAN': 'CA', 'CCK': 'CC', 'CHE': 'CH',
        'CHL': 'CL', 'CHN': 'CN', 'CIV': 'CI', 'CMR': 'CM', 'COD': 'CD', 'COG': 'CG',
        'COK': 'CK', 'COL': 'CO', 'COM': 'KM', 'CPV': 'CV', 'CRI': 'CR', 'CUB': 'CU',
        'CUW': 'CW', 'CXR': 'CX', 'CYM': 'KY', 'CYP': 'CY', 'CZE': 'CZ', 'DEU': 'DE',
        'DJI': 'DJ', 'DMA': 'DM', 'DNK': 'DK', 'DOM': 'DO', 'DZA': 'DZ', 'ECU': 'EC',
        'EGY': 'EG', 'ERI': 'ER', 'ESH': 'EH', 'ESP': 'ES', 'EST': 'EE', 'ETH': 'ET',
        'FIN': 'FI', 'FJI': 'FJ', 'FLK': 'FK', 'FRA': 'FR', 'FRO': 'FO', 'FSM': 'FM',
        'GAB': 'GA', 'GBR': 'GB', 'GEO': 'GE', 'GGY': 'GG', 'GHA': 'GH', 'GIB': 'GI',
        'GIN': 'GN', 'GLP': 'GP', 'GMB': 'GM', 'GNB': 'GW', 'GNQ': 'GQ', 'GRC': 'GR',
        'GRD': 'GD', 'GRL': 'GL', 'GTM': 'GT', 'GUF': 'GF', 'GUM': 'GU', 'GUY': 'GY',
        'HKG': 'HK', 'HMD': 'HM', 'HND': 'HN', 'HRV': 'HR', 'HTI': 'HT', 'HUN': 'HU',
        'IDN': 'ID', 'IMN': 'IM', 'IND': 'IN', 'IOT': 'IO', 'IRL': 'IE', 'IRN': 'IR',
        'IRQ': 'IQ', 'ISL': 'IS', 'ISR': 'IL', 'ITA': 'IT', 'JAM': 'JM', 'JEY': 'JE',
        'JOR': 'JO', 'JPN': 'JP', 'KAZ': 'KZ', 'KEN': 'KE', 'KGZ': 'KG', 'KHM': 'KH',
        'KIR': 'KI', 'KNA': 'KN', 'KOR': 'KR', 'KWT': 'KW', 'LAO': 'LA', 'LBN': 'LB',
        'LBR': 'LR', 'LBY': 'LY', 'LCA': 'LC', 'LIE': 'LI', 'LKA': 'LK', 'LSO': 'LS',
        'LTU': 'LT', 'LUX': 'LU', 'LVA': 'LV', 'MAC': 'MO', 'MAF': 'MF', 'MAR': 'MA',
        'MCO': 'MC', 'MDA': 'MD', 'MDG': 'MG', 'MDV': 'MV', 'MEX': 'MX', 'MHL': 'MH',
        'MKD': 'MK', 'MLI': 'ML', 'MLT': 'MT', 'MMR': 'MM', 'MNE': 'ME', 'MNG': 'MN',
        'MNP': 'MP', 'MOZ': 'MZ', 'MRT': 'MR', 'MSR': 'MS', 'MTQ': 'MQ', 'MUS': 'MU',
        'MWI': 'MW', 'MYS': 'MY', 'MYT': 'YT', 'NAM': 'NA', 'NCL': 'NC', 'NER': 'NE',
        'NFK': 'NF', 'NGA': 'NG', 'NIC': 'NI', 'NIU': 'NU', 'NLD': 'NL', 'NOR': 'NO',
        'NPL': 'NP', 'NRU': 'NR', 'NZL': 'NZ', 'OMN': 'OM', 'PAK': 'PK', 'PAN': 'PA',
        'PCN': 'PN', 'PER': 'PE', 'PHL': 'PH', 'PLW': 'PW', 'PNG': 'PG', 'POL': 'PL',
        'PRI': 'PR', 'PRK': 'KP', 'PRT': 'PT', 'PRY': 'PY', 'PSE': 'PS', 'PYF': 'PF',
        'QAT': 'QA', 'REU': 'RE', 'ROU': 'RO', 'RUS': 'RU', 'RWA': 'RW', 'SAU': 'SA',
        'SDN': 'SD', 'SEN': 'SN', 'SGP': 'SG', 'SGS': 'GS', 'SHN': 'SH', 'SJM': 'SJ',
        'SLB': 'SB', 'SLE': 'SL', 'SLV': 'SV', 'SMR': 'SM', 'SOM': 'SO', 'SPM': 'PM',
        'SRB': 'RS', 'SSD': 'SS', 'STP': 'ST', 'SUR': 'SR', 'SVK': 'SK', 'SVN': 'SI',
        'SWE': 'SE', 'SWZ': 'SZ', 'SXM': 'SX', 'SYC': 'SC', 'SYR': 'SY', 'TCA': 'TC',
        'TCD': 'TD', 'TGO': 'TG', 'THA': 'TH', 'TJK': 'TJ', 'TKL': 'TK', 'TKM': 'TM',
        'TLS': 'TL', 'TON': 'TO', 'TTO': 'TT', 'TUN': 'TN', 'TUR': 'TR', 'TUV': 'TV',
        'TWN': 'TW', 'TZA': 'TZ', 'UGA': 'UG', 'UKR': 'UA', 'UMI': 'UM', 'URY': 'UY',
        'USA': 'US', 'UZB': 'UZ', 'VAT': 'VA', 'VCT': 'VC', 'VEN': 'VE', 'VGB': 'VG',
        'VIR': 'VI', 'VNM': 'VN', 'VUT': 'VU', 'WLF': 'WF', 'WSM': 'WS', 'YEM': 'YE',
        'ZAF': 'ZA', 'ZMB': 'ZM', 'ZWE': 'ZW',
    }

    _ISO2_NAME = {}
    _ISO2_TO_ISO3 = {}
    _gj_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "world_map.geojson")
    if not os.path.exists(_gj_path):
        _gj_path = r"C:\Users\YE\Downloads\world_map.geojson"
    if os.path.exists(_gj_path):
        try:
            with open(_gj_path, "r", encoding="utf-8") as _gf:
                for _feat in json.load(_gf).get("features", []):
                    _p = _feat.get("properties", {})
                    _iso3 = _p.get("iso", "") or ""
                    _nm = _p.get("name", "") or ""
                    if _iso3:
                        _iso2 = _ISO3_TO_ISO2.get(_iso3, _iso3[:2])
                        _ISO2_NAME[_iso2] = _nm
                        _ISO2_TO_ISO3[_iso2] = _iso3
        except Exception:
            pass

    def get_country_downloads(package_name, total_downloads):
        """Real per-country downloads for one plugin, cumulative since 2025-01-01.

        Queries the site's own Metabase "Download Stats" dashboard ("Download by
        Country" card), which returns {ISO2: count}. Falls back to an empty list
        if the fetch fails (e.g. transient network) so generation never crashes.
        """
        if not package_name:
            return []
        end = reference_date.strftime("%Y-%m-%d")
        params = [
            {"id": "193f985e", "type": "string/=", "value": package_name},
            {"id": "ce07c624", "type": "date/all-options", "value": f"2025-01-01~{end}"},
        ]
        try:
            req = urllib.request.Request(
                f"{_MB_BASE}/dashcard/28/card/26/json",
                data=json.dumps({"parameters": params}).encode("utf-8"),
                headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=40) as _resp:
                rows = json.load(_resp)
        except Exception as _e:
            print(f"    [warn] country data fetch failed for {package_name}: {_e}")
            return []

        counts = {}
        for _r in rows:
            _iso2 = _r.get("Country Code")
            _cnt = int(_r.get("Sum of Download Count", 0) or 0)
            if _iso2 and _cnt > 0:
                counts[_iso2] = counts.get(_iso2, 0) + _cnt

        _sum = sum(counts.values()) or total_downloads or 1
        _out = []
        for _iso2, _cnt in sorted(counts.items(), key=lambda kv: kv[1], reverse=True):
            _out.append({
                "country": _ISO2_NAME.get(_iso2, _iso2),
                "flag": _iso2_to_flag(_iso2),
                "region": _ISO2_REGION.get(_iso2, "Asia-Pacific"),
                "iso": _iso2,
                "iso3": _ISO2_TO_ISO3.get(_iso2, ""),
                "downloads": _cnt,
                "percentage": round((_cnt / _sum) * 100, 1),
            })
        return _out

    all_tags = []
    min_qgis_versions = []

    for plugin in root.findall('pyqgis_plugin'):
        author = plugin.find('author_name')
        if author is not None and "Yusuf Eminoglu" in author.text:
            name = plugin.attrib.get('name')
            download_url = plugin.find('download_url').text if plugin.find('download_url') is not None else None
            package_name = name
            if download_url and '/plugins/' in download_url:
                package_name = download_url.split('/plugins/')[1].split('/')[0]
            downloads = int(plugin.find('downloads').text) if plugin.find('downloads') is not None else 0
            create_date_str = plugin.find('create_date').text if plugin.find('create_date') is not None else None
            update_date_str = plugin.find('update_date').text if plugin.find('update_date') is not None else None
            version = plugin.attrib.get('version')

            qgis_min = plugin.find('qgis_minimum_version').text if plugin.find('qgis_minimum_version') is not None else "3.0"
            homepage = plugin.find('homepage').text if plugin.find('homepage') is not None else ""
            tracker = plugin.find('tracker').text if plugin.find('tracker') is not None else ""
            repository = plugin.find('repository').text if plugin.find('repository') is not None else ""
            avg_vote = float(plugin.find('average_vote').text) if plugin.find('average_vote') is not None and plugin.find('average_vote').text else 0.0
            votes_count = int(plugin.find('rating_votes').text) if plugin.find('rating_votes') is not None and plugin.find('rating_votes').text else 0
            is_experimental = plugin.find('experimental').text if plugin.find('experimental') is not None else "no"

            tags_elem = plugin.find('tags')
            tags = [t.strip() for t in tags_elem.text.split(',')] if tags_elem is not None and tags_elem.text else []
            all_tags.extend(tags)
            min_qgis_versions.append(qgis_min)

            create_date = datetime.fromisoformat(create_date_str) if create_date_str else reference_date
            update_date = datetime.fromisoformat(update_date_str) if update_date_str else reference_date

            days_active = (reference_date - create_date).days
            if days_active <= 0:
                days_active = 1
            months_active = days_active / 30.4375
            avg_monthly_downloads = downloads / months_active

            days_to_target = (target_date - reference_date).days
            if days_to_target < 0:
                days_to_target = 0
            projected_additional = avg_monthly_downloads * (days_to_target / 30.4375)
            projected_total = downloads + projected_additional

            next_milestone = 1000
            if downloads >= 10000:
                next_milestone = ((downloads // 5000) + 1) * 5000
            elif downloads >= 5000:
                next_milestone = 10000
            elif downloads >= 1000:
                next_milestone = ((downloads // 1000) + 1) * 1000
            milestone_progress = (downloads / next_milestone) * 100

            remaining_to_milestone = next_milestone - downloads
            if avg_monthly_downloads > 0 and remaining_to_milestone > 0:
                days_to_milestone = (remaining_to_milestone / avg_monthly_downloads) * 30.4375
                milestone_est_date = (reference_date + timedelta(days=days_to_milestone)).strftime('%b %d, %Y')
            else:
                milestone_est_date = "Reached"

            if downloads >= 2000 and avg_monthly_downloads >= 500:
                quadrant = "Popular Momentum"
                quadrant_color = "red"
            elif downloads < 2000 and avg_monthly_downloads >= 500:
                quadrant = "High Velocity"
                quadrant_color = "emerald"
            elif downloads >= 1000 and avg_monthly_downloads < 500:
                quadrant = "Stable Classic"
                quadrant_color = "indigo"
            else:
                quadrant = "Niche Specialist"
                quadrant_color = "slate"

            plugin_countries = get_country_downloads(package_name, downloads)
            calculated_score = round(votes_count * avg_vote, 4)

            yusuf_plugins.append({
                'name': name,
                'version': version,
                'downloads': downloads,
                'create_date': create_date.strftime('%Y-%m-%d'),
                'update_date': update_date.strftime('%Y-%m-%d'),
                'days_active': days_active,
                'months_active': round(months_active, 2),
                'avg_monthly_downloads': round(avg_monthly_downloads, 1),
                'projected_total_downloads': round(projected_total),
                'category': get_category(name),
                'tags': tags,
                'next_milestone': next_milestone,
                'milestone_progress': round(milestone_progress, 1),
                'milestone_est_date': milestone_est_date,
                'qgis_minimum_version': qgis_min,
                'homepage': homepage,
                'tracker': tracker,
                'repository': repository,
                'average_vote': avg_vote,
                'votes_count': votes_count,
                'calculated_score': calculated_score,
                'is_experimental': is_experimental,
                'quadrant': quadrant,
                'quadrant_color': quadrant_color,
                'countries': plugin_countries
            })

    yusuf_plugins.sort(key=lambda x: x['downloads'], reverse=True)

    # Resolve each plugin's main icon (from assets/plugin_icons/, keyed by the GitHub
    # repo slug) and inline it as a base64 data URI, so the static dashboard can draw
    # the real plugin icon in the BCG matrix with zero external requests. The icons are
    # committed in this repo because CI regenerates the page without the sibling dirs.
    _icon_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "plugin_icons")

    def resolve_plugin_icon(repository):
        if not repository:
            return None
        slug = repository.rstrip("/").split("/")[-1].lower()
        for ext, mime in ((".png", "image/png"), (".svg", "image/svg+xml")):
            path = os.path.join(_icon_dir, slug + ext)
            if os.path.exists(path):
                with open(path, "rb") as _f:
                    _b64 = base64.b64encode(_f.read()).decode("ascii")
                return f"data:{mime};base64,{_b64}"
        return None

    for _p in yusuf_plugins:
        _p['icon'] = resolve_plugin_icon(_p.get('repository', ''))

    # Portfolio calculations
    total_downloads = sum(p['downloads'] for p in yusuf_plugins)
    earliest_create_date = min(datetime.fromisoformat(p['create_date'] + "T00:00:00+00:00") for p in yusuf_plugins)
    portfolio_days_active = (reference_date - earliest_create_date).days
    portfolio_months_active = portfolio_days_active / 30.4375

    portfolio_overall_monthly_avg = total_downloads / portfolio_months_active
    sum_individual_monthly_avgs = sum(p['avg_monthly_downloads'] for p in yusuf_plugins)

    planx_start = datetime(2026, 4, 5, tzinfo=timezone.utc)
    planx_days = (reference_date - planx_start).days
    if planx_days <= 0:
        planx_days = 1
    planx_months = planx_days / 30.4375
    active_period_monthly_avg = total_downloads / planx_months

    tag_counts = Counter(all_tags)
    top_tags = [{'tag': k, 'count': v} for k, v in tag_counts.most_common(12)]

    qgis_counts = Counter(min_qgis_versions)
    qgis_compatibility = [{'version': k, 'count': v} for k, v in qgis_counts.items()]
    qgis_compatibility.sort(key=lambda x: x['version'])

    categories_stats = {}
    for p in yusuf_plugins:
        cat = p['category']
        if cat not in categories_stats:
            categories_stats[cat] = {'count': 0, 'downloads': 0, 'total_rating_sum': 0.0, 'total_votes': 0}
        categories_stats[cat]['count'] += 1
        categories_stats[cat]['downloads'] += p['downloads']
        categories_stats[cat]['total_rating_sum'] += (p['average_vote'] * p['votes_count'])
        categories_stats[cat]['total_votes'] += p['votes_count']

    # =========================================================================
    # [3/5] PERSISTENT HISTORICAL SNAPSHOT STORE & FORENSIC AUDIT ENGINE
    # =========================================================================
    print("[3/5] Syncing persistent historical store, computing econometrics, and auditing entropy...")
    history_file_path = os.path.join(os.path.dirname(__file__), "plugins_history.json")

    history = []
    if os.path.exists(history_file_path):
        try:
            with open(history_file_path, "r", encoding="utf-8") as hf:
                history = json.load(hf)
        except Exception as e:
            print(f"Warning: Could not parse history file: {e}")
            history = []

    if not history:
        baseline_snapshot = {
            "timestamp": "2026-08-15T07:46:00Z",
            "date_str": "Aug 15, 2026 10:46 UTC+3",
            "total_downloads": 80113,
            "plugins": {
                p['name']: {
                    "downloads": p['downloads'],
                    "average_vote": 4.846029588984898 if p['name'] == "PlanX GeoStats Lab" else p['average_vote'],
                    "votes_count": 39 if p['name'] == "PlanX GeoStats Lab" else p['votes_count'],
                    "total_score": round(39 * 4.846029588984898, 2) if p['name'] == "PlanX GeoStats Lab" else p['calculated_score'],
                    "version": p['version']
                } for p in yusuf_plugins
            }
        }
        history.append(baseline_snapshot)

    current_snapshot = {
        "timestamp": reference_date.isoformat(),
        "date_str": reference_date.strftime('%b %d, %Y %H:%M UTC'),
        "total_downloads": total_downloads,
        "plugins": {
            p['name']: {
                "downloads": p['downloads'],
                "average_vote": p['average_vote'],
                "votes_count": p['votes_count'],
                "total_score": p['calculated_score'],
                "version": p['version']
            } for p in yusuf_plugins
        }
    }

    should_append = True
    if history:
        last_snap = history[-1]
        if last_snap.get("date_str") == current_snapshot["date_str"]:
            history[-1] = current_snapshot
            should_append = False

    if should_append:
        history.append(current_snapshot)

    with open(history_file_path, "w", encoding="utf-8") as hf:
        json.dump(history, hf, indent=2, ensure_ascii=False)

    baseline = history[0]["plugins"]
    base_timestamp_str = history[0].get("timestamp")
    base_date = datetime.fromisoformat(base_timestamp_str) if base_timestamp_str else None
    delta_days = (reference_date - base_date).days if base_date else 0

    # 1. Advanced Econometric Modeling: Gini, Diversity, and Bayesian Reliability
    downloads_list = [p['downloads'] for p in yusuf_plugins]
    n_plugins = len(downloads_list)
    sorted_dl = sorted(downloads_list)
    index_sum = sum((i + 1) * d for i, d in enumerate(sorted_dl))
    gini_raw = (2.0 * index_sum) / (n_plugins * total_downloads) - ((n_plugins + 1.0) / n_plugins) if total_downloads > 0 else 0.0
    gini_corrected = (n_plugins / (n_plugins - 1.0)) * gini_raw if n_plugins > 1 else gini_raw

    shares = [d / total_downloads for d in downloads_list if d > 0]
    hhi = sum(s ** 2 for s in shares)
    shannon_entropy_portfolio = -sum(s * math.log(s) for s in shares)
    n_effective = math.exp(shannon_entropy_portfolio)

    total_portfolio_votes = sum(p['votes_count'] for p in yusuf_plugins)
    prior_mean_rating = (sum(p['average_vote'] * p['votes_count'] for p in yusuf_plugins) / total_portfolio_votes) if total_portfolio_votes > 0 else 4.80
    m_bayesian = 5.0
    prior_var = 0.25

    # 2. Forensic Surveillance & Shannon Influx Entropy Engine
    H_MAX_ENTROPY = math.log2(5.0)  # 2.321928 bits
    anomaly_reports = []
    raided_plugins = []

    for p in yusuf_plugins:
        name = p['name']
        cur_votes = p['votes_count']
        cur_avg = p['average_vote']
        cur_score = cur_votes * cur_avg
        cur_dl = p['downloads']
        v_hist = p['avg_monthly_downloads']

        # Bayesian Rating
        z_weight = cur_votes / (cur_votes + m_bayesian)
        r_bayes = z_weight * cur_avg + (1.0 - z_weight) * prior_mean_rating
        cred_floor = max(1.0, r_bayes - 1.96 * math.sqrt(prior_var / (cur_votes + m_bayesian)))

        # Baseline Reconciliation
        base_data = baseline.get(name, {
            "votes_count": cur_votes,
            "average_vote": cur_avg,
            "total_score": cur_score,
            "downloads": cur_dl
        })

        base_votes = base_data.get("votes_count", cur_votes)
        base_avg = base_data.get("average_vote", cur_avg)
        base_score = base_votes * base_avg
        base_dl = base_data.get("downloads", cur_dl)

        delta_votes = cur_votes - base_votes
        delta_score = cur_score - base_score
        delta_rating = cur_avg - base_avg
        implied_new_rating = (delta_score / delta_votes) if delta_votes > 0 else 0.0

        # Adoption Acceleration & Kinetic Momentum
        if delta_days > 0 and base_dl < cur_dl:
            v_recent = (cur_dl - base_dl) / (delta_days / 30.4375)
            alpha_kinetic = (v_recent / v_hist) if v_hist > 0 else 1.0
            accel = (v_recent - v_hist) / (0.5 * (p['days_active'] + delta_days) / 30.4375)
        else:
            v_recent = v_hist
            alpha_kinetic = 1.0
            accel = 0.0

        if alpha_kinetic >= 2.5:
            regime, regime_badge = "Hyper-Explosive", "rose"
        elif alpha_kinetic >= 1.3:
            regime, regime_badge = "Accelerating Expansion", "emerald"
        elif alpha_kinetic >= 0.8:
            regime, regime_badge = "Steady-State Cruising", "cyan"
        elif alpha_kinetic >= 0.3:
            regime, regime_badge = "Decelerating Growth", "amber"
        else:
            regime, regime_badge = "Plateau / Dormant", "slate"

        # Shannon Entropy of Influx Vector
        if delta_votes > 0:
            r_clamped = max(1.0, min(5.0, implied_new_rating))
            if r_clamped <= 1.5:
                probs = [1.0 - (r_clamped - 1.0), r_clamped - 1.0, 0.0, 0.0, 0.0]
            elif r_clamped <= 2.0:
                probs = [2.0 - r_clamped, r_clamped - 1.0, 0.0, 0.0, 0.0]
            elif r_clamped >= 4.5:
                probs = [0.0, 0.0, 0.0, 5.0 - r_clamped, 1.0 - (5.0 - r_clamped)]
            else:
                probs = [0.1, 0.2, 0.4, 0.2, 0.1]
            p_sum = sum(probs)
            norm_p = [prob / p_sum for prob in probs]
            shannon_h = -sum(prob * math.log2(prob) for prob in norm_p if prob > 1e-6)
            eas_score = (1.0 - (shannon_h / H_MAX_ENTROPY)) * max(0.0, (5.0 - r_clamped) / 4.0) * min(1.0, delta_votes / 3.0) * 100.0
            purity = (norm_p[0] if r_clamped < 2.5 else norm_p[4]) * 100.0
        else:
            shannon_h = H_MAX_ENTROPY
            eas_score = 0.0
            purity = 0.0

        if delta_votes > 0 and (cur_votes - delta_votes) > 0:
            reconciled_after_purge = (cur_score - (delta_votes * 1.0)) / (cur_votes - delta_votes)
        else:
            reconciled_after_purge = cur_avg

        target_recovering_rating = 4.80
        if cur_avg < target_recovering_rating:
            needed_5_stars = max(0, int((cur_votes * (target_recovering_rating - cur_avg)) / (5.0 - target_recovering_rating) + 0.999))
        else:
            needed_5_stars = 0

        damage_index = max(0.0, (base_avg - cur_avg) * cur_votes)

        # Cryptographic Evidence Signature
        sig_raw = f"{name}:{cur_votes}:{cur_avg}:{delta_votes}:{implied_new_rating}:{reference_date.isoformat()}"
        evidence_hash = hashlib.sha256(sig_raw.encode("utf-8")).hexdigest()[:16].upper()

        if delta_votes >= 3 and implied_new_rating <= 1.35:
            status = "CRITICAL 1-STAR RAID"
            severity = "critical"
            badge_color = "rose"
            raided_plugins.append(name)
        elif (delta_votes >= 2 and implied_new_rating <= 2.20) or (delta_rating <= -0.20 and delta_votes >= 2):
            status = "SUSPICIOUS DROP"
            severity = "high"
            badge_color = "amber"
            raided_plugins.append(name)
        elif delta_votes > 0 and implied_new_rating >= 3.8:
            status = "POSITIVE GROWTH"
            severity = "positive"
            badge_color = "emerald"
        elif delta_votes > 0:
            status = "ORGANIC ACTIVITY"
            severity = "normal"
            badge_color = "indigo"
        else:
            status = "STABLE BASELINE"
            severity = "stable"
            badge_color = "slate"

        # Superlatives & Honors Badges
        honors = []
        if name == "PlanX CAD Toolset" or cur_dl >= 15000:
            honors.append({"badge": "Crown Jewel", "icon": "fa-crown", "color": "amber"})
        if v_hist >= 600:
            honors.append({"badge": "Speed Demon", "icon": "fa-bolt-lightning", "color": "cyan"})
        if cur_avg >= 4.75 and cur_votes >= 15:
            honors.append({"badge": "Academic Standard", "icon": "fa-graduation-cap", "color": "emerald"})
        if p['days_active'] < 180 and v_hist >= 350:
            honors.append({"badge": "Rising Star", "icon": "fa-rocket", "color": "rose"})

        p.update({
            'bayesian_rating': round(r_bayes, 3),
            'rating_credibility_floor_95': round(cred_floor, 3),
            'kinetic_ratio': round(alpha_kinetic, 2),
            'adoption_acceleration': round(accel, 2),
            'kinetic_regime': regime,
            'kinetic_badge': regime_badge,
            'honors': honors,
            'evidence_hash': evidence_hash
        })

        anomaly_reports.append({
            "name": name,
            "category": p['category'],
            "version": p['version'],
            "homepage": p['homepage'],
            "repository": p['repository'],
            "tracker": p['tracker'],
            "baseline_date": history[0].get("date_str", "Baseline"),
            "baseline_votes": base_votes,
            "baseline_rating": round(base_avg, 3),
            "baseline_score": round(base_score, 2),
            "current_votes": cur_votes,
            "current_rating": round(cur_avg, 3),
            "current_score": round(cur_score, 2),
            "delta_votes": delta_votes,
            "delta_rating": round(delta_rating, 3),
            "delta_score": round(delta_score, 2),
            "damage_index": round(damage_index, 1),
            "implied_new_rating": round(implied_new_rating, 2),
            "shannon_entropy": round(shannon_h, 3),
            "entropy_score": round(eas_score, 1),
            "purity_pct": round(purity, 1),
            "reconciled_after_purge": round(reconciled_after_purge, 3),
            "needed_5_stars_to_recover": needed_5_stars,
            "evidence_hash": evidence_hash,
            "status": status,
            "severity": severity,
            "badge_color": badge_color
        })

    # Coordinated Cross-Plugin Attack Correlation Logic
    raided_count = len(raided_plugins)
    total_raid_votes = sum(a['delta_votes'] for a in anomaly_reports if a['severity'] in ('critical', 'high'))

    if raided_count >= 3:
        campaign_level = "CRITICAL_COORDINATED_SYBIL_CAMPAIGN"
        campaign_threat_score = min(100, int((raided_count / n_plugins * 100) * 1.5 + total_raid_votes * 4))
        campaign_desc = f"Simultaneous coordinated assault detected across {raided_count} independent plugins ({total_raid_votes} fraudulent votes)."
    elif raided_count >= 2:
        campaign_level = "SUSPICIOUS_MULTI_TARGET_ANOMALY"
        campaign_threat_score = min(100, int((raided_count / n_plugins * 100) + total_raid_votes * 3))
        campaign_desc = f"Multi-target anomaly identified across {raided_count} plugins."
    elif raided_count == 1:
        campaign_level = "ISOLATED_ANOMALOUS_TARGET"
        campaign_threat_score = 45
        campaign_desc = f"Isolated single-plugin vote bombing on {raided_plugins[0]}."
    else:
        campaign_level = "NO_COORDINATED_THREAT"
        campaign_threat_score = 0
        campaign_desc = "No coordinated cross-portfolio campaign detected."

    correlation_meta = {
        "campaign_level": campaign_level,
        "campaign_threat_score": campaign_threat_score,
        "campaign_desc": campaign_desc,
        "raided_plugins": raided_plugins,
        "raided_count": raided_count,
        "total_raid_votes": total_raid_votes,
        "audit_timestamp": reference_date.strftime('%Y-%m-%d %H:%M:%S UTC'),
        "portfolio_evidence_signature": hashlib.sha256(f"PORTFOLIO:{raided_count}:{total_raid_votes}:{reference_date.isoformat()}".encode()).hexdigest()[:24].upper()
    }

    severity_order = {"critical": 0, "high": 1, "amber": 2, "normal": 3, "positive": 4, "stable": 5}
    anomaly_reports.sort(key=lambda x: (severity_order.get(x['severity'], 9), -x['delta_votes'], -x['entropy_score']))

    critical_count = sum(1 for a in anomaly_reports if a['severity'] == 'critical')
    warning_count = sum(1 for a in anomaly_reports if a['severity'] == 'high')

    # =========================================================================
    # GEOSPATIAL & MACRO-REGIONAL INTELLIGENCE & SUITE AFFINITY MATRIX
    # =========================================================================
    macro_regions_meta = {
        "Western Europe": {"code": "WEU", "icon": "fa-landmark", "rank_title": "Primary Anchor Market", "color": "#0ea5e9"},
        "North America": {"code": "NAM", "icon": "fa-city", "rank_title": "High-Volume Engine", "color": "#38bdf8"},
        "Latin America": {"code": "LAM", "icon": "fa-mountain-sun", "rank_title": "Rapid Growth Frontier", "color": "#10b981"},
        "Eastern Europe & Middle East": {"code": "EME", "icon": "fa-mosque", "rank_title": "Strategic Core Hub", "color": "#f59e0b"},
        "Asia-Pacific": {"code": "APAC", "icon": "fa-satellite-dish", "rank_title": "High-Velocity Tech Hub", "color": "#818cf8"},
        "Africa": {"code": "AFR", "icon": "fa-earth-africa", "rank_title": "Emerging Market", "color": "#14b8a6"}
    }

    country_iso_atlas = {
        "United States": {"iso": "US", "iso3": "USA", "cx": 274.7, "cy": 180.8, "reg": "North America"},
        "Canada": {"iso": "CA", "iso3": "CAN", "cx": 278.1, "cy": 158.5, "reg": "North America"},
        "Germany": {"iso": "DE", "iso3": "DEU", "cx": 515.7, "cy": 135.0, "reg": "Western Europe"},
        "France": {"iso": "FR", "iso3": "FRA", "cx": 486.3, "cy": 147.0, "reg": "Western Europe"},
        "United Kingdom": {"iso": "GB", "iso3": "GBR", "cx": 479.7, "cy": 138.2, "reg": "Western Europe"},
        "Spain": {"iso": "ES", "iso3": "ESP", "cx": 470.1, "cy": 175.7, "reg": "Western Europe"},
        "Italy": {"iso": "IT", "iso3": "ITA", "cx": 513.3, "cy": 170.8, "reg": "Western Europe"},
        "Netherlands": {"iso": "NL", "iso3": "NLD", "cx": 493.1, "cy": 135.3, "reg": "Western Europe"},
        "Turkey": {"iso": "TR", "iso3": "TUR", "cx": 567.6, "cy": 177.3, "reg": "Eastern Europe & Middle East"},
        "Poland": {"iso": "PL", "iso3": "POL", "cx": 536.0, "cy": 136.0, "reg": "Eastern Europe & Middle East"},
        "Brazil": {"iso": "BR", "iso3": "BRA", "cx": 352.3, "cy": 360.5, "reg": "Latin America"},
        "Mexico": {"iso": "MX", "iso3": "MEX", "cx": 215.7, "cy": 244.6, "reg": "Latin America"},
        "India": {"iso": "IN", "iso3": "IND", "cx": 685.9, "cy": 214.2, "reg": "Asia-Pacific"},
        "China": {"iso": "CN", "iso3": "CHN", "cx": 790.4, "cy": 177.4, "reg": "Asia-Pacific"},
        "Japan": {"iso": "JP", "iso3": "JPN", "cx": 852.5, "cy": 191.2, "reg": "Asia-Pacific"},
        "Australia": {"iso": "AU", "iso3": "AUS", "cx": 877.6, "cy": 424.3, "reg": "Asia-Pacific"}
    }

    country_data_map = {}
    suite_totals = {}
    for p in yusuf_plugins:
        c = p['category']
        suite_totals[c] = suite_totals.get(c, 0) + p['downloads']

    regional_totals = {}
    suite_region_matrix = {}

    for p in yusuf_plugins:
        p_name = p['name']
        cat = p['category']
        if cat not in suite_region_matrix:
            suite_region_matrix[cat] = {}

        for c in p.get('countries', []):
            c_name = c['country']
            c_flag = c['flag']
            c_reg = c['region']
            d = c['downloads']

            if c_name not in country_data_map:
                country_data_map[c_name] = {
                    'country': c_name,
                    'flag': c_flag,
                    'region': c_reg,
                    'iso': c.get('iso', 'XX'),
                    'iso3': c.get('iso3', ''),
                    'cx': 500,
                    'cy': 250,
                    'downloads': 0,
                    'suite_downloads': {},
                    'top_plugins': []
                }

            country_data_map[c_name]['downloads'] += d
            country_data_map[c_name]['suite_downloads'][cat] = country_data_map[c_name]['suite_downloads'].get(cat, 0) + d
            country_data_map[c_name]['top_plugins'].append({
                'name': p_name,
                'downloads': d,
                'category': cat,
                'percentage': c['percentage']
            })

            regional_totals[c_reg] = regional_totals.get(c_reg, 0) + d
            suite_region_matrix[cat][c_reg] = suite_region_matrix[cat].get(c_reg, 0) + d

    for c_name, c_info in country_data_map.items():
        c_info['top_plugins'].sort(key=lambda x: x['downloads'], reverse=True)
        c_info['percentage'] = round((c_info['downloads'] / total_downloads) * 100, 1) if total_downloads > 0 else 0
        dom_suite = max(c_info['suite_downloads'].items(), key=lambda x: x[1])[0] if c_info['suite_downloads'] else "N/A"
        c_info['dominant_suite'] = dom_suite

    global_countries = sorted(country_data_map.values(), key=lambda x: x['downloads'], reverse=True)

    sorted_regions = sorted(regional_totals.items(), key=lambda x: x[1], reverse=True)
    macro_regions_cards = []
    for rank_idx, (reg_name, reg_dl) in enumerate(sorted_regions, start=1):
        reg_pct = round((reg_dl / total_downloads) * 100, 1) if total_downloads > 0 else 0
        meta = macro_regions_meta.get(reg_name, {"code": "REG", "icon": "fa-globe", "rank_title": "Regional Market", "color": "#0ea5e9"})

        reg_suites = {s: suite_region_matrix[s].get(reg_name, 0) for s in suite_totals}
        dom_suite = max(reg_suites.items(), key=lambda x: x[1]) if reg_suites else ("N/A", 0)
        dom_suite_pct = round((dom_suite[1] / reg_dl) * 100, 1) if reg_dl > 0 else 0

        reg_plugins_map = {}
        for p in yusuf_plugins:
            for c in p.get('countries', []):
                if c['region'] == reg_name:
                    reg_plugins_map[p['name']] = reg_plugins_map.get(p['name'], 0) + c['downloads']
        top_3_plugins = sorted(reg_plugins_map.items(), key=lambda x: x[1], reverse=True)[:3]
        top_3_formatted = [{'name': name, 'downloads': dl, 'percentage': round((dl / reg_dl) * 100, 1)} for name, dl in top_3_plugins]

        macro_regions_cards.append({
            'rank': rank_idx,
            'region': reg_name,
            'code': meta['code'],
            'icon': meta['icon'],
            'rank_title': meta['rank_title'],
            'color': meta['color'],
            'downloads': reg_dl,
            'percentage': reg_pct,
            'dominant_suite': dom_suite[0],
            'dominant_suite_share': dom_suite_pct,
            'top_plugins': top_3_formatted,
            'country_count': sum(1 for c in country_data_map.values() if c['region'] == reg_name)
        })

    affinity_matrix = []
    all_regions_ordered = [r['region'] for r in macro_regions_cards]

    for suite_name, suite_dl in suite_totals.items():
        suite_global_share = (suite_dl / total_downloads) if total_downloads > 0 else 0
        region_cells = []

        for reg_name in all_regions_ordered:
            r_dl = regional_totals.get(reg_name, 0)
            sr_dl = suite_region_matrix.get(suite_name, {}).get(reg_name, 0)

            reg_share = round((sr_dl / r_dl) * 100, 1) if r_dl > 0 else 0.0
            suite_share = round((sr_dl / suite_dl) * 100, 1) if suite_dl > 0 else 0.0
            lq = round((sr_dl / r_dl) / (suite_dl / total_downloads), 2) if (r_dl > 0 and suite_dl > 0) else 1.00

            if lq >= 1.15:
                affinity_status = "Over-Indexing"
                badge_color = "emerald"
            elif lq <= 0.85:
                affinity_status = "Under-Indexed"
                badge_color = "amber"
            else:
                affinity_status = "Balanced"
                badge_color = "cyan"

            region_cells.append({
                'region': reg_name,
                'downloads': sr_dl,
                'regional_share': reg_share,
                'suite_share': suite_share,
                'location_quotient': lq,
                'affinity_status': affinity_status,
                'badge_color': badge_color
            })

        affinity_matrix.append({
            'suite': suite_name,
            'global_downloads': suite_dl,
            'global_share': round(suite_global_share * 100, 1),
            'cells': region_cells
        })

    # Time series history by plugin for interactive dual-axis chart
    history_by_plugin = {}
    history_timestamps = [s.get("date_str", s.get("timestamp")) for s in history]

    for p in yusuf_plugins:
        name = p['name']
        rating_series = []
        votes_series = []
        for s in history:
            p_snap = s.get("plugins", {}).get(name)
            if p_snap:
                rating_series.append(round(p_snap.get("average_vote", 0.0), 2))
                votes_series.append(p_snap.get("votes_count", 0))
            else:
                rating_series.append(0.0)
                votes_series.append(0)

        history_by_plugin[name] = {
            "ratings": rating_series,
            "votes": votes_series
        }

    # Community Impact & Planning Efficiency Valuation
    total_hours_saved = sum(p['downloads'] * 0.75 for p in yusuf_plugins)
    total_economic_val_usd = total_hours_saved * 50.0

    pipelines_data = [
        {
            "id": "morphology",
            "name": "Urban Spatial Analytics & Network Morphology Pipeline",
            "category": "Urban Analytics & Space Syntax",
            "icon": "fa-network-wired",
            "color": "#0ea5e9",
            "desc": "Autonomous workflow converting raw OpenStreetMap street networks into axial graph centrality, local spatial autocorrelation (Moran's I/LISA), and multi-dimensional bivariate cartography.",
            "estimated_time": "~4.5 mins / city",
            "steps": [
                {"step": 1, "plugin": "02Agent OSM Downloader", "action": "Bounded Highway & Urban Fabric Acquisition", "type": "Input: BBOX / Admin Area", "output": "OSM Vector Layer"},
                {"step": 2, "plugin": "PlanX", "action": "Space Syntax Axial Integration & Choice Analysis", "type": "Topology Graph", "output": "Centrality Vectors"},
                {"step": 3, "plugin": "PlanX GeoStats Lab", "action": "Moran's I & Local Getis-Ord Gi* Hotspot Detection", "type": "Spatial Statistics", "output": "LISA Significance Layer"},
                {"step": 4, "plugin": "PlanX CartoLab", "action": "Bivariate & Value-by-Alpha Publication Rendering", "type": "Cartography", "output": "Publication Cartogram"},
                {"step": 5, "plugin": "PlanX DataCube Lab", "action": "Spatio-Temporal Aggregation & Voxel Cubes", "type": "Time-Series", "output": "EHSA 3D Cube"}
            ]
        },
        {
            "id": "3d_massing",
            "name": "Generative 3D City Simulation & Procedural Massing",
            "category": "3D GIS & Generative Urban Design",
            "icon": "fa-cubes",
            "color": "#6366f1",
            "desc": "End-to-end procedural city builder: fetches building footprints, extrudes massing models, applies parametric building codes (FAR/TAKS), and runs multi-objective evolutionary optimization.",
            "estimated_time": "~6.0 mins / district",
            "steps": [
                {"step": 1, "plugin": "3D OSM Model", "action": "Single-Click WebGL 3D Urban Fabric Extraction", "type": "OSM Fetcher", "output": "3D Building Polygons"},
                {"step": 2, "plugin": "OSM Quick 3D", "action": "Native QGIS 3D Canvas Extrusion & 2D Massing", "type": "Native 3D", "output": "Extruded Massing Layer"},
                {"step": 3, "plugin": "PlanX 3D City Viewer", "action": "Interactive WebGL/Three.js Urban Viewer Export", "type": "Web 3D", "output": "Three.js Scene Bundle"},
                {"step": 4, "plugin": "PlanX Urban Procedural 3D", "action": "Parametric Zoning & Envelope Allocation", "type": "Zoning Code", "output": "Procedural Envelopes"},
                {"step": 5, "plugin": "Parametric Process", "action": "NSGA-II Multi-Objective Evolutionary Optimization", "type": "Pareto Solver", "output": "Optimal Pareto Solutions"}
            ]
        },
        {
            "id": "master_planning",
            "name": "Statutory Master Planning & Automated Parcel Division",
            "category": "CAD & Urban Planning",
            "icon": "fa-draw-polygon",
            "color": "#10b981",
            "desc": "Converts legacy CAD/DXF/DWG/NCZ files into GeoPackages, aligns road platforms with tangent fillets, and subdivides urban blocks into optimal parcels with setback rules.",
            "estimated_time": "~3.2 mins / block",
            "steps": [
                {"step": 1, "plugin": "02CadGis", "action": "Universal CAD (DWG/DXF/NCZ/DGN) Conversion", "type": "CAD Ingestion", "output": "Standard GeoPackage"},
                {"step": 2, "plugin": "PlanX CAD Toolset", "action": "Road Platform Alignment & Engineering Drafting", "type": "CAD Platform", "output": "Aligned Road Polylines"},
                {"step": 3, "plugin": "EasyFillet", "action": "Precision Tangent Arc & Corner Fillet Generation", "type": "Geometry Engine", "output": "Filleted Corner Layer"},
                {"step": 4, "plugin": "ParcelFlux", "action": "Urban Block Subdivision (Spine offset, frontage)", "type": "Subdivision", "output": "Divided Parcels"},
                {"step": 5, "plugin": "PlanX UIP Toolset", "action": "Statutory Master Plan (UIP) Standards Compliance", "type": "Zoning Audit", "output": "Validated Master Plan"}
            ]
        },
        {
            "id": "resilience",
            "name": "Climate Resilience & Multi-Criteria Suitability Suite",
            "category": "Resilience & Decision Support",
            "icon": "fa-shield-halved",
            "color": "#f59e0b",
            "desc": "Models urban vulnerability across seismic hazards, urban heat islands (UHI), inundation zones, and raster AHP suitability criteria with synchronized multi-canvas validation.",
            "estimated_time": "~5.0 mins / basin",
            "steps": [
                {"step": 1, "plugin": "PlanX: Urban Resilience", "action": "Seismic, Flood & Urban Heat Vulnerability Indexing", "type": "Hazard Engine", "output": "Resilience Risk Score"},
                {"step": 2, "plugin": "PlanX Suitability Lab", "action": "Raster MCDA & Analytical Hierarchy Process (AHP)", "type": "Decision Model", "output": "Suitability Surface"},
                {"step": 3, "plugin": "02viz", "action": "Interactive Multi-Engine (Python/R) Chart Studio", "type": "Statistical Viz", "output": "Risk Distribution Chart"},
                {"step": 4, "plugin": "02Multimap", "action": "Multi-Panel Synchronized Canvas Validation", "type": "Multi-Canvas", "output": "Laser-Synced Comparison"}
            ]
        },
        {
            "id": "truth_gaming",
            "name": "Map Truth Lab & AI-Assisted Workflow Studio",
            "category": "Playable GIS & AI Workflows",
            "icon": "fa-gamepad",
            "color": "#ec4899",
            "desc": "Projection distortion audit, interactive Size Duel gaming, generative map artwork, and visual AI model orchestration for automated multi-step processing recipes.",
            "estimated_time": "~2.8 mins / recipe",
            "steps": [
                {"step": 1, "plugin": "02truesize", "action": "True-Size Distortion Audit & Tissot Indicatrix", "type": "Projection Lab", "output": "Projection Scorecard"},
                {"step": 2, "plugin": "02Urban Portrait", "action": "City as a Face: Reversible Luminance Map Art", "type": "Generative Art", "output": "Vector Artwork Canvas"},
                {"step": 3, "plugin": "02GeoQuest", "action": "Gamified Map Studio & Interactive Value Duel", "type": "Playable Engine", "output": "Offline Game Package"},
                {"step": 4, "plugin": "02Agent Smart Modeler", "action": "Visual AI Flow Execution & Workflow Proposals", "type": "AI Modeler", "output": "Compiled Pipeline Model"}
            ]
        }
    ]

    total_votes = sum(p['votes_count'] for p in yusuf_plugins)
    total_score = sum(p['average_vote'] * p['votes_count'] for p in yusuf_plugins)
    overall_rating = (total_score / total_votes) if total_votes > 0 else 4.80
    portfolio_bayesian_avg = sum(p['bayesian_rating'] for p in yusuf_plugins) / len(yusuf_plugins) if yusuf_plugins else 4.80
    portfolio_monthly_velocity = active_period_monthly_avg
    active_count = len(yusuf_plugins)

    embedded_data = {
        'plugins': yusuf_plugins,
        'summary': {
            'total_plugins': len(yusuf_plugins),
            'total_downloads': total_downloads,
            'community_hours_saved': round(total_hours_saved),
            'economic_value_usd': round(total_economic_val_usd),
            'overall_raw_rating': round(overall_rating, 2),
            'portfolio_bayesian_rating': round(portfolio_bayesian_avg, 2),
            'total_votes': total_votes,
            'active_plugins': active_count,
            'portfolio_monthly_velocity': round(portfolio_monthly_velocity),
            'active_period_monthly_avg': round(active_period_monthly_avg),
            'portfolio_overall_monthly_avg': round(portfolio_overall_monthly_avg),
            'sum_individual_monthly_avgs': round(sum_individual_monthly_avgs),
            'categories': categories_stats,
            'top_tags': top_tags,
            'qgis_compatibility': qgis_compatibility,
            'global_countries': global_countries,
            'macro_regions': macro_regions_cards,
            'suite_affinity_matrix': affinity_matrix,
            'pipelines': pipelines_data,
            'econometrics': {
                'gini_coefficient': round(gini_raw, 4),
                'gini_corrected': round(gini_corrected, 4),
                'herfindahl_index_hhi': round(hhi, 4),
                'shannon_entropy': round(shannon_entropy_portfolio, 4),
                'effective_plugin_count': round(n_effective, 2),
                'prior_mean_rating': round(prior_mean_rating, 3)
            },
            'critical_anomalies': critical_count,
            'warning_anomalies': warning_count,
            'total_snapshots': len(history)
        },
        'anomalies': anomaly_reports,
        'correlation': correlation_meta,
        'history_meta': {
            'snapshots': history,
            'timestamps': history_timestamps,
            'by_plugin': history_by_plugin
        }
    }

    # =============================================================
    # [4/5] REAL WORLD GEOJSON VECTOR CARTOGRAPHY ENGINE
    # =============================================================
    print("[4/5] Processing real world GeoJSON boundaries and generating SVG cartography...")

    geojson_path = os.path.join(os.path.dirname(__file__), "world_map.geojson")
    if not os.path.exists(geojson_path):
        geojson_path = r"C:\Users\YE\Downloads\world_map.geojson"

    world_svg_layer_elements = []

    if os.path.exists(geojson_path):
        try:
            with open(geojson_path, "r", encoding="utf-8") as gf:
                world_geojson = json.load(gf)

            W_map = 960.0
            H_map = 500.0

            def project_equirectangular(lon, lat):
                lat = max(-75.0, min(83.0, lat))
                x = (lon + 180.0) * (W_map / 360.0)
                y = (90.0 - lat) * (H_map / 180.0) * 0.92 + 18.0
                return round(x, 1), round(y, 1)

            def simplify_points(pts, tolerance=0.28):
                if len(pts) <= 3:
                    return pts
                simplified = [pts[0]]
                for p in pts[1:-1]:
                    prev = simplified[-1]
                    dist = math.hypot(p[0] - prev[0], p[1] - prev[1])
                    if dist >= tolerance:
                        simplified.append(p)
                simplified.append(pts[-1])
                return simplified

            def coords_to_svg_path(coords, geom_type, tolerance=0.28):
                paths = []
                if geom_type == 'Polygon':
                    polys = [coords]
                elif geom_type == 'MultiPolygon':
                    polys = coords
                else:
                    return ""
                
                for poly in polys:
                    for ring in poly:
                        if not ring or len(ring) < 3:
                            continue
                        projected = [project_equirectangular(pt[0], pt[1]) for pt in ring]
                        simplified = simplify_points(projected, tolerance)
                        if len(simplified) < 3:
                            continue
                        ring_str = [f"M{simplified[0][0]},{simplified[0][1]}"]
                        for pt in simplified[1:]:
                            ring_str.append(f"L{pt[0]},{pt[1]}")
                        ring_str.append("Z")
                        paths.append("".join(ring_str))
                return " ".join(paths)

            iso3_to_iso2 = {
                'USA': 'US', 'CAN': 'CA', 'DEU': 'DE', 'FRA': 'FR', 'GBR': 'GB',
                'ESP': 'ES', 'ITA': 'IT', 'NLD': 'NL', 'TUR': 'TR', 'POL': 'PL',
                'BRA': 'BR', 'MEX': 'MX', 'IND': 'IND', 'CHN': 'CN', 'JPN': 'JP',
                'AUS': 'AU', 'RUS': 'RU', 'ZAF': 'ZA', 'ARG': 'AR', 'KOR': 'KR',
                'SWE': 'SE', 'NOR': 'NO', 'FIN': 'FI', 'DNK': 'DK', 'CHE': 'CH',
                'AUT': 'AT', 'BEL': 'BE', 'PRT': 'PT', 'GRC': 'GR', 'CZE': 'CZ',
                'ROU': 'RO', 'HUN': 'HU', 'NZL': 'NZ', 'SGP': 'SG', 'IDN': 'ID',
                'MYS': 'MY', 'PHL': 'PH', 'THA': 'TH', 'VNM': 'VN', 'EGY': 'EG',
                'SAU': 'SA', 'ARE': 'AE', 'ISR': 'IL', 'COL': 'CO', 'CHL': 'CL',
                'PER': 'PE', 'VEN': 'VE', 'UKR': 'UA', 'IRL': 'IE'
            }

            iso3_point_map = {}
            for feat in world_geojson.get('features', []):
                props = feat.get('properties', {})
                geom = feat.get('geometry', {})
                name = props.get('name', '')
                iso3 = props.get('iso', '')
                lon = props.get('lon')
                lat = props.get('lat')
                if iso3 and lon is not None and lat is not None:
                    iso3_point_map[iso3] = (lon, lat)
                if name == 'Antarctica':
                    continue
                iso2 = iso3_to_iso2.get(iso3, iso3[:2] if iso3 else 'XX')
                d_path = coords_to_svg_path(geom.get('coordinates', []), geom.get('type', ''), tolerance=0.28)
                if not d_path:
                    continue
                clean_name = name.replace('"', '&quot;')
                world_svg_layer_elements.append(
                    f'<path id="geo-{iso2}" data-iso="{iso2}" data-iso3="{iso3}" data-name="{clean_name}" '
                    f'class="country-path cursor-pointer transition-all duration-200" d="{d_path}" />'
                )
            print(f"[4/5] Processed {len(world_svg_layer_elements)} real-world sovereign country polygons.")

            # Correct the country marker positions: replace the hardcoded atlas
            # cx/cy with each country's own representative point from the GeoJSON
            # (properties.lon/lat), projected into the same equirectangular space
            # the polygons are drawn in. Without this the dots land off-country.
            for c_name, c_info in country_data_map.items():
                iso3 = c_info.get('iso3', '')
                if iso3 in iso3_point_map:
                    lon, lat = iso3_point_map[iso3]
                    c_info['cx'], c_info['cy'] = project_equirectangular(lon, lat)
        except Exception as ge:
            print(f"Warning: Failed to load world_map.geojson: {ge}")

    world_svg_layer_html = "\\n".join(world_svg_layer_elements)

    html_template = """<!DOCTYPE html>
<html lang="en" data-theme="obsidian">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QGIS Plugin Portfolio Analytics & Governance Studio — Yusuf Eminoğlu</title>
    
    <!-- Comprehensive SEO Keywords & Metadata -->
    <meta name="description" content="Enterprise analytics, telemetry, growth forecasting, and rating abuse forensic surveillance studio for Yusuf Eminoğlu's 24 production QGIS plugins across urban analytics, spatial statistics, CAD, and 3D GIS.">
    <meta name="keywords" content="QGIS, QGIS Plugins, Yusuf Eminoğlu, PlanX, Urban Analytics, Spatial Statistics, Space Syntax, GIS, Remote Sensing, Urban Planning, Cartography, PyQGIS, GeoPackage, Three.js, OpenStreetMap, Rating Governance, Forensic Telemetry, Open Source GIS, Python GIS">
    <meta name="author" content="Yusuf Eminoğlu">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://yusufeminoglu.github.io/qgis-plugins-governance/">

    <!-- Open Graph / Facebook / LinkedIn -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://yusufeminoglu.github.io/qgis-plugins-governance/">
    <meta property="og:title" content="QGIS Plugin Portfolio Analytics & Governance Studio — Yusuf Eminoğlu">
    <meta property="og:description" content="Enterprise telemetry, adoption forecasting, and rating abuse forensic surveillance for 24 QGIS urban analytics plugins.">
    <meta property="og:image" content="https://yusufeminoglu.github.io/qgis-plugins-governance/preview.png">

    <!-- Twitter Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="https://yusufeminoglu.github.io/qgis-plugins-governance/">
    <meta name="twitter:title" content="QGIS Plugin Portfolio Analytics & Governance Studio">
    <meta name="twitter:description" content="Enterprise analytics, telemetry, and rating abuse forensic surveillance for 24 QGIS urban analytics plugins.">

    <!-- JSON-LD Structured Data (Schema.org) -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "name": "QGIS Plugin Portfolio Analytics & Governance Studio",
      "author": {
        "@type": "Person",
        "name": "Yusuf Eminoğlu",
        "url": "https://plugins.qgis.org/plugins/author/Yusuf%20Eminoglu/"
      },
      "description": "Enterprise analytics, telemetry, growth forecasting, and rating abuse forensic surveillance studio for 24 production QGIS plugins.",
      "applicationCategory": "DeveloperApplication",
      "operatingSystem": "Cross-platform",
      "offers": {
        "@type": "Offer",
        "price": "0.00",
        "priceCurrency": "USD"
      }
    }
    </script>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- FontAwesome Pro/Free Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- ApexCharts -->
    <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
    <script>
        tailwind.config = {
            darkMode: ['class', '[data-theme="obsidian"]'],
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
                        heading: ['Plus Jakarta Sans', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace'],
                    },
                    colors: {
                        obsidian: {
                            950: '#070a10',
                            900: '#0b111e',
                            850: '#101828',
                            800: '#142036',
                            750: '#1a2942',
                            700: '#223554'
                        }
                    }
                }
            }
        }
    </script>
    <style>
        /* =========================================================================
           MASTER DESIGN SYSTEM & SEMANTIC TOKEN ARCHITECTURE
           ========================================================================= */
        :root {
            --bg-canvas: #070a10;
            --bg-canvas-subtle: #0b111e;
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --text-muted: #64748b;
            --text-accent: #38bdf8;

            --panel-bg: rgba(16, 24, 40, 0.72);
            --panel-bg-hover: rgba(20, 32, 54, 0.82);
            --panel-border: rgba(255, 255, 255, 0.08);
            --panel-border-hover: rgba(56, 189, 248, 0.35);
            --panel-specular: linear-gradient(180deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.00) 100%);
            --panel-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.55), 0 0 0 1px rgba(255, 255, 255, 0.05);
            --panel-shadow-hover: 0 20px 40px -8px rgba(0, 0, 0, 0.7), 0 0 24px -2px rgba(56, 189, 248, 0.12);

            --nested-bg: rgba(7, 10, 16, 0.75);
            --nested-border: rgba(255, 255, 255, 0.06);
            --input-bg: #0b111e;
            --input-border: rgba(255, 255, 255, 0.12);

            --font-heading: 'Plus Jakarta Sans', sans-serif;
            --font-body: 'Inter', sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }

        [data-theme="alabaster"] {
            --bg-canvas: #f1f5f9;
            --bg-canvas-subtle: #e2e8f0;
            --text-main: #0f172a;
            --text-sub: #334155;
            --text-muted: #475569;
            --text-accent: #0284c7;

            --panel-bg: rgba(255, 255, 255, 0.88);
            --panel-bg-hover: rgba(255, 255, 255, 0.98);
            --panel-border: rgba(15, 23, 42, 0.08);
            --panel-border-hover: rgba(2, 132, 199, 0.45);
            --panel-specular: linear-gradient(180deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.4) 100%);
            --panel-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 10px 25px -5px rgba(15, 23, 42, 0.06), 0 0 0 1px rgba(15, 23, 42, 0.04);
            --panel-shadow-hover: 0 12px 30px -4px rgba(15, 23, 42, 0.12), 0 0 20px 0 rgba(2, 132, 199, 0.15);

            --nested-bg: rgba(248, 250, 252, 0.85);
            --nested-border: rgba(15, 23, 42, 0.08);
            --input-bg: #ffffff;
            --input-border: rgba(15, 23, 42, 0.16);
        }

        body {
            background-color: var(--bg-canvas);
            color: var(--text-main);
            font-family: var(--font-body);
            letter-spacing: -0.011em;
            overflow-x: hidden;
            transition: background-color 0.3s ease, color 0.3s ease;
        }
        h1, h2, h3, h4, h5, h6, .font-heading {
            font-family: var(--font-heading);
            letter-spacing: -0.028em;
        }
        .font-mono {
            font-family: var(--font-mono);
            font-feature-settings: "tnum" 1, "zero" 1, "cv05" 1;
        }

        #bg-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            z-index: 0;
        }

        .studio-container {
            position: relative;
            z-index: 10;
            width: 100%;
            max-width: 1720px;
            margin-left: auto;
            margin-right: auto;
            padding-left: clamp(1rem, 2.5vw, 2.5rem);
            padding-right: clamp(1rem, 2.5vw, 2.5rem);
        }

        .glass-panel {
            position: relative;
            background: var(--panel-bg);
            backdrop-filter: blur(24px) saturate(180%);
            -webkit-backdrop-filter: blur(24px) saturate(180%);
            border: 1px solid var(--panel-border);
            box-shadow: var(--panel-shadow);
            border-radius: 1.5rem;
            transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1),
                        border-color 0.25s ease,
                        box-shadow 0.28s cubic-bezier(0.16, 1, 0.3, 1),
                        background 0.3s ease;
        }
        .glass-panel::before {
            content: '';
            position: absolute;
            inset: 0 0 auto 0;
            height: 1px;
            background: var(--panel-specular);
            border-radius: 1.5rem 1.5rem 0 0;
            pointer-events: none;
        }
        .glass-panel:hover {
            transform: translateY(-2px);
            border-color: var(--panel-border-hover);
            box-shadow: var(--panel-shadow-hover);
            background: var(--panel-bg-hover);
        }

        .glass-panel-danger {
            background: linear-gradient(135deg, rgba(244, 63, 94, 0.09) 0%, var(--panel-bg) 100%);
            border: 1px solid rgba(244, 63, 94, 0.35);
            box-shadow: 0 12px 35px -6px rgba(244, 63, 94, 0.22);
        }

        .btn-luxury {
            background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
            border: 1px solid rgba(56, 189, 248, 0.4);
            box-shadow: 0 4px 14px rgba(2, 132, 199, 0.28);
            color: #ffffff !important;
            transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .btn-luxury:hover {
            background: linear-gradient(135deg, #0369a1 0%, #075985 100%);
            border-color: rgba(56, 189, 248, 0.75);
            box-shadow: 0 8px 22px rgba(2, 132, 199, 0.45);
            transform: translateY(-1px);
        }

        .btn-danger {
            background: linear-gradient(135deg, #e11d48 0%, #be123c 100%);
            border: 1px solid rgba(251, 113, 133, 0.4);
            box-shadow: 0 4px 14px rgba(225, 29, 72, 0.28);
            color: #ffffff !important;
            transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .btn-danger:hover {
            background: linear-gradient(135deg, #be123c 0%, #9f1239 100%);
            box-shadow: 0 8px 24px rgba(225, 29, 72, 0.45);
            transform: translateY(-1px);
        }

        @keyframes pulse-ring {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(244, 63, 94, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(244, 63, 94, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(244, 63, 94, 0); }
        }
        .pulse-live {
            animation: pulse-ring 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }

        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: var(--bg-canvas); }
        ::-webkit-scrollbar-thumb { background: var(--text-muted); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--text-accent); }

        kbd {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 4px;
            padding: 1px 5px;
            font-size: 10px;
            font-family: var(--font-mono);
            color: var(--text-sub);
        }
        [data-theme="alabaster"] kbd {
            background: rgba(15, 23, 42, 0.06);
            border-color: rgba(15, 23, 42, 0.14);
            color: var(--text-sub);
        }

        @media print {
            body { background: #fff !important; color: #000 !important; }
            .glass-panel { background: #fff !important; border: 1px solid #ddd !important; box-shadow: none !important; color: #000 !important; }
            header, nav, button, .btn-luxury, .btn-danger, #bg-canvas, kbd, select, input { display: none !important; }
            .tab-pane { display: block !important; }
        }
    </style>
</head>
<body class="min-h-screen pb-14 selection:bg-cyan-500 selection:text-white">

    <!-- Interactive Background Constellation -->
    <canvas id="bg-canvas"></canvas>

    <!-- Ambient Radial Glows -->
    <div class="fixed top-0 left-1/4 w-[500px] h-[500px] bg-cyan-500/5 rounded-full blur-[140px] -z-10 pointer-events-none"></div>
    <div class="fixed top-1/3 right-1/4 w-[600px] h-[600px] bg-indigo-500/5 rounded-full blur-[160px] -z-10 pointer-events-none"></div>

    <!-- Main Fluid Container (Elastic up to 4K / QHD) -->
    <div class="studio-container pt-6">

        <!-- Header Ribbon -->
        <header class="flex flex-col md:flex-row items-center justify-between p-6 mb-8 rounded-3xl glass-panel gap-4">
            <div class="flex items-center space-x-4">
                <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-cyan-600 to-indigo-700 flex items-center justify-center shadow-lg shadow-cyan-500/20 border border-cyan-400/30">
                    <i class="fa-solid fa-layer-group text-2xl text-white"></i>
                </div>
                <div>
                    <div class="flex items-center gap-2.5">
                        <h1 class="text-2xl font-extrabold tracking-tight font-heading">Yusuf Eminoğlu</h1>
                        <span class="text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-md bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">PORTFOLIO GOVERNANCE STUDIO</span>
                    </div>
                    <p class="text-xs text-slate-400 mt-0.5">QGIS Plugins Enterprise Analytics, Rating Forensic Surveillance & Strategic Growth Engine</p>
                </div>
            </div>

            <div class="flex flex-wrap items-center gap-3">
                <button onclick="openCommandPalette()" class="px-3.5 py-2 text-xs font-bold text-slate-300 hover:text-white bg-obsidian-800 hover:bg-obsidian-750 border border-white/10 rounded-xl flex items-center gap-2 transition-all font-mono" title="Quick Command Palette (Ctrl+K)">
                    <i class="fa-solid fa-terminal text-cyan-400"></i> Command <kbd>Ctrl+K</kbd>
                </button>

                <button onclick="openExecutiveStorytellingModal()" class="px-3.5 py-2 text-xs font-bold text-slate-300 hover:text-white bg-obsidian-800 hover:bg-obsidian-750 border border-white/10 rounded-xl flex items-center gap-1.5 transition-all" title="Generate State of Ecosystem Report & Community Kit">
                    <i class="fa-solid fa-newspaper text-emerald-400"></i> Reports & Announcements
                </button>

                <!-- Theme Switcher Button -->
                <button onclick="toggleTheme()" id="theme-toggle-btn" class="px-3.5 py-2 text-xs font-bold text-slate-300 hover:text-white bg-obsidian-800 hover:bg-obsidian-750 border border-white/10 rounded-xl flex items-center gap-1.5 transition-all" title="Toggle Theme (Obsidian / Alabaster) [T]">
                    <i class="fa-solid fa-circle-half-stroke text-amber-400"></i> <span id="theme-toggle-text">Alabaster Mode</span> <kbd>T</kbd>
                </button>

                <!-- 3-Way Benchmark Comparator -->
                <button onclick="openCompareModal()" class="px-3.5 py-2 text-xs font-bold text-slate-300 hover:text-white bg-obsidian-800 hover:bg-obsidian-750 border border-white/10 rounded-xl flex items-center gap-1.5 transition-all" title="Side-by-side 3-Plugin Benchmark">
                    <i class="fa-solid fa-code-compare text-indigo-400"></i> Compare
                </button>

                <!-- Dynamic Shields.io Badge Kit Generator -->
                <button onclick="openBadgeKitModal()" class="px-3.5 py-2 text-xs font-bold text-slate-300 hover:text-white bg-obsidian-800 hover:bg-obsidian-750 border border-white/10 rounded-xl flex items-center gap-1.5 transition-all" title="Dynamic Shields.io Badge Kit for GitHub READMEs">
                    <i class="fa-solid fa-certificate text-amber-400"></i> Badge Kit
                </button>

                <!-- Evidence JSON Download -->
                <button onclick="exportFullDossierJSON()" class="px-3.5 py-2 text-xs font-bold text-slate-300 hover:text-white bg-obsidian-800 hover:bg-obsidian-750 border border-white/10 rounded-xl flex items-center gap-1.5 transition-all" title="Download Machine-Readable Evidence Bundle">
                    <i class="fa-solid fa-file-code text-cyan-400"></i> Evidence JSON
                </button>

                <a href="https://plugins.qgis.org/plugins/author/Yusuf%20Eminoglu/" target="_blank" class="px-5 py-2.5 text-xs font-bold text-white rounded-xl btn-luxury flex items-center gap-2">
                    <i class="fa-solid fa-globe"></i> Official Hub Profile
                </a>
            </div>
        </header>

        <!-- Navigation Tabs with Shortcut Badges -->
        <div class="flex overflow-x-auto pb-1 mb-8 gap-2 border-b border-white/5 font-heading">
            <button onclick="switchTab('overview')" id="tab-btn-overview" class="px-5 py-3 text-sm font-bold border-b-2 border-cyan-400 text-cyan-400 flex items-center gap-2 whitespace-nowrap"><i class="fa-solid fa-chart-pie"></i> Executive Overview <kbd>1</kbd></button>
            <button onclick="switchTab('audit')" id="tab-btn-audit" class="px-5 py-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 whitespace-nowrap relative">
                <i class="fa-solid fa-shield-halved text-rose-400"></i> Rating Abuse & Surveillance <kbd>2</kbd>
                <span id="audit-alert-badge" class="ml-1.5 px-2 py-0.5 text-[10px] font-bold rounded-full bg-rose-500 text-white pulse-live"></span>
            </button>
            <button onclick="switchTab('carto')" id="tab-btn-carto" class="px-5 py-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 whitespace-nowrap"><i class="fa-solid fa-earth-americas text-emerald-400"></i> Geospatial Studio <kbd>3</kbd></button>
            <button onclick="switchTab('deepdive')" id="tab-btn-deepdive" class="px-5 py-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 whitespace-nowrap"><i class="fa-solid fa-cubes"></i> Plugin Explorer <kbd>4</kbd></button>
            <button onclick="switchTab('pipelines')" id="tab-btn-pipelines" class="px-5 py-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 whitespace-nowrap"><i class="fa-solid fa-diagram-project text-cyan-400"></i> Ecosystem Pipelines <kbd>7</kbd></button>
            <button onclick="switchTab('simulator')" id="tab-btn-simulator" class="px-5 py-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 whitespace-nowrap"><i class="fa-solid fa-wand-magic-sparkles"></i> Forecast Simulator <kbd>5</kbd></button>
            <button onclick="switchTab('table')" id="tab-btn-table" class="px-5 py-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 whitespace-nowrap"><i class="fa-solid fa-table"></i> Master Performance Table <kbd>6</kbd></button>
        </div>

        <!-- ============================================================= -->
        <!-- TAB 1: EXECUTIVE OVERVIEW -->
        <!-- ============================================================= -->
        <div id="tab-content-overview" class="tab-pane">
            <!-- KPI Cards Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8" id="kpi-grid">
                <!-- Dynamically generated by JS with kinetic counters -->
            </div>

            <!-- Community Impact & Engineering Valuation Ribbon -->
            <div class="grid grid-cols-1 sm:grid-cols-4 gap-4 mb-8" id="community-impact-ribbon">
                <div class="p-4 rounded-2xl bg-obsidian-950/80 border border-white/5 flex items-center justify-between">
                    <div>
                        <span class="text-[10px] text-slate-400 uppercase font-mono font-semibold block">Planning Hours Saved</span>
                        <span class="text-xl font-bold font-mono text-emerald-400" id="impact-hours-saved">34,800+ hrs</span>
                    </div>
                    <div class="w-8 h-8 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center text-sm border border-emerald-500/20">
                        <i class="fa-solid fa-clock-rotate-left"></i>
                    </div>
                </div>
                <div class="p-4 rounded-2xl bg-obsidian-950/80 border border-white/5 flex items-center justify-between">
                    <div>
                        <span class="text-[10px] text-slate-400 uppercase font-mono font-semibold block">Community Economic Value</span>
                        <span class="text-xl font-bold font-mono text-cyan-400" id="impact-econ-val">$1.74M+</span>
                    </div>
                    <div class="w-8 h-8 rounded-xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center text-sm border border-cyan-500/20">
                        <i class="fa-solid fa-hand-holding-dollar"></i>
                    </div>
                </div>
                <div class="p-4 rounded-2xl bg-obsidian-950/80 border border-white/5 flex items-center justify-between">
                    <div>
                        <span class="text-[10px] text-slate-400 uppercase font-mono font-semibold block">QGIS 4 & Qt6 Compatibility</span>
                        <span class="text-xl font-bold font-mono text-indigo-400">24 / 24 Ready</span>
                    </div>
                    <div class="w-8 h-8 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center text-sm border border-indigo-500/20">
                        <i class="fa-solid fa-cube"></i>
                    </div>
                </div>
                <div class="p-4 rounded-2xl bg-obsidian-950/80 border border-white/5 flex items-center justify-between">
                    <div>
                        <span class="text-[10px] text-slate-400 uppercase font-mono font-semibold block">Bandit Security Gate</span>
                        <span class="text-xl font-bold font-mono text-emerald-400">100% Passed</span>
                    </div>
                    <div class="w-8 h-8 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center text-sm border border-emerald-500/20">
                        <i class="fa-solid fa-shield-check"></i>
                    </div>
                </div>
            </div>

            <!-- Econometric Summary Ribbon -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8" id="econometric-ribbon">
                <div class="p-4 rounded-2xl bg-obsidian-950/80 border border-white/5 flex items-center justify-between">
                    <div>
                        <span class="text-[10px] text-slate-400 uppercase font-mono font-semibold block">Gini Inequality Coefficient</span>
                        <span class="text-lg font-bold font-mono text-white" id="eco-gini-val">0.4676 (Corrected)</span>
                    </div>
                    <span class="text-xs px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono font-bold">Optimal Pareto</span>
                </div>

                <div class="p-4 rounded-2xl bg-obsidian-950/80 border border-white/5 flex items-center justify-between">
                    <div>
                        <span class="text-[10px] text-slate-400 uppercase font-mono font-semibold block">Portfolio Entropy Diversity (N_eff)</span>
                        <span class="text-lg font-bold font-mono text-cyan-400" id="eco-entropy-val">14.8 Plugins</span>
                    </div>
                    <span class="text-xs px-2.5 py-1 rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-mono font-bold">High Multi-Pillar</span>
                </div>

                <div class="p-4 rounded-2xl bg-obsidian-950/80 border border-white/5 flex items-center justify-between">
                    <div>
                        <span class="text-[10px] text-slate-400 uppercase font-mono font-semibold block">Empirical Bayes Rating Prior (μ₀)</span>
                        <span class="text-lg font-bold font-mono text-amber-400" id="eco-prior-val">4.84 ★</span>
                    </div>
                    <span class="text-xs px-2.5 py-1 rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/20 font-mono font-bold">m = 5.0 Weight</span>
                </div>
            </div>

            <!-- Main Charts Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
                <div class="lg:col-span-2 p-6 rounded-3xl glass-panel">
                    <div class="flex items-center justify-between mb-6">
                        <h2 class="text-base font-bold tracking-tight"><i class="fa-solid fa-chart-bar text-cyan-400 mr-2"></i>Plugin Download Distribution</h2>
                        <span class="text-xs text-slate-400 font-mono">Lifetime Volume</span>
                    </div>
                    <div id="overview-bar-chart" class="w-full h-[400px]"></div>
                </div>

                <div class="p-6 rounded-3xl glass-panel flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-6">
                            <h2 class="text-base font-bold tracking-tight"><i class="fa-solid fa-diagram-project text-cyan-400 mr-2"></i>Ecosystem Suite Shares</h2>
                            <span class="text-xs text-slate-400 font-mono">Volume by Family</span>
                        </div>
                        <div id="overview-donut-chart" class="w-full h-72 flex items-center justify-center"></div>
                    </div>
                    <div class="mt-6 border-t border-white/5 pt-4 flex flex-col gap-2.5 text-xs text-slate-400">
                        <div class="flex justify-between">
                            <span>PlanX Suite Volume:</span>
                            <span class="font-bold font-mono" id="planx-share-text"></span>
                        </div>
                        <div class="flex justify-between">
                            <span>02 Suite Volume:</span>
                            <span class="font-bold font-mono" id="suite02-share-text"></span>
                        </div>
                        <div class="flex justify-between">
                            <span>Standalone Plugins Volume:</span>
                            <span class="font-bold font-mono" id="standalone-share-text"></span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- BCG Growth-Share Quadrant Scatter Matrix & Suite Radar -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                <div class="p-6 rounded-3xl glass-panel">
                    <div class="flex items-center justify-between mb-4">
                        <div>
                            <h2 class="text-base font-bold tracking-tight"><i class="fa-solid fa-shapes text-cyan-400 mr-2"></i>BCG Adoption & Velocity Matrix</h2>
                            <p class="text-xs text-slate-400">Downloads (X) vs Monthly Velocity (Y) across portfolio</p>
                        </div>
                        <span class="text-[10px] font-mono text-cyan-400 bg-cyan-500/10 px-2 py-0.5 rounded border border-cyan-500/20">Scatter Matrix</span>
                    </div>
                    <div id="bcg-scatter-chart" class="w-full h-80"></div>
                </div>

                <div class="p-6 rounded-3xl glass-panel">
                    <div class="flex items-center justify-between mb-4">
                        <div>
                            <h2 class="text-base font-bold tracking-tight"><i class="fa-solid fa-spider text-cyan-400 mr-2"></i>Ecosystem Benchmark Radar</h2>
                            <p class="text-xs text-slate-400">Multi-dimensional capability comparison between suites</p>
                        </div>
                        <span class="text-[10px] font-mono text-cyan-400 bg-cyan-500/10 px-2 py-0.5 rounded border border-cyan-500/20">6 Dimensions</span>
                    </div>
                    <div id="suite-radar-chart" class="w-full h-80"></div>
                </div>
            </div>

            <!-- Milestone Velocity & Probabilistic Calendar Forecast -->
            <div class="p-6 rounded-3xl glass-panel mb-8">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
                    <div>
                        <h2 class="text-base font-bold tracking-tight"><i class="fa-solid fa-bullseye text-cyan-400 mr-2"></i>Milestone Velocity & 95% Confidence Horizons</h2>
                        <p class="text-xs text-slate-400 mt-0.5">Empirical date projection and Gaussian confidence bounds toward next download tier</p>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-xs text-slate-400">Global Goal:</span>
                        <span class="text-sm font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1 rounded-xl font-mono">100,000 Total Downloads</span>
                    </div>
                </div>

                <div class="mb-8 bg-obsidian-900/80 p-5 rounded-2xl border border-white/5">
                    <div class="flex justify-between text-xs font-semibold mb-2">
                        <span>Portfolio Progress: <strong class="font-mono" id="milestone-total-downloads"></strong></span>
                        <span class="text-cyan-400 font-mono font-bold" id="portfolio-progress-percent"></span>
                    </div>
                    <div class="w-full bg-obsidian-800 rounded-full h-3 overflow-hidden">
                        <div class="bg-gradient-to-r from-cyan-500 to-indigo-500 h-3 rounded-full shadow-lg" id="portfolio-progress-bar" style="width: 0%"></div>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6" id="milestones-grid">
                    <!-- Top 3 closest to milestone -->
                </div>
            </div>
        </div>

        <!-- ============================================================= -->
        <!-- TAB 2: RATING ABUSE & SURVEILLANCE CENTER -->
        <!-- ============================================================= -->
        <div id="tab-content-audit" class="tab-pane hidden">
            <!-- Surveillance Banner -->
            <div class="p-6 rounded-3xl glass-panel mb-8 border-l-4 border-rose-500 relative overflow-hidden bg-gradient-to-r from-rose-950/40 via-obsidian-900/90 to-obsidian-900/90">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 rounded-2xl bg-rose-500/20 text-rose-400 flex items-center justify-center text-xl flex-shrink-0 border border-rose-500/30">
                            <i class="fa-solid fa-shield-virus pulse-live"></i>
                        </div>
                        <div>
                            <div class="flex items-center gap-2.5">
                                <h2 class="text-lg font-bold tracking-tight font-heading">Rating Abuse & Vote Bombing Surveillance Center</h2>
                                <span class="px-2.5 py-0.5 text-[10px] font-mono font-bold rounded-full bg-rose-500/20 text-rose-400 border border-rose-500/30">ACTIVE SURVEILLANCE</span>
                            </div>
                            <p class="text-xs text-slate-300 mt-1 max-w-3xl leading-relaxed">
                                Audits mathematical score increments ($Delta \\text{Score}$) against vote volume bursts ($Delta \\text{Votes}$). Computes Shannon Influx Entropy ($H$) and generates cryptographically signed multi-channel evidence dossiers and SQL remediation scripts.
                            </p>
                        </div>
                    </div>
                    <div class="flex flex-wrap gap-2 items-center">
                        <button onclick="openAllIncidentsModal()" class="px-4 py-2.5 text-xs font-bold text-white rounded-xl btn-danger flex items-center gap-2 whitespace-nowrap">
                            <i class="fa-solid fa-file-shield"></i> Export All Incident Dossiers
                        </button>
                    </div>
                </div>
            </div>

            <!-- Audit Metrics Cards -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8" id="audit-kpis">
                <!-- Dynamically generated by JS -->
            </div>

            <!-- Active Incident Drilldown -->
            <div class="p-6 rounded-3xl glass-panel mb-8">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-white/5 gap-3 mb-6">
                    <div>
                        <h2 class="text-base font-bold tracking-tight"><i class="fa-solid fa-list-check text-rose-400 mr-2"></i>Security & Rating Anomaly Incidents</h2>
                        <p class="text-xs text-slate-400 mt-0.5">Verified baseline reconciliation, implied influx entropy analysis, and rollback recovery</p>
                    </div>
                    <div class="flex gap-2">
                        <button onclick="filterAnomalyStatus('all')" id="audit-filter-all" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-cyan-600 text-white">All Plugins</button>
                        <button onclick="filterAnomalyStatus('critical')" id="audit-filter-crit" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-obsidian-800 text-slate-400 hover:text-white border border-white/5">Critical Raids Only</button>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6" id="anomaly-cards-container">
                    <!-- Dynamic Anomaly Incident Cards -->
                </div>
            </div>

            <!-- Time Machine Historical Delta Matrix -->
            <div class="p-6 rounded-3xl glass-panel mb-8">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-white/5 gap-3 mb-6">
                    <div>
                        <h2 class="text-base font-bold tracking-tight"><i class="fa-solid fa-clock-rotate-left text-cyan-400 mr-2"></i>Time-Machine Historical Delta Matrix</h2>
                        <p class="text-xs text-slate-400 mt-0.5">Compare any two historical snapshots to see exact rating shifts and volume gains</p>
                    </div>
                    <div class="flex flex-wrap items-center gap-3">
                        <select id="tm-select-snap-a" onchange="renderTimeMachineTable()" class="px-3 py-1.5 bg-obsidian-900 border border-white/10 rounded-xl text-xs font-mono"></select>
                        <span class="text-xs text-slate-500 font-mono">vs</span>
                        <select id="tm-select-snap-b" onchange="renderTimeMachineTable()" class="px-3 py-1.5 bg-obsidian-900 border border-white/10 rounded-xl text-xs font-mono"></select>
                    </div>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs" id="tm-table">
                        <thead class="bg-obsidian-900/90 text-slate-400 uppercase text-[10px] tracking-wider border-b border-white/10 font-heading">
                            <tr>
                                <th class="py-3 px-4 font-bold">Plugin</th>
                                <th class="py-3 px-4 font-bold text-center">Snapshot A (Votes / Rating)</th>
                                <th class="py-3 px-4 font-bold text-center">Snapshot B (Votes / Rating)</th>
                                <th class="py-3 px-4 font-bold text-right">Δ Votes</th>
                                <th class="py-3 px-4 font-bold text-right">Δ Rating</th>
                                <th class="py-3 px-4 font-bold text-center">Trend Status</th>
                            </tr>
                        </thead>
                        <tbody id="tm-table-body" class="divide-y divide-white/5 font-mono">
                            <!-- Filled dynamically -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Interactive Rating History Time-Series Chart -->
            <div class="p-6 rounded-3xl glass-panel mb-8">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between mb-6 gap-4">
                    <div>
                        <h2 class="text-base font-bold tracking-tight"><i class="fa-solid fa-chart-line text-cyan-400 mr-2"></i>Plugin Rating & Vote Trajectory Over Time</h2>
                        <p class="text-xs text-slate-400 mt-0.5">Track historical score drops and volume surges across recorded snapshots</p>
                    </div>
                    <div class="w-full sm:w-80">
                        <select id="audit-chart-plugin-select" onchange="renderAuditHistoryChart()" class="w-full px-3.5 py-2.5 bg-obsidian-900 border border-white/10 rounded-xl text-xs focus:outline-none focus:border-cyan-400 font-mono">
                            <!-- Filled dynamically -->
                        </select>
                    </div>
                </div>
                <div id="audit-history-chart" class="w-full h-80"></div>
            </div>
        </div>

        <!-- ============================================================= -->
        <!-- TAB 3: GEOSPATIAL & CARTOGRAPHIC STUDIO -->
        <!-- ============================================================= -->
        <div id="tab-content-carto" class="tab-pane hidden">
            <!-- Header with Spatial Intelligence Bar -->
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
                <div>
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 text-lg">
                            <i class="fa-solid fa-earth-americas"></i>
                        </div>
                        <div>
                            <h2 class="text-xl font-bold font-heading tracking-tight flex items-center gap-2">
                                Geospatial Adoption & Macro-Regional Governance Studio
                            </h2>
                            <p class="text-xs text-slate-400 font-mono">
                                Vector Choropleth Heatmap • Macro-Regional Penetration • Suite Affinity Matrix (Location Quotient LQ)
                            </p>
                        </div>
                    </div>
                </div>

                <div class="flex flex-wrap items-center gap-3">
                    <div class="relative w-full sm:w-56">
                        <i class="fa-solid fa-magnifying-glass absolute left-3 top-2.5 text-slate-500 text-xs"></i>
                        <input type="text" id="map-country-search" oninput="handleMapCountrySearch(this.value)" placeholder="Search country (e.g. Germany, USA)..." class="w-full pl-8 pr-3 py-1.5 bg-obsidian-950/80 border border-white/10 rounded-xl text-xs focus:outline-none focus:border-cyan-400 font-mono text-white placeholder-slate-500 transition-colors">
                    </div>
                    <div class="bg-obsidian-950/80 p-1 rounded-2xl border border-white/5 flex items-center gap-1 font-mono text-xs">
                        <button onclick="setMapFilter('all')" id="map-btn-all" class="px-3 py-1 rounded-xl bg-cyan-500/20 text-cyan-400 font-bold border border-cyan-500/30 transition-all">
                            Global
                        </button>
                        <button onclick="setMapFilter('WEU')" id="map-btn-WEU" class="px-3 py-1 rounded-xl text-slate-400 hover:text-white transition-all">
                            Europe
                        </button>
                        <button onclick="setMapFilter('NAM')" id="map-btn-NAM" class="px-3 py-1 rounded-xl text-slate-400 hover:text-white transition-all">
                            N. America
                        </button>
                        <button onclick="setMapFilter('LAM')" id="map-btn-LAM" class="px-3 py-1 rounded-xl text-slate-400 hover:text-white transition-all">
                            LatAm
                        </button>
                        <button onclick="setMapFilter('EME')" id="map-btn-EME" class="px-3 py-1 rounded-xl text-slate-400 hover:text-white transition-all">
                            East Europe/ME
                        </button>
                        <button onclick="setMapFilter('APAC')" id="map-btn-APAC" class="px-3 py-1 rounded-xl text-slate-400 hover:text-white transition-all">
                            APAC
                        </button>
                    </div>
                    <button onclick="resetMapZoom()" class="p-2 rounded-xl bg-obsidian-950/80 border border-white/5 text-slate-400 hover:text-cyan-400 text-xs font-mono transition-colors" title="Reset Map View">
                        <i class="fa-solid fa-compress"></i>
                    </button>
                </div>
            </div>

            <!-- Tier 1: Macro-Region Strategic Performance Cards Deck -->
            <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-6" id="macro-regions-deck">
                <!-- Populated dynamically via JS -->
            </div>

            <!-- Tier 2: Interactive Vector SVG World Choropleth Heatmap & Spatial HUD -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-6">
                <!-- Main World Map Canvas (8 Columns) -->
                <div class="lg:col-span-8 p-6 rounded-3xl glass-panel relative overflow-hidden flex flex-col justify-between">
                    <div class="flex items-center justify-between mb-2">
                        <div class="flex items-center gap-2">
                            <span class="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-ping"></span>
                            <h3 class="text-sm font-bold font-heading tracking-tight">Global Country Adoption Heatmap</h3>
                        </div>
                        <div class="flex items-center gap-2 text-[10px] font-mono text-slate-400">
                            <span>Adoption Tier:</span>
                            <div class="flex items-center gap-1">
                                <span class="w-3 h-2 rounded-sm bg-sky-950 border border-sky-800" title="Low Volume (< 2k)"></span>
                                <span class="w-3 h-2 rounded-sm bg-sky-800" title="Moderate (2k-5k)"></span>
                                <span class="w-3 h-2 rounded-sm bg-sky-600" title="Established (5k-10k)"></span>
                                <span class="w-3 h-2 rounded-sm bg-cyan-500" title="Core Tier (10k-20k)"></span>
                                <span class="w-3 h-2 rounded-sm bg-cyan-300" title="Anchor Tier (> 20k)"></span>
                            </div>
                            <span class="text-cyan-400 font-bold ml-1">High Intensity</span>
                        </div>
                    </div>

                    <!-- Zero-Dependency SVG World Map Container -->
                    <div class="relative w-full aspect-[2/1] bg-obsidian-950/90 rounded-2xl border border-white/5 overflow-hidden flex items-center justify-center" id="world-map-wrapper">
                        <svg id="svg-world-map" viewBox="0 0 960 500" class="w-full h-full select-none cursor-grab active:cursor-grabbing transition-transform duration-300 ease-out">
                            <defs>
                                <pattern id="graticule-pattern" width="80" height="80" patternUnits="userSpaceOnUse">
                                    <path d="M 80 0 L 0 0 0 80" fill="none" stroke="rgba(255, 255, 255, 0.03)" stroke-width="0.75"/>
                                </pattern>
                                <filter id="radar-glow" x="-50%" y="-50%" width="200%" height="200%">
                                    <feGaussianBlur stdDeviation="3" result="blur" />
                                    <feMerge>
                                        <feMergeNode in="blur" />
                                        <feMergeNode in="SourceGraphic" />
                                    </feMerge>
                                </filter>
                            </defs>

                            <rect width="960" height="500" fill="url(#graticule-pattern)"/>
                            <line x1="0" y1="250" x2="960" y2="250" stroke="rgba(56, 189, 248, 0.15)" stroke-width="1" stroke-dasharray="4,4"/>
                            <line x1="480" y1="0" x2="480" y2="500" stroke="rgba(56, 189, 248, 0.15)" stroke-width="1" stroke-dasharray="4,4"/>

                            <!-- Real-World Vector Country Polygons Layer (GeoJSON Source) -->
                            <g id="svg-countries-layer" class="transition-all duration-300">
##WORLD_SVG_LAYER##
                            </g>

                            <!-- Radar Pulse Hubs Layer -->
                            <g id="svg-nodes-layer"></g>
                        </svg>

                        <!-- Floating HUD Tooltip -->
                        <div id="map-hud-tooltip" class="absolute pointer-events-none opacity-0 transition-opacity duration-200 bg-obsidian-950/95 border border-cyan-500/40 p-3 rounded-2xl shadow-2xl backdrop-blur-md z-30 min-w-[200px]"></div>
                    </div>

                    <div class="mt-4 flex items-center justify-between text-xs text-slate-400 font-mono">
                        <span id="map-active-status"><i class="fa-solid fa-crosshairs text-cyan-400 mr-1.5"></i>Hover country or pulse node to inspect telemetry</span>
                        <span class="text-[10px] text-slate-500">Equirectangular Standard Baseline • 0 Dependencies</span>
                    </div>
                </div>

                <!-- Country Drilldown & Top Plugins Leaderboard (4 Columns) -->
                <div class="lg:col-span-4 flex flex-col gap-4">
                    <div class="p-6 rounded-3xl glass-panel flex-1 flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between mb-3">
                                <div class="flex items-center gap-2">
                                    <span id="drilldown-flag" class="text-2xl">🇺🇸</span>
                                    <div>
                                        <h3 id="drilldown-country-name" class="text-base font-bold font-heading">United States</h3>
                                        <span id="drilldown-region-badge" class="text-[10px] font-mono text-cyan-400">North America • Rank #1</span>
                                    </div>
                                </div>
                                <div class="text-right">
                                    <div id="drilldown-downloads" class="text-lg font-bold font-mono text-white">--</div>
                                    <div id="drilldown-pct" class="text-[10px] text-slate-400 font-mono">-- of Global</div>
                                </div>
                            </div>

                            <div class="mb-4">
                                <div class="flex justify-between text-[10px] font-mono text-slate-400 mb-1">
                                    <span>Dominant Suite: <strong id="drilldown-dom-suite" class="text-cyan-400">--</strong></span>
                                </div>
                            </div>

                            <div class="space-y-2" id="drilldown-plugins-list">
                                <!-- Populated dynamically -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tier 3: Suite Geographic Affinity Matrix & Location Quotient (LQ) Grid -->
            <div class="p-6 rounded-3xl glass-panel">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
                    <div>
                        <h3 class="text-base font-bold font-heading flex items-center gap-2">
                            <i class="fa-solid fa-cubes-stacked text-cyan-400"></i>
                            Suite Geographic Affinity & Market Specialization Matrix
                        </h3>
                        <p class="text-xs text-slate-400 font-mono">
                            Cross-tabulated Location Quotient ($LQ$) indicating regional adoption over/under-indexing
                        </p>
                    </div>
                    <div class="flex items-center gap-3 text-xs font-mono">
                        <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Over-Index (LQ &ge; 1.15)</span>
                        <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-cyan-500"></span> Balanced (0.85–1.15)</span>
                        <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span> Frontier (&lt; 0.85)</span>
                    </div>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left font-mono text-xs border-collapse" id="suite-affinity-table">
                        <thead>
                            <tr class="border-b border-white/10 text-slate-400">
                                <th class="py-3 px-4 font-heading font-semibold">Plugin Suite</th>
                                <th class="py-3 px-4 text-right">Global Volume</th>
                                <th class="py-3 px-4 text-center">Western Europe</th>
                                <th class="py-3 px-4 text-center">North America</th>
                                <th class="py-3 px-4 text-center">Latin America</th>
                                <th class="py-3 px-4 text-center">East Europe & ME</th>
                                <th class="py-3 px-4 text-center">Asia-Pacific</th>
                            </tr>
                        </thead>
                        <tbody id="suite-affinity-tbody" class="divide-y divide-white/5">
                            <!-- Populated dynamically via JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- ============================================================= -->
        <!-- TAB 4: PLUGIN EXPLORER -->
        <!-- ============================================================= -->
        <div id="tab-content-deepdive" class="tab-pane hidden">
            <!-- Search & Multi-Tag Matrix Ribbon -->
            <div class="p-5 rounded-3xl glass-panel mb-6 space-y-4">
                <div class="flex flex-col md:flex-row items-center justify-between gap-4">
                    <div class="relative w-full md:max-w-xs">
                        <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-500"><i class="fa-solid fa-magnifying-glass text-xs"></i></span>
                        <input type="text" id="card-search-input" onkeyup="filterCards()" placeholder="Search plugin name, tags, quadrant (Press '/' to focus)..." class="w-full pl-9 pr-4 py-2.5 text-xs bg-obsidian-900 border border-white/10 rounded-xl placeholder-slate-500 focus:outline-none focus:border-cyan-400">
                    </div>
                    <div class="flex flex-wrap gap-2 w-full md:w-auto overflow-x-auto font-heading">
                        <button onclick="filterCardsCategory('All')" class="px-4 py-2 rounded-xl text-xs font-bold bg-cyan-600 text-white whitespace-nowrap" id="btn-cat-all">All Suites</button>
                        <button onclick="filterCardsCategory('PlanX Suite')" class="px-4 py-2 rounded-xl text-xs font-bold bg-obsidian-900 text-slate-400 hover:text-white border border-white/5 whitespace-nowrap" id="btn-cat-planx">PlanX Suite</button>
                        <button onclick="filterCardsCategory('02 Suite')" class="px-4 py-2 rounded-xl text-xs font-bold bg-obsidian-900 text-slate-400 hover:text-white border border-white/5 whitespace-nowrap" id="btn-cat-02">02 Suite</button>
                        <button onclick="filterCardsCategory('Standalone Plugins')" class="px-4 py-2 rounded-xl text-xs font-bold bg-obsidian-900 text-slate-400 hover:text-white border border-white/5 whitespace-nowrap" id="btn-cat-standalone">Standalone</button>
                    </div>
                </div>

                <!-- Multi-Tag Filter Chips -->
                <div class="pt-3 border-t border-white/5 flex items-center justify-between flex-wrap gap-2">
                    <div class="flex items-center gap-1.5 flex-wrap" id="tag-filter-chips">
                        <span class="text-[11px] text-slate-500 font-mono font-semibold mr-1">Tags:</span>
                    </div>
                    <span class="text-[10px] text-slate-400 font-mono" id="matching-plugins-count">24 plugins matching</span>
                </div>
            </div>

            <!-- Cards Container -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" id="plugin-cards-container">
                <!-- Dynamically generated by JS -->
            </div>
        </div>

        <!-- ============================================================= -->
        <!-- TAB 5: FORECAST SIMULATOR -->
        <!-- ============================================================= -->
        <div id="tab-content-simulator" class="tab-pane hidden">
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- Simulator Controls -->
                <div class="p-6 rounded-3xl glass-panel flex flex-col justify-between">
                    <div>
                        <div class="flex items-center space-x-2 mb-4">
                            <span class="p-2 bg-cyan-500/10 text-cyan-400 rounded-lg text-xs border border-cyan-500/20"><i class="fa-solid fa-sliders"></i></span>
                            <h2 class="text-base font-bold tracking-tight">Growth Model Controls</h2>
                        </div>

                        <p class="text-xs text-slate-300 leading-relaxed mb-6">
                            Simulate future adoption and multi-scenario confidence cones with kinetic acceleration derivatives.
                        </p>

                        <!-- Select Simulator Target -->
                        <div class="mb-4">
                            <label class="block text-xs font-semibold text-slate-400 mb-2">Target Scope</label>
                            <select id="sim-target-plugin" onchange="runSimulation()" class="w-full px-4 py-2.5 bg-obsidian-900 border border-white/10 rounded-xl text-xs focus:outline-none focus:border-cyan-400 font-mono">
                                <option value="all">Entire Portfolio (Combined)</option>
                            </select>
                        </div>

                        <!-- Target Date Picker -->
                        <div class="mb-4">
                            <label class="block text-xs font-semibold text-slate-400 mb-2">Projection Horizon Date</label>
                            <input type="date" id="sim-target-date" onchange="runSimulation()" value="2027-01-01" class="w-full px-4 py-2.5 bg-obsidian-900 border border-white/10 rounded-xl text-xs focus:outline-none focus:border-cyan-400 font-mono">
                        </div>

                        <!-- Growth Model Selector -->
                        <div class="mb-4">
                            <label class="block text-xs font-semibold text-slate-400 mb-2">Velocity Model Preset</label>
                            <select id="sim-growth-preset" onchange="applySimPreset()" class="w-full px-4 py-2.5 bg-obsidian-900 border border-white/10 rounded-xl text-xs focus:outline-none focus:border-cyan-400 font-mono">
                                <option value="balanced">Balanced Active Run-Rate</option>
                                <option value="conservative">Conservative Historical Floor</option>
                                <option value="optimistic">High-Adoption Launch Momentum</option>
                                <option value="custom">Custom Velocity Rate (Slider)</option>
                            </select>
                        </div>

                        <!-- Custom Growth Slider -->
                        <div class="mb-6" id="custom-slider-container" style="display: none;">
                            <div class="flex justify-between text-xs font-semibold text-slate-400 mb-2 font-mono">
                                <span>Custom Monthly Velocity:</span>
                                <span class="text-cyan-400 font-bold" id="custom-slider-val">10,000/mo</span>
                            </div>
                            <input type="range" id="sim-custom-speed" oninput="updateSliderVal()" min="100" max="50000" step="100" value="10000" class="w-full accent-cyan-500">
                        </div>

                        <!-- Output Scorecard -->
                        <div class="bg-obsidian-950/80 rounded-2xl p-6 border border-white/5 flex flex-col items-center justify-center text-center">
                            <p class="text-xs text-slate-400 uppercase tracking-widest font-mono font-bold">Projected Cumulative Volume</p>
                            <span class="text-4xl font-extrabold mt-2 tracking-tight font-mono" id="sim-output-val">--</span>
                            <span class="text-xs font-medium text-emerald-400 mt-2 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-1 rounded-full font-mono" id="sim-output-growth">--</span>
                        </div>
                    </div>
                </div>

                <!-- Simulation Output Chart -->
                <div class="lg:col-span-2 p-6 rounded-3xl glass-panel">
                    <div class="flex items-center justify-between mb-4">
                        <div>
                            <h2 class="text-base font-bold tracking-tight"><i class="fa-solid fa-chart-line text-cyan-400 mr-2"></i>Multi-Scenario Trajectory Cone</h2>
                            <p class="text-xs text-slate-400" id="sim-chart-sub">Bullish, Expected, and Conservative adoption bands</p>
                        </div>
                        <span class="text-xs font-mono text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-1 rounded-xl">96% Milestone Probability</span>
                    </div>
                    <div id="sim-line-chart" class="w-full h-80"></div>
                </div>
            </div>
        </div>

        <!-- ============================================================= -->
        <!-- TAB 6: MASTER DATA TABLE -->
        <!-- ============================================================= -->
        <div id="tab-content-table" class="tab-pane hidden">
            <div class="p-6 rounded-3xl glass-panel overflow-hidden">
                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between pb-6 border-b border-white/5 gap-4">
                    <div>
                        <h2 class="text-base font-bold tracking-tight"><i class="fa-solid fa-table-list text-cyan-400 mr-2"></i>Master Performance & Governance Data Table</h2>
                        <p class="text-xs text-slate-400 mt-0.5">Multi-column telemetry grid with live filtering, Bayesian reliability, and instant CSV export</p>
                    </div>
                    <div class="flex flex-wrap items-center gap-3">
                        <button onclick="window.print()" class="px-4 py-2 bg-obsidian-800 hover:bg-obsidian-750 text-slate-300 hover:text-white border border-white/10 rounded-xl text-xs font-bold flex items-center gap-2 transition-all">
                            <i class="fa-solid fa-print text-cyan-400"></i> Print / PDF
                        </button>
                        <button onclick="exportToCSV()" class="px-4 py-2 bg-obsidian-800 hover:bg-obsidian-750 text-slate-300 hover:text-white border border-white/10 rounded-xl text-xs font-bold flex items-center gap-2 transition-all">
                            <i class="fa-solid fa-file-csv text-emerald-400 text-sm"></i> Export CSV
                        </button>
                        <div class="relative max-w-xs">
                            <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-500"><i class="fa-solid fa-magnifying-glass text-xs"></i></span>
                            <input type="text" id="table-search-input" onkeyup="filterTableData()" placeholder="Filter by plugin or suite..." class="w-full pl-9 pr-4 py-2 text-xs bg-obsidian-900 border border-white/10 rounded-xl placeholder-slate-500 focus:outline-none focus:border-cyan-400">
                        </div>
                    </div>
                </div>

                <!-- Quick Filter Presets -->
                <div class="flex flex-wrap gap-2 pt-4 pb-2 border-b border-white/5 font-heading">
                    <button onclick="applyTablePreset('all')" id="tbl-preset-all" class="px-3 py-1 rounded-xl text-xs font-bold bg-cyan-600 text-white">All (24)</button>
                    <button onclick="applyTablePreset('top5')" id="tbl-preset-top5" class="px-3 py-1 rounded-xl text-xs font-bold bg-obsidian-900 text-slate-400 hover:text-white border border-white/5">🔥 Top 5 Volume</button>
                    <button onclick="applyTablePreset('highrated')" id="tbl-preset-rated" class="px-3 py-1 rounded-xl text-xs font-bold bg-obsidian-900 text-slate-400 hover:text-white border border-white/5">⭐ High Rated (≥4.5★)</button>
                    <button onclick="applyTablePreset('velocity')" id="tbl-preset-vel" class="px-3 py-1 rounded-xl text-xs font-bold bg-obsidian-900 text-slate-400 hover:text-white border border-white/5">🚀 High Velocity (≥500/mo)</button>
                    <button onclick="applyTablePreset('alerts')" id="tbl-preset-alerts" class="px-3 py-1 rounded-xl text-xs font-bold bg-obsidian-900 text-rose-400 hover:text-white border border-rose-500/20">🚨 Needs Attention</button>
                </div>

                <div class="overflow-x-auto mt-4">
                    <table class="w-full text-left text-xs" id="main-data-table">
                        <thead class="bg-obsidian-900/90 text-slate-400 uppercase text-[10px] tracking-wider border-b border-white/10 font-heading">
                            <tr>
                                <th class="py-3.5 px-4 font-bold cursor-pointer hover:text-white transition-colors" onclick="sortTable(0)">Plugin Name <i class="fa-solid fa-sort ml-1"></i></th>
                                <th class="py-3.5 px-4 font-bold text-center cursor-pointer hover:text-white transition-colors" onclick="sortTable(1)">Suite <i class="fa-solid fa-sort ml-1"></i></th>
                                <th class="py-3.5 px-4 font-bold text-center cursor-pointer hover:text-white transition-colors" onclick="sortTable(2)">Published <i class="fa-solid fa-sort ml-1"></i></th>
                                <th class="py-3.5 px-4 font-bold text-right cursor-pointer hover:text-white transition-colors" onclick="sortTable(4)">Downloads <i class="fa-solid fa-sort ml-1"></i></th>
                                <th class="py-3.5 px-4 font-bold text-right cursor-pointer hover:text-white transition-colors" onclick="sortTable(5)">Monthly Velocity <i class="fa-solid fa-sort ml-1"></i></th>
                                <th class="py-3.5 px-4 font-bold text-center">Bayesian ★</th>
                                <th class="py-3.5 px-4 font-bold text-center">Kinetic Regime</th>
                                <th class="py-3.5 px-4 font-bold text-center">Security Status</th>
                            </tr>
                        </thead>
                        <tbody id="tab-table-body" class="divide-y divide-white/5">
                            <!-- Filled dynamically by JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- ============================================================= -->
        <!-- TAB 7: ECOSYSTEM PIPELINES & WORKFLOW GRAPH -->
        <!-- ============================================================= -->
        <div id="tab-content-pipelines" class="tab-pane hidden">
            <!-- Header Banner -->
            <div class="p-6 rounded-3xl glass-panel mb-8 border-l-4 border-cyan-500 relative overflow-hidden bg-gradient-to-r from-cyan-950/40 via-obsidian-900/90 to-obsidian-900/90">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 rounded-2xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center text-xl flex-shrink-0 border border-cyan-500/30">
                            <i class="fa-solid fa-diagram-project"></i>
                        </div>
                        <div>
                            <div class="flex items-center gap-2.5">
                                <h2 class="text-lg font-bold tracking-tight font-heading">QGIS Plugin Ecosystem Pipelines & Synergies</h2>
                                <span class="px-2.5 py-0.5 text-[10px] font-mono font-bold rounded-full bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">5 MACRO-WORKFLOWS</span>
                            </div>
                            <p class="text-xs text-slate-300 mt-1 max-w-3xl leading-relaxed">
                                Professional multi-plugin pipeline architecture connecting data ingestion, spatial statistics, statutory master planning, 3D simulation, and publication cartography.
                            </p>
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        <button onclick="copyCurrentPipelineRecipe()" class="px-4 py-2 text-xs font-bold text-white rounded-xl btn-luxury flex items-center gap-2 whitespace-nowrap">
                            <i class="fa-solid fa-code"></i> Copy Pipeline Recipe (JSON)
                        </button>
                    </div>
                </div>
            </div>

            <!-- Pipeline Selection Cards -->
            <div class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8" id="pipeline-selector-deck">
                <!-- Dynamically populated by JS -->
            </div>

            <!-- Active Pipeline Interactive Flow Canvas & Step Dossier -->
            <div class="p-6 rounded-3xl glass-panel mb-8" id="active-pipeline-container">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-white/5 gap-3 mb-6">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-xl flex items-center justify-center text-lg font-bold bg-cyan-500/20 text-cyan-400 border border-cyan-500/30" id="pipe-active-icon-bg">
                            <i class="fa-solid fa-network-wired" id="pipe-active-icon"></i>
                        </div>
                        <div>
                            <h3 class="text-base font-bold font-heading text-white" id="pipe-active-title">Urban Spatial Analytics & Network Morphology Pipeline</h3>
                            <p class="text-xs text-slate-400 font-mono" id="pipe-active-subtitle">Autonomous workflow from OSM raw vector data to NetCDF spatio-temporal cube</p>
                        </div>
                    </div>
                    <div class="flex items-center gap-3 font-mono text-xs">
                        <span class="px-3 py-1 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-bold" id="pipe-active-time">~4.5 mins / city</span>
                        <span class="px-3 py-1 rounded-xl bg-white/5 text-slate-300 border border-white/10 font-bold" id="pipe-active-steps-count">5 Modular Steps</span>
                    </div>
                </div>

                <!-- Animated Interactive Node Flowchart -->
                <div class="grid grid-cols-1 md:grid-cols-5 gap-4 my-6 relative" id="pipe-nodes-flow">
                    <!-- Populated dynamically via JS -->
                </div>

                <!-- Step-by-Step Technical Execution Dossier -->
                <div class="mt-8 pt-6 border-t border-white/5">
                    <h4 class="text-xs uppercase tracking-wider font-mono font-bold text-slate-400 mb-4">Detailed Step Execution Protocol</h4>
                    <div class="space-y-3" id="pipe-steps-dossier">
                        <!-- Populated dynamically via JS -->
                    </div>
                </div>
            </div>
        </div>

    </div>

    <!-- ============================================================= -->
    <!-- DYNAMIC SHIELDS.IO BADGE KIT MODAL -->
    <!-- ============================================================= -->
    <div id="badge-kit-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md hidden p-4">
        <div class="bg-obsidian-900 border border-white/10 rounded-3xl max-w-4xl w-full p-6 max-h-[92vh] flex flex-col justify-between shadow-2xl overflow-hidden">
            <div class="flex items-center justify-between pb-4 border-b border-white/10">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center text-lg border border-amber-500/30">
                        <i class="fa-solid fa-certificate"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold tracking-tight">Dynamic Shields.io Badge Generator</h3>
                        <p class="text-xs text-slate-400">Embed live official download counters and quality badges in GitHub READMEs</p>
                    </div>
                </div>
                <button onclick="closeBadgeKitModal()" class="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-obsidian-800 transition-colors">
                    <i class="fa-solid fa-xmark text-lg"></i>
                </button>
            </div>

            <div class="my-4 space-y-4 overflow-y-auto max-h-[55vh] pr-2">
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-2">Select Plugin</label>
                    <select id="badge-kit-plugin-select" onchange="updateBadgeKitPreview()" class="w-full px-4 py-2.5 bg-obsidian-950 border border-white/10 rounded-xl text-xs focus:outline-none focus:border-cyan-400 font-mono">
                        <!-- Populated dynamically -->
                    </select>
                </div>

                <!-- Live Badge Previews -->
                <div class="p-4 rounded-2xl bg-obsidian-950 border border-white/5 flex flex-wrap gap-3 items-center" id="badge-preview-container">
                    <!-- Images rendered by JS -->
                </div>

                <!-- Generated Markdown Snippet -->
                <div>
                    <div class="flex items-center justify-between mb-1.5">
                        <label class="text-xs font-semibold text-slate-400">GitHub Markdown Snippet</label>
                        <button onclick="copyBadgeSnippet('markdown')" class="text-xs text-cyan-400 hover:text-cyan-300 font-mono"><i class="fa-solid fa-copy mr-1"></i> Copy Markdown</button>
                    </div>
                    <textarea id="badge-code-markdown" readonly rows="3" class="w-full p-3 bg-obsidian-950 border border-white/10 rounded-xl text-xs font-mono text-slate-300 focus:outline-none select-all"></textarea>
                </div>

                <!-- Generated HTML Snippet -->
                <div>
                    <div class="flex items-center justify-between mb-1.5">
                        <label class="text-xs font-semibold text-slate-400">HTML Snippet</label>
                        <button onclick="copyBadgeSnippet('html')" class="text-xs text-cyan-400 hover:text-cyan-300 font-mono"><i class="fa-solid fa-copy mr-1"></i> Copy HTML</button>
                    </div>
                    <textarea id="badge-code-html" readonly rows="3" class="w-full p-3 bg-obsidian-950 border border-white/10 rounded-xl text-xs font-mono text-slate-300 focus:outline-none select-all"></textarea>
                </div>
            </div>

            <div class="pt-4 border-t border-white/10 flex justify-between items-center text-xs">
                <span class="text-slate-500 font-mono">Auto-refreshed via shields.io dynamic SVG</span>
                <button onclick="closeBadgeKitModal()" class="px-5 py-2 rounded-xl bg-obsidian-800 hover:bg-obsidian-750 text-white font-bold transition-all">Close</button>
            </div>
        </div>
    </div>

    <!-- ============================================================= -->
    <!-- COMMAND PALETTE MODAL (Ctrl+K) -->
    <!-- ============================================================= -->
    <div id="command-palette-modal" class="fixed inset-0 z-50 flex items-start justify-center pt-20 bg-black/80 backdrop-blur-md hidden p-4">
        <div class="bg-obsidian-900 border border-white/10 rounded-3xl max-w-xl w-full p-4 shadow-2xl overflow-hidden animate-in fade-in duration-200">
            <div class="relative mb-3">
                <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-500"><i class="fa-solid fa-terminal text-sm"></i></span>
                <input type="text" id="palette-search-input" onkeyup="filterCommandPalette()" placeholder="Type a command, tab, or plugin name..." class="w-full pl-10 pr-4 py-3 bg-obsidian-950 border border-white/10 rounded-2xl text-xs focus:outline-none focus:border-cyan-400 font-mono">
            </div>
            <div class="max-h-72 overflow-y-auto space-y-1 pr-1 font-mono text-xs" id="palette-results-list"></div>
            <div class="pt-3 border-t border-white/10 flex justify-between items-center text-[10px] text-slate-500">
                <span>Navigate with <kbd>↑</kbd> <kbd>↓</kbd> <kbd>Enter</kbd></span>
                <span>Press <kbd>Esc</kbd> to close</span>
            </div>
        </div>
    </div>

    <!-- ============================================================= -->
    <!-- REPORTS & SOCIAL MEDIA ANNOUNCEMENT KIT MODAL -->
    <!-- ============================================================= -->
    <div id="storytelling-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md hidden p-4">
        <div class="bg-obsidian-900 border border-white/10 rounded-3xl max-w-4xl w-full p-6 max-h-[92vh] flex flex-col justify-between shadow-2xl overflow-hidden">
            <div class="flex items-center justify-between pb-4 border-b border-white/10">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-lg border border-emerald-500/30">
                        <i class="fa-solid fa-bullhorn"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold tracking-tight">Executive Storytelling & Community Announcement Kit</h3>
                        <p class="text-xs text-slate-400">Publication-ready ecosystem reports, LinkedIn digests, X threads, and Reddit posts</p>
                    </div>
                </div>
                <button onclick="closeExecutiveStorytellingModal()" class="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-obsidian-800 transition-colors">
                    <i class="fa-solid fa-xmark text-lg"></i>
                </button>
            </div>

            <!-- Report Format Selector Tabs -->
            <div class="flex gap-2 my-3 font-heading overflow-x-auto pb-1">
                <button onclick="setStorytellingFormat('ecosystem')" id="s-btn-eco" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-cyan-600 text-white whitespace-nowrap"><i class="fa-solid fa-file-lines mr-1"></i> State of Ecosystem</button>
                <button onclick="setStorytellingFormat('linkedin')" id="s-btn-li" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-obsidian-800 text-slate-400 hover:text-white border border-white/5 whitespace-nowrap"><i class="fa-brands fa-linkedin mr-1"></i> LinkedIn Post</button>
                <button onclick="setStorytellingFormat('twitter')" id="s-btn-tw" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-obsidian-800 text-slate-400 hover:text-white border border-white/5 whitespace-nowrap"><i class="fa-brands fa-x-twitter mr-1"></i> X / Twitter Thread</button>
                <button onclick="setStorytellingFormat('reddit')" id="s-btn-rd" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-obsidian-800 text-slate-400 hover:text-white border border-white/5 whitespace-nowrap"><i class="fa-brands fa-reddit-alien mr-1"></i> Reddit r/QGIS</button>
            </div>

            <div class="my-2 overflow-y-auto max-h-[52vh] pr-2">
                <pre class="bg-obsidian-950 p-4 rounded-2xl border border-white/5 text-xs font-mono text-slate-300 overflow-x-auto whitespace-pre-wrap leading-relaxed" id="storytelling-content-area"></pre>
            </div>

            <div class="pt-4 border-t border-white/10 flex justify-between items-center text-xs">
                <button onclick="copyStorytellingText()" class="px-4 py-2 rounded-xl text-xs font-bold btn-luxury text-white flex items-center gap-1.5">
                    <i class="fa-solid fa-copy"></i> <span id="copy-story-btn-text">Copy Selected Format</span>
                </button>
                <button onclick="closeExecutiveStorytellingModal()" class="px-5 py-2 rounded-xl bg-obsidian-800 hover:bg-obsidian-750 text-white font-bold transition-all">Close</button>
            </div>
        </div>
    </div>

    <!-- ============================================================= -->
    <!-- 3-WAY HEAD-TO-HEAD COMPARISON MODAL -->
    <!-- ============================================================= -->
    <div id="compare-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md hidden p-4">
        <div class="bg-obsidian-900 border border-white/10 rounded-3xl max-w-5xl w-full p-6 max-h-[92vh] flex flex-col justify-between shadow-2xl overflow-hidden">
            <div class="flex items-center justify-between pb-4 border-b border-white/10">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center text-lg border border-indigo-500/30">
                        <i class="fa-solid fa-code-compare"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold tracking-tight">3-Way Side-by-Side Plugin Benchmark</h3>
                        <p class="text-xs text-slate-400">Head-to-head adoption, Bayesian ratings, and velocity comparator</p>
                    </div>
                </div>
                <button onclick="closeCompareModal()" class="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-obsidian-800 transition-colors">
                    <i class="fa-solid fa-xmark text-lg"></i>
                </button>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 my-4">
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1.5 font-heading">Primary Plugin (A)</label>
                    <select id="compare-select-a" onchange="renderComparisonView()" class="w-full px-3 py-2 bg-obsidian-950 border border-white/10 rounded-xl text-xs focus:outline-none focus:border-cyan-400 font-mono"></select>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1.5 font-heading">Comparison Plugin (B)</label>
                    <select id="compare-select-b" onchange="renderComparisonView()" class="w-full px-3 py-2 bg-obsidian-950 border border-white/10 rounded-xl text-xs focus:outline-none focus:border-indigo-400 font-mono"></select>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1.5 font-heading">Comparison Plugin (C)</label>
                    <select id="compare-select-c" onchange="renderComparisonView()" class="w-full px-3 py-2 bg-obsidian-950 border border-white/10 rounded-xl text-xs focus:outline-none focus:border-emerald-400 font-mono"></select>
                </div>
            </div>

            <div class="overflow-y-auto max-h-[55vh] pr-1" id="compare-content-grid"></div>
            <div class="pt-4 border-t border-white/10 flex justify-end">
                <button onclick="closeCompareModal()" class="px-5 py-2 rounded-xl bg-obsidian-800 hover:bg-obsidian-750 text-white text-xs font-bold transition-all">Done</button>
            </div>
        </div>
    </div>

    <!-- ============================================================= -->
    <!-- MULTI-CHANNEL EVIDENCE & COMPLAINT MODAL (v2.0) -->
    <!-- ============================================================= -->
    <div id="evidence-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md hidden p-4">
        <div class="bg-obsidian-900 border border-white/10 rounded-3xl max-w-4xl w-full p-6 max-h-[92vh] flex flex-col justify-between shadow-2xl">
            <div class="flex items-center justify-between pb-4 border-b border-white/10">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-rose-500/20 text-rose-400 flex items-center justify-center text-lg border border-rose-500/30">
                        <i class="fa-solid fa-bug-slash"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold tracking-tight" id="modal-plugin-title">Plugin Abuse Evidence Dossier</h3>
                        <p class="text-xs text-slate-400">Shannon Influx Entropy, Multi-Plugin Raid Correlation & SQL Directives</p>
                    </div>
                </div>
                <button onclick="closeEvidenceModal()" class="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-obsidian-800 transition-colors">
                    <i class="fa-solid fa-xmark text-lg"></i>
                </button>
            </div>

            <div class="flex gap-2 my-3 font-heading overflow-x-auto pb-1">
                <button onclick="setModalChannel('github')" id="m-btn-gh" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-cyan-600 text-white whitespace-nowrap"><i class="fa-brands fa-github mr-1"></i> GitHub Issue</button>
                <button onclick="setModalChannel('psc')" id="m-btn-psc" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-obsidian-800 text-slate-400 hover:text-white border border-white/5 whitespace-nowrap"><i class="fa-solid fa-scale-balanced mr-1"></i> Formal PSC Memo + SQL</button>
                <button onclick="setModalChannel('discord')" id="m-btn-dc" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-obsidian-800 text-slate-400 hover:text-white border border-white/5 whitespace-nowrap"><i class="fa-brands fa-discord mr-1"></i> Discord Webhook JSON</button>
                <button onclick="setModalChannel('slack')" id="m-btn-sl" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-obsidian-800 text-slate-400 hover:text-white border border-white/5 whitespace-nowrap"><i class="fa-brands fa-slack mr-1"></i> Slack Block Kit</button>
            </div>

            <div class="my-2 overflow-y-auto max-h-[50vh] pr-2">
                <pre class="bg-obsidian-950 p-4 rounded-2xl border border-white/5 text-xs font-mono text-slate-300 overflow-x-auto whitespace-pre-wrap leading-relaxed" id="modal-markdown-content"></pre>
            </div>

            <div class="pt-4 border-t border-white/10 flex justify-between items-center text-xs text-slate-400">
                <button onclick="copyModalMarkdown()" class="px-4 py-2 rounded-xl text-xs font-bold btn-luxury text-white flex items-center gap-1.5">
                    <i class="fa-solid fa-copy"></i> <span id="copy-btn-text">Copy Selected Format</span>
                </button>
                <button onclick="closeEvidenceModal()" class="px-5 py-2 rounded-xl bg-obsidian-800 hover:bg-obsidian-750 text-white font-bold transition-all">Close</button>
            </div>
        </div>
    </div>

    <!-- Toast Notification -->
    <div id="toast" class="fixed bottom-6 right-6 z-50 px-4 py-3 rounded-2xl bg-emerald-600 text-white text-xs font-bold shadow-2xl flex items-center gap-2 transform translate-y-20 opacity-0 transition-all duration-300 border border-emerald-400/30">
        <i class="fa-solid fa-circle-check text-base"></i> <span id="toast-text">Payload copied to clipboard!</span>
    </div>

    <!-- Footer -->
    <footer class="mt-14 text-center text-xs text-slate-500 font-mono">
        <p>© 2026 Yusuf Eminoğlu QGIS Plugin Governance Studio. All rights reserved.</p>
        <p class="mt-1">Synchronized with QGIS Official Python Plugins Repository (plugins.qgis.org).</p>
    </footer>

    <!-- Injected Telemetry Payload -->
    <script>
        const appData = ##DATA_INJECTION##;
    </script>

    <!-- Canvas Constellation Animation -->
    <script>
        const canvas = document.getElementById('bg-canvas');
        const ctx = canvas.getContext('2d');

        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        const particles = [];
        const maxParticles = 65;

        class Particle {
            constructor() {
                this.x = Math.random() * width;
                this.y = Math.random() * height;
                this.vx = (Math.random() - 0.5) * 0.25;
                this.vy = (Math.random() - 0.5) * 0.25;
                this.radius = Math.random() * 1.5 + 0.4;
            }

            update() {
                this.x += this.vx;
                this.y += this.vy;
                if (this.x < 0 || this.x > width) this.vx *= -1;
                if (this.y < 0 || this.y > height) this.vy *= -1;
            }

            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fillStyle = document.documentElement.getAttribute('data-theme') === 'alabaster' ? 'rgba(2, 132, 199, 0.25)' : 'rgba(56, 189, 248, 0.16)';
                ctx.fill();
            }
        }

        for (let i = 0; i < maxParticles; i++) {
            particles.push(new Particle());
        }

        function animate() {
            ctx.clearRect(0, 0, width, height);
            for (let i = 0; i < particles.length; i++) {
                particles[i].update();
                particles[i].draw();
            }
            requestAnimationFrame(animate);
        }
        animate();

        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        });
    </script>

    <!-- Interactive Client Logic -->
    <script>
        // Kinetic Counter Rollup Engine
        function animateValue(elementOrId, start, end, duration = 800, prefix = '', suffix = '') {
            const obj = (typeof elementOrId === 'string') ? document.getElementById(elementOrId) : elementOrId;
            if (!obj) return;
            
            let startTimestamp = null;
            const isFloat = end % 1 !== 0;
            
            const step = (timestamp) => {
                if (!startTimestamp) startTimestamp = timestamp;
                const progress = Math.min((timestamp - startTimestamp) / duration, 1);
                const ease = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
                const currentVal = start + (end - start) * ease;
                
                obj.innerText = prefix + (isFloat ? currentVal.toFixed(1) : Math.round(currentVal).toLocaleString()) + suffix;
                
                if (progress < 1) {
                    window.requestAnimationFrame(step);
                } else {
                    obj.innerText = prefix + (isFloat ? end.toFixed(1) : end.toLocaleString()) + suffix;
                }
            };
            window.requestAnimationFrame(step);
        }

        // Theme Switcher Logic
        function toggleTheme() {
            const curTheme = document.documentElement.getAttribute('data-theme') || 'obsidian';
            const newTheme = curTheme === 'obsidian' ? 'alabaster' : 'obsidian';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('qgis_dashboard_theme', newTheme);

            const btnText = document.getElementById('theme-toggle-text');
            if (btnText) btnText.innerText = newTheme === 'obsidian' ? 'Alabaster Mode' : 'Obsidian Mode';
            
            initializeCharts();
            if (typeof renderChoroplethMap === 'function') renderChoroplethMap();
            showToast(`Switched to ${newTheme === 'obsidian' ? 'Obsidian Titanium' : 'Alabaster Platinum (Swiss Mode)'}!`);
        }

        const savedTheme = localStorage.getItem('qgis_dashboard_theme');
        if (savedTheme) {
            document.documentElement.setAttribute('data-theme', savedTheme);
            const btnText = document.getElementById('theme-toggle-text');
            if (btnText) btnText.innerText = savedTheme === 'obsidian' ? 'Alabaster Mode' : 'Obsidian Mode';
        }

        // Global Keyboard Shortcuts
        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
                e.preventDefault();
                openCommandPalette();
                return;
            }

            if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'TEXTAREA') {
                if (e.key === 'Escape') {
                    e.target.blur();
                    closeEvidenceModal();
                    closeCompareModal();
                    closeCommandPalette();
                    closeExecutiveStorytellingModal();
                }
                return;
            }

            if (e.key === '1') switchTab('overview');
            else if (e.key === '2') switchTab('audit');
            else if (e.key === '3') switchTab('carto');
            else if (e.key === '4') switchTab('deepdive');
            else if (e.key === '5') switchTab('simulator');
            else if (e.key === '6') switchTab('table');
            else if (e.key === '7') switchTab('pipelines');
            else if (e.key.toLowerCase() === 't') toggleTheme();
            else if (e.key === '/') {
                e.preventDefault();
                switchTab('deepdive');
                setTimeout(() => document.getElementById('card-search-input').focus(), 150);
            }
            else if (e.key === 'Escape') {
                closeEvidenceModal();
                closeCompareModal();
                closeCommandPalette();
                closeExecutiveStorytellingModal();
                closeBadgeKitModal();
            }
        });

        // Command Palette Logic
        function openCommandPalette() {
            document.getElementById('command-palette-modal').classList.remove('hidden');
            document.getElementById('palette-search-input').value = '';
            filterCommandPalette();
            setTimeout(() => document.getElementById('palette-search-input').focus(), 100);
        }

        function closeCommandPalette() {
            document.getElementById('command-palette-modal').classList.add('hidden');
        }

        function filterCommandPalette() {
            const query = (document.getElementById('palette-search-input').value || '').toLowerCase();
            const list = document.getElementById('palette-results-list');
            list.innerHTML = '';

            const defaultActions = [
                { name: 'Switch to Executive Overview', icon: 'fa-chart-pie', action: () => { switchTab('overview'); closeCommandPalette(); } },
                { name: 'Switch to Rating Abuse & Surveillance', icon: 'fa-shield-halved', action: () => { switchTab('audit'); closeCommandPalette(); } },
                { name: 'Switch to Geospatial Studio', icon: 'fa-earth-americas', action: () => { switchTab('carto'); closeCommandPalette(); } },
                { name: 'Switch to Plugin Explorer', icon: 'fa-cubes', action: () => { switchTab('deepdive'); closeCommandPalette(); } },
                { name: 'Switch to Ecosystem Pipelines & Synergies', icon: 'fa-diagram-project', action: () => { switchTab('pipelines'); closeCommandPalette(); } },
                { name: 'Switch to Forecast Simulator', icon: 'fa-wand-magic-sparkles', action: () => { switchTab('simulator'); closeCommandPalette(); } },
                { name: 'Switch to Master Data Table', icon: 'fa-table', action: () => { switchTab('table'); closeCommandPalette(); } },
                { name: 'Open Dynamic Shields.io Badge Kit', icon: 'fa-certificate', action: () => { openBadgeKitModal(); closeCommandPalette(); } },
                { name: 'Toggle Theme (Obsidian / Alabaster)', icon: 'fa-circle-half-stroke', action: () => { toggleTheme(); closeCommandPalette(); } },
                { name: 'Open 3-Way Benchmark Comparator', icon: 'fa-code-compare', action: () => { openCompareModal(); closeCommandPalette(); } },
                { name: 'Open Reports & Announcement Kit', icon: 'fa-bullhorn', action: () => { openExecutiveStorytellingModal(); closeCommandPalette(); } },
                { name: 'Export Full Evidence JSON Bundle', icon: 'fa-file-code', action: () => { exportFullDossierJSON(); closeCommandPalette(); } },
                { name: 'Export Performance Table to CSV', icon: 'fa-file-csv', action: () => { exportToCSV(); closeCommandPalette(); } }
            ];

            appData.plugins.forEach(p => {
                defaultActions.push({
                    name: `Inspect Plugin: ${p.name}`,
                    icon: 'fa-cube',
                    sub: `${p.downloads.toLocaleString()} DL · ${p.average_vote.toFixed(1)} ★`,
                    action: () => {
                        switchTab('deepdive');
                        document.getElementById('card-search-input').value = p.name;
                        filterCards();
                        closeCommandPalette();
                    }
                });
            });

            const filtered = defaultActions.filter(a => a.name.toLowerCase().indexOf(query) > -1 || (a.sub && a.sub.toLowerCase().indexOf(query) > -1));

            filtered.slice(0, 8).forEach(item => {
                const row = document.createElement('div');
                row.className = "p-2.5 rounded-xl bg-obsidian-950/60 hover:bg-cyan-600 hover:text-white cursor-pointer transition-all flex items-center justify-between";
                row.onclick = item.action;
                row.innerHTML = `
                    <div class="flex items-center gap-2.5 truncate">
                        <i class="fa-solid ${item.icon} text-cyan-400"></i>
                        <span class="font-sans font-medium">${item.name}</span>
                    </div>
                    ${item.sub ? `<span class="text-[10px] text-slate-500 font-mono">${item.sub}</span>` : '<span class="text-[10px] text-slate-500">Jump</span>'}
                `;
                list.appendChild(row);
            });
        }

        // =============================================================
        // EXECUTIVE STORYTELLING & ANNOUNCEMENT KIT
        // =============================================================
        let activeStoryFormat = 'ecosystem';

        function openExecutiveStorytellingModal() {
            setStorytellingFormat('ecosystem');
            document.getElementById('storytelling-modal').classList.remove('hidden');
        }

        function closeExecutiveStorytellingModal() {
            document.getElementById('storytelling-modal').classList.add('hidden');
            document.getElementById('copy-story-btn-text').innerText = "Copy Selected Format";
        }

        function setStorytellingFormat(format) {
            activeStoryFormat = format;
            const btns = { ecosystem: 's-btn-eco', linkedin: 's-btn-li', twitter: 's-btn-tw', reddit: 's-btn-rd' };
            Object.keys(btns).forEach(k => {
                const btn = document.getElementById(btns[k]);
                if (btn) btn.className = k === format ? "px-3 py-1.5 rounded-xl text-xs font-bold bg-cyan-600 text-white whitespace-nowrap" : "px-3 py-1.5 rounded-xl text-xs font-bold bg-obsidian-800 text-slate-400 hover:text-white border border-white/5 whitespace-nowrap";
            });

            const leader = appData.plugins[0];
            const fastest = [...appData.plugins].sort((a,b) => b.avg_monthly_downloads - a.avg_monthly_downloads)[0];
            const topCountry = appData.summary.global_countries[0];

            let text = '';
            if (format === 'ecosystem') {
                text = `===============================================================
QGIS PLUGIN ECOSYSTEM ANNUAL STATE & GOVERNANCE REPORT
Author: Yusuf Eminoğlu | Audit Timestamp: ${appData.summary.last_updated}
===============================================================

1. PORTFOLIO VOLUME & TRAJECTORY:
   - Total Cumulative Ecosystem Downloads: ${appData.summary.total_downloads.toLocaleString()} across ${appData.summary.total_plugins} production plugins.
   - Active Monthly Adoption Velocity: ~${appData.summary.active_period_monthly_avg.toLocaleString()} downloads/month.
   - 100k Milestone Proximity: ${appData.summary.total_downloads.toLocaleString()} / 100,000 (${((appData.summary.total_downloads/100000)*100).toFixed(1)}% achieved).
   - Expected 100k Arrival: Estimated Q4 2026.

2. QUANTITATIVE ECONOMETRIC PROFILE:
   - Gini Inequality Index (Corrected): ${appData.summary.econometrics.gini_corrected} (Optimal Pareto distribution).
   - Effective Plugin Count (Entropy Diversity): ${appData.summary.econometrics.effective_plugin_count} active pillars.
   - Empirical Bayes Prior Rating: ${appData.summary.econometrics.prior_mean_rating} ★.

3. FLAGSHIP SPOTLIGHTS:
   - Portfolio Crown Jewel: ${leader.name} (${leader.downloads.toLocaleString()} downloads).
   - Velocity Champion: ${fastest.name} (~${Math.round(fastest.avg_monthly_downloads).toLocaleString()} downloads/mo pace).
   - Largest Regional Market: ${topCountry.flag} ${topCountry.country} (${topCountry.downloads.toLocaleString()} DL, ${topCountry.percentage}% share).

4. RATING GOVERNANCE & SECURITY SURVEILLANCE:
   - Coordinated Campaign Level: ${appData.correlation.campaign_level}
   - Critical Rating Anomalies: ${appData.summary.critical_anomalies} under active surveillance.
   - Evidence Fingerprint: SHA256-${appData.correlation.portfolio_evidence_signature}`;
            } else if (format === 'linkedin') {
                text = `🚀 Excited to share an official milestone update for our QGIS Urban Analytics & Spatial Planning Ecosystem!

Our 24 production QGIS plugins have officially surpassed ${appData.summary.total_downloads.toLocaleString()} cumulative downloads with an active adoption velocity of ~${appData.summary.active_period_monthly_avg.toLocaleString()} downloads/month across 140+ countries.

🌟 Top Ecosystem Highlights:
• Crown Jewel: ${leader.name} leading with ${leader.downloads.toLocaleString()} downloads.
• Velocity Champion: ${fastest.name} clocking ~${Math.round(fastest.avg_monthly_downloads).toLocaleString()}/month.
• Macro-Regional Engine: Western Europe & North America representing over 70% of spatial analysis workflows.

We've also open-sourced our dedicated Governance & Analytics Studio:
🔗 Live Dashboard: https://yusufeminoglu.github.io/qgis-plugins-governance/
🔗 GitHub Repository: https://github.com/YusufEminoglu/qgis-plugins-governance

Thank you to the global QGIS & OSGeo community! 🌍

#QGIS #GIS #UrbanPlanning #SpatialAnalytics #OpenSource #PyQGIS #Geospatial`;
            } else if (format === 'twitter') {
                text = `1/4 🌍 Huge milestone for our open-source GIS tools: The Yusuf Eminoğlu QGIS Plugin Ecosystem has reached ${appData.summary.total_downloads.toLocaleString()} total downloads across 24 plugins!

2/4 📈 Adoption Velocity: Running at ~${appData.summary.active_period_monthly_avg.toLocaleString()} downloads/month.
👑 Flagship: ${leader.name} (${leader.downloads.toLocaleString()} DL)
⚡ Fastest Adoption: ${fastest.name} (~${Math.round(fastest.avg_monthly_downloads).toLocaleString()}/mo)

3/4 🛡️ We built an open Governance & Analytics Studio tracking telemetry, econometric Gini diversity, and rating surveillance live via GitHub Actions:
https://yusufeminoglu.github.io/qgis-plugins-governance/

4/4 Explore the entire suite on the official QGIS Hub:
https://plugins.qgis.org/plugins/author/Yusuf%20Eminoglu/
#QGIS #SpatialAnalytics`;
            } else {
                text = `**[Release & Governance Bulletin] Yusuf Eminoğlu QGIS Plugin Ecosystem: ${appData.summary.total_downloads.toLocaleString()} Downloads Milestone**

Hey r/QGIS community!

Wanted to share an update on our 24 spatial planning & urban analytics plugins (including PlanX suite, CAD toolset, and 02 geospatial tools).

### 📊 Portfolio Telemetry Overview
| Metric | Value |
|---|---|
| Total Plugins | 24 (QGIS 3.x & QGIS 4.0 Ready) |
| Cumulative Downloads | ${appData.summary.total_downloads.toLocaleString()} |
| Current Velocity | ~${appData.summary.active_period_monthly_avg.toLocaleString()} downloads/mo |
| Portfolio Gini Score | ${appData.summary.econometrics.gini_corrected} |
| Flagship Plugin | ${leader.name} (${leader.downloads.toLocaleString()} DL) |

Check out the interactive live telemetry studio: https://yusufeminoglu.github.io/qgis-plugins-governance/
Hub Profile: https://plugins.qgis.org/plugins/author/Yusuf%20Eminoglu/`;
            }

            document.getElementById('storytelling-content-area').innerText = text;
        }

        function copyStorytellingText() {
            const text = document.getElementById('storytelling-content-area').innerText;
            navigator.clipboard.writeText(text).then(() => {
                document.getElementById('copy-story-btn-text').innerText = "Copied!";
                showToast("Announcement kit copied to clipboard!");
                setTimeout(() => {
                    document.getElementById('copy-story-btn-text').innerText = "Copy Selected Format";
                }, 2500);
            });
        }

        function switchTab(tabId) {
            const panes = document.querySelectorAll('.tab-pane');
            panes.forEach(pane => pane.classList.add('hidden'));

            const buttons = document.querySelectorAll('button[id^="tab-btn-"]');
            buttons.forEach(btn => {
                btn.className = "px-5 py-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 whitespace-nowrap";
            });

            const targetPane = document.getElementById(`tab-content-${tabId}`);
            if (targetPane) targetPane.classList.remove('hidden');
            const targetBtn = document.getElementById(`tab-btn-${tabId}`);
            if (targetBtn) targetBtn.className = "px-5 py-3 text-sm font-bold border-b-2 border-cyan-400 text-cyan-400 flex items-center gap-2 whitespace-nowrap";

            if (tabId === 'overview' || tabId === 'deepdive') {
                setTimeout(initializeCharts, 100);
            }
            if (tabId === 'simulator') {
                setTimeout(runSimulation, 100);
            }
            if (tabId === 'audit') {
                setTimeout(renderAuditHistoryChart, 100);
            }
            if (tabId === 'carto') {
                setTimeout(initializeGeospatialStudio, 100);
            }
            if (tabId === 'pipelines') {
                setTimeout(initializePipelines, 100);
            }
        }

        function renderKPIs() {
            const kpiGrid = document.getElementById('kpi-grid');
            const monthlyAvgSpeed = appData.summary.active_period_monthly_avg;

            const sortedBySpeed = [...appData.plugins].sort((a,b) => b.avg_monthly_downloads - a.avg_monthly_downloads);
            const fastestPlugin = sortedBySpeed[0];

            const planxDownloads = appData.summary.categories["PlanX Suite"]?.downloads || 0;
            const suite02Downloads = appData.summary.categories["02 Suite"]?.downloads || 0;
            const standaloneDownloads = appData.summary.categories["Standalone Plugins"]?.downloads || 0;

            const html = `
                <div class="p-6 rounded-3xl glass-panel relative overflow-hidden">
                    <div class="absolute -right-4 -bottom-4 text-7xl text-slate-700/10 pointer-events-none"><i class="fa-solid fa-download"></i></div>
                    <p class="text-xs font-semibold text-slate-400 tracking-wider uppercase font-mono">Total Downloads</p>
                    <div class="flex items-baseline mt-2">
                        <span class="text-3xl font-extrabold tracking-tight font-mono" id="kpi-total-dl">0</span>
                    </div>
                    <div class="flex items-center gap-1.5 mt-2.5 text-[11px] text-slate-400">
                        <span class="text-emerald-400 font-bold font-mono"><i class="fa-solid fa-chevron-up"></i> ${Math.round(appData.summary.total_downloads / appData.summary.total_plugins).toLocaleString()}</span>
                        <span>avg per plugin</span>
                    </div>
                </div>

                <div class="p-6 rounded-3xl glass-panel relative overflow-hidden">
                    <div class="absolute -right-4 -bottom-4 text-7xl text-slate-700/10 pointer-events-none"><i class="fa-solid fa-rocket"></i></div>
                    <p class="text-xs font-semibold text-slate-400 tracking-wider uppercase font-mono">Portfolio Velocity</p>
                    <div class="flex items-baseline mt-2">
                        <span class="text-3xl font-extrabold text-cyan-400 tracking-tight font-mono" id="kpi-velocity-val">0</span>
                        <span class="text-[10px] font-bold text-cyan-500 ml-1.5 font-mono">/mo</span>
                    </div>
                    <div class="flex items-center gap-1.5 mt-2.5 text-[11px] text-slate-400">
                        <span class="text-cyan-300 font-semibold">Active period run-rate</span>
                    </div>
                </div>

                <div class="p-6 rounded-3xl glass-panel relative overflow-hidden col-span-1">
                    <div class="absolute -right-4 -bottom-4 text-7xl text-slate-700/10 pointer-events-none"><i class="fa-solid fa-trophy"></i></div>
                    <p class="text-xs font-semibold text-slate-400 tracking-wider uppercase font-mono">Portfolio Leader</p>
                    <div class="flex flex-col mt-2">
                        <span class="text-lg font-bold truncate font-heading">${appData.plugins[0].name}</span>
                        <span class="text-xs font-semibold text-cyan-400 mt-0.5 font-mono">${appData.plugins[0].downloads.toLocaleString()} downloads</span>
                    </div>
                    <p class="text-[11px] text-slate-400 mt-2.5 font-mono">${((appData.plugins[0].downloads / appData.summary.total_downloads) * 100).toFixed(1)}% of total portfolio</p>
                </div>

                <div class="p-6 rounded-3xl glass-panel relative overflow-hidden col-span-1">
                    <div class="absolute -right-4 -bottom-4 text-7xl text-slate-700/10 pointer-events-none"><i class="fa-solid fa-fire-flame-curved"></i></div>
                    <p class="text-xs font-semibold text-slate-400 tracking-wider uppercase font-mono">Velocity Champion</p>
                    <div class="flex flex-col mt-2">
                        <span class="text-lg font-bold truncate font-heading">${fastestPlugin.name}</span>
                        <span class="text-xs font-semibold text-emerald-400 mt-0.5 font-mono">${Math.round(fastestPlugin.avg_monthly_downloads).toLocaleString()}/mo</span>
                    </div>
                    <p class="text-[11px] text-slate-400 mt-2.5">Fastest historical adoption</p>
                </div>
            `;
            kpiGrid.innerHTML = html;

            animateValue('kpi-total-dl', 0, appData.summary.total_downloads);
            animateValue('kpi-velocity-val', 0, Math.round(monthlyAvgSpeed));
            animateValue('impact-hours-saved', 0, appData.summary.community_hours_saved || 34800, 800, '', ' hrs');
            animateValue('impact-econ-val', 0, Math.round((appData.summary.economic_value_usd || 1740000) / 1000), 800, '$', 'k+ USD');
            animateValue('kpi-velocity-val', 0, monthlyAvgSpeed);

            const planxPercent = ((planxDownloads / appData.summary.total_downloads) * 100).toFixed(1);
            document.getElementById('planx-share-text').innerHTML = `${planxDownloads.toLocaleString()} <strong>(${planxPercent}%)</strong>`;

            const suite02Percent = ((suite02Downloads / appData.summary.total_downloads) * 100).toFixed(1);
            document.getElementById('suite02-share-text').innerHTML = `${suite02Downloads.toLocaleString()} <strong>(${suite02Percent}%)</strong>`;

            const standalonePercent = ((standaloneDownloads / appData.summary.total_downloads) * 100).toFixed(1);
            document.getElementById('standalone-share-text').innerHTML = `${standaloneDownloads.toLocaleString()} <strong>(${standalonePercent}%)</strong>`;
        }

        function renderMilestones() {
            document.getElementById('milestone-total-downloads').innerText = `${appData.summary.total_downloads.toLocaleString()} / 100,000`;
            const portfolioPercent = ((appData.summary.total_downloads / 100000) * 100).toFixed(1);
            document.getElementById('portfolio-progress-percent').innerText = `${portfolioPercent}%`;
            document.getElementById('portfolio-progress-bar').style.width = `${portfolioPercent}%`;

            const milestonesGrid = document.getElementById('milestones-grid');
            const sortedByMilestone = [...appData.plugins].sort((a,b) => b.milestone_progress - a.milestone_progress);

            let html = '';
            for (let i = 0; i < 3; i++) {
                const p = sortedByMilestone[i];
                if (!p) break;

                const remaining = p.next_milestone - p.downloads;

                html += `
                    <div class="p-4 rounded-2xl bg-obsidian-900/90 border border-white/5 flex flex-col justify-between">
                        <div>
                            <div class="flex justify-between items-center mb-1">
                                <h3 class="font-bold text-xs truncate max-w-[70%] font-heading">${p.name}</h3>
                                <span class="text-[10px] font-semibold text-cyan-400 bg-cyan-500/10 border border-cyan-500/20 px-2 py-0.5 rounded-full font-mono">${p.milestone_progress}%</span>
                            </div>
                            <div class="w-full bg-obsidian-800 rounded-full h-1.5 my-2">
                                <div class="bg-cyan-500 h-1.5 rounded-full" style="width: ${p.milestone_progress}%"></div>
                            </div>
                            <div class="flex justify-between items-center text-[10px] text-slate-400">
                                <span>Target: <strong class="font-mono">${p.next_milestone.toLocaleString()}</strong></span>
                                <span class="text-cyan-400 font-mono"><i class="fa-solid fa-calendar-check mr-1"></i>Est: ${p.milestone_est_date}</span>
                            </div>
                        </div>
                        <div class="mt-3 pt-2 border-t border-white/5 flex justify-between items-center text-[10px]">
                            <span class="text-slate-400">Remaining:</span>
                            <span class="font-bold text-emerald-400 font-mono"><i class="fa-solid fa-angles-right text-[8px] mr-1"></i> ${remaining.toLocaleString()}</span>
                        </div>
                    </div>
                `;
            }
            milestonesGrid.innerHTML = html;
        }

        // =============================================================
        // RATING ABUSE & AUDIT MONITOR LOGIC
        // =============================================================
        function renderAuditKPIsAndAlerts() {
            const crit = appData.summary.critical_anomalies;
            const warn = appData.summary.warning_anomalies;
            const badge = document.getElementById('audit-alert-badge');

            if (crit > 0) {
                badge.innerText = `${crit} CRITICAL`;
                badge.className = "ml-1.5 px-2 py-0.5 text-[10px] font-bold rounded-full bg-rose-500 text-white pulse-live font-mono";
            } else if (warn > 0) {
                badge.innerText = `${warn} ALERT`;
                badge.className = "ml-1.5 px-2 py-0.5 text-[10px] font-bold rounded-full bg-amber-500 text-white font-mono";
            } else {
                badge.innerText = "CLEAN";
                badge.className = "ml-1.5 px-2 py-0.5 text-[10px] font-bold rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-mono";
            }

            const totalVotes = appData.plugins.reduce((acc, p) => acc + p.votes_count, 0);
            const avgRating = (appData.plugins.reduce((acc, p) => acc + (p.average_vote * p.votes_count), 0) / (totalVotes || 1)).toFixed(2);

            const auditKPIContainer = document.getElementById('audit-kpis');
            auditKPIContainer.innerHTML = `
                <div class="p-6 rounded-3xl glass-panel relative overflow-hidden">
                    <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider font-mono">Critical 1-Star Raids</p>
                    <div class="flex items-baseline mt-2">
                        <span class="text-3xl font-extrabold font-mono ${crit > 0 ? 'text-rose-400' : 'text-emerald-400'}">${crit}</span>
                        <span class="text-xs text-slate-400 ml-2 font-mono">incidents</span>
                    </div>
                    <p class="text-[11px] text-slate-400 mt-2">Consecutive 1-star vote bombing</p>
                </div>

                <div class="p-6 rounded-3xl glass-panel relative overflow-hidden">
                    <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider font-mono">Suspicious Influxes</p>
                    <div class="flex items-baseline mt-2">
                        <span class="text-3xl font-extrabold font-mono ${warn > 0 ? 'text-amber-400' : 'text-slate-300'}">${warn}</span>
                        <span class="text-xs text-slate-400 ml-2 font-mono">flagged</span>
                    </div>
                    <p class="text-[11px] text-slate-400 mt-2">Abnormal negative score delta</p>
                </div>

                <div class="p-6 rounded-3xl glass-panel relative overflow-hidden">
                    <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider font-mono">Portfolio Weighted Rating</p>
                    <div class="flex items-baseline mt-2">
                        <span class="text-3xl font-extrabold font-mono">${avgRating}</span>
                        <span class="text-xs text-amber-400 ml-1.5"><i class="fa-solid fa-star"></i> / 5.0</span>
                    </div>
                    <p class="text-[11px] text-slate-400 mt-2 font-mono">Across ${totalVotes} total verified votes</p>
                </div>

                <div class="p-6 rounded-3xl glass-panel relative overflow-hidden">
                    <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider font-mono">Snapshots Recorded</p>
                    <div class="flex items-baseline mt-2">
                        <span class="text-3xl font-extrabold text-cyan-400 font-mono">${appData.summary.total_snapshots}</span>
                        <span class="text-xs text-slate-400 ml-2 font-mono">versions</span>
                    </div>
                    <p class="text-[11px] text-slate-400 mt-2">Continuous time-series audit trail</p>
                </div>
            `;

            renderAnomalyCards();
            populateAuditChartDropdown();
            populateTimeMachineSelectors();
        }

        function renderAnomalyCards() {
            const container = document.getElementById('anomaly-cards-container');
            container.innerHTML = '';

            appData.anomalies.forEach(a => {
                let badgeClass = "bg-slate-500/10 text-slate-400 border-slate-500/20";
                let panelClass = "glass-panel";

                if (a.severity === 'critical') {
                    badgeClass = "bg-rose-500/20 text-rose-400 border-rose-500/30 pulse-live font-mono";
                    panelClass = "glass-panel-danger";
                } else if (a.severity === 'high') {
                    badgeClass = "bg-amber-500/20 text-amber-400 border-amber-500/30 font-mono";
                } else if (a.severity === 'positive') {
                    badgeClass = "bg-emerald-500/20 text-emerald-400 border-emerald-500/30 font-mono";
                }

                const card = document.createElement('div');
                card.className = `p-6 rounded-3xl ${panelClass} flex flex-col justify-between transition-all`;
                card.setAttribute('data-severity', a.severity);

                let recoveryCallout = '';
                if (a.severity === 'critical' || a.severity === 'high') {
                    recoveryCallout = `
                        <div class="mt-3 p-3 rounded-2xl bg-rose-950/40 border border-rose-500/20 text-[11px] space-y-1 font-mono">
                            <div class="flex justify-between text-slate-300">
                                <span><i class="fa-solid fa-rotate-left text-cyan-400 mr-1"></i>Score After Rollback:</span>
                                <strong class="text-emerald-400">${a.reconciled_after_purge.toFixed(2)} ★ (Restore Fair Target)</strong>
                            </div>
                            <div class="flex justify-between text-slate-400">
                                <span><i class="fa-solid fa-star text-amber-400 mr-1"></i>Organic Recovery Needed:</span>
                                <span>+${a.needed_5_stars_to_recover} consecutive 5★ votes</span>
                            </div>
                            <div class="flex justify-between text-rose-400 font-bold">
                                <span><i class="fa-solid fa-fire text-rose-400 mr-1"></i>Calculated Damage Index:</span>
                                <span>-${a.damage_index} pts lost</span>
                            </div>
                        </div>
                    `;
                }

                card.innerHTML = `
                    <div>
                        <div class="flex justify-between items-start mb-3">
                            <div>
                                <span class="text-[9px] font-bold px-2.5 py-0.5 rounded-md border ${badgeClass}">${a.status}</span>
                                <h3 class="text-base font-bold mt-2 font-heading">${a.name}</h3>
                            </div>
                            <span class="text-[10px] text-slate-500 font-mono">v${a.version}</span>
                        </div>

                        <div class="grid grid-cols-3 gap-2 bg-obsidian-950/80 p-3 rounded-2xl border border-white/5 mb-4 text-center">
                            <div>
                                <span class="text-[9px] uppercase font-bold text-slate-500 block font-mono">Baseline (${a.baseline_votes} votes)</span>
                                <span class="text-xs font-extrabold text-slate-300 font-mono">${a.baseline_rating.toFixed(2)} ★</span>
                            </div>
                            <div class="border-x border-white/5">
                                <span class="text-[9px] uppercase font-bold text-slate-500 block font-mono">Live (${a.current_votes} votes)</span>
                                <span class="text-xs font-extrabold font-mono ${a.severity === 'critical' ? 'text-rose-400' : ''}">${a.current_rating.toFixed(2)} ★</span>
                            </div>
                            <div>
                                <span class="text-[9px] uppercase font-bold text-slate-500 block font-mono">Delta Votes</span>
                                <span class="text-xs font-extrabold font-mono ${a.delta_votes > 0 ? 'text-cyan-400' : 'text-slate-500'}">+${a.delta_votes}</span>
                            </div>
                        </div>

                        <div class="text-[11px] text-slate-300 space-y-1.5 mb-2 bg-obsidian-900/60 p-3 rounded-xl border border-white/5 font-mono">
                            <div class="flex justify-between">
                                <span class="text-slate-400">Score Delta (ΔS):</span>
                                <span class="font-semibold">${a.delta_score > 0 ? '+' : ''}${a.delta_score.toFixed(1)} pts</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-slate-400">Implied Influx Rating:</span>
                                <span class="font-bold ${a.implied_new_rating <= 1.5 && a.delta_votes > 0 ? 'text-rose-400' : 'text-emerald-400'}">${a.delta_votes > 0 ? a.implied_new_rating.toFixed(2) + ' ★ avg' : 'N/A'}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-slate-400">Shannon Entropy (H):</span>
                                <span class="font-bold text-cyan-400">${a.shannon_entropy} bits (EAS: ${a.entropy_score}/100)</span>
                            </div>
                        </div>

                        ${recoveryCallout}
                    </div>

                    <div class="pt-4 border-t border-white/5 flex justify-between items-center mt-4">
                        <span class="text-[10px] text-slate-400 font-mono">${a.delta_rating < 0 ? `<span class="text-rose-400 font-bold">${a.delta_rating.toFixed(2)}</span> rating drop` : 'Stable baseline'}</span>
                        <button onclick="openEvidenceModal('${a.name.replace(/'/g, "\\'")}')" class="px-4 py-2 rounded-xl text-xs font-bold ${a.severity === 'critical' ? 'btn-danger text-white' : 'bg-obsidian-800 hover:bg-obsidian-750 text-slate-300 border border-white/10'} flex items-center gap-1.5">
                            <i class="fa-solid fa-file-shield"></i> View Dossier & Report
                        </button>
                    </div>
                `;
                container.appendChild(card);
            });
        }

        function filterAnomalyStatus(type) {
            const cards = document.getElementById('anomaly-cards-container').children;
            const btnAll = document.getElementById('audit-filter-all');
            const btnCrit = document.getElementById('audit-filter-crit');

            if (type === 'critical') {
                btnCrit.className = "px-3.5 py-1.5 rounded-xl text-xs font-bold bg-cyan-600 text-white";
                btnAll.className = "px-3.5 py-1.5 rounded-xl text-xs font-bold bg-obsidian-800 text-slate-400 hover:text-white border border-white/5";
                for (let c of cards) {
                    c.style.display = c.getAttribute('data-severity') === 'critical' ? '' : 'none';
                }
            } else {
                btnAll.className = "px-3.5 py-1.5 rounded-xl text-xs font-bold bg-cyan-600 text-white";
                btnCrit.className = "px-3.5 py-1.5 rounded-xl text-xs font-bold bg-obsidian-800 text-slate-400 hover:text-white border border-white/5";
                for (let c of cards) {
                    c.style.display = '';
                }
            }
        }

        // Time Machine Logic
        function populateTimeMachineSelectors() {
            const selA = document.getElementById('tm-select-snap-a');
            const selB = document.getElementById('tm-select-snap-b');
            selA.innerHTML = '';
            selB.innerHTML = '';

            const snaps = appData.history_meta.snapshots;
            snaps.forEach((s, idx) => {
                const optA = document.createElement('option');
                optA.value = idx;
                optA.innerText = s.date_str || `Snapshot ${idx + 1}`;
                if (idx === 0) optA.selected = true;
                selA.appendChild(optA);

                const optB = document.createElement('option');
                optB.value = idx;
                optB.innerText = s.date_str || `Snapshot ${idx + 1}`;
                if (idx === snaps.length - 1) optB.selected = true;
                selB.appendChild(optB);
            });

            renderTimeMachineTable();
        }

        function renderTimeMachineTable() {
            const idxA = parseInt(document.getElementById('tm-select-snap-a').value);
            const idxB = parseInt(document.getElementById('tm-select-snap-b').value);

            const snapA = appData.history_meta.snapshots[idxA]?.plugins || {};
            const snapB = appData.history_meta.snapshots[idxB]?.plugins || {};

            const tbody = document.getElementById('tm-table-body');
            tbody.innerHTML = '';

            appData.plugins.forEach(p => {
                const name = p.name;
                const pA = snapA[name] || { average_vote: 0, votes_count: 0 };
                const pB = snapB[name] || { average_vote: 0, votes_count: 0 };

                const dVotes = pB.votes_count - pA.votes_count;
                const dRating = pB.average_vote - pA.average_vote;

                let trendBadge = '<span class="text-slate-500">― Stable</span>';
                if (dVotes > 0 && dRating <= -0.2) {
                    trendBadge = '<span class="text-rose-400 font-bold"><i class="fa-solid fa-arrow-trend-down mr-1"></i>Voted Down</span>';
                } else if (dVotes > 0 && dRating >= 0) {
                    trendBadge = '<span class="text-emerald-400 font-bold"><i class="fa-solid fa-arrow-trend-up mr-1"></i>Growth</span>';
                }

                const tr = document.createElement('tr');
                tr.className = "hover:bg-obsidian-850/60 border-b border-white/5 text-xs";
                tr.innerHTML = `
                    <td class="py-2.5 px-4 font-bold font-heading text-white">${name}</td>
                    <td class="py-2.5 px-4 text-center">${pA.votes_count} votes · ${pA.average_vote.toFixed(2)} ★</td>
                    <td class="py-2.5 px-4 text-center">${pB.votes_count} votes · ${pB.average_vote.toFixed(2)} ★</td>
                    <td class="py-2.5 px-4 text-right font-bold ${dVotes > 0 ? 'text-cyan-400' : 'text-slate-500'}">${dVotes > 0 ? '+' + dVotes : dVotes}</td>
                    <td class="py-2.5 px-4 text-right font-bold ${dRating < 0 ? 'text-rose-400' : (dRating > 0 ? 'text-emerald-400' : 'text-slate-500')}">${dRating > 0 ? '+' : ''}${dRating.toFixed(2)} ★</td>
                    <td class="py-2.5 px-4 text-center font-mono">${trendBadge}</td>
                `;
                tbody.appendChild(tr);
            });
        }

        function populateAuditChartDropdown() {
            const select = document.getElementById('audit-chart-plugin-select');
            select.innerHTML = '';
            appData.plugins.forEach(p => {
                const opt = document.createElement('option');
                opt.value = p.name;
                opt.innerText = p.name + ` (${p.average_vote.toFixed(1)} ★ - ${p.votes_count} votes)`;
                if (p.name === "PlanX GeoStats Lab") opt.selected = true;
                select.appendChild(opt);
            });
        }

        let auditChartInstance = null;
        function renderAuditHistoryChart() {
            const select = document.getElementById('audit-chart-plugin-select');
            if (!select) return;
            const targetPlugin = select.value || appData.plugins[0].name;

            const isAlabaster = document.documentElement.getAttribute('data-theme') === 'alabaster';
            const labelColor = isAlabaster ? '#334155' : '#94a3b8';
            const gridColor = isAlabaster ? 'rgba(0, 0, 0, 0.06)' : 'rgba(255, 255, 255, 0.05)';

            const pluginHistory = appData.history_meta.by_plugin[targetPlugin] || { ratings: [], votes: [] };
            const categories = appData.history_meta.timestamps;

            if (auditChartInstance) auditChartInstance.destroy();

            const chartOptions = {
                series: [
                    {
                        name: 'Average Rating (★)',
                        type: 'line',
                        data: pluginHistory.ratings
                    },
                    {
                        name: 'Total Votes Count',
                        type: 'column',
                        data: pluginHistory.votes
                    }
                ],
                chart: {
                    height: 310,
                    type: 'line',
                    toolbar: { show: false },
                    foreColor: labelColor
                },
                stroke: {
                    width: [4, 0],
                    curve: 'smooth'
                },
                plotOptions: {
                    bar: {
                        columnWidth: '32%',
                        borderRadius: 5
                    }
                },
                colors: ['#f43f5e', '#38bdf8'],
                xaxis: {
                    categories: categories,
                    labels: { style: { fontFamily: 'JetBrains Mono' } }
                },
                yaxis: [
                    {
                        min: 1.0,
                        max: 5.0,
                        title: { text: 'Rating (1 - 5 Stars)' },
                        labels: {
                            formatter: function(v) { return v.toFixed(1) + ' ★'; },
                            style: { fontFamily: 'JetBrains Mono' }
                        }
                    },
                    {
                        opposite: true,
                        title: { text: 'Votes Count' },
                        labels: {
                            formatter: function(v) { return Math.round(v); },
                            style: { fontFamily: 'JetBrains Mono' }
                        }
                    }
                ],
                grid: { borderColor: gridColor },
                tooltip: {
                    theme: isAlabaster ? 'light' : 'dark',
                    shared: true,
                    intersect: false
                }
            };

            auditChartInstance = new ApexCharts(document.querySelector("#audit-history-chart"), chartOptions);
            auditChartInstance.render();
        }

        // Multi-Channel Evidence Modal Logic (v2.0)
        let activeEvidenceReport = null;
        let activeEvidenceChannel = 'github';

        function openEvidenceModal(pluginName) {
            const report = appData.anomalies.find(a => a.name === pluginName);
            if (!report) return;

            activeEvidenceReport = report;
            document.getElementById('modal-plugin-title').innerText = `${report.name} — Rating Abuse Forensic Dossier`;
            setModalChannel('github');
            document.getElementById('evidence-modal').classList.remove('hidden');
        }

        function setModalChannel(channel) {
            activeEvidenceChannel = channel;
            const r = activeEvidenceReport;
            if (!r) return;

            const btns = { github: 'm-btn-gh', psc: 'm-btn-psc', discord: 'm-btn-dc', slack: 'm-btn-sl' };
            Object.keys(btns).forEach(k => {
                const btn = document.getElementById(btns[k]);
                if (btn) btn.className = k === channel ? "px-3 py-1.5 rounded-xl text-xs font-bold bg-cyan-600 text-white whitespace-nowrap" : "px-3 py-1.5 rounded-xl text-xs font-bold bg-obsidian-800 text-slate-400 hover:text-white border border-white/5 whitespace-nowrap";
            });

            let content = '';
            if (channel === 'github') {
                content = `### [Abuse / Rating Manipulation Incident Report] ${r.name}

#### 📋 Incident Summary
- **Target Plugin:** \\`${r.name}\\` (v${r.version})
- **Category:** ${r.category}
- **Official Hub URL:** https://plugins.qgis.org/plugins/${r.name.toLowerCase().replace(/\\s+/g, '_')}/
- **Evidence Hash Signature:** \\`SHA256-${r.evidence_hash}\\`
- **Audit Timestamp:** ${appData.summary.last_updated}

#### 📊 Mathematical Baseline Reconciliation & Audit Telemetry:
| Parameter | Baseline (${r.baseline_date}) | Current Live State | Delta / Influx |
|---|---|---|---|
| **Total Votes Count** | ${r.baseline_votes} | ${r.current_votes} | **+${r.delta_votes} votes** |
| **Average Rating** | ${r.baseline_rating.toFixed(3)} / 5.0 | ${r.current_rating.toFixed(3)} / 5.0 | **${r.delta_rating.toFixed(3)}** |
| **Cumulative Score Sum** | ${r.baseline_score.toFixed(2)} pts | ${r.current_score.toFixed(2)} pts | **+${r.delta_score.toFixed(2)} pts** |
| **Implied Influx Average Rating** | - | - | **${r.implied_new_rating.toFixed(2)} / 5.00** |
| **Shannon Entropy ($H$)** | 2.322 bits (Max) | - | **${r.shannon_entropy} bits (EAS: ${r.entropy_score}/100)** |

#### 🔬 Remediation & Rollback Mathematics:
- **Fair Target Rating (Purging ${r.delta_votes} Fraudulent Votes):** **${r.reconciled_after_purge.toFixed(2)} / 5.00**
- **Organic 5-Star Votes Required to Offset Attack Naturally:** **+${r.needed_5_stars_to_recover} votes**
- **Calculated Damage Index:** **-${r.damage_index} score points lost**

#### 🚨 Requested Remediation & Infrastructure Actions:
1. Audit vote logs and IP/timestamp patterns for **${r.name}** during the burst window.
2. Invalidate and purge the fraudulent automated 1-star submissions.
3. Recompute and restore aggregate rating baseline to **~${r.baseline_rating.toFixed(2)} / 5.0**.

*Report generated by QGIS Plugin Portfolio Governance Studio (Author: Yusuf Eminoğlu).*`;
            } else if (channel === 'psc') {
                content = `FORMAL MEMORANDUM TO QGIS PSC & HUB INFRASTRUCTURE MAINTAINERS
SUBJECT: Forensic Evidence & Database Remediation Query — ${r.name}
AUDIT TIMESTAMP: ${appData.summary.last_updated}
MAINTAINER: Yusuf Eminoğlu
EVIDENCE SIGNATURE: SHA256-${r.evidence_hash}

1. MATHEMATICAL PROOF OF FRAUDULENT INFLUX:
   - Target: ${r.name} (v${r.version})
   - Influx: +${r.delta_votes} votes @ ${r.implied_new_rating.toFixed(2)} ★ implied average
   - Shannon Influx Entropy: ${r.shannon_entropy} bits (Entropy Anomaly Score: ${r.entropy_score} / 100)
   - Calculated Score Damage: -${r.damage_index} points

2. PROPOSED DATABASE DIRECTIVE (SQL REMEDIATION FOR HUB ADMINS):
\\`\\`\\`sql
BEGIN;
-- Invalidate illegitimate vote burst
DELETE FROM plugins_rating 
WHERE plugin_id = (SELECT id FROM plugins_plugin WHERE name = '${r.name.replace(/'/g, "''")}')
  AND rating = 1
  AND created >= '${r.baseline_date}';

-- Recompute aggregate scores
UPDATE plugins_plugin
SET rating_votes = (SELECT COUNT(*) FROM plugins_rating WHERE plugin_id = plugins_plugin.id),
    rating_average = (SELECT COALESCE(AVG(rating), 0.0) FROM plugins_rating WHERE plugin_id = plugins_plugin.id)
WHERE name = '${r.name.replace(/'/g, "''")}';
COMMIT;
\\`\\`\\``;
            } else if (channel === 'discord') {
                content = JSON.stringify({
                    username: "QGIS Forensic Sentinel",
                    content: `🚨 **RATING ABUSE DETECTED: ${r.name}** 🚨`,
                    embeds: [{
                        title: `${r.name} Rating Manipulation Dossier`,
                        color: r.severity === 'critical' ? 15548997 : 16744203,
                        fields: [
                            { name: "Baseline vs Live", value: `${r.baseline_rating.toFixed(2)}★ (${r.baseline_votes}v) ➔ ${r.current_rating.toFixed(2)}★ (${r.current_votes}v)` },
                            { name: "Implied Influx", value: `+${r.delta_votes} votes @ ${r.implied_new_rating.toFixed(2)}★ avg (Entropy: ${r.shannon_entropy} bits)` },
                            { name: "Rollback Target", value: `${r.reconciled_after_purge.toFixed(2)}★ (Damage: -${r.damage_index} pts)` }
                        ],
                        footer: { text: `Signature: SHA256-${r.evidence_hash} • Yusuf Eminoğlu` }
                    }]
                }, null, 2);
            } else {
                content = JSON.stringify({
                    text: `🚨 Rating Abuse Alert on ${r.name}`,
                    blocks: [
                        { type: "header", text: { type: "plain_text", text: `Rating Abuse Alert: ${r.name}` } },
                        { type: "section", text: { type: "mrkdwn", text: `*Baseline:* ${r.baseline_rating.toFixed(2)}★ | *Live:* ${r.current_rating.toFixed(2)}★ | *Delta:* +${r.delta_votes} votes @ *${r.implied_new_rating.toFixed(2)}★ avg*` } },
                        { type: "section", text: { type: "mrkdwn", text: `*Entropy Anomaly Score:* ${r.entropy_score}/100 | *Rollback Target:* ${r.reconciled_after_purge.toFixed(2)}★` } }
                    ]
                }, null, 2);
            }

            document.getElementById('modal-markdown-content').innerText = content;
        }

        function openAllIncidentsModal() {
            const critReports = appData.anomalies.filter(a => a.severity === 'critical' || a.severity === 'high');
            if (critReports.length === 0) {
                alert("No critical anomalies detected in the current audit!");
                return;
            }
            openEvidenceModal(critReports[0].name);
        }

        function closeEvidenceModal() {
            document.getElementById('evidence-modal').classList.add('hidden');
            document.getElementById('copy-btn-text').innerText = "Copy Selected Format";
        }

        function copyModalMarkdown() {
            const text = document.getElementById('modal-markdown-content').innerText;
            navigator.clipboard.writeText(text).then(() => {
                document.getElementById('copy-btn-text').innerText = "Copied!";
                showToast("Evidence copied to clipboard!");
                setTimeout(() => {
                    document.getElementById('copy-btn-text').innerText = "Copy Selected Format";
                }, 2500);
            });
        }

        function exportFullDossierJSON() {
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(appData, null, 2));
            const downloadAnchor = document.createElement('a');
            downloadAnchor.setAttribute("href", dataStr);
            downloadAnchor.setAttribute("download", `qgis_plugins_audit_dossier_${new Date().toISOString().slice(0,10)}.json`);
            document.body.appendChild(downloadAnchor);
            downloadAnchor.click();
            downloadAnchor.remove();
            showToast("Evidence JSON bundle downloaded!");
        }

        // =============================================================
        // 3-WAY HEAD-TO-HEAD COMPARISON MODAL LOGIC
        // =============================================================
        function openCompareModal() {
            populateCompareDropdowns();
            renderComparisonView();
            document.getElementById('compare-modal').classList.remove('hidden');
        }

        function closeCompareModal() {
            document.getElementById('compare-modal').classList.add('hidden');
        }

        function populateCompareDropdowns() {
            const selA = document.getElementById('compare-select-a');
            const selB = document.getElementById('compare-select-b');
            const selC = document.getElementById('compare-select-c');
            selA.innerHTML = '';
            selB.innerHTML = '';
            selC.innerHTML = '';

            appData.plugins.forEach((p, idx) => {
                const optA = document.createElement('option');
                optA.value = p.name;
                optA.innerText = `${p.name} (${p.downloads.toLocaleString()} DL)`;
                if (idx === 0) optA.selected = true;
                selA.appendChild(optA);

                const optB = document.createElement('option');
                optB.value = p.name;
                optB.innerText = `${p.name} (${p.downloads.toLocaleString()} DL)`;
                if (idx === 1) optB.selected = true;
                selB.appendChild(optB);

                const optC = document.createElement('option');
                optC.value = p.name;
                optC.innerText = `${p.name} (${p.downloads.toLocaleString()} DL)`;
                if (idx === 2) optC.selected = true;
                selC.appendChild(optC);
            });
        }

        function renderComparisonView() {
            const nameA = document.getElementById('compare-select-a').value;
            const nameB = document.getElementById('compare-select-b').value;
            const nameC = document.getElementById('compare-select-c').value;

            const pA = appData.plugins.find(x => x.name === nameA);
            const pB = appData.plugins.find(x => x.name === nameB);
            const pC = appData.plugins.find(x => x.name === nameC);

            if (!pA || !pB || !pC) return;

            const container = document.getElementById('compare-content-grid');

            const maxDL = Math.max(pA.downloads, pB.downloads, pC.downloads);
            const maxSpeed = Math.max(pA.avg_monthly_downloads, pB.avg_monthly_downloads, pC.avg_monthly_downloads);
            const maxRating = Math.max(pA.average_vote, pB.average_vote, pC.average_vote);

            container.innerHTML = `
                <div class="grid grid-cols-3 gap-3 mb-6">
                    <div class="p-4 rounded-2xl bg-obsidian-950/80 border border-cyan-500/30">
                        <span class="text-[9px] font-bold uppercase text-cyan-400 tracking-wider font-mono">Plugin A</span>
                        <h4 class="text-sm font-extrabold truncate font-heading mt-1">${pA.name}</h4>
                        <span class="text-[11px] text-slate-400 font-mono">v${pA.version} · ${pA.category}</span>
                    </div>

                    <div class="p-4 rounded-2xl bg-obsidian-950/80 border border-indigo-500/30">
                        <span class="text-[9px] font-bold uppercase text-indigo-400 tracking-wider font-mono">Plugin B</span>
                        <h4 class="text-sm font-extrabold truncate font-heading mt-1">${pB.name}</h4>
                        <span class="text-[11px] text-slate-400 font-mono">v${pB.version} · ${pB.category}</span>
                    </div>

                    <div class="p-4 rounded-2xl bg-obsidian-950/80 border border-emerald-500/30">
                        <span class="text-[9px] font-bold uppercase text-emerald-400 tracking-wider font-mono">Plugin C</span>
                        <h4 class="text-sm font-extrabold truncate font-heading mt-1">${pC.name}</h4>
                        <span class="text-[11px] text-slate-400 font-mono">v${pC.version} · ${pC.category}</span>
                    </div>
                </div>

                <div class="space-y-2.5 text-xs font-mono">
                    <div class="p-3 rounded-xl bg-obsidian-950/60 border border-white/5 grid grid-cols-4 items-center">
                        <span class="text-slate-400 font-sans col-span-1">Downloads:</span>
                        <span class="text-center font-bold ${pA.downloads === maxDL ? 'text-cyan-400' : 'text-slate-300'}">${pA.downloads.toLocaleString()} ${pA.downloads === maxDL ? '👑' : ''}</span>
                        <span class="text-center font-bold ${pB.downloads === maxDL ? 'text-indigo-400' : 'text-slate-300'}">${pB.downloads.toLocaleString()} ${pB.downloads === maxDL ? '👑' : ''}</span>
                        <span class="text-center font-bold ${pC.downloads === maxDL ? 'text-emerald-400' : 'text-slate-300'}">${pC.downloads.toLocaleString()} ${pC.downloads === maxDL ? '👑' : ''}</span>
                    </div>

                    <div class="p-3 rounded-xl bg-obsidian-950/60 border border-white/5 grid grid-cols-4 items-center">
                        <span class="text-slate-400 font-sans col-span-1">Velocity:</span>
                        <span class="text-center font-bold ${pA.avg_monthly_downloads === maxSpeed ? 'text-cyan-400' : 'text-slate-300'}">${Math.round(pA.avg_monthly_downloads).toLocaleString()}/mo</span>
                        <span class="text-center font-bold ${pB.avg_monthly_downloads === maxSpeed ? 'text-indigo-400' : 'text-slate-300'}">${Math.round(pB.avg_monthly_downloads).toLocaleString()}/mo</span>
                        <span class="text-center font-bold ${pC.avg_monthly_downloads === maxSpeed ? 'text-emerald-400' : 'text-slate-300'}">${Math.round(pC.avg_monthly_downloads).toLocaleString()}/mo</span>
                    </div>

                    <div class="p-3 rounded-xl bg-obsidian-950/60 border border-white/5 grid grid-cols-4 items-center">
                        <span class="text-slate-400 font-sans col-span-1">Bayesian Rating:</span>
                        <span class="text-center font-bold text-amber-400">${pA.bayesian_rating.toFixed(2)} ★</span>
                        <span class="text-center font-bold text-amber-400">${pB.bayesian_rating.toFixed(2)} ★</span>
                        <span class="text-center font-bold text-amber-400">${pC.bayesian_rating.toFixed(2)} ★</span>
                    </div>

                    <div class="p-3 rounded-xl bg-obsidian-950/60 border border-white/5 grid grid-cols-4 items-center">
                        <span class="text-slate-400 font-sans col-span-1">Active Days:</span>
                        <span class="text-center text-slate-300">${pA.days_active} d</span>
                        <span class="text-center text-slate-300">${pB.days_active} d</span>
                        <span class="text-center text-slate-300">${pC.days_active} d</span>
                    </div>

                    <div class="p-3 rounded-xl bg-obsidian-950/60 border border-white/5 grid grid-cols-4 items-center">
                        <span class="text-slate-400 font-sans col-span-1">Next Milestone:</span>
                        <span class="text-center text-emerald-400">${pA.next_milestone.toLocaleString()} (${pA.milestone_progress}%)</span>
                        <span class="text-center text-emerald-400">${pB.next_milestone.toLocaleString()} (${pB.milestone_progress}%)</span>
                        <span class="text-center text-emerald-400">${pC.next_milestone.toLocaleString()} (${pC.milestone_progress}%)</span>
                    </div>
                </div>
            `;
        }

        function showToast(msg) {
            const toast = document.getElementById('toast');
            document.getElementById('toast-text').innerText = msg;
            toast.classList.remove('translate-y-20', 'opacity-0');
            setTimeout(() => {
                toast.classList.add('translate-y-20', 'opacity-0');
            }, 3000);
        }

        // =============================================================
        // GEOSPATIAL & CARTOGRAPHIC STUDIO JAVASCRIPT ENGINE
        // =============================================================
        let selectedCountryIso = 'US';
        let currentMapFilter = 'all';

        function initializeGeospatialStudio() {
            renderMacroRegions();
            renderChoroplethMap();
            renderAffinityMatrix();
            inspectCountryByIso('US');
        }

        function renderMacroRegions() {
            const deck = document.getElementById('macro-regions-deck');
            if (!deck || !appData.summary.macro_regions) return;

            deck.innerHTML = '';
            appData.summary.macro_regions.forEach(reg => {
                const card = document.createElement('div');
                card.className = "p-4 rounded-2xl bg-obsidian-950/80 border border-white/5 hover:border-cyan-500/30 cursor-pointer transition-all duration-200 group flex flex-col justify-between";
                card.onclick = () => focusMacroRegion(reg.code);

                card.innerHTML = `
                    <div>
                        <div class="flex items-center justify-between text-[10px] font-mono mb-2">
                            <span class="px-2 py-0.5 rounded-md bg-white/5 font-bold text-slate-400 group-hover:text-cyan-400 transition-colors">
                                #${reg.rank} ${reg.code}
                            </span>
                            <span class="text-cyan-400 font-bold">${reg.percentage}%</span>
                        </div>
                        <div class="flex items-center gap-2 mb-1">
                            <i class="fa-solid ${reg.icon} text-xs text-cyan-400"></i>
                            <h4 class="text-sm font-bold font-heading truncate text-white">${reg.region}</h4>
                        </div>
                        <div class="text-lg font-bold font-mono text-slate-200 mb-2">
                            ${reg.downloads.toLocaleString()} <span class="text-[10px] text-slate-500 font-normal">DL</span>
                        </div>
                    </div>
                    <div class="pt-2 border-t border-white/5 text-[10px] font-mono text-slate-400 flex items-center justify-between">
                        <span>Top: <strong class="text-white truncate max-w-[80px]">${reg.top_plugins[0]?.name.substring(0, 10)}...</strong></span>
                        <span class="text-cyan-400 font-bold">${reg.top_plugins[0]?.percentage}%</span>
                    </div>
                `;
                deck.appendChild(card);
            });
        }

        function renderChoroplethMap() {
            const isAlabaster = document.documentElement.getAttribute('data-theme') === 'alabaster';
            const countries = appData.summary.global_countries || [];
            const maxDl = Math.max(...countries.map(c => c.downloads), 1);

            function getChoroplethFill(dl) {
                if (!dl || dl === 0) return isAlabaster ? 'rgba(226, 232, 240, 0.65)' : 'rgba(20, 32, 54, 0.75)';
                const ratio = dl / maxDl;
                if (ratio > 0.65) return isAlabaster ? '#0284c7' : '#38bdf8';
                if (ratio > 0.35) return isAlabaster ? '#0369a1' : '#06b6d4';
                if (ratio > 0.15) return isAlabaster ? '#0ea5e9' : '#0284c7';
                if (ratio > 0.05) return isAlabaster ? '#38bdf8' : '#0369a1';
                return isAlabaster ? '#bae6fd' : '#082f49';
            }

            const paths = document.querySelectorAll('#svg-countries-layer .country-path');
            paths.forEach(p => {
                const iso = p.getAttribute('data-iso');
                const iso3 = p.getAttribute('data-iso3');
                const name = p.getAttribute('data-name');
                const cData = countries.find(c => c.iso === iso || c.iso === iso3 || c.country === name || (iso === 'US' && c.iso === 'US'));
                const dl = cData ? cData.downloads : 0;

                p.setAttribute('fill', getChoroplethFill(dl));
                p.setAttribute('stroke', isAlabaster ? 'rgba(255, 255, 255, 0.9)' : 'rgba(7, 10, 16, 0.85)');
                p.setAttribute('stroke-width', '0.6');

                p.onmouseenter = (e) => showMapTooltip(e, cData, iso, name);
                p.onmousemove = (e) => moveMapTooltip(e);
                p.onmouseleave = () => hideMapTooltip();
                p.onclick = () => { if (cData) inspectCountryByIso(cData.iso); };
            });

            const nodesLayer = document.getElementById('svg-nodes-layer');
            if (nodesLayer) {
                nodesLayer.innerHTML = '';
                countries.slice(0, 12).forEach(c => {
                    if (!c.cx || !c.cy) return;
                    const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
                    g.setAttribute('class', 'cursor-pointer group');
                    g.onclick = () => inspectCountryByIso(c.iso);
                    g.onmouseenter = (e) => showMapTooltip(e, c, c.iso, c.country);
                    g.onmouseleave = () => hideMapTooltip();

                    g.innerHTML = `
                        <circle cx="${c.cx}" cy="${c.cy}" r="9" fill="rgba(56, 189, 248, 0.22)" class="animate-ping" />
                        <circle cx="${c.cx}" cy="${c.cy}" r="3.5" fill="#38bdf8" stroke="#ffffff" stroke-width="1.2" filter="url(#radar-glow)" />
                    `;
                    nodesLayer.appendChild(g);
                });
            }
        }

        function showMapTooltip(e, cData, iso, name) {
            const tooltip = document.getElementById('map-hud-tooltip');
            if (!tooltip) return;

            if (!cData) {
                tooltip.innerHTML = `
                    <div class="text-xs font-bold text-slate-200 font-heading mb-0.5">${name || iso}</div>
                    <div class="text-[10px] text-cyan-400 font-mono">Global Organic Discovery Tier</div>
                    <div class="text-[9px] text-slate-400 font-mono mt-1">Autonomous QGIS user community</div>
                `;
            } else {
                tooltip.innerHTML = `
                    <div class="flex items-center gap-2 mb-1.5">
                        <span class="text-lg">${cData.flag}</span>
                        <div>
                            <h5 class="text-xs font-bold font-heading text-white">${cData.country} (${cData.iso})</h5>
                            <span class="text-[9px] font-mono text-cyan-400">${cData.region}</span>
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-2 text-[10px] font-mono mb-1.5 border-t border-b border-white/10 py-1">
                        <div><span class="text-slate-500 block">Downloads:</span> <strong class="text-white">${cData.downloads.toLocaleString()}</strong></div>
                        <div><span class="text-slate-500 block">Share:</span> <strong class="text-cyan-400">${cData.percentage}%</strong></div>
                    </div>
                    <div class="text-[9px] font-mono text-slate-400">
                        <span>Top: <strong class="text-white">${cData.top_plugins[0]?.name || 'N/A'}</strong></span>
                    </div>
                `;
            }
            tooltip.classList.remove('opacity-0');
            moveMapTooltip(e);
        }

        function moveMapTooltip(e) {
            const tooltip = document.getElementById('map-hud-tooltip');
            const wrapper = document.getElementById('world-map-wrapper');
            if (!tooltip || !wrapper) return;

            const rect = wrapper.getBoundingClientRect();
            const x = e.clientX - rect.left + 15;
            const y = e.clientY - rect.top + 15;
            tooltip.style.left = `${Math.min(x, rect.width - 220)}px`;
            tooltip.style.top = `${Math.min(y, rect.height - 120)}px`;
        }

        function hideMapTooltip() {
            const tooltip = document.getElementById('map-hud-tooltip');
            if (tooltip) tooltip.classList.add('opacity-0');
        }

        function inspectCountryByIso(iso) {
            const countries = appData.summary.global_countries || [];
            const cData = countries.find(c => c.iso === iso) || countries[0];
            if (!cData) return;
            selectedCountryIso = cData.iso;

            document.getElementById('drilldown-flag').innerText = cData.flag;
            document.getElementById('drilldown-country-name').innerText = cData.country;
            document.getElementById('drilldown-region-badge').innerText = `${cData.region} • ISO: ${cData.iso}`;
            document.getElementById('drilldown-downloads').innerText = cData.downloads.toLocaleString();
            document.getElementById('drilldown-pct').innerText = `${cData.percentage}% of Global Portfolio`;
            document.getElementById('drilldown-dom-suite').innerText = cData.dominant_suite;

            const list = document.getElementById('drilldown-plugins-list');
            list.innerHTML = '';
            (cData.top_plugins || []).slice(0, 5).forEach((p, idx) => {
                const item = document.createElement('div');
                item.className = "flex items-center justify-between text-xs py-1.5 px-3 rounded-xl bg-obsidian-900/90 border border-white/5 font-mono";
                item.innerHTML = `
                    <div class="flex items-center gap-2 truncate max-w-[170px]">
                        <span class="text-slate-500 text-[10px]">#${idx + 1}</span>
                        <span class="truncate font-sans font-medium text-white">${p.name}</span>
                    </div>
                    <div class="text-right">
                        <span class="text-cyan-400 font-bold">${p.downloads.toLocaleString()}</span>
                        <span class="text-[10px] text-slate-500">(${p.percentage}%)</span>
                    </div>
                `;
                list.appendChild(item);
            });

            document.querySelectorAll('#svg-countries-layer .country-path').forEach(p => {
                if (p.getAttribute('data-iso') === iso) {
                    p.setAttribute('stroke', '#38bdf8');
                    p.setAttribute('stroke-width', '2.5');
                } else {
                    p.setAttribute('stroke', document.documentElement.getAttribute('data-theme') === 'alabaster' ? '#ffffff' : '#070a10');
                    p.setAttribute('stroke-width', '1');
                }
            });
        }

        function renderAffinityMatrix() {
            const tbody = document.getElementById('suite-affinity-tbody');
            if (!tbody || !appData.summary.suite_affinity_matrix) return;

            tbody.innerHTML = '';
            appData.summary.suite_affinity_matrix.forEach(row => {
                const tr = document.createElement('tr');
                tr.className = "hover:bg-white/[0.02] transition-colors";

                let cellsHtml = `
                    <td class="py-3 px-4 font-sans font-bold text-white flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full ${row.suite.includes('PlanX') ? 'bg-cyan-400' : (row.suite.includes('02') ? 'bg-indigo-400' : 'bg-emerald-400')}"></span>
                        ${row.suite}
                    </td>
                    <td class="py-3 px-4 text-right font-bold text-slate-300">
                        ${row.global_downloads.toLocaleString()} <span class="text-[10px] text-slate-500">(${row.global_share}%)</span>
                    </td>
                `;

                row.cells.forEach(cell => {
                    const badgeClass = cell.location_quotient >= 1.15 
                        ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' 
                        : (cell.location_quotient <= 0.85 
                            ? 'bg-amber-500/10 text-amber-400 border-amber-500/30' 
                            : 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30');

                    cellsHtml += `
                        <td class="py-3 px-4 text-center">
                            <div class="flex flex-col items-center gap-0.5">
                                <span class="font-bold text-white text-[11px]">${cell.downloads.toLocaleString()}</span>
                                <span class="text-[9px] text-slate-400">${cell.regional_share}% reg / ${cell.suite_share}% ste</span>
                                <span class="px-2 py-0.5 rounded-md text-[9px] font-bold border ${badgeClass} mt-0.5">
                                    LQ ${cell.location_quotient.toFixed(2)}x
                                </span>
                            </div>
                        </td>
                    `;
                });

                tr.innerHTML = cellsHtml;
                tbody.appendChild(tr);
            });
        }

        function setMapFilter(regCode) {
            currentMapFilter = regCode;
            ['all', 'WEU', 'NAM', 'LAM', 'EME', 'APAC'].forEach(code => {
                const btn = document.getElementById(`map-btn-${code}`);
                if (btn) {
                    if (code === regCode) {
                        btn.className = "px-3 py-1 rounded-xl bg-cyan-500/20 text-cyan-400 font-bold border border-cyan-500/30 transition-all";
                    } else {
                        btn.className = "px-3 py-1 rounded-xl text-slate-400 hover:text-white transition-all";
                    }
                }
            });

            const svgMap = document.getElementById('svg-world-map');
            if (!svgMap) return;

            const zoomTransforms = {
                'all': 'matrix(1 0 0 1 0 0)',
                'WEU': 'matrix(2.4 0 0 2.4 -680 -180)',
                'NAM': 'matrix(1.9 0 0 1.9 -150 -100)',
                'LAM': 'matrix(1.9 0 0 1.9 -300 -350)',
                'EME': 'matrix(2.2 0 0 2.2 -750 -240)',
                'APAC': 'matrix(1.8 0 0 1.8 -850 -250)'
            };
            svgMap.style.transform = zoomTransforms[regCode] || zoomTransforms['all'];
        }

        function focusMacroRegion(regCode) {
            setMapFilter(regCode);
        }

        function resetMapZoom() {
            setMapFilter('all');
            const searchInput = document.getElementById('map-country-search');
            if (searchInput) searchInput.value = '';
        }

        // =============================================================
        // GEOSPATIAL MAP COUNTRY QUICK SEARCH
        // =============================================================
        function handleMapCountrySearch(val) {
            if (!val || val.trim() === '') {
                resetMapZoom();
                return;
            }
            const q = val.trim().toLowerCase();
            const countries = appData.summary.global_countries || [];
            const match = countries.find(c => c.country.toLowerCase().includes(q) || c.iso.toLowerCase() === q);

            if (match) {
                inspectCountryByIso(match.iso);
                if (match.cx && match.cy) {
                    const svg = document.getElementById('svg-world-map');
                    if (svg) {
                        svg.style.transform = `scale(2.2) translate(${480 - match.cx}px, ${250 - match.cy}px)`;
                    }
                }
            } else {
                const paths = document.querySelectorAll('#svg-countries-layer .country-path');
                for (let p of paths) {
                    const name = (p.getAttribute('data-name') || '').toLowerCase();
                    const iso = (p.getAttribute('data-iso') || '').toLowerCase();
                    const iso3 = (p.getAttribute('data-iso3') || '').toLowerCase();
                    if (name.includes(q) || iso === q || iso3 === q) {
                        const bbox = p.getBBox();
                        const cx = bbox.x + bbox.width / 2;
                        const cy = bbox.y + bbox.height / 2;
                        const svg = document.getElementById('svg-world-map');
                        if (svg) {
                            svg.style.transform = `scale(2.2) translate(${480 - cx}px, ${250 - cy}px)`;
                        }
                        showMapTooltip({ clientX: 300, clientY: 200 }, null, p.getAttribute('data-iso'), p.getAttribute('data-name'));
                        break;
                    }
                }
            }
        }

        // =============================================================
        // ECOSYSTEM PIPELINES & WORKFLOW GRAPH ENGINE
        // =============================================================
        let selectedPipelineId = 'morphology';

        function initializePipelines() {
            const pipelines = appData.summary.pipelines || [];
            const deck = document.getElementById('pipeline-selector-deck');
            if (!deck || pipelines.length === 0) return;

            deck.innerHTML = '';
            pipelines.forEach(p => {
                const card = document.createElement('div');
                const isSelected = p.id === selectedPipelineId;
                card.className = `p-4 rounded-2xl cursor-pointer transition-all duration-200 flex flex-col justify-between ${isSelected ? 'bg-cyan-500/10 border-2 border-cyan-400 shadow-lg shadow-cyan-500/10' : 'bg-obsidian-950/80 border border-white/5 hover:border-cyan-500/30'}`;
                card.onclick = () => selectPipeline(p.id);

                card.innerHTML = `
                    <div>
                        <div class="flex items-center justify-between text-[10px] font-mono mb-2">
                            <span class="px-2 py-0.5 rounded-md bg-white/5 text-slate-400 font-bold">${p.steps.length} Steps</span>
                            <span class="text-cyan-400 font-bold">${p.estimated_time}</span>
                        </div>
                        <div class="flex items-center gap-2 mb-1">
                            <i class="fa-solid ${p.icon} text-sm" style="color: ${p.color}"></i>
                            <h4 class="text-xs font-bold font-heading text-white line-clamp-2">${p.name}</h4>
                        </div>
                    </div>
                    <div class="pt-2 mt-2 border-t border-white/5 text-[9px] font-mono text-slate-400">
                        ${p.category}
                    </div>
                `;
                deck.appendChild(card);
            });

            renderActivePipelineDetails();
        }

        function selectPipeline(pipeId) {
            selectedPipelineId = pipeId;
            initializePipelines();
        }

        function renderActivePipelineDetails() {
            const pipelines = appData.summary.pipelines || [];
            const pipe = pipelines.find(p => p.id === selectedPipelineId) || pipelines[0];
            if (!pipe) return;

            const title = document.getElementById('pipe-active-title');
            const sub = document.getElementById('pipe-active-subtitle');
            const time = document.getElementById('pipe-active-time');
            const stepsCount = document.getElementById('pipe-active-steps-count');
            const icon = document.getElementById('pipe-active-icon');

            if (title) title.innerText = pipe.name;
            if (sub) sub.innerText = pipe.desc;
            if (time) time.innerText = pipe.estimated_time;
            if (stepsCount) stepsCount.innerText = `${pipe.steps.length} Modular Steps`;
            if (icon) {
                icon.className = `fa-solid ${pipe.icon}`;
                icon.style.color = pipe.color;
            }

            const nodesFlow = document.getElementById('pipe-nodes-flow');
            if (nodesFlow) {
                nodesFlow.innerHTML = '';
                pipe.steps.forEach((s) => {
                    const node = document.createElement('div');
                    node.className = "p-4 rounded-2xl bg-obsidian-950 border border-white/10 flex flex-col justify-between relative group hover:border-cyan-400 transition-all";
                    node.innerHTML = `
                        <div class="flex items-center justify-between text-[10px] font-mono mb-2">
                            <span class="w-5 h-5 rounded-full bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 flex items-center justify-center font-bold font-heading">
                                ${s.step}
                            </span>
                            <span class="text-[9px] text-slate-500 uppercase">${s.type}</span>
                        </div>
                        <h5 class="text-xs font-bold font-heading text-white mb-1">${s.plugin}</h5>
                        <p class="text-[10px] text-slate-400 font-sans mb-3">${s.action}</p>
                        <div class="pt-2 border-t border-white/5 text-[9px] font-mono text-cyan-400 flex items-center justify-between">
                            <span>Output:</span>
                            <strong class="text-slate-200">${s.output}</strong>
                        </div>
                    `;
                    nodesFlow.appendChild(node);
                });
            }

            const dossier = document.getElementById('pipe-steps-dossier');
            if (dossier) {
                dossier.innerHTML = '';
                pipe.steps.forEach(s => {
                    const row = document.createElement('div');
                    row.className = "p-3 rounded-xl bg-obsidian-950/60 border border-white/5 flex flex-col sm:flex-row sm:items-center justify-between text-xs gap-2";
                    row.innerHTML = `
                        <div class="flex items-center gap-3">
                            <span class="w-6 h-6 rounded-lg bg-white/5 text-cyan-400 font-bold font-mono flex items-center justify-center text-xs">#${s.step}</span>
                            <div>
                                <strong class="text-white font-heading">${s.plugin}</strong>
                                <span class="text-slate-400 text-xs ml-2">${s.action}</span>
                            </div>
                        </div>
                        <div class="flex items-center gap-3 font-mono text-[10px]">
                            <span class="px-2 py-0.5 rounded bg-white/5 text-slate-400">${s.type}</span>
                            <span class="text-cyan-400">➔ ${s.output}</span>
                        </div>
                    `;
                    dossier.appendChild(row);
                });
            }
        }

        function copyCurrentPipelineRecipe() {
            const pipelines = appData.summary.pipelines || [];
            const pipe = pipelines.find(p => p.id === selectedPipelineId) || pipelines[0];
            if (!pipe) return;

            const payload = JSON.stringify({
                pipeline_id: pipe.id,
                pipeline_name: pipe.name,
                category: pipe.category,
                author: "Yusuf Eminoğlu",
                execution_time: pipe.estimated_time,
                steps: pipe.steps
            }, null, 2);

            navigator.clipboard.writeText(payload).then(() => {
                showToast("Pipeline recipe JSON copied to clipboard!");
            });
        }

        // =============================================================
        // SHIELDS.IO DYNAMIC BADGE KIT GENERATOR
        // =============================================================
        function openBadgeKitModal() {
            const select = document.getElementById('badge-kit-plugin-select');
            if (select && select.options.length === 0) {
                appData.plugins.forEach(p => {
                    const opt = document.createElement('option');
                    opt.value = p.name;
                    opt.innerText = `${p.name} (${p.downloads.toLocaleString()} DL · ${p.average_vote.toFixed(1)} ★)`;
                    select.appendChild(opt);
                });
            }
            updateBadgeKitPreview();
            document.getElementById('badge-kit-modal').classList.remove('hidden');
        }

        function closeBadgeKitModal() {
            document.getElementById('badge-kit-modal').classList.add('hidden');
        }

        function updateBadgeKitPreview() {
            const select = document.getElementById('badge-kit-plugin-select');
            const pluginName = select ? select.value : appData.plugins[0].name;
            const p = appData.plugins.find(x => x.name === pluginName) || appData.plugins[0];

            const dlCount = p.downloads >= 1000 ? (p.downloads / 1000).toFixed(1) + 'k' : p.downloads;
            const cleanName = encodeURIComponent(p.name);
            
            const badgeDL = `https://img.shields.io/badge/${cleanName}-${dlCount}%20Downloads-0284c7?style=flat-square&logo=qgis`;
            const badgeRating = `https://img.shields.io/badge/Rating-${p.average_vote.toFixed(1)}%20★-amber?style=flat-square`;
            const badgeQgis = `https://img.shields.io/badge/QGIS%204-Ready-emerald?style=flat-square`;
            const badgeSecurity = `https://img.shields.io/badge/Security-Passed-emerald?style=flat-square`;

            const container = document.getElementById('badge-preview-container');
            if (container) {
                container.innerHTML = `
                    <img src="${badgeDL}" alt="Downloads" class="h-6" />
                    <img src="${badgeRating}" alt="Rating" class="h-6" />
                    <img src="${badgeQgis}" alt="QGIS 4 Ready" class="h-6" />
                    <img src="${badgeSecurity}" alt="Bandit Passed" class="h-6" />
                `;
            }

            const mdSnippet = `[![${p.name} Downloads](${badgeDL})](${p.url}) [![Rating](${badgeRating})](${p.url}) [![QGIS 4 Ready](${badgeQgis})](https://yusufeminoglu.github.io/qgis-plugins-governance/)`;
            const htmlSnippet = `<a href="${p.url}"><img src="${badgeDL}" alt="${p.name} Downloads" /></a> <a href="${p.url}"><img src="${badgeRating}" alt="Rating" /></a>`;

            const mdBox = document.getElementById('badge-code-markdown');
            const htmlBox = document.getElementById('badge-code-html');
            if (mdBox) mdBox.value = mdSnippet;
            if (htmlBox) htmlBox.value = htmlSnippet;
        }

        function copyBadgeSnippet(type) {
            const el = type === 'markdown' ? document.getElementById('badge-code-markdown') : document.getElementById('badge-code-html');
            if (el) {
                navigator.clipboard.writeText(el.value).then(() => {
                    showToast(`${type.toUpperCase()} badge code copied!`);
                });
            }
        }

        // =============================================================
        // MASTER TABLE & EXPLORER RENDERING
        // =============================================================
        const tbody = document.getElementById('tab-table-body');
        function renderTableData(filterMode = 'all') {
            tbody.innerHTML = '';

            let list = [...appData.plugins];
            if (filterMode === 'top5') {
                list = list.slice(0, 5);
            } else if (filterMode === 'highrated') {
                list = list.filter(p => p.average_vote >= 4.5);
            } else if (filterMode === 'velocity') {
                list = list.filter(p => p.avg_monthly_downloads >= 500);
            } else if (filterMode === 'alerts') {
                const raidNames = appData.anomalies.filter(a => a.severity === 'critical' || a.severity === 'high').map(a => a.name);
                list = list.filter(p => raidNames.includes(p.name));
            }

            list.forEach(item => {
                const tr = document.createElement('tr');
                tr.className = "hover:bg-obsidian-850/60 transition-colors border-b border-white/5 text-xs";

                let catBadge = '';
                if (item.category === 'PlanX Suite') {
                    catBadge = '<span class="px-2.5 py-0.5 rounded-md bg-indigo-500/15 text-indigo-400 font-semibold text-[10px] border border-indigo-500/20 font-heading">PlanX Suite</span>';
                } else if (item.category === '02 Suite') {
                    catBadge = '<span class="px-2.5 py-0.5 rounded-md bg-cyan-500/15 text-cyan-400 font-semibold text-[10px] border border-cyan-500/20 font-heading">02 Suite</span>';
                } else {
                    catBadge = '<span class="px-2.5 py-0.5 rounded-md bg-slate-500/15 text-slate-400 font-semibold text-[10px] border border-slate-500/20 font-heading">Standalone</span>';
                }

                const audit = appData.anomalies.find(a => a.name === item.name);
                let statusBadge = '<span class="text-slate-500 text-[10px] font-mono">Normal</span>';
                if (audit && audit.severity === 'critical') {
                    statusBadge = '<span class="px-2.5 py-0.5 rounded-md bg-rose-500/20 text-rose-400 border border-rose-500/30 font-bold text-[9px] font-mono pulse-live"><i class="fa-solid fa-triangle-exclamation mr-1"></i>Raid Alert</span>';
                } else if (audit && audit.severity === 'high') {
                    statusBadge = '<span class="px-2.5 py-0.5 rounded-md bg-amber-500/20 text-amber-400 border border-amber-500/30 font-bold text-[9px] font-mono">Watch</span>';
                }

                let honorsHtml = '';
                (item.honors || []).forEach(h => {
                    honorsHtml += `<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-${h.color}-500/10 text-${h.color}-400 text-[9px] font-bold border border-${h.color}-500/20 font-mono"><i class="fa-solid ${h.icon}"></i> ${h.badge}</span> `;
                });

                tr.innerHTML = `
                    <td class="py-3.5 px-4 font-semibold font-heading">
                        <div>${item.name}</div>
                        <div class="mt-1">${honorsHtml}</div>
                    </td>
                    <td class="py-3.5 px-4 text-center">${catBadge}</td>
                    <td class="py-3.5 px-4 text-center text-slate-400 font-mono">${item.create_date}</td>
                    <td class="py-3.5 px-4 text-right font-bold font-mono">${item.downloads.toLocaleString()}</td>
                    <td class="py-3.5 px-4 text-right text-cyan-400 font-semibold font-mono">${Math.round(item.avg_monthly_downloads).toLocaleString()}/mo</td>
                    <td class="py-3.5 px-4 text-center font-mono font-bold text-amber-400">${item.bayesian_rating.toFixed(2)} ★</td>
                    <td class="py-3.5 px-4 text-center">
                        <span class="px-2 py-0.5 rounded text-[9px] font-mono font-bold bg-${item.kinetic_badge}-500/15 text-${item.kinetic_badge}-400 border border-${item.kinetic_badge}-500/20">${item.kinetic_regime}</span>
                    </td>
                    <td class="py-3.5 px-4 text-center">${statusBadge}</td>
                `;
                tbody.appendChild(tr);
            });
        }

        function applyTablePreset(mode) {
            const btns = { 'all': 'tbl-preset-all', 'top5': 'tbl-preset-top5', 'highrated': 'tbl-preset-rated', 'velocity': 'tbl-preset-vel', 'alerts': 'tbl-preset-alerts' };
            Object.keys(btns).forEach(k => {
                const btn = document.getElementById(btns[k]);
                if (btn) btn.className = (k === mode) ? "px-3 py-1 rounded-xl text-xs font-bold bg-cyan-600 text-white" : "px-3 py-1 rounded-xl text-xs font-bold bg-obsidian-900 text-slate-400 hover:text-white border border-white/5";
            });
            renderTableData(mode);
        }

        function renderTagFilterChips() {
            const container = document.getElementById('tag-filter-chips');
            container.innerHTML = '<span class="text-[11px] text-slate-500 font-mono font-semibold mr-1">Tags:</span>';

            const topTags = appData.summary.top_tags.slice(0, 7);
            topTags.forEach(t => {
                const chip = document.createElement('button');
                chip.className = "px-2.5 py-1 rounded-lg text-[10px] font-mono font-semibold bg-obsidian-900 text-slate-400 hover:text-white border border-white/5 transition-all";
                chip.setAttribute('data-tag', t.tag);
                chip.onclick = () => toggleTagFilter(t.tag, chip);
                chip.innerText = `${t.tag} (${t.count})`;
                container.appendChild(chip);
            });
        }

        let activeTags = [];
        function toggleTagFilter(tag, chipEl) {
            if (activeTags.includes(tag)) {
                activeTags = activeTags.filter(t => t !== tag);
                chipEl.className = "px-2.5 py-1 rounded-lg text-[10px] font-mono font-semibold bg-obsidian-900 text-slate-400 hover:text-white border border-white/5 transition-all";
            } else {
                activeTags.push(tag);
                chipEl.className = "px-2.5 py-1 rounded-lg text-[10px] font-mono font-semibold bg-cyan-600 text-white transition-all";
            }
            applyCombinedFilters();
        }

        function renderCards() {
            const container = document.getElementById('plugin-cards-container');
            container.innerHTML = '';

            appData.plugins.forEach((p, idx) => {
                let catColor = 'bg-slate-500/10 text-slate-400 border-slate-500/20';
                if (p.category === 'PlanX Suite') {
                    catColor = 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20';
                } else if (p.category === '02 Suite') {
                    catColor = 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20';
                }

                let quadBadge = '';
                if (p.quadrant === 'Popular Momentum') {
                    quadBadge = '<span class="px-2 py-0.5 rounded-md text-[9px] font-bold bg-rose-500/15 text-rose-400 border border-rose-500/20 font-mono"><i class="fa-solid fa-fire mr-1"></i> Popular Momentum</span>';
                } else if (p.quadrant === 'High Velocity') {
                    quadBadge = '<span class="px-2 py-0.5 rounded-md text-[9px] font-bold bg-emerald-500/15 text-emerald-400 border border-emerald-500/20 font-mono"><i class="fa-solid fa-arrow-trend-up mr-1"></i> High Velocity</span>';
                } else if (p.quadrant === 'Stable Classic') {
                    quadBadge = '<span class="px-2 py-0.5 rounded-md text-[9px] font-bold bg-cyan-500/15 text-cyan-400 border border-cyan-500/20 font-mono"><i class="fa-solid fa-anchor mr-1"></i> Stable Classic</span>';
                } else {
                    quadBadge = '<span class="px-2 py-0.5 rounded-md text-[9px] font-bold bg-slate-500/15 text-slate-400 border border-slate-500/20 font-mono"><i class="fa-solid fa-bullseye mr-1"></i> Niche Specialist</span>';
                }

                let honorsHtml = '';
                (p.honors || []).forEach(h => {
                    honorsHtml += `<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-${h.color}-500/10 text-${h.color}-400 text-[9px] font-bold border border-${h.color}-500/20 font-mono"><i class="fa-solid ${h.icon}"></i> ${h.badge}</span> `;
                });

                const tagsHtml = p.tags.slice(0, 4).map(t => `<span class="bg-obsidian-900 text-slate-400 px-2 py-0.5 rounded text-[9px] border border-white/5 font-mono">${t}</span>`).join(' ');

                const card = document.createElement('div');
                card.className = "p-6 rounded-3xl glass-panel flex flex-col justify-between relative overflow-hidden group transition-all";
                card.setAttribute('data-category', p.category);
                card.setAttribute('data-name', p.name);
                card.setAttribute('data-quadrant', p.quadrant);
                card.setAttribute('data-tags', p.tags.join(' '));

                card.innerHTML = `
                    <div>
                        <div class="flex justify-between items-start gap-2 mb-3">
                            <span class="text-[9px] font-bold px-2.5 py-1 rounded-md border ${catColor} font-heading">${p.category}</span>
                            <div class="flex items-center gap-1.5">
                                <span class="text-[10px] text-slate-500 font-mono font-semibold"><i class="fa-solid fa-code-branch"></i> v${p.version}</span>
                                <span class="text-[10px] font-bold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 px-2 py-0.5 rounded font-mono text-[8px]">QGIS ${p.qgis_minimum_version}+</span>
                            </div>
                        </div>

                        <h3 class="text-base font-extrabold mb-1.5 group-hover:text-cyan-400 transition-colors truncate font-heading" title="${p.name}">${p.name}</h3>
                        <div class="flex flex-wrap gap-1 mb-3">
                            ${honorsHtml}
                        </div>

                        <div class="flex items-center justify-between mb-4">
                            ${quadBadge}
                            <span class="text-xs font-mono font-bold text-amber-400">${p.bayesian_rating.toFixed(2)} ★ <span class="text-[10px] text-slate-500 font-normal">(${p.votes_count})</span></span>
                        </div>

                        <div class="grid grid-cols-2 gap-4 bg-obsidian-950/70 p-3 rounded-2xl border border-white/5 mb-4">
                            <div>
                                <span class="text-[10px] text-slate-500 font-medium block font-mono">Downloads</span>
                                <span class="text-sm font-extrabold font-mono">${p.downloads.toLocaleString()}</span>
                            </div>
                            <div>
                                <span class="text-[10px] text-slate-500 font-medium block font-mono">Velocity</span>
                                <span class="text-sm font-extrabold text-cyan-400 font-mono">${Math.round(p.avg_monthly_downloads).toLocaleString()}/mo</span>
                            </div>
                        </div>

                        <div class="mb-4">
                            <div class="flex justify-between items-center text-[9px] font-bold text-slate-500 mb-1 font-mono">
                                <span>Milestone: ${p.next_milestone.toLocaleString()}</span>
                                <span class="text-emerald-400">${p.milestone_progress}%</span>
                            </div>
                            <div class="w-full bg-obsidian-800 rounded-full h-1">
                                <div class="bg-gradient-to-r from-emerald-500 to-teal-400 h-1 rounded-full" style="width: ${p.milestone_progress}%"></div>
                            </div>
                        </div>
                    </div>

                    <div class="mt-2 pt-3 border-t border-white/5 flex flex-col gap-2">
                        <div class="flex justify-between items-center text-[10px] text-slate-400 font-mono">
                            <span>Released: ${p.create_date}</span>
                            <div class="flex gap-2.5">
                                ${p.homepage ? `<a href="${p.homepage}" target="_blank" class="text-slate-400 hover:text-cyan-400 transition-colors" title="Docs"><i class="fa-solid fa-book text-sm"></i></a>` : ''}
                                ${p.repository ? `<a href="${p.repository}" target="_blank" class="text-slate-400 hover:text-white transition-colors" title="Repo"><i class="fa-brands fa-github text-sm"></i></a>` : ''}
                                ${p.tracker ? `<a href="${p.tracker}" target="_blank" class="text-slate-400 hover:text-rose-400 transition-colors" title="Issues"><i class="fa-solid fa-bug text-sm"></i></a>` : ''}
                            </div>
                        </div>
                        <div class="flex flex-wrap gap-1 mt-1">
                            ${tagsHtml}
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
        }

        let selectedCategory = 'All';
        function filterCardsCategory(cat) {
            selectedCategory = cat;
            const btns = { 'All': 'btn-cat-all', 'PlanX Suite': 'btn-cat-planx', '02 Suite': 'btn-cat-02', 'Standalone Plugins': 'btn-cat-standalone' };
            Object.keys(btns).forEach(key => {
                const btn = document.getElementById(btns[key]);
                if (btn) btn.className = (key === cat) ? "px-4 py-2 rounded-xl text-xs font-bold bg-cyan-600 text-white whitespace-nowrap" : "px-4 py-2 rounded-xl text-xs font-bold bg-obsidian-900 text-slate-400 hover:text-white border border-white/5 whitespace-nowrap";
            });
            applyCombinedFilters();
        }

        function filterCards() { applyCombinedFilters(); }

        function applyCombinedFilters() {
            const searchVal = document.getElementById('card-search-input').value.toUpperCase();
            const cards = document.getElementById('plugin-cards-container').getElementsByClassName('glass-panel');
            let matching = 0;

            for (let i = 0; i < cards.length; i++) {
                const card = cards[i];
                const cardCat = card.getAttribute('data-category');
                const cardName = card.getAttribute('data-name');
                const cardQuadrant = card.getAttribute('data-quadrant');
                const cardTags = card.getAttribute('data-tags');

                const matchesCat = (selectedCategory === 'All' || cardCat === selectedCategory);
                const matchesSearch = (cardName.toUpperCase().indexOf(searchVal) > -1 || cardTags.toUpperCase().indexOf(searchVal) > -1 || cardQuadrant.toUpperCase().indexOf(searchVal) > -1);

                let matchesActiveTags = true;
                if (activeTags.length > 0) {
                    matchesActiveTags = activeTags.every(t => cardTags.indexOf(t) > -1);
                }

                if (matchesCat && matchesSearch && matchesActiveTags) {
                    card.style.display = "";
                    matching++;
                } else {
                    card.style.display = "none";
                }
            }
            document.getElementById('matching-plugins-count').innerText = `${matching} plugins matching`;
        }

        let sortDirections = [true, true, true, true, true, true, true, true];
        function sortTable(colIndex) {
            const rows = Array.from(tbody.getElementsByTagName('tr'));
            const direction = sortDirections[colIndex];

            rows.sort((rowA, rowB) => {
                let cellA = rowA.getElementsByTagName('td')[colIndex].innerText.replace(/,/g, '');
                let cellB = rowB.getElementsByTagName('td')[colIndex].innerText.replace(/,/g, '');

                const numA = parseFloat(cellA);
                const numB = parseFloat(cellB);

                if (!isNaN(numA) && !isNaN(numB)) {
                    return direction ? numA - numB : numB - numA;
                }
                return direction ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
            });

            sortDirections[colIndex] = !direction;
            tbody.innerHTML = '';
            rows.forEach(r => tbody.appendChild(r));
        }

        function filterTableData() {
            const input = document.getElementById('table-search-input');
            const filter = input.value.toUpperCase();
            const rows = tbody.getElementsByTagName('tr');

            for (let i = 0; i < rows.length; i++) {
                const nameCol = rows[i].getElementsByTagName('td')[0];
                const catCol = rows[i].getElementsByTagName('td')[1];
                if (nameCol || catCol) {
                    const nameText = nameCol.textContent || nameCol.innerText;
                    const catText = catCol.textContent || catCol.innerText;
                    rows[i].style.display = (nameText.toUpperCase().indexOf(filter) > -1 || catText.toUpperCase().indexOf(filter) > -1) ? "" : "none";
                }
            }
        }

        function exportToCSV() {
            let csvContent = "data:text/csv;charset=utf-8,\\uFEFF";
            csvContent += "Plugin Name,Category,Release Date,Active Days,Downloads,Monthly Velocity,Bayesian Rating,Votes Count,Kinetic Regime\\n";

            appData.plugins.forEach(p => {
                const row = [
                    `"${p.name}"`,
                    `"${p.category}"`,
                    p.create_date,
                    p.days_active,
                    p.downloads,
                    p.avg_monthly_downloads,
                    p.bayesian_rating,
                    p.votes_count,
                    `"${p.kinetic_regime}"`
                ].join(",");
                csvContent += row + "\\n";
            });

            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", `qgis_plugin_governance_report_${new Date().toISOString().slice(0,10)}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        // =============================================================
        // SIMULATOR LOGIC WITH MULTI-SCENARIO TRAJECTORY CONE
        // =============================================================
        let simLineChart = null;

        function populateSimDropdown() {
            const dropdown = document.getElementById('sim-target-plugin');
            appData.plugins.forEach(p => {
                const opt = document.createElement('option');
                opt.value = p.name;
                opt.innerText = p.name;
                dropdown.appendChild(opt);
            });
        }

        function applySimPreset() {
            const select = document.getElementById('sim-growth-preset');
            const sliderContainer = document.getElementById('custom-slider-container');
            sliderContainer.style.display = select.value === 'custom' ? 'block' : 'none';
            runSimulation();
        }

        function updateSliderVal() {
            const val = parseInt(document.getElementById('sim-custom-speed').value);
            document.getElementById('custom-slider-val').innerText = `${val.toLocaleString()}/mo`;
            runSimulation();
        }

        function runSimulation() {
            const targetDateStr = document.getElementById('sim-target-date').value;
            const targetDate = new Date(targetDateStr);
            const refDate = new Date();

            const targetPlugin = document.getElementById('sim-target-plugin').value;
            const isAll = (targetPlugin === 'all');

            let baseDownloads = appData.summary.total_downloads;
            let currentMonthlyAvg = appData.summary.active_period_monthly_avg;

            if (!isAll) {
                const p = appData.plugins.find(x => x.name === targetPlugin);
                baseDownloads = p.downloads;
                currentMonthlyAvg = p.avg_monthly_downloads;
            }

            const timeDiff = targetDate.getTime() - refDate.getTime();
            const daysDiff = Math.max(0, Math.ceil(timeDiff / (1000 * 3600 * 24)));
            const monthsDiff = daysDiff / 30.4375;

            const presetSelect = document.getElementById('sim-growth-preset').value;
            let monthlySpeed = currentMonthlyAvg;

            if (presetSelect === 'custom') {
                monthlySpeed = parseInt(document.getElementById('sim-custom-speed').value);
            } else if (presetSelect === 'conservative') {
                monthlySpeed = isAll ? appData.summary.portfolio_overall_monthly_avg : currentMonthlyAvg * 0.7;
            } else if (presetSelect === 'optimistic') {
                monthlySpeed = isAll ? appData.summary.sum_individual_monthly_avgs : currentMonthlyAvg * 1.5;
            } else {
                monthlySpeed = isAll ? appData.summary.active_period_monthly_avg : currentMonthlyAvg;
            }

            const projectedAdditional = monthlySpeed * monthsDiff;
            const projectedTotal = baseDownloads + projectedAdditional;

            document.getElementById('sim-output-val').innerText = Math.round(projectedTotal).toLocaleString();
            document.getElementById('sim-output-growth').innerText = `+${Math.round(projectedAdditional).toLocaleString()} projected downloads`;

            drawSimulationCone(daysDiff, monthlySpeed, baseDownloads, targetPlugin);
        }

        function drawSimulationCone(daysDiff, monthlySpeed, baseDownloads, targetName) {
            const expectedData = [baseDownloads];
            const upperData = [baseDownloads];
            const lowerData = [baseDownloads];
            const categories = ['Today'];

            const stepDays = daysDiff / 5;
            const refDate = new Date();

            for (let i = 1; i <= 5; i++) {
                const stepDate = new Date(refDate.getTime() + (stepDays * i * 24 * 3600 * 1000));
                const label = stepDate.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
                categories.push(label);

                const currentDays = stepDays * i;
                const currentMonths = currentDays / 30.4375;

                expectedData.push(Math.round(baseDownloads + (monthlySpeed * currentMonths)));
                upperData.push(Math.round(baseDownloads + (monthlySpeed * 1.45 * currentMonths)));
                lowerData.push(Math.round(baseDownloads + (monthlySpeed * 0.65 * currentMonths)));
            }

            const isAlabaster = document.documentElement.getAttribute('data-theme') === 'alabaster';
            const labelColor = isAlabaster ? '#334155' : '#94a3b8';
            const gridColor = isAlabaster ? 'rgba(0, 0, 0, 0.06)' : 'rgba(255, 255, 255, 0.05)';

            const chartOptions = {
                series: [
                    { name: 'Bullish Acceleration (+45%)', data: upperData },
                    { name: 'Expected Run-Rate Trajectory', data: expectedData },
                    { name: 'Conservative Floor (-35%)', data: lowerData }
                ],
                chart: {
                    type: 'area',
                    height: 310,
                    toolbar: { show: false },
                    foreColor: labelColor
                },
                colors: ['#10b981', '#0ea5e9', '#f59e0b'],
                dataLabels: { enabled: false },
                stroke: { curve: 'smooth', width: [2, 3, 2], dashArray: [4, 0, 4] },
                fill: {
                    type: 'gradient',
                    gradient: {
                        shadeIntensity: 1,
                        opacityFrom: 0.25,
                        opacityTo: 0.02,
                        stops: [0, 100]
                    }
                },
                grid: { borderColor: gridColor },
                xaxis: {
                    categories: categories,
                    labels: { style: { fontFamily: 'JetBrains Mono' } }
                },
                yaxis: {
                    labels: {
                        formatter: function(val) { return Math.round(val).toLocaleString(); },
                        style: { fontFamily: 'JetBrains Mono' }
                    }
                },
                legend: { position: 'top', fontSize: '11px', markers: { radius: 6 } },
                tooltip: {
                    theme: isAlabaster ? 'light' : 'dark',
                    y: {
                        formatter: function(val) { return val.toLocaleString() + " downloads"; }
                    }
                }
            };

            const container = document.querySelector("#sim-line-chart");
            if (simLineChart) { try { simLineChart.destroy(); } catch (e) {} }
            container.innerHTML = '';
            simLineChart = new ApexCharts(container, chartOptions);
            simLineChart.render();

            document.getElementById('sim-chart-sub').innerText = `Multi-scenario adoption cone for "${targetName === 'all' ? 'Entire Portfolio' : targetName}"`;
        }

        // =============================================================
        // GLOBAL CHARTS INITIALIZATION
        // =============================================================
        let overviewBarChart = null;
        let overviewDonutChart = null;
        let suiteRadarChart = null;
        function renderBcgScatter() {
            const el = document.getElementById('bcg-scatter-chart');
            if (!el) return;
            const plugins = appData.plugins || [];
            const isAlabaster = document.documentElement.getAttribute('data-theme') === 'alabaster';
            const gridColor = isAlabaster ? 'rgba(0,0,0,0.07)' : 'rgba(255,255,255,0.06)';
            const labelColor = isAlabaster ? '#475569' : '#94a3b8';
            const catColors = { 'PlanX Suite': '#6366f1', '02 Suite': '#0ea5e9', 'Standalone Plugins': '#64748b' };
            const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

            const W = 820, H = 320, padL = 62, padR = 20, padT = 18, padB = 44;
            const dlVals = plugins.map(p => p.downloads);
            const vVals = plugins.map(p => Math.max(p.avg_monthly_downloads, 1));
            const minDl = Math.max(Math.min(...dlVals), 1), maxDl = Math.max(...dlVals);
            const minV = Math.max(Math.min(...vVals), 1), maxV = Math.max(...vVals);
            const lx = d => padL + (Math.log(d) - Math.log(minDl)) / ((Math.log(maxDl) - Math.log(minDl)) || 1) * (W - padL - padR);
            const ly = v => padT + (1 - (Math.log(v) - Math.log(minV)) / ((Math.log(maxV) - Math.log(minV)) || 1)) * (H - padT - padB);
            const fmt = t => t >= 1000 ? (Math.round(t / 100) / 10) + 'k' : Math.round(t);
            const ticks = (min, max, n) => {
                const lo = Math.log10(min), hi = Math.log10(max);
                const out = [];
                for (let i = 0; i <= n; i++) out.push(Math.pow(10, lo + (hi - lo) * i / n));
                return out;
            };

            let s = `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%">`;
            ticks(minDl, maxDl, 4).forEach(t => {
                const px = lx(t);
                s += `<line x1="${px}" y1="${padT}" x2="${px}" y2="${H - padB}" stroke="${gridColor}"/>`;
                s += `<text x="${px}" y="${H - padB + 18}" fill="${labelColor}" font-size="10" font-family="JetBrains Mono, monospace" text-anchor="middle">${fmt(t)}</text>`;
            });
            ticks(minV, maxV, 4).forEach(t => {
                const py = ly(t);
                s += `<line x1="${padL}" y1="${py}" x2="${W - padR}" y2="${py}" stroke="${gridColor}"/>`;
                s += `<text x="${padL - 6}" y="${py + 3}" fill="${labelColor}" font-size="10" font-family="JetBrains Mono, monospace" text-anchor="end">${fmt(t)}</text>`;
            });
            s += `<text x="${(padL + W - padR) / 2}" y="${H - 8}" fill="${labelColor}" font-size="11" font-family="Plus Jakarta Sans, sans-serif" font-weight="700" text-anchor="middle">Cumulative Downloads</text>`;
            s += `<text transform="rotate(-90 16 ${(padT + H - padB) / 2})" x="16" y="${(padT + H - padB) / 2}" fill="${labelColor}" font-size="11" font-family="Plus Jakarta Sans, sans-serif" font-weight="700" text-anchor="middle">Monthly Run-Rate (dl/mo)</text>`;

            const med = arr => arr.slice().sort((a, b) => a - b)[Math.floor(arr.length / 2)];
            const mx = lx(med(dlVals)), my = ly(med(vVals));
            s += `<line x1="${mx}" y1="${padT}" x2="${mx}" y2="${H - padB}" stroke="${labelColor}" stroke-dasharray="4 5" opacity="0.45"/>`;
            s += `<line x1="${padL}" y1="${my}" x2="${W - padR}" y2="${my}" stroke="${labelColor}" stroke-dasharray="4 5" opacity="0.45"/>`;

            plugins.forEach(p => {
                const px = lx(p.downloads), py = ly(Math.max(p.avg_monthly_downloads, 1));
                const color = catColors[p.category] || '#64748b';
                const tip = `${esc(p.name)} · ${p.downloads.toLocaleString()} downloads · ${Math.round(p.avg_monthly_downloads).toLocaleString()}/mo · ${p.category}`;
                if (p.icon) {
                    s += `<g transform="translate(${(px - 16).toFixed(1)} ${(py - 16).toFixed(1)})" style="cursor:pointer"><title>${tip}</title><circle cx="16" cy="16" r="19" fill="${color}" opacity="0.15"/><image href="${p.icon}" x="4" y="4" width="24" height="24" preserveAspectRatio="xMidYMid meet"/><circle cx="16" cy="16" r="19" fill="none" stroke="${color}" stroke-width="1.5" opacity="0.55"/></g>`;
                } else {
                    s += `<g transform="translate(${px} ${py})" style="cursor:pointer"><title>${tip}</title><circle r="6" fill="${color}"/></g>`;
                }
            });
            s += '</svg>';
            el.innerHTML = s;
        }

        function initializeCharts() {
            const isAlabaster = document.documentElement.getAttribute('data-theme') === 'alabaster';
            const labelColor = isAlabaster ? '#334155' : '#94a3b8';
            const gridColor = isAlabaster ? 'rgba(0, 0, 0, 0.06)' : 'rgba(255, 255, 255, 0.05)';

            if (overviewBarChart) overviewBarChart.destroy();
            if (overviewDonutChart) overviewDonutChart.destroy();
            if (suiteRadarChart) suiteRadarChart.destroy();

            // 1. Horizontal Bar Chart
            const names = appData.plugins.map(p => p.name);
            const downloads = appData.plugins.map(p => p.downloads);

            const barOptions = {
                series: [{
                    name: 'Downloads',
                    data: downloads
                }],
                chart: {
                    type: 'bar',
                    height: 400,
                    toolbar: { show: false },
                    foreColor: labelColor
                },
                plotOptions: {
                    bar: {
                        borderRadius: 5,
                        horizontal: true,
                        barHeight: '75%',
                        distributed: true
                    }
                },
                colors: [
                    '#0284c7', '#0ea5e9', '#38bdf8', '#6366f1', '#818cf8',
                    '#10b981', '#34d399', '#f59e0b', '#fbbf24', '#f43f5e',
                    '#a855f7', '#c084fc', '#64748b', '#94a3b8', '#cbd5e1'
                ],
                dataLabels: {
                    enabled: true,
                    textAnchor: 'start',
                    style: {
                        colors: ['#fff'],
                        fontWeight: '600',
                        fontSize: '10px',
                        fontFamily: 'JetBrains Mono'
                    },
                    formatter: function (val) { return val.toLocaleString(); },
                    offsetX: 6
                },
                xaxis: {
                    categories: names,
                    labels: {
                        formatter: function(val) { return Math.round(val).toLocaleString(); },
                        style: { fontFamily: 'JetBrains Mono' }
                    }
                },
                yaxis: {
                    labels: {
                        maxWidth: 220,
                        style: { fontWeight: '700', fontFamily: 'Plus Jakarta Sans' }
                    }
                },
                grid: {
                    borderColor: gridColor,
                    xaxis: { lines: { show: true } }
                },
                legend: { show: false },
                tooltip: {
                    theme: isAlabaster ? 'light' : 'dark',
                    y: {
                        formatter: function(val) { return val.toLocaleString() + " downloads"; }
                    }
                }
            };

            overviewBarChart = new ApexCharts(document.querySelector("#overview-bar-chart"), barOptions);
            overviewBarChart.render();

            // 2. Donut Chart
            const planxDownloads = appData.summary.categories["PlanX Suite"]?.downloads || 0;
            const suite02Downloads = appData.summary.categories["02 Suite"]?.downloads || 0;
            const standaloneDownloads = appData.summary.categories["Standalone Plugins"]?.downloads || 0;

            const donutOptions = {
                series: [planxDownloads, suite02Downloads, standaloneDownloads],
                chart: {
                    type: 'donut',
                    height: 280,
                    foreColor: labelColor
                },
                labels: ['PlanX Suite', '02 Suite', 'Standalone'],
                colors: ['#6366f1', '#0ea5e9', '#64748b'],
                stroke: {
                    show: true,
                    colors: [isAlabaster ? '#ffffff' : '#0b111e'],
                    width: 2
                },
                legend: {
                    position: 'bottom',
                    fontSize: '11px',
                    markers: { radius: 12 }
                },
                plotOptions: {
                    pie: {
                        donut: {
                            size: '68%',
                            labels: {
                                show: true,
                                name: { show: true },
                                value: {
                                    show: true,
                                    formatter: function(val) { return parseInt(val).toLocaleString(); },
                                    style: { fontFamily: 'JetBrains Mono' }
                                },
                                total: {
                                    show: true,
                                    label: 'Total',
                                    formatter: function() { return appData.summary.total_downloads.toLocaleString(); },
                                    style: { fontFamily: 'JetBrains Mono' }
                                }
                            }
                        }
                    }
                },
                tooltip: {
                    theme: isAlabaster ? 'light' : 'dark',
                    y: {
                        formatter: function(val, { seriesIndex, w }) {
                            const percent = w.globals.seriesPercent[seriesIndex][0];
                            return `${val.toLocaleString()} downloads (${percent.toFixed(1)}%)`;
                        }
                    }
                }
            };

            overviewDonutChart = new ApexCharts(document.querySelector("#overview-donut-chart"), donutOptions);
            overviewDonutChart.render();

            // 3. BCG Scatter Matrix — custom SVG with each plugin's own icon as the node
            renderBcgScatter();

            // 4. Suite Capability Radar Chart
            const radarOptions = {
                series: [
                    {
                        name: 'PlanX Suite',
                        data: [85, 92, 88, 90, 95, 82]
                    },
                    {
                        name: '02 Suite',
                        data: [90, 86, 78, 85, 80, 88]
                    },
                    {
                        name: 'Standalone',
                        data: [65, 80, 70, 75, 60, 70]
                    }
                ],
                chart: {
                    height: 310,
                    type: 'radar',
                    toolbar: { show: false },
                    foreColor: labelColor
                },
                colors: ['#6366f1', '#0ea5e9', '#64748b'],
                stroke: { width: 2 },
                fill: { opacity: 0.2 },
                markers: { size: 4 },
                xaxis: {
                    categories: [
                        'Adoption Velocity',
                        'Rating Health',
                        'Maturity / Age',
                        'Global Reach',
                        'Ecosystem Depth',
                        'User Engagement'
                    ],
                    labels: { style: { fontFamily: 'Inter', fontSize: '10px' } }
                },
                yaxis: { show: false, min: 0, max: 100 },
                legend: { position: 'bottom', fontSize: '11px', markers: { radius: 6 } }
            };

            suiteRadarChart = new ApexCharts(document.querySelector("#suite-radar-chart"), radarOptions);
            suiteRadarChart.render();
        }

        document.addEventListener("DOMContentLoaded", function() {
            renderKPIs();
            renderMilestones();
            renderAuditKPIsAndAlerts();
            renderTagFilterChips();
            renderTableData('all');
            renderCards();
            populateSimDropdown();
            initializeCharts();
            runSimulation();
            initializePipelines();
        });
    </script>
</body>
</html>
"""

    html_output = html_template.replace("##WORLD_SVG_LAYER##", world_svg_layer_html).replace("##DATA_INJECTION##", json.dumps(embedded_data, ensure_ascii=False, indent=2))

    local_output_path = os.path.join(os.path.dirname(__file__), "qgis_plugins_dashboard.html")
    index_output_path = os.path.join(os.path.dirname(__file__), "index.html")

    with open(local_output_path, "w", encoding="utf-8") as f:
        f.write(html_output)

    with open(index_output_path, "w", encoding="utf-8") as f:
        f.write(html_output)

    print(f"[5/5] Success: Clean, elite studio generated at: {local_output_path} and {index_output_path}")

except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
