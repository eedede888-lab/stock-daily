#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tpex_fetch.py — 抓「上櫃(TPEx)」個股券商分點進出明細。

上櫃資料在 TPEx 的 brokerBS 頁，且受 Cloudflare Turnstile（「我不是機器人」）保護。
過去 headful 的內建 Chromium 可被 Turnstile 自動放行，但 Cloudflare 已收緊偵測：
內建 Chromium 連挑戰 iframe 都不渲染、token 永遠是空的，查詢自然送不出去。

現行解法（2026-06 起）：改用 **patchright**（Playwright 的修補版，消除 Cloudflare 用來
偵測自動化的 CDP 痕跡，例如 Runtime.enable 洩漏）＋ 系統真 Chrome（channel="chrome"）
＋ 持久化使用者設定檔（保存 cf_clearance，第二次起更快）。實測 Turnstile 約 5~12 秒
**自動**產生 token，無需人工點選。

取得資料的方式：頁面查詢結果是分頁 HTML 表格（不完整），但表單內有「下載 CSV」按鈕，
按下會回傳**完整**單表 CSV。注意 **Turnstile token 是一次性**的——必須在拿到 token 後
「直接」按下載鈕，不可先按「查詢」把 token 用掉，否則會下載到 0 byte 空檔。

下載偵測：不使用 Playwright 的 expect_download/dl.path()（該機制透過 CDP 回報下載
事件，實測會被 Chrome 版本更新影響而不可靠——按鈕確實被點到、Chrome 也確實把檔案存
到磁碟，但 CDP 不一定通知 Playwright，導致永遠等不到事件而逾時）。改成指定固定下載
資料夾（downloads_path），點擊後直接輪詢磁碟找新出現且大小穩定的檔案。

下載到的 CSV 第 3 行起為「序號,券商,價格,買進股數,賣出股數」單欄表，轉成與 BSR 相同格式
的乾淨 CSV（序號,券商,股價,買進股數,賣出股數），build.py / 下游可直接吃。

前置：
    pip install patchright
    python -m patchright install chromium     # 或確保系統已裝 Google Chrome
用法（需「有桌面」環境，會跳出瀏覽器視窗；--hide 可把視窗移到螢幕外給排程用）：
    python tpex_fetch.py 3105 6261
    python tpex_fetch.py --hide 3105 6261
