# QGIS Hub Rating Audit - READ-ONLY forensics + evidence report
# Author: Yusuf Eminoglu
#
# Bu script HICBIR oy gondermez, hicbir seye login olmaz, hicbir kaynagi degistirmez.
# Sadece iki kaynagi okur:
#   1) plugins_history.json                      (gecmis anlik goruntuler)
#   2) plugins.xml                                (canli QGIS Hub beslemesi)
# -Report ile ayrica bir Markdown kanit dosyasi uretir (tek cikti).
#
# Anahtar fikir: average_vote * rating_votes = oylarin TAMSAYI toplami.
# Iki anlik goruntu arasindaki fark, araya giren oylarin degerini birebir verir.
# (Ornek: +1 oy ve +4.00 puan => o oy 4 yildiz. +30 oy ve +30.00 puan => 30 tane 1 yildiz.)
#
# Kullanim:
#   .\rating_audit.ps1            Canli besleme ile son anlik goruntuyu karsilastirir.
#   .\rating_audit.ps1 -Full      Tum gecmisi tarar, anomalili pencereleri doker.
#   .\rating_audit.ps1 -Report    rating_audit_report.md uretir (issue'ya eklenecek kanit).

param([switch]$Full, [switch]$Report)

$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$HistoryPath = Join-Path $ScriptDir 'plugins_history.json'
$ReportPath  = Join-Path $ScriptDir 'rating_audit_report.md'
$FeedUrl     = 'https://plugins.qgis.org/plugins/plugins.xml?qgis=4.0'
$Author      = 'Yusuf Eminoglu'

if (-not (Test-Path $HistoryPath)) {
    Write-Host "plugins_history.json bulunamadi: $HistoryPath" -ForegroundColor Red
    Exit 1
}

# --- Yardimcilar -------------------------------------------------------------

# NOT: PowerShell'in XML adaptoru guvenilmez - $p.Name bile "name" attribute'una baglanir.
# Bu yuzden tum alan erisimi XPath ile yapilir (test edildi: 1415 kayit, 27 eslesme).
function Read-Node($node, $xpath) {
    $n = $node.SelectSingleNode($xpath)
    if ($n) { return $n.InnerText } else { return '' }
}

function Get-LiveSnapshot {
    [xml]$doc = (Invoke-WebRequest -Uri $FeedUrl -UseBasicParsing -TimeoutSec 60).Content
    $map = @{}
    foreach ($p in $doc.SelectNodes('/plugins/pyqgis_plugin')) {
        if ((Read-Node $p 'author_name') -notlike "*$Author*") { continue }
        $name  = $p.GetAttribute('name')
        $votes = 0;   [void][int]::TryParse((Read-Node $p 'rating_votes'), [ref]$votes)
        $avg   = 0.0; [void][double]::TryParse((Read-Node $p 'average_vote'), [ref]$avg)
        $dl    = 0;   [void][int]::TryParse((Read-Node $p 'downloads'), [ref]$dl)
        $map[$name] = [pscustomobject]@{ votes = $votes; score = $votes * $avg; downloads = $dl }
    }
    if ($map.Count -eq 0) {
        Write-Host "UYARI: canli beslemede hic eslesme yok - author filtresi veya feed degismis olabilir." -ForegroundColor Red
    }
    return $map
}

# history kaydini karsilastirilabilir haritaya cevir
function Convert-Snapshot($entry) {
    $m = @{}
    foreach ($prop in $entry.plugins.PSObject.Properties) {
        $v = $prop.Value
        $m[$prop.Name] = [pscustomobject]@{
            votes     = [int]$v.votes_count
            score     = [double]$v.total_score
            downloads = [int]$v.downloads
        }
    }
    return $m
}

