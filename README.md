# RR_Assignment5
PhD course on Reproducible Research, Assignment 5, Python data analysis task

Reproducible Research – Assignment 5
===================================

Author: Jiaqi Li  
Repository: Reproducible_Research_Assignment5

--------------------------------------------------
Project Overview
--------------------------------------------------

This project contains a small Python-based data analysis workflow developed
for Assignment 5 of the Reproducible Research course.

The repository demonstrates:
- Use of a Python virtual environment (venv)
- Clear separation between raw data, processed data, and outputs
- Reproducible execution using a requirements file
- Version control with Git and GitHub

--------------------------------------------------
Repository Structure
--------------------------------------------------

.
├── file_1.py
├── requirements.txt
├── .gitignore
├── data_files/
│   ├── 60_40_01.csv
│   ├── 60_40_02.csv
│   ├── 60_40_03.csv
│   └── metadata.json
├── output/
│   ├── processed_60_40_01.csv
│   ├── processed_60_40_02.csv
│   ├── processed_60_40_03.csv
│   ├── summary_table.csv
│   ├── hist_60_40_01.png
│   ├── hist_60_40_02.png
│   └── hist_60_40_03.png
└── README.txt

--------------------------------------------------
Requirements
--------------------------------------------------

- Python 3.12
- Packages listed in requirements.txt

--------------------------------------------------
Setup Instructions
--------------------------------------------------

1. Clone the repository:

   git clone https://github.com/Li-Jiaqi/Reproducible_Research_Assignment5.git
   cd Reproducible_Research_Assignment5

2. Create a virtual environment:

   python -m venv venv

3. Activate the virtual environment:

   On Windows:
     venv\Scripts\activate

   On macOS/Linux:
     source venv/bin/activate

4. Install required packages:

   pip install -r requirements.txt

--------------------------------------------------
Running the Code
--------------------------------------------------

Run the main analysis script using:

   python Assignment5.py

The script reads input data from the data_files/ directory and generates
processed data files and visual outputs in the output/ directory.

--------------------------------------------------
Reproducibility Notes
--------------------------------------------------

- The virtual environment directory (venv/) is intentionally excluded from
  version control.
- All required Python dependencies are captured in requirements.txt.
- Outputs included in the repository were generated using the provided script
  and input data.

--------------------------------------------------
Notes
--------------------------------------------------

This repository is intended for educational purposes as part of a coursework
assignment and focuses on demonstrating reproducible research practices rather
than optimised performance or large-scale data handling.