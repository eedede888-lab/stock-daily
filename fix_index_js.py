import json, os

OUT_DIR = "site/data"

jp = os.path.join(OUT_DIR, "index.json")
key = "index"

with open(jp, encoding="utf-8") as f:
    content = f.read()

js_path = os.path.join(OUT_DIR, "index.js")
with open(js_path, "w", encoding="utf-8") as f:
    f.write("window.__DATAREG&&window.__DATAREG(" + json.dumps(key) + "," + content + ");")

print("Done! index.js size:", os.path.getsize(js_path))

# 確認內容有 weekly_dates
with open(js_path, encoding="utf-8") as f:
    content = f.read()
print("has weekly_dates:", "weekly_dates" in content)
print("has wkey:", "wkey" in content)
