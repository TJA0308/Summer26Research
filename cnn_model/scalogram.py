import argparse
import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image

FS         = 16393 # Sample rate, number of samples per second in the original signal
DOWNSAMPLE = 2 # Downsample factor to reduce the effective sample rate for CWT (2 means 8196.5 Hz)
F_MIN      = 20.0 # Minimum frequency 
F_MAX      = 4000.0 # Maximum frequency
N_FREQS    = 300 # Number of frequency bins
SIGMA      = 8.0 # Width of the Gaussian window, higher sigma means sharper frequency resolution but worse time resolution
IMG_SIZE   = 224 # Size of the output image
CHANNELS   = ["ai4", "ai6"]   # ai4=feed-axis vibration, ai6=acoustic; ai5 (cross-axis) dropped
TIME_COL   = "time"


def analytic_morlet_cwt(signal, fs, n_freqs=64, f_min=1.0, f_max=None, sigma=6.0):
    if f_max is None:
        f_max = fs / 2.5

    freqs   = np.geomspace(f_min, f_max, n_freqs)
    N       = len(signal)
    sig_fft = np.fft.fft(signal.astype(np.float64))
    f_axis  = np.fft.fftfreq(N, d=1.0 / fs)

    power = np.empty((n_freqs, N), dtype=np.float32)
    for i, f0 in enumerate(freqs):
        sigma_f = f0 / sigma
        H = np.where(
            f_axis >= 0,
            np.exp(-0.5 * ((f_axis - f0) / sigma_f) ** 2),
            0.0,
        )
        z = np.fft.ifft(sig_fft * H)
        power[i] = (z.real ** 2 + z.imag ** 2).astype(np.float32)

    return power, freqs


def power_to_uint8(power, lo=None, hi=None):
    p = np.log1p(power.astype(np.float32))
    if lo is None or hi is None:
        lo, hi = np.percentile(p, 2), np.percentile(p, 98)
    if hi > lo:
        p = (np.clip(p, lo, hi) - lo) / (hi - lo)
    else:
        p = np.zeros_like(p)
    return (p * 255).astype(np.uint8)


def build_rgb_image(powers, img_size, global_ranges=None):
    """global_ranges: list of (lo, hi) per channel, or None for per-image norm."""
    planes = []
    for i, power in enumerate(powers):
        lo, hi = global_ranges[i] if global_ranges else (None, None)
        gray = power_to_uint8(power, lo=lo, hi=hi)
        resized = np.array(
            Image.fromarray(gray).resize((img_size, img_size), resample=Image.LANCZOS)
        )
        planes.append(resized)
    while len(planes) < 3:
        planes.append(np.zeros((img_size, img_size), dtype=np.uint8))
    return np.stack(planes, axis=2)


def compute_powers(df, channels, fs_eff, f_min, f_max, n_freqs, sigma, downsample):
    powers = []
    for ch in channels:
        sig = df[ch].values[::downsample].astype(np.float32)
        sig -= sig.mean()
        power, _ = analytic_morlet_cwt(sig, fs=fs_eff, n_freqs=n_freqs,
                                        f_min=f_min, f_max=f_max, sigma=sigma)
        powers.append(power)
    return powers