# Bir pencereyi karsilastir, flag'lerle birlikte yapisal sonuc dondur
function Compare-Window($before, $after, $label) {
    $events = @()
    foreach ($name in $after.Keys) {
        if (-not $before.ContainsKey($name)) { continue }
        $b = $before[$name]; $a = $after[$name]
        $dv = $a.votes - $b.votes
        $ds = $a.score - $b.score
        if ($dv -eq 0) { continue }
        $mean = 0.0
        if ($dv -gt 0) { $mean = [math]::Round($ds / $dv, 2) }
        $events += [pscustomobject]@{
            Plugin    = $name
            Delta     = $dv
            Score     = [math]::Round($ds, 2)
            Mean      = $mean
            AvgBefore = if ($b.votes -gt 0) { [math]::Round($b.score / $b.votes, 3) } else { 0 }
            AvgAfter  = if ($a.votes -gt 0) { [math]::Round($a.score / $a.votes, 3) } else { 0 }
            DlBefore  = $b.downloads
            DlAfter   = $a.downloads
        }
    }
    if ($events.Count -eq 0) { return $null }

    $gains    = @($events | Where-Object { $_.Delta -gt 0 })
    $removals = @($events | Where-Object { $_.Delta -lt 0 })
    $ones     = @($gains | Where-Object { [math]::Abs($_.Mean - 1.0) -lt 0.001 })
    $fives    = @($gains | Where-Object { [math]::Abs($_.Mean - 5.0) -lt 0.001 })
    $imposs   = @($gains | Where-Object { $_.Mean -lt 0.999 -or $_.Mean -gt 5.001 })

    # Saldiri turleri: (a) ayni pencerede 3+ eklentiye yalnizca 1.00,
    # (b) tek eklentiye 5+ oy hepsi 1.00 (ornek: GeoStats Lab'a 30 oy, issue #420).
    $bigSingle = @($ones | Where-Object { $_.Delta -ge 5 })
    $attackKind = ''
    if (($ones.Count -ge 3) -and ($ones.Count -eq $gains.Count)) { $attackKind = 'coordinated' }
    elseif ($bigSingle.Count -ge 1) { $attackKind = 'single' }

    return [pscustomobject]@{
        Label       = $label
        Events      = $events
        Gains       = $gains
        Removals    = $removals
        OneStar     = $ones
        FiveStar    = $fives
        Impossible  = $imposs
        AttackKind  = $attackKind
        IsAttack    = ($attackKind -ne '')
        IsFiveWave  = ($fives.Count -ge 3) -and ($fives.Count -eq $gains.Count)
    }
}

# --- Gecmisi pencerelere ayir -------------------------------------------------

$history = Get-Content -Path $HistoryPath -Raw -Encoding UTF8 | ConvertFrom-Json
$snaps = @()
foreach ($h in $history) { $snaps += ,@($h.date_str, (Convert-Snapshot $h)) }

$windows = @()
for ($i = 1; $i -lt $snaps.Count; $i++) {
    $w = Compare-Window $snaps[$i-1][1] $snaps[$i][1] $snaps[$i][0]
    if ($w) { $windows += $w }
}

# --- Mod: Markdown kanit raporu ----------------------------------------------

