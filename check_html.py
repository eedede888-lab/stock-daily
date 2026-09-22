#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_html.py — 檢查 debug/ 資料夾裡的回應 HTML，找出頁面結構線索。
用法：python check_html.py debug/2330_try1_ZDZ93_response.html
"""
import sys, re

if len(sys.argv) < 2:
    print("用法: python check_html.py <html檔路徑>")
    sys.exit(1)

path = sys.argv[1]
with open(path, "r", encoding="utf-8", errors="replace") as f:
    html = f.read()

def show(label, pattern_or_text, is_regex=False):
    print(f"===== {label} =====")
    if is_regex:
        m = re.search(pattern_or_text, html, re.I)
        print(m.group(0) if m else "(找不到)")
    else:
        found = pattern_or_text in html
        print("存在" if found else "不存在")
    print()

show("title 標題", r"<title>.*?</title>", is_regex=True)
show("CaptchaControl1 欄位", "CaptchaControl1")
show("TextBox_Stkno 欄位", "TextBox_Stkno")
show("HyperLink_DownloadCSV", "HyperLink_DownloadCSV")
show("「查無資料」字樣", "查無資料")
show("「驗證碼」字樣", "驗證碼")
show("btnOK 按鈕", "btnOK")

print("===== 檔案前 800 字（原始 HTML） =====")
print(html[:800])
print()
print(f"===== 檔案總長度: {len(html)} 字元 =====")
