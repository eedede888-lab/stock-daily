#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build.py — 把 data/ 下每天的 Excel 轉成靜態網站用的 JSON / PNG。"""
import os, re, json, glob, sys
import openpyxl

SKIP_EXISTING = "--force" not in sys.argv
ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, "data")
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
        s = stocks.setdefault(code, {})
        if "日報" in fn:
            s["daily"] = path
        elif "分析結果" in fn:
            s["analysis"] = path
    return market, stocks



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


def main():
    date_dirs = sorted([d for d in glob.glob(os.path.join(DATA_DIR, "*")) if os.path.isdir(d)])
    global_mkt = build_global_market_map(date_dirs)
    index = {"dates": []}
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
            # 名稱優先用 stock_names.json，其次放量訊號檔，最後留空
            name = NAME_OVERRIDES.get(code)
            if not name:
                if name_map is None:
                    name_map = build_name_map(market)
                name = name_map.get(code, "")
            mkt = global_mkt.get(code, "TW")  # 未知市場別預設上市
            if SKIP_EXISTING and stock_json_ok(stock_json):
                print(f"  {code} {name}: (skip)", flush=True)
            else:
                st = process_stock(code, name, stocks[code], stock_json)
                print(f"  {code} {name}: {st}", flush=True)
            stock_list.append({"code": code, "name": name, "mkt": mkt})
        index["dates"].append({"date": date, "label": label, "has_market": bool(market), "stocks": stock_list})
    index["dates"].sort(key=lambda d: d["date"], reverse=True)
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"\nindex.json: {len(index['dates'])} days -> {OUT_DIR}", flush=True)
    emit_js_wrappers()
    print("emitted .js wrappers", flush=True)


if __name__ == "__main__":
    main()
