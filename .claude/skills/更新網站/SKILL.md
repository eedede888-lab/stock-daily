---
name: 更新網站
description: 重新產生網站資料並發佈到 Cloudflare Pages（Access 登入保護）。當使用者說「更新網站」「重新上線」「重新部署」「把新資料發佈出去」時使用。會偵測新資料、執行 build.py、跑煙霧測試、commit、（可選）push 備份原始碼，並用 wrangler 部署到 Cloudflare、驗證上線。
---

# 更新網站

一鍵把 `data/` 裡的新資料產生並發佈到 Cloudflare Pages：https://stock-daily-s6v.pages.dev/
（此站受 Cloudflare Access 保護，需登入才看得到內容。）

## 前置確認
- 一律在 repo **根目錄** `D:\Users\2205\Desktop\main\AI_Project\stock` 執行（不要進到 `site/`，那裡有殘留的巢狀 git repo）。
- 確認 `python`、`node` 可用；`npx wrangler` 已用 `wrangler login` 登入過（OAuth token 存在本機）。

## 步驟

1. **產生資料**
   ```bash
   python build.py
   ```
   只會處理尚未建好的日期。若使用者明確要求重建全部（例如改過 build.py 邏輯），改用 `python build.py --force`。

2. **煙霧測試**（確認沒有渲染錯誤）
   ```bash
   node site/smoke.js site
   ```
   若有錯誤就停下來回報，不要硬推上線。

3. **檢視變更並提交**（原始碼版本備份；注意：GitHub Pages 已停用，push 不會自動部署）
   ```bash
   git status
   git add -A
   git commit -m "更新個股資料：<簡述新增的日期/個股>"
   ```
   commit 訊息請反映實際變更（新增了哪些日期/個股）。

4. **推送備份**（可選，需要使用者同意才 push）
   ```bash
   git push
   ```
   GitHub Pages 的自動部署 workflow 已停用，push 只是把原始碼/已建好的 `site/data` 推上 GitHub 做版本備份，不會發佈網頁。

5. **部署到 Cloudflare Pages**（這一步才是真正發佈）
   ```bash
   npx wrangler pages deploy site --project-name stock-daily
   ```
   會把整個 `site/` 目錄上傳（Direct Upload）。成功時 wrangler 會印出本次部署網址。

6. **驗證部署**
   ```bash
   curl -sI https://stock-daily-s6v.pages.dev/ | head -5
   ```
   因為有 Access 保護，**未登入應回 302** 並轉址到 Cloudflare 登入頁——看到 302 同時代表「已上線」且「保護仍生效」。若回 200 直接看到內容，代表 Access 沒生效，要回報。
   要確認新資料是否上線，可在瀏覽器登入後開站查看；或部署成功的 wrangler 輸出本身即為佐證。

## 注意
- 原始 `data/` 不會進 git（已 git-ignore），只有處理後的 `site/data/` 會被部署。
- 正式站是 **Cloudflare Pages（Direct Upload，專案名 `stock-daily`）**，沒有跟 GitHub 連動，所以一定要跑步驟 5 才會更新線上內容。
- GitHub Pages（github.io）已停用發佈，不再對外提供網頁。
- 部署/推送屬於對外發佈，動手前先向使用者確認。
