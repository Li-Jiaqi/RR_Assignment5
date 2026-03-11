import os
print("Working directory:", os.getcwd())

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------
# 1. Setup paths
# ---------------------------------------------------------
data_dir = Path("data_files")  
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# ---------------------------------------------------------
# 2. Load metadata
# ---------------------------------------------------------
with open(data_dir / "metadata.json", "r") as f:
    metadata = json.load(f)

scale_factor = metadata["scale-factor-px-micron"]   # px per µm
area_column = metadata["area"]                      # "Area_px"


# ---------------------------------------------------------
# 3. Helper function: process one CSV file
# ---------------------------------------------------------
def process_file(csv_path):
    df = pd.read_csv(csv_path)

    # Convert area (px²) → diameter (µm)
    # area_px = π * (radius_px)^2
    # radius_px = sqrt(area_px / π)
    # diameter_px = 2 * radius_px
    # diameter_um = diameter_px / scale_factor
    df["diameter_um"] = 2 * np.sqrt(df[area_column] / np.pi) / scale_factor

    return df

# ---------------------------------------------------------
# 4. Process all CSV files
# ---------------------------------------------------------
csv_files = ["60_40_01.csv", "60_40_02.csv", "60_40_03.csv"]

processed_data = {}

for csv_name in csv_files:
    df = process_file(data_dir / csv_name)
    processed_data[csv_name] = df

    # Save pre‑processed CSV
    df.to_csv(output_dir / f"processed_{csv_name}", index=False)

# ---------------------------------------------------------
# 5. Analyse data: statistics + histograms
# ---------------------------------------------------------
summary_rows = []

for csv_name, df in processed_data.items():
    sample_label = metadata[csv_name]

    diam = df["diameter_um"]

    stats = {
        "sample": sample_label,
        "min_diameter_um": diam.min(),
        "max_diameter_um": diam.max(),
        "median_diameter_um": diam.median()
    }
    summary_rows.append(stats)

    # Plot histogram
    plt.figure(figsize=(6,4))
    plt.hist(diam, bins=20, edgecolor="black")
    plt.xlabel("Diameter (µm)")
    plt.ylabel("Count")
    plt.title(f"Histogram of diameters — {sample_label}")

    # Save histogram
    plt.tight_layout()
    plt.savefig(output_dir / f"hist_{csv_name.replace('.csv','')}.png", dpi=300)
    plt.close()

# ---------------------------------------------------------
# 6. Save summary table
# ---------------------------------------------------------
summary_df = pd.DataFrame(summary_rows)
summary_df.to_csv(output_dir / "summary_table.csv", index=False)

print("Processing complete. Files saved in 'output/' folder.")