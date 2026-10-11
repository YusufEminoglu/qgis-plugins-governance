# QGIS Hub Rating Manipulation - Evidence Report

**Reporter:** Yusuf Eminoglu (plugin author, 29 plugins on plugins.qgis.org)
**Generated:** 2026-09-25 11:37 UTC+3
**Data source:** `plugins_history.json` - 144 snapshots, Aug 15, 2026 10:46 UTC+3 to Sep 16, 2026 00:09 UTC
**Live feed:** https://plugins.qgis.org/plugins/plugins.xml?qgis=4.0

## Method

The Hub feed exposes `average_vote` and `rating_votes` per plugin. Their product is the **integer sum of all stars cast**. The difference between two consecutive snapshots therefore reveals the exact value of every vote cast in between - a vote cannot be added or removed without changing this number.

Because each vote is an integer 1-5, the implied mean star value per interval is decisive:
a mixed set of real user votes always produces a fractional mean; **every vote in a window averaging exactly 1.00 or exactly 5.00 was cast by the same mechanism at the same time.**

## 1. Coordinated 1-star attacks

4 window(s) carrying only 1.00-valued votes. In a **coordinated wave** every plugin
receiving votes in that window received only 1-star votes; in a **bulk batch** a single plugin
absorbed a large block of 1-star votes at once.

### Aug 16, 2026 13:28 UTC - bulk batch on 1 plugin(s), 30 votes, all exactly 1.00

| Plugin | 1-star votes | rating before | rating after |
|---|---|---|---|
| PlanX GeoStats Lab | 30 | 4.846 | 3.174 |

### Aug 24, 2026 21:44 UTC - coordinated wave, 4 plugins, 51 votes, all exactly 1.00

| Plugin | 1-star votes | rating before | rating after |
|---|---|---|---|
| 02Agent OSM Downloader | 10 | 5 | 3.75 |
| 02CadGis Universal CAD/GIS Importer | 18 | 4.761 | 3.965 |
| OSM Quick 3D | 10 | 4.718 | 4.295 |
| PlanX CAD Toolset | 13 | 4.783 | 4.11 |

### Aug 26, 2026 11:53 UTC - bulk batch on 1 plugin(s), 10 votes, all exactly 1.00

| Plugin | 1-star votes | rating before | rating after |
|---|---|---|---|
| 3D OSM Model | 10 | 4.667 | 4.408 |

### Aug 30, 2026 08:54 UTC - bulk batch on 19 plugin(s), 68 votes, all exactly 1.00

| Plugin | 1-star votes | rating before | rating after |
|---|---|---|---|
| 02Agent Smart Modeler | 4 | 4.999 | 3.666 |
| 02GeoQuest - Playable Map Studio | 6 | 5 | 3.8 |
| 02-Multimap: Sync-up Multimaps | 4 | 4.4 | 4.263 |
| 02truesize - Map Truth Lab | 4 | 4.607 | 4.156 |
| 02Urban Portrait - City as a Face | 4 | 4.769 | 3.882 |
| EasyFillet | 5 | 5 | 4.13 |
| Parametric Process | 2 | 4.999 | 4 |
| ParcelFlux | 3 | 4.706 | 4.15 |
| PlanX | 3 | 4.443 | 4.317 |
| PlanX 3D City Viewer | 4 | 4.852 | 4.355 |
| PlanX CartoLab | 3 | 4.789 | 4.273 |
| PlanX DataCube Lab | 4 | 4.714 | 3.889 |
| PlanX Settlement Planning Toolset | 5 | 5 | 4 |
| PlanX Suitability Lab | 6 | 4.846 | 4.125 |
| PlanX Urban Procedural 3D | 2 | 4.555 | 3.909 |
| PlanX Uygulama İmar Planı (Master Plan) Toolset | 4 | 5 | 4.111 |
| PlanX: Urban Resilience | 3 | 4.432 | 4.175 |
| QGIS 2.5D Styling | 1 | 4.995 | 2.998 |
| SmartModeler GIS | 1 | 4.998 | 3.665 |

