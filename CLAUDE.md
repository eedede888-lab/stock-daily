# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A daily stock-information website for Taiwan equities. A partner produces Excel files each day; `build.py` converts them into a compact static site under `site/`, which is published to GitHub Pages. There is no backend, database, or build framework — the front end is hand-written HTML + vanilla JS loading pre-generated data files.

Live site: https://tongwade.github.io/stock-daily/ — Repo: `tongwade/stock-daily`

## Commands

```bash
# Regenerate site data from Excel (skips already-built dates)
python build.py

# Force full rebuild of every date (use after changing build.py logic)
python build.py --force

# Headless smoke test: evals app.js against a DOM stub and renders every
# date/stock to catch runtime errors. Run from repo root:
node site/smoke.js site

# Local preview: just open site/index.html in a browser.
# It works over file:// (no server needed) — see the .js-wrapper note below.

# Deploy: commit + push to main; GitHub Actions redeploys site/ automatically.
git add -A && git commit -m "..." && git push
```

Python deps: `openpyxl` (Excel parsing). The smoke test needs Node.

## Daily update workflow

1. Drop the day's Excel files into a new `data/YYYYMMDD/` folder.
2. Run `python build.py` (it only processes dates not yet built).
3. Run `node site/smoke.js site` to confirm no render errors.
4. `git push` — Actions rebuilds Pages in ~1 min.

## Architecture

Two-stage pipeline: **Excel → (build.py) → site/data/*.js → (static front end) → GitHub Pages**.

### build.py (Excel → data files)
- Scans `data/YYYYMMDD/` folders. Files are classified by name in `classify()`:
  - `台股放量訊號*.xlsx` → market file (sheets: 今日放量訊號, 量能延續追蹤, 出關股追蹤, 處置股清單, 勝率回測) → `site/data/YYYYMMDD/market.json`
  - `{code}*日報*.xlsx` → per-stock broker buy/sell top-20 (買進前20, 賣出前20)
  - `{code}*分析結果*.xlsx` → per-stock price/volume + broker detail (買賣價量與家數, 券商明細, ~12k rows)
  - `{code}*charts*.xlsx` files are **ignored** — the 6 technical charts are now drawn live by Chart.js from the broker buy/sell/detail data, so no PNGs are extracted or stored.
- Per-stock output merged into `site/data/YYYYMMDD/{code}.json`.
- Generates `site/data/index.json` — the date list + which stocks each date has; the front end builds all menus from this.
- New stocks/dates need **no code changes** — they are auto-detected. Stock display names come from `stock_names.json` (code→name overrides), falling back to names in the market file.
- `SKIP_EXISTING` (default true; `--force` disables) skips dates whose output JSON already parses correctly.

### The .js wrapper trick (important)
`emit_js_wrappers()` writes a `.js` copy of every `.json` that calls `window.__DATAREG(key, data)`. The front end (`app.js` `loadData()`) loads data by injecting `<script src="data/KEY.js">` tags, **not** fetch — so the site works when opened directly via `file://` with no web server. Consequences:
- The deployed/used data files are the **`.js`** ones. The `.json` files are intermediate products and are git-ignored by `site/.gitignore` (`data/**/*.json`). Do not expect `data/index.json` to exist on the live site — use `data/index.js`.
- Any new data file produced by hand must follow the same `window.__DATAREG(...)` wrapper format.

### Front end (site/)
- `index.html` — three tab views: 大盤放量訊號 (market signals), 勝率回測 (win-rate backtest), 個股分析 (per-stock). A date `<select>` switches the active day across all views.
- `app.js` — vanilla JS. `cache`/`pending` registry feeds the `__DATAREG` loader. Renderers: `renderMarket` (Grid.js table), `renderWinrate` (Chart.js bar + tables), `renderStock`/`loadStock` (price/volume Chart.js, detail Grid.js), `renderBrokerCharts` (the 6 technical charts as live Chart.js bar+line plots built from `buy_top`/`sell_top`/`broker_detail`). When `app.js` changes, bump the `?v=` cache-buster on its `<script>` tag in `index.html`.
- Third-party libs (Grid.js, Chart.js) load from CDN via `<script>` in `index.html`.

### Deployment
- Active path: `.github/workflows/pages.yml` (GitHub Actions) uploads `./site` as the Pages artifact on push to `main`. Pages is configured with `build_type=workflow`. Pushing to `.github/workflows/` requires the gh token to have the `workflow` scope.
- `site/deploy.bat` is a **legacy** alternative (treats `site/` itself as a repo root, pushes, and uses classic branch-based Pages). Not used by the current setup.

## Gotchas

- **Nested git repo**: `site/.git` exists as a leftover from `deploy.bat`'s design, separate from the root repo that actually deploys. Run git commands from the repo **root** (`stock/`); git commands inside `site/` act on the stale nested repo and won't affect the live site.
- **Raw data is not deployed**: root `data/` (the source Excel, tens of MB) is git-ignored. Only the processed `site/data/` is published. Keep `data/` locally to allow rebuilds.
- Excel parsing relies on locating a header row containing a key column (代號 / 分類 / 股價) via `find_header`; if a source file's layout changes, parsing silently returns empty records rather than erroring.
