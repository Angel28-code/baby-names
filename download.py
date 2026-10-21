import io
import urllib.error
import urllib.request
import zipfile

urls = [
    "https://www.ssa.gov/oact/babynames/names.zip",
    "https://web.archive.org/web/2026id_/https://www.ssa.gov/oact/babynames/names.zip",
]

data = None
for url in urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            data = response.read()
            break
    except urllib.error.HTTPError:
        continue

with zipfile.ZipFile(io.BytesIO(data)) as z:
    with open("ssa-baby-names.csv", "w", encoding="utf-8") as out:
        out.write("year,name,sex,count\n")
        for filename in sorted(z.namelist()):
            if filename.startswith("yob") and filename.endswith(".txt"):
                year = filename[3:7]
                for line in z.read(filename).decode("utf-8").splitlines():
                    if line.strip():
                        out.write(f"{year},{line}\n")