## 2. Same-signature 5-star bursts

5 window(s) carrying the **identical mechanical signature** in the opposite direction.
I did not cast these and have no explanation for them; they are reported here for completeness because
they sit in the same dataset and would not survive any honest recount of my plugins' scores.

### Aug 17, 2026 06:25 UTC - 6 plugins, 6 votes, all exactly 5.00

| Plugin | 5-star votes | rating before | rating after |
|---|---|---|---|
| 02Agent OSM Downloader | 1 | 4.999 | 5 |
| 02CadGis Universal CAD/GIS Importer | 1 | 4.711 | 4.717 |
| 02-Multimap: Sync-up Multimaps | 1 | 4.394 | 4.403 |
| 02viz - Geospatial Visualization Studio | 1 | 4.559 | 4.565 |
| PlanX | 1 | 4.362 | 4.371 |
| PlanX CAD Toolset | 1 | 4.74 | 4.745 |

### Aug 21, 2026 00:29 UTC - 12 plugins, 32 votes, all exactly 5.00

| Plugin | 5-star votes | rating before | rating after |
|---|---|---|---|
| 02Agent OSM Downloader | 2 | 5 | 5 |
| 02CadGis Universal CAD/GIS Importer | 3 | 4.746 | 4.758 |
| 02-Multimap: Sync-up Multimaps | 3 | 4.408 | 4.43 |
| 02viz - Geospatial Visualization Studio | 3 | 4.595 | 4.61 |
| 3D OSM Model | 3 | 4.648 | 4.656 |
| OSM Quick 3D | 3 | 4.69 | 4.703 |
| ParcelFlux | 1 | 4.643 | 4.666 |
| PlanX | 3 | 4.389 | 4.413 |
| PlanX CAD Toolset | 3 | 4.759 | 4.772 |
| PlanX GeoStats Lab | 3 | 3.301 | 3.368 |
| PlanX Suitability Lab | 2 | 4.809 | 4.826 |
| PlanX: Urban Resilience | 3 | 4.322 | 4.382 |

### Aug 21, 2026 18:18 UTC - 13 plugins, 14 votes, all exactly 5.00

| Plugin | 5-star votes | rating before | rating after |
|---|---|---|---|
| 02CadGis Universal CAD/GIS Importer | 1 | 4.758 | 4.762 |
| 02-Multimap: Sync-up Multimaps | 1 | 4.43 | 4.437 |
| 02truesize - Map Truth Lab | 1 | 4.541 | 4.56 |
| 02viz - Geospatial Visualization Studio | 1 | 4.61 | 4.615 |
| 3D OSM Model | 1 | 4.656 | 4.659 |
| OSM Quick 3D | 2 | 4.703 | 4.71 |
| Parametric Process | 1 | 4.999 | 4.999 |
| ParcelFlux | 1 | 4.666 | 4.687 |
| PlanX | 1 | 4.413 | 4.421 |
| PlanX CAD Toolset | 1 | 4.772 | 4.776 |
| PlanX GeoStats Lab | 1 | 3.368 | 3.39 |
| PlanX Suitability Lab | 1 | 4.826 | 4.833 |
| PlanX: Urban Resilience | 1 | 4.382 | 4.4 |

### Aug 25, 2026 12:20 UTC - 6 plugins, 6 votes, all exactly 5.00

| Plugin | 5-star votes | rating before | rating after |
|---|---|---|---|
| 02Agent OSM Downloader | 1 | 3.757 | 3.794 |
| 02CadGis Universal CAD/GIS Importer | 1 | 3.977 | 3.988 |
| 3D OSM Model | 1 | 4.664 | 4.667 |
| OSM Quick 3D | 1 | 4.295 | 4.303 |
| PlanX | 1 | 4.436 | 4.443 |
| PlanX GeoStats Lab | 1 | 3.43 | 3.45 |

