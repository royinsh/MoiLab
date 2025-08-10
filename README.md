# AKTA Data Preprocessing

This script preprocess FPLC signal data given in csv formats. The output is returned to the clipboard.

## Arguments

### --path
Absolute path to the data file.

### --type
Type of signal to be processed. Input is either UV, 1, or 2 (1 and 2 are fluorescence signals titled as Analog in 1/2)

### --bin
Bin size in mL to downsample the data. Input is recommended to be between 0.01 and 0.1.

### --norm
Whether to MinMax normalize the data. Input is 0/1.

### --base
Whether to baseline correct the data (Baseline is defined as the average signal of the last 200 rows). Input is 0/1.

## Example
`python fsec.py --path path/to/csv --type 1 --bin 0.05 --base 1 --norm 1`
The above command reduces the resolution of the Analog in 1 (GFP) signal to 0.05mL, baseline corrects it and normalizes it. 





