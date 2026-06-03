# 每日個股資訊網站

每日更新的台股個股資訊靜態網站。合作夥伴每天產出 Excel 檔，`build.py` 會把它們轉成精簡的靜態網站資料，發佈到 Cloudflare Pages（需登入）。

**沒有後端、沒有資料庫、沒有前端框架** —— 前端是手寫的 HTML + 原生 JavaScript，直接讀取事先產生好的資料檔。

🔗 **線上網站**：https://stock-daily-s6v.pages.dev/ （需透過 Cloudflare Access 登入）

<p align="left">
  <img src="stock-daily-qrcode.png" width="160" alt="網站 QR Code">
</p>

---

## 網站內容

| 分頁 | 說明 |
| --- | --- |
| **大盤放量訊號** | 當日放量、量能延續、出關股、處置股等訊號表格（可搜尋、排序） |
| **勝率回測** | 放量訊號的歷史勝率回測圖表與表格 |
| **個股分析** | 各檔個股的價量走勢圖、券商買賣超明細、買賣家數等 |

上方可用日期下拉選單切換不同交易日的資料。

---

## 每日更新流程

1. 把當天的 Excel 檔放進新的 `data/YYYYMMDD/` 資料夾。
2. 執行 `python build.py`（只會處理尚未產生的日期）。
3. 執行 `node site/smoke.js site` 確認沒有渲染錯誤。
4. `git push` —— GitHub Actions 約 1 分鐘內自動重新發佈網站。

> 💡 在 Claude Code 中可直接用 `/更新網站` skill 一鍵完成上述步驟。

---

## 指令

```bash
# 從 Excel 重新產生網站資料（已產生的日期會跳過）
python build.py

# 強制重建所有日期（修改 build.py 邏輯後使用）
python build.py --force

# 無頭煙霧測試：用 DOM stub 跑 app.js，渲染每個日期/個股以抓出執行錯誤
node site/smoke.js site

# 本機預覽：直接用瀏覽器開啟 site/index.html 即可（支援 file://，免架伺服器）

# 發佈：commit + push 到 main，GitHub Actions 會自動重新部署 site/
git add -A && git commit -m "..." && git push
```

需求：Python 套件 `openpyxl`（解析 Excel）；煙霧測試需要 Node.js。

---

## 架構

兩段式管線：**Excel → (build.py) → site/data/\*.js → (靜態前端) → GitHub Pages**

### build.py（Excel → 資料檔）
- 掃描 `data/YYYYMMDD/` 資料夾，依檔名在 `classify()` 中分類：
  - `台股放量訊號*.xlsx` → 大盤訊號檔（多個工作表）
  - `{代號}*日報*.xlsx` → 個股券商買賣超前 20
  - `{代號}*分析結果*.xlsx` → 個股價量與券商明細
  - `{代號}*charts*.xlsx` → **不再使用**；6 張技術走勢圖改由前端 Chart.js 直接用券商買賣超資料即時繪製，不再抽出或存放 PNG
- 產生 `site/data/index.json` 索引（日期清單 + 每個日期有哪些個股），前端據此建立所有選單。
- **新增個股／日期不需改任何程式碼**，會自動偵測。個股顯示名稱可在 `stock_names.json`（代號→名稱）覆寫。

### .js 包裝檔的小技巧（重要）
`build.py` 會為每個 `.json` 另外產生一份 `.js` 副本，內容是呼叫 `window.__DATAREG(key, data)`。前端用注入 `<script>` 標籤的方式載入資料（而非 fetch），因此**直接用 `file://` 開啟也能運作，免架伺服器**。

> 線上實際使用的是 `.js` 檔；`.json` 為中間產物，已被 `site/.gitignore` 忽略。

### 前端（site/）
- `index.html` —— 三個分頁與日期下拉選單。
- `app.js` —— 原生 JS，透過 `__DATAREG` 載入器供應資料；用 Grid.js 畫表格、Chart.js 畫圖表。
- 第三方函式庫（Grid.js、Chart.js）由 CDN 載入。

### 部署
- `.github/workflows/pages.yml`（GitHub Actions）：push 到 `main` 時，把 `./site` 上傳為 Pages 產物並部署。
- `site/deploy.bat` 為**舊版**的替代部署方式，目前未使用。

---

## 注意事項

- **原始資料不會上傳**：根目錄 `data/`（原始 Excel，數十 MB）已被 git 忽略，只有處理後的 `site/data/` 會發佈。請在本機保留 `data/` 以便重建。
- **巢狀 git repo**：`site/.git` 是 `deploy.bat` 留下的殘留，與真正部署用的根目錄 repo 不同。請一律在 repo **根目錄** 執行 git 指令。
- Excel 解析靠 `find_header` 尋找含關鍵欄位（代號／分類／股價）的標題列；若來源檔版面改變，解析會靜默回傳空資料而非報錯。