### Sep 09, 2026 20:50 UTC - 6 plugins, 6 votes, all exactly 5.00

| Plugin | 5-star votes | rating before | rating after |
|---|---|---|---|
| 02Agent Smart Modeler | 1 | 3.714 | 3.8 |
| 02-Multimap: Sync-up Multimaps | 1 | 4.248 | 4.254 |
| PlanX | 1 | 4.309 | 4.318 |
| PlanX GeoStats Lab | 1 | 3.458 | 3.476 |
| PlanX Suitability Lab | 1 | 4.125 | 4.151 |
| SmartModeler GIS | 1 | 3.665 | 3.999 |

## 3. Records inconsistent with vote casting (direct data tampering)

- **PlanX GeoStats Lab** - Aug 20, 2026 10:03 UTC: +2 votes but +12 score (implied mean 6).
  A set of integer 1-5 votes cannot produce a mean outside 1.00-5.00, so this is not a vote cast - it is an edit of existing vote records.

## 4. Votes removed to date

**None.** No `rating_votes` counter has decreased in any of the 144 snapshots.
The purge of fake votes requested in issue #420 has not been performed - the manipulated scores remain live.

## 5. Cumulative per-plugin totals

| Plugin | 1-star votes received | 5-star vote sources | net |
|---|---|---|---|
| 02Agent OSM Downloader | 11 | 16 | 27 |
| 02Agent Smart Modeler | 4 | 9 | 13 |
| 02CadGis Universal CAD/GIS Importer | 18 | 22 | 40 |
| 02CartoLab | 2 | 5 | 7 |
| 02GeoQuest - Playable Map Studio | 6 | 3 | 9 |
| 02-Multimap: Sync-up Multimaps | 4 | 7 | 11 |
| 02Route 3D - Multi-Criteria 3D Mobility Studio | 0 | 2 | 2 |
| 02truesize - Map Truth Lab | 4 | 4 | 8 |
| 02Urban Portrait - City as a Face | 4 | 0 | 4 |
| 02viz - Geospatial Visualization Studio | 0 | 14 | 14 |
| 3D OSM Model | 12 | 14 | 26 |
| EasyFillet | 5 | 0 | 5 |
| OSM Quick 3D | 10 | 17 | 27 |
| Parametric Process | 2 | 1 | 3 |
| ParcelFlux | 3 | 4 | 7 |
| PlanX | 3 | 11 | 14 |
| PlanX 3D City Viewer | 4 | 0 | 4 |
| PlanX CAD Toolset | 13 | 10 | 23 |
| PlanX CartoLab | 3 | 1 | 4 |
| PlanX DataCube Lab | 4 | 0 | 4 |
| PlanX GeoStats Lab | 31 | 12 | 43 |
| PlanX Settlement Planning Toolset | 5 | 0 | 5 |
| PlanX Suitability Lab | 6 | 7 | 13 |
| PlanX Urban Procedural 3D | 2 | 1 | 3 |
| PlanX Uygulama İmar Planı (Master Plan) Toolset | 4 | 0 | 4 |
| PlanX: Urban Resilience | 3 | 8 | 11 |
| QGIS 2.5D Styling | 1 | 4 | 5 |
| SmartModeler GIS | 1 | 1 | 2 |

## 6. Requested actions

1. Purge the votes identified above and recompute every affected plugin score from the remaining records.
2. On the anti-abuse fix: per-IP throttling cannot work here. Per Lova Andriarimalala's 2026-08-19 post to
   QGIS-Developer, 100 of 100 sampled vote IPs matched Cloudflare edge ranges, so the per-address cap in
   PR #423 counts Cloudflare's rotating proxy pool rather than a voter. Any effective fix must key on an
   authenticated account, not an address.

---

_Generated read-only from public feed data by `rating_audit.ps1`. No votes were cast, no accounts were used._
