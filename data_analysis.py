import os
print("Working directory:", os.getcwd())

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def load_metadata(metadata_path: Path) -> dict[str, Any]:
    """Load metadata from a JSON file.

    Parameters
    ----------
    metadata_path : Path
        Path to the metadata JSON file.

    Returns
    -------
    dict[str, Any]
        Parsed metadata dictionary.

    Raises
    ------
    FileNotFoundError
        If the metadata file does not exist.
    ValueError
        If the file cannot be parsed as valid JSON.
    """
    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_path}")

    try:
        with metadata_path.open("r", encoding="utf-8") as file:
            metadata = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in metadata file: {metadata_path}") from exc

    return metadata

def validate_metadata(metadata: dict[str, Any]) -> tuple[float, str]:
    """Validate required metadata fields.

    Parameters
    ----------
    metadata : dict[str, Any]
        Metadata dictionary.

    Returns
    -------
    tuple[float, str]
        Scale factor (px per micron) and area column name.

    Raises
    ------
    KeyError
        If required metadata fields are missing.
    ValueError
        If values are invalid.
    """
    required_keys = ["scale-factor-px-micron", "area"]
    for key in required_keys:
        if key not in metadata:
            raise KeyError(f"Required metadata key missing: {key}")

    scale_factor = metadata["scale-factor-px-micron"]
    area_column = metadata["area"]

    if not isinstance(scale_factor, (int, float)) or scale_factor <= 0:
        raise ValueError(
            "'scale-factor-px-micron' must be a positive number."
        )

    if not isinstance(area_column, str) or not area_column.strip():
        raise ValueError("'area' must be a non-empty string.")

    return float(scale_factor), area_column

def load_csv(csv_path: Path) -> pd.DataFrame:
    """Load one CSV file into a DataFrame.

    Parameters
    ----------
    csv_path : Path
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Loaded DataFrame.

    Raises
    ------
    FileNotFoundError
        If the CSV file does not exist.
    ValueError
        If the CSV file cannot be read.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    try:
        return pd.read_csv(csv_path)
    except Exception as exc:
        raise ValueError(f"Could not read CSV file: {csv_path}") from exc
    
def compute_diameter_um(
    df: pd.DataFrame,
    area_column: str,
    scale_factor: float,
) -> pd.DataFrame:
    """Compute equivalent particle diameter in microns from area in pixels^2.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing the area column.
    area_column : str
        Name of the column containing particle area in pixels^2.
    scale_factor : float
        Conversion factor in pixels per micron.

    Returns
    -------
    pd.DataFrame
        Copy of the input DataFrame with a new column 'diameter_um'.

    Raises
    ------
    KeyError
        If the area column is missing.
    ValueError
        If area values are invalid.
    """
    if area_column not in df.columns:
        raise KeyError(f"Area column '{area_column}' not found in CSV file.")

    result = df.copy()

    if result[area_column].isnull().any():
        raise ValueError(f"Column '{area_column}' contains missing values.")

    if (result[area_column] < 0).any():
        raise ValueError(f"Column '{area_column}' contains negative values.")

    result["diameter_um"] = (
        2 * (result[area_column] / math.pi) ** 0.5 / scale_factor
    )
    return result

def process_csv_file(
    csv_path: Path,
    area_column: str,
    scale_factor: float,
) -> pd.DataFrame:
    """Load and process one CSV file.

    Parameters
    ----------
    csv_path : Path
        Path to input CSV file.
    area_column : str
        Name of area column in pixels^2.
    scale_factor : float
        Conversion factor in pixels per micron.

    Returns
    -------
    pd.DataFrame
        Processed DataFrame with diameter column.
    """
    df = load_csv(csv_path)
    return compute_diameter_um(df, area_column, scale_factor)


def get_sample_label(metadata: dict[str, Any], csv_name: str) -> str:
    """Return the human-readable sample label for a CSV file.

    Parameters
    ----------
    metadata : dict[str, Any]
        Metadata dictionary.
    csv_name : str
        CSV file name.

    Returns
    -------
    str
        Sample label.

    Notes
    -----
    If the sample label is not present in metadata, the file stem is used.
    """
    return str(metadata.get(csv_name, Path(csv_name).stem))


def summarise_diameters(sample_label: str, diameters: pd.Series) -> dict[str, float | str]:
    """Compute summary statistics for a diameter series.

    Parameters
    ----------
    sample_label : str
        Human-readable sample name.
    diameters : pd.Series
        Series containing diameter values in microns.

    Returns
    -------
    dict[str, float | str]
        Dictionary of summary statistics.
    """
    return {
        "sample": sample_label,
        "min_diameter_um": float(diameters.min()),
        "max_diameter_um": float(diameters.max()),
        "median_diameter_um": float(diameters.median()),
        "mean_diameter_um": float(diameters.mean()),
    }


def plot_histogram(
    diameters: pd.Series,
    sample_label: str,
    output_path: Path,
    bins: int = 20,
) -> None:
    """Plot and save a histogram of particle diameters.

    Parameters
    ----------
    diameters : pd.Series
        Diameter values in microns.
    sample_label : str
        Human-readable sample name.
    output_path : Path
        Output file path for the histogram image.
    bins : int, optional
        Number of histogram bins, by default 20.
    """
    plt.figure(figsize=(6, 4))
    plt.hist(diameters, bins=bins, edgecolor="black")
    plt.xlabel("Diameter (µm)")
    plt.ylabel("Count")
    plt.title(f"Histogram of diameters - {sample_label}")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def ensure_directory(directory: Path) -> None:
    """Create a directory if it does not already exist.

    Parameters
    ----------
    directory : Path
        Directory path to create.
    """
    directory.mkdir(parents=True, exist_ok=True)

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