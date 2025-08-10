import __main__
import argparse
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import os

parser = argparse.ArgumentParser()
parser.add_argument("--file", help="file name")
parser.add_argument("--type", help="data type (UV/1/2)")
parser.add_argument("--bin", help="bin size", type=float)
parser.add_argument("--norm", help="normalize (0/1)", type=int)
parser.add_argument("--basecor", help="baseline correct (0/1)", type=int)


def get_xy(signal, df):
    col_id = next(index for index, value in df.iloc[1].items() if value == signal)
    xy = df.iloc[3:, col_id:col_id+2]
    xy.dropna(inplace=True)
    xy.columns = df.iloc[2,col_id:col_id+2]
    xy = xy.astype(float)
    return xy

def normalize(xy):
    signal = np.array(xy.iloc[:,1]).astype(float)
    min = np.min(signal)
    max = np.max(signal)
    norm = (signal - min) / (max - min)
    xy_norm = pd.DataFrame({'mL': xy.iloc[:,0], 'signal_norm': norm})
    return xy_norm

def baselinecorrect(xy):
    signal = np.array(xy.iloc[:,1]).astype(float)
    baseline = signal[-200:].mean()
    baseline_corrected = signal - baseline
    xy_baseline_corrected = pd.DataFrame({'mL': xy.iloc[:,0], 'baseline_corrected': baseline_corrected})
    return xy_baseline_corrected

def downsample(xy, bin_size):
    volume_col = xy.columns[0]
    signal_col = xy.columns[1]

    # Round elution volumes to nearest bin
    xy['binned_volume'] = (xy[volume_col] / bin_size).round() * bin_size

    # Group by binned volume and average absorbance
    binned_data = xy.groupby('binned_volume')[signal_col].mean().reset_index()

    return binned_data

def main():
    args = parser.parse_args()

    file_name = args.file
    data_type = args.type
    bin_size = args.bin
    norm = args.norm
    baselinecor = args.basecor

    workdir = os.getcwd()

    csv = workdir + '/' + file_name + ".csv"
    df = pd.read_csv(csv, encoding='utf-16',encoding_errors='ignore', on_bad_lines='warn', sep='\t', header=None)

    if data_type == "UV":
        data = get_xy("UV", df)
    elif data_type == "1":
        data = get_xy("Analog in 1", df)
    elif data_type == "2":
        data = get_xy("Analog in 2", df)

    if baselinecor:
        data = baselinecorrect(data)

    if norm:
        data = normalize(data)

    if bin_size:
        data = downsample(data, bin_size)
        peak_distance = 0.3 / bin_size # minimumvolume peaks are apart from each other
    else:
        peak_distance = 100 #arbitrary. Need dynamic adjustment depending on UV or FSEC

    peak_id = find_peaks(data.iloc[:,1], prominence=0.01) #distance=peak_distance
    peaks = data.iloc[peak_id[0]].reset_index()
    data['peak_volume'] = peaks.iloc[:,1]
    data['peak_signal'] = peaks.iloc[:,2]

    data.to_clipboard()

if __name__ == '__main__':
    main()
    






