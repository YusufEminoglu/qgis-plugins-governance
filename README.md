# Geophilo QGIS Plugins dashboard

Downloads, releases and reach of the Geophilo plugins on the QGIS Plugin Hub, rebuilt every day.

**Live:** https://geophilo.com/governance/ · **QGIS Hub:** https://plugins.qgis.org/plugins/author/Geophilo/

## What it shows

- All-time downloads, downloads in the last 30 and 7 days (with the change against the previous 30 days), releases and countries reached.
- Downloads per week across all plugins, and the share of each suite (PlanX, 02, standalone).
- Every plugin with its version and Hub date, total and 30-day downloads, a 30-day trend line, the supported QGIS range and links to the Hub page, the manual on geophilo.com and the source.
- The ten most downloaded plugins of the last 30 days and the releases of the last 60 days.
- Downloads by country on a world map, with the leading countries listed.

## Where the numbers come from

| Figure | Source |
|---|---|
| Version, total downloads, dates, QGIS range, links | `https://plugins.qgis.org/plugins/plugins.xml?qgis=4.0` |
| Downloads per day and week, releases | `plugins_history.json`: one snapshot of plugins.xml per day, appended by every run |
| Downloads per country | The Hub's public download statistics (Metabase), recorded since 2024-05-30 |

Nothing is estimated: when a source does not answer, the dashboard says the figure is unavailable. Plugins are
matched by author (Geophilo) and stored under their Hub package name, which never changes, so renaming a plugin on
the Hub does not break its history.

## Build

```bash
python generate_dashboard.py      # writes index.html, qgis_plugins_dashboard.html and appends plugins_history.json
```

The page layout lives in `dashboard_template.html`; the script injects the data and the world map into it.
The GitLab schedule (`.gitlab-ci.yml`) runs the same command once a day, commits the three files and deploys the page.

`archive/` keeps the 2026 rating-abuse investigation (report, audit script). The Hub no longer shows ratings, so the
dashboard no longer tracks them.

## License

MIT · Geophilo
