
from pathlib import Path
from io import BytesIO
import time
import requests
import pandas as pd
from PIL import Image
from tqdm import tqdm

BASE = "https://skyserver.sdss.org/dr18/SkyServerWS"
ROOT = Path("data")
N_PER_CLASS = 300

session = requests.Session()
session.headers.update({"User-Agent": "AstronomyCNNStudent/1.0"})

def get_catalog(obj_type, count):
    sql = f"""
    SELECT TOP {count}
        objid, ra, dec
    FROM PhotoObj
    WHERE type = {obj_type}
      AND clean = 1
      AND r BETWEEN 14 AND 19
    ORDER BY objid
    """

    response = session.get(
        f"{BASE}/SearchTools/SqlSearch",
        params={"cmd": sql, "format": "csv"},
        timeout=90
    )
    response.raise_for_status()

    print("Response preview:", response.text[:300])

    catalog = pd.read_csv(BytesIO(response.content), comment="#")
    catalog.columns = catalog.columns.str.strip().str.lower()

    required = {"objid", "ra", "dec"}

    if not required.issubset(catalog.columns):
        raise ValueError(
            f"Unexpected SDSS response. "
            f"Expected {required}, got {catalog.columns.tolist()}. "
            f"Response: {response.text[:500]}"
        )

    return catalog

def download_cutout(ra, dec, output):
    response = session.get(
        f"{BASE}/ImgCutout/getjpeg",
        params={
            "ra": ra,
            "dec": dec,
            "scale": 0.4,
            "width": 224,
            "height": 224
        },
        timeout=40
    )
    response.raise_for_status()

    img = Image.open(BytesIO(response.content))
    img.convert("RGB").save(output, "JPEG")

records = []

for label, obj_type in [("star", 6), ("galaxy", 3)]:
    folder = ROOT / label
    folder.mkdir(parents=True, exist_ok=True)

    catalog = get_catalog(obj_type, N_PER_CLASS * 2)
    saved = 0

    
    for row in tqdm(catalog.itertuples(index=False), desc=label):

        if saved >= N_PER_CLASS:
            break

        path = folder / f"{label}_{saved:04d}.jpg"

        try:
            download_cutout(row.ra, row.dec, path)
            records.append({
                "filepath": str(path),
                "label": label,
                "source": "SDSS",
                "object_id": str(row.objid)
            })
            saved += 1
            time.sleep(0.2)
        except (requests.RequestException, OSError) as exc:
            print("Skipped:", exc)

pd.DataFrame(records).to_csv("sdss_labels.csv", index=False)
print("Downloaded", len(records), "SDSS images")