def process_csv(csv_path, output_dir, fs=FS, downsample=DOWNSAMPLE, f_min=F_MIN,
                f_max=F_MAX, n_freqs=N_FREQS, sigma=SIGMA, img_size=IMG_SIZE,
                channels=CHANNELS, time_col=TIME_COL, n_windows=1, global_ranges=None,
                pernorm=False):
    stem      = csv_path.stem
    df        = pd.read_csv(csv_path)
    missing   = [c for c in channels if c not in df.columns]
    if missing:
        raise ValueError(f"{csv_path.name}: missing columns {missing}. Available: {df.columns.tolist()}")

    fs_eff    = fs // downsample
    f_max_use = f_max if f_max is not None else fs_eff / 2.5
    df        = df[[time_col] + channels]
    N         = len(df)

    print(f"  {csv_path.name} ({N} samples) …", end=" ", flush=True)

    # When pernorm=True, derive normalization ranges from the full run signal
    # so all windows of this run share the same scale.
    norm_ranges = global_ranges
    if pernorm and global_ranges is None:
        full_powers = compute_powers(df, channels, fs_eff, f_min, f_max_use, n_freqs, sigma, downsample)
        norm_ranges = []
        for pw in full_powers:
            lp = np.log1p(pw.astype(np.float32))
            norm_ranges.append((float(np.percentile(lp, 2)), float(np.percentile(lp, 98))))

    if n_windows == 1:
        powers = compute_powers(df, channels, fs_eff, f_min, f_max_use, n_freqs, sigma, downsample)
        img    = build_rgb_image(powers, img_size, global_ranges=norm_ranges)
        out    = output_dir / f"{stem}.png"
        Image.fromarray(img).save(out)
        print(f"-> {out.name}")
        return [out]

    # Evenly-spaced overlapping windows of fixed length (N//2).
    # hop is computed so that n_windows windows span the full signal,
    # with the last window always ending at N.
    window_size = N // 2
    hop         = max(1, (N - window_size) // (n_windows - 1)) if n_windows > 1 else N
    saved       = []
    for w in range(n_windows):
        start  = w * hop
        end    = start + window_size
        if end > N:
            end   = N
            start = max(0, end - window_size)
        df_win = df.iloc[start:end].reset_index(drop=True)
        powers = compute_powers(df_win, channels, fs_eff, f_min, f_max_use, n_freqs, sigma, downsample)
        img    = build_rgb_image(powers, img_size, global_ranges=norm_ranges)
        out    = output_dir / f"{stem}_w{w + 1}.png"
        Image.fromarray(img).save(out)
        saved.append(out)
        print(f"\n    w{w + 1} [{start}:{end}] -> {out.name}", end=" ")

    print()
    return saved


def write_labels_template(output_dir, saved_paths):
    rows     = [{"filename": p.name, "label": 0} for p in sorted(saved_paths)]
    lbl_path = output_dir / "labels.csv"
    pd.DataFrame(rows).to_csv(lbl_path, index=False)
    print(f"\n  labels.csv -> {lbl_path}")
    return lbl_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir",  required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--single",     default=None)
    parser.add_argument("--fs",         type=int,   default=FS)
    parser.add_argument("--downsample", type=int,   default=DOWNSAMPLE)
    parser.add_argument("--f_min",      type=float, default=F_MIN)
    parser.add_argument("--f_max",      type=float, default=F_MAX)
    parser.add_argument("--n_freqs",    type=int,   default=N_FREQS)
    parser.add_argument("--sigma",      type=float, default=SIGMA)
    parser.add_argument("--img_size",   type=int,   default=IMG_SIZE)
    parser.add_argument("--n_windows",  type=int,   default=1,
                        help="Windows per run (1=full signal, 2=two overlapping half-signal windows)")
    parser.add_argument("--global_norm", action="store_true",
                        help="Two-pass global normalization: preserves amplitude across runs (better for feed/DOC)")
    parser.add_argument("--pernorm",    action="store_true",
                        help="Per-run normalization: normalize each run's windows using stats from its full signal")
    parser.add_argument("--labels",     action="store_true")
    args = parser.parse_args()

    input_dir  = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_files = ([input_dir / args.single] if args.single
                 else sorted(input_dir.glob("*.csv")))
    if not csv_files:
        print(f"No CSV files found in {input_dir}")
        return

    fs_eff = args.fs // args.downsample

    print(f"\n{'='*62}")
    print(f"  Analytic Morlet CWT Scalogram Generator")
    print(f"{'='*62}")
    print(f"  Input    : {input_dir}  ({len(csv_files)} file(s))")
    print(f"  Output   : {output_dir}")
    print(f"  Fs       : {args.fs} Hz -> {fs_eff} Hz  ({args.downsample}x downsample)")
    print(f"  Freqs    : {args.f_min}-{args.f_max} Hz  ({args.n_freqs} bins, log-spaced)")
    print(f"  Sigma    : {args.sigma} cycles  |  Image: {args.img_size}x{args.img_size} px")
    ch_str = ", ".join(CHANNELS) + (", zeros" * (3 - len(CHANNELS)))
    print(f"  Channels : {ch_str}  ->  R, G, B")
    print(f"{'='*62}\n")

    global_ranges = None
    if args.global_norm:
        print("Pass 1/2 — computing global power statistics …")
        all_log_powers = [[] for _ in CHANNELS]
        for csv_path in csv_files:
            try:
                df = pd.read_csv(csv_path)
                df = df[[TIME_COL] + CHANNELS]
                fs_eff = args.fs // args.downsample
                f_max_use = args.f_max if args.f_max else fs_eff / 2.5
                powers = compute_powers(df, CHANNELS, fs_eff, args.f_min, f_max_use,
                                        args.n_freqs, args.sigma, args.downsample)
                for ch_i, pw in enumerate(powers):
                    all_log_powers[ch_i].append(np.log1p(pw.astype(np.float32)).ravel())
            except Exception as e:
                print(f"  WARNING pass1 {csv_path.name}: {e}")
        global_ranges = []
        for ch_i, chunks in enumerate(all_log_powers):
            combined = np.concatenate(chunks)
            lo, hi = np.percentile(combined, 2), np.percentile(combined, 98)
            global_ranges.append((lo, hi))
            print(f"  {CHANNELS[ch_i]}: log-power p2={lo:.3f}, p98={hi:.3f}")
        print(f"\nPass 2/2 — saving images with global normalization …")

    all_saved = []
    for i, csv_path in enumerate(csv_files, 1):
        print(f"[{i}/{len(csv_files)}]", end=" ")
        try:
            saved = process_csv(csv_path, output_dir, fs=args.fs, downsample=args.downsample,
                                f_min=args.f_min, f_max=args.f_max, n_freqs=args.n_freqs,
                                sigma=args.sigma, img_size=args.img_size, channels=CHANNELS,
                                time_col=TIME_COL, n_windows=args.n_windows,
                                global_ranges=global_ranges, pernorm=args.pernorm)
            all_saved.extend(saved)
        except Exception as e:
            print(f"  ERROR: {e}")

    if args.labels:
        write_labels_template(output_dir, all_saved)

    print(f"\nDone. {len(all_saved)} scalogram(s) saved to {output_dir}/")


if __name__ == "__main__":
    main()
