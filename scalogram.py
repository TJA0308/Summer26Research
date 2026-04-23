import os
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image


FS          = 16393       
DOWNSAMPLE  = 4           
F_MIN       = 10.0          
F_MAX       = 2000       
N_FREQS     = 128        
SIGMA       = 6.0          
IMG_SIZE    = 224          
CHANNELS    = ["ai4", "ai5", "ai6"]   
TIME_COL    = "X_Value"
CMAP        = "jet"        

def morlet_cwt(signal: np.ndarray, fs: float,
               n_freqs: int = 64,
               f_min: float = 1.0,
               f_max: float = None,
               sigma: float = 6.0) -> tuple[np.ndarray, np.ndarray]:
    
    if f_max is None:
        f_max = fs / 2.5          # stay safely below Nyquist

    freqs   = np.geomspace(f_min, f_max, n_freqs)
    N       = len(signal)
    sig_fft = np.fft.rfft(signal, n=N)
    f_axis  = np.fft.rfftfreq(N, d=1.0 / fs)

    power = np.empty((n_freqs, N), dtype=np.float32)
    for i, f0 in enumerate(freqs):
        sigma_f  = f0 / sigma                             # bandwidth at this freq
        H        = np.exp(-0.5 * ((f_axis - f0) / sigma_f) ** 2)
        conv     = np.fft.irfft(sig_fft * H, n=N)
        power[i] = conv ** 2

    return power, freqs


def channel_to_rgb_array(power: np.ndarray, cmap_name: str = "jet") -> np.ndarray:
    p = power.astype(np.float32)
    p_min, p_max = p.min(), p.max()
    if p_max > p_min:
        p = (p - p_min) / (p_max - p_min)
    else:
        p = np.zeros_like(p)

    cmap   = plt.get_cmap(cmap_name)
    rgb    = (cmap(p)[:, :, :3] * 255).astype(np.uint8)   # drop alpha
    return rgb


def process_csv(csv_path: Path,
                output_dir: Path,
                fs: int         = FS,
                downsample: int = DOWNSAMPLE,
                f_min: float    = F_MIN,
                f_max: float    = F_MAX,
                n_freqs: int    = N_FREQS,
                sigma: float    = SIGMA,
                img_size: int   = IMG_SIZE,
                channels: list  = CHANNELS,
                time_col: str   = TIME_COL,
                cmap: str       = CMAP) -> Path:
    
    stem = csv_path.stem                         
    out_path = output_dir / f"{stem}.png"

    print(f"  Loading  {csv_path.name} …", end=" ", flush=True)
    df = pd.read_csv(csv_path)

    missing = [c for c in channels if c not in df.columns]
    if missing:
        raise ValueError(f"{csv_path.name}: missing columns {missing}. "
                         f"Available: {df.columns.tolist()}")

    fs_eff = fs // downsample
    if f_max is None:
        f_max_use = fs_eff / 2.5
    else:
        f_max_use = f_max

    channel_images = []
    for ch in channels:
        sig = df[ch].values[::downsample].astype(np.float32)
        sig -= sig.mean()

        power, _ = morlet_cwt(sig, fs=fs_eff,
                               n_freqs=n_freqs,
                               f_min=f_min,
                               f_max=f_max_use,
                               sigma=sigma)

        power = np.log1p(power)

        rgb_arr = channel_to_rgb_array(power, cmap_name=cmap)
        channel_images.append(rgb_arr)

    resized = []
    for arr in channel_images:
        img = Image.fromarray(arr).resize((img_size, img_size),
                                          resample=Image.LANCZOS)
        resized.append(np.array(img))

    r = resized[0].mean(axis=2).astype(np.uint8)   
    g = resized[1].mean(axis=2).astype(np.uint8)   
    b = resized[2].mean(axis=2).astype(np.uint8)  
    composite = np.stack([r, g, b], axis=2)        

    Image.fromarray(composite).save(out_path)
    print(f"saved → {out_path.name}")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Generate Morlet CWT scalograms from run CSVs")
    parser.add_argument("--input_dir",  required=True,  help="Directory containing run*.csv files")
    parser.add_argument("--output_dir", required=True,  help="Directory to save .png scalograms")
    parser.add_argument("--single",     default=None,   help="Process only this filename (e.g. run1.csv)")
    parser.add_argument("--fs",         type=int,   default=FS)
    parser.add_argument("--downsample", type=int,   default=DOWNSAMPLE)
    parser.add_argument("--f_min",      type=float, default=F_MIN)
    parser.add_argument("--f_max",      type=float, default=None)
    parser.add_argument("--n_freqs",    type=int,   default=N_FREQS)
    parser.add_argument("--sigma",      type=float, default=SIGMA)
    parser.add_argument("--img_size",   type=int,   default=IMG_SIZE)
    parser.add_argument("--cmap",       default=CMAP)
    args = parser.parse_args()

    input_dir  = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.single:
        csv_files = [input_dir / args.single]
    else:
        csv_files = sorted(input_dir.glob("*.csv"))
        if not csv_files:
            print(f"No CSV files found in {input_dir}")
            return

    print(f"\n{'='*55}")
    print(f"  Morlet CWT Scalogram Generator")
    print(f"{'='*55}")
    print(f"  Input  : {input_dir}  ({len(csv_files)} file(s))")
    print(f"  Output : {output_dir}")
    print(f"  Fs     : {args.fs} Hz  →  {args.fs // args.downsample} Hz (after {args.downsample}x downsample)")
    print(f"  Freqs  : {args.f_min} – {'Nyquist' if args.f_max is None else args.f_max} Hz  ({args.n_freqs} bins)")
    print(f"  Sigma  : {args.sigma}   |  Image: {args.img_size}x{args.img_size}  |  Cmap: {args.cmap}")
    print(f"  Channels (R,G,B): {CHANNELS}")
    print(f"{'='*55}\n")

    for i, csv_path in enumerate(csv_files, 1):
        print(f"[{i}/{len(csv_files)}]", end=" ")
        try:
            process_csv(csv_path, output_dir,
                        fs=args.fs,
                        downsample=args.downsample,
                        f_min=args.f_min,
                        f_max=args.f_max,
                        n_freqs=args.n_freqs,
                        sigma=args.sigma,
                        img_size=args.img_size,
                        channels=CHANNELS,
                        time_col=TIME_COL,
                        cmap=args.cmap)
        except Exception as e:
            print(f"  ERROR: {e}")

    print(f"\nDone. {len(csv_files)} scalogram(s) saved to {output_dir}/")


if __name__ == "__main__":
    main()