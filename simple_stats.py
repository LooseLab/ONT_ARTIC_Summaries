import os, sys
import numpy as np
import pandas as pd
import argparse

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("-o", "--output", help="Output file", metavar="FILE")
    p.add_argument("input", help="Input files.", nargs="+", metavar="FILE")
    args = p.parse_args()
    # Flowcell_id	run_id	experiment_id	sample_id	pore_count	run_time	number_of_barcodes	barcode_id	pass_filtering	read_count	yield	mean_length	median_length	std_length	min_length	max_length
    for file_to_read in args.input:

        try:
            df2 = pd.read_csv(
                file_to_read,
                sep="\t",
                usecols=[
                    "filename_fastq",
                    "mux",
                    "channel",
                    "start_time",
                    "duration",
                    "run_id",
                    "experiment_id",
                    "sample_id",
                    "passes_filtering",
                    "barcode_arrangement",
                    "sequence_length_template",
                ],
            )
        except ValueError as e:
            print("{!r} could not be read.".format(file_to_read), file=sys.stderr)
            print("{!r}.".format(e), file=sys.stderr)

            continue

        df2["flowcell_id"] = df2["filename_fastq"].str[0:8]

        pore_count = len(
            df2.groupby(["mux", "channel"])
            .size()
            .reset_index()
            .rename(columns={0: "count"})
        )

        run_time = np.max(df2["start_time"] + df2["duration"])

        df_final = df2.groupby(
            [
                "run_id",
                "experiment_id",
                "sample_id",
                "flowcell_id",
                "passes_filtering",
                "barcode_arrangement",
            ]
        ).agg(
            {
                "sequence_length_template": [
                    "sum",
                    "count",
                    "min",
                    "max",
                    "mean",
                    "median",
                    "std",
                ]
            }
        )

        df_final.columns = df_final.columns.droplevel(0)
        df_final = df_final.reset_index()

        df_final["pore_count"] = pore_count
        df_final["barcode_count"] = len(df_final["barcode_arrangement"].unique())
        df_final["run_time"] = run_time

        df_final = df_final.rename(
            columns={
                "sum": "yield",
                "count": "read_count",
                "min": "min_length",
                "max": "max_length",
                "mean": "mean_length",
                "median": "median_length",
                "std": "std_length",
            }
        )

        output_order = [
            "run_id",
            "experiment_id",
            "sample_id",
            "flowcell_id",
            "run_time",
            "pore_count",
            "barcode_count",
            "passes_filtering",
            "barcode_arrangement",
            "yield",
            "read_count",
            "min_length",
            "max_length",
            "mean_length",
            "median_length",
            "std_length",
        ]
        if not os.path.isfile(args.output):
            df_final[output_order].to_csv(
                args.output, sep="\t", header=True, index=False
            )
        else:
            df_final[output_order].to_csv(
                args.output, sep="\t", header=False, index=False, mode="a"
            )
