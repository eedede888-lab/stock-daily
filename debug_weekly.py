import os, re, glob

WEEKLY_DIR = "data/weekly"
week_dirs = sorted([d for d in glob.glob(os.path.join(WEEKLY_DIR, "*")) if os.path.isdir(d)])
print("week_dirs:", week_dirs)
for wdir in week_dirs:
    wkey = os.path.basename(wdir)
    print("wkey:", wkey)
    print("match:", re.match(r"\d{8}-\d{4,8}$", wkey))
    files = glob.glob(os.path.join(wdir, "*.xlsx"))
    print("xlsx files:", [os.path.basename(f) for f in files])
