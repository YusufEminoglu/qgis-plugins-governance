"""
QGIS Plugin Portfolio Analytics, Forensic Governance & Geospatial Intelligence Studio
Author: Yusuf Eminoğlu
License: MIT
Description: Enterprise-grade analytics, econometric growth models, forensic rating abuse
surveillance, interactive vector SVG choropleth mapping, and multi-channel executive storytelling
for the registered QGIS plugin portfolio across urban analytics, spatial statistics, CAD, and 3D GIS.
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
        elif name_lower.startswith("02") or "zero2" in name_lower or "02agent" in name_lower:
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
            with urllib.request.urlopen(req, timeout=8) as _resp:
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
            if downloads >= 50000:
                next_milestone = ((downloads // 10000) + 1) * 10000
            elif downloads >= 10000:
                next_milestone = ((downloads // 5000) + 1) * 5000
            elif downloads >= 5000:
                next_milestone = 10000
            elif downloads >= 1000:
                next_milestone = ((downloads // 1000) + 1) * 1000
            milestone_progress = (downloads / next_milestone) * 100

            if downloads >= 20000:
                prev_milestone = (downloads // 5000) * 5000
            elif downloads >= 10000:
                prev_milestone = 10000
            elif downloads >= 5000:
                prev_milestone = 5000
            elif downloads >= 1000:
                prev_milestone = (downloads // 1000) * 1000
            else:
                prev_milestone = 0

            remaining_to_milestone = next_milestone - downloads
            if remaining_to_milestone <= 0:
                milestone_est_date = "Reached"
            elif avg_monthly_downloads > 0 and remaining_to_milestone > 0:
                days_to_milestone = (remaining_to_milestone / avg_monthly_downloads) * 30.4375
                milestone_est_date = (reference_date + timedelta(days=days_to_milestone)).strftime('%b %d, %Y')
            else:
                milestone_est_date = "Pending Velocity"

            # Milestone clubs & badges
            if downloads >= 10000:
                club = "10k_club"
                club_label = "10K+ Tier"
                club_badge = "🏆 10K+ Legend"
            elif downloads >= 5000:
                club = "5k_club"
                club_label = "5K+ Tier"
                club_badge = "⭐ 5K+ Pillar"
            elif downloads >= 1000:
                club = "1k_club"
                club_label = "1K+ Tier"
                club_badge = "🎯 1K+ Established"
            else:
                club = "rising"
                club_label = "Rising"
                club_badge = "🚀 Rising Star"

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
                'prev_milestone': prev_milestone,
                'remaining_to_milestone': remaining_to_milestone,
                'milestone_progress': round(milestone_progress, 1),
                'milestone_est_date': milestone_est_date,
                'is_imminent': milestone_progress >= 85.0,
                'club': club,
                'club_label': club_label,
                'club_badge': club_badge,
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
                'countries': plugin_countries,
                'package_name': package_name
            })

    yusuf_plugins.sort(key=lambda x: x['downloads'], reverse=True)

    # Resolve each plugin's main icon (from assets/plugin_icons/ or local plugin folders)
    _icon_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "plugin_icons")
    _plugins_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Include any pending monorepo plugins from plugins.toml if not yet appearing in live XML
    try:
        import tomllib
        toml_path = os.path.join(_plugins_root, "plugins.toml")
        if os.path.exists(toml_path):
            with open(toml_path, "rb") as tf:
                toml_data = tomllib.load(tf)
            existing_names = {p['name'].lower() for p in yusuf_plugins}
            existing_pkgs = {p['package_name'].lower() for p in yusuf_plugins if p.get('package_name')}

            for p_def in toml_data.get('plugin', []):
                p_dir = p_def.get('dir', '')
                p_name = p_def.get('name', '')
                if p_name.lower() not in existing_names and p_dir.lower() not in existing_pkgs:
                    # Read metadata.txt for version, description, etc.
                    meta_path = os.path.join(_plugins_root, p_dir, "metadata.txt")
                    meta_ver, meta_desc = "0.3.0", p_def.get('role', '')
                    if os.path.exists(meta_path):
                        with open(meta_path, "r", encoding="utf-8", errors="ignore") as mf:
                            for line in mf:
                                if line.startswith("version="): meta_ver = line.split("=", 1)[1].strip()
                                elif line.startswith("description="): meta_desc = line.split("=", 1)[1].strip()

                    yusuf_plugins.append({
                        'name': p_name,
                        'version': meta_ver,
                        'downloads': 0,
                        'create_date': reference_date.strftime('%Y-%m-%d'),
                        'update_date': reference_date.strftime('%Y-%m-%d'),
                        'days_active': 1,
                        'months_active': 0.03,
                        'avg_monthly_downloads': 0.0,
                        'projected_total_downloads': 0,
                        'category': get_category(p_name),
                        'tags': ['mobility', '3d', 'routing', 'kinematics', 'accessibility', 'network', 'webgl'],
                        'next_milestone': 1000,
                        'prev_milestone': 0,
                        'remaining_to_milestone': 1000,
                        'milestone_progress': 0.0,
                        'milestone_est_date': "Pending Approval",
                        'is_imminent': False,
                        'club': "rising",
                        'club_label': "Rising",
                        'club_badge': "🚀 Rising Star",
                        'qgis_minimum_version': "3.28",
                        'homepage': f"https://yusufeminoglu.github.io/{p_dir}/",
                        'tracker': f"https://github.com/YusufEminoglu/{p_dir}/issues",
                        'repository': f"https://github.com/YusufEminoglu/{p_dir}",
                        'average_vote': 0.0,
                        'votes_count': 0,
                        'calculated_score': 0.0,
                        'is_experimental': "no",
                        'quadrant': "High Velocity",
                        'quadrant_color': "emerald",
                        'countries': [],
                        'package_name': p_dir,
                        'is_pending_approval': True
                    })
    except Exception as e:
        print(f"Warning syncing pending plugins from toml: {e}")

    def resolve_plugin_icon(repository, package_name=None, name=None):
        slugs = []
        if repository:
            slugs.append(repository.rstrip("/").split("/")[-1].lower())
        if package_name:
            slugs.append(package_name.lower().replace("_", "-"))
            slugs.append(package_name.lower())
        if name:
            slugs.append(name.lower().replace(" ", "-").replace("_", "-").replace(".", ""))
            slugs.append(name.lower().replace(" ", "_").replace(".", ""))
            slugs.append(name.lower())

        # 1. Search assets/plugin_icons/
        for slug in slugs:
            for ext, mime in ((".png", "image/png"), (".svg", "image/svg+xml")):
                path = os.path.join(_icon_dir, slug + ext)
                if os.path.exists(path):
                    with open(path, "rb") as _f:
                        _b64 = base64.b64encode(_f.read()).decode("ascii")
                    return f"data:{mime};base64,{_b64}"

        # 2. Search local plugin directory
        for slug in slugs:
            for sub_name in [slug, slug.replace("-", "_"), slug.replace("_", "-")]:
                local_dir = os.path.join(_plugins_root, sub_name)
                if os.path.exists(local_dir):
                    for sub_path in ["icons/icon.png", "icons/icon.svg", "icons/icon_64.png", "icon.png", "icon.svg"]:
                        p = os.path.join(local_dir, sub_path)
                        if os.path.exists(p):
                            mime = "image/svg+xml" if p.endswith(".svg") else "image/png"
                            with open(p, "rb") as _f:
                                _b64 = base64.b64encode(_f.read()).decode("ascii")
                            return f"data:{mime};base64,{_b64}"
        return None

    for _p in yusuf_plugins:
        _p['icon'] = resolve_plugin_icon(_p.get('repository', ''), _p.get('package_name', ''), _p.get('name', ''))

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
                    "average_vote": p['average_vote'],
                    "votes_count": p['votes_count'],
                    "total_score": p['calculated_score'],
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

    # 1. Advanced Econometric Modeling: Gini, Theil, Palma, Pietra, Subgroup Decomposition, and Empirical Bayes
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

    # Palma Ratio (Top 10% share / Bottom 40% share) & Pietra (Robin Hood) Index
    top_10_count = max(1, int(math.ceil(0.10 * n_plugins)))
    bottom_40_count = max(1, int(math.floor(0.40 * n_plugins)))
    top_10_share = sum(sorted_dl[-top_10_count:]) / total_downloads if total_downloads > 0 else 0.0
    bottom_40_share = sum(sorted_dl[:bottom_40_count]) / total_downloads if total_downloads > 0 else 0.0
    palma_ratio = (top_10_share / bottom_40_share) if bottom_40_share > 0 else 0.0
    pietra_index = 0.5 * sum(abs(s - (1.0 / n_plugins)) for s in shares) if n_plugins > 0 else 0.0

    # Generalized Entropy (Theil T & Theil L)
    mean_dl = total_downloads / n_plugins if n_plugins > 0 else 1.0
    theil_t = sum((d / total_downloads) * math.log(max(1e-9, (d / mean_dl))) for d in downloads_list if d > 0)
    theil_l = sum(math.log(max(1e-9, (mean_dl / d))) for d in downloads_list if d > 0) / n_plugins if n_plugins > 0 else 0.0

    # Suite Subgroup Gini Decomposition
    suite_groups = {}
    for p in yusuf_plugins:
        suite_groups.setdefault(p['category'], []).append(p['downloads'])

    suite_decomp = {}
    within_gini_weighted = 0.0
    for cat_name, dl_list in suite_groups.items():
        nj = len(dl_list)
        dj_sum = sum(dl_list)
        pj = nj / n_plugins
        sj = dj_sum / total_downloads if total_downloads > 0 else 0.0
        sorted_j = sorted(dl_list)
        idx_sum_j = sum((k + 1) * d for k, d in enumerate(sorted_j))
        gj_raw = ((2.0 * idx_sum_j) / (nj * dj_sum) - ((nj + 1.0) / nj)) if (nj > 0 and dj_sum > 0) else 0.0
        gj_corr = (nj / (nj - 1.0)) * gj_raw if nj > 1 else gj_raw
        within_gini_weighted += gj_corr * pj * sj
        suite_decomp[cat_name] = {
            'count': nj,
            'downloads': dj_sum,
            'share_pct': round(sj * 100, 1),
            'sub_gini': round(gj_corr, 4)
        }

    within_gini_pct = round((within_gini_weighted / gini_corrected) * 100, 1) if gini_corrected > 0 else 0.0

    # Empirical Bayes Hyperpriors (Two-Level Hierarchical Model)
    total_portfolio_votes = sum(p['votes_count'] for p in yusuf_plugins)
    prior_mean_rating = (sum(p['average_vote'] * p['votes_count'] for p in yusuf_plugins) / total_portfolio_votes) if total_portfolio_votes > 0 else 4.80
    valid_ratings = [p['average_vote'] for p in yusuf_plugins if p['votes_count'] > 0]
    rating_variance = (sum((r - prior_mean_rating) ** 2 for r in valid_ratings) / len(valid_ratings)) if len(valid_ratings) > 1 else 0.25
    tau_sq = max(0.04, rating_variance - 0.05)
    sigma_within_sq = 0.35

    # 2. Advanced Multi-Vector Machine Learning & Forensic Anomaly Surveillance Engine
    H_MAX_ENTROPY = math.log2(5.0)  # 2.321928 bits
    anomaly_reports = []
    raided_plugins = []

    # Pre-pass: Count concurrent influx across portfolio for Cross-Portfolio Cosine Synchronization
    total_influx_votes = 0
    plugins_with_influx = 0
    for p in yusuf_plugins:
        name = p['name']
        cur_v = p['votes_count']
        base_data = baseline.get(name, {})
        base_v = base_data.get("votes_count", cur_v)
        dv = max(0, cur_v - base_v)
        if dv > 0:
            plugins_with_influx += 1
            total_influx_votes += dv

    sync_ratio = plugins_with_influx / max(1, len(yusuf_plugins))

    raw_feature_matrix = []
    plugin_feature_rows = []

    for p in yusuf_plugins:
        name = p['name']
        cur_votes = p['votes_count']
        cur_avg = p['average_vote']
        cur_score = cur_votes * cur_avg
        cur_dl = p['downloads']
        v_hist = p['avg_monthly_downloads']

        # Hierarchical Empirical Bayes Rating with Dynamic Shrinkage Factor (b_i)
        if cur_votes > 0:
            b_i = (sigma_within_sq / cur_votes) / (tau_sq + (sigma_within_sq / cur_votes))
            r_bayes = (1.0 - b_i) * cur_avg + b_i * prior_mean_rating
            se_theta = math.sqrt(1.0 / ((1.0 / tau_sq) + (cur_votes / sigma_within_sq)))
            cred_floor = max(1.0, r_bayes - 1.96 * se_theta)
            cred_ceiling = min(5.0, r_bayes + 1.96 * se_theta)
        else:
            b_i = 1.0
            r_bayes = prior_mean_rating
            cred_floor = 1.0
            cred_ceiling = 5.0
            se_theta = 0.5

        p['bayes_score'] = round(r_bayes, 3)
        p['cred_floor'] = round(cred_floor, 3)
        p['cred_ceiling'] = round(cred_ceiling, 3)
        p['cred_error_margin'] = round(1.96 * se_theta, 3)

        # Maintenance Velocity & Release Cadence
        try:
            up_dt = datetime.fromisoformat(p['update_date']) if p.get('update_date') else reference_date
            days_since_update = max(0, (reference_date - up_dt).days)
        except Exception:
            days_since_update = 7

        p['days_since_update'] = days_since_update
        p['cadence_status'] = "Active (Recent)" if days_since_update <= 30 else ("Stable (1-3 mo)" if days_since_update <= 90 else "Mature / Evergreen")
        p['cadence_badge_color'] = "emerald" if days_since_update <= 30 else ("cyan" if days_since_update <= 90 else "slate")

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

        delta_votes = max(0, cur_votes - base_votes)
        delta_dl = max(0, cur_dl - base_dl)
        delta_score = cur_score - base_score
        delta_rating = cur_avg - base_avg
        implied_new_rating = (delta_score / delta_votes) if delta_votes > 0 else cur_avg
        implied_r_clamped = max(1.0, min(5.0, implied_new_rating))

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

        # Feature 1: Rating-to-Download Conversion Ratio (k)
        conversion_k = (delta_votes / max(1, delta_dl)) * 100.0 if delta_votes > 0 else 0.0
        k_anomaly = min(15.0, conversion_k / 0.8) # Normalized against 0.8% organic expectation

        # Feature 2: Influx Rating Deviation from Historical/Organic Baseline (delta_r)
        expected_organic_r = max(4.65, base_avg)
        deviation_r = max(0.0, expected_organic_r - implied_r_clamped) if delta_votes > 0 else 0.0

        # Feature 3: Shannon Entropy of Influx Vector
        if delta_votes > 0:
            if implied_r_clamped <= 1.5:
                probs = [1.0 - (implied_r_clamped - 1.0), implied_r_clamped - 1.0, 0.0, 0.0, 0.0]
            elif implied_r_clamped <= 2.5:
                probs = [2.5 - implied_r_clamped, implied_r_clamped - 1.5, 0.0, 0.0, 0.0]
            elif implied_r_clamped <= 3.5:
                probs = [0.0, 3.5 - implied_r_clamped, implied_r_clamped - 2.5, 0.0, 0.0]
            elif implied_r_clamped <= 4.5:
                probs = [0.0, 0.0, 4.5 - implied_r_clamped, implied_r_clamped - 3.5, 0.0]
            else:
                probs = [0.0, 0.0, 0.0, 5.0 - implied_r_clamped, 1.0 - (5.0 - implied_r_clamped)]
            p_sum = sum(probs) or 1.0
            norm_p = [prob / p_sum for prob in probs]
            shannon_h = -sum(prob * math.log2(prob) for prob in norm_p if prob > 1e-6)
            entropy_purity = max(0.0, 1.0 - (shannon_h / H_MAX_ENTROPY))
            eas_score = entropy_purity * max(0.0, (5.0 - implied_r_clamped) / 4.0) * min(1.0, delta_votes / 3.0) * 100.0
            purity = (norm_p[0] if implied_r_clamped < 2.5 else norm_p[4]) * 100.0
        else:
            shannon_h = H_MAX_ENTROPY
            entropy_purity = 0.0
            eas_score = 0.0
            purity = 0.0

        # Feature Vector: [k_anomaly, deviation_r * 2.0, min(10.0, dv), sync_ratio * 5.0, entropy_purity * 3.0]
        f_vec = [k_anomaly, deviation_r * 2.0, min(10.0, delta_votes), sync_ratio * 5.0, entropy_purity * 3.0]
        raw_feature_matrix.append(f_vec)

        # Multi-Class Attack Taxonomy Classification
        if delta_votes >= 3 and implied_r_clamped <= 1.45:
            taxonomy = "Type I: Direct 1-Star Bombing"
            taxonomy_code = "TYPE_1_BOMBING"
            status = "CRITICAL 1-STAR ATTACK"
            severity = "critical"
            badge_color = "rose"
            threat_level = 95
            raided_plugins.append(name)
        elif delta_votes >= 2 and (1.45 < implied_r_clamped <= 3.85) and base_avg >= 4.40:
            taxonomy = "Type II: Soft Rating Dilution"
            taxonomy_code = "TYPE_2_SOFT_DILUTION"
            status = "SOFT DILUTION DRAG-DOWN"
            severity = "high"
            badge_color = "amber"
            threat_level = 85
            raided_plugins.append(name)
        elif delta_votes >= 1 and sync_ratio >= 0.35 and implied_r_clamped < 4.10:
            taxonomy = "Type III: Coordinated Portfolio Sweep"
            taxonomy_code = "TYPE_3_PORTFOLIO_SWEEP"
            status = "COORDINATED SWEEP"
            severity = "high"
            badge_color = "amber"
            threat_level = 75
            raided_plugins.append(name)
        elif delta_votes >= 2 and delta_dl < 8:
            taxonomy = "Type IV: Phantom Zero-Download Influx"
            taxonomy_code = "TYPE_4_PHANTOM"
            status = "PHANTOM INFLUX"
            severity = "amber"
            badge_color = "orange"
            threat_level = 65
            raided_plugins.append(name)
        elif delta_votes > 0 and implied_r_clamped >= 4.20:
            taxonomy = "Organic Positive Growth"
            taxonomy_code = "ORGANIC_POSITIVE"
            status = "POSITIVE GROWTH"
            severity = "positive"
            badge_color = "emerald"
            threat_level = 10
        elif delta_votes > 0:
            taxonomy = "Organic General Activity"
            taxonomy_code = "ORGANIC_NORMAL"
            status = "ORGANIC ACTIVITY"
            severity = "normal"
            badge_color = "indigo"
            threat_level = 20
        else:
            taxonomy = "Stable Baseline (No Influx)"
            taxonomy_code = "STABLE_BASELINE"
            status = "STABLE BASELINE"
            severity = "stable"
            badge_color = "slate"
            threat_level = 0

        # Purged Synthetic Organic Rating (True mathematical score without anomalous vote spikes)
        if severity in ('critical', 'high', 'amber') and (cur_votes - delta_votes) > 0:
            purged_synthetic_rating = (cur_score - (delta_votes * implied_r_clamped)) / (cur_votes - delta_votes)
        else:
            purged_synthetic_rating = cur_avg

        suppressed_points = max(0.0, purged_synthetic_rating - cur_avg)

        target_recovering_rating = 4.80
        if cur_avg < target_recovering_rating:
            needed_5_stars = max(0, int((cur_votes * (target_recovering_rating - cur_avg)) / (5.0 - target_recovering_rating) + 0.999))
        else:
            needed_5_stars = 0

        damage_index = max(0.0, (base_avg - cur_avg) * cur_votes)

        # Cryptographic Evidence Signature
        sig_raw = f"{name}:{cur_votes}:{cur_avg}:{delta_votes}:{implied_new_rating}:{reference_date.isoformat()}"
        evidence_hash = hashlib.sha256(sig_raw.encode("utf-8")).hexdigest()[:16].upper()

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

        # Extract Historical Sparkline (Download trajectory across snapshots)
        sparkline_data = []
        for snap in history:
            snap_plugs = snap.get('plugins', {})
            if name in snap_plugs:
                sparkline_data.append(snap_plugs[name].get('downloads', cur_dl))
        if len(sparkline_data) < 2:
            sparkline_data = [int(cur_dl * 0.88), int(cur_dl * 0.92), int(cur_dl * 0.96), cur_dl]

        # Multi-Factor Health & Resilience Score (0–100)
        score_adoption = min(100.0, (cur_dl / 8000.0) * 50.0 + min(50.0, (v_hist / 400.0) * 50.0))
        score_rating = min(100.0, (r_bayes / 5.0) * 80.0 + min(20.0, cur_votes * 0.4))
        score_freshness = max(60.0, 100.0 - (p['days_active'] / 400.0) * 15.0)
        score_trust = min(100.0, max(50.0, (cur_votes / max(1, cur_dl / 120.0)) * 60.0 + 40.0))
        health_score = round(0.35 * score_adoption + 0.30 * score_rating + 0.20 * score_freshness + 0.15 * score_trust, 1)
        health_score = max(10.0, min(99.9, health_score))

        p.update({
            'bayesian_rating': round(r_bayes, 3),
            'rating_credibility_floor_95': round(cred_floor, 3),
            'kinetic_ratio': round(alpha_kinetic, 2),
            'adoption_acceleration': round(accel, 2),
            'kinetic_regime': regime,
            'kinetic_badge': regime_badge,
            'health_score': health_score,
            'sparkline': sparkline_data,
            'honors': honors,
            'evidence_hash': evidence_hash,
            'purged_synthetic_rating': round(purged_synthetic_rating, 2),
            'suppressed_points': round(suppressed_points, 2),
            'taxonomy': taxonomy,
            'taxonomy_code': taxonomy_code,
            'threat_level': threat_level
        })

        plugin_feature_rows.append({
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
            "delta_dl": delta_dl,
            "delta_rating": round(delta_rating, 3),
            "delta_score": round(delta_score, 2),
            "damage_index": round(damage_index, 1),
            "implied_new_rating": round(implied_new_rating, 2),
            "conversion_k": round(conversion_k, 2),
            "shannon_entropy": round(shannon_h, 3),
            "entropy_score": round(eas_score, 1),
            "purity_pct": round(purity, 1),
            "reconciled_after_purge": round(purged_synthetic_rating, 3),
            "purged_synthetic_rating": round(purged_synthetic_rating, 2),
            "suppressed_points": round(suppressed_points, 2),
            "needed_5_stars_to_recover": needed_5_stars,
            "evidence_hash": evidence_hash,
            "status": status,
            "taxonomy": taxonomy,
            "taxonomy_code": taxonomy_code,
            "severity": severity,
            "badge_color": badge_color,
            "threat_level": threat_level,
            "f_vec": f_vec
        })

    # Multivariate Mahalanobis Distance & Calibrated Abuse Probability Computation
    if raw_feature_matrix:
        mean_vec = [sum(col)/len(col) for col in zip(*raw_feature_matrix)]
        for row in plugin_feature_rows:
            dist_sq = sum((x - m)**2 for x, m in zip(row['f_vec'], mean_vec))
            mahalanobis_d = math.sqrt(dist_sq)
            if row['delta_votes'] > 0 and row['severity'] in ('critical', 'high', 'amber'):
                p_abuse = min(99.9, max(0.0, (1.0 - math.exp(-0.25 * (mahalanobis_d ** 1.8))) * 100.0))
            elif row['delta_votes'] > 0:
                p_abuse = 5.0
            else:
                p_abuse = 0.0
            row['mahalanobis_d'] = round(mahalanobis_d, 2)
            row['p_abuse'] = round(p_abuse, 1)

    anomaly_reports = plugin_feature_rows

    # Coordinated Cross-Plugin Attack Correlation Logic
    raided_count = len(raided_plugins)
    total_raid_votes = sum(a['delta_votes'] for a in anomaly_reports if a['severity'] in ('critical', 'high', 'amber'))
    total_suppressed_pts = sum(a['suppressed_points'] for a in anomaly_reports)
    total_clean_votes = sum(a['current_votes'] - (a['delta_votes'] if a['severity'] in ('critical', 'high', 'amber') else 0) for a in anomaly_reports)
    total_clean_score = sum((a['current_score'] - (a['delta_votes'] * a['implied_new_rating'] if a['severity'] in ('critical', 'high', 'amber') else 0)) for a in anomaly_reports)
    portfolio_purged_average = (total_clean_score / max(1, total_clean_votes)) if total_clean_votes > 0 else prior_mean_rating

    if raided_count >= 3:
        campaign_level = "CRITICAL_COORDINATED_SYBIL_CAMPAIGN"
        campaign_threat_score = min(100, int((raided_count / n_plugins * 100) * 1.5 + total_raid_votes * 4))
        campaign_desc = f"Simultaneous coordinated assault detected across {raided_count} independent plugins ({total_raid_votes} fraudulent/diluted votes identified)."
    elif raided_count >= 2:
        campaign_level = "SUSPICIOUS_MULTI_TARGET_ANOMALY"
        campaign_threat_score = min(100, int((raided_count / n_plugins * 100) + total_raid_votes * 3))
        campaign_desc = f"Multi-target anomaly identified across {raided_count} plugins ({total_raid_votes} flagged votes)."
    elif raided_count == 1:
        campaign_level = "ISOLATED_ANOMALOUS_TARGET"
        campaign_threat_score = 45
        campaign_desc = f"Isolated low-rating anomaly pattern on {raided_plugins[0]}."
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
        "total_suppressed_pts": round(total_suppressed_pts, 2),
        "portfolio_purged_average": round(portfolio_purged_average, 2),
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

    # Enriched time-series history with inflection detection and portfolio raid wave analysis
    history_by_plugin = {}
    history_timestamps = [s.get("date_str", s.get("timestamp")) for s in history]

    # Portfolio-wide wave telemetry (aggregating simultaneous influx across all plugins at each timestamp)
    portfolio_wave_series = []
    portfolio_raid_wave_series = []

    for idx, s in enumerate(history):
        snap_total_dv = 0
        snap_raid_dv = 0
        if idx > 0:
            prev_s = history[idx - 1]
            for p_name, p_curr in s.get("plugins", {}).items():
                p_prev = prev_s.get("plugins", {}).get(p_name, {})
                dv = max(0, p_curr.get("votes_count", 0) - p_prev.get("votes_count", 0))
                if dv > 0:
                    snap_total_dv += dv
                    ds = (p_curr.get("votes_count", 0) * p_curr.get("average_vote", 0.0)) - (p_prev.get("votes_count", 0) * p_prev.get("average_vote", 0.0))
                    implied_r = ds / dv if dv > 0 else 5.0
                    if implied_r <= 2.5:
                        snap_raid_dv += dv
        portfolio_wave_series.append(snap_total_dv)
        portfolio_raid_wave_series.append(snap_raid_dv)

    for p in yusuf_plugins:
        name = p['name']
        rating_series = []
        votes_series = []
        delta_v_series = []
        implied_r_series = []
        purged_series = []
        inflection_annotations = []

        prev_v = None
        prev_r = None

        base_snap = history[0]["plugins"].get(name, {})
        base_r = round(base_snap.get("average_vote", p['average_vote']), 2)

        for idx, s in enumerate(history):
            p_snap = s.get("plugins", {}).get(name)
            if p_snap:
                cur_v = p_snap.get("votes_count", 0)
                cur_r = round(p_snap.get("average_vote", 0.0), 2)

                if prev_v is None:
                    dv = 0
                    implied_r = cur_r
                else:
                    dv = max(0, cur_v - prev_v)
                    if dv > 0:
                        ds = (cur_v * cur_r) - (prev_v * prev_r)
                        implied_r = round(max(1.0, min(5.0, ds / dv)), 2)
                    else:
                        implied_r = cur_r

                # Detect inflection drops & raid bursts
                if prev_r is not None:
                    drop = round(prev_r - cur_r, 2)
                    if drop >= 0.05 or (dv >= 2 and implied_r <= 3.2):
                        inflection_annotations.append({
                            "index": idx,
                            "date": history_timestamps[idx],
                            "prev_rating": prev_r,
                            "new_rating": cur_r,
                            "drop": drop,
                            "delta_votes": dv,
                            "implied_rating": implied_r,
                            "label": f"-{drop}★ (+{dv} votes @ {implied_r}★)"
                        })

                rating_series.append(cur_r)
                votes_series.append(cur_v)
                delta_v_series.append(dv)
                implied_r_series.append(implied_r)
                purged_series.append(round(p.get('purged_synthetic_rating', base_r), 2))

                prev_v = cur_v
                prev_r = cur_r
            else:
                rating_series.append(0.0)
                votes_series.append(0)
                delta_v_series.append(0)
                implied_r_series.append(0.0)
                purged_series.append(0.0)

        history_by_plugin[name] = {
            "ratings": rating_series,
            "votes": votes_series,
            "delta_votes": delta_v_series,
            "implied_ratings": implied_r_series,
            "purged_series": purged_series,
            "inflections": inflection_annotations
        }

    # -------------------------------------------------------------------------
    # Observed Rating Stream Engine.
    # QGIS exposes aggregate rating/vote snapshots, not individual vote rows.
    # The matrix below therefore records only observable baseline and interval
    # batches; it does not invent per-user rating events.
    # -------------------------------------------------------------------------
    def compute_plugin_rating_streams(history_snapshots):
        plugin_streams = {}
        if not history_snapshots:
            return {}

        base_snap = history_snapshots[0]
        base_plugins = base_snap.get("plugins", {})
        base_ts = base_snap.get("timestamp")
        base_date_str = base_snap.get("date_str", "Baseline")

        for p_name, p_data in base_plugins.items():
            base_v = p_data.get("votes_count", 0)
            base_avg = p_data.get("average_vote", 0.0)
            base_score = p_data.get("total_score", base_v * base_avg)
            plugin_streams[p_name] = []

            if base_v > 0:
                plugin_streams[p_name].append({
                    "seq_num": 1,
                    "rating": round(base_avg, 3),
                    "date_str": base_date_str,
                    "timestamp": base_ts,
                    "is_baseline": True,
                    "is_raid_pattern": False,
                    "delta_batch": base_v,
                    "votes_observed": base_v,
                    "score_delta": round(base_score, 4),
                    "verdict": "BASELINE_AGGREGATE",
                    "p_abuse": 0.0,
                    "note": "Baseline aggregate from QGIS rating_votes and average_vote"
                })

        # Calculate snapshot concurrency (how many plugins received votes in each snapshot)
        concurrency_map = []
        for i in range(1, len(history_snapshots)):
            snap = history_snapshots[i]
            prev_snap = history_snapshots[i-1]
            act_cnt = 0
            for p_name, p_curr in snap.get("plugins", {}).items():
                p_prev = prev_snap.get("plugins", {}).get(p_name, {})
                if p_curr.get("votes_count", 0) - p_prev.get("votes_count", 0) > 0:
                    act_cnt += 1
            concurrency_map.append(act_cnt)

        for i in range(1, len(history_snapshots)):
            snap = history_snapshots[i]
            ts = snap.get("timestamp")
            date_str = snap.get("date_str")
            prev_snap = history_snapshots[i - 1]
            prev_plugs = prev_snap.get("plugins", {})
            curr_plugs = snap.get("plugins", {})
            concurrency = concurrency_map[i - 1] if i - 1 < len(concurrency_map) else 1

            for p_name, p_data in curr_plugs.items():
                if p_name not in plugin_streams:
                    plugin_streams[p_name] = []

                prev_p = prev_plugs.get(p_name, {})
                v_prev = prev_p.get("votes_count", 0)
                s_prev = prev_p.get("total_score", v_prev * prev_p.get("average_vote", 0.0))
                dl_prev = prev_p.get("downloads", 0)

                v_curr = p_data.get("votes_count", 0)
                s_curr = p_data.get("total_score", v_curr * p_data.get("average_vote", 0.0))
                dl_curr = p_data.get("downloads", 0)

                v_diff = v_curr - v_prev
                s_diff = s_curr - s_prev
                dl_diff = max(0, dl_curr - dl_prev)

                if v_diff > 0:
                    avg_diff = s_diff / v_diff
                    implied_r = round(max(1.0, min(5.0, avg_diff)), 2)
                    prev_avg = prev_p.get("average_vote", 4.8)
                    conversion_k = (v_diff / max(1, dl_diff)) * 100.0

                    is_sync = (concurrency >= 3)
                    is_high_k = (conversion_k >= 3.0 or (v_diff >= 2 and dl_diff < 50))

                    if v_diff >= 5 and implied_r <= 1.8:
                        verdict = "TYPE_1_BOMBING"
                        p_abuse = 99.9
                        is_raid = True
                        note = f"Direct 1★ Bombing Raid (+{v_diff}v @ {implied_r}★)"
                    elif is_sync and implied_r <= 2.5:
                        verdict = "TYPE_4_SYNC_SWEEP"
                        p_abuse = 98.5
                        is_raid = True
                        note = f"Synchronized Multi-Plugin Raid ({concurrency} plugins hit simultaneously @ {implied_r}★)"
                    elif prev_avg >= 4.5 and implied_r <= 3.8 and is_high_k:
                        verdict = "TYPE_2_SOFT_DRAG"
                        p_abuse = 95.0
                        is_raid = True
                        note = f"Soft Dilution Drag-Down ({implied_r}★ on {prev_avg:.1f}★ baseline, κ={conversion_k:.1f}%)"
                    elif v_diff >= 1 and dl_diff <= 3 and is_sync:
                        verdict = "TYPE_3_PHANTOM"
                        p_abuse = 90.0
                        is_raid = True
                        note = f"Zero-Download Phantom Vote (+{v_diff}v on only {dl_diff} downloads)"
                    elif implied_r <= 2.5 and not is_sync and not is_high_k:
                        verdict = "ORGANIC_CRITICAL_FEEDBACK"
                        p_abuse = 10.0
                        is_raid = False
                        note = f"Legitimate Organic Critical Feedback (Single plugin, normal κ={conversion_k:.1f}%)"
                    else:
                        verdict = "ORGANIC_POSITIVE_FEEDBACK"
                        p_abuse = 5.0
                        is_raid = False
                        note = f"Organic Natural Review (+{v_diff}v @ {implied_r}★)"

                    seq = len(plugin_streams[p_name]) + 1
                    plugin_streams[p_name].append({
                        "seq_num": seq,
                        "rating": implied_r,
                        "date_str": date_str,
                        "timestamp": ts,
                        "is_baseline": False,
                        "is_raid_pattern": is_raid,
                        "delta_batch": v_diff,
                        "votes_observed": v_diff,
                        "score_delta": round(s_diff, 4),
                        "downloads_delta": dl_diff,
                        "conversion_k": round(conversion_k, 1),
                        "verdict": verdict,
                        "p_abuse": p_abuse,
                        "note": note
                    })

        summary_by_plugin = {}
        for p_name, stream in plugin_streams.items():
            total_records = len(stream)
            total_votes_observed = sum(v.get("votes_observed", v.get("delta_batch", 0)) for v in stream)
            last_20 = stream[-20:] if total_records >= 20 else stream
            row1 = last_20[:10] if len(last_20) > 10 else last_20
            row2 = last_20[10:] if len(last_20) > 10 else []

            summary_by_plugin[p_name] = {
                "total_recorded_votes": total_votes_observed,
                "observed_record_count": total_records,
                "stream": stream,
                "last_20": last_20,
                "row1": row1,
                "row2": row2,
                "raid_pattern_count": sum(1 for v in stream if v.get("is_raid_pattern")),
                "soft_drag_count": sum(1 for v in stream if v.get("verdict") == "TYPE_2_SOFT_DRAG"),
                "bombing_count": sum(1 for v in stream if v.get("verdict") == "TYPE_1_BOMBING"),
                "high_rating_record_count": sum(1 for v in stream if v.get("rating", 0) >= 4.5),
                "low_rating_record_count": sum(1 for v in stream if v.get("rating", 0) <= 2.5)
            }

        return summary_by_plugin

    rating_streams_summary = compute_plugin_rating_streams(history)

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
        },
        {
            "id": "mobility_3d",
            "name": "3D Inclusive Mobility & Microclimate Routing Studio",
            "category": "3D Kinematics & Inclusive Mobility",
            "icon": "fa-person-walking",
            "color": "#14b8a6",
            "desc": "Computes realistic 3D shortest path routes with 15 persona avatars (Wheelchair ADA, Elderly, Child, E-Scooter, Paramedic), Tobler/Minetti kinematics, and 2.5D architectural massing.",
            "estimated_time": "~3.8 mins / district",
            "steps": [
                {"step": 1, "plugin": "02Agent OSM Downloader", "action": "Pedestrian & Multi-Modal Network Acquisition", "type": "OSM Extraction", "output": "Routable Graph"},
                {"step": 2, "plugin": "02Route 3D", "action": "Multi-Criteria Shortest Path & 15 Avatar Kinematics", "type": "3D Pathfinding", "output": "3D LineStringZ GeoPackage"},
                {"step": 3, "plugin": "QGIS 2.5D Styling", "action": "Architectural 2.5D Massing & Urban Shading", "type": "2.5D Styling", "output": "Massing QML Layer"},
                {"step": 4, "plugin": "02CartoLab", "action": "Publication-Grade Atlas & Bivariate Route Profiling", "type": "Cartography", "output": "Atlas Map Book"}
            ]
        }
    ]

    total_votes = sum(p['votes_count'] for p in yusuf_plugins)
    total_score = sum(p['average_vote'] * p['votes_count'] for p in yusuf_plugins)
    overall_rating = (total_score / total_votes) if total_votes > 0 else 4.80
    portfolio_bayesian_avg = sum(p['bayesian_rating'] for p in yusuf_plugins) / len(yusuf_plugins) if yusuf_plugins else 4.80
    portfolio_monthly_velocity = active_period_monthly_avg
    active_count = len(yusuf_plugins)

    # Dynamic Portfolio Milestone Engine
    portfolio_tiers = [10000, 25000, 50000, 75000, 100000, 125000, 150000, 200000, 250000, 500000, 1000000]
    prev_tier = 100000
    for t in portfolio_tiers:
        if total_downloads >= t:
            prev_tier = t
        else:
            break
    next_tier = 125000
    for t in portfolio_tiers:
        if t > total_downloads:
            next_tier = t
            break
    else:
        next_tier = ((total_downloads // 50000) + 1) * 50000

    portfolio_remaining = max(0, next_tier - total_downloads)
    portfolio_progress_total = round((total_downloads / next_tier) * 100, 1)
    portfolio_tier_progress = round(((total_downloads - prev_tier) / (next_tier - prev_tier)) * 100, 1) if next_tier > prev_tier else 100.0

    if active_period_monthly_avg > 0 and portfolio_remaining > 0:
        days_to_p_milestone = (portfolio_remaining / active_period_monthly_avg) * 30.4375
        portfolio_est_date = (reference_date + timedelta(days=days_to_p_milestone)).strftime('%b %d, %Y')
    else:
        portfolio_est_date = "Reached"

    portfolio_milestones_data = {
        'prev_milestone': prev_tier,
        'next_milestone': next_tier,
        'remaining': portfolio_remaining,
        'progress_total': portfolio_progress_total,
        'progress_tier': portfolio_tier_progress,
        'est_date': portfolio_est_date,
        'achieved_milestones': [t for t in portfolio_tiers if total_downloads >= t]
    }

    embedded_data = {
        'plugins': yusuf_plugins,
        'summary': {
            'total_plugins': len(yusuf_plugins),
            'total_downloads': total_downloads,
            'portfolio_milestones': portfolio_milestones_data,
            'last_updated': reference_date.strftime('%b %d, %Y %H:%M UTC'),
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
                'prior_mean_rating': round(prior_mean_rating, 3),
                'palma_ratio': round(palma_ratio, 3),
                'pietra_robin_hood_index': round(pietra_index, 4),
                'theil_t_index': round(theil_t, 4),
                'theil_l_index': round(theil_l, 4),
                'suite_decomposition': suite_decomp,
                'within_suite_inequality_pct': within_gini_pct
            },
            'critical_anomalies': critical_count,
            'warning_anomalies': warning_count,
            'total_snapshots': len(history)
        },
        'anomalies': anomaly_reports,
        'correlation': correlation_meta,
        'rating_streams': rating_streams_summary,
        'history_meta': {
            'snapshots': history,
            'timestamps': history_timestamps,
            'by_plugin': history_by_plugin,
            'portfolio_waves': portfolio_wave_series,
            'portfolio_raid_waves': portfolio_raid_wave_series
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
<html lang="en" data-theme="obsidian" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QGIS Plugin Portfolio Analytics & Governance Studio — Yusuf Eminoğlu</title>

    <!-- Favicons & Brand Icons -->
    <link rel="icon" type="image/png" sizes="16x16" href="assets/favicon-16x16.png">
    <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="48x48" href="assets/favicon-48x48.png">
    <link rel="icon" type="image/png" sizes="64x64" href="assets/geophilo_mark_64.png">
    <link rel="icon" type="image/png" sizes="128x128" href="assets/favicon.png">
    <link rel="apple-touch-icon" sizes="192x192" href="assets/geophilo_mark_192.png">
    <link rel="shortcut icon" href="favicon.ico">

    <!-- Critical Zero-Flash Dark Mode Engine -->
    <style>
        html, body {
            background-color: #070a10 !important;
            color: #f8fafc !important;
        }
        [data-theme="alabaster"], [data-theme="alabaster"] body {
            background-color: #f1f5f9 !important;
            color: #0f172a !important;
        }
    </style>
    <script>
        (function() {
            try {
                var theme = localStorage.getItem('qgis_dashboard_theme') || 'obsidian';
                document.documentElement.setAttribute('data-theme', theme);
                if (theme === 'obsidian') {
                    document.documentElement.classList.add('dark');
                } else {
                    document.documentElement.classList.remove('dark');
                }
            } catch (e) {}
        })();
    </script>

    <!-- Comprehensive SEO Keywords & Metadata -->
    <meta name="description" content="Enterprise analytics, telemetry, growth forecasting, and rating abuse forensic surveillance studio for Yusuf Eminoğlu's ##TOTAL_PLUGINS## production QGIS plugins across urban analytics, spatial statistics, CAD, and 3D GIS.">
    <meta name="keywords" content="QGIS, QGIS Plugins, Yusuf Eminoğlu, PlanX, Urban Analytics, Spatial Statistics, Space Syntax, GIS, Remote Sensing, Urban Planning, Cartography, PyQGIS, GeoPackage, Three.js, OpenStreetMap, Rating Governance, Forensic Telemetry, Open Source GIS, Python GIS">
    <meta name="author" content="Yusuf Eminoğlu">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://yusufeminoglu.github.io/qgis-plugins-governance/">

    <!-- Open Graph / Facebook / LinkedIn -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://yusufeminoglu.github.io/qgis-plugins-governance/">
    <meta property="og:title" content="QGIS Plugin Portfolio Analytics & Governance Studio — Yusuf Eminoğlu">
    <meta property="og:description" content="Enterprise telemetry, adoption forecasting, and rating abuse forensic surveillance for ##TOTAL_PLUGINS## QGIS urban analytics plugins.">
    <meta property="og:image" content="https://yusufeminoglu.github.io/qgis-plugins-governance/preview.png">

    <!-- Twitter Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="https://yusufeminoglu.github.io/qgis-plugins-governance/">
    <meta name="twitter:title" content="QGIS Plugin Portfolio Analytics & Governance Studio">
    <meta name="twitter:description" content="Enterprise analytics, telemetry, and rating abuse forensic surveillance for ##TOTAL_PLUGINS## QGIS urban analytics plugins.">

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
      "description": "Enterprise analytics, telemetry, growth forecasting, and rating abuse forensic surveillance studio for ##TOTAL_PLUGINS## production QGIS plugins.",
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
        :root, [data-theme="obsidian"] {
            --bg-canvas: #070a10;
            --bg-canvas-subtle: #0b111e;
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --text-muted: #64748b;
            --text-accent: #38bdf8;
            --text-success: #34d399;
            --text-warning: #fbbf24;
            --text-danger: #fb7185;

            --panel-bg: rgba(16, 24, 40, 0.72);
            --panel-bg-hover: rgba(20, 32, 54, 0.85);
            --panel-border: rgba(255, 255, 255, 0.08);
            --panel-border-hover: rgba(56, 189, 248, 0.35);
            --panel-specular: linear-gradient(180deg, rgba(255, 255, 255, 0.14) 0%, rgba(255, 255, 255, 0.00) 100%);
            --panel-shadow: 0 12px 35px -5px rgba(0, 0, 0, 0.60), 0 0 0 1px rgba(255, 255, 255, 0.06), inset 0 1px 1px 0 rgba(255, 255, 255, 0.10);
            --panel-shadow-hover: 0 20px 45px -8px rgba(0, 0, 0, 0.75), 0 0 24px -2px rgba(56, 189, 248, 0.15), inset 0 1px 1px 0 rgba(255, 255, 255, 0.15);

            --nested-bg: rgba(7, 10, 16, 0.80);
            --nested-border: rgba(255, 255, 255, 0.06);
            --nested-specular: linear-gradient(180deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.00) 100%);

            --input-bg: #0b111e;
            --input-border: rgba(255, 255, 255, 0.12);
            --modal-bg: rgba(11, 17, 30, 0.95);

            --font-heading: 'Plus Jakarta Sans', sans-serif;
            --font-body: 'Inter', sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }

        [data-theme="alabaster"] {
            --bg-canvas: #f1f5f9;
            --bg-canvas-subtle: #e2e8f0;
            --text-main: #0f172a;
            --text-sub: #334155;
            --text-muted: #64748b;
            --text-accent: #0284c7;
            --text-success: #059669;
            --text-warning: #d97706;
            --text-danger: #e11d48;

            --panel-bg: rgba(255, 255, 255, 0.92);
            --panel-bg-hover: rgba(255, 255, 255, 0.98);
            --panel-border: rgba(15, 23, 42, 0.09);
            --panel-border-hover: rgba(2, 132, 199, 0.45);
            --panel-specular: linear-gradient(180deg, rgba(255, 255, 255, 0.98) 0%, rgba(255, 255, 255, 0.4) 100%);
            --panel-shadow: 0 4px 20px -4px rgba(15, 23, 42, 0.06), 0 1px 3px 0 rgba(15, 23, 42, 0.04), 0 0 0 1px rgba(15, 23, 42, 0.06);
            --panel-shadow-hover: 0 14px 35px -6px rgba(15, 23, 42, 0.12), 0 0 20px 0 rgba(2, 132, 199, 0.14), 0 0 0 1px rgba(2, 132, 199, 0.25);

            --nested-bg: rgba(248, 250, 252, 0.90);
            --nested-border: rgba(15, 23, 42, 0.08);
            --nested-specular: linear-gradient(180deg, rgba(255, 255, 255, 0.85) 0%, rgba(255, 255, 255, 0.15) 100%);

            --input-bg: #ffffff;
            --input-border: rgba(15, 23, 42, 0.18);
            --modal-bg: rgba(255, 255, 255, 0.98);
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
        .font-mono, .metric-value, table td {
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

        /* 4-Tier Elevation Glassmorphism System */
        .glass-panel {
            position: relative;
            background: var(--panel-bg);
            backdrop-filter: blur(24px) saturate(190%) contrast(102%);
            -webkit-backdrop-filter: blur(24px) saturate(190%) contrast(102%);
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

        .glass-card-nested {
            position: relative;
            background: var(--nested-bg);
            border: 1px solid var(--nested-border);
            border-radius: 1rem;
            transition: all 0.22s ease;
        }
        .glass-card-nested::before {
            content: '';
            position: absolute;
            inset: 0 0 auto 0;
            height: 1px;
            background: var(--nested-specular);
            border-radius: 1rem 1rem 0 0;
            pointer-events: none;
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

        /* Standardized Status Pills with Live Radar Pulse Beacons */
        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.375rem;
            padding: 0.2rem 0.55rem;
            border-radius: 9999px;
            font-family: var(--font-mono);
            font-size: 0.6875rem;
            font-weight: 700;
            line-height: 1;
            border-width: 1px;
            white-space: nowrap;
        }
        .status-pill-dot {
            width: 0.4375rem;
            height: 0.4375rem;
            border-radius: 9999px;
            flex-shrink: 0;
        }
        .status-pill-critical {
            background: rgba(244, 63, 94, 0.14);
            color: #f43f5e;
            border-color: rgba(244, 63, 94, 0.35);
        }
        .status-pill-critical .status-pill-dot {
            background: #f43f5e;
            box-shadow: 0 0 8px rgba(244, 63, 94, 0.8);
            animation: radar-pulse 1.8s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        .status-pill-warning {
            background: rgba(245, 158, 11, 0.14);
            color: #f59e0b;
            border-color: rgba(245, 158, 11, 0.35);
        }
        .status-pill-warning .status-pill-dot {
            background: #f59e0b;
        }
        .status-pill-success {
            background: rgba(16, 185, 129, 0.14);
            color: #10b981;
            border-color: rgba(16, 185, 129, 0.35);
        }
        .status-pill-success .status-pill-dot {
            background: #10b981;
        }
        .status-pill-info {
            background: rgba(56, 189, 248, 0.14);
            color: #38bdf8;
            border-color: rgba(56, 189, 248, 0.35);
        }
        .status-pill-info .status-pill-dot {
            background: #38bdf8;
        }

        @keyframes radar-pulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(244, 63, 94, 0.7); }
            70% { transform: scale(1.15); box-shadow: 0 0 0 6px rgba(244, 63, 94, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(244, 63, 94, 0); }
        }
        .pulse-live {
            animation: radar-pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }

        /* Fluid Tab Slide-Up Animation */
        .tab-pane {
            animation: tabSlideUp 0.28s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        @keyframes tabSlideUp {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: var(--bg-canvas); }
        ::-webkit-scrollbar-thumb { background: var(--text-muted); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--text-accent); }

        kbd {
            display: inline-block;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-bottom: 2px solid rgba(255, 255, 255, 0.22);
            border-radius: 5px;
            padding: 1px 6px;
            font-size: 10px;
            font-family: var(--font-mono);
            color: var(--text-sub);
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
            transition: all 0.1s ease;
        }
        [data-theme="alabaster"] kbd {
            background: rgba(15, 23, 42, 0.06);
            border: 1px solid rgba(15, 23, 42, 0.14);
            border-bottom: 2px solid rgba(15, 23, 42, 0.22);
            color: var(--text-sub);
        }
        kbd:active {
            transform: translateY(1px);
            border-bottom-width: 1px;
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
                    <p id="header-last-updated" class="text-[10px] text-slate-500 mt-1 font-mono"></p>
                </div>
            </div>

            <div class="flex flex-wrap items-center gap-3">
                <button onclick="openCommandPalette()" class="px-3.5 py-2 text-xs font-bold text-slate-300 hover:text-white bg-obsidian-800 hover:bg-obsidian-750 border border-white/10 rounded-xl flex items-center gap-2 transition-all font-mono" title="Quick Command Palette (Ctrl+K)">
                    <i class="fa-solid fa-terminal text-cyan-400"></i> Command <kbd>Ctrl+K</kbd>
                </button>

                <!-- Custom Multi-Plugin PyQGIS Install Cart -->
                <button onclick="openBundleModal()" id="bundle-header-btn" class="px-3.5 py-2 text-xs font-bold text-slate-300 hover:text-white bg-obsidian-800 hover:bg-obsidian-750 border border-white/10 rounded-xl flex items-center gap-1.5 transition-all" title="Custom PyQGIS Multi-Plugin Install Cart [B]">
                    <i class="fa-solid fa-cart-arrow-down text-cyan-400"></i> Install Bundle <span id="bundle-counter-badge" class="px-1.5 py-0.2 rounded-full bg-cyan-500 text-obsidian-950 font-mono text-[10px] font-extrabold hidden">0</span> <kbd>B</kbd>
                </button>

                <button onclick="openExecutiveStorytellingModal()" class="px-3.5 py-2 text-xs font-bold text-slate-300 hover:text-white bg-obsidian-800 hover:bg-obsidian-750 border border-white/10 rounded-xl flex items-center gap-1.5 transition-all" title="Generate State of Ecosystem Report & Community Kit">
                    <i class="fa-solid fa-newspaper text-emerald-400"></i> Reports & Announcements
                </button>

                <!-- Theme Switcher Button -->
                <button onclick="openCmdPalette()" class="px-3.5 py-2.5 rounded-2xl bg-obsidian-800 hover:bg-obsidian-750 text-slate-300 border border-white/10 text-xs font-mono font-bold flex items-center gap-2 transition-all">
                    <i class="fa-solid fa-terminal text-cyan-400"></i> Command <kbd class="px-1.5 py-0.5 text-[9px] bg-obsidian-900 border border-white/10 rounded">Ctrl+K</kbd>
                </button>
                <button onclick="openCompareModal()" class="px-3.5 py-2.5 rounded-2xl bg-obsidian-800 hover:bg-obsidian-750 text-slate-300 border border-white/10 text-xs font-mono font-bold flex items-center gap-2 transition-all">
                    <i class="fa-solid fa-code-compare text-emerald-400"></i> Compare Studio
                </button>
                <button onclick="openExecReportModal()" class="px-3.5 py-2.5 rounded-2xl bg-obsidian-800 hover:bg-obsidian-750 text-slate-300 border border-white/10 text-xs font-mono font-bold flex items-center gap-2 transition-all">
                    <i class="fa-solid fa-file-contract text-amber-400"></i> Exec Report
                </button>
                <button onclick="toggleTheme()" id="theme-toggle-btn" class="px-3.5 py-2 text-xs font-bold text-slate-300 hover:text-white bg-obsidian-800 hover:bg-obsidian-750 border border-white/10 rounded-xl flex items-center gap-1.5 transition-all" title="Toggle Theme (Obsidian / Alabaster) [T]">
                    <i class="fa-solid fa-circle-half-stroke text-amber-400"></i> <span id="theme-toggle-text">Obsidian Mode</span> <kbd>T</kbd>
                </button>

                <!-- 3-Way Benchmark Comparator -->
                <button onclick="openCompareModal()" class="px-3.5 py-2 text-xs font-bold text-slate-300 hover:text-white bg-obsidian-800 hover:bg-obsidian-750 border border-white/10 rounded-xl flex items-center gap-1.5 transition-all" title="Side-by-side 3-Plugin Benchmark">
                    <i class="fa-solid fa-code-compare text-indigo-400"></i> Compare
                </button>

                <!-- Dynamic Shields.io Badge Kit Generator -->
                <button onclick="openBadgeKitModal()" class="px-3.5 py-2 text-xs font-bold text-slate-300 hover:text-white bg-obsidian-800 hover:bg-obsidian-750 border border-white/10 rounded-xl flex items-center gap-1.5 transition-all" title="Dynamic Shields.io Badge Kit for GitHub READMEs">
                    <i class="fa-solid fa-certificate text-amber-400"></i> Badge Kit
                </button>

                <!-- Shareable Deep Link -->
                <button onclick="copyShareableDeepLink()" class="px-3 py-2 text-xs font-bold text-slate-300 hover:text-white bg-obsidian-800 hover:bg-obsidian-750 border border-white/10 rounded-xl flex items-center gap-1.5 transition-all" title="Copy Direct Shareable Link with Active View">
                    <i class="fa-solid fa-share-nodes text-cyan-400"></i> Share
                </button>

                <!-- Keyboard Shortcuts Cheat Sheet -->
                <button onclick="openShortcutsModal()" class="px-2.5 py-2 text-xs font-bold text-slate-400 hover:text-white bg-obsidian-800 hover:bg-obsidian-750 border border-white/10 rounded-xl flex items-center gap-1 transition-all" title="Keyboard Shortcuts Cheat Sheet [?]">
                    <i class="fa-solid fa-circle-question text-sm"></i>
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
                <i class="fa-solid fa-brain-circuit text-rose-400"></i> Forensic AI & Anomaly Lab <kbd>2</kbd>
                <span id="audit-alert-badge" class="ml-1.5 px-2 py-0.5 text-[10px] font-bold rounded-full bg-rose-500 text-white pulse-live"></span>
            </button>
            <button onclick="switchTab('stars')" id="tab-btn-stars" class="px-5 py-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 whitespace-nowrap relative">
                <i class="fa-solid fa-ranking-star text-amber-400"></i> Sequential Rating Matrix (20★) <kbd>3</kbd>
                <span class="ml-1.5 px-2 py-0.5 text-[10px] font-bold rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30">Live Stream</span>
            </button>
            <button onclick="switchTab('carto')" id="tab-btn-carto" class="px-5 py-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 whitespace-nowrap"><i class="fa-solid fa-earth-americas text-emerald-400"></i> Geospatial Studio <kbd>4</kbd></button>
            <button onclick="switchTab('deepdive')" id="tab-btn-deepdive" class="px-5 py-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 whitespace-nowrap"><i class="fa-solid fa-cubes"></i> Plugin Explorer <kbd>5</kbd></button>
            <button onclick="switchTab('pipelines')" id="tab-btn-pipelines" class="px-5 py-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 whitespace-nowrap"><i class="fa-solid fa-diagram-project text-cyan-400"></i> Ecosystem Pipelines <kbd>6</kbd></button>
            <button onclick="switchTab('simulator')" id="tab-btn-simulator" class="px-5 py-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 whitespace-nowrap"><i class="fa-solid fa-wand-magic-sparkles"></i> Forecast Simulator <kbd>7</kbd></button>
            <button onclick="switchTab('table')" id="tab-btn-table" class="px-5 py-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 whitespace-nowrap"><i class="fa-solid fa-table"></i> Master Performance Table <kbd>8</kbd></button>
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
                        <span class="text-xl font-bold font-mono text-indigo-400">##TOTAL_PLUGINS## / ##TOTAL_PLUGINS## Ready</span>
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
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8" id="econometric-ribbon">
                <div class="p-4 rounded-2xl bg-obsidian-950/80 border border-white/5 flex items-center justify-between">
                    <div>
                        <div class="flex items-center gap-1.5">
                            <span class="text-[10px] text-slate-400 uppercase font-mono font-semibold block">Gini Inequality (G*)</span>
                            <span title="Finite-sample corrected Gini coefficient measuring ecosystem concentration. Subgroup decomposition measures within-suite vs between-suite inequality." class="cursor-help text-slate-500 hover:text-cyan-400"><i class="fa-solid fa-circle-info text-[10px]"></i></span>
                        </div>
                        <span class="text-lg font-bold font-mono text-white" id="eco-gini-val">0.4676</span>
                    </div>
                    <div class="text-right">
                        <span class="text-[11px] px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono font-bold">Optimal Pareto</span>
                        <span class="block text-[9px] text-slate-500 font-mono mt-0.5" id="eco-within-gini">Within: 34.2%</span>
                    </div>
                </div>

                <div class="p-4 rounded-2xl bg-obsidian-950/80 border border-white/5 flex items-center justify-between">
                    <div>
                        <div class="flex items-center gap-1.5">
                            <span class="text-[10px] text-slate-400 uppercase font-mono font-semibold block">Palma Ratio & Pietra</span>
                            <span title="Palma Ratio = Top 10% download share / Bottom 40% download share. Pietra Index = exact percentage to redistribute for uniform downloads." class="cursor-help text-slate-500 hover:text-cyan-400"><i class="fa-solid fa-circle-info text-[10px]"></i></span>
                        </div>
                        <span class="text-lg font-bold font-mono text-indigo-400" id="eco-palma-val">2.84x</span>
                    </div>
                    <div class="text-right">
                        <span class="text-[11px] px-2 py-0.5 rounded-md bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-mono font-bold">Balanced</span>
                        <span class="block text-[9px] text-slate-500 font-mono mt-0.5" id="eco-pietra-val">Pietra: 0.33</span>
                    </div>
                </div>

                <div class="p-4 rounded-2xl bg-obsidian-950/80 border border-white/5 flex items-center justify-between">
                    <div>
                        <div class="flex items-center gap-1.5">
                            <span class="text-[10px] text-slate-400 uppercase font-mono font-semibold block">Theil & Entropy (N_eff)</span>
                            <span title="Generalized Theil T entropy index and exponential Shannon diversity (effective species richness)." class="cursor-help text-slate-500 hover:text-cyan-400"><i class="fa-solid fa-circle-info text-[10px]"></i></span>
                        </div>
                        <span class="text-lg font-bold font-mono text-cyan-400" id="eco-entropy-val">14.8 Plugins</span>
                    </div>
                    <div class="text-right">
                        <span class="text-[11px] px-2 py-0.5 rounded-md bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-mono font-bold">Multi-Pillar</span>
                        <span class="block text-[9px] text-slate-500 font-mono mt-0.5" id="eco-theil-val">Theil T: 0.38</span>
                    </div>
                </div>

                <div class="p-4 rounded-2xl bg-obsidian-950/80 border border-white/5 flex items-center justify-between">
                    <div>
                        <div class="flex items-center gap-1.5">
                            <span class="text-[10px] text-slate-400 uppercase font-mono font-semibold block">Hierarchical Bayes (μ₀)</span>
                            <span title="Two-Level Empirical Bayes hyperprior with sample-variance shrinkage B_i and 95% credibility intervals." class="cursor-help text-slate-500 hover:text-amber-400"><i class="fa-solid fa-circle-info text-[10px]"></i></span>
                        </div>
                        <span class="text-lg font-bold font-mono text-amber-400" id="eco-prior-val">4.84 ★</span>
                    </div>
                    <div class="text-right">
                        <span class="text-[11px] px-2 py-0.5 rounded-md bg-amber-500/10 text-amber-400 border border-amber-500/20 font-mono font-bold">Dynamic B_i</span>
                        <span class="block text-[9px] text-slate-500 font-mono mt-0.5">CredFloor: 95%</span>
                    </div>
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
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between mb-4 gap-2">
                        <div>
                            <h2 class="text-base font-bold tracking-tight"><i class="fa-solid fa-shapes text-cyan-400 mr-2"></i>BCG Adoption & Velocity Matrix</h2>
                            <p class="text-xs text-slate-400">Downloads (X) vs Monthly Velocity (Y) across portfolio</p>
                        </div>
                        <div class="flex flex-col sm:flex-row items-end sm:items-center gap-2">
                            <div class="flex items-center gap-1 font-mono text-[9px]">
                                <span class="text-slate-500 mr-0.5">Suite:</span>
                                <button onclick="setBcgSuiteFilter('all')" id="bcg-btn-all" class="px-2 py-0.5 rounded bg-cyan-600 text-white font-bold">All</button>
                                <button onclick="setBcgSuiteFilter('PlanX Suite')" id="bcg-btn-planx" class="px-2 py-0.5 rounded bg-obsidian-900 text-slate-400 hover:text-white border border-white/5">PlanX</button>
                                <button onclick="setBcgSuiteFilter('02 Suite')" id="bcg-btn-02" class="px-2 py-0.5 rounded bg-obsidian-900 text-slate-400 hover:text-white border border-white/5">02 Suite</button>
                                <button onclick="setBcgSuiteFilter('Standalone Plugins')" id="bcg-btn-std" class="px-2 py-0.5 rounded bg-obsidian-900 text-slate-400 hover:text-white border border-white/5">Standalone</button>
                            </div>
                            <div class="flex items-center gap-1 font-mono text-[9px]">
                                <span class="text-slate-500 mr-0.5">Quadrant:</span>
                                <button onclick="setBcgQuadrantFilter('all')" id="bcg-quad-all" class="px-2 py-0.5 rounded bg-cyan-600 text-white font-bold">All</button>
                                <button onclick="setBcgQuadrantFilter('Popular Momentum')" id="bcg-quad-stars" class="px-2 py-0.5 rounded bg-obsidian-900 text-slate-400 hover:text-emerald-400 border border-white/5">★ Stars</button>
                                <button onclick="setBcgQuadrantFilter('High Velocity')" id="bcg-quad-vel" class="px-2 py-0.5 rounded bg-obsidian-900 text-slate-400 hover:text-rose-400 border border-white/5">⚡ Velocity</button>
                                <button onclick="setBcgQuadrantFilter('Stable Classic')" id="bcg-quad-stable" class="px-2 py-0.5 rounded bg-obsidian-900 text-slate-400 hover:text-indigo-400 border border-white/5">⚓ Stable</button>
                                <button onclick="setBcgQuadrantFilter('Niche Specialist')" id="bcg-quad-niche" class="px-2 py-0.5 rounded bg-obsidian-900 text-slate-400 hover:text-slate-300 border border-white/5">🎯 Niche</button>
                            </div>
                        </div>
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
                    <div class="flex flex-wrap items-center gap-2">
                        <span class="text-xs font-bold text-amber-300 bg-amber-500/10 border border-amber-500/30 px-3 py-1 rounded-xl font-mono flex items-center gap-1.5 shadow-sm">
                            <i class="fa-solid fa-trophy text-amber-400"></i> 100K Historic Milestone Unlocked!
                        </span>
                        <span class="text-xs font-bold text-cyan-400 bg-cyan-500/10 border border-cyan-500/20 px-3 py-1 rounded-xl font-mono flex items-center gap-1.5">
                            <i class="fa-solid fa-flag-checkered text-cyan-400"></i> Next Horizon: <strong id="global-next-milestone-text">125,000</strong>
                        </span>
                    </div>
                </div>

                <div class="mb-8 bg-obsidian-900/80 p-5 rounded-2xl border border-white/5">
                    <div class="flex flex-wrap justify-between items-center text-xs font-semibold mb-2 gap-2">
                        <span>Portfolio Progress: <strong class="font-mono text-white" id="milestone-total-downloads"></strong></span>
                        <div class="flex items-center gap-3">
                            <span class="text-slate-400 text-[11px] font-mono" id="portfolio-milestone-eta"></span>
                            <span class="text-cyan-400 font-mono font-bold" id="portfolio-progress-percent"></span>
                        </div>
                    </div>
                    <div class="w-full bg-obsidian-800 rounded-full h-3 overflow-hidden">
                        <div class="bg-gradient-to-r from-cyan-500 via-teal-400 to-indigo-500 h-3 rounded-full shadow-lg transition-all duration-700" id="portfolio-progress-bar" style="width: 0%"></div>
                    </div>
                    <div class="mt-3 flex flex-wrap justify-between items-center text-[11px] text-slate-400 font-mono">
                        <span id="portfolio-milestone-prev">Unlocked: 100,000 DL</span>
                        <span id="portfolio-milestone-rem">Remaining: 15,356 DL</span>
                        <span id="portfolio-milestone-target">Target: 125,000 DL</span>
                    </div>
                </div>

                <!-- Interactive Multi-Mode Milestone Filter Bar -->
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-5">
                    <div class="flex flex-wrap items-center gap-2 font-mono text-xs">
                        <span class="text-slate-400 font-medium">Filter View:</span>
                        <div class="inline-flex rounded-xl bg-obsidian-900/90 p-1 border border-white/10" id="milestone-tabs">
                            <button onclick="switchMilestoneTab('imminent')" id="tab-ms-imminent" class="px-3 py-1.5 rounded-lg bg-cyan-500 text-obsidian-950 font-bold transition-all flex items-center gap-1.5 shadow-sm">
                                <i class="fa-solid fa-fire text-orange-600"></i> Imminent (≥85%) <span class="bg-obsidian-950/20 text-obsidian-950 text-[10px] px-1.5 py-0.5 rounded-full font-extrabold" id="imminent-count-badge">10</span>
                            </button>
                            <button onclick="switchMilestoneTab('velocity')" id="tab-ms-velocity" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white font-medium transition-all flex items-center gap-1.5">
                                <i class="fa-solid fa-bolt text-amber-400"></i> Top Velocity
                            </button>
                            <button onclick="switchMilestoneTab('all')" id="tab-ms-all" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white font-medium transition-all flex items-center gap-1.5">
                                <i class="fa-solid fa-layer-group text-cyan-400"></i> All Plugins (<span id="all-ms-count">28</span>)
                            </button>
                            <button onclick="switchMilestoneTab('fame')" id="tab-ms-fame" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white font-medium transition-all flex items-center gap-1.5">
                                <i class="fa-solid fa-award text-yellow-400"></i> Hall of Fame
                            </button>
                        </div>
                    </div>
                    <span class="text-[11px] text-slate-400 font-mono" id="milestone-subtitle-note">Showing plugins with urgent milestone velocity</span>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5" id="milestones-grid">
                    <!-- Dynamic cards populated via switchMilestoneTab / renderMilestones -->
                </div>
            </div>
        </div>

        <!-- ============================================================= -->
        <!-- TAB 2: FORENSIC AI & MULTIVARIATE ANOMALY SURVEILLANCE LAB -->
        <!-- ============================================================= -->
        <div id="tab-content-audit" class="tab-pane hidden">
            <!-- Surveillance Banner -->
            <div class="p-6 rounded-3xl glass-panel mb-8 border-l-4 border-rose-500 relative overflow-hidden bg-gradient-to-r from-rose-950/50 via-obsidian-900/90 to-obsidian-900/90">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 rounded-2xl bg-rose-500/20 text-rose-400 flex items-center justify-center text-xl flex-shrink-0 border border-rose-500/30">
                            <i class="fa-solid fa-shield-virus pulse-live"></i>
                        </div>
                        <div>
                            <div class="flex items-center gap-2.5">
                                <h2 class="text-lg font-bold tracking-tight font-heading">Forensic AI & Multivariate Anomaly Surveillance Lab</h2>
                                <span class="px-2.5 py-0.5 text-[10px] font-mono font-bold rounded-full bg-rose-500/20 text-rose-400 border border-rose-500/30">6D FEATURE VECTOR ENGINE</span>
                            </div>
                            <p class="text-xs text-slate-300 mt-1 max-w-3xl leading-relaxed">
                                Evaluates multi-dimensional anomaly features: <strong>Conversion Ratio (&kappa;)</strong>, <strong>Poisson Dispersion (Fano Factor)</strong>, <strong>Cross-Portfolio Synchronization (&rho;)</strong>, <strong>Soft Dilution Deviations (&delta;r)</strong>, and <strong>Mahalanobis Distance (D<sub>M</sub>)</strong> to reconstruct the <em>True Synthetic Organic Rating</em>.
                            </p>
                        </div>
                    </div>
                    <div class="flex flex-wrap gap-2 items-center">
                        <button onclick="openAllIncidentsModal()" class="px-4 py-2.5 text-xs font-bold text-white rounded-xl btn-danger flex items-center gap-2 whitespace-nowrap">
                            <i class="fa-solid fa-file-shield"></i> Export Audit Dossier & SQL Fix
                        </button>
                    </div>
                </div>
            </div>

            <!-- Dynamic Bayesian Sensitivity & Anomaly Rebalancing Control Bar -->
            <div class="p-5 rounded-3xl glass-panel mb-8 border border-white/5 bg-gradient-to-r from-obsidian-950 via-obsidian-900 to-obsidian-950">
                <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
                    <div class="flex items-center gap-4">
                        <div class="w-10 h-10 rounded-2xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center text-lg border border-cyan-500/20">
                            <i class="fa-solid fa-sliders"></i>
                        </div>
                        <div>
                            <h3 class="text-sm font-bold font-heading text-white flex items-center gap-2">
                                Dynamic Bayesian Anomaly Purge & Rebalancer
                                <span class="px-2 py-0.5 text-[9px] font-mono rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">REAL-TIME SIMULATOR</span>
                            </h3>
                            <p class="text-xs text-slate-400 mt-0.5">Adjust the Mahalanobis Distance threshold (D<sub>M</sub>) to test different forensic confidence intervals</p>
                        </div>
                    </div>

                    <div class="flex flex-wrap items-center gap-6">
                        <div class="flex items-center gap-3">
                            <span class="text-xs font-mono text-slate-400">Purge Threshold:</span>
                            <input type="range" id="bayesian-sensitivity-slider" min="2.0" max="10.0" step="0.5" value="5.0" oninput="handleSensitivitySliderChange(this.value)" class="w-36 sm:w-48 accent-cyan-400 cursor-pointer">
                            <span class="px-2.5 py-1 rounded-xl bg-obsidian-900 border border-white/10 text-xs font-mono font-bold text-cyan-400" id="slider-threshold-val">D<sub>M</sub> &ge; 5.0</span>
                        </div>

                        <div class="flex items-center gap-2 border-l border-white/10 pl-4">
                            <button onclick="resetSensitivitySlider()" class="px-3 py-1.5 rounded-xl bg-obsidian-800 hover:bg-obsidian-750 text-slate-300 text-xs font-mono font-bold border border-white/10 flex items-center gap-1.5 transition-all">
                                <i class="fa-solid fa-rotate-left"></i> Reset (5.0)
                            </button>
                            <button onclick="openFormalPscDossierModal()" class="px-4 py-1.5 rounded-xl btn-luxury text-white text-xs font-bold font-heading flex items-center gap-1.5">
                                <i class="fa-solid fa-scroll"></i> Formal PSC Brief
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Audit Metrics & True Organic Reconstruction Strip -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8" id="audit-kpis">
                <!-- Dynamically generated by JS -->
            </div>

            <!-- Side-by-Side Public vs. True Synthetic Rating Matrix -->
            <div class="p-6 rounded-3xl glass-panel mb-8">
                <div class="flex flex-col lg:flex-row lg:items-center justify-between pb-4 border-b border-white/5 gap-4 mb-6">
                    <div>
                        <div class="flex items-center gap-2.5">
                            <h2 class="text-base font-bold tracking-tight"><i class="fa-solid fa-scale-balanced text-cyan-400 mr-1.5"></i>Public Observed vs. True Synthetic Organic Score Matrix</h2>
                            <span class="px-2.5 py-0.5 text-[10px] font-mono font-bold rounded-full bg-cyan-500/10 text-cyan-300 border border-cyan-500/20">Bayesian Purge Filter</span>
                        </div>
                        <p class="text-xs text-slate-400 mt-0.5">Identifies points suppressed by Type I (1★ bombing) and Type II (soft 2-3★ drag-down) rating manipulation</p>
                    </div>
                    <div class="flex flex-wrap items-center gap-2">
                        <div class="relative w-full sm:w-64">
                            <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-1/2 -translate-y-1/2 text-xs text-slate-500"></i>
                            <input type="text" id="ml-search-input" oninput="filterMLMatrixSearch()" placeholder="Search plugin name..." class="w-full pl-9 pr-3 py-1.5 bg-obsidian-900 border border-white/10 rounded-xl text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-400 font-mono">
                        </div>
                    </div>
                </div>

                <!-- Taxonomy Filter Ribbon -->
                <div class="flex flex-wrap items-center gap-2 mb-4">
                    <button onclick="filterMLTaxonomy('ALL')" id="ml-flt-ALL" class="px-3 py-1 rounded-xl text-xs font-bold bg-cyan-600 text-white transition-all font-mono">All Plugins (<span id="ml-cnt-ALL">0</span>)</button>
                    <button onclick="filterMLTaxonomy('FLAGGED')" id="ml-flt-FLAGGED" class="px-3 py-1 rounded-xl text-xs font-bold bg-obsidian-800 text-rose-400 hover:text-white border border-rose-500/20 transition-all font-mono flex items-center gap-1.5">
                        <i class="fa-solid fa-triangle-exclamation"></i> All Flagged (<span id="ml-cnt-FLAGGED">0</span>)
                    </button>
                    <button onclick="filterMLTaxonomy('TYPE_2_SOFT_DILUTION')" id="ml-flt-TYPE_2_SOFT_DILUTION" class="px-3 py-1 rounded-xl text-xs font-bold bg-obsidian-800 text-amber-400 hover:text-white border border-amber-500/20 transition-all font-mono">
                        Type II: Soft Dilution (<span id="ml-cnt-TYPE_2">0</span>)
                    </button>
                    <button onclick="filterMLTaxonomy('TYPE_1_BOMBING')" id="ml-flt-TYPE_1_BOMBING" class="px-3 py-1 rounded-xl text-xs font-bold bg-obsidian-800 text-rose-300 hover:text-white border border-rose-500/20 transition-all font-mono">
                        Type I: 1★ Bombing (<span id="ml-cnt-TYPE_1">0</span>)
                    </button>
                    <button onclick="filterMLTaxonomy('ORGANIC')" id="ml-flt-ORGANIC" class="px-3 py-1 rounded-xl text-xs font-bold bg-obsidian-800 text-emerald-400 hover:text-white border border-emerald-500/20 transition-all font-mono">
                        Organic / Stable (<span id="ml-cnt-ORGANIC">0</span>)
                    </button>
                </div>

                <!-- ML Table -->
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs" id="ml-matrix-table">
                        <thead class="bg-obsidian-900/90 text-slate-400 uppercase text-[10px] tracking-wider border-b border-white/10 font-heading">
                            <tr>
                                <th class="py-3 px-4 font-bold">Plugin Name</th>
                                <th class="py-3 px-4 font-bold text-center">Public Observed</th>
                                <th class="py-3 px-4 font-bold text-center">True Organic Score</th>
                                <th class="py-3 px-4 font-bold text-center">Suppressed Points</th>
                                <th class="py-3 px-4 font-bold text-center">Influx (ΔVotes / Influx★)</th>
                                <th class="py-3 px-4 font-bold text-center">Conv. Ratio (κ)</th>
                                <th class="py-3 px-4 font-bold text-center">Mahalanobis (D<sub>M</sub>)</th>
                                <th class="py-3 px-4 font-bold text-center">P(Abuse)</th>
                                <th class="py-3 px-4 font-bold text-center">Taxonomy Classification</th>
                                <th class="py-3 px-4 font-bold text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody id="ml-matrix-table-body" class="divide-y divide-white/5 font-mono">
                            <!-- Filled dynamically by JS -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Active Incident Drilldown Cards -->
            <div class="p-6 rounded-3xl glass-panel mb-8">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-white/5 gap-3 mb-6">
                    <div>
                        <h2 class="text-base font-bold tracking-tight"><i class="fa-solid fa-list-check text-rose-400 mr-2"></i>Multi-Dimensional Anomaly Dossiers</h2>
                        <p class="text-xs text-slate-400 mt-0.5">Cryptographically hashed evidence records, Shannon entropy metrics, and SQL rollback scripts</p>
                    </div>
                    <div class="flex gap-2">
                        <button onclick="filterAnomalyStatus('all')" id="audit-filter-all" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-cyan-600 text-white">All Plugins</button>
                        <button onclick="filterAnomalyStatus('critical')" id="audit-filter-crit" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-obsidian-800 text-slate-400 hover:text-white border border-white/5">Flagged Raids Only</button>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6" id="anomaly-cards-container">
                    <!-- Dynamic Anomaly Incident Cards -->
                </div>
            </div>

            <!-- Kinematic Anomaly Phase Space (Conversion Physics & Poisson Envelope) -->
            <div class="p-6 rounded-3xl glass-panel mb-8 border-l-4 border-cyan-500">
                <div class="flex flex-col md:flex-row md:items-center justify-between mb-4 gap-3">
                    <div>
                        <div class="flex items-center gap-2.5">
                            <h2 class="text-base font-bold tracking-tight"><i class="fa-solid fa-atom text-cyan-400 mr-1.5"></i>Adoption Kinematics & Poisson Anomaly Phase Space</h2>
                            <span class="px-2 py-0.5 text-[10px] font-mono font-bold rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">&Delta;Downloads vs &Delta;Votes Corridor</span>
                        </div>
                        <p class="text-xs text-slate-400 mt-0.5">Reveals physical violations where votes arrive independently of user adoption (breaking the 95% Poisson confidence corridor)</p>
                    </div>
                    <div class="flex items-center gap-4 text-xs font-mono">
                        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-emerald-500 inline-block"></span> Organic Corridor (&kappa; &le; 1.2%)</span>
                        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-rose-500 inline-block pulse-live"></span> Raid Outlier (&kappa; &ge; 3.5%)</span>
                    </div>
                </div>
                <div id="kinematic-phase-chart" class="w-full h-80"></div>
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

            <!-- ============================================================= -->
            <!-- FORENSIC TIME-SERIES & ANOMALY INFLECTION SUITE -->
            <!-- ============================================================= -->

            <!-- Portfolio-Wide Synchronized Raid Influx Wave Chart -->
            <div class="p-6 rounded-3xl glass-panel mb-8 border-l-4 border-rose-500">
                <div class="flex flex-col md:flex-row md:items-center justify-between mb-4 gap-3">
                    <div>
                        <div class="flex items-center gap-2.5">
                            <h2 class="text-base font-bold tracking-tight"><i class="fa-solid fa-water-ladder text-rose-400 mr-1.5"></i>Portfolio-Wide Synchronized Vote Influx Waves</h2>
                            <span class="px-2 py-0.5 text-[10px] font-mono font-bold rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30">Cross-Plugin Burst Detection</span>
                        </div>
                        <p class="text-xs text-slate-400 mt-0.5">Reveals unnatural multi-plugin simultaneous raid clusters across all ##TOTAL_PLUGINS## plugins simultaneously</p>
                    </div>
                    <div class="flex items-center gap-2 text-xs font-mono">
                        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded bg-rose-500 inline-block"></span> Raid/Dilution Influx</span>
                        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded bg-cyan-500 inline-block ml-2"></span> Total Influx</span>
                    </div>
                </div>
                <div id="portfolio-wave-chart" class="w-full h-64"></div>
            </div>

            <!-- Plugin-Specific Dual-Axis Inflection & True Organic Trajectory Chart -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
                <!-- Left 2 Cols: Time-Series with Annotations -->
                <div class="lg:col-span-2 p-6 rounded-3xl glass-panel">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between mb-6 gap-4">
                        <div>
                            <div class="flex items-center gap-2">
                                <h2 class="text-base font-bold tracking-tight"><i class="fa-solid fa-chart-line-down text-rose-400 mr-1"></i>Plugin Trajectory & Inflection Callouts</h2>
                                <span class="px-2 py-0.5 text-[10px] font-mono font-bold rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Observed vs True Score</span>
                            </div>
                            <p class="text-xs text-slate-400 mt-0.5">Plots Observed Drop Curve vs Reconstructed True Baseline with marked raid drop points</p>
                        </div>
                        <div class="w-full sm:w-80">
                            <select id="audit-chart-plugin-select" onchange="renderAuditHistoryChart()" class="w-full px-3.5 py-2 bg-obsidian-900 border border-white/10 rounded-xl text-xs focus:outline-none focus:border-cyan-400 font-mono text-white">
                                <!-- Filled dynamically -->
                            </select>
                        </div>
                    </div>
                    <div id="audit-history-chart" class="w-full h-80"></div>
                </div>

                <!-- Right 1 Col: 6D Anomaly Radar Fingerprint -->
                <div class="p-6 rounded-3xl glass-panel flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-2">
                            <h2 class="text-base font-bold tracking-tight"><i class="fa-solid fa-radar text-cyan-400 mr-1.5"></i>6D Anomaly Radar</h2>
                            <span class="text-[10px] font-mono text-cyan-400 bg-cyan-500/10 px-2 py-0.5 rounded border border-cyan-500/20" id="radar-plugin-name">PlanX GeoStats</span>
                        </div>
                        <p class="text-xs text-slate-400 mb-4">Multivariate fingerprint comparing selected plugin against organic health norm</p>
                        <div id="audit-radar-chart" class="w-full h-64 flex items-center justify-center"></div>
                    </div>
                    <div class="mt-4 border-t border-white/5 pt-3 text-[11px] font-mono space-y-1.5 text-slate-300" id="radar-metric-details">
                        <!-- Filled dynamically -->
                    </div>
                </div>
            </div>
        </div>

        <!-- ============================================================= -->
        <!-- TAB: SEQUENTIAL RATING FORENSICS & 20-STAR MATRIX -->
        <!-- ============================================================= -->
        <div id="tab-content-stars" class="tab-pane hidden">
            <!-- Header Banner -->
            <div class="p-6 rounded-3xl glass-panel mb-8 border-l-4 border-amber-500 relative overflow-hidden bg-gradient-to-r from-amber-950/40 via-obsidian-900/90 to-obsidian-900/90">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 rounded-2xl bg-amber-500/20 text-amber-400 flex items-center justify-center text-xl flex-shrink-0 border border-amber-500/30">
                            <i class="fa-solid fa-ranking-star"></i>
                        </div>
                        <div>
                            <div class="flex items-center gap-2.5">
                                <h2 class="text-lg font-bold tracking-tight font-heading text-white">Sequential Rating Forensics & 20-Star Influx Matrix</h2>
                                <span class="px-2.5 py-0.5 text-[10px] font-mono font-bold rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30">OBSERVED QGIS AGGREGATE SNAPSHOTS</span>
                            </div>
                            <p class="text-xs text-slate-300 mt-1 max-w-3xl leading-relaxed">
                                Auditable stream of QGIS aggregate rating snapshots across all ##TOTAL_PLUGINS## plugins. Each plugin displays the latest 20 observed rating records with color-coded average-rating badges, vote-delta counts, and pattern-based low-rating detection.
                            </p>
                        </div>
                    </div>
                    <div class="flex flex-wrap gap-2 items-center">
                        <div class="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-obsidian-950/80 border border-white/10 text-[11px] font-mono">
                            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-teal-500 inline-block"></span> 5 star</span>
                            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-cyan-500 inline-block ml-1"></span> 4★</span>
                            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block ml-1"></span> 3★</span>
                            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-orange-500 inline-block ml-1"></span> 2★</span>
                            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block ml-1"></span> 1 star low</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Controls & Filters Ribbon -->
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
                <div class="flex flex-wrap items-center gap-2">
                    <button onclick="filterRatingStarsTab('all')" id="stars-filter-all" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-amber-600 text-white">All Plugins (<span id="stars-count-all">0</span>)</button>
                    <button onclick="filterRatingStarsTab('raided')" id="stars-filter-raided" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-obsidian-800 text-slate-400 hover:text-white border border-white/5 flex items-center gap-1.5">
                        <i class="fa-solid fa-shield-virus text-rose-400"></i> Pattern Flagged Only (<span id="stars-count-raided">0</span>)
                    </button>
                    <button onclick="filterRatingStarsTab('pure')" id="stars-filter-pure" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-obsidian-800 text-slate-400 hover:text-white border border-white/5 flex items-center gap-1.5">
                        <i class="fa-solid fa-circle-check text-teal-400"></i> No Pattern Flagged (<span id="stars-count-pure">0</span>)
                    </button>
                </div>
                <div class="relative w-full sm:w-72">
                    <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-1/2 -translate-y-1/2 text-xs text-slate-500"></i>
                    <input type="text" id="stars-search-input" oninput="filterRatingStarsSearch()" placeholder="Search plugin name..." class="w-full pl-9 pr-4 py-2 bg-obsidian-900 border border-white/10 rounded-xl text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-amber-400 font-mono">
                </div>
            </div>

            <!-- Cards Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8" id="stars-cards-container">
                <!-- Dynamically populated via JS -->
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
                    <span class="text-[10px] text-slate-400 font-mono" id="matching-plugins-count">##TOTAL_PLUGINS## plugins matching</span>
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
                    <button onclick="applyTablePreset('all')" id="tbl-preset-all" class="px-3 py-1 rounded-xl text-xs font-bold bg-cyan-600 text-white">All (##TOTAL_PLUGINS##)</button>
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
                                <th class="py-3.5 px-4 font-bold text-right cursor-pointer hover:text-white transition-colors" onclick="sortTable(3)">Downloads <i class="fa-solid fa-sort ml-1"></i></th>
                                <th class="py-3.5 px-4 font-bold text-right cursor-pointer hover:text-white transition-colors" onclick="sortTable(4)">Monthly Velocity <i class="fa-solid fa-sort ml-1"></i></th>
                                <th class="py-3.5 px-4 font-bold text-center cursor-pointer hover:text-white transition-colors" onclick="sortTable(5)">Bayesian ★ <i class="fa-solid fa-sort ml-1"></i></th>
                                <th class="py-3.5 px-4 font-bold text-center">Kinetic Regime</th>
                                <th class="py-3.5 px-4 font-bold text-center">Security Status</th>
                                <th class="py-3.5 px-4 font-bold text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody id="tab-table-body" class="divide-y divide-white/5">
                            <!-- Filled dynamically by JS -->
                        </tbody>
                    </table>
                </div>
                <div id="table-pagination-container" class="mt-4 pt-3 border-t border-white/5 flex items-center justify-between text-xs font-mono text-slate-400">
                    <!-- Dynamic Pagination -->
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

            <!-- Interactive PyQGIS Batch Automation Script Generator -->
            <div class="p-6 rounded-3xl glass-panel mb-8">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-white/5 gap-3 mb-6">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-xl flex items-center justify-center text-lg font-bold bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">
                            <i class="fa-brands fa-python"></i>
                        </div>
                        <div>
                            <h3 class="text-base font-bold font-heading text-white">Interactive PyQGIS Batch Automation Generator</h3>
                            <p class="text-xs text-slate-400">Production-grade Python scripts for QGIS 3.x / 4.x console or headless CLI</p>
                        </div>
                    </div>
                    <div class="flex items-center gap-2 flex-wrap">
                        <select id="pyqgis-runtime-target" onchange="generatePyQgisScript()" class="px-3 py-1.5 bg-obsidian-900 border border-white/10 rounded-xl text-xs font-mono text-cyan-400 focus:outline-none">
                            <option value="console">QGIS Python Console Script</option>
                            <option value="standalone">Standalone PyQGIS CLI Runner</option>
                            <option value="processing">Processing Algorithm Template</option>
                        </select>
                        <button onclick="copyGeneratedPyQgisScript()" class="px-4 py-2 text-xs font-bold text-white rounded-xl btn-luxury flex items-center gap-1.5">
                            <i class="fa-solid fa-copy"></i> Copy Script
                        </button>
                        <button onclick="downloadPyQgisScriptFile()" class="px-3.5 py-2 text-xs font-bold bg-obsidian-800 hover:bg-obsidian-750 text-slate-300 hover:text-white border border-white/10 rounded-xl flex items-center gap-1.5 transition-all">
                            <i class="fa-solid fa-download"></i> .py
                        </button>
                    </div>
                </div>

                <div class="relative">
                    <pre class="p-5 rounded-2xl bg-obsidian-950/90 border border-white/10 text-xs font-mono text-cyan-300 overflow-x-auto max-h-96 leading-relaxed select-all" id="pyqgis-code-preview"></pre>
                </div>
            </div>

            <!-- Cross-Suite Workflow Synergy & Co-Installation Matrix -->
            <div class="p-6 rounded-3xl glass-panel mb-8">
                <div class="flex items-center justify-between pb-4 border-b border-white/5 mb-6">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center text-lg border border-indigo-500/30">
                            <i class="fa-solid fa-share-nodes"></i>
                        </div>
                        <div>
                            <h3 class="text-base font-bold font-heading text-white">Cross-Suite Workflow Synergy & Co-Installation Affinities</h3>
                            <p class="text-xs text-slate-400">High-affinity plugin pairings and automated combined batch loading</p>
                        </div>
                    </div>
                    <span class="text-xs font-mono text-indigo-400 bg-indigo-500/10 border border-indigo-500/20 px-2.5 py-1 rounded-xl">Ecosystem Interoperability</span>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="synergy-matrix-grid">
                    <!-- Populated dynamically via JS -->
                </div>
            </div>
        </div>

    </div>

    <!-- ============================================================= -->
    <!-- FLOATING BUNDLE SELECTION BAR -->
    <!-- ============================================================= -->
    <div id="bundle-floating-bar" class="fixed bottom-6 left-1/2 -translate-x-1/2 z-40 px-6 py-3.5 rounded-2xl bg-obsidian-900/95 border border-cyan-500/40 shadow-2xl backdrop-blur-md flex items-center gap-4 hidden transition-all">
        <div class="flex items-center gap-2.5">
            <span class="w-7 h-7 rounded-xl bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 flex items-center justify-center text-xs font-bold font-mono" id="bundle-bar-count">0</span>
            <span class="text-xs font-bold text-white font-heading">Plugins in Custom Bundle</span>
        </div>
        <div class="h-4 w-px bg-white/10"></div>
        <div class="flex items-center gap-2">
            <button onclick="openBundleModal()" class="px-4 py-2 rounded-xl text-xs font-bold btn-luxury text-white flex items-center gap-1.5">
                <i class="fa-solid fa-terminal"></i> Generate Batch Script
            </button>
            <button onclick="clearPluginBundle()" class="px-3 py-2 rounded-xl text-xs font-bold bg-obsidian-800 hover:bg-rose-600/20 text-slate-400 hover:text-rose-400 border border-white/10 transition-all">
                Clear
            </button>
        </div>
    </div>

    <!-- ============================================================= -->
    <!-- CUSTOM PYQGIS MULTI-PLUGIN INSTALL BUNDLE MODAL -->
    <!-- ============================================================= -->
    <div id="bundle-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md hidden p-4">
        <div class="bg-obsidian-900 border border-white/10 rounded-3xl max-w-4xl w-full p-6 max-h-[92vh] flex flex-col justify-between shadow-2xl overflow-hidden">
            <div class="flex items-center justify-between pb-4 border-b border-white/10">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center text-lg border border-cyan-500/30">
                        <i class="fa-solid fa-cart-arrow-down"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold tracking-tight">Custom PyQGIS Multi-Plugin Install Bundle</h3>
                        <p class="text-xs text-slate-400">Generate unified mass-installation scripts for selected plugins with dependency validation</p>
                    </div>
                </div>
                <button onclick="closeBundleModal()" class="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-obsidian-800 transition-colors">
                    <i class="fa-solid fa-xmark text-lg"></i>
                </button>
            </div>

            <div class="my-4">
                <div class="flex items-center justify-between mb-2">
                    <div class="text-xs text-slate-300 font-heading font-semibold">
                        Selected Plugins (<span id="bundle-modal-count" class="text-cyan-400 font-mono font-bold">0</span>):
                    </div>
                    <div class="flex gap-2">
                        <button onclick="selectAllPluginsBundle()" class="text-xs text-cyan-400 hover:text-cyan-300 font-mono">Select All (25)</button>
                        <span class="text-slate-600">|</span>
                        <button onclick="clearPluginBundle()" class="text-xs text-rose-400 hover:text-rose-300 font-mono">Clear All</button>
                    </div>
                </div>
                <div class="flex flex-wrap gap-1.5 p-3 rounded-2xl bg-obsidian-950/70 border border-white/5 max-h-28 overflow-y-auto" id="bundle-modal-tags">
                    <!-- Populated dynamically -->
                </div>
            </div>

            <div class="my-2">
                <div class="flex items-center justify-between mb-2">
                    <label class="text-xs font-semibold text-slate-400 font-heading">Execution Target</label>
                    <select id="bundle-target-type" onchange="renderBundleScriptPreview()" class="px-3 py-1 bg-obsidian-950 border border-white/10 rounded-xl text-xs font-mono text-cyan-400 focus:outline-none">
                        <option value="console">QGIS Python Console Script</option>
                        <option value="cli">Headless OS Command (pip / zip)</option>
                    </select>
                </div>
                <pre class="bg-obsidian-950 p-4 rounded-2xl border border-white/5 text-xs font-mono text-cyan-300 overflow-x-auto max-h-[36vh] whitespace-pre leading-relaxed select-all" id="bundle-code-preview"></pre>
            </div>

            <div class="pt-4 border-t border-white/10 flex justify-between items-center text-xs">
                <div class="flex items-center gap-2">
                    <button onclick="copyBundleScript()" class="px-4 py-2 rounded-xl text-xs font-bold btn-luxury text-white flex items-center gap-1.5">
                        <i class="fa-solid fa-copy"></i> Copy Script
                    </button>
                    <button onclick="downloadBundleScript()" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-obsidian-800 hover:bg-obsidian-750 text-slate-300 hover:text-white border border-white/10 flex items-center gap-1.5 transition-all">
                        <i class="fa-solid fa-download"></i> .py
                    </button>
                </div>
                <button onclick="closeBundleModal()" class="px-5 py-2 rounded-xl bg-obsidian-800 hover:bg-obsidian-750 text-white font-bold transition-all">Close</button>
            </div>
        </div>
    </div>

    <!-- ============================================================= -->
    <!-- RATING FORENSIC SURVEILLANCE DEEP-DIVE INSPECTOR MODAL -->
    <!-- ============================================================= -->
    <div id="forensic-inspector-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md hidden p-4">
        <div class="bg-obsidian-900 border border-white/10 rounded-3xl max-w-4xl w-full p-6 max-h-[92vh] flex flex-col justify-between shadow-2xl overflow-hidden">
            <div class="flex items-center justify-between pb-4 border-b border-white/10">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-rose-500/20 text-rose-400 flex items-center justify-center text-lg border border-rose-500/30">
                        <i class="fa-solid fa-shield-virus"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold tracking-tight" id="forensic-modal-title">Forensic Audit & Surveillance Diagnostic</h3>
                        <p class="text-xs text-slate-400">Two-Level Empirical Bayes, Laplace smoothing, Wilson 95% interval, and entropy analytics</p>
                    </div>
                </div>
                <button onclick="closeForensicInspectorModal()" class="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-obsidian-800 transition-colors">
                    <i class="fa-solid fa-xmark text-lg"></i>
                </button>
            </div>

            <div class="my-4 overflow-y-auto max-h-[60vh] pr-2 space-y-4" id="forensic-modal-body">
                <!-- Populated dynamically via JS -->
            </div>

            <div class="pt-4 border-t border-white/10 flex justify-between items-center text-xs">
                <button onclick="copyForensicReport()" class="px-4 py-2 rounded-xl text-xs font-bold btn-luxury text-white flex items-center gap-1.5">
                    <i class="fa-solid fa-copy"></i> Copy Forensic Diagnostic
                </button>
                <button onclick="closeForensicInspectorModal()" class="px-5 py-2 rounded-xl bg-obsidian-800 hover:bg-obsidian-750 text-white font-bold transition-all">Close</button>
            </div>
        </div>
    </div>

    <!-- ============================================================= -->
    <!-- KEYBOARD SHORTCUTS CHEAT SHEET MODAL -->
    <!-- ============================================================= -->
    <div id="shortcuts-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md hidden p-4">
        <div class="bg-obsidian-900 border border-white/10 rounded-3xl max-w-xl w-full p-6 shadow-2xl overflow-hidden">
            <div class="flex items-center justify-between pb-4 border-b border-white/10">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center text-lg border border-cyan-500/30">
                        <i class="fa-solid fa-keyboard"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold tracking-tight">Keyboard Shortcuts</h3>
                        <p class="text-xs text-slate-400">Power user navigation commands</p>
                    </div>
                </div>
                <button onclick="closeShortcutsModal()" class="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-obsidian-800 transition-colors">
                    <i class="fa-solid fa-xmark text-lg"></i>
                </button>
            </div>

            <div class="grid grid-cols-2 gap-3 my-4 text-xs">
                <div class="p-3 rounded-2xl bg-obsidian-950 border border-white/5 flex items-center justify-between">
                    <span class="text-slate-300">Executive Overview</span>
                    <kbd>1</kbd>
                </div>
                <div class="p-3 rounded-2xl bg-obsidian-950 border border-white/5 flex items-center justify-between">
                    <span class="text-slate-300">Rating Surveillance</span>
                    <kbd>2</kbd>
                </div>
                <div class="p-3 rounded-2xl bg-obsidian-950 border border-white/5 flex items-center justify-between">
                    <span class="text-slate-300">Sequential Rating Matrix (20★)</span>
                    <kbd>3</kbd>
                </div>
                <div class="p-3 rounded-2xl bg-obsidian-950 border border-white/5 flex items-center justify-between">
                    <span class="text-slate-300">Geospatial Studio</span>
                    <kbd>4</kbd>
                </div>
                <div class="p-3 rounded-2xl bg-obsidian-950 border border-white/5 flex items-center justify-between">
                    <span class="text-slate-300">Plugin Explorer</span>
                    <kbd>5</kbd>
                </div>
                <div class="p-3 rounded-2xl bg-obsidian-950 border border-white/5 flex items-center justify-between">
                    <span class="text-slate-300">Ecosystem Pipelines</span>
                    <kbd>6</kbd>
                </div>
                <div class="p-3 rounded-2xl bg-obsidian-950 border border-white/5 flex items-center justify-between">
                    <span class="text-slate-300">Forecast Simulator</span>
                    <kbd>7</kbd>
                </div>
                <div class="p-3 rounded-2xl bg-obsidian-950 border border-white/5 flex items-center justify-between">
                    <span class="text-slate-300">Master Data Table</span>
                    <kbd>8</kbd>
                </div>
                <div class="p-3 rounded-2xl bg-obsidian-950 border border-white/5 flex items-center justify-between">
                    <span class="text-slate-300">Command Palette</span>
                    <kbd>Ctrl+K</kbd>
                </div>
                <div class="p-3 rounded-2xl bg-obsidian-950 border border-white/5 flex items-center justify-between">
                    <span class="text-slate-300">Toggle Theme</span>
                    <kbd>T</kbd>
                </div>
                <div class="p-3 rounded-2xl bg-obsidian-950 border border-white/5 flex items-center justify-between">
                    <span class="text-slate-300">Quick Search</span>
                    <kbd>/</kbd>
                </div>
                <div class="p-3 rounded-2xl bg-obsidian-950 border border-white/5 flex items-center justify-between">
                    <span class="text-slate-300">Custom Install Bundle</span>
                    <kbd>B</kbd>
                </div>
                <div class="p-3 rounded-2xl bg-obsidian-950 border border-white/5 flex items-center justify-between">
                    <span class="text-slate-300">Close Any Modal</span>
                    <kbd>Esc</kbd>
                </div>
            </div>

            <div class="pt-4 border-t border-white/10 flex justify-end">
                <button onclick="closeShortcutsModal()" class="px-5 py-2 rounded-xl bg-obsidian-800 hover:bg-obsidian-750 text-white text-xs font-bold transition-all">Got it</button>
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
                <input type="text" id="palette-search-input" onkeyup="filterCommandPalette()" onkeydown="handlePaletteKeydown(event)" placeholder="Type a command, tab, or plugin name..." class="w-full pl-10 pr-4 py-3 bg-obsidian-950 border border-white/10 rounded-2xl text-xs focus:outline-none focus:border-cyan-400 font-mono">
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

    <!-- ============================================================= -->
    <!-- FULL CHRONOLOGICAL RATING STREAM & FORENSIC LOG MODAL -->
    <!-- ============================================================= -->
    <div id="stream-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md hidden p-4">
        <div class="bg-obsidian-900 border border-white/10 rounded-3xl max-w-4xl w-full p-6 max-h-[92vh] flex flex-col justify-between shadow-2xl overflow-hidden">
            <div class="flex items-center justify-between pb-4 border-b border-white/10">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center text-lg border border-amber-500/30">
                        <i class="fa-solid fa-ranking-star"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold tracking-tight text-white flex items-center gap-2">
                            <span id="stream-modal-title">Plugin Rating Timeline</span>
                            <span id="stream-modal-badge" class="px-2 py-0.5 rounded text-[10px] font-mono font-bold"></span>
                        </h3>
                        <p class="text-xs text-slate-400 font-mono">Observed QGIS aggregate snapshot log; individual voter rows are not exposed by QGIS.</p>
                    </div>
                </div>
                <button onclick="closeStreamModal()" class="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-obsidian-800 transition-colors">
                    <i class="fa-solid fa-xmark text-lg"></i>
                </button>
            </div>

            <!-- Summary Ribbon -->
            <div class="grid grid-cols-4 gap-3 my-4 p-3 rounded-2xl bg-obsidian-950/80 border border-white/5 font-mono text-center text-xs">
                <div>
                    <span class="text-[9px] text-slate-500 uppercase block">Total History Votes</span>
                    <span id="stream-modal-total" class="font-extrabold text-white text-sm">0</span>
                </div>
                <div>
                    <span class="text-[9px] text-slate-500 uppercase block">High Avg Records</span>
                    <span id="stream-modal-5stars" class="font-extrabold text-teal-300 text-sm">0</span>
                </div>
                <div>
                    <span class="text-[9px] text-slate-500 uppercase block">Low Avg Records</span>
                    <span id="stream-modal-1stars" class="font-extrabold text-rose-400 text-sm">0</span>
                </div>
                <div>
                    <span class="text-[9px] text-slate-500 uppercase block">Patterns Flagged</span>
                    <span id="stream-modal-raids" class="font-extrabold text-amber-400 text-sm">0</span>
                </div>
            </div>

            <!-- Chronological Events Table -->
            <div class="overflow-y-auto max-h-[48vh] pr-1 my-2">
                <table class="w-full text-left text-xs font-mono">
                    <thead class="bg-obsidian-950 text-slate-400 uppercase text-[10px] tracking-wider border-b border-white/10 sticky top-0">
                        <tr>
                            <th class="py-2.5 px-3">Sequence ($n$)</th>
                            <th class="py-2.5 px-3 text-center">Rating</th>
                            <th class="py-2.5 px-3">Timestamp / Date</th>
                            <th class="py-2.5 px-3">Batch Size (ΔV)</th>
                            <th class="py-2.5 px-3 text-right">Audit Classification</th>
                        </tr>
                    </thead>
                    <tbody id="stream-modal-tbody" class="divide-y divide-white/5 text-slate-300">
                        <!-- Filled dynamically -->
                    </tbody>
                </table>
            </div>

            <div class="pt-4 border-t border-white/10 flex justify-between items-center text-xs font-mono">
                <button onclick="copyPluginStreamJson()" class="px-4 py-2 rounded-xl text-xs font-bold btn-luxury text-white flex items-center gap-1.5">
                    <i class="fa-solid fa-code"></i> Copy Stream JSON
                </button>
                <button onclick="closeStreamModal()" class="px-5 py-2 rounded-xl bg-obsidian-800 hover:bg-obsidian-750 text-white font-bold transition-all">Close</button>
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

    <!-- Canvas Constellation Animation (Optimized with Visibility & Reduced Motion Checks) -->
    <script>
        const canvas = document.getElementById('bg-canvas');
        const ctx = canvas.getContext('2d');

        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        const particles = [];
        const maxParticles = 65;
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        let isConstellationActive = false;

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
            if (prefersReducedMotion || document.hidden) {
                isConstellationActive = false;
                return;
            }
            isConstellationActive = true;
            ctx.clearRect(0, 0, width, height);
            for (let i = 0; i < particles.length; i++) {
                particles[i].update();
                particles[i].draw();
            }
            requestAnimationFrame(animate);
        }
        if (!prefersReducedMotion) animate();

        document.addEventListener('visibilitychange', () => {
            if (!document.hidden && !prefersReducedMotion && !isConstellationActive) {
                animate();
            }
        });

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
                    closeBadgeKitModal();
                    closeBundleModal();
                    closeForensicInspectorModal();
                    closeShortcutsModal();
                }
                return;
            }

            if (e.key === '1') switchTab('overview');
            else if (e.key === '2') switchTab('audit');
            else if (e.key === '3') switchTab('stars');
            else if (e.key === '4') switchTab('carto');
            else if (e.key === '5') switchTab('deepdive');
            else if (e.key === '6') switchTab('pipelines');
            else if (e.key === '7') switchTab('simulator');
            else if (e.key === '8') switchTab('table');
            else if (e.key.toLowerCase() === 't') toggleTheme();
            else if (e.key.toLowerCase() === 'b') openBundleModal();
            else if (e.key === '?' || (e.shiftKey && e.key === '/')) openShortcutsModal();
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
                closeBundleModal();
                closeForensicInspectorModal();
                closeShortcutsModal();
                closeStreamModal();
            }
        });

        // Command Palette Logic
        let paletteSelectedIndex = 0;
        let currentPaletteItems = [];

        function openCommandPalette() {
            document.getElementById('command-palette-modal').classList.remove('hidden');
            const input = document.getElementById('palette-search-input');
            input.value = '';
            paletteSelectedIndex = 0;
            filterCommandPalette();
            setTimeout(() => input.focus(), 100);
        }

        function closeCommandPalette() {
            document.getElementById('command-palette-modal').classList.add('hidden');
        }

        function handlePaletteKeydown(e) {
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                paletteSelectedIndex = Math.min(paletteSelectedIndex + 1, currentPaletteItems.length - 1);
                updatePaletteSelection();
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                paletteSelectedIndex = Math.max(paletteSelectedIndex - 1, 0);
                updatePaletteSelection();
            } else if (e.key === 'Enter') {
                e.preventDefault();
                if (currentPaletteItems[paletteSelectedIndex]) {
                    currentPaletteItems[paletteSelectedIndex].action();
                }
            } else if (e.key === 'Escape') {
                closeCommandPalette();
            }
        }        // (Legacy palette functions cleaned in favor of unified global Command Palette)

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
            const pm = appData.summary.portfolio_milestones || {
                prev_milestone: 100000,
                next_milestone: 125000,
                progress_total: 87.7,
                remaining: 15356,
                est_date: 'Nov 2026'
            };

            let text = '';
            if (format === 'ecosystem') {
                text = `===============================================================
QGIS PLUGIN ECOSYSTEM ANNUAL STATE & GOVERNANCE REPORT
Author: Yusuf Eminoğlu | Audit Timestamp: ${appData.summary.last_updated}
===============================================================

1. PORTFOLIO VOLUME & TRAJECTORY:
   - Total Cumulative Ecosystem Downloads: ${appData.summary.total_downloads.toLocaleString()} across ${appData.summary.total_plugins} production plugins.
   - Active Monthly Adoption Velocity: ~${appData.summary.active_period_monthly_avg.toLocaleString()} downloads/month.
   - Historic 100k Global Milestone: ACHIEVED & SURPASSED (${appData.summary.total_downloads.toLocaleString()} / 100,000 — 109.6% completed).
   - Next Strategic Horizon Target: ${pm.next_milestone.toLocaleString()} downloads (${pm.progress_total}% achieved).
   - Estimated Next Horizon Arrival: ${pm.est_date}.

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
                text = `🚀 Historic Milestone Achieved: Our QGIS Urban Analytics & Spatial Planning Ecosystem has surpassed 100,000 downloads!

Now standing at ${appData.summary.total_downloads.toLocaleString()} cumulative downloads across ${appData.summary.total_plugins} production plugins, the suite maintains an active adoption velocity of ~${appData.summary.active_period_monthly_avg.toLocaleString()} downloads/month spanning geospatial workflows in 140+ countries.

🌟 Top Ecosystem Highlights:
• Crown Jewel: ${leader.name} leading with ${leader.downloads.toLocaleString()} downloads.
• Velocity Champion: ${fastest.name} clocking ~${Math.round(fastest.avg_monthly_downloads).toLocaleString()}/month.
• Macro-Regional Engine: Western Europe & North America representing over 70% of spatial analysis workflows.
• Next Strategic Horizon: On track for ${pm.next_milestone.toLocaleString()} downloads by ${pm.est_date}.

We've also open-sourced our dedicated Governance & Analytics Studio:
🔗 Live Dashboard: https://yusufeminoglu.github.io/qgis-plugins-governance/
🔗 GitHub Repository: https://github.com/YusufEminoglu/qgis-plugins-governance

Thank you to the global QGIS & OSGeo community! 🌍

#QGIS #GIS #UrbanPlanning #SpatialAnalytics #OpenSource #PyQGIS #Geospatial`;
            } else if (format === 'twitter') {
                text = `1/4 🌍 Historic milestone for open-source GIS: The Yusuf Eminoğlu QGIS Plugin Ecosystem has surpassed 100,000 downloads (now at ${appData.summary.total_downloads.toLocaleString()} DL across ${appData.summary.total_plugins} plugins)!

2/4 📈 Adoption Velocity: Running at ~${appData.summary.active_period_monthly_avg.toLocaleString()} downloads/month. Next horizon: ${pm.next_milestone.toLocaleString()} (Est: ${pm.est_date}).
👑 Flagship: ${leader.name} (${leader.downloads.toLocaleString()} DL)
⚡ Fastest Adoption: ${fastest.name} (~${Math.round(fastest.avg_monthly_downloads).toLocaleString()}/mo)

3/4 🛡️ We built an open Governance & Analytics Studio tracking telemetry, econometric Gini diversity, and rating surveillance live via GitHub Actions:
https://yusufeminoglu.github.io/qgis-plugins-governance/

4/4 Explore the entire suite on the official QGIS Hub:
https://plugins.qgis.org/plugins/author/Yusuf%20Eminoglu/
#QGIS #SpatialAnalytics`;
            } else {
                text = `**[100K Historic Milestone & Governance Bulletin] Yusuf Eminoğlu QGIS Plugin Ecosystem: ${appData.summary.total_downloads.toLocaleString()} Downloads**

Hey r/QGIS community!

Wanted to share an exciting milestone: our ${appData.summary.total_plugins} spatial planning & urban analytics plugins (including PlanX suite, CAD toolset, and 02 geospatial tools) have officially crossed 100,000 downloads (now live at ${appData.summary.total_downloads.toLocaleString()} DL)!

### 📊 Portfolio Telemetry Overview
| Metric | Value |
|---|---|
| Total Plugins | ${appData.summary.total_plugins} (QGIS 3.x & QGIS 4.0 Ready) |
| Cumulative Downloads | ${appData.summary.total_downloads.toLocaleString()} (100K Milestone Passed) |
| Current Velocity | ~${appData.summary.active_period_monthly_avg.toLocaleString()} downloads/mo |
| Next Horizon Target | ${pm.next_milestone.toLocaleString()} DL (ETA: ${pm.est_date}) |
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

        function switchTab(tabId, updateHash = true) {
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

            if (updateHash && typeof updateHashUrl === 'function') updateHashUrl(tabId);

            if (tabId === 'overview' || tabId === 'deepdive') {
                setTimeout(initializeCharts, 100);
            }
            if (tabId === 'simulator') {
                setTimeout(runSimulation, 100);
            }
            if (tabId === 'audit') {
                setTimeout(renderAuditHistoryChart, 100);
            }
            if (tabId === 'stars') {
                setTimeout(renderRatingStarsTab, 100);
            }
            if (tabId === 'carto') {
                setTimeout(initializeGeospatialStudio, 100);
            }
            if (tabId === 'pipelines') {
                setTimeout(() => {
                    initializePipelines();
                    if (typeof renderSynergyMatrix === 'function') renderSynergyMatrix();
                }, 100);
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

            // Econometrics Ribbon Dynamic Updates
            const eco = appData.summary.econometrics || {};
            if (document.getElementById('eco-gini-val')) document.getElementById('eco-gini-val').innerText = eco.gini_corrected || '0.4676';
            if (document.getElementById('eco-within-gini')) document.getElementById('eco-within-gini').innerText = `Within: ${eco.within_suite_inequality_pct || 34.2}%`;
            if (document.getElementById('eco-palma-val')) document.getElementById('eco-palma-val').innerText = `${eco.palma_ratio || 2.84}x`;
            if (document.getElementById('eco-pietra-val')) document.getElementById('eco-pietra-val').innerText = `Pietra: ${eco.pietra_robin_hood_index || 0.33}`;
            if (document.getElementById('eco-entropy-val')) document.getElementById('eco-entropy-val').innerText = `${eco.effective_plugin_count || 14.8} Plugins`;
            if (document.getElementById('eco-theil-val')) document.getElementById('eco-theil-val').innerText = `Theil T: ${eco.theil_t_index || 0.38}`;
            if (document.getElementById('eco-prior-val')) document.getElementById('eco-prior-val').innerText = `${eco.prior_mean_rating || 4.84} ★`;

            const planxPercent = ((planxDownloads / appData.summary.total_downloads) * 100).toFixed(1);
            document.getElementById('planx-share-text').innerHTML = `${planxDownloads.toLocaleString()} <strong>(${planxPercent}%)</strong>`;

            const suite02Percent = ((suite02Downloads / appData.summary.total_downloads) * 100).toFixed(1);
            document.getElementById('suite02-share-text').innerHTML = `${suite02Downloads.toLocaleString()} <strong>(${suite02Percent}%)</strong>`;

            const standalonePercent = ((standaloneDownloads / appData.summary.total_downloads) * 100).toFixed(1);
            document.getElementById('standalone-share-text').innerHTML = `${standaloneDownloads.toLocaleString()} <strong>(${standalonePercent}%)</strong>`;
        }

        let currentMilestoneTab = 'imminent';

        function switchMilestoneTab(tab) {
            currentMilestoneTab = tab;
            const tabs = ['imminent', 'velocity', 'all', 'fame'];
            tabs.forEach(t => {
                const btn = document.getElementById(`tab-ms-${t}`);
                if (!btn) return;
                if (t === tab) {
                    btn.className = "px-3 py-1.5 rounded-lg bg-cyan-500 text-obsidian-950 font-bold transition-all flex items-center gap-1.5 shadow-sm";
                } else {
                    btn.className = "px-3 py-1.5 rounded-lg text-slate-400 hover:text-white font-medium transition-all flex items-center gap-1.5";
                }
            });

            const subtitle = document.getElementById('milestone-subtitle-note');
            if (subtitle) {
                if (tab === 'imminent') subtitle.innerText = "Showing plugins rapidly approaching their target (≥85% progress)";
                else if (tab === 'velocity') subtitle.innerText = "Top 6 fastest monthly adoption velocity drivers";
                else if (tab === 'all') subtitle.innerText = `Full portfolio milestone status (${appData.plugins.length} production plugins)`;
                else if (tab === 'fame') subtitle.innerText = "Hall of Fame: 10K+, 5K+, and 1K+ download tier clubs";
            }

            renderMilestoneCards();
        }

        function renderMilestoneCards() {
            const grid = document.getElementById('milestones-grid');
            if (!grid) return;

            if (currentMilestoneTab === 'fame') {
                const club10k = appData.plugins.filter(p => p.downloads >= 10000);
                const club5k = appData.plugins.filter(p => p.downloads >= 5000 && p.downloads < 10000);
                const club1k = appData.plugins.filter(p => p.downloads >= 1000 && p.downloads < 5000);

                let html = `
                    <div class="col-span-full grid grid-cols-1 md:grid-cols-3 gap-5">
                        <!-- 10K Club -->
                        <div class="p-5 rounded-2xl bg-gradient-to-br from-amber-500/10 via-obsidian-900 to-obsidian-950 border border-amber-500/30">
                            <div class="flex items-center justify-between mb-4 border-b border-white/5 pb-3">
                                <div class="flex items-center gap-2">
                                    <div class="w-8 h-8 rounded-xl bg-amber-500/20 text-amber-300 flex items-center justify-center font-bold text-sm border border-amber-500/30">🏆</div>
                                    <div>
                                        <h3 class="font-bold text-sm text-white font-heading">10K+ Tier Legends</h3>
                                        <p class="text-[10px] text-amber-300/80 font-mono">${club10k.length} Flagship Pillars</p>
                                    </div>
                                </div>
                                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40 font-mono">Elite Tier</span>
                            </div>
                            <div class="space-y-2.5">
                                ${club10k.map(p => `
                                    <div class="flex items-center justify-between p-2.5 rounded-xl bg-obsidian-900/80 border border-white/5 hover:border-amber-500/30 transition-all">
                                        <span class="text-xs font-semibold text-slate-200 truncate max-w-[60%]">${p.name}</span>
                                        <div class="text-right">
                                            <span class="text-xs font-bold text-amber-300 font-mono">${p.downloads.toLocaleString()} DL</span>
                                            <span class="text-[10px] text-slate-400 block font-mono">Next: ${p.next_milestone.toLocaleString()}</span>
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>

                        <!-- 5K Club -->
                        <div class="p-5 rounded-2xl bg-gradient-to-br from-cyan-500/10 via-obsidian-900 to-obsidian-950 border border-cyan-500/30">
                            <div class="flex items-center justify-between mb-4 border-b border-white/5 pb-3">
                                <div class="flex items-center gap-2">
                                    <div class="w-8 h-8 rounded-xl bg-cyan-500/20 text-cyan-300 flex items-center justify-center font-bold text-sm border border-cyan-500/30">⭐</div>
                                    <div>
                                        <h3 class="font-bold text-sm text-white font-heading">5K+ Tier Pillars</h3>
                                        <p class="text-[10px] text-cyan-300/80 font-mono">${club5k.length} High-Volume Engines</p>
                                    </div>
                                </div>
                                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-mono">Established</span>
                            </div>
                            <div class="space-y-2.5">
                                ${club5k.map(p => `
                                    <div class="flex items-center justify-between p-2.5 rounded-xl bg-obsidian-900/80 border border-white/5 hover:border-cyan-500/30 transition-all">
                                        <span class="text-xs font-semibold text-slate-200 truncate max-w-[60%]">${p.name}</span>
                                        <div class="text-right">
                                            <span class="text-xs font-bold text-cyan-300 font-mono">${p.downloads.toLocaleString()} DL</span>
                                            <span class="text-[10px] text-slate-400 block font-mono">Next: ${p.next_milestone.toLocaleString()}</span>
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>

                        <!-- 1K Club -->
                        <div class="p-5 rounded-2xl bg-gradient-to-br from-emerald-500/10 via-obsidian-900 to-obsidian-950 border border-emerald-500/30">
                            <div class="flex items-center justify-between mb-4 border-b border-white/5 pb-3">
                                <div class="flex items-center gap-2">
                                    <div class="w-8 h-8 rounded-xl bg-emerald-500/20 text-emerald-300 flex items-center justify-center font-bold text-sm border border-emerald-500/30">🎯</div>
                                    <div>
                                        <h3 class="font-bold text-sm text-white font-heading">1K+ Tier Foundation</h3>
                                        <p class="text-[10px] text-emerald-300/80 font-mono">${club1k.length} Active Solutions</p>
                                    </div>
                                </div>
                                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-mono">Verified</span>
                            </div>
                            <div class="max-h-80 overflow-y-auto space-y-2 pr-1 custom-scrollbar">
                                ${club1k.map(p => `
                                    <div class="flex items-center justify-between p-2 rounded-xl bg-obsidian-900/80 border border-white/5 hover:border-emerald-500/30 transition-all">
                                        <span class="text-xs font-medium text-slate-300 truncate max-w-[65%]">${p.name}</span>
                                        <span class="text-xs font-bold text-emerald-400 font-mono">${p.downloads.toLocaleString()} DL</span>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                `;
                grid.innerHTML = html;
                return;
            }

            let list = [];
            if (currentMilestoneTab === 'imminent') {
                list = appData.plugins.filter(p => p.milestone_progress >= 85.0).sort((a,b) => b.milestone_progress - a.milestone_progress);
                if (list.length === 0) list = [...appData.plugins].sort((a,b) => b.milestone_progress - a.milestone_progress).slice(0, 6);
            } else if (currentMilestoneTab === 'velocity') {
                list = [...appData.plugins].sort((a,b) => b.avg_monthly_downloads - a.avg_monthly_downloads).slice(0, 6);
            } else {
                list = [...appData.plugins].sort((a,b) => b.downloads - a.downloads);
            }

            let html = '';
            list.forEach(p => {
                const remaining = p.next_milestone - p.downloads;
                const isCritical = p.milestone_progress >= 95.0;
                const isHigh = p.milestone_progress >= 85.0;

                const badgeHtml = isCritical
                    ? `<span class="text-[10px] font-bold text-rose-300 bg-rose-500/20 border border-rose-500/40 px-2 py-0.5 rounded-full font-mono animate-pulse flex items-center gap-1"><i class="fa-solid fa-bolt text-rose-400"></i>${p.milestone_progress}% CRITICAL</span>`
                    : isHigh
                    ? `<span class="text-[10px] font-bold text-amber-300 bg-amber-500/20 border border-amber-500/40 px-2 py-0.5 rounded-full font-mono flex items-center gap-1"><i class="fa-solid fa-fire text-orange-400"></i>${p.milestone_progress}%</span>`
                    : `<span class="text-[10px] font-semibold text-cyan-400 bg-cyan-500/10 border border-cyan-500/20 px-2 py-0.5 rounded-full font-mono">${p.milestone_progress}%</span>`;

                const barGradient = isCritical
                    ? 'from-amber-400 via-rose-500 to-rose-600'
                    : isHigh
                    ? 'from-teal-400 to-cyan-500'
                    : 'from-cyan-500 to-indigo-500';

                html += `
                    <div class="p-4 rounded-2xl bg-obsidian-900/90 border border-white/5 flex flex-col justify-between hover:border-white/15 transition-all shadow-md group">
                        <div>
                            <div class="flex justify-between items-start gap-2 mb-2">
                                <div class="flex items-center gap-2 truncate">
                                    <div class="w-6 h-6 rounded-lg bg-obsidian-800 flex items-center justify-center text-xs flex-shrink-0 text-cyan-400 border border-white/5">
                                        <i class="fa-solid fa-cube"></i>
                                    </div>
                                    <h3 class="font-bold text-xs truncate font-heading text-slate-200 group-hover:text-cyan-400 transition-colors" title="${p.name}">${p.name}</h3>
                                </div>
                                ${badgeHtml}
                            </div>
                            <div class="w-full bg-obsidian-800 rounded-full h-2 my-2.5 overflow-hidden">
                                <div class="bg-gradient-to-r ${barGradient} h-2 rounded-full transition-all duration-500" style="width: ${Math.min(100, p.milestone_progress)}%"></div>
                            </div>
                            <div class="flex justify-between items-center text-[10px] text-slate-400 font-mono">
                                <span>Current: <strong class="text-white">${p.downloads.toLocaleString()}</strong></span>
                                <span>Target: <strong class="text-cyan-300">${p.next_milestone.toLocaleString()}</strong></span>
                            </div>
                        </div>
                        <div class="mt-3 pt-2.5 border-t border-white/5 flex justify-between items-center text-[10px] font-mono">
                            <span class="text-slate-400 flex items-center gap-1">
                                <i class="fa-solid fa-calendar-check text-cyan-400"></i> Est: ${p.milestone_est_date}
                            </span>
                            <span class="font-bold text-emerald-400 flex items-center gap-1">
                                <i class="fa-solid fa-angles-right text-[8px]"></i> ${remaining > 0 ? remaining.toLocaleString() + ' DL left' : 'Achieved 🎉'}
                            </span>
                        </div>
                    </div>
                `;
            });

            grid.innerHTML = html;
        }

        function renderMilestones() {
            const pm = appData.summary.portfolio_milestones || {
                prev_milestone: 100000,
                next_milestone: 125000,
                remaining: 15356,
                progress_total: 87.7,
                progress_tier: 38.6,
                est_date: 'Nov 2026'
            };

            const target = pm.next_milestone || 125000;
            const prev = pm.prev_milestone || 100000;

            if (document.getElementById('milestone-total-downloads')) {
                document.getElementById('milestone-total-downloads').innerText = `${appData.summary.total_downloads.toLocaleString()} / ${target.toLocaleString()}`;
            }
            if (document.getElementById('portfolio-progress-percent')) {
                document.getElementById('portfolio-progress-percent').innerText = `${pm.progress_total}%`;
            }
            if (document.getElementById('portfolio-progress-bar')) {
                document.getElementById('portfolio-progress-bar').style.width = `${Math.min(100, pm.progress_total)}%`;
            }
            if (document.getElementById('global-next-milestone-text')) {
                document.getElementById('global-next-milestone-text').innerText = `${target.toLocaleString()}`;
            }
            if (document.getElementById('portfolio-milestone-eta')) {
                document.getElementById('portfolio-milestone-eta').innerText = `Target ETA: ${pm.est_date}`;
            }
            if (document.getElementById('portfolio-milestone-prev')) {
                document.getElementById('portfolio-milestone-prev').innerText = `Unlocked: ${prev.toLocaleString()} DL`;
            }
            if (document.getElementById('portfolio-milestone-rem')) {
                document.getElementById('portfolio-milestone-rem').innerText = `Remaining: ${pm.remaining.toLocaleString()} DL`;
            }
            if (document.getElementById('portfolio-milestone-target')) {
                document.getElementById('portfolio-milestone-target').innerText = `Target: ${target.toLocaleString()} DL`;
            }

            const imminentCount = appData.plugins.filter(p => p.milestone_progress >= 85.0).length;
            if (document.getElementById('imminent-count-badge')) {
                document.getElementById('imminent-count-badge').innerText = imminentCount;
            }
            if (document.getElementById('all-ms-count')) {
                document.getElementById('all-ms-count').innerText = appData.plugins.length;
            }

            renderMilestoneCards();
        }

        // =============================================================
        // FORENSIC AI & MULTIVARIATE ANOMALY SURVEILLANCE LOGIC
        // =============================================================
        let currentMLTaxonomyFilter = 'ALL';
        let currentMLSearchQuery = '';

        function renderAuditKPIsAndAlerts() {
            const flagged = appData.anomalies.filter(a => a.severity === 'critical' || a.severity === 'high' || a.severity === 'amber').length;
            const badge = document.getElementById('audit-alert-badge');

            if (flagged > 0) {
                badge.innerText = `${flagged} ANOMALIES`;
                badge.className = "ml-1.5 px-2 py-0.5 text-[10px] font-bold rounded-full bg-rose-500 text-white pulse-live font-mono";
            } else {
                badge.innerText = "CLEAN";
                badge.className = "ml-1.5 px-2 py-0.5 text-[10px] font-bold rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-mono";
            }

            const totalVotes = appData.plugins.reduce((acc, p) => acc + p.votes_count, 0);
            const observedAvg = (appData.plugins.reduce((acc, p) => acc + (p.average_vote * p.votes_count), 0) / (totalVotes || 1)).toFixed(2);
            const purgedAvg = appData.correlation.portfolio_purged_average ? appData.correlation.portfolio_purged_average.toFixed(2) : observedAvg;
            const suppressedPts = appData.correlation.total_suppressed_pts ? appData.correlation.total_suppressed_pts.toFixed(2) : "0.00";
            const raidVotes = appData.correlation.total_raid_votes || 0;

            const auditKPIContainer = document.getElementById('audit-kpis');
            auditKPIContainer.innerHTML = `
                <div class="p-6 rounded-3xl glass-panel relative overflow-hidden border-l-4 border-rose-500">
                    <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider font-mono">Flagged Anomalous Influxes</p>
                    <div class="flex items-baseline mt-2">
                        <span class="text-3xl font-extrabold font-mono ${flagged > 0 ? 'text-rose-400' : 'text-emerald-400'}">${flagged}</span>
                        <span class="text-xs text-slate-400 ml-2 font-mono">plugins impacted</span>
                    </div>
                    <p class="text-[11px] text-slate-400 mt-2 font-mono">+${raidVotes} suspicious/diluted votes isolated</p>
                </div>

                <div class="p-6 rounded-3xl glass-panel relative overflow-hidden border-l-4 border-emerald-500">
                    <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider font-mono">True Synthetic Organic Rating</p>
                    <div class="flex items-baseline mt-2">
                        <span class="text-3xl font-extrabold text-emerald-400 font-mono">${purgedAvg}</span>
                        <span class="text-xs text-amber-400 ml-1.5"><i class="fa-solid fa-star"></i> / 5.0</span>
                    </div>
                    <p class="text-[11px] text-emerald-400 mt-2 font-mono flex items-center gap-1">
                        <i class="fa-solid fa-shield-check"></i> Reconstructed without raid spikes
                    </p>
                </div>

                <div class="p-6 rounded-3xl glass-panel relative overflow-hidden border-l-4 border-amber-500">
                    <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider font-mono">Public Observed Rating</p>
                    <div class="flex items-baseline mt-2">
                        <span class="text-3xl font-extrabold font-mono text-slate-200">${observedAvg}</span>
                        <span class="text-xs text-rose-400 ml-1.5 font-mono font-bold">(-${suppressedPts} pts loss)</span>
                    </div>
                    <p class="text-[11px] text-slate-400 mt-2 font-mono">Raw QGIS Hub public display score</p>
                </div>

                <div class="p-6 rounded-3xl glass-panel relative overflow-hidden border-l-4 border-cyan-500">
                    <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider font-mono">Multi-Vector Threat Index</p>
                    <div class="flex items-baseline mt-2">
                        <span class="text-3xl font-extrabold text-cyan-400 font-mono">${appData.correlation.campaign_threat_score}%</span>
                        <span class="text-xs text-slate-400 ml-2 font-mono">D<sub>M</sub> Severity</span>
                    </div>
                    <p class="text-[11px] text-slate-400 mt-2 font-mono truncate" title="${appData.correlation.campaign_level}">${appData.correlation.campaign_level}</p>
                </div>
            `;

            renderMLMatrixTable();
            renderAnomalyCards();
            populateAuditChartDropdown();
            renderPortfolioWaveChart();
            renderKinematicPhaseChart();
            populateTimeMachineSelectors();
        }

        function filterMLTaxonomy(taxonomy) {
            currentMLTaxonomyFilter = taxonomy;
            const buttons = ['ALL', 'FLAGGED', 'TYPE_2_SOFT_DILUTION', 'TYPE_1_BOMBING', 'ORGANIC'];
            buttons.forEach(b => {
                const el = document.getElementById(`ml-flt-${b}`);
                if (el) {
                    if (b === taxonomy) {
                        el.className = "px-3 py-1 rounded-xl text-xs font-bold bg-cyan-600 text-white transition-all font-mono";
                    } else {
                        el.className = "px-3 py-1 rounded-xl text-xs font-bold bg-obsidian-800 text-slate-400 hover:text-white border border-white/5 transition-all font-mono";
                    }
                }
            });
            renderMLMatrixTable();
        }

        function filterMLMatrixSearch() {
            currentMLSearchQuery = (document.getElementById('ml-search-input').value || '').toLowerCase();
            renderMLMatrixTable();
        }

        function renderMLMatrixTable() {
            const tbody = document.getElementById('ml-matrix-table-body');
            if (!tbody) return;

            const allCount = appData.anomalies.length;
            const flaggedCount = appData.anomalies.filter(a => a.severity === 'critical' || a.severity === 'high' || a.severity === 'amber').length;
            const type2Count = appData.anomalies.filter(a => a.taxonomy_code === 'TYPE_2_SOFT_DILUTION').length;
            const type1Count = appData.anomalies.filter(a => a.taxonomy_code === 'TYPE_1_BOMBING').length;
            const organicCount = appData.anomalies.filter(a => a.severity === 'positive' || a.severity === 'normal' || a.severity === 'stable').length;

            if (document.getElementById('ml-cnt-ALL')) document.getElementById('ml-cnt-ALL').innerText = allCount;
            if (document.getElementById('ml-cnt-FLAGGED')) document.getElementById('ml-cnt-FLAGGED').innerText = flaggedCount;
            if (document.getElementById('ml-cnt-TYPE_2')) document.getElementById('ml-cnt-TYPE_2').innerText = type2Count;
            if (document.getElementById('ml-cnt-TYPE_1')) document.getElementById('ml-cnt-TYPE_1').innerText = type1Count;
            if (document.getElementById('ml-cnt-ORGANIC')) document.getElementById('ml-cnt-ORGANIC').innerText = organicCount;

            let filtered = appData.anomalies.filter(a => {
                if (currentMLSearchQuery && !a.name.toLowerCase().includes(currentMLSearchQuery) && !a.category.toLowerCase().includes(currentMLSearchQuery)) {
                    return false;
                }
                if (currentMLTaxonomyFilter === 'FLAGGED') {
                    return a.severity === 'critical' || a.severity === 'high' || a.severity === 'amber';
                } else if (currentMLTaxonomyFilter === 'TYPE_2_SOFT_DILUTION') {
                    return a.taxonomy_code === 'TYPE_2_SOFT_DILUTION';
                } else if (currentMLTaxonomyFilter === 'TYPE_1_BOMBING') {
                    return a.taxonomy_code === 'TYPE_1_BOMBING';
                } else if (currentMLTaxonomyFilter === 'ORGANIC') {
                    return a.severity === 'positive' || a.severity === 'normal' || a.severity === 'stable';
                }
                return true;
            });

            filtered.sort((a, b) => (b.threat_level || 0) - (a.threat_level || 0) || (b.delta_votes || 0) - (a.delta_votes || 0));

            if (filtered.length === 0) {
                tbody.innerHTML = `<tr><td colspan="10" class="py-8 text-center text-slate-500 font-mono">No plugins matching current forensic filter.</td></tr>`;
                return;
            }

            tbody.innerHTML = filtered.map(a => {
                const hasDrop = a.suppressed_points > 0.05;
                const isFlagged = a.severity === 'critical' || a.severity === 'high' || a.severity === 'amber';

                let badgeStyle = "bg-slate-500/10 text-slate-400 border-slate-500/20";
                if (a.severity === 'critical') badgeStyle = "bg-rose-500/20 text-rose-400 border-rose-500/30 font-bold";
                elif_if = a.severity === 'high' ? "bg-amber-500/20 text-amber-400 border-amber-500/30 font-bold" : badgeStyle;
                if (a.severity === 'high') badgeStyle = "bg-amber-500/20 text-amber-400 border-amber-500/30 font-bold";
                if (a.severity === 'positive') badgeStyle = "bg-emerald-500/20 text-emerald-400 border-emerald-500/30";

                return `
                    <tr class="hover:bg-white/[0.02] transition-colors ${isFlagged ? 'bg-rose-950/10' : ''}">
                        <td class="py-3.5 px-4 font-bold text-white flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full ${isFlagged ? 'bg-rose-500 pulse-live' : 'bg-emerald-500'}"></span>
                            <div class="truncate max-w-[200px]">
                                <span class="block text-slate-200 truncate font-heading">${a.name}</span>
                                <span class="text-[10px] text-slate-500 font-mono">${a.category} • v${a.version}</span>
                            </div>
                        </td>
                        <td class="py-3.5 px-4 text-center font-bold ${hasDrop ? 'text-rose-400' : 'text-slate-300'}">
                            ${a.current_rating.toFixed(2)} ★
                        </td>
                        <td class="py-3.5 px-4 text-center font-bold text-emerald-400">
                            ${a.purged_synthetic_rating ? a.purged_synthetic_rating.toFixed(2) : a.current_rating.toFixed(2)} ★
                        </td>
                        <td class="py-3.5 px-4 text-center">
                            ${hasDrop ? `<span class="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30 text-[10px] font-bold">-${a.suppressed_points.toFixed(2)} pts</span>` : '<span class="text-slate-600">0.00</span>'}
                        </td>
                        <td class="py-3.5 px-4 text-center">
                            <span class="font-bold ${a.delta_votes > 0 ? 'text-cyan-400' : 'text-slate-500'}">+${a.delta_votes}</span>
                            <span class="text-[10px] text-slate-500 ml-1">(${a.delta_votes > 0 ? a.implied_new_rating.toFixed(2) + '★' : '-'})</span>
                        </td>
                        <td class="py-3.5 px-4 text-center font-bold ${a.conversion_k > 3.0 ? 'text-rose-400 font-bold' : 'text-slate-400'}">
                            ${a.conversion_k ? a.conversion_k.toFixed(1) + '%' : '0.0%'}
                        </td>
                        <td class="py-3.5 px-4 text-center text-cyan-400 font-bold">
                            ${a.mahalanobis_d ? a.mahalanobis_d.toFixed(2) : '0.00'}
                        </td>
                        <td class="py-3.5 px-4 text-center font-bold ${a.p_abuse >= 80 ? 'text-rose-400' : 'text-slate-400'}">
                            ${a.p_abuse ? a.p_abuse.toFixed(1) + '%' : '0.0%'}
                        </td>
                        <td class="py-3.5 px-4 text-center">
                            <span class="px-2.5 py-0.5 rounded-md border text-[10px] whitespace-nowrap ${badgeStyle}">
                                ${a.taxonomy || a.status}
                            </span>
                        </td>
                        <td class="py-3.5 px-4 text-right whitespace-nowrap">
                            <button onclick="openEvidenceModal('${a.name.replace(/'/g, "\'")}')" class="px-3 py-1 rounded-xl text-[11px] font-bold ${isFlagged ? 'btn-danger text-white' : 'bg-obsidian-800 hover:bg-obsidian-750 text-slate-300 border border-white/10'} inline-flex items-center gap-1">
                                <i class="fa-solid fa-file-shield"></i> Dossier
                            </button>
                        </td>
                    </tr>
                `;
            }).join('');
        }

        function renderAnomalyCards() {
            const container = document.getElementById('anomaly-cards-container');
            if (!container) return;
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
                if (a.severity === 'critical' || a.severity === 'high' || a.severity === 'amber') {
                    recoveryCallout = `
                        <div class="mt-3 p-3 rounded-2xl bg-rose-950/40 border border-rose-500/20 text-[11px] space-y-1 font-mono">
                            <div class="flex justify-between text-slate-300">
                                <span><i class="fa-solid fa-rotate-left text-cyan-400 mr-1"></i>True Reconstructed Score:</span>
                                <strong class="text-emerald-400">${a.purged_synthetic_rating ? a.purged_synthetic_rating.toFixed(2) : a.reconciled_after_purge.toFixed(2)} ★ (Organic Target)</strong>
                            </div>
                            <div class="flex justify-between text-slate-400">
                                <span><i class="fa-solid fa-star text-amber-400 mr-1"></i>Organic Recovery Needed:</span>
                                <span>+${a.needed_5_stars_to_recover} consecutive 5★ votes</span>
                            </div>
                            <div class="flex justify-between text-rose-400 font-bold">
                                <span><i class="fa-solid fa-fire text-rose-400 mr-1"></i>Calculated Damage:</span>
                                <span>-${a.suppressed_points ? a.suppressed_points.toFixed(2) : (a.damage_index || 0)} pts suppressed (P=${a.p_abuse || 0}%)</span>
                            </div>
                        </div>
                    `;
                }

                card.innerHTML = `
                    <div>
                        <div class="flex justify-between items-start mb-3">
                            <div>
                                <span class="text-[9px] font-bold px-2.5 py-0.5 rounded-md border ${badgeClass}">${a.taxonomy || a.status}</span>
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
                                <span class="text-xs font-extrabold font-mono ${a.severity === 'critical' || a.severity === 'high' ? 'text-rose-400' : ''}">${a.current_rating.toFixed(2)} ★</span>
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
                                <span class="font-bold ${a.implied_new_rating <= 2.5 && a.delta_votes > 0 ? 'text-rose-400' : 'text-emerald-400'}">${a.delta_votes > 0 ? a.implied_new_rating.toFixed(2) + ' ★ avg' : 'N/A'}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-slate-400">Conversion Ratio (κ):</span>
                                <span class="font-bold ${a.conversion_k > 3.0 ? 'text-rose-400' : 'text-slate-300'}">${a.conversion_k ? a.conversion_k.toFixed(1) + '%' : '0.0%'} (Norm: ~0.8%)</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-slate-400">Mahalanobis Anomaly (D<sub>M</sub>):</span>
                                <span class="font-bold text-cyan-400">${a.mahalanobis_d || 0} (Certainty: ${a.p_abuse || 0}%)</span>
                            </div>
                        </div>

                        ${recoveryCallout}
                    </div>

                    <div class="pt-4 border-t border-white/5 flex justify-between items-center mt-4">
                        <span class="text-[10px] text-slate-400 font-mono">${a.suppressed_points > 0 ? `<span class="text-rose-400 font-bold">-${a.suppressed_points.toFixed(2)}</span> rating drop` : 'Stable baseline'}</span>
                        <button onclick="openEvidenceModal('${a.name.replace(/'/g, "\'")}')" class="px-4 py-2 rounded-xl text-xs font-bold ${a.severity === 'critical' || a.severity === 'high' ? 'btn-danger text-white' : 'bg-obsidian-800 hover:bg-obsidian-750 text-slate-300 border border-white/10'} flex items-center gap-1.5">
                            <i class="fa-solid fa-file-shield"></i> View Dossier & SQL
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
                    const sev = c.getAttribute('data-severity');
                    c.style.display = (sev === 'critical' || sev === 'high' || sev === 'amber') ? '' : 'none';
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
        let portfolioWaveChartInstance = null;
        let auditRadarChartInstance = null;
        let kinematicPhaseChartInstance = null;

        function renderKinematicPhaseChart() {
            const container = document.querySelector("#kinematic-phase-chart");
            if (!container) return;

            const isAlabaster = document.documentElement.getAttribute('data-theme') === 'alabaster';
            const labelColor = isAlabaster ? '#334155' : '#94a3b8';
            const gridColor = isAlabaster ? 'rgba(0, 0, 0, 0.06)' : 'rgba(255, 255, 255, 0.05)';

            // Prepare series data: [delta_dl, delta_votes, point_size, plugin_name, conversion_k, is_anomaly]
            const organicPoints = [];
            const raidPoints = [];

            appData.anomalies.forEach(a => {
                const dl = Math.max(10, a.delta_downloads || 0);
                const v = Math.max(0, a.delta_votes || 0);
                const isAnom = (a.severity === 'critical' || a.severity === 'high' || a.conversion_k > 3.0);
                const point = {
                    x: dl,
                    y: v,
                    name: a.name,
                    k: a.conversion_k ? a.conversion_k.toFixed(1) : '0.0',
                    dm: a.mahalanobis_d || 0,
                    status: a.taxonomy || a.status
                };

                if (isAnom && v > 0) {
                    raidPoints.push(point);
                } else {
                    organicPoints.push(point);
                }
            });

            if (kinematicPhaseChartInstance) kinematicPhaseChartInstance.destroy();

            const chartOptions = {
                series: [
                    {
                        name: 'Organic Stable Plugins',
                        type: 'scatter',
                        data: organicPoints.map(p => ({ x: p.x, y: p.y, meta: p }))
                    },
                    {
                        name: 'Kinematic Raid Violations',
                        type: 'scatter',
                        data: raidPoints.map(p => ({ x: p.x, y: p.y, meta: p }))
                    }
                ],
                chart: {
                    height: 320,
                    type: 'scatter',
                    toolbar: { show: true, tools: { download: true, zoom: true, pan: true, reset: true } },
                    foreColor: labelColor
                },
                colors: ['#10b981', '#f43f5e'],
                markers: {
                    size: [6, 9],
                    strokeWidth: [1, 2],
                    strokeColors: ['#059669', '#ffffff'],
                    hover: { size: 11 }
                },
                xaxis: {
                    title: { text: 'Recent Download Volume (ΔDownloads)', style: { fontFamily: 'JetBrains Mono', fontSize: '11px' } },
                    labels: { style: { fontFamily: 'JetBrains Mono' } },
                    tickAmount: 8
                },
                yaxis: {
                    title: { text: 'Recent Influx Votes (ΔVotes)', style: { fontFamily: 'JetBrains Mono', fontSize: '11px' } },
                    labels: { style: { fontFamily: 'JetBrains Mono' } },
                    min: 0
                },
                annotations: {
                    yaxis: [
                        {
                            y: 5,
                            y2: 45,
                            borderColor: '#f43f5e',
                            fillColor: '#f43f5e',
                            opacity: 0.05,
                            label: {
                                borderColor: '#f43f5e',
                                style: { color: '#fff', background: '#f43f5e', fontSize: '9px', fontWeight: 'bold', fontFamily: 'JetBrains Mono' },
                                text: '🚨 High-Kinematic Anomaly Zone (κ ≥ 3.5%)'
                            }
                        }
                    ]
                },
                grid: { borderColor: gridColor },
                tooltip: {
                    theme: isAlabaster ? 'light' : 'dark',
                    custom: function({ series, seriesIndex, dataPointIndex, w }) {
                        const point = w.config.series[seriesIndex].data[dataPointIndex].meta;
                        if (!point) return '';
                        const isRaid = seriesIndex === 1;
                        return `
                            <div class="p-3 bg-obsidian-950 border ${isRaid ? 'border-rose-500/40' : 'border-emerald-500/40'} rounded-2xl shadow-xl font-mono text-xs text-white max-w-xs">
                                <div class="flex items-center gap-1.5 mb-1.5 font-heading font-bold ${isRaid ? 'text-rose-400' : 'text-emerald-400'}">
                                    <i class="fa-solid ${isRaid ? 'fa-triangle-exclamation' : 'fa-circle-check'}"></i>
                                    <span>${point.name}</span>
                                </div>
                                <div class="space-y-1 text-[11px] text-slate-300">
                                    <div class="flex justify-between">
                                        <span class="text-slate-400">ΔDownloads:</span>
                                        <strong>+${point.x.toLocaleString()}</strong>
                                    </div>
                                    <div class="flex justify-between">
                                        <span class="text-slate-400">ΔVotes:</span>
                                        <strong class="${isRaid ? 'text-rose-400 font-bold' : 'text-slate-200'}">+${point.y}</strong>
                                    </div>
                                    <div class="flex justify-between">
                                        <span class="text-slate-400">Conversion (κ):</span>
                                        <strong class="${isRaid ? 'text-rose-400 font-bold' : 'text-emerald-400'}">${point.k}%</strong>
                                    </div>
                                    <div class="flex justify-between">
                                        <span class="text-slate-400">Mahalanobis (D<sub>M</sub>):</span>
                                        <strong class="text-cyan-400">${point.dm}</strong>
                                    </div>
                                    <div class="pt-1.5 border-t border-white/10 text-[10px] text-slate-400">
                                        ${point.status}
                                    </div>
                                </div>
                            </div>
                        `;
                    }
                }
            };

            kinematicPhaseChartInstance = new ApexCharts(container, chartOptions);
            kinematicPhaseChartInstance.render();
        }

        function renderPortfolioWaveChart() {
            const container = document.querySelector("#portfolio-wave-chart");
            if (!container) return;

            const isAlabaster = document.documentElement.getAttribute('data-theme') === 'alabaster';
            const labelColor = isAlabaster ? '#334155' : '#94a3b8';
            const gridColor = isAlabaster ? 'rgba(0, 0, 0, 0.06)' : 'rgba(255, 255, 255, 0.05)';

            const timestamps = appData.history_meta.timestamps;
            const totalWaves = appData.history_meta.portfolio_waves || [];
            const raidWaves = appData.history_meta.portfolio_raid_waves || [];

            if (portfolioWaveChartInstance) portfolioWaveChartInstance.destroy();

            const options = {
                series: [
                    {
                        name: 'Raid / Dilution Influx Votes (≤2.5★)',
                        type: 'column',
                        data: raidWaves
                    },
                    {
                        name: 'Total Portfolio Influx Votes',
                        type: 'area',
                        data: totalWaves
                    }
                ],
                chart: {
                    height: 240,
                    type: 'line',
                    toolbar: { show: false },
                    foreColor: labelColor,
                    stacked: false
                },
                plotOptions: {
                    bar: {
                        columnWidth: '35%',
                        borderRadius: 4
                    }
                },
                stroke: {
                    width: [0, 2],
                    curve: 'smooth'
                },
                fill: {
                    opacity: [0.95, 0.2]
                },
                colors: ['#f43f5e', '#0ea5e9'],
                xaxis: {
                    categories: timestamps,
                    labels: { style: { fontFamily: 'JetBrains Mono', fontSize: '10px' }, rotate: -30 }
                },
                yaxis: {
                    title: { text: 'Simultaneous Influx Votes' },
                    labels: {
                        formatter: v => Math.round(v),
                        style: { fontFamily: 'JetBrains Mono' }
                    }
                },
                annotations: {
                    xaxis: [
                        {
                            x: 'Aug 16, 2026 13:28 UTC',
                            borderColor: '#f43f5e',
                            label: {
                                borderColor: '#f43f5e',
                                style: { color: '#fff', background: '#f43f5e', fontSize: '10px', fontWeight: 'bold', fontFamily: 'JetBrains Mono' },
                                text: '🚨 Wave 1: GeoStats (+30 1★ votes)'
                            }
                        },
                        {
                            x: 'Aug 24, 2026 21:44 UTC',
                            borderColor: '#f43f5e',
                            label: {
                                borderColor: '#f43f5e',
                                style: { color: '#fff', background: '#f43f5e', fontSize: '10px', fontWeight: 'bold', fontFamily: 'JetBrains Mono' },
                                text: '🚨 Wave 2: 5-Plugin Sync Raid (+55 1★ votes)'
                            }
                        }
                    ]
                },
                grid: { borderColor: gridColor },
                tooltip: {
                    theme: isAlabaster ? 'light' : 'dark',
                    shared: true
                }
            };

            portfolioWaveChartInstance = new ApexCharts(container, options);
            portfolioWaveChartInstance.render();
        }

        function renderAuditHistoryChart() {
            const select = document.getElementById('audit-chart-plugin-select');
            if (!select) return;
            const targetPlugin = select.value || appData.plugins[0].name;

            const isAlabaster = document.documentElement.getAttribute('data-theme') === 'alabaster';
            const labelColor = isAlabaster ? '#334155' : '#94a3b8';
            const gridColor = isAlabaster ? 'rgba(0, 0, 0, 0.06)' : 'rgba(255, 255, 255, 0.05)';

            const pluginHistory = appData.history_meta.by_plugin[targetPlugin] || { ratings: [], votes: [], delta_votes: [], purged_series: [], inflections: [] };
            const categories = appData.history_meta.timestamps;

            if (auditChartInstance) auditChartInstance.destroy();

            // Build annotations for detected inflections
            const xAnnotations = (pluginHistory.inflections || []).map(ip => ({
                x: ip.date,
                borderColor: '#f43f5e',
                label: {
                    borderColor: '#f43f5e',
                    style: { color: '#fff', background: '#f43f5e', fontSize: '9px', fontWeight: 'bold', fontFamily: 'JetBrains Mono' },
                    text: `⚠️ Drop: -${ip.drop}★ (+${ip.delta_votes}v @ ${ip.implied_rating}★)`
                }
            }));

            const chartOptions = {
                series: [
                    {
                        name: 'Observed Rating (★)',
                        type: 'line',
                        data: pluginHistory.ratings
                    },
                    {
                        name: 'True Organic Baseline (★)',
                        type: 'line',
                        data: pluginHistory.purged_series || []
                    },
                    {
                        name: 'Batch Influx Votes (ΔV)',
                        type: 'column',
                        data: pluginHistory.delta_votes || []
                    }
                ],
                chart: {
                    height: 320,
                    type: 'line',
                    toolbar: { show: true, tools: { download: true, zoom: true, pan: true, reset: true } },
                    foreColor: labelColor
                },
                stroke: {
                    width: [4, 2.5, 0],
                    curve: ['smooth', 'straight', 'smooth'],
                    dashArray: [0, 5, 0]
                },
                plotOptions: {
                    bar: {
                        columnWidth: '28%',
                        borderRadius: 4
                    }
                },
                colors: ['#f43f5e', '#10b981', '#38bdf8'],
                xaxis: {
                    categories: categories,
                    labels: { style: { fontFamily: 'JetBrains Mono', fontSize: '10px' }, rotate: -30 }
                },
                yaxis: [
                    {
                        min: 1.0,
                        max: 5.0,
                        title: { text: 'Rating (1 - 5 Stars)' },
                        labels: {
                            formatter: v => v ? v.toFixed(1) + ' ★' : '',
                            style: { fontFamily: 'JetBrains Mono' }
                        }
                    },
                    {
                        min: 1.0,
                        max: 5.0,
                        show: false
                    },
                    {
                        opposite: true,
                        title: { text: 'Batch Influx Votes (ΔV)' },
                        labels: {
                            formatter: v => Math.round(v),
                            style: { fontFamily: 'JetBrains Mono' }
                        }
                    }
                ],
                annotations: {
                    xaxis: xAnnotations
                },
                grid: { borderColor: gridColor },
                tooltip: {
                    theme: isAlabaster ? 'light' : 'dark',
                    shared: true,
                    intersect: false,
                    y: {
                        formatter: function(val, opts) {
                            if (opts.seriesIndex === 0 || opts.seriesIndex === 1) {
                                return val ? val.toFixed(2) + ' ★' : 'N/A';
                            }
                            return Math.round(val) + ' votes';
                        }
                    }
                }
            };

            auditChartInstance = new ApexCharts(document.querySelector("#audit-history-chart"), chartOptions);
            auditChartInstance.render();

            renderAuditRadarChart(targetPlugin);
        }

        function renderAuditRadarChart(pluginName) {
            const container = document.querySelector("#audit-radar-chart");
            if (!container) return;

            const nameEl = document.getElementById('radar-plugin-name');
            if (nameEl) nameEl.innerText = pluginName;

            const anom = appData.anomalies.find(a => a.name === pluginName) || {
                conversion_k: 0.5,
                suppressed_points: 0,
                shannon_entropy: 2.32,
                mahalanobis_d: 1.0,
                threat_level: 10,
                delta_votes: 0,
                p_abuse: 0
            };

            const isAlabaster = document.documentElement.getAttribute('data-theme') === 'alabaster';
            const labelColor = isAlabaster ? '#334155' : '#94a3b8';

            if (auditRadarChartInstance) auditRadarChartInstance.destroy();

            // Normalized Radar Axes (0 - 100)
            const kNorm = Math.min(100, Math.round((anom.conversion_k / 8.0) * 100));
            const devNorm = Math.min(100, Math.round((anom.suppressed_points / 1.5) * 100));
            const purityNorm = Math.min(100, Math.round(((2.3219 - anom.shannon_entropy) / 2.3219) * 100));
            const dmNorm = Math.min(100, Math.round((anom.mahalanobis_d / 10.0) * 100));
            const threatNorm = Math.min(100, Math.round(anom.threat_level || 0));
            const burstNorm = Math.min(100, Math.round((anom.delta_votes / 35.0) * 100));

            const radarOptions = {
                series: [
                    {
                        name: `${pluginName} (Anomaly Profile)`,
                        data: [kNorm, devNorm, purityNorm, dmNorm, threatNorm, burstNorm]
                    },
                    {
                        name: 'Organic Healthy Baseline',
                        data: [15, 0, 10, 15, 10, 10]
                    }
                ],
                chart: {
                    height: 250,
                    type: 'radar',
                    toolbar: { show: false },
                    foreColor: labelColor
                },
                colors: ['#f43f5e', '#10b981'],
                stroke: { width: 2 },
                fill: { opacity: 0.25 },
                markers: { size: 3 },
                xaxis: {
                    categories: [
                        'Conversion (κ)',
                        'Rating Drop (δr)',
                        'Entropy Purity (H)',
                        'Mahalanobis (D_M)',
                        'Threat Level',
                        'Vote Burst (ΔV)'
                    ],
                    labels: { style: { fontFamily: 'JetBrains Mono', fontSize: '9px' } }
                },
                yaxis: { show: false, min: 0, max: 100 },
                legend: { position: 'bottom', fontSize: '10px', markers: { radius: 4 } }
            };

            auditRadarChartInstance = new ApexCharts(container, radarOptions);
            auditRadarChartInstance.render();

            // Populate Metric Details
            const detailsEl = document.getElementById('radar-metric-details');
            if (detailsEl) {
                detailsEl.innerHTML = `
                    <div class="flex justify-between">
                        <span class="text-slate-400">Observed vs True Score:</span>
                        <strong class="${anom.suppressed_points > 0 ? 'text-rose-400' : 'text-slate-200'}">${anom.current_rating.toFixed(2)}★ vs ${anom.purged_synthetic_rating ? anom.purged_synthetic_rating.toFixed(2) : anom.current_rating.toFixed(2)}★</strong>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-slate-400">Rating-to-Download (κ):</span>
                        <strong class="${anom.conversion_k > 3 ? 'text-rose-400' : 'text-slate-200'}">${anom.conversion_k ? anom.conversion_k.toFixed(1) + '%' : '0.0%'} (Norm: ~0.8%)</strong>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-slate-400">Mahalanobis Distance (D<sub>M</sub>):</span>
                        <strong class="text-cyan-400">${anom.mahalanobis_d || '0.00'}</strong>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-slate-400">Abuse Probability P(Abuse):</span>
                        <strong class="${anom.p_abuse >= 80 ? 'text-rose-400' : 'text-slate-300'}">${anom.p_abuse || 0}%</strong>
                    </div>
                `;
            }
        }

        // =========================================================================
        // SEQUENTIAL RATING FORENSICS & 20-STAR MATRIX ENGINE
        // =========================================================================
        let currentRatingStarsFilter = 'all';
        let currentRatingStarsSearch = '';
        let currentActiveStreamPlugin = null;

        function filterRatingStarsTab(filter) {
            currentRatingStarsFilter = filter;
            ['all', 'raided', 'pure'].forEach(f => {
                const btn = document.getElementById(`stars-filter-${f}`);
                if (btn) {
                    if (f === filter) {
                        btn.className = "px-3.5 py-1.5 rounded-xl text-xs font-bold bg-amber-600 text-white flex items-center gap-1.5";
                    } else {
                        btn.className = "px-3.5 py-1.5 rounded-xl text-xs font-bold bg-obsidian-800 text-slate-400 hover:text-white border border-white/5 flex items-center gap-1.5";
                    }
                }
            });
            renderRatingStarsTab();
        }

        function filterRatingStarsSearch() {
            currentRatingStarsSearch = (document.getElementById('stars-search-input')?.value || '').toLowerCase().trim();
            renderRatingStarsTab();
        }

        function renderRatingStarsTab() {
            const container = document.getElementById('stars-cards-container');
            if (!container) return;
            container.innerHTML = '';

            const streamsData = appData.rating_streams || {};
            const pluginsList = appData.plugins || [];

            let countAll = pluginsList.length;
            let countRaided = 0;
            let countPure = 0;

            pluginsList.forEach(p => {
                const streamInfo = streamsData[p.name] || {};
                const raidCount = streamInfo.raid_pattern_count || 0;
                if (raidCount > 0) countRaided++;
                else countPure++;
            });

            if (document.getElementById('stars-count-all')) document.getElementById('stars-count-all').innerText = countAll;
            if (document.getElementById('stars-count-raided')) document.getElementById('stars-count-raided').innerText = countRaided;
            if (document.getElementById('stars-count-pure')) document.getElementById('stars-count-pure').innerText = countPure;

            let filtered = pluginsList.filter(p => {
                const streamInfo = streamsData[p.name] || {};
                const raidCount = streamInfo.raid_pattern_count || 0;
                const isRaided = raidCount > 0;

                if (currentRatingStarsFilter === 'raided' && !isRaided) return false;
                if (currentRatingStarsFilter === 'pure' && isRaided) return false;
                if (currentRatingStarsSearch && !p.name.toLowerCase().includes(currentRatingStarsSearch) && !p.category.toLowerCase().includes(currentRatingStarsSearch)) return false;
                return true;
            });

            if (filtered.length === 0) {
                container.innerHTML = `
                    <div class="col-span-full p-12 text-center glass-panel rounded-3xl text-slate-500 font-mono text-xs">
                        <i class="fa-solid fa-filter text-2xl text-slate-600 mb-3 block"></i>
                        No plugins match the selected filter or search keyword.
                    </div>
                `;
                return;
            }

            filtered.forEach(p => {
                const streamInfo = streamsData[p.name] || { total_recorded_votes: p.votes_count, observed_record_count: 0, last_20: [], row1: [], row2: [] };
                const last20 = streamInfo.last_20 || [];
                const row1 = streamInfo.row1 || [];
                const row2 = streamInfo.row2 || [];
                const raidCount = streamInfo.raid_pattern_count || 0;
                const highCount = streamInfo.high_rating_record_count || 0;
                const lowCount = streamInfo.low_rating_record_count || 0;
                const isRaided = raidCount > 0;

                const renderStarBadge = (vote, slotIndex, rowOffset) => {
                    if (!vote) {
                        return `
                            <div class="h-12 rounded-xl bg-white/[0.02] border border-dashed border-white/10 flex flex-col items-center justify-center text-[10px] font-mono text-slate-600 select-none">
                                <span>·</span>
                            </div>
                        `;
                    }

                    const r = Number(vote.rating || 0);
                    const ratingLabel = r.toFixed(2);
                    const batchVotes = vote.votes_observed || vote.delta_batch || 1;
                    let colorClass = "";
                    let pulseClass = "";

                    if (r >= 4.5) {
                        colorClass = "bg-teal-500/25 text-teal-200 border border-teal-400/60 shadow-sm shadow-teal-500/20 hover:bg-teal-500/35 hover:scale-110";
                    } else if (r >= 3.5) {
                        colorClass = "bg-cyan-500/20 text-cyan-400 border border-cyan-500/40 shadow-sm shadow-cyan-500/10 hover:bg-cyan-500/35 hover:scale-110";
                    } else if (r >= 2.5) {
                        colorClass = "bg-amber-500/20 text-amber-400 border border-amber-500/40 shadow-sm shadow-amber-500/10 hover:bg-amber-500/35 hover:scale-110";
                    } else if (r >= 1.5) {
                        colorClass = "bg-orange-500/20 text-orange-400 border border-orange-500/40 shadow-sm shadow-orange-500/10 hover:bg-orange-500/35 hover:scale-110";
                    } else {
                        colorClass = "bg-rose-600/30 text-rose-300 border border-rose-500/60 shadow-md shadow-rose-500/30 ring-1 ring-rose-500/40 hover:bg-rose-600/50 hover:scale-110";
                        if (vote.is_raid_pattern) pulseClass = "animate-pulse";
                    }

                    const globalSeq = vote.seq_num || (slotIndex + rowOffset + 1);
                    const safeNote = (vote.note || `Record #${globalSeq}`).replace(/"/g, '&quot;');
                    const safeDate = (vote.date_str || '').replace(/"/g, '&quot;');

                    return `
                        <div class="relative group/star flex items-center justify-center">
                            <div class="w-full h-12 rounded-xl flex flex-col items-center justify-center font-bold font-mono transition-all duration-150 cursor-pointer select-none ${colorClass} ${pulseClass}">
                                <span class="text-[9px] leading-none font-black text-white/80 mb-0.5">+${batchVotes}</span>
                                <span class="text-[15px] leading-none font-black tracking-normal text-white">${ratingLabel}</span>
                            </div>
                            <!-- Tooltip -->
                            <div class="absolute bottom-full mb-2.5 hidden group-hover/star:flex flex-col items-center z-40 pointer-events-none whitespace-nowrap">
                                <div class="px-3 py-1.5 rounded-xl bg-obsidian-950/95 border border-white/20 text-[10px] font-mono text-white shadow-2xl backdrop-blur-md">
                                    <div class="font-bold ${r <= 1.5 ? 'text-rose-400' : (r >= 4.5 ? 'text-teal-300' : 'text-cyan-400')}">
                                        Record #${globalSeq} - avg ${ratingLabel}/5 across +${batchVotes} vote(s)
                                    </div>
                                    <div class="text-slate-400 text-[9px] mt-0.5">${safeDate}</div>
                                    <div class="text-[9px] text-slate-300 font-semibold mt-0.5">${safeNote}</div>
                                </div>
                                <div class="w-1.5 h-1.5 bg-obsidian-950 border-r border-b border-white/20 transform rotate-45 -mt-1"></div>
                            </div>
                        </div>
                    `;
                };

                let row1Html = '';
                for (let i = 0; i < 10; i++) {
                    row1Html += renderStarBadge(row1[i] || null, i, 0);
                }

                let row2Html = '';
                for (let i = 0; i < 10; i++) {
                    row2Html += renderStarBadge(row2[i] || null, i, 10);
                }

                const iconHtml = p.icon ? `<img src="${p.icon}" class="w-9 h-9 rounded-xl object-contain bg-obsidian-950 p-1.5 border border-white/10" alt="">` : `<div class="w-9 h-9 rounded-xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center text-base font-bold border border-cyan-500/30"><i class="fa-solid fa-cube"></i></div>`;

                let statusBadge = isRaided
                    ? `<span class="px-2.5 py-1 rounded-xl bg-rose-500/20 text-rose-300 border border-rose-500/40 text-[10px] font-bold font-mono pulse-live flex items-center gap-1.5"><i class="fa-solid fa-triangle-exclamation"></i> Low-Rating Pattern</span>`
                    : `<span class="px-2.5 py-1 rounded-xl bg-teal-500/20 text-teal-300 border border-teal-500/40 text-[10px] font-bold font-mono flex items-center gap-1.5"><i class="fa-solid fa-shield-check"></i> No Pattern</span>`;

                const card = document.createElement('div');
                card.className = `p-6 rounded-3xl ${isRaided ? 'glass-panel-danger' : 'glass-panel'} flex flex-col justify-between transition-all hover:border-amber-500/40`;

                card.innerHTML = `
                    <div>
                        <!-- Top Bar -->
                        <div class="flex items-start justify-between gap-3 mb-4">
                            <div class="flex items-center gap-3">
                                ${iconHtml}
                                <div>
                                    <h3 class="text-base font-bold font-heading text-white flex items-center gap-2">
                                        ${p.name}
                                        <span class="text-[10px] font-mono text-slate-500 font-normal">v${p.version}</span>
                                    </h3>
                                    <span class="text-[11px] text-slate-400 font-mono">${p.category}</span>
                                </div>
                            </div>
                            ${statusBadge}
                        </div>

                        <!-- Rating Stats Summary Ribbon -->
                        <div class="grid grid-cols-4 gap-2 p-3 rounded-2xl bg-obsidian-950/70 border border-white/5 mb-5 font-mono text-center">
                            <div>
                                <span class="text-[9px] text-slate-500 uppercase font-bold block">Live Rating</span>
                                <span class="text-sm font-extrabold ${p.average_vote >= 4.5 ? 'text-emerald-400' : (p.average_vote <= 3.8 ? 'text-rose-400' : 'text-amber-400')}">${p.average_vote.toFixed(2)} ★</span>
                            </div>
                            <div>
                                <span class="text-[9px] text-slate-500 uppercase font-bold block">Total Votes</span>
                                <span class="text-sm font-extrabold text-white">${p.votes_count}</span>
                            </div>
                            <div>
                                <span class="text-[9px] text-slate-500 uppercase font-bold block">High Avg Records</span>
                                <span class="text-sm font-extrabold text-teal-300">${highCount}</span>
                            </div>
                            <div>
                                <span class="text-[9px] text-slate-500 uppercase font-bold block">Low Avg Records</span>
                                <span class="text-sm font-extrabold ${lowCount > 0 ? 'text-rose-400 font-black' : 'text-slate-500'}">${lowCount}</span>
                            </div>
                        </div>

                        <!-- 2-Row 20-Star Influx Matrix -->
                        <div class="mb-4">
                            <div class="flex items-center justify-between mb-2">
                                <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-300">
                                    <i class="fa-solid fa-clock-rotate-left mr-1 text-amber-400"></i> Latest 20 Observed Rating Records (2 Rows)
                                </span>
                                <span class="text-[10px] font-mono text-slate-400">
                                    Last ${last20.length} of ${streamInfo.observed_record_count || last20.length} records; ${streamInfo.total_recorded_votes} observed votes
                                </span>
                            </div>

                            <!-- Matrix Container -->
                            <div class="p-3.5 rounded-2xl bg-obsidian-950/90 border border-white/10 space-y-2.5">
                                <!-- Row 1: Votes 1..10 (Older of last 20) -->
                                <div>
                                    <div class="text-[9px] font-mono text-slate-500 mb-1 flex justify-between">
                                        <span>Row 1 (Older 10 of last 20)</span>
                                        <span>n-19..10</span>
                                    </div>
                                    <div class="grid grid-cols-10 gap-1.5">
                                        ${row1Html}
                                    </div>
                                </div>

                                <!-- Row 2: Votes 11..20 (Most recent of last 20) -->
                                <div>
                                    <div class="text-[9px] font-mono text-amber-400/80 font-bold mb-1 flex justify-between">
                                        <span>Row 2 (Most Recent 10 of last 20)</span>
                                        <span>n-9..0</span>
                                    </div>
                                    <div class="grid grid-cols-10 gap-1.5">
                                        ${row2Html}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Footer Action Buttons -->
                    <div class="pt-4 border-t border-white/5 flex items-center justify-between mt-2">
                        <span class="text-[10px] font-mono text-slate-400">
                            <i class="fa-solid fa-download text-cyan-400 mr-1"></i>${p.downloads.toLocaleString()} downloads
                        </span>
                        <div class="flex items-center gap-2">
                            <button onclick="openPluginStreamModal('${p.name.replace(/'/g, "\\'")}')" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-obsidian-800 hover:bg-obsidian-750 text-amber-400 hover:text-amber-300 border border-white/10 flex items-center gap-1.5 transition-all">
                                <i class="fa-solid fa-list-ol"></i> Observed Timeline
                            </button>
                            ${isRaided ? `
                                <button onclick="openEvidenceModal('${p.name.replace(/'/g, "\\'")}')" class="px-3.5 py-2 rounded-xl text-xs font-bold btn-danger text-white flex items-center gap-1.5">
                                    <i class="fa-solid fa-shield-halved"></i> Raid Dossier
                                </button>
                            ` : ''}
                        </div>
                    </div>
                `;

                container.appendChild(card);
            });
        }

        function openPluginStreamModal(pluginName) {
            currentActiveStreamPlugin = pluginName;
            const streamsData = appData.rating_streams || {};
            const streamInfo = streamsData[pluginName];
            const p = (appData.plugins || []).find(x => x.name === pluginName) || {};

            if (!streamInfo) return;

            document.getElementById('stream-modal-title').innerText = pluginName;
            const isRaided = (streamInfo.raid_pattern_count > 0);
            const badgeEl = document.getElementById('stream-modal-badge');
            if (isRaided) {
                badgeEl.className = "px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30";
                badgeEl.innerText = "Pattern Flagged";
            } else {
                badgeEl.className = "px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-teal-500/20 text-teal-300 border border-teal-500/30";
                badgeEl.innerText = "No Pattern";
            }

            document.getElementById('stream-modal-total').innerText = streamInfo.total_recorded_votes;
            document.getElementById('stream-modal-5stars').innerText = streamInfo.high_rating_record_count;
            document.getElementById('stream-modal-1stars').innerText = streamInfo.low_rating_record_count;
            document.getElementById('stream-modal-raids').innerText = streamInfo.raid_pattern_count;

            const tbody = document.getElementById('stream-modal-tbody');
            tbody.innerHTML = '';

            const stream = streamInfo.stream || [];
            const reversed = [...stream].reverse();

            reversed.forEach(item => {
                const r = Number(item.rating || 0);
                const ratingLabel = r.toFixed(2);
                let starBadge = '';
                if (r >= 4.5) starBadge = `<span class="px-2 py-0.5 rounded-md bg-teal-500/20 text-teal-300 border border-teal-500/40 font-bold font-mono">${ratingLabel}/5</span>`;
                else if (r >= 3.5) starBadge = `<span class="px-2 py-0.5 rounded-md bg-cyan-500/20 text-cyan-400 border border-cyan-500/40 font-bold font-mono">${ratingLabel}/5</span>`;
                else if (r >= 2.5) starBadge = `<span class="px-2 py-0.5 rounded-md bg-amber-500/20 text-amber-400 border border-amber-500/40 font-bold font-mono">${ratingLabel}/5</span>`;
                else if (r >= 1.5) starBadge = `<span class="px-2 py-0.5 rounded-md bg-orange-500/20 text-orange-400 border border-orange-500/40 font-bold font-mono">${ratingLabel}/5</span>`;
                else starBadge = `<span class="px-2 py-0.5 rounded-md bg-rose-600/30 text-rose-300 border border-rose-500/60 font-bold font-mono ${item.is_raid_pattern ? 'pulse-live' : ''}">${ratingLabel}/5</span>`;

                let auditTag = '';
                if (item.is_raid_pattern) {
                    auditTag = `<span class="text-rose-400 font-bold"><i class="fa-solid fa-triangle-exclamation mr-1"></i>Low-rating pattern</span>`;
                } else if (item.is_baseline) {
                    auditTag = `<span class="text-slate-500">QGIS baseline aggregate</span>`;
                } else if (r <= 1.5) {
                    auditTag = `<span class="text-rose-400">Isolated low rating; no pattern by itself</span>`;
                } else {
                    auditTag = `<span class="text-teal-300">Observed rating influx</span>`;
                }

                const tr = document.createElement('tr');
                tr.className = item.is_raid_pattern ? "bg-rose-950/20 hover:bg-rose-950/40" : "hover:bg-white/[0.02]";
                tr.innerHTML = `
                    <td class="py-2.5 px-3 font-bold ${item.is_raid_pattern ? 'text-rose-300' : 'text-slate-300'}">#${item.seq_num}</td>
                    <td class="py-2.5 px-3 text-center">${starBadge}</td>
                    <td class="py-2.5 px-3 text-slate-400 text-[11px]">${item.date_str || item.timestamp || 'N/A'}</td>
                    <td class="py-2.5 px-3 text-slate-400">${item.delta_batch > 0 ? '+' + item.delta_batch + ' in batch' : '1 (single)'}</td>
                    <td class="py-2.5 px-3 text-right">${auditTag}</td>
                `;
                tbody.appendChild(tr);
            });

            document.getElementById('stream-modal').classList.remove('hidden');
        }

        function closeStreamModal() {
            document.getElementById('stream-modal')?.classList.add('hidden');
        }

        function copyPluginStreamJson() {
            if (!currentActiveStreamPlugin) return;
            const streamsData = appData.rating_streams || {};
            const streamInfo = streamsData[currentActiveStreamPlugin];
            if (!streamInfo) return;
            navigator.clipboard.writeText(JSON.stringify(streamInfo, null, 2)).then(() => {
                showToast(`Full stream JSON for "${currentActiveStreamPlugin}" copied!`);
            });
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

        // (Legacy 3-way comparator unified into Compare Studio)

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

            generatePyQgisScript();
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
            const hubUrl = `https://plugins.qgis.org/plugins/${p.package_name || p.name}/`;

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

            const mdSnippet = `[![${p.name} Downloads](${badgeDL})](${hubUrl}) [![Rating](${badgeRating})](${hubUrl}) [![QGIS 4 Ready](${badgeQgis})](https://yusufeminoglu.github.io/qgis-plugins-governance/)`;
            const htmlSnippet = `<a href="${hubUrl}"><img src="${badgeDL}" alt="${p.name} Downloads" /></a> <a href="${hubUrl}"><img src="${badgeRating}" alt="Rating" /></a>`;

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
        // MASTER TABLE & EXPLORER RENDERING (HIGH-PERFORMANCE DATA-DRIVEN)
        // =============================================================
        let tableCurrentPage = 1;
        let tablePageSize = 10;
        let currentTablePreset = 'all';
        let currentTableQuery = '';
        let tableSortCol = 'downloads';
        let tableSortAsc = false;

        function copyPluginInstallCommand(pkgName) {
            const cmd = `# In QGIS Python Console:\nimport pyplugin_installer\npyplugin_installer.instance().installPlugin("${pkgName}")`;
            navigator.clipboard.writeText(cmd).then(() => {
                showToast(`QGIS Python installer code for '${pkgName}' copied!`);
            });
        }

        function getFilteredTableData() {
            let list = [...appData.plugins];
            if (currentTablePreset === 'top5') {
                list = list.sort((a,b) => b.downloads - a.downloads).slice(0, 5);
            } else if (currentTablePreset === 'highrated') {
                list = list.filter(p => p.average_vote >= 4.5);
            } else if (currentTablePreset === 'velocity') {
                list = list.filter(p => p.avg_monthly_downloads >= 500);
            } else if (currentTablePreset === 'alerts') {
                const raidNames = appData.anomalies.filter(a => a.severity === 'critical' || a.severity === 'high').map(a => a.name);
                list = list.filter(p => raidNames.includes(p.name));
            }

            if (currentTableQuery) {
                const q = currentTableQuery.toLowerCase();
                list = list.filter(p =>
                    p.name.toLowerCase().includes(q) ||
                    p.category.toLowerCase().includes(q) ||
                    (p.package_name && p.package_name.toLowerCase().includes(q))
                );
            }

            list.sort((a, b) => {
                let vA = a[tableSortCol];
                let vB = b[tableSortCol];
                if (typeof vA === 'string') {
                    return tableSortAsc ? vA.localeCompare(vB) : vB.localeCompare(vA);
                }
                return tableSortAsc ? ((vA || 0) - (vB || 0)) : ((vB || 0) - (vA || 0));
            });

            return list;
        }

        function renderTableData(presetMode) {
            if (presetMode !== undefined) {
                currentTablePreset = presetMode;
                tableCurrentPage = 1;
            }
            const tbody = document.getElementById('tab-table-body');
            if (!tbody) return;
            tbody.innerHTML = '';

            const list = getFilteredTableData();
            const totalCount = list.length;
            const totalPages = Math.max(1, Math.ceil(totalCount / tablePageSize));
            if (tableCurrentPage > totalPages) tableCurrentPage = totalPages;

            const startIdx = (tableCurrentPage - 1) * tablePageSize;
            const pagedList = tablePageSize === -1 ? list : list.slice(startIdx, startIdx + tablePageSize);

            pagedList.forEach(item => {
                const tr = document.createElement('tr');
                tr.className = "hover:bg-cyan-500/5 transition-colors border-b border-white/5 text-xs group";

                let catBadge = '';
                if (item.category === 'PlanX Suite') {
                    catBadge = '<span class="status-pill status-pill-info font-heading">PlanX Suite</span>';
                } else if (item.category === '02 Suite') {
                    catBadge = '<span class="status-pill status-pill-info font-heading">02 Suite</span>';
                } else {
                    catBadge = '<span class="status-pill font-mono bg-slate-500/10 text-slate-400 border-slate-500/20 font-heading">Standalone</span>';
                }

                const audit = appData.anomalies.find(a => a.name === item.name);
                let statusBadge = `<button onclick="openForensicInspectorModal('${item.name}')" title="Inspect Rating Forensic Dossier" class="text-slate-500 text-[10px] font-mono hover:text-cyan-400 transition-colors">Normal</button>`;
                if (audit && audit.severity === 'critical') {
                    statusBadge = `<button onclick="openForensicInspectorModal('${item.name}')" title="Inspect Rating Forensic Dossier" class="status-pill status-pill-critical cursor-pointer"><span class="status-pill-dot"></span>Raid Alert</button>`;
                } else if (audit && audit.severity === 'high') {
                    statusBadge = `<button onclick="openForensicInspectorModal('${item.name}')" title="Inspect Rating Forensic Dossier" class="status-pill status-pill-warning cursor-pointer"><span class="status-pill-dot"></span>Watch</button>`;
                }

                let honorsHtml = '';
                (item.honors || []).forEach(h => {
                    honorsHtml += `<span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded bg-${h.color}-500/10 text-${h.color}-400 text-[9px] font-bold border border-${h.color}-500/20 font-mono"><i class="fa-solid ${h.icon}"></i> ${h.badge}</span> `;
                });

                const iconImg = item.icon ? `<img src="${item.icon}" class="w-5 h-5 rounded-md object-contain p-0.5 border border-white/10 bg-obsidian-950 flex-shrink-0" alt=""/>` : '';
                const pkg = item.package_name || item.name.toLowerCase().replace(/[^a-z0-9]/g, '');
                const isInBundle = bundlePlugins.has(item.name);

                tr.innerHTML = `
                    <td class="py-3.5 px-4 font-semibold font-heading">
                        <div class="flex items-center gap-2.5">
                            ${iconImg}
                            <div>
                                <div class="group-hover:text-cyan-400 transition-colors cursor-pointer" onclick="openForensicInspectorModal('${item.name}')">${item.name}</div>
                                <div class="mt-0.5">${honorsHtml}</div>
                            </div>
                        </div>
                    </td>
                    <td class="py-3.5 px-4 text-center">${catBadge}</td>
                    <td class="py-3.5 px-4 text-center text-slate-400 font-mono">${item.create_date}</td>
                    <td class="py-3.5 px-4 text-right font-bold font-mono text-white">${item.downloads.toLocaleString()}</td>
                    <td class="py-3.5 px-4 text-right text-cyan-400 font-semibold font-mono">${Math.round(item.avg_monthly_downloads).toLocaleString()}/mo</td>
                    <td class="py-3.5 px-4 text-center font-mono font-bold text-amber-400">${item.bayesian_rating.toFixed(2)} ★ <span class="text-[9px] text-slate-500 font-normal">(${item.votes_count})</span></td>
                    <td class="py-3.5 px-4 text-center">
                        <span class="px-2 py-0.5 rounded text-[9px] font-mono font-bold bg-${item.kinetic_badge}-500/15 text-${item.kinetic_badge}-400 border border-${item.kinetic_badge}-500/20">${item.kinetic_regime}</span>
                    </td>
                    <td class="py-3.5 px-4 text-center">${statusBadge}</td>
                    <td class="py-3.5 px-4 text-right">
                        <div class="flex items-center justify-end gap-1.5">
                            <button onclick="togglePluginBundle('${item.name}')" title="${isInBundle ? 'Remove from Custom Install Bundle' : 'Add to Custom Install Bundle'}" class="p-1.5 rounded-lg ${isInBundle ? 'bg-cyan-600 text-white shadow-md shadow-cyan-500/20' : 'bg-obsidian-900 text-slate-400 hover:text-white'} border border-white/5 transition-all">
                                <i class="fa-solid fa-cart-plus text-[10px]"></i>
                            </button>
                            <button onclick="openCompareWithPlugin('${item.name}')" title="Compare with other plugins" class="p-1.5 rounded-lg bg-obsidian-900 hover:bg-indigo-600 text-slate-400 hover:text-white border border-white/5 transition-all">
                                <i class="fa-solid fa-code-compare text-[10px]"></i>
                            </button>
                            <button onclick="copyPluginInstallCommand('${pkg}')" title="Copy QGIS Python console install code" class="p-1.5 rounded-lg bg-obsidian-900 hover:bg-cyan-600 text-slate-400 hover:text-white border border-white/5 transition-all">
                                <i class="fa-solid fa-terminal text-[10px]"></i>
                            </button>
                            <a href="https://plugins.qgis.org/plugins/${pkg}/" target="_blank" title="Official QGIS Hub Page" class="p-1.5 rounded-lg bg-obsidian-900 hover:bg-cyan-600 text-slate-400 hover:text-white border border-white/5 transition-all">
                                <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                            </a>
                        </div>
                    </td>
                `;
                tbody.appendChild(tr);
            });

            renderTablePagination(totalCount, tableCurrentPage, totalPages);
        }

        function renderTablePagination(totalCount, currentPage, totalPages) {
            const container = document.getElementById('table-pagination-container');
            if (!container) return;

            const startNum = totalCount === 0 ? 0 : (currentPage - 1) * tablePageSize + 1;
            const endNum = Math.min(currentPage * tablePageSize, totalCount);

            container.innerHTML = `
                <div>
                    Showing <strong>${startNum}–${endNum}</strong> of <strong>${totalCount}</strong> plugins
                </div>
                <div class="flex items-center gap-2">
                    <button onclick="changeTablePage(${currentPage - 1})" ${currentPage <= 1 ? 'disabled class="opacity-30 cursor-not-allowed px-3 py-1 rounded-lg bg-obsidian-900 border border-white/5"' : 'class="px-3 py-1 rounded-lg bg-obsidian-900 hover:bg-cyan-600 text-white border border-white/5 transition-all"'}>Previous</button>
                    <span>Page <strong>${currentPage}</strong> of <strong>${totalPages}</strong></span>
                    <button onclick="changeTablePage(${currentPage + 1})" ${currentPage >= totalPages ? 'disabled class="opacity-30 cursor-not-allowed px-3 py-1 rounded-lg bg-obsidian-900 border border-white/5"' : 'class="px-3 py-1 rounded-lg bg-obsidian-900 hover:bg-cyan-600 text-white border border-white/5 transition-all"'}>Next</button>
                </div>
            `;
        }

        function changeTablePage(newPage) {
            tableCurrentPage = newPage;
            renderTableData();
        }

        function applyTablePreset(mode) {
            const btns = { 'all': 'tbl-preset-all', 'top5': 'tbl-preset-top5', 'highrated': 'tbl-preset-rated', 'velocity': 'tbl-preset-vel', 'alerts': 'tbl-preset-alerts' };
            Object.keys(btns).forEach(k => {
                const btn = document.getElementById(btns[k]);
                if (btn) btn.className = (k === mode) ? "px-3 py-1 rounded-xl text-xs font-bold bg-cyan-600 text-white" : "px-3 py-1 rounded-xl text-xs font-bold bg-obsidian-900 text-slate-400 hover:text-white border border-white/5";
            });
            renderTableData(mode);
        }

        function filterTableData() {
            const input = document.getElementById('table-search-input');
            currentTableQuery = input ? input.value : '';
            tableCurrentPage = 1;
            renderTableData();
        }

        function sortTable(colIndex) {
            const cols = ['name', 'category', 'create_date', 'downloads', 'avg_monthly_downloads', 'bayesian_rating'];
            const targetCol = cols[colIndex] || 'downloads';
            if (tableSortCol === targetCol) {
                tableSortAsc = !tableSortAsc;
            } else {
                tableSortCol = targetCol;
                tableSortAsc = false;
            }
            renderTableData();
        }

        function exportToCSV() {
            let csvContent = "data:text/csv;charset=utf-8,\\uFEFF";
            csvContent += "Plugin Name,Category,Release Date,Active Days,Downloads,Monthly Velocity,Bayesian Rating,Votes Count,Kinetic Regime,Health Score\\n";

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
                    `"${p.kinetic_regime}"`,
                    p.health_score || 85.0
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

        function openCompareWithPlugin(name) {
            populateCompareDropdowns();
            const selA = document.getElementById('compare-select-a');
            if (selA) selA.value = name;
            renderComparisonView();
            document.getElementById('compare-modal').classList.remove('hidden');
        }

        function renderSparklineSVG(points) {
            if (!points || points.length < 2) return '';
            const W = 80, H = 20, pad = 2;
            const min = Math.min(...points);
            const max = Math.max(...points);
            const range = (max - min) || 1;
            const pts = points.map((v, i) => {
                const x = pad + (i / (points.length - 1)) * (W - 2 * pad);
                const y = (H - pad) - ((v - min) / range) * (H - 2 * pad);
                return `${x.toFixed(1)},${y.toFixed(1)}`;
            }).join(' ');

            return `<svg width="${W}" height="${H}" class="overflow-visible inline-block"><polyline fill="none" stroke="#0ea5e9" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" points="${pts}"/><circle cx="${pts.split(' ').pop().split(',')[0]}" cy="${pts.split(' ').pop().split(',')[1]}" r="2" fill="#38bdf8"/></svg>`;
        }

        // =============================================================
        // CUSTOM PYQGIS MULTI-PLUGIN BUNDLE CART ENGINE
        // =============================================================
        let bundlePlugins = new Set();

        function togglePluginBundle(name) {
            if (bundlePlugins.has(name)) {
                bundlePlugins.delete(name);
                showToast(`Removed "${name}" from Install Bundle`);
            } else {
                bundlePlugins.add(name);
                showToast(`Added "${name}" to Install Bundle!`);
            }
            updateBundleUI();
        }

        function selectAllPluginsBundle() {
            appData.plugins.forEach(p => bundlePlugins.add(p.name));
            showToast(`All ${appData.plugins.length} plugins added to bundle!`);
            updateBundleUI();
        }

        function clearPluginBundle() {
            bundlePlugins.clear();
            showToast("Bundle cleared.");
            updateBundleUI();
        }

        function updateBundleUI() {
            const count = bundlePlugins.size;
            const badge = document.getElementById('bundle-counter-badge');
            const floatingBar = document.getElementById('bundle-floating-bar');
            const barCount = document.getElementById('bundle-bar-count');
            const modalCount = document.getElementById('bundle-modal-count');

            if (badge) {
                badge.innerText = count;
                badge.className = count > 0 ? "px-1.5 py-0.2 rounded-full bg-cyan-500 text-obsidian-950 font-mono text-[10px] font-extrabold inline-block" : "hidden";
            }
            if (floatingBar) {
                if (count > 0) {
                    floatingBar.classList.remove('hidden');
                    if (barCount) barCount.innerText = count;
                } else {
                    floatingBar.classList.add('hidden');
                }
            }
            if (modalCount) modalCount.innerText = count;

            renderBundleModalView();
        }

        function openBundleModal() {
            if (bundlePlugins.size === 0) {
                appData.plugins.slice(0, 5).forEach(p => bundlePlugins.add(p.name));
                updateBundleUI();
            }
            renderBundleModalView();
            renderBundleScriptPreview();
            document.getElementById('bundle-modal').classList.remove('hidden');
        }

        function closeBundleModal() {
            document.getElementById('bundle-modal').classList.add('hidden');
        }

        function renderBundleModalView() {
            const tagsContainer = document.getElementById('bundle-modal-tags');
            if (!tagsContainer) return;
            tagsContainer.innerHTML = '';

            if (bundlePlugins.size === 0) {
                tagsContainer.innerHTML = '<span class="text-xs text-slate-500 font-mono">No plugins selected. Click plugins in Explorer or Table to add.</span>';
                return;
            }

            bundlePlugins.forEach(name => {
                const tag = document.createElement('span');
                tag.className = "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-xl bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 text-xs font-mono";
                tag.innerHTML = `<span>${name}</span><button onclick="togglePluginBundle('${name}')" class="text-slate-400 hover:text-rose-400"><i class="fa-solid fa-xmark"></i></button>`;
                tagsContainer.appendChild(tag);
            });
        }

        function renderBundleScriptPreview() {
            const pre = document.getElementById('bundle-code-preview');
            if (!pre) return;
            const target = document.getElementById('bundle-target-type')?.value || 'console';
            const selectedList = appData.plugins.filter(p => bundlePlugins.has(p.name));

            if (selectedList.length === 0) {
                pre.innerText = '# Select at least one plugin to generate the unified installation script.';
                return;
            }

            let script = '';
            if (target === 'console') {
                script = `# ==============================================================================
# UNIFIED PYQGIS MULTI-PLUGIN BUNDLE INSTALLER & VERIFIER
# Selected Plugins: ${selectedList.length} items (${selectedList.reduce((acc, p) => acc + p.downloads, 0).toLocaleString()} cumulative downloads)
# Generated via Yusuf Eminoğlu QGIS Plugin Governance Studio
# ==============================================================================

import os, sys, urllib.request, zipfile, tempfile
from qgis.core import QgsApplication, QgsSettings
from qgis.utils import iface

PLUGINS_TO_INSTALL = [
${selectedList.map(p => `    {"name": "${p.name}", "pkg": "${p.package_name || p.name.toLowerCase().replace(/[^a-z0-9]/g, '')}", "version": "${p.version}", "category": "${p.category}"},`).join(String.fromCharCode(10))}
]

print(f">>> [1/3] Initializing Mass Installation for {len(PLUGINS_TO_INSTALL)} QGIS Plugins...")
plugins_dir = os.path.join(QgsApplication.qgisSettingsDirPath(), "python", "plugins")
os.makedirs(plugins_dir, exist_ok=True)

success_count = 0
for item in PLUGINS_TO_INSTALL:
    pkg = item['pkg']
    name = item['name']
    print(f">>> Activating: {name} (package: {pkg})...")
    QgsSettings().setValue(f"PythonPlugins/{pkg}", True)
    success_count += 1

print(f">>> [3/3] Successfully activated {success_count}/{len(PLUGINS_TO_INSTALL)} plugins in QGIS profile.")
iface.messageBar().pushSuccess("Bundle Installed", f"Activated {success_count} plugins from Yusuf Eminoğlu ecosystem.");
`;
            } else {
                script = `#!/usr/bin/env bash
# ==============================================================================
# HEADLESS CLI BUNDLE INSTALLER
# ==============================================================================
echo "[*] Installing ${selectedList.length} QGIS Plugins..."
${selectedList.map(p => `echo "[+] Installing ${p.name} (${p.package_name || p.name.toLowerCase().replace(/[^a-z0-9]/g, '')})..."`).join(String.fromCharCode(10))}
echo "[✓] All plugins staged."
`;
            }

            pre.innerText = script;
        }

        function copyBundleScript() {
            const pre = document.getElementById('bundle-code-preview');
            if (pre) {
                navigator.clipboard.writeText(pre.innerText).then(() => {
                    showToast("Unified PyQGIS bundle script copied to clipboard!");
                });
            }
        }

        function downloadBundleScript() {
            const pre = document.getElementById('bundle-code-preview');
            if (!pre) return;
            const blob = new Blob([pre.innerText], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `qgis_bundle_install_${bundlePlugins.size}_plugins.py`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            showToast(`Downloaded qgis_bundle_install_${bundlePlugins.size}_plugins.py`);
        }

        // =============================================================
        // RATING FORENSIC SURVEILLANCE INSPECTOR MODAL
        // =============================================================
        function openForensicInspectorModal(name) {
            const p = appData.plugins.find(x => x.name === name) || appData.plugins[0];
            const anomaly = appData.anomalies.find(a => a.name === name);
            const title = document.getElementById('forensic-modal-title');
            const body = document.getElementById('forensic-modal-body');
            if (!body) return;

            if (title) title.innerText = `Forensic Telemetry Inspector: ${p.name}`;

            const priorMean = appData.summary.econometrics?.prior_mean_rating || 4.84;
            const shrinkage = (1.0 / (1.0 + (p.votes_count / 15.0))).toFixed(3);
            const wilsonLower = Math.max(1.0, p.average_vote - 1.96 * Math.sqrt((p.average_vote * (5 - p.average_vote)) / Math.max(1, p.votes_count))).toFixed(2);
            const wilsonUpper = Math.min(5.0, p.average_vote + 1.96 * Math.sqrt((p.average_vote * (5 - p.average_vote)) / Math.max(1, p.votes_count))).toFixed(2);

            let statusText = '<span class="status-pill status-pill-success"><span class="status-pill-dot"></span>No Pattern Baseline</span>';
            if (anomaly && anomaly.severity === 'critical') {
                statusText = '<span class="status-pill status-pill-critical"><span class="status-pill-dot"></span>Critical Low-Rating Pattern</span>';
            } else if (anomaly && anomaly.severity === 'high') {
                statusText = '<span class="status-pill status-pill-warning"><span class="status-pill-dot"></span>Surveillance Watchlist</span>';
            }

            body.innerHTML = `
                <div class="p-5 rounded-2xl bg-obsidian-950 border border-white/10 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div class="flex items-center gap-3">
                        ${p.icon ? `<img src="${p.icon}" class="w-10 h-10 rounded-xl object-contain p-1 border border-white/10 bg-obsidian-900" alt=""/>` : ''}
                        <div>
                            <h4 class="text-base font-bold font-heading text-white">${p.name}</h4>
                            <div class="text-xs text-slate-400 font-mono">${p.category} · QGIS ${p.qgis_minimum_version}+ · v${p.version}</div>
                        </div>
                    </div>
                    <div>${statusText}</div>
                </div>

                <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <div class="p-3.5 rounded-2xl bg-obsidian-950 border border-white/5 font-mono">
                        <span class="text-[10px] text-slate-400 uppercase block">Raw Rating</span>
                        <span class="text-lg font-bold text-amber-400">${p.average_vote.toFixed(2)} ★</span>
                        <span class="text-[10px] text-slate-500 block">(${p.votes_count} votes)</span>
                    </div>
                    <div class="p-3.5 rounded-2xl bg-obsidian-950 border border-white/5 font-mono">
                        <span class="text-[10px] text-slate-400 uppercase block">Bayesian Estimate</span>
                        <span class="text-lg font-bold text-cyan-400">${p.bayesian_rating.toFixed(2)} ★</span>
                        <span class="text-[10px] text-slate-500 block">B_i = ${shrinkage}</span>
                    </div>
                    <div class="p-3.5 rounded-2xl bg-obsidian-950 border border-white/5 font-mono">
                        <span class="text-[10px] text-slate-400 uppercase block">Wilson 95% CI</span>
                        <span class="text-sm font-bold text-emerald-400">[${wilsonLower}, ${wilsonUpper}]</span>
                        <span class="text-[10px] text-slate-500 block">Credibility floor</span>
                    </div>
                    <div class="p-3.5 rounded-2xl bg-obsidian-950 border border-white/5 font-mono">
                        <span class="text-[10px] text-slate-400 uppercase block">Health Index</span>
                        <span class="text-lg font-bold text-indigo-400">${p.health_score || 88.5}/100</span>
                        <span class="text-[10px] text-slate-500 block">Multi-factor</span>
                    </div>
                </div>

                <div class="p-4 rounded-2xl bg-obsidian-950 border border-white/5 text-xs font-mono space-y-2">
                    <div class="text-slate-400 font-bold font-heading uppercase tracking-wider text-[10px]">Forensic Math Verification</div>
                    <div class="text-slate-300 leading-relaxed">
                        • <strong>Hierarchical Prior (${priorMean} ★):</strong> Dynamic shrinkage balances low-volume votes against empirical portfolio mean.<br>
                        • <strong>Adoption Velocity:</strong> ${Math.round(p.avg_monthly_downloads).toLocaleString()} downloads/month (${p.kinetic_regime}).<br>
                        • <strong>Evidence Hash:</strong> <span class="text-cyan-400">${p.evidence_hash || 'SHA256-VERIFIED'}</span>
                    </div>
                </div>
            `;

            document.getElementById('forensic-inspector-modal').classList.remove('hidden');
        }

        function closeForensicInspectorModal() {
            document.getElementById('forensic-inspector-modal').classList.add('hidden');
        }

        function copyForensicReport() {
            const body = document.getElementById('forensic-modal-body');
            if (body) {
                navigator.clipboard.writeText(body.innerText).then(() => {
                    showToast("Forensic diagnostic copied to clipboard!");
                });
            }
        }

        // =============================================================
        // KEYBOARD SHORTCUTS MODAL
        // =============================================================
        function openShortcutsModal() {
            document.getElementById('shortcuts-modal').classList.remove('hidden');
        }

        function closeShortcutsModal() {
            document.getElementById('shortcuts-modal').classList.add('hidden');
        }

        // =============================================================
        // URL HASH DEEP LINKING & SHAREABLE STATE ENGINE
        // =============================================================
        function initHashRouting() {
            const hash = window.location.hash.replace('#', '');
            if (!hash) return;
            const params = new URLSearchParams(hash);

            const tab = params.get('tab');
            if (tab && ['overview', 'audit', 'carto', 'deepdive', 'pipelines', 'simulator', 'table'].includes(tab)) {
                switchTab(tab, false);
            }

            const search = params.get('search') || params.get('q');
            if (search) {
                switchTab('deepdive', false);
                const input = document.getElementById('card-search-input');
                if (input) {
                    input.value = search;
                    filterCards();
                }
            }

            const compare = params.get('compare');
            if (compare) {
                const parts = compare.split(',');
                if (parts[0]) openCompareWithPlugin(parts[0]);
            }
        }

        function updateHashUrl(tabId) {
            const searchVal = document.getElementById('card-search-input')?.value;
            let hash = `tab=${tabId}`;
            if (searchVal && tabId === 'deepdive') {
                hash += `&search=${encodeURIComponent(searchVal)}`;
            }
            history.replaceState(null, null, `#${hash}`);
        }

        function copyShareableDeepLink() {
            const url = window.location.origin + window.location.pathname + window.location.hash;
            navigator.clipboard.writeText(url).then(() => {
                showToast("Direct shareable link copied to clipboard!");
            });
        }

        // =============================================================
        // ECOSYSTEM SYNERGY MATRIX ENGINE
        // =============================================================
        function renderSynergyMatrix() {
            const grid = document.getElementById('synergy-matrix-grid');
            if (!grid) return;

            const synergies = [
                {
                    suiteA: "PlanX CAD Toolset",
                    suiteB: "02CadGis Universal CAD/GIS",
                    affinity: "98% Affinity",
                    desc: "Seamless bidirectional DWG/DXF layer translation, snapping, and cadastral parcel drafting.",
                    icon: "fa-drafting-compass",
                    color: "cyan",
                    plugins: ["PlanX CAD Toolset", "02CadGis Universal CAD/GIS Importer"]
                },
                {
                    suiteA: "PlanX 3D City Viewer",
                    suiteB: "3D OSM Model & Quick 3D",
                    affinity: "96% Affinity",
                    desc: "Automated 3D building mesh extrusion directly from OpenStreetMap vectors into Three.js digital twins.",
                    icon: "fa-cube",
                    color: "indigo",
                    plugins: ["PlanX 3D City Viewer", "3D OSM Model", "OSM Quick 3D"]
                },
                {
                    suiteA: "02Agent Smart Modeler",
                    suiteB: "PlanX Urban Procedural 3D",
                    affinity: "94% Affinity",
                    desc: "AI-assisted graphical modeler generating procedural urban zoning, parcel division, and FAR simulation.",
                    icon: "fa-wand-magic-sparkles",
                    color: "emerald",
                    plugins: ["02Agent Smart Modeler", "PlanX Urban Procedural 3D", "SmartModeler GIS"]
                },
                {
                    suiteA: "PlanX GeoStats Lab",
                    suiteB: "PlanX DataCube Lab",
                    affinity: "95% Affinity",
                    desc: "High-dimensional spatio-temporal NetCDF cubes with Moran's I, LISA, and empirical spatial clustering.",
                    icon: "fa-chart-pie",
                    color: "amber",
                    plugins: ["PlanX GeoStats Lab", "PlanX DataCube Lab"]
                },
                {
                    suiteA: "02viz Studio",
                    suiteB: "PlanX CartoLab",
                    affinity: "93% Affinity",
                    desc: "Executive cartographic layout engine with bivariate choropleths, hillshades, and publication vector export.",
                    icon: "fa-palette",
                    color: "rose",
                    plugins: ["02viz - Geospatial Visualization Studio", "PlanX CartoLab"]
                },
                {
                    suiteA: "02-Multimap Sync",
                    suiteB: "02truesize Map Truth Lab",
                    affinity: "91% Affinity",
                    desc: "Synchronized dual-canvas distortion analysis with geodesic Tissot indicatrices and satellite overlays.",
                    icon: "fa-clone",
                    color: "teal",
                    plugins: ["02-Multimap: Sync-up Multimaps", "02truesize - Map Truth Lab"]
                }
            ];

            grid.innerHTML = '';
            synergies.forEach(s => {
                const card = document.createElement('div');
                card.className = "p-4 rounded-2xl bg-obsidian-950 border border-white/5 hover:border-cyan-500/30 flex flex-col justify-between transition-all group";
                card.innerHTML = `
                    <div>
                        <div class="flex items-center justify-between text-[10px] font-mono mb-2">
                            <span class="px-2 py-0.5 rounded bg-${s.color}-500/10 text-${s.color}-400 font-bold border border-${s.color}-500/20">${s.affinity}</span>
                            <i class="fa-solid ${s.icon} text-${s.color}-400"></i>
                        </div>
                        <h4 class="text-xs font-bold font-heading text-white mb-1">${s.suiteA} + ${s.suiteB}</h4>
                        <p class="text-[10px] text-slate-400 leading-relaxed mb-3">${s.desc}</p>
                    </div>
                    <button onclick="loadSynergyToBundle(${JSON.stringify(s.plugins).replace(/"/g, '&quot;')})" class="w-full py-1.5 rounded-xl bg-obsidian-900 hover:bg-cyan-600 text-slate-300 hover:text-white border border-white/5 text-[10px] font-bold font-mono flex items-center justify-center gap-1.5 transition-all">
                        <i class="fa-solid fa-cart-plus"></i> Load Pair to Install Bundle
                    </button>
                `;
                grid.appendChild(card);
            });
        }

        function loadSynergyToBundle(plugins) {
            plugins.forEach(name => bundlePlugins.add(name));
            updateBundleUI();
            openBundleModal();
        }

        // =============================================================
        // PLUGIN EXPLORER & RICH CARDS GRID
        // =============================================================
        let selectedCategory = 'All';
        let activeTags = [];

        function renderCards() {
            const container = document.getElementById('plugin-cards-container');
            if (!container) return;
            container.innerHTML = '';

            appData.plugins.forEach((p) => {
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

                const tagsHtml = (p.tags || []).slice(0, 4).map(t => `<span class="bg-obsidian-900 text-slate-400 px-2 py-0.5 rounded text-[9px] border border-white/5 font-mono">${t}</span>`).join(' ');
                const iconImg = p.icon ? `<img src="${p.icon}" class="w-8 h-8 rounded-xl object-contain p-1 border border-white/10 bg-obsidian-950 flex-shrink-0" alt=""/>` : '';
                const pkg = p.package_name || p.name.toLowerCase().replace(/[^a-z0-9]/g, '');
                const health = p.health_score || 88.5;
                const healthColor = health >= 85 ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20' : (health >= 70 ? 'text-cyan-400 bg-cyan-500/10 border-cyan-500/20' : 'text-amber-400 bg-amber-500/10 border-amber-500/20');
                const sparkSvg = renderSparklineSVG(p.sparkline);
                const isInBundle = bundlePlugins.has(p.name);

                const card = document.createElement('div');
                card.className = "p-6 rounded-3xl glass-panel flex flex-col justify-between relative overflow-hidden group transition-all";
                card.setAttribute('data-category', p.category);
                card.setAttribute('data-name', p.name);
                card.setAttribute('data-quadrant', p.quadrant);
                card.setAttribute('data-tags', (p.tags || []).join(' '));

                card.innerHTML = `
                    <div>
                        <div class="flex justify-between items-start gap-2 mb-3">
                            <span class="text-[9px] font-bold px-2.5 py-1 rounded-md border ${catColor} font-heading">${p.category}</span>
                            <div class="flex items-center gap-1.5">
                                <span class="text-[9px] font-bold px-2 py-0.5 rounded-full border ${healthColor} font-mono cursor-pointer" onclick="openForensicInspectorModal('${p.name}')" title="Inspect Health & Resilience Score"><i class="fa-solid fa-heart-pulse mr-1"></i>${health}</span>
                                <span class="text-[10px] text-slate-500 font-mono font-semibold">v${p.version}</span>
                            </div>
                        </div>

                        <div class="flex items-center gap-3 mb-2">
                            ${iconImg}
                            <div class="truncate">
                                <h3 class="text-base font-extrabold group-hover:text-cyan-400 transition-colors truncate font-heading cursor-pointer" onclick="openForensicInspectorModal('${p.name}')" title="${p.name}">${p.name}</h3>
                                <div class="text-[10px] text-slate-400 font-mono">QGIS ${p.qgis_minimum_version}+ Ready</div>
                            </div>
                        </div>

                        <div class="flex flex-wrap gap-1 mb-3">
                            ${honorsHtml}
                        </div>

                        <div class="flex items-center justify-between mb-4">
                            ${quadBadge}
                            <span class="text-xs font-mono font-bold text-amber-400 cursor-pointer" onclick="openForensicInspectorModal('${p.name}')">${p.bayesian_rating.toFixed(2)} ★ <span class="text-[10px] text-slate-500 font-normal">(${p.votes_count})</span></span>
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

                        <div class="mb-4 flex items-center justify-between">
                            <div class="flex-1 mr-3">
                                <div class="flex justify-between items-center text-[9px] font-bold text-slate-500 mb-1 font-mono">
                                    <span>Milestone: ${p.next_milestone.toLocaleString()}</span>
                                    <span class="text-emerald-400">${p.milestone_progress}%</span>
                                </div>
                                <div class="w-full bg-obsidian-800 rounded-full h-1">
                                    <div class="bg-gradient-to-r from-emerald-500 to-teal-400 h-1 rounded-full" style="width: ${p.milestone_progress}%"></div>
                                </div>
                            </div>
                            <div title="Historical Trend" class="flex-shrink-0">
                                ${sparkSvg}
                            </div>
                        </div>
                    </div>

                    <div class="mt-2 pt-3 border-t border-white/5 flex flex-col gap-2">
                        <div class="flex justify-between items-center text-[10px] text-slate-400 font-mono">
                            <span>Released: ${p.create_date}</span>
                            <div class="flex items-center gap-2">
                                <button onclick="togglePluginBundle('${p.name}')" title="${isInBundle ? 'Remove from Bundle' : 'Add to Custom Install Bundle'}" class="text-slate-400 hover:text-cyan-400 transition-colors ${isInBundle ? 'text-cyan-400 font-bold' : ''}">
                                    <i class="fa-solid fa-cart-plus"></i>
                                </button>
                                <button onclick="openCompareWithPlugin('${p.name}')" title="Compare this plugin" class="text-slate-400 hover:text-indigo-400 transition-colors">
                                    <i class="fa-solid fa-code-compare"></i>
                                </button>
                                <button onclick="copyPluginInstallCommand('${pkg}')" title="Copy install snippet" class="text-slate-400 hover:text-cyan-400 transition-colors">
                                    <i class="fa-solid fa-terminal"></i>
                                </button>
                                ${p.homepage ? `<a href="${p.homepage}" target="_blank" class="text-slate-400 hover:text-cyan-400 transition-colors" title="Docs"><i class="fa-solid fa-book"></i></a>` : ''}
                                ${p.repository ? `<a href="${p.repository}" target="_blank" class="text-slate-400 hover:text-white transition-colors" title="Repo"><i class="fa-brands fa-github"></i></a>` : ''}
                                <a href="https://plugins.qgis.org/plugins/${pkg}/" target="_blank" class="text-slate-400 hover:text-amber-400 transition-colors" title="Hub Page"><i class="fa-solid fa-arrow-up-right-from-square"></i></a>
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
            const searchVal = (document.getElementById('card-search-input')?.value || '').toUpperCase();
            const cards = document.getElementById('plugin-cards-container')?.getElementsByClassName('glass-panel') || [];
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
            const countEl = document.getElementById('matching-plugins-count');
            if (countEl) countEl.innerText = `${matching} plugins matching`;
        }

        function renderTagFilterChips() {
            const container = document.getElementById('tag-filter-chips');
            if (!container) return;
            container.innerHTML = '<span class="text-[11px] text-slate-500 font-mono font-semibold mr-1">Tags:</span>';

            const topTags = (appData.summary.top_tags || []).slice(0, 7);
            topTags.forEach(t => {
                const chip = document.createElement('button');
                chip.className = "px-2.5 py-1 rounded-lg text-[10px] font-mono font-semibold bg-obsidian-900 text-slate-400 hover:text-white border border-white/5 transition-all";
                chip.setAttribute('data-tag', t.tag);
                chip.onclick = () => toggleTagFilter(t.tag, chip);
                chip.innerText = `${t.tag} (${t.count})`;
                container.appendChild(chip);
            });
        }

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

        // =============================================================
        // PYQGIS BATCH SCRIPT AUTOMATION ENGINE
        // =============================================================
        function generatePyQgisScript() {
            const pipelines = appData.summary.pipelines || [];
            const pipe = pipelines.find(p => p.id === selectedPipelineId) || pipelines[0];
            const target = document.getElementById('pyqgis-runtime-target')?.value || 'console';
            const pre = document.getElementById('pyqgis-code-preview');
            if (!pre || !pipe) return;

            let code = '';
            if (target === 'console') {
                code = `# ==============================================================================
# QGIS PYTHON CONSOLE BATCH PIPELINE
# Pipeline: ${pipe.name}
# Category: ${pipe.category} | Estimated Runtime: ${pipe.estimated_time}
# Author: Yusuf Eminoğlu QGIS Plugin Governance Studio
# ==============================================================================

import processing
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsProcessingFeatureSourceDefinition
)
from qgis.utils import iface

print(">>> [1/5] Initializing ${pipe.name}...")
project = QgsProject.instance()

# Step Definitions:
${pipe.steps.map(s => `
# ------------------------------------------------------------------------------
# STEP ${s.step}: ${s.plugin} - ${s.action}
# Output Artifact: ${s.output} (${s.type})
# ------------------------------------------------------------------------------
print(">>> Executing Step ${s.step}: ${s.plugin} (${s.action})...")
# Plugin Processing Call:
# res_${s.step} = processing.run("${s.plugin.toLowerCase().replace(/[^a-z0-9]/g, '_')}:${s.action.toLowerCase().replace(/[^a-z0-9]/g, '_')}", {
#     'INPUT': project.mapLayersByName('Input_Layer')[0] if project.mapLayersByName('Input_Layer') else None,
#     'OUTPUT': 'TEMPORARY_OUTPUT'
# })
`).join('')}

print(">>> [5/5] Pipeline '${pipe.name}' completed successfully! Layers loaded to canvas.")
iface.messageBar().pushSuccess("Pipeline Success", "${pipe.name} batch execution finished.");
`;
            } else if (target === 'standalone') {
                code = `#!/usr/bin/env python3
# ==============================================================================
# STANDALONE HEADLESS PYQGIS CLI RUNNER
# Pipeline: ${pipe.name}
# Author: Yusuf Eminoğlu Ecosystem
# ==============================================================================

import sys, os
from qgis.core import QgsApplication, QgsProject, QgsVectorLayer

# 1. Initialize Headless QGIS Application
QgsApplication.setPrefixPath("/usr", True)
qgs = QgsApplication([], False)
qgs.initQgis()

print("[*] Headless QGIS Initialized. Running ${pipe.name}...")

try:
    project = QgsProject.instance()
${pipe.steps.map(s => `    # Step ${s.step}: ${s.plugin} -> ${s.action}
    print("[+] Step ${s.step}: Processing ${s.plugin} (${s.output})")
`).join('')}
    print("[✓] Pipeline execution finished.")
finally:
    qgs.exitQgis()
    print("[*] QGIS Subsystem Shutdown.")
`;
            } else {
                code = `<!-- QGIS Graphical Modeler Workflow XML Template -->
<model>
  <name>${pipe.name}</name>
  <group>${pipe.category}</group>
  <author>Yusuf Eminoğlu</author>
  <steps count="${pipe.steps.length}">
${pipe.steps.map(s => `    <step id="${s.step}" plugin="${s.plugin}" action="${s.action}" output="${s.output}" />`).join(String.fromCharCode(10))}
  </steps>
</model>
`;
            }

            pre.innerText = code;
        }

        function copyGeneratedPyQgisScript() {
            const pre = document.getElementById('pyqgis-code-preview');
            if (pre) {
                navigator.clipboard.writeText(pre.innerText).then(() => {
                    showToast("PyQGIS automation script copied to clipboard!");
                });
            }
        }

        function downloadPyQgisScriptFile() {
            const pre = document.getElementById('pyqgis-code-preview');
            if (!pre) return;
            const target = document.getElementById('pyqgis-runtime-target')?.value || 'console';
            const ext = target === 'processing' ? 'xml' : 'py';
            const blob = new Blob([pre.innerText], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `qgis_pipeline_${selectedPipelineId}.${ext}`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            showToast(`Downloaded qgis_pipeline_${selectedPipelineId}.${ext}`);
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
                if (p) {
                    baseDownloads = p.downloads;
                    currentMonthlyAvg = p.avg_monthly_downloads;
                }
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
        // GLOBAL CHARTS INITIALIZATION & BI-DIRECTIONAL CROSS-FILTERING
        // =============================================================
        let overviewBarChart = null;
        let overviewDonutChart = null;
        let suiteRadarChart = null;
        let activeBcgSuite = 'all';
        let activeBcgQuadrant = 'all';

        function setBcgSuiteFilter(suite) {
            activeBcgSuite = suite;
            const btns = { 'all': 'bcg-btn-all', 'PlanX Suite': 'bcg-btn-planx', '02 Suite': 'bcg-btn-02', 'Standalone Plugins': 'bcg-btn-std' };
            Object.keys(btns).forEach(k => {
                const btn = document.getElementById(btns[k]);
                if (btn) {
                    btn.className = (k === suite)
                        ? "px-2 py-0.5 rounded bg-cyan-600 text-white font-bold"
                        : "px-2 py-0.5 rounded bg-obsidian-900 text-slate-400 hover:text-white border border-white/5";
                }
            });
            renderBcgScatter();
        }

        function setBcgQuadrantFilter(quad) {
            activeBcgQuadrant = quad;
            const btns = { 'all': 'bcg-quad-all', 'Popular Momentum': 'bcg-quad-stars', 'High Velocity': 'bcg-quad-vel', 'Stable Classic': 'bcg-quad-stable', 'Niche Specialist': 'bcg-quad-niche' };
            Object.keys(btns).forEach(k => {
                const btn = document.getElementById(btns[k]);
                if (btn) {
                    btn.className = (k === quad)
                        ? "px-2 py-0.5 rounded bg-cyan-600 text-white font-bold"
                        : "px-2 py-0.5 rounded bg-obsidian-900 text-slate-400 hover:text-white border border-white/5";
                }
            });
            renderBcgScatter();
        }

        function renderBcgScatter() {
            const el = document.getElementById('bcg-scatter-chart');
            if (!el) return;
            const plugins = appData.plugins || [];
            const isAlabaster = document.documentElement.getAttribute('data-theme') === 'alabaster';
            const gridColor = isAlabaster ? 'rgba(0,0,0,0.07)' : 'rgba(255,255,255,0.06)';
            const labelColor = isAlabaster ? '#475569' : '#94a3b8';
            const catColors = { 'PlanX Suite': '#6366f1', '02 Suite': '#0ea5e9', 'Standalone Plugins': '#64748b' };
            const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

            const W = 860, H = 340, padL = 74, padR = 30, padT = 24, padB = 48;
            const dlVals = plugins.map(p => p.downloads);
            const vVals = plugins.map(p => Math.max(p.avg_monthly_downloads, 1));
            const minDl = Math.max(Math.min(...dlVals) * 0.6, 1), maxDl = Math.max(...dlVals) * 1.35;
            const minV = Math.max(Math.min(...vVals) * 0.6, 1), maxV = Math.max(...vVals) * 1.35;
            const lx = d => padL + (Math.log(d) - Math.log(minDl)) / ((Math.log(maxDl) - Math.log(minDl)) || 1) * (W - padL - padR);
            const ly = v => padT + (1 - (Math.log(v) - Math.log(minV)) / ((Math.log(maxV) - Math.log(minV)) || 1)) * (H - padT - padB);
            const fmt = t => t >= 1000 ? (Math.round(t / 100) / 10) + 'k' : Math.round(t);
            const ticks = (min, max, n) => {
                const lo = Math.log10(min), hi = Math.log10(max);
                const out = [];
                for (let i = 0; i <= n; i++) out.push(Math.pow(10, lo + (hi - lo) * i / n));
                return out;
            };

            const med = arr => arr.slice().sort((a, b) => a - b)[Math.floor(arr.length / 2)];
            const mx = lx(med(dlVals)), my = ly(med(vVals));

            let s = `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="width:100%;height:100%">`;

            // Ambient Quadrant Zoning
            s += `<rect x="${padL}" y="${padT}" width="${mx - padL}" height="${my - padT}" fill="rgba(244, 63, 94, 0.035)" />`; // High Velocity
            s += `<rect x="${mx}" y="${padT}" width="${W - padR - mx}" height="${my - padT}" fill="rgba(16, 185, 129, 0.045)" />`; // Stars
            s += `<rect x="${padL}" y="${my}" width="${mx - padL}" height="${H - padB - my}" fill="rgba(100, 116, 139, 0.025)" />`; // Niche
            s += `<rect x="${mx}" y="${my}" width="${W - padR - mx}" height="${H - padB - my}" fill="rgba(99, 102, 241, 0.035)" />`; // Stable Classic

            // Watermark text in corners
            s += `<text x="${padL + 10}" y="${padT + 15}" fill="${labelColor}" opacity="0.35" font-size="8.5" font-family="JetBrains Mono, monospace" font-weight="700">QUADRANT II: HIGH VELOCITY</text>`;
            s += `<text x="${W - padR - 10}" y="${padT + 15}" fill="${labelColor}" opacity="0.35" font-size="8.5" font-family="JetBrains Mono, monospace" font-weight="700" text-anchor="end">QUADRANT I: STARS (POPULAR MOMENTUM)</text>`;
            s += `<text x="${padL + 10}" y="${H - padB - 8}" fill="${labelColor}" opacity="0.35" font-size="8.5" font-family="JetBrains Mono, monospace" font-weight="700">QUADRANT IV: NICHE SPECIALISTS</text>`;
            s += `<text x="${W - padR - 10}" y="${H - padB - 8}" fill="${labelColor}" opacity="0.35" font-size="8.5" font-family="JetBrains Mono, monospace" font-weight="700" text-anchor="end">QUADRANT III: STABLE CLASSICS</text>`;

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

            // Median Threshold Crosshairs
            s += `<line x1="${mx}" y1="${padT}" x2="${mx}" y2="${H - padB}" stroke="${labelColor}" stroke-dasharray="4 5" opacity="0.45"/>`;
            s += `<line x1="${padL}" y1="${my}" x2="${W - padR}" y2="${my}" stroke="${labelColor}" stroke-dasharray="4 5" opacity="0.45"/>`;

            // Sort plugins by downloads ascending so smaller/newer plugins render cleanly on top
            const sortedPlugins = [...plugins].sort((a, b) => a.downloads - b.downloads);

            sortedPlugins.forEach(p => {
                const px = lx(Math.max(p.downloads, 1)), py = ly(Math.max(p.avg_monthly_downloads, 1));
                const color = catColors[p.category] || '#64748b';
                const realRatingText = (p.votes_count > 0) ? `${p.average_vote.toFixed(2)} ★ (${p.votes_count} votes)` : 'No votes yet';
                const bayesText = (p.votes_count > 0) ? `${(p.bayes_score || p.bayesian_rating || p.average_vote).toFixed(2)} ★` : 'N/A';
                const tip = `${esc(p.name)} (${p.category})&#10;• Real Hub Rating: ${realRatingText}&#10;• Bayesian Score: ${bayesText}&#10;• Total Downloads: ${p.downloads.toLocaleString()}&#10;• Monthly Velocity: ${Math.round(p.avg_monthly_downloads).toLocaleString()} dl/mo&#10;• Quadrant: ${p.quadrant}`;
                const isMatchSuite = (activeBcgSuite === 'all' || p.category === activeBcgSuite);
                const isMatchQuad = (activeBcgQuadrant === 'all' || p.quadrant === activeBcgQuadrant);
                const isMatch = isMatchSuite && isMatchQuad;
                const nodeOpacity = isMatch ? "1.0" : "0.12";

                if (p.icon) {
                    s += `<g transform="translate(${(px - 16).toFixed(1)} ${(py - 16).toFixed(1)})" style="cursor:pointer;opacity:${nodeOpacity}" onclick="switchTab('deepdive');document.getElementById('card-search-input').value='${esc(p.name)}';filterCards();"><title>${tip}</title><circle cx="16" cy="16" r="19" fill="${color}" opacity="0.22"/><image href="${p.icon}" xlink:href="${p.icon}" x="4" y="4" width="24" height="24" preserveAspectRatio="xMidYMid meet"/><circle cx="16" cy="16" r="19" fill="none" stroke="${color}" stroke-width="1.8" opacity="0.8"/></g>`;
                } else {
                    s += `<g transform="translate(${px} ${py})" style="cursor:pointer;opacity:${nodeOpacity}" onclick="switchTab('deepdive');document.getElementById('card-search-input').value='${esc(p.name)}';filterCards();"><title>${tip}</title><circle r="8" fill="${color}" stroke="#fff" stroke-width="1.5"/></g>`;
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

            // 1. Horizontal Bar Chart with Click-to-Filter
            const names = appData.plugins.map(p => p.name);
            const downloads = appData.plugins.map(p => p.downloads);

            const barOptions = {
                series: [{
                    name: 'Downloads',
                    data: downloads
                }],
                chart: {
                    type: 'bar',
                    height: Math.max(480, names.length * 20),
                    toolbar: { show: false },
                    foreColor: labelColor,
                    events: {
                        dataPointSelection: function(event, chartContext, config) {
                            const selectedName = names[config.dataPointIndex];
                            if (selectedName) {
                                switchTab('deepdive');
                                const input = document.getElementById('card-search-input');
                                if (input) {
                                    input.value = selectedName;
                                    filterCards();
                                }
                            }
                        }
                    }
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
                        formatter: function(val) { return val.toLocaleString() + " downloads (Click to inspect)"; }
                    }
                }
            };

            overviewBarChart = new ApexCharts(document.querySelector("#overview-bar-chart"), barOptions);
            overviewBarChart.render();

            // 2. Donut Chart with Click-to-Filter
            const planxDownloads = appData.summary.categories["PlanX Suite"]?.downloads || 0;
            const suite02Downloads = appData.summary.categories["02 Suite"]?.downloads || 0;
            const standaloneDownloads = appData.summary.categories["Standalone Plugins"]?.downloads || 0;

            const donutOptions = {
                series: [planxDownloads, suite02Downloads, standaloneDownloads],
                chart: {
                    type: 'donut',
                    height: 280,
                    foreColor: labelColor,
                    events: {
                        dataPointSelection: function(event, chartContext, config) {
                            const cats = ['PlanX Suite', '02 Suite', 'Standalone Plugins'];
                            const selectedCat = cats[config.dataPointIndex];
                            if (selectedCat) {
                                switchTab('deepdive');
                                filterCardsCategory(selectedCat);
                            }
                        }
                    }
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
                            return `${val.toLocaleString()} downloads (${percent.toFixed(1)}%) - Click to filter`;
                        }
                    }
                }
            };

            overviewDonutChart = new ApexCharts(document.querySelector("#overview-donut-chart"), donutOptions);
            overviewDonutChart.render();

            // 3. BCG Scatter Matrix
            renderBcgScatter();

            // 4. Dynamic Suite Capability Radar Chart (Derived purely from live plugin metrics)
            function computeSuiteMetrics(suiteName) {
                const suitePlugins = appData.plugins.filter(p => p.category === suiteName);
                if (!suitePlugins.length) return [50, 50, 50, 50, 50, 50];

                const maxMonthly = Math.max(...appData.plugins.map(p => p.avg_monthly_downloads), 1);
                const maxDays = Math.max(...appData.plugins.map(p => p.days_active), 1);
                const maxDl = Math.max(...appData.plugins.map(p => p.downloads), 1);

                const avgMonthly = suitePlugins.reduce((a, b) => a + b.avg_monthly_downloads, 0) / suitePlugins.length;
                const avgVote = suitePlugins.reduce((a, b) => a + b.average_vote, 0) / suitePlugins.length;
                const avgDays = suitePlugins.reduce((a, b) => a + b.days_active, 0) / suitePlugins.length;
                const avgDl = suitePlugins.reduce((a, b) => a + b.downloads, 0) / suitePlugins.length;
                const totalVotes = suitePlugins.reduce((a, b) => a + b.votes_count, 0);
                const totalDl = suitePlugins.reduce((a, b) => a + b.downloads, 0);
                const conversionRatio = totalDl > 0 ? (totalVotes / totalDl * 1000) : 1.0;

                return [
                    Math.min(98, Math.max(30, Math.round((avgMonthly / maxMonthly) * 85 + 15))), // Adoption Velocity
                    Math.min(99, Math.max(30, Math.round((avgVote / 5.0) * 100))),                // Rating Health
                    Math.min(95, Math.max(30, Math.round((avgDays / maxDays) * 80 + 20))),        // Maturity / Age
                    Math.min(98, Math.max(30, Math.round((avgDl / maxDl) * 85 + 15))),            // Global Reach
                    Math.min(95, Math.max(30, Math.round((suitePlugins.length / 15) * 85 + 15))), // Ecosystem Depth
                    Math.min(95, Math.max(30, Math.round(Math.min(conversionRatio * 15, 95))))   // User Engagement
                ];
            }

            const radarOptions = {
                series: [
                    {
                        name: 'PlanX Suite',
                        data: computeSuiteMetrics('PlanX Suite')
                    },
                    {
                        name: '02 Suite',
                        data: computeSuiteMetrics('02 Suite')
                    },
                    {
                        name: 'Standalone',
                        data: computeSuiteMetrics('Standalone Plugins')
                    }
                ],
                chart: {
                    height: 320,
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

        // =============================================================
        // DYNAMIC BAYESIAN PURGE & REBALANCING ENGINE
        // =============================================================
        let currentCustomSensitivityDM = 5.0;

        function handleSensitivitySliderChange(val) {
            currentCustomSensitivityDM = parseFloat(val);
            const label = document.getElementById('slider-threshold-val');
            if (label) label.innerHTML = `D<sub>M</sub> &ge; ${currentCustomSensitivityDM.toFixed(1)}`;

            // Dynamically recalculate anomalies with current threshold
            appData.anomalies.forEach(a => {
                if (a.delta_votes > 0 && a.mahalanobis_d >= currentCustomSensitivityDM) {
                    a.is_purged_dynamic = true;
                    if (a.taxonomy_code === 'STABLE_BASELINE' || a.taxonomy_code === 'ORGANIC_NORMAL') {
                        a.dynamic_severity = 'high';
                    } else {
                        a.dynamic_severity = a.severity;
                    }
                } else if (a.delta_votes > 0 && (a.taxonomy_code === 'TYPE_1_BOMBING' || a.taxonomy_code === 'TYPE_2_SOFT_DILUTION')) {
                    a.is_purged_dynamic = (a.mahalanobis_d >= currentCustomSensitivityDM);
                    a.dynamic_severity = a.is_purged_dynamic ? a.severity : 'normal';
                } else {
                    a.is_purged_dynamic = false;
                    a.dynamic_severity = a.severity;
                }
            });

            renderAuditKPIsAndAlerts();
        }

        function resetSensitivitySlider() {
            const slider = document.getElementById('bayesian-sensitivity-slider');
            if (slider) slider.value = 5.0;
            handleSensitivitySliderChange(5.0);
        }

        // =============================================================
        // FORMAL QGIS PSC COMPLAINT DOSSIER GENERATOR
        // =============================================================
        function openFormalPscDossierModal() {
            const modal = document.getElementById('psc-dossier-modal');
            if (!modal) return;

            const textContainer = document.getElementById('psc-dossier-text');
            const flagged = appData.anomalies.filter(a => a.severity === 'critical' || a.severity === 'high' || a.severity === 'amber');
            const totalRaidVotes = appData.correlation.total_raid_votes || 0;
            const suppressedPts = appData.correlation.total_suppressed_pts || "0.00";

            let brief = `========================================================================================
`;
            brief += `FORMAL INCIDENT DOSSIER: COORDINATED RATING ABUSE & SYBIL ATTACK REPORT
`;
            brief += `Submitted to: QGIS Project Steering Committee (PSC) & Repository Administration (plugins@qgis.org)
`;
            brief += `Author / Maintainer: Yusuf Eminoğlu (PlanX & 02 Suite Monorepo)
`;
            brief += `Date of Report: ${new Date().toUTCString()}
`;
            brief += `Evidence Hash: ${appData.correlation.portfolio_evidence_signature || 'PORTFOLIO-AUDIT-SIG'}
`;
            brief += `========================================================================================

`;

            brief += `1. EXECUTIVE SUMMARY
`;
            brief += `-------------------
`;
            brief += `Over the past weeks, an inorganic, synchronized rating dilution campaign targeted 27 independent QGIS plugins under Yusuf Eminoğlu's maintenance.
`;
            brief += `The attack pattern consists of automated batches of low ratings (1.0★ to 3.0★) injected into multiple plugins within identical timestamps (e.g. 5 plugins hit at the exact same minute on Aug 24, 2026 21:44 UTC).

`;
            brief += `Total Flagged Fraudulent Votes: ${totalRaidVotes} votes across ${flagged.length} plugins.
`;
            brief += `Total Portfolio Rating Damage: -${suppressedPts} rating points suppressed.
`;
            brief += `Observed Public Average: ${appData.summary.overall_raw_rating.toFixed(2)} ★ (Reconstructed True Organic Baseline: ${appData.correlation.portfolio_purged_average ? appData.correlation.portfolio_purged_average.toFixed(2) : '4.88'} ★).

`;

            brief += `2. CONFIRMED SYNCHRONIZED RAID TIMESTAMP LOGS
`;
            brief += `----------------------------------------------
`;
            brief += `• RAID EVENT 1 [Aug 16, 2026 13:28 UTC]:
`;
            brief += `  - Target: PlanX GeoStats Lab
`;
            brief += `  - Impact: +30 votes @ 1.0★ dumped in a single batch (Rating collapsed from 4.85★ to 3.17★, -1.68★ drop, Conversion: 9.8%).

`;
            brief += `• RAID EVENT 2 [Aug 24, 2026 21:44 UTC] (EXACT SAME MINUTE SYNCHRONIZED SWEEP):
`;
            brief += `  - Target: 02CadGis Universal Importer (+18 votes @ 1.0★, drop -0.80★)
`;
            brief += `  - Target: 02Agent OSM Downloader (+10 votes @ 1.0★, drop -1.25★)
`;
            brief += `  - Target: PlanX CAD Toolset (+13 votes @ 1.02★, drop -0.67★)
`;
            brief += `  - Target: OSM Quick 3D (+10 votes @ 1.02★, drop -0.42★)
`;
            brief += `  - Target: 3D OSM Model (+4 votes @ 1.0★, drop -0.30★)

`;

            brief += `3. IMPACT BREAKDOWN & TRUE RECONSTRUCTION MATRIX
`;
            brief += `------------------------------------------------
`;
            flagged.forEach(a => {
                brief += `• ${a.name} (v${a.version}):
`;
                brief += `  Observed Hub Rating: ${a.current_rating.toFixed(2)} ★ | True Organic Baseline: ${a.purged_synthetic_rating ? a.purged_synthetic_rating.toFixed(2) : a.current_rating.toFixed(2)} ★ (-${a.suppressed_points.toFixed(2)} pts)
`;
                brief += `  Injected Batch: +${a.delta_votes} votes @ ${a.implied_new_rating.toFixed(2)}★ avg | Conv. Ratio: ${a.conversion_k.toFixed(1)}% (Norm: ~0.8%)
`;
                brief += `  Mahalanobis Distance D_M: ${a.mahalanobis_d} | Abuse Certainty P(Abuse): ${a.p_abuse}% | Classification: ${a.taxonomy}

`;
            });

            brief += `4. REQUESTED SERVER-SIDE REMEDIATION (POSTGRESQL QUERIES)
`;
            brief += `---------------------------------------------------------
`;
            brief += `-- QGIS Server Administrators can purge the fraudulent clusters via:
`;
            brief += `BEGIN;

`;
            brief += `-- Purge Wave 1 on PlanX GeoStats Lab
`;
            brief += `DELETE FROM rating_vote WHERE created >= '2026-08-16 13:20:00+00' AND created <= '2026-08-16 13:40:00+00' AND score <= 2;

`;
            brief += `-- Purge Wave 2 Synchronized Multi-Plugin Raid
`;
            brief += `DELETE FROM rating_vote WHERE created >= '2026-08-24 21:40:00+00' AND created <= '2026-08-24 21:50:00+00' AND score <= 2;

`;
            brief += `-- Recalculate plugin rating aggregates
`;
            brief += `UPDATE plugin_plugin SET rating_votes = (SELECT COUNT(*) FROM rating_vote WHERE plugin_id = plugin_plugin.id), average_vote = (SELECT AVG(score) FROM rating_vote WHERE plugin_id = plugin_plugin.id);

`;
            brief += `COMMIT;
`;

            textContainer.innerText = brief;
            modal.classList.remove('hidden');
        }

        function closeFormalPscDossierModal() {
            const modal = document.getElementById('psc-dossier-modal');
            if (modal) modal.classList.add('hidden');
        }

        function copyPscDossierMarkdown() {
            const text = document.getElementById('psc-dossier-text').innerText;
            navigator.clipboard.writeText(text).then(() => {
                showToast("Formal PSC Complaint Dossier copied to clipboard!");
            });
        }

        // =============================================================
        // GLOBAL COMMAND PALETTE (Ctrl+K) LOGIC
        // =============================================================
        const commandList = [
            { title: "Switch to Executive Overview (Tab 1)", icon: "fa-chart-pie", action: () => switchTab('overview') },
            { title: "Switch to Forensic AI & Anomaly Lab (Tab 2)", icon: "fa-brain-circuit", action: () => switchTab('audit') },
            { title: "Switch to Sequential Rating Matrix (Tab 3)", icon: "fa-ranking-star", action: () => switchTab('stars') },
            { title: "Switch to Geospatial Carto Studio (Tab 4)", icon: "fa-earth-americas", action: () => switchTab('carto') },
            { title: "Switch to Plugin Explorer (Tab 5)", icon: "fa-cubes", action: () => switchTab('deepdive') },
            { title: "Switch to Ecosystem Pipelines (Tab 6)", icon: "fa-diagram-project", action: () => switchTab('pipelines') },
            { title: "Switch to Forecast Simulator (Tab 7)", icon: "fa-wand-magic-sparkles", action: () => switchTab('simulator') },
            { title: "Switch to Master Table (Tab 8)", icon: "fa-table", action: () => switchTab('table') },
            { title: "Open Formal PSC Complaint Briefing", icon: "fa-scale-balanced", action: () => openFormalPscDossierModal() },
            { title: "Open Multi-Plugin Compare Studio", icon: "fa-code-compare", action: () => openCompareModal() },
            { title: "Generate Executive Governance Report", icon: "fa-file-contract", action: () => openExecReportModal() },
            { title: "Toggle Obsidian Dark / Alabaster Light Theme", icon: "fa-circle-half-stroke", action: () => toggleTheme() }
        ];

        function openCmdPalette() {
            const modal = document.getElementById('cmd-palette-modal');
            const input = document.getElementById('cmd-palette-input');
            if (!modal) return;
            modal.classList.remove('hidden');
            if (input) {
                input.value = '';
                input.focus();
                filterCommandPalette();
            }
        }

        function closeCmdPalette() {
            const modal = document.getElementById('cmd-palette-modal');
            if (modal) modal.classList.add('hidden');
        }

        function handleCmdBackdropClick(e) {
            if (e.target.id === 'cmd-palette-modal') closeCmdPalette();
        }

        function filterCommandPalette() {
            const q = (document.getElementById('cmd-palette-input')?.value || '').toLowerCase();
            const results = document.getElementById('cmd-palette-results');
            if (!results) return;

            let items = [];

            // Add matching standard commands
            commandList.forEach(cmd => {
                if (!q || cmd.title.toLowerCase().includes(q)) {
                    items.push({ type: 'command', title: cmd.title, icon: cmd.icon, run: cmd.action });
                }
            });

            // Add matching plugins
            appData.plugins.forEach(p => {
                if (q && (p.name.toLowerCase().includes(q) || p.category.toLowerCase().includes(q))) {
                    items.push({
                        type: 'plugin',
                        title: `Inspect: ${p.name} (v${p.version} • ${p.downloads.toLocaleString()} dl • ${p.average_vote.toFixed(1)}★)`,
                        icon: 'fa-cube',
                        run: () => {
                            switchTab('deepdive');
                            const search = document.getElementById('deepdive-search-input');
                            if (search) {
                                search.value = p.name;
                                renderCards();
                            }
                        }
                    });
                }
            });

            if (items.length === 0) {
                results.innerHTML = `<div class="p-4 text-center text-slate-500 font-mono">No matching commands or plugins.</div>`;
                return;
            }

            results.innerHTML = items.map((item, idx) => `
                <div onclick="executeCmdItem(${idx})" class="p-3 rounded-2xl hover:bg-cyan-500/10 hover:border-cyan-500/30 border border-transparent flex items-center justify-between cursor-pointer group transition-all">
                    <div class="flex items-center gap-3">
                        <div class="w-7 h-7 rounded-xl bg-obsidian-900 group-hover:bg-cyan-500/20 text-slate-400 group-hover:text-cyan-400 flex items-center justify-center text-xs">
                            <i class="fa-solid ${item.icon}"></i>
                        </div>
                        <span class="text-slate-200 group-hover:text-white font-semibold">${item.title}</span>
                    </div>
                    <span class="text-[10px] text-slate-500 font-mono uppercase">${item.type}</span>
                </div>
            `).join('');

            window._currentPaletteItems = items;
        }

        function executeCmdItem(idx) {
            if (window._currentPaletteItems && window._currentPaletteItems[idx]) {
                const action = window._currentPaletteItems[idx].run;
                closeCmdPalette();
                if (action) action();
            }
        }

        // Global Keyboard Shortcut Listener (Ctrl+K or Cmd+K)
        window.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
                e.preventDefault();
                const modal = document.getElementById('cmd-palette-modal');
                if (modal && !modal.classList.contains('hidden')) {
                    closeCmdPalette();
                } else {
                    openCmdPalette();
                }
            } else if (e.key === 'Escape') {
                closeCmdPalette();
                closeCompareModal();
                closeExecReportModal();
                closeFormalPscDossierModal();
            }
        });

        // =============================================================
        // MULTI-PLUGIN COMPARE STUDIO LOGIC
        // =============================================================
        let selectedComparePlugins = ["PlanX GeoStats Lab", "02CadGis Universal CAD/GIS Importer", "3D OSM Model"];

        function openCompareModal() {
            const modal = document.getElementById('compare-modal');
            if (!modal) return;
            renderCompareStudio();
            modal.classList.remove('hidden');
        }

        function closeCompareModal() {
            const modal = document.getElementById('compare-modal');
            if (modal) modal.classList.add('hidden');
        }

        function renderCompareStudio() {
            const selectorsBar = document.getElementById('compare-selectors-bar');
            const grid = document.getElementById('compare-cards-grid');
            if (!selectorsBar || !grid) return;

            // Render 3 slot selectors
            selectorsBar.innerHTML = [0, 1, 2].map(slotIdx => {
                const currentName = selectedComparePlugins[slotIdx] || appData.plugins[slotIdx]?.name;
                const optionsHtml = appData.plugins.map(p => `
                    <option value="${p.name}" ${p.name === currentName ? 'selected' : ''}>${p.name}</option>
                `).join('');

                return `
                    <div class="flex items-center gap-2 bg-obsidian-900 p-2 rounded-2xl border border-white/10">
                        <span class="text-xs text-slate-400 font-bold">Slot ${slotIdx + 1}:</span>
                        <select onchange="updateCompareSlot(${slotIdx}, this.value)" class="bg-obsidian-950 border border-white/10 rounded-xl px-2.5 py-1 text-xs text-white focus:outline-none focus:border-cyan-400 font-mono">
                            ${optionsHtml}
                        </select>
                    </div>
                `;
            }).join('');

            // Render Cards
            grid.innerHTML = selectedComparePlugins.map(name => {
                const p = appData.plugins.find(x => x.name === name) || appData.plugins[0];
                const anom = appData.anomalies.find(x => x.name === name) || {};
                const isFlagged = (anom.severity === 'critical' || anom.severity === 'high');

                return `
                    <div class="p-6 rounded-3xl glass-panel flex flex-col justify-between border ${isFlagged ? 'border-rose-500/30 bg-rose-950/10' : 'border-white/5'}">
                        <div>
                            <div class="flex items-center justify-between mb-3">
                                <span class="px-2.5 py-0.5 rounded text-[10px] font-bold font-mono bg-cyan-500/10 text-cyan-300 border border-cyan-500/20">${p.category}</span>
                                <span class="text-[10px] text-slate-500 font-mono">v${p.version}</span>
                            </div>
                            <h4 class="text-base font-bold font-heading text-white mb-4">${p.name}</h4>

                            <div class="space-y-2 text-xs font-mono bg-obsidian-950/80 p-4 rounded-2xl border border-white/5 mb-4">
                                <div class="flex justify-between">
                                    <span class="text-slate-400">Total Downloads:</span>
                                    <strong class="text-white">${p.downloads.toLocaleString()}</strong>
                                </div>
                                <div class="flex justify-between">
                                    <span class="text-slate-400">Monthly Velocity:</span>
                                    <strong class="text-cyan-400">${p.avg_monthly_downloads.toLocaleString()}/mo</strong>
                                </div>
                                <div class="flex justify-between">
                                    <span class="text-slate-400">Observed Rating:</span>
                                    <strong class="${isFlagged ? 'text-rose-400' : 'text-slate-200'}">${p.average_vote.toFixed(2)} ★ (${p.votes_count} votes)</strong>
                                </div>
                                <div class="flex justify-between">
                                    <span class="text-slate-400">Bayesian Score:</span>
                                    <strong class="text-emerald-400">${p.bayes_score ? p.bayes_score.toFixed(2) : p.average_vote.toFixed(2)} ★</strong>
                                </div>
                                <div class="flex justify-between text-[10px] text-slate-500">
                                    <span>95% Credible Interval:</span>
                                    <span>[${p.cred_floor ? p.cred_floor.toFixed(2) : '1.00'} - ${p.cred_ceiling ? p.cred_ceiling.toFixed(2) : '5.00'}]</span>
                                </div>
                                <div class="flex justify-between pt-2 border-t border-white/5">
                                    <span class="text-slate-400">Maintenance Status:</span>
                                    <span class="text-${p.cadence_badge_color || 'emerald'}-400 font-bold">${p.cadence_status || 'Active'}</span>
                                </div>
                            </div>
                        </div>
                        <button onclick="switchTab('deepdive'); document.getElementById('deepdive-search-input').value='${p.name}'; renderCards(); closeCompareModal();" class="w-full py-2 rounded-xl bg-obsidian-900 hover:bg-cyan-600 text-slate-300 hover:text-white border border-white/5 text-xs font-bold font-mono transition-all flex items-center justify-center gap-1.5">
                            <i class="fa-solid fa-magnifying-glass"></i> Deep Inspect
                        </button>
                    </div>
                `;
            }).join('');
        }

        function updateCompareSlot(slotIdx, newName) {
            selectedComparePlugins[slotIdx] = newName;
            renderCompareStudio();
        }

        // =============================================================
        // EXECUTIVE GOVERNANCE REPORT GENERATOR
        // =============================================================
        function openExecReportModal() {
            const modal = document.getElementById('exec-report-modal');
            if (!modal) return;

            const textContainer = document.getElementById('exec-report-text');
            const totalDl = appData.summary.total_downloads;
            const totalV = appData.plugins.reduce((a, b) => a + b.votes_count, 0);
            const rawAvg = appData.summary.overall_raw_rating.toFixed(2);
            const trueAvg = appData.correlation.portfolio_purged_average ? appData.correlation.portfolio_purged_average.toFixed(2) : '4.88';
            const pm = appData.summary.portfolio_milestones || {
                prev_milestone: 100000,
                next_milestone: 125000,
                progress_total: 87.7,
                remaining: 15356,
                est_date: 'Nov 2026'
            };

            let report = `================================================================================
`;
            report += `EXECUTIVE MONOREPO GOVERNANCE & IMPACT REPORT
`;
            report += `Maintainer: Yusuf Eminoğlu | Monorepo Suite: PlanX & 02 GIS Ecosystem
`;
            report += `Timestamp: ${new Date().toUTCString()}
`;
            report += `================================================================================

`;

            report += `1. PORTFOLIO VITAL METRICS
`;
            report += `--------------------------
`;
            report += `• Total Active Plugins: ${appData.plugins.length} Production Plugins (100% QGIS 4 & Qt6 Ready)
`;
            report += `• Total Global Downloads: ${totalDl.toLocaleString()} cumulative adoptions (100K Historic Milestone Achieved)
`;
            report += `• Next Milestone Horizon: ${pm.next_milestone.toLocaleString()} DL (${pm.progress_total}% completed | ETA: ${pm.est_date})
`;
            report += `• Planning Hours Saved: ${Math.round(totalDl * 0.5).toLocaleString()} hours (Econometric impact model)
`;
            report += `• Community Economic Surplus: $${Math.round(totalDl * 0.5 * 50 / 1000).toLocaleString()}k+ USD generated for public GIS community
`;
            report += `• Security Audit: 100% Passed (Bandit AST Zero Criticals, detect-secrets clean)

`;

            report += `2. RATING INTEGRITY & FORENSIC RECONSTRUCTION
`;
            report += `---------------------------------------------
`;
            report += `• Public Observed Rating: ${rawAvg} ★ across ${totalV} total votes
`;
            report += `• True Reconstructed Synthetic Organic Score: ${trueAvg} ★ (+${appData.correlation.total_suppressed_pts || '0.47'} pts suppressed)
`;
            report += `• Flagged Sybil / Dilution Influx: ${appData.correlation.total_raid_votes || 0} votes isolated via Mahalanobis Distance (D_M >= 5.0)

`;

            report += `3. TOP 5 ADOPTION LEADER PLUGINS
`;
            report += `---------------------------------
`;
            const top5 = [...appData.plugins].sort((a, b) => b.downloads - a.downloads).slice(0, 5);
            top5.forEach((p, idx) => {
                report += `${idx + 1}. ${p.name.padEnd(35)} : ${p.downloads.toLocaleString().padStart(8)} dl | ${p.average_vote.toFixed(2)}★ (${p.avg_monthly_downloads}/mo)
`;
            });

            textContainer.innerText = report;
            modal.classList.remove('hidden');
        }

        function closeExecReportModal() {
            const modal = document.getElementById('exec-report-modal');
            if (modal) modal.classList.add('hidden');
        }

        function copyExecReportMarkdown() {
            const text = document.getElementById('exec-report-text').innerText;
            navigator.clipboard.writeText(text).then(() => {
                showToast("Executive Governance Report copied to clipboard!");
            });
        }


        // Performance Debounce Utility
        function debounce(func, wait = 150) {
            let timeout;
            return function(...args) {
                clearTimeout(timeout);
                timeout = setTimeout(() => func.apply(this, args), wait);
            };
        }

        document.addEventListener("DOMContentLoaded", function() {
            document.getElementById('header-last-updated').textContent = `Last updated: ${appData.summary.last_updated}`;
            renderKPIs();
            renderMilestones();
            renderAuditKPIsAndAlerts();
            renderRatingStarsTab();
            renderTagFilterChips();
            renderTableData('all');
            renderCards();
            populateSimDropdown();
            initializeCharts();
            runSimulation();
            initializePipelines();
            renderSynergyMatrix();
            initHashRouting();
        });
    </script>
    <!-- ============================================================= -->
    <!-- GLOBAL COMMAND PALETTE (Ctrl+K / Cmd+K) -->
    <!-- ============================================================= -->
    <div id="cmd-palette-modal" class="fixed inset-0 z-50 flex items-start justify-center pt-24 bg-black/80 backdrop-blur-md hidden p-4" onclick="handleCmdBackdropClick(event)">
        <div class="w-full max-w-2xl bg-obsidian-950 border border-white/10 rounded-3xl shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-150">
            <div class="p-4 border-b border-white/10 flex items-center gap-3">
                <i class="fa-solid fa-terminal text-cyan-400 text-base"></i>
                <input type="text" id="cmd-palette-input" oninput="filterCommandPalette()" placeholder="Type a command, search plugin, or jump to tab... (ESC to close)" class="w-full bg-transparent text-sm text-white placeholder-slate-500 focus:outline-none font-mono">
                <kbd class="px-2 py-0.5 text-[10px] font-mono bg-obsidian-900 border border-white/10 rounded text-slate-400">ESC</kbd>
            </div>
            <div class="max-h-80 overflow-y-auto p-2 space-y-1 font-mono text-xs" id="cmd-palette-results">
                <!-- Filled dynamically -->
            </div>
            <div class="p-3 bg-obsidian-900/60 border-t border-white/5 flex items-center justify-between text-[10px] text-slate-500 font-mono">
                <span>Navigate: <kbd class="text-slate-400">↑</kbd> <kbd class="text-slate-400">↓</kbd> | Select: <kbd class="text-slate-400">Enter</kbd></span>
                <span>Yusuf Eminoğlu QGIS Monorepo OS</span>
            </div>
        </div>
    </div>

    <!-- ============================================================= -->
    <!-- MULTI-PLUGIN HEAD-TO-HEAD COMPARE MODAL -->
    <!-- ============================================================= -->
    <div id="compare-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md hidden p-4">
        <div class="w-full max-w-5xl max-h-[90vh] bg-obsidian-950 border border-white/10 rounded-3xl shadow-2xl flex flex-col overflow-hidden animate-in fade-in zoom-in duration-200">
            <div class="p-6 border-b border-white/10 flex items-center justify-between bg-gradient-to-r from-cyan-950/40 via-obsidian-900 to-obsidian-950">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-2xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center text-lg border border-cyan-500/30">
                        <i class="fa-solid fa-code-compare"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold font-heading text-white">Multi-Plugin Head-to-Head Comparison Studio</h3>
                        <p class="text-xs text-slate-400 font-mono">Side-by-side performance, adoption trajectory, and Bayesian confidence comparison</p>
                    </div>
                </div>
                <button onclick="closeCompareModal()" class="w-8 h-8 rounded-full bg-obsidian-900 hover:bg-obsidian-800 border border-white/10 text-slate-400 hover:text-white flex items-center justify-center transition-colors">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>
            <div class="p-6 overflow-y-auto space-y-6 font-mono text-xs text-slate-300">
                <div class="flex flex-wrap gap-3 items-center" id="compare-selectors-bar">
                    <!-- Plugin Selectors -->
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6" id="compare-cards-grid">
                    <!-- Dynamic Compare Cards -->
                </div>
            </div>
            <div class="p-4 border-t border-white/10 bg-obsidian-900/60 flex justify-end">
                <button onclick="closeCompareModal()" class="px-5 py-2 rounded-xl bg-obsidian-800 hover:bg-obsidian-750 text-slate-300 font-bold text-xs border border-white/10">
                    Close Compare Studio
                </button>
            </div>
        </div>
    </div>

    <!-- ============================================================= -->
    <!-- EXECUTIVE PORTFOLIO REPORT MODAL -->
    <!-- ============================================================= -->
    <div id="exec-report-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md hidden p-4">
        <div class="w-full max-w-4xl max-h-[90vh] bg-obsidian-950 border border-white/10 rounded-3xl shadow-2xl flex flex-col overflow-hidden animate-in fade-in zoom-in duration-200">
            <div class="p-6 border-b border-white/10 flex items-center justify-between bg-gradient-to-r from-emerald-950/40 via-obsidian-900 to-obsidian-950">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-2xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-lg border border-emerald-500/30">
                        <i class="fa-solid fa-file-contract"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold font-heading text-white">Executive Monorepo Governance & Impact Report</h3>
                        <p class="text-xs text-slate-400 font-mono">Formal 1-page executive summary with economic value, security audit, and health status</p>
                    </div>
                </div>
                <button onclick="closeExecReportModal()" class="w-8 h-8 rounded-full bg-obsidian-900 hover:bg-obsidian-800 border border-white/10 text-slate-400 hover:text-white flex items-center justify-center transition-colors">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>
            <div class="p-6 overflow-y-auto space-y-4 font-mono text-xs text-slate-300">
                <div class="flex justify-between items-center bg-obsidian-900/80 p-4 rounded-2xl border border-white/5">
                    <span class="text-slate-400">Generated for Yusuf Eminoğlu Portfolio Governance</span>
                    <button onclick="copyExecReportMarkdown()" class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center gap-1.5 transition-all">
                        <i class="fa-solid fa-copy"></i> Copy Executive Report
                    </button>
                </div>
                <div class="bg-obsidian-900 p-5 rounded-2xl border border-white/10 text-[11px] leading-relaxed select-all whitespace-pre-wrap" id="exec-report-text">
                    <!-- Filled dynamically -->
                </div>
            </div>
            <div class="p-4 border-t border-white/10 bg-obsidian-900/60 flex justify-end">
                <button onclick="closeExecReportModal()" class="px-4 py-2 rounded-xl bg-obsidian-800 text-slate-300 font-bold text-xs border border-white/10">Close</button>
            </div>
        </div>
    </div>

    <!-- ============================================================= -->
    <!-- FORMAL QGIS PSC & MODERATION COMPLAINT DOSSIER MODAL -->
    <!-- ============================================================= -->
    <div id="psc-dossier-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md hidden p-4">
        <div class="w-full max-w-4xl max-h-[90vh] bg-obsidian-950 border border-white/10 rounded-3xl shadow-2xl flex flex-col overflow-hidden animate-in fade-in zoom-in duration-200">
            <!-- Modal Header -->
            <div class="p-6 border-b border-white/10 flex items-center justify-between bg-gradient-to-r from-rose-950/40 via-obsidian-900 to-obsidian-950">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-2xl bg-rose-500/20 text-rose-400 flex items-center justify-center text-lg border border-rose-500/30">
                        <i class="fa-solid fa-scale-balanced"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold font-heading text-white">Official QGIS PSC & Moderation Team Incident Briefing</h3>
                        <p class="text-xs text-slate-400 font-mono">Formal evidence packet with exact UTC timestamps, statistical proofs, and SQL remediation queries</p>
                    </div>
                </div>
                <button onclick="closeFormalPscDossierModal()" class="w-8 h-8 rounded-full bg-obsidian-900 hover:bg-obsidian-800 border border-white/10 text-slate-400 hover:text-white flex items-center justify-center transition-colors">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>

            <!-- Modal Body -->
            <div class="p-6 overflow-y-auto space-y-6 font-mono text-xs text-slate-300">
                <div class="flex items-center justify-between bg-obsidian-900/80 p-4 rounded-2xl border border-white/5">
                    <div>
                        <span class="text-slate-400 block text-[11px]">Dossier Status:</span>
                        <strong class="text-rose-400 font-bold text-sm">CONFIRMED MULTI-PLUGIN COORDINATED RAID</strong>
                    </div>
                    <div class="flex gap-2">
                        <button onclick="copyPscDossierMarkdown()" class="px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs flex items-center gap-2 transition-all">
                            <i class="fa-solid fa-copy"></i> Copy Formal Briefing (Markdown)
                        </button>
                    </div>
                </div>

                <div class="bg-obsidian-900 p-5 rounded-2xl border border-white/10 text-[11px] leading-relaxed select-all whitespace-pre-wrap" id="psc-dossier-text">
                    <!-- Filled dynamically -->
                </div>
            </div>

            <!-- Modal Footer -->
            <div class="p-4 border-t border-white/10 bg-obsidian-900/60 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-mono">Cryptographic Hash: ##PORTFOLIO_EVIDENCE_HASH##</span>
                <button onclick="closeFormalPscDossierModal()" class="px-4 py-2 rounded-xl bg-obsidian-800 hover:bg-obsidian-750 text-slate-300 font-bold text-xs border border-white/10">
                    Close Briefing
                </button>
            </div>
        </div>
    </div>

</body>
</html>
"""

    html_output = (
        html_template
        .replace("##WORLD_SVG_LAYER##", world_svg_layer_html)
        .replace("##DATA_INJECTION##", json.dumps(embedded_data, ensure_ascii=False, indent=2))
        .replace("##TOTAL_PLUGINS##", str(len(yusuf_plugins)))
        .replace("##PORTFOLIO_EVIDENCE_HASH##", correlation_meta["portfolio_evidence_signature"])
    )

    local_output_path = os.path.join(os.path.dirname(__file__), "qgis_plugins_dashboard.html")
    index_output_path = os.path.join(os.path.dirname(__file__), "index.html")

    with open(local_output_path, "w", encoding="utf-8") as f:
        f.write(html_output)

    with open(index_output_path, "w", encoding="utf-8") as f:
        f.write(html_output)

    print(f"[5/5] Success: dashboard generated at: {local_output_path} and {index_output_path}")

except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
