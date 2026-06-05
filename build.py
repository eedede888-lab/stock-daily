#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build.py — 把 data/ 下每天/每週的 Excel 轉成靜態網站用的 JSON。"""
import os, re, json, glob, sys
import openpyxl
from datetime import datetime

SKIP_EXISTING = "--force" not in sys.argv
ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, "data")
WEEKLY_DIR = os.path.join(DATA_DIR, "weekly")   # data/weekly/YYYYMMDD-YYYYMMDD/
OUT_DIR = os.path.join(ROOT, "site", "data")

def load_name_overrides():
    p = os.path.join(ROOT, "stock_names.json")
    if os.path.exists(p):
        try:
            with open(p, encoding="utf-8") as f:
                return {str(k): str(v) for k, v in json.load(f).items()}
        except Exception:
            pass
    return {}

NAME_OVERRIDES = load_name_overrides()


def rows_of(path, sheet):
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    if sheet not in wb.sheetnames:
        wb.close(); return []
    ws = wb[sheet]
    out = [list(r) for r in ws.iter_rows(values_only=True)]
    wb.close(); return out


def find_header(rows, key="代號"):
    for i, r in enumerate(rows):
        cells = [str(c).strip() if c is not None else "" for c in r]
        if key in cells:
            return i, cells
    return None, None


def to_records(rows, key="代號"):
    hi, header = find_header(rows, key)
    if hi is None:
        return []
    recs = []
    for r in rows[hi + 1:]:
        if r is None:
            continue
        if all(c is None or str(c).strip() == "" for c in r):
            continue
        first = str(r[0]).strip() if r[0] is not None else ""
        if first.startswith("──") or first.startswith("【"):
            continue
        rec = {}
        for h, v in zip(header, r):
            if h == "":
                continue
            rec[h] = v
        recs.append(rec)
    return recs


