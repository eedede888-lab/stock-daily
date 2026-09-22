#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
path = sys.argv[1] if len(sys.argv) > 1 else "debug/2330_try1_27DDK_response.html"
with open(path, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()
print(f"長度: {len(content)} 字元")
print("----- 完整內容 -----")
print(content)
print("--------------------")
