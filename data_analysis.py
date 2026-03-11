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
