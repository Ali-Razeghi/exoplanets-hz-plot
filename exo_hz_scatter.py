# Exoplanets — Rough Habitable Zone (HZ) Scatter
# این نسخه پنجره نمودار را نمایش می‌دهد + فایل خروجی را ذخیره می‌کند

import matplotlib
matplotlib.use("TkAgg")  # برای نمایش پنجره؛ اگه کار نکرد، از Qt5Agg یا WXAgg استفاده کن

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive

# تنظیمات
OUT_DIR = os.path.join(os.path.dirname(__file__) or ".", "outputs")
HZ_MIN, HZ_MAX = 0.35, 1.5   # محدوده ساده HZ
RADIUS_MAX = 1.8             # شعاع حداکثر برای نامزدها

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("Downloading exoplanet catalog...")

    tbl = NasaExoplanetArchive.query_criteria(
        table="pscomppars",
        select=("pl_name,pl_rade,pl_bmasse,pl_orbper,pl_eqt,pl_insol,"
                "discoverymethod,disc_year,st_teff,sy_dist"),
        where="pl_rade IS NOT NULL AND pl_insol IS NOT NULL"
    ).to_pandas()

    df = tbl.dropna(subset=["pl_rade", "pl_insol"]).copy()
    df["is_hz_small"] = (df["pl_insol"].between(HZ_MIN, HZ_MAX)) & (df["pl_rade"] <= RADIUS_MAX)

    # رسم
    plt.figure(figsize=(7.6, 5.4))
    plt.scatter(df["pl_insol"], df["pl_rade"], s=8, alpha=0.35, label="All planets")
    hz = df[df["is_hz_small"]]
    if not hz.empty:
        plt.scatter(hz["pl_insol"], hz["pl_rade"], s=22, alpha=0.9, label="HZ small candidates")

    plt.xscale("log")
    plt.xlabel("Insolation (S⊕)")
    plt.ylabel("Radius (R⊕)")
    plt.title("Exoplanets — Rough Habitable Zone & Small-Radius Candidates")
    plt.legend()
    plt.tight_layout()

    out_img = os.path.join(OUT_DIR, "exoplanets_hz.png")
    plt.savefig(out_img, dpi=150)
    plt.show()  # این خط باعث میشه نمودار روی صفحه باز بشه

    print(f"Saved plot: {out_img}")

    if not hz.empty:
        top10 = hz.nsmallest(10, "pl_rade")[["pl_name","pl_rade","pl_insol","disc_year"]]
        print("\nSample small HZ-like candidates:")
        print(top10.to_string(index=False))

if __name__ == "__main__":
    main()
