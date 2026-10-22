import io
import time
from datetime import timedelta

import matplotlib.pyplot as plt
import pandas as pd
import requests

# ---------------------------------------------------------------- settings
DATASET_ID = "goesp_part_flux_P5M"   # GOES primary, 5-minute particle flux (ISWA HAPI)
START = pd.Timestamp("2026-02-01", tz="UTC")
END = pd.Timestamp.now(tz="UTC").floor("5min")
CHUNK_DAYS = 7                        # size of each download request
PLOT_COLS = ["P10"]                   # channel(s) to plot (see printed column list)
RAW_CSV = "goes_primary_5min_2026-02_to_now.csv"
HOURLY_CSV = "goes_primary_1h_2026-02_to_now.csv"

BASE = "https://iswa.ccmc.gsfc.nasa.gov/hapi"


# ---------------------------------------------------------------- metadata
def get_info(dataset_id):
    """Ask the server which columns the dataset has, and what its fill values are."""
    r = requests.get(f"{BASE}/info", params={"id": dataset_id}, timeout=60)
    r.raise_for_status()
    return r.json()


info = get_info(DATASET_ID)
params_meta = info["parameters"]               # first entry is Time
columns = [p["name"] for p in params_meta]
fills = {p["name"]: p.get("fill") for p in params_meta[1:]}

print("Columns available:", columns)
print("Coverage according to server:",
      info.get("startDate"), "->", info.get("stopDate"))


# ---------------------------------------------------------------- download
def download(start, end):
    frames = []
    t0 = start
    while t0 < end:
        t1 = min(t0 + timedelta(days=CHUNK_DAYS), end)
        r = requests.get(
            f"{BASE}/data",
            params={
                "id": DATASET_ID,
                "time.min": t0.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "time.max": t1.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "format": "csv",
            },
            timeout=120,
        )
        # HAPI uses 404 / code 1201 for "no data in this interval"
        if r.status_code == 404:
            print(f"  no data {t0:%Y-%m-%d} -> {t1:%Y-%m-%d}")
        else:
            r.raise_for_status()
            if r.text.strip():
                frames.append(pd.read_csv(io.StringIO(r.text), comment="#",
                                          header=None, names=columns))
                print(f"  got {len(frames[-1]):5d} rows "
                      f"{t0:%Y-%m-%d} -> {t1:%Y-%m-%d}")
        t0 = t1
        time.sleep(1)                          # be polite to the server
    return pd.concat(frames, ignore_index=True)


df = download(START, END)

# ---------------------------------------------------------------- clean
time_col = columns[0]
df[time_col] = pd.to_datetime(df[time_col], utc=True)
for c in columns[1:]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
    if fills[c] is not None:                   # replace fill values with NaN
        df.loc[df[c] == float(fills[c]), c] = float("nan")

df = (df.drop_duplicates(time_col)
        .sort_values(time_col)
        .set_index(time_col))
df.index.name = "Time"

df.to_csv(RAW_CSV)
print(f"Saved 5-min data ({len(df)} rows) to {RAW_CSV}")

# ---------------------------------------------------------------- 1-hour cadence
hourly = df.resample("1h").mean()
hourly.to_csv(HOURLY_CSV)
print(f"Saved hourly data ({len(hourly)} rows) to {HOURLY_CSV}")

# ---------------------------------------------------------------- plot
fig, ax = plt.subplots(figsize=(15, 6))
for c in PLOT_COLS:
    if c not in hourly.columns:
        raise KeyError(f"{c} not in dataset; choose from {list(hourly.columns)}")
    ax.plot(hourly.index, hourly[c], lw=1, label=f"{c} (1-h mean)")

ax.axhline(10, color="red", ls="--", lw=1, label="10 pfu (NOAA S1)")
ax.set_yscale("log")
ax.set_xlabel("Time (UTC)")
ax.set_ylabel("Proton flux (pfu)")
ax.set_title("GOES primary proton flux, Feb 2026 to present (1-hour cadence)")
ax.grid(True, which="both", ls="--", alpha=0.4)
ax.legend()
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig("goes_proton_flux_hourly.png", dpi=200)
plt.show()
