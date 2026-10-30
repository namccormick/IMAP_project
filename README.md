# GOES SEP Monitoring, February 2026 to present

Downloads GOES primary 5-minute solar particle flux data from the NASA
ISWA/CCMC HAPI server and plots it at 1-hour cadence, to identify when
solar energetic particle (SEP) events occur. Individual flux enhancements
are then examined in more detail using multi-spacecraft data.

The project has two stages:

1. **Event identification:** GOES flux over ~6 months (this README, Part 1)
2. **Event analysis:** multi-spacecraft data for a selected event (Part 2)

## Part 1: GOES event identification

### Data source

- Server: NASA CCMC ISWA HAPI (https://iswa.ccmc.gsfc.nasa.gov/hapi)
- Dataset ID: `goesp_part_flux_P5M` (GOES primary, 5-minute particle flux)
- Time range: 1 February 2026 to the present (set by `START` / `END` in the script)
- Data downloaded on 23 October 2026

### Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Usage

```bash
python goes_sep_download_plot.py
```

The script will:
1. Query the server for the dataset's columns and coverage.
2. Download the data in 7-day chunks.
3. Replace fill values with NaN and remove duplicate timestamps.
4. Save the 5-minute data and a 1-hour mean version as CSV.
5. Plot the proton flux (log scale).

### Outputs

| File | Description |
|------|-------------|
| `goes_primary_5min_2026-02_to_now.csv` | Raw 5-minute data, all channels |
| `goes_primary_1h_2026-02_to_now.csv` | 1-hour mean of the above |
| `goes_proton_flux_hourly.png` | Plot of the hourly flux |

These files are not tracked by git (see `.gitignore`). Re-run the script
to regenerate them.

### Configuration

Edit the settings at the top of `goes_sep_download_plot.py`:
- `START`, `END`: time range
- `PLOT_COLS`: channel(s) to plot (e.g. `["P10"]` for >10 MeV)
- `CHUNK_DAYS`: size of each download request

## Part 2: Multi-spacecraft analysis of selected events

Spikes in the GOES flux that may be due to solar energetic particle events
are examined in more detail using data from several spacecraft at different
locations in the inner heliosphere. Data are retrieved with the SERPENTINE data loader tool (https://serpentine-h2020.eu/hub/).

### Event 1: 30 March to 3 April 2026

| Item | Detail |
|------|--------|
| Time window | 30 March 2026 to 3 April 2026 |
| Spacecraft | Solar Orbiter, Parker Solar Probe, SOHO, WIND, STEREO-A |
| Instruments / species | PSP ISOIS-EPILO and ISOIS-EPIHI-HET, SOLO/(EPT and HET), STEREO-A/SEPT, WIND/SDP, and SOHO/ERNE/HED.|
| Data downloaded on | 29/10/2026 |

The event was chosen on the suggestion of my supervisor. This event is quite broad, without a core of protons >500 MeV.

### Usage

```jupyter lab
GOES_events_v1.ipynb
```

The script will:
1. Read the data into jupyter lab
2. Resample, clean and combine the data.]
3. Plot the data.


### Adding further events

To analyse another event, [describe the steps, e.g. copy the script, change
the time window, and choose spacecraft that have data for that period].

## Notes

- Flux is in pfu (particles / (cm² s sr)). 10 pfu in the >10 MeV channel is
  the NOAA S1 radiation storm threshold.
- GOES data are real-time (RT) data and may be revised or replaced by
  science-quality data later, so re-download before using them in a publication.
- The primary GOES satellite can change over time, which can introduce small
  step changes in the data.
- The spacecraft in Part 2 are at different heliocentric distances and
  longitudes, and use different instruments and energy channels, so
  intensities are not directly comparable without cross-calibration.


## Author

Naomi McCormick, University of Lancashire