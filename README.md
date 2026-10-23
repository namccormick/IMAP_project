# GOES SEP Monitoring, February 2026 to present

Downloads GOES primary 5-minute solar particle flux data from the NASA
ISWA/CCMC HAPI server and plots it at 1-hour cadence, to identify when
solar energetic particle (SEP) events occur.

## Data source

- Server: NASA CCMC ISWA HAPI (https://iswa.ccmc.gsfc.nasa.gov/hapi)
- Dataset ID: `goesp_part_flux_P5M` (GOES primary, 5-minute particle flux)
- Time range: 1 February 2026 to the present (set by `START` / `END` in the script)
- Data downloaded on 23 October 2026

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python goes_sep_download_plot.py
```

The script will:
1. Query the server for the dataset's columns and coverage.
2. Download the data in 7-day chunks.
3. Replace fill values with NaN and remove duplicate timestamps.
4. Save the 5-minute data and a 1-hour mean version as CSV.
5. Plot the proton flux (log scale).

## Outputs

| File | Description |
|------|-------------|
| `goes_primary_5min_2026-02_to_now.csv` | Raw 5-minute data, all channels |
| `goes_primary_1h_2026-02_to_now.csv` | 1-hour mean of the above |
| `goes_proton_flux_hourly.png` | Plot of the hourly flux |

These files are not tracked by git (see `.gitignore`). Re-run the script
to regenerate them.

## Configuration

Edit the settings at the top of `goes_sep_download_plot.py`:
- `START`, `END`: time range
- `PLOT_COLS`: channel(s) to plot (e.g. `["P10"]` for >10 MeV)
- `CHUNK_DAYS`: size of each download request

## Notes

- Flux is in pfu (particles / (cm² s sr)). 10 pfu in the >10 MeV channel is
  the NOAA S1 radiation storm threshold.
- This is real-time (RT) data and may be revised or replaced by
  science-quality data later, so re-download before using it in a publication.
- The primary GOES satellite can change over time, which can introduce small
  step changes in the data.

## Author

Naomi McCormick, University of Lancashire