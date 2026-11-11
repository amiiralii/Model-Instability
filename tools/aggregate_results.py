"""
Aggregate CSV results from results/X/ directory.
Each row represents a dataset, each column represents a treatment.
"""
import glob
import os
import pandas as pd
from pathlib import Path

def aggregate_results_0(input_dir: str, output_dir: str = None):
    """
    Reads all CSV files from input_dir and aggregates them.
    
    Each CSV file has treatments in first column and metrics in other columns.
    Output will have treatments as columns and datasets as rows.
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir) if output_dir else input_path
    
    # Find all CSV files
    csv_files = sorted(input_path.glob("*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {input_dir}")
        return
    
    print(f"Found {len(csv_files)} CSV files")
    
    # Read all CSV files
    columns = []
    with open(csv_files[0], "r") as f:
        for ln in f:
            col = ln.split(",")[0]
            if col not in columns: columns.append(col)
    agg_all = pd.DataFrame(columns=columns)

    for csv_file in csv_files:
        dataset_name = csv_file.stem  # filename without extension
        with open(csv_file, "r") as f:
            tmp = {}
            for ln in f:
                data = ln.split(",")
                tmp[data[0]] = data[1].strip()
        agg_all = pd.concat([agg_all, pd.DataFrame([tmp])], ignore_index=True)
    
    output_file = output_path / f"aggregated.csv"
    agg_all.to_csv(output_file, index=False)
    print(f"\nSaved aggregation to: {output_file}")
    print(agg_all.to_string(index=False))

if __name__ == "__main__":
    # Choose paths that contain raw CSV files. XX redirects to where all csv files exist
    input_dir = "RQ1/results/"
    output_dir = "RQ1/results/aggregates"

    aggregate_results_0(input_dir, output_dir)


