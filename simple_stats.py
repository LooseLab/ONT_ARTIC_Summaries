import os, sys
import numpy as np
import pandas as pd
import argparse

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument(
        "-o",
        "--output",
        help="File name to write out the summary stats.",
        metavar="FILE",
    )
    p.add_argument(
        "input",
        help="One or many input files. These must be ONT sequencing summary files as called by MinKNOW or Guppy with bardoing options set. Reads demultiplexed with PoreChop will not work. The files can be optionally compressed.",
        nargs="+",
        metavar="FILE",
    )
    p.add_argument(
        "-c",
        "--centre",
        help="Sequencing Center Generating this Data.",
        metavar="STRING",
    )
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

        pore_count = {}
        run_time = {}
        barcode_count = {}
        for run_id, gb in df2.groupby(["run_id"]):
            pore_count[run_id] = len(
                gb.groupby(["mux", "channel"])
                .size()
                .reset_index()
                .rename(columns={0: "count"})
            )
            run_time[run_id] = np.max(gb["start_time"] + gb["duration"])
            barcode_count[run_id] = len(gb["barcode_arrangement"].unique())

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

        df_final["pore_count"] = df_final["run_id"].map(pore_count)
        df_final["barcode_count"] = df_final["run_id"].map(barcode_count)
        df_final["run_time"] = df_final["run_id"].map(run_time)
        df_final["sequencing_centre"] = args.centre

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
            "sequencing_centre",
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
