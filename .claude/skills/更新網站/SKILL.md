---
name: 更新網站
description: 重新產生網站資料並發佈到 GitHub Pages。當使用者說「更新網站」「重新上線」「重新部署」「把新資料發佈出去」時使用。會偵測新資料、執行 build.py、跑煙霧測試、commit、push，並等待 GitHub Actions 部署完成後驗證線上網站。
---

# 更新網站

一鍵把 `data/` 裡的新資料產生並發佈到 https://tongwade.github.io/stock-daily/

## 前置確認
- 一律在 repo **根目錄** `D:\Users\2205\Desktop\main\AI_Project\stock` 執行（不要進到 `site/`，那裡有殘留的巢狀 git repo）。
- 確認 `python` 與 `node` 可用。

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

3. **檢視變更並提交**
   ```bash
   git status
   git add -A
   git commit -m "更新個股資料：<簡述新增的日期/個股>"
   ```
   commit 訊息請反映實際變更（新增了哪些日期/個股）。

4. **推送**（需要使用者明確同意才 push，因為這是發佈動作）
   ```bash
   git push
   ```

5. **等待並驗證部署**
   - 用 `gh run list --limit 1` 觀察最新一次 Deploy workflow（gh 在 PowerShell 需先 `$env:Path += ";$env:ProgramFiles\GitHub CLI"`）。
   - Actions 成功後（約 1 分鐘），抓取 `https://tongwade.github.io/stock-daily/data/index.js` 確認新日期已上線。

## 注意
- 原始 `data/` 不會上傳（已 git-ignore），只有處理後的 `site/data/` 會發佈。
- push 屬於對外發佈，動手前先向使用者確認。