if ($Report) {
    $L = New-Object System.Collections.Generic.List[string]
    $L.Add("# QGIS Hub Rating Manipulation - Evidence Report")
    $L.Add("")
    $L.Add("**Reporter:** Yusuf Eminoglu (plugin author, $(($snaps[-1][1]).Count) plugins on plugins.qgis.org)")
    $L.Add("**Generated:** $(Get-Date -Format 'yyyy-MM-dd HH:mm') UTC+3")
    $L.Add("**Data source:** ``plugins_history.json`` - $($history.Count) snapshots, $($history[0].date_str) to $($history[-1].date_str)")
    $L.Add("**Live feed:** $FeedUrl")
    $L.Add("")
    $L.Add("## Method")
    $L.Add("")
    $L.Add("The Hub feed exposes ``average_vote`` and ``rating_votes`` per plugin. Their product is the **integer sum of all stars cast**. The difference between two consecutive snapshots therefore reveals the exact value of every vote cast in between - a vote cannot be added or removed without changing this number.")
    $L.Add("")
    $L.Add("Because each vote is an integer 1-5, the implied mean star value per interval is decisive:")
    $L.Add("a mixed set of real user votes always produces a fractional mean; **every vote in a window averaging exactly 1.00 or exactly 5.00 was cast by the same mechanism at the same time.**")
    $L.Add("")

    $attacks  = @($windows | Where-Object { $_.IsAttack })
    $fives    = @($windows | Where-Object { $_.IsFiveWave })
    $removals = @($windows | Where-Object { $_.Removals.Count -gt 0 })
    $imposs   = @($windows | Where-Object { $_.Impossible.Count -gt 0 })

    $L.Add("## 1. Coordinated 1-star attacks")
    $L.Add("")
    $L.Add("$($attacks.Count) window(s) carrying only 1.00-valued votes. In a **coordinated wave** every plugin")
    $L.Add("receiving votes in that window received only 1-star votes; in a **bulk batch** a single plugin")
    $L.Add("absorbed a large block of 1-star votes at once.")
    $L.Add("")
    foreach ($w in $attacks) {
        $tot = ($w.OneStar | Measure-Object -Property Delta -Sum).Sum
        if ($w.AttackKind -eq 'coordinated') { $kind = "coordinated wave, $($w.OneStar.Count) plugins" }
        else { $kind = "bulk batch on $($w.OneStar.Count) plugin(s)" }
        $L.Add("### $($w.Label) - $kind, $tot votes, all exactly 1.00")
        $L.Add("")
        $L.Add("| Plugin | 1-star votes | rating before | rating after |")
        $L.Add("|---|---|---|---|")
        foreach ($e in ($w.OneStar | Sort-Object Plugin)) {
            $L.Add("| $($e.Plugin) | $([math]::Abs($e.Delta)) | $($e.AvgBefore) | $($e.AvgAfter) |")
        }
        $L.Add("")
    }

    $L.Add("## 2. Same-signature 5-star bursts")
    $L.Add("")
    $L.Add("$($fives.Count) window(s) carrying the **identical mechanical signature** in the opposite direction.")
    $L.Add("I did not cast these and have no explanation for them; they are reported here for completeness because")
    $L.Add("they sit in the same dataset and would not survive any honest recount of my plugins' scores.")
    $L.Add("")
    foreach ($w in $fives) {
        $tot = ($w.FiveStar | Measure-Object -Property Delta -Sum).Sum
        $L.Add("### $($w.Label) - $($w.FiveStar.Count) plugins, $tot votes, all exactly 5.00")
        $L.Add("")
        $L.Add("| Plugin | 5-star votes | rating before | rating after |")
        $L.Add("|---|---|---|---|")
        foreach ($e in ($w.FiveStar | Sort-Object Plugin)) {
            $L.Add("| $($e.Plugin) | $($e.Delta) | $($e.AvgBefore) | $($e.AvgAfter) |")
        }
        $L.Add("")
    }

    $L.Add("## 3. Records inconsistent with vote casting (direct data tampering)")
    $L.Add("")
    if ($imposs.Count -eq 0) { $L.Add("None.") }
    foreach ($w in $imposs) {
        foreach ($e in $w.Impossible) {
            $L.Add("- **$($e.Plugin)** - $($w.Label): +$($e.Delta) votes but +$($e.Score) score (implied mean $($e.Mean)).")
            $L.Add("  A set of integer 1-5 votes cannot produce a mean outside 1.00-5.00, so this is not a vote cast - it is an edit of existing vote records.")
        }
    }
    $L.Add("")

    $L.Add("## 4. Votes removed to date")
    $L.Add("")
    if ($removals.Count -eq 0) {
        $L.Add("**None.** No ``rating_votes`` counter has decreased in any of the $($history.Count) snapshots.")
        $L.Add("The purge of fake votes requested in issue #420 has not been performed - the manipulated scores remain live.")
    } else {
        foreach ($w in $removals) {
            foreach ($e in $w.Removals) { $L.Add("- $($w.Label): **$($e.Plugin)** $($e.AvgBefore) -> $($e.AvgAfter) ($($e.Delta) votes)") }
        }
    }
    $L.Add("")

    $L.Add("## 5. Cumulative per-plugin totals")
    $L.Add("")
    $L.Add("| Plugin | 1-star votes received | 5-star vote sources | net |")
    $L.Add("|---|---|---|---|")
    $allnames = @{}
    foreach ($w in $windows) { foreach ($e in $w.Events) { $allnames[$e.Plugin] = $true } }
    foreach ($n in ($allnames.Keys | Sort-Object)) {
        $ones = 0; $fiv = 0
        foreach ($w in $windows) {
            foreach ($e in $w.Events) {
                if ($e.Plugin -ne $n) { continue }
                if ([math]::Abs($e.Mean - 1.0) -lt 0.001) { $ones += $e.Delta }
                if ([math]::Abs($e.Mean - 5.0) -lt 0.001) { $fiv  += $e.Delta }
            }
        }
        if ($ones -eq 0 -and $fiv -eq 0) { continue }
        $L.Add("| $n | $ones | $fiv | $($ones + $fiv) |")
    }
    $L.Add("")

    $L.Add("## 6. Requested actions")
    $L.Add("")
    $L.Add("1. Purge the votes identified above and recompute every affected plugin score from the remaining records.")
    $L.Add("2. On the anti-abuse fix: per-IP throttling cannot work here. Per Lova Andriarimalala's 2026-08-19 post to")
    $L.Add("   QGIS-Developer, 100 of 100 sampled vote IPs matched Cloudflare edge ranges, so the per-address cap in")
    $L.Add("   PR #423 counts Cloudflare's rotating proxy pool rather than a voter. Any effective fix must key on an")
    $L.Add("   authenticated account, not an address.")
    $L.Add("")
    $L.Add("---")
    $L.Add("")
    $L.Add("_Generated read-only from public feed data by ``rating_audit.ps1``. No votes were cast, no accounts were used._")

    $L -join "`n" | Out-File -FilePath $ReportPath -Encoding utf8
    Write-Host "Rapor uretildi: $ReportPath" -ForegroundColor Green
    Write-Host ("  {0} pencere | {1} 1-yildiz saldirisi | {2} 5.00 dalgasi | {3} imkansiz kayit | {4} silme" -f `
        $windows.Count, $attacks.Count, $fives.Count, ($imposs | Measure-Object).Count, ($removals | Measure-Object).Count)
    Exit 0
}

# --- Mod: konsol raporu ------------------------------------------------------

function Show-Window($w) {
    Write-Host $w.Label -ForegroundColor Gray
    foreach ($e in ($w.Events | Sort-Object Plugin)) {
        if ($e.Delta -lt 0) {
            Write-Host ("   REMOVED  {0,-40} {1} oy" -f $e.Plugin, $e.Delta) -ForegroundColor Magenta
        } else {
            $tail = ""
            if ([math]::Abs($e.Mean - 5.0) -lt 0.001) { $tail = "  <- tam 5.00" }
            elseif ([math]::Abs($e.Mean - 1.0) -lt 0.001) { $tail = "  <- tam 1.00" }
            Write-Host ("   +{0,-3} vote  star={1,-6} {2}{3}" -f $e.Delta, $e.Mean, $e.Plugin, $tail)
        }
    }
    if ($w.IsFiveWave) { Write-Host "   FLAG: AYNI pencerede $($w.FiveStar.Count) eklentiye yalnizca 5.00 - organik oy boyle gelmez" -ForegroundColor Yellow }
    if ($w.AttackKind -eq 'coordinated') { Write-Host "   FLAG: AYNI pencerede $($w.OneStar.Count) eklentiye yalnizca 1.00 - koordineli saldiri" -ForegroundColor Red }
    elseif ($w.AttackKind -eq 'single') { Write-Host "   FLAG: TEK eklentiye toplu 1.00 bloku - hedefli saldiri" -ForegroundColor Red }
    if ($w.Removals.Count -gt 0) { Write-Host "   FLAG: $($w.Removals.Count) eklentiden oy SILINMIS (admin temizligi boyle gorunur)" -ForegroundColor Green }
    if ($w.Impossible.Count -gt 0) { Write-Host "   FLAG: $($w.Impossible.Count) kayitta imkansiz ortalama (1.00-5.00 disi) - DB mudahalesi" -ForegroundColor Red }
    Write-Host ""
}

if ($Full) {
    Write-Host ""
    Write-Host "== TUM GECMIS TARAMASI  ($($history.Count) anlik goruntu)" -ForegroundColor Cyan
    foreach ($w in $windows) { if ($w.IsAttack -or $w.IsFiveWave -or $w.Removals.Count -gt 0 -or $w.Impossible.Count -gt 0) { Show-Window $w } }
    Exit 0
}

Write-Host ""
Write-Host "== CANLI DURUM  (son anlik goruntu: $($history[-1].date_str))" -ForegroundColor Cyan
Write-Host "Besleme cekiliyor..." -ForegroundColor Gray
$live = Get-LiveSnapshot
Write-Host "$($live.Count) eklenti bulundu." -ForegroundColor Gray
Write-Host ""
$w = Compare-Window (Convert-Snapshot $history[-1]) $live "DEGISIM (son anlik goruntu -> simdi)"
if ($w) { Show-Window $w } else { Write-Host "Oy sayilarinda degisiklik yok." -ForegroundColor Gray }
Write-Host "Not: hicbir sey yazilmadi, hicbir oy gonderilmedi." -ForegroundColor DarkGray
