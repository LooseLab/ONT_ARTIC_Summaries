# ONT_ARTIC_Summaries

To install:

Clone this repository:

```git clone https://github.com/LooseLab/ONT_ARTIC_Summaries```

Then:

```buildoutcfg
cd ONT_ARTIC_Summaries
conda env create -f environment.yml
```


To activate:

```
conda activate ONT_ARTIC_Summaries
```


To run:

```
python simple_stats.py -o output.file -c NOTTS sequencing_summary_file1.txt sequencing_summary_file2.txt```
```

You can optionally use wildcards to find sequencing summary files:

```
python simple_stats.py -o output.file -c NOTTS sequencing_summary*.txt
```

Note: if the output file already exists, data will be appended to it.

Help:
```
python simple_stats.py -h
usage: simple_stats.py [-h] [-o FILE] [-c STRING] FILE [FILE ...]

positional arguments:
  FILE                  One or many input files. These must be ONT sequencing
                        summary files as called by MinKNOW or Guppy with
                        bardoing options set. Reads demultiplexed with
                        PoreChop will not work. The files can be optionally
                        compressed.

optional arguments:
  -h, --help            show this help message and exit
  -o FILE, --output FILE
                        File name to write out the summary stats.
  -c STRING, --centre STRING
                        Sequencing Center Generating this Data.
```

Expected output is a TSV file:
```
sequencing_centre       run_id  experiment_id   sample_id       flowcell_id     run_time        pore_count      barcode_count   passes_filtering        barcode_arrangement     yield   read_count      min_length      max_length      mean_length     median_length   std_length
NOTTS   d00b486adc2ea7266fc2d4549d293d6fb22638f1        CV      CV094_24_M1     FAN43036        17069.68        1345    25      False   barcode05       189458  358     254     926     529.2122905027933       500.5   95.17517191957664
NOTTS   d00b486adc2ea7266fc2d4549d293d6fb22638f1        CV      CV094_24_M1     FAN43036        17069.68        1345    25      False   barcode06       230839  448     225     1555    515.265625      502.0   87.33024300710545
...
NOTTS   d00b486adc2ea7266fc2d4549d293d6fb22638f1        CV      CV094_24_M1     FAN43036        17069.68        1345    25      True    barcode05       42963045        83875   164     1870    512.2270640834575       507.0   57.61899716876888
NOTTS   d00b486adc2ea7266fc2d4549d293d6fb22638f1        CV      CV094_24_M1     FAN43036        17069.68        1345    25      True    barcode06       50445170        98387   187     1666    512.7219043166272       509.0   47.506330979971004
...
```
The file contains one row per barcode pass/fail dataset. So a run with 96 barcodes will generate 194 rows.

These data will be used to analyse yield and performance of various ARTIC protocols. The script anticipates sequencing summary files from MinKNOW/Guppy running with barcoding enabled. It will skip any files that do not contain barcoded data.

Once you have collated the data from your centre, please either send the data to Matt Loose or upload to the shared google doc. 
