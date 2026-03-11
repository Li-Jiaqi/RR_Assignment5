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