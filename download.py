import io
import urllib.request
import zipfile

url = "https://www.ssa.gov/oact/babynames/names.zip"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

with urllib.request.urlopen(req) as response:
    with zipfile.ZipFile(io.BytesIO(response.read())) as z:
        with open("ssa-baby-names.csv", "w", encoding="utf-8") as out:
            out.write("year,name,sex,count\n")
            for filename in sorted(z.namelist()):
                if filename.startswith("yob") and filename.endswith(".txt"):
                    year = filename[3:7]
                    for line in z.read(filename).decode("utf-8").splitlines():
                        if line.strip():
                            out.write(f"{year},{line}\n")