產出：每檔 {code}_bsr.csv（序號,券商,股價,買進股數,賣出股數）＋ {code}_tpex_raw.csv（原始下載）
"""
import os, re, csv, sys, io, time, json, random, argparse, datetime

PAGE = "https://www.tpex.org.tw/zh-tw/mainboard/trading/info/brokerBS.html"
PROFILE_DIRNAME = ".patchright_profile"   # 持久化設定檔（存 cf_clearance，加速 Turnstile）


def _to_int(x):
    x = str(x or "").replace(",", "").strip().strip('"')
    if not x:
        return 0
    try:
        return int(float(x))
    except ValueError:
        return 0


def parse_tpex_csv(csv_text):
    """解析 TPEx 下載的券商買賣 CSV。
    格式：前兩行為標題（券商買賣證券成交價量資訊 / 證券代碼,xxxx），
          第三行為表頭「序號,券商,價格,買進股數,賣出股數」，其後為資料列。
    回傳 list[dict]：序號 / 券商 / 股價 / 買進股數 / 賣出股數。"""
    out = []
    started = False
    for r in csv.reader(io.StringIO(csv_text)):
        if not r:
            continue
        if not started:
            if r[0].strip() == "序號":       # 找到表頭列後才開始讀資料
                started = True
            continue
        if len(r) < 5 or not r[0].strip().isdigit():
            continue
        out.append({
            "序號": _to_int(r[0]),
            "券商": r[1].strip(),
            "股價": r[2].strip().strip('"'),
            "買進股數": _to_int(r[3]),
            "賣出股數": _to_int(r[4]),
        })
    return out


def _wait_turnstile(page, timeout_s=45):
    """等 Turnstile 自動產生 token（patchright 多半 5~12 秒）。回傳 token 字串（逾時為空字串）。"""
    deadline = timeout_s * 2
    for _ in range(deadline):
        try:
            tok = page.eval_on_selector(
                "input[name='cf-turnstile-response']", "e=>e&&e.value") or ""
        except Exception:
            tok = ""
        if tok:
            return tok
        time.sleep(0.5)
    return ""


def _wait_new_stable_file(dl_dir, before_set, timeout_s=20):
    """輪詢 dl_dir，找出新出現且大小已穩定不再變化的檔案，回傳完整路徑或 None。"""
    deadline = time.time() + timeout_s
    candidate = None
    while time.time() < deadline:
        now_set = set(os.listdir(dl_dir))
        new_files = [f for f in (now_set - before_set) if not f.endswith((".crdownload", ".tmp"))]
        if new_files:
            newest = max(new_files, key=lambda f: os.path.getmtime(os.path.join(dl_dir, f)))
            p1 = os.path.join(dl_dir, newest)
            try:
                s1 = os.path.getsize(p1)
                time.sleep(0.6)
                s2 = os.path.getsize(p1)
            except OSError:
                time.sleep(0.3); continue
            if s1 == s2 and s1 > 0:
                return p1
            candidate = p1
        time.sleep(0.4)
    return candidate


def _looks_like_disconnect(e):
    """粗略判斷例外是否代表瀏覽器/context 已經死掉（而不是單一代號的普通失敗）。"""
    name = type(e).__name__
    msg = str(e).lower()
    return ("targetclosed" in name.lower() or "closed" in msg
            or "disconnected" in msg or "crashed" in msg)


def _ensure_automatic_downloads_allowed(profile_dir, patterns):
    """強制把 Chrome「自動下載多個檔案」的網站權限改成允許（保險用，不一定是主因，
    但無害且成本很低）。只在 Chrome 沒有在跑時呼叫才有效，要在
    launch_persistent_context 之前執行。"""
    pref_path = os.path.join(profile_dir, "Default", "Preferences")
    if not os.path.isfile(pref_path):
        return
    try:
        with open(pref_path, "r", encoding="utf-8") as f:
            prefs = json.load(f)
    except Exception:
        return
    content_settings = prefs.setdefault("profile", {}).setdefault("content_settings", {})
    exceptions = content_settings.setdefault("exceptions", {})
    auto_dl = exceptions.setdefault("automatic_downloads", {})
    changed = False
    for pattern in patterns:
        entry = auto_dl.get(pattern)
        if not entry or entry.get("setting") != 1:
            auto_dl[pattern] = {"last_modified": "13300000000000000", "setting": 1}
            changed = True
    if not changed:
        return
    try:
        with open(pref_path, "w", encoding="utf-8") as f:
            json.dump(prefs, f, ensure_ascii=False)
    except Exception:
        pass


def _human_click(page, selector, timeout=8000):
    """先把滑鼠用分段、帶隨機抖動的路徑移到目標按鈕上，停頓一下再點擊，取代瞬間
    直接點擊——後者是很典型的自動化特徵，容易被 Cloudflare 的行為偵測抓到。"""
    el = page.wait_for_selector(selector, timeout=timeout)
    box = el.bounding_box()
    if not box:
        el.click()
        return
    target_x = box["x"] + box["width"] / 2
    target_y = box["y"] + box["height"] / 2
    start_x = target_x + random.uniform(-150, 150)
    start_y = target_y + random.uniform(-100, 100)
    page.mouse.move(start_x, start_y)
    steps = random.randint(8, 14)
    for i in range(1, steps + 1):
        t = i / steps
        ease = t * t * (3 - 2 * t)
        x = start_x + (target_x - start_x) * ease + random.uniform(-2, 2)
        y = start_y + (target_y - start_y) * ease + random.uniform(-2, 2)
        page.mouse.move(x, y)
        time.sleep(random.uniform(0.01, 0.03))
    time.sleep(random.uniform(0.1, 0.3))
    page.mouse.click(target_x, target_y)


def fetch_one(page, code, raw_dir, dl_dir, hide):
    """對已開好的 page 抓一檔：等 Turnstile → 直接下載 CSV → 解析。
    下載逾時或 token 失效時，同一頁重新整理、重新拿一組新 token 再試一次；
    兩次都失敗且視窗可見時，改為提示使用者手動點下載當最後防線。
    回傳 (records | None, err)；err 為 None 表成功。
    若判斷是瀏覽器/context 已經斷線，例外會直接往外拋出，由呼叫端決定是否重啟瀏覽器。"""
    page.on("dialog", lambda d: (
        print(f"  [{code}] 頁面跳出對話框：{d.message!r}，自動確認", flush=True),
        d.accept()))
    try:
        page.goto(PAGE, wait_until="domcontentloaded", timeout=45000)
        time.sleep(1.5)
        page.fill("input.code", str(code))
        page.keyboard.press("Escape")  # 關閉代號欄位的自動完成下拉選單
        time.sleep(0.3)

        dl_path = None
        for attempt in (1, 2):
            tok = _wait_turnstile(page)
            if not tok:
                if attempt == 2:
                    return None, "turnstile-timeout（Turnstile 未自動過，可能需更新 patchright 或手動點一次）"
            else:
                before_set = set(os.listdir(dl_dir))
                _human_click(page, "#tables-form button.response[data-format='utf-8']", timeout=8000)
                dl_path = _wait_new_stable_file(dl_dir, before_set, timeout_s=20)
                if dl_path:
                    break
                if attempt == 2:
                    if hide:
                        return None, "下載逾時（資料夾沒出現新檔案，token 可能已失效）"
                    print(f"  [{code}] 自動下載連續失敗，可能被網站的機器人偵測擋下來了。"
                          f"視窗還開著，請直接手動點一次「下載 CSV (UTF-8)」，"
                          f"完成後回到這裡按 Enter 繼續（不處理就直接按 Enter 放棄這檔）…",
                          flush=True)
                    before_manual = set(os.listdir(dl_dir))
                    try:
                        input()
                    except Exception:
                        pass
                    dl_path = _wait_new_stable_file(dl_dir, before_manual, timeout_s=5)
                    if not dl_path:
                        return None, "手動救援仍未偵測到新檔案"
                    break
            # 重試前重新整理頁面，讓 Turnstile 重新產生一組新 token
            page.reload(wait_until="domcontentloaded", timeout=45000)
            time.sleep(1.5)
            page.fill("input.code", str(code))
            page.keyboard.press("Escape")
            time.sleep(0.3)

        data = open(dl_path, "rb").read()
        txt = data.decode("utf-8-sig", "replace")
        # 存原始下載供除錯/校正
        with open(os.path.join(raw_dir, f"{code}_tpex_raw.csv"), "w",
                  encoding="utf-8-sig", newline="") as f:
            f.write(txt)
        if len(data) < 100:
            return None, f"下載檔過小({len(data)} bytes)，可能 token 失效或當日無資料"
        return parse_tpex_csv(txt), None
    except Exception as e:
        if _looks_like_disconnect(e):
            raise
        return None, f"例外 {type(e).__name__}: {e}"
    finally:
        try:
            page.close()
        except Exception:
            pass


def save_csv(records, path):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["序號", "券商", "股價", "買進股數", "賣出股數"])
        w.writeheader(); w.writerows(records)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("codes", nargs="+")
    ap.add_argument("--out", default=None)
    ap.add_argument("--date", default=None)
    ap.add_argument("--keep-open", action="store_true", help="跑完不關視窗（除錯用）")
    ap.add_argument("--hide", action="store_true",
                    help="把瀏覽器視窗移到螢幕外（排程無人值守用；視窗仍真實存在，Turnstile 照過）")
    args = ap.parse_args()

    try:
        from patchright.sync_api import sync_playwright
    except ImportError:
        print("缺少 patchright，請先安裝：pip install patchright 並 python -m patchright install chromium",
              flush=True)
        sys.exit(2)

    root = os.path.dirname(os.path.abspath(__file__))
    date = args.date or datetime.date.today().strftime("%Y%m%d")
    out_dir = args.out or os.path.join(root, "data", date)
    os.makedirs(out_dir, exist_ok=True)
    profile = os.path.join(root, PROFILE_DIRNAME)
    dl_dir = os.path.join(root, "_tpex_downloads")
    os.makedirs(dl_dir, exist_ok=True)

    print(f"TPEx(上櫃) 抓取 {len(args.codes)} 檔 → {out_dir}", flush=True)
    ok = 0; failed = []
    DL_ORIGIN_PATTERNS = ["https://www.tpex.org.tw,*", "https://www.tpex.org.tw:443,*",
                          "[*.]tpex.org.tw,*"]
    with sync_playwright() as p:
        launch_args = ["--no-first-run", "--no-default-browser-check"]
        if args.hide:   # 視窗移到螢幕外，無人值守時不打擾（仍是真實 headful，Turnstile 可過）
            launch_args += ["--window-position=-32000,-32000", "--window-size=1100,800"]

        def launch_ctx():
            _ensure_automatic_downloads_allowed(profile, DL_ORIGIN_PATTERNS)
            return p.chromium.launch_persistent_context(
                profile, channel="chrome", headless=False, no_viewport=True,
                accept_downloads=True, downloads_path=dl_dir, args=launch_args)

        ctx = launch_ctx()
        remaining = list(args.codes)
        retry_budget = 3  # 整趟最多重啟 3 次瀏覽器
        try:
            while remaining:
                code = remaining[0]
                page = None
                try:
                    page = ctx.new_page()
                    recs, err = fetch_one(page, code, out_dir, dl_dir, args.hide)
                    if err:
                        print(f"  {code}: {err}", flush=True)
                        failed.append(code)
                    elif not recs:
                        print(f"  {code}: 解析不到資料（raw 已存）", flush=True)
                        failed.append(code)
                    else:
                        buy = sum(r["買進股數"] for r in recs); sell = sum(r["賣出股數"] for r in recs)
                        balanced = abs(buy - sell) <= max(50, buy * 0.001)
                        save_csv(recs, os.path.join(out_dir, f"{code}_bsr.csv"))
                        print(f"  {code}: {len(recs)} 筆，Σ買={buy:,} Σ賣={sell:,} "
                              f"{'OK' if balanced else '[!] 買賣不平衡(資料可能不完整)'}", flush=True)
                        ok += 1
                    remaining.pop(0)
                    time.sleep(1.0)
                except Exception as e:
                    if not _looks_like_disconnect(e) or retry_budget <= 0:
                        print(f"  {code}: 無法復原的例外 {type(e).__name__}: {e}", flush=True)
                        failed.append(code); remaining.pop(0)
                        continue
                    retry_budget -= 1
                    print(f"  瀏覽器連線中斷（常見原因：暫時性偵測波動或 Chrome 背景更新），"
                          f"3 秒後重新啟動並從 {code} 繼續（剩餘重試次數 {retry_budget}）…",
                          flush=True)
                    page = None
                    try:
                        ctx.close()
                    except Exception:
                        pass
                    time.sleep(3)
                    ctx = launch_ctx()
                    continue  # 不 pop，重試同一個 code
            if args.keep_open:
                print("（--keep-open）視窗保留中，按 Enter 關閉…", flush=True)
                try: input()
                except Exception: pass
        finally:
            try:
                ctx.close()
            except Exception:
                pass
    print(f"完成 {ok}/{len(args.codes)}" + (f"；失敗：{','.join(failed)}" if failed else ""), flush=True)
    sys.exit(0 if ok == len(args.codes) else 1)


if __name__ == "__main__":
    main()