def num(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return v
    s = str(v).strip().replace(",", "").replace("%", "")
    try:
        f = float(s)
        return int(f) if f.is_integer() else f
    except ValueError:
        return v


def build_name_map(market_file):
    name_map = {}
    if not market_file:
        return name_map
    small_sheets = ["今日放量訊號", "量能延續追蹤", "出關股追蹤", "處置股清單"]
    wb = openpyxl.load_workbook(market_file, data_only=True, read_only=True)
    for sh in small_sheets:
        if sh not in wb.sheetnames:
            continue
        rows = [list(r) for r in wb[sh].iter_rows(values_only=True)]
        hi, header = find_header(rows, "代號")
        if hi is None or "股票名稱" not in header:
            continue
        ci, ni = header.index("代號"), header.index("股票名稱")
        for r in rows[hi + 1:]:
            if r and r[ci] is not None and r[ni]:
                name_map[str(r[ci]).strip()] = str(r[ni]).strip()
    wb.close(); return name_map


# 市場別 → Yahoo 股市代號後綴（上市 TWSE→TW，上櫃 TPEX→TWO）。
def yahoo_suffix(market):
    m = str(market or "").strip().upper()
    if m in ("TPEX", "OTC", "上櫃", "櫃買"):
        return "TWO"
    return "TW"  # 預設視為上市


def build_market_map(market_file):
    """代號 → Yahoo 後綴（TW / TWO），掃描各小分頁的「市場」欄。"""
    mkt_map = {}
    if not market_file:
        return mkt_map
    sheets = ["今日放量訊號", "量能延續追蹤", "出關股追蹤", "處置股清單"]
    wb = openpyxl.load_workbook(market_file, data_only=True, read_only=True)
    for sh in sheets:
        if sh not in wb.sheetnames:
            continue
        rows = [list(r) for r in wb[sh].iter_rows(values_only=True)]
        hi, header = find_header(rows, "代號")
        if hi is None or "市場" not in header:
            continue
        ci, mi = header.index("代號"), header.index("市場")
        for r in rows[hi + 1:]:
            if r and r[ci] is not None and r[mi]:
                mkt_map[str(r[ci]).strip()] = yahoo_suffix(r[mi])
    wb.close(); return mkt_map




def market_json_ok(path):
    if not os.path.exists(path):
        return False
    try:
        with open(path, encoding="utf-8") as f:
            json.load(f)
        return True
    except Exception:
        return False

def stock_json_ok(path):
    """既有檔案需能正確解析且含 name 才視為完成，否則重建。"""
    if not os.path.exists(path):
        return False
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        return bool(d.get("name"))
    except Exception:
        return False

def process_market(market_file, out_path):
    SHEETS = {
        "signals": ("今日放量訊號", "代號"),
        "continuation": ("量能延續追蹤", "代號"),
        "release": ("出關股追蹤", "代號"),
        "disposed": ("處置股清單", "代號"),
        "winrate": ("勝率回測", "分類"),
    }
    data = {}
    for key, (sheet, hkey) in SHEETS.items():
        recs = to_records(rows_of(market_file, sheet), hkey)
        for rec in recs:
            for k, v in rec.items():
                rec[k] = num(v)
        data[key] = recs
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    return {k: len(v) for k, v in data.items()}


def process_stock(code, name, files, out_path):
    daily, analysis = files.get("daily"), files.get("analysis")
    out = {"code": code, "name": name, "buy_top": [], "sell_top": [], "price_volume": [], "broker_detail": []}
    if daily:
        out["buy_top"] = [{k: num(v) for k, v in r.items()} for r in to_records(rows_of(daily, "買進前20"), "券商")]
        out["sell_top"] = [{k: num(v) for k, v in r.items()} for r in to_records(rows_of(daily, "賣出前20"), "券商")]
    if analysis:
        out["price_volume"] = [{k: num(v) for k, v in r.items()} for r in to_records(rows_of(analysis, "買賣價量與家數"), "股價")]
        keep = ["股價", "券商", "買進股數", "賣出股數", "買進占比", "賣出占比", "最高買進", "最高賣出"]
        det = []
        for r in to_records(rows_of(analysis, "券商明細"), "股價"):
            det.append({k: num(r.get(k)) for k in keep if k in r})
        out["broker_detail"] = det
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    return {"buy": len(out["buy_top"]), "sell": len(out["sell_top"]),
            "pv": len(out["price_volume"]), "detail": len(out["broker_detail"])}


def classify(files_in_dir):
    """日報資料夾用：分類 market / daily / analysis，忽略 charts。"""
    market = None
    stocks = {}
    for path in files_in_dir:
        fn = os.path.basename(path)
        if fn.startswith("台股放量訊號"):
            market = path; continue
        m = re.match(r"^(\d{4})", fn)
        if not m:
            continue
        code = m.group(1)
        if "charts" in fn.lower():   # 忽略 charts.xlsx（已無用途）
            continue
        s = stocks.setdefault(code, {})
        if "日報" in fn:
            s["daily"] = path
        elif "分析結果" in fn:
            s["analysis"] = path
    return market, stocks


def classify_weekly(files_in_dir):
    """週報資料夾用：分類 weekly（週報）/ volume_avg（大量與均價）。"""
    stocks = {}
    for path in files_in_dir:
        fn = os.path.basename(path)
        m = re.match(r"^(\d{4})", fn)
        if not m:
            continue
        code = m.group(1)
        if "charts" in fn.lower():
            continue
        s = stocks.setdefault(code, {})
        if "週報" in fn:
            s["weekly"] = path
        elif "大量與均價" in fn:
            s["volume_avg"] = path
    return stocks




def process_weekly(code, name, files, out_path):
    """讀取週報的買進前20/賣出前20，結構與 process_stock 相同。"""
    weekly = files.get("weekly")
    out = {"code": code, "name": name, "buy_top": [], "sell_top": []}
    if weekly:
        out["buy_top"] = [{k: num(v) for k, v in r.items()}
                          for r in to_records(rows_of(weekly, "買進前20"), "券商")]
        out["sell_top"] = [{k: num(v) for k, v in r.items()}
                          for r in to_records(rows_of(weekly, "賣出前20"), "券商")]
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    return {"buy": len(out["buy_top"]), "sell": len(out["sell_top"])}


def process_volume_avg(code, name, files, out_path):
    """解析「大量與均價」Excel，輸出每日摘要 + 前10明細。

    工作表版面（工作表1）：
      Row 3  : 大欄標題（大量 / 前10買量 / 前10買進均價 / 大量 / 前10賣量…）
      Row 4  : 細欄標題（股價 / 買進股數 / 賣出股數 / 買進家數 / 賣出家數 / 最高買進 / 最高賣出 / 收盤價）
      Row 6~ : 每日摘要（日期, 大量股價, 買進股數, 賣出股數, 買進家數, 賣出家數,
                        最高買進股數, 最高賣出股數, 收盤價,
                        前10買量, 前10買進均價, None,
                        大量(同前), 前10賣量, 前10賣出均價）
      空行後
      Row 14 : 各日期欄位（col 0,4,8,12,16 為 datetime）
      Row 15 : 買/價/賣/價（每日4欄重複）
      Row 16+: 前10券商明細（每列20欄，每5欄一天）
      Row 27 : 各日前10買量/賣量小計
      Row 28 : 各日前10均價
    """
    va_file = files.get("volume_avg")
    out = {"code": code, "name": name, "daily_summary": [], "top10_detail": []}
    if not va_file:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
        return {"days": 0}

    rows = [list(r) for r in
            openpyxl.load_workbook(va_file, data_only=True, read_only=True)["工作表1"]
            .iter_rows(values_only=True)]

    # --- 每日摘要（row index 6~10，遇 None 日期停止）---
    summary_cols = ["date", "price", "buy_qty", "sell_qty",
                    "buy_cnt", "sell_cnt", "max_buy_qty", "max_sell_qty", "close",
                    "top10_buy_qty", "top10_buy_avg", None,
                    None, "top10_sell_qty", "top10_sell_avg"]
    daily = []
    for r in rows[6:]:
        if r[0] is None:
            break
        rec = {}
        for i, col in enumerate(summary_cols):
            if col is None or i >= len(r):
                continue
            v = r[i]
            if col == "date":
                rec[col] = v.strftime("%Y-%m-%d") if hasattr(v, "strftime") else str(v)
            else:
                rec[col] = num(v)
        daily.append(rec)
    out["daily_summary"] = daily

    # --- 找前10明細區塊（日期列，row 14 = index 14）---
    # 每天佔4欄（買量, 買均價, 賣量, 賣均價），5天共20欄
    date_row = rows[14]
    dates_order = []
    for i in range(0, 20, 4):
        v = date_row[i]
        if v is not None:
            d = v.strftime("%Y-%m-%d") if hasattr(v, "strftime") else str(v)
            dates_order.append((d, i))

    detail = {d: [] for d, _ in dates_order}
    for r in rows[16:]:
        if all(c is None for c in r):
            break
        for d, base in dates_order:
            if len(r) <= base + 3:
                continue
            buy_qty, buy_avg, sell_qty, sell_avg = r[base], r[base+1], r[base+2], r[base+3]
            if buy_qty is None and sell_qty is None:
                continue
            detail[d].append({
                "buy_qty":  num(buy_qty),
                "buy_avg":  num(buy_avg),
                "sell_qty": num(sell_qty),
                "sell_avg": num(sell_avg),
            })

    out["top10_detail"] = [{"date": d, "brokers": detail[d]} for d, _ in dates_order]

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    return {"days": len(daily)}


def emit_js_wrappers():
    """把每個 .json 另存成同名 .js，供 file:// 直接以 <script> 載入（免伺服器）。"""
    import glob as _g
    for jp in _g.glob(os.path.join(OUT_DIR, "**", "*.json"), recursive=True):
        key = os.path.relpath(jp, OUT_DIR)[:-5].replace(os.sep, "/")
        with open(jp, encoding="utf-8") as f:
            content = f.read()
        with open(jp[:-5] + ".js", "w", encoding="utf-8") as f:
            f.write("window.__DATAREG&&window.__DATAREG(" + json.dumps(key) + "," + content + ");")


def build_global_market_map(date_dirs):
    """跨所有日期累積 代號→Yahoo後綴；市場別穩定，避免某天沒進放量分頁就抓不到。"""
    g = {}
    for ddir in date_dirs:
        files = glob.glob(os.path.join(ddir, "*.xlsx"))
        market, _ = classify(files)
        if market:
            g.update(build_market_map(market))
    return g


def weekly_json_ok(path):
    if not os.path.exists(path):
        return False
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        return bool(d.get("name"))
    except Exception:
        return False


def main():
    # ── 日報 ──────────────────────────────────────────────────────────────
    date_dirs = sorted([d for d in glob.glob(os.path.join(DATA_DIR, "*"))
                        if os.path.isdir(d) and os.path.basename(d) != "weekly"])
    global_mkt = build_global_market_map(date_dirs)
    index = {"dates": [], "weekly_dates": []}
    for ddir in date_dirs:
        date = os.path.basename(ddir)
        if not re.fullmatch(r"\d{8}", date):
            continue
        label = f"{date[:4]}-{date[4:6]}-{date[6:]}"
        out_day = os.path.join(OUT_DIR, date)
        os.makedirs(out_day, exist_ok=True)
        files = glob.glob(os.path.join(ddir, "*.xlsx"))
        market, stocks = classify(files)
        print(f"\n=== {date} ===", flush=True)
        market_json = os.path.join(out_day, "market.json")
        if market:
            if SKIP_EXISTING and market_json_ok(market_json):
                print("  market.json (skip)", flush=True)
            else:
                print("  market.json:", process_market(market, market_json), flush=True)
        name_map = None
        stock_list = []
        for code in sorted(stocks):
            stock_json = os.path.join(out_day, f"{code}.json")
            name = NAME_OVERRIDES.get(code)
            if not name:
                if name_map is None:
                    name_map = build_name_map(market)
                name = name_map.get(code, "")
            mkt = global_mkt.get(code, "TW")
            if SKIP_EXISTING and stock_json_ok(stock_json):
                print(f"  {code} {name}: (skip)", flush=True)
            else:
                st = process_stock(code, name, stocks[code], stock_json)
                print(f"  {code} {name}: {st}", flush=True)
            stock_list.append({"code": code, "name": name, "mkt": mkt})
        index["dates"].append({"date": date, "label": label, "has_market": bool(market), "stocks": stock_list})
    index["dates"].sort(key=lambda d: d["date"], reverse=True)

    # ── 週報 ──────────────────────────────────────────────────────────────
    if os.path.isdir(WEEKLY_DIR):
        week_dirs = sorted([d for d in glob.glob(os.path.join(WEEKLY_DIR, "*"))
                            if os.path.isdir(d)])
        for wdir in week_dirs:
            wkey = os.path.basename(wdir)          # e.g. 20260522-0528
            # 接受 YYYYMMDD-MMDD 或 YYYYMMDD-YYYYMMDD 格式
            if not re.match(r"\d{8}-\d{4,8}$", wkey):
                continue
            parts = wkey.split("-")
            start = parts[0]
            end_raw = parts[1]
            end = (start[:4] + end_raw) if len(end_raw) == 4 else end_raw
            label = f"{start[:4]}-{start[4:6]}-{start[6:]} ~ {end[:4]}-{end[4:6]}-{end[6:]}"
            out_week = os.path.join(OUT_DIR, "weekly", wkey)
            os.makedirs(out_week, exist_ok=True)
            files = glob.glob(os.path.join(wdir, "*.xlsx"))
            stocks = classify_weekly(files)
            print(f"\n=== 週報 {wkey} ===", flush=True)
            stock_list = []
            for code in sorted(stocks):
                name = NAME_OVERRIDES.get(code, "")
                # 週報主檔
                w_json = os.path.join(out_week, f"{code}.json")
                if SKIP_EXISTING and weekly_json_ok(w_json):
                    print(f"  {code} {name}: (skip)", flush=True)
                else:
                    st = process_weekly(code, name, stocks[code], w_json)
                    print(f"  {code} {name} 週報: {st}", flush=True)
                # 大量與均價（獨立檔案）
                va_json = os.path.join(out_week, f"{code}_vol.json")
                if SKIP_EXISTING and weekly_json_ok(va_json):
                    print(f"  {code} {name} vol: (skip)", flush=True)
                else:
                    vt = process_volume_avg(code, name, stocks[code], va_json)
                    print(f"  {code} {name} vol: {vt}", flush=True)
                mkt = global_mkt.get(code, "TW")
                stock_list.append({"code": code, "name": name, "mkt": mkt})
            index["weekly_dates"].append({
                "wkey": wkey, "label": label,
                "start": start, "end": end,
                "stocks": stock_list,
            })
        index["weekly_dates"].sort(key=lambda d: d["start"], reverse=True)

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"\nindex.json: {len(index['dates'])} days, {len(index['weekly_dates'])} weeks -> {OUT_DIR}", flush=True)
    emit_js_wrappers()
    print("emitted .js wrappers", flush=True)


if __name__ == "__main__":
    main()
