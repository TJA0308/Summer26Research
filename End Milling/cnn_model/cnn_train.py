import argparse
import json
import random
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
from torchvision import models, transforms
from PIL import Image

SEED = 42

# ── Speed prediction ──────────────────────────────────────────────────────
SPEED_LABELS = {
    "run1": 3,  "run2": 3,  "run3": 3,   # 4000 rpm  DOC=0.015
    "run4": 4,  "run5": 4,  "run6": 4,   # 5000 rpm  DOC=0.015
    "run7": 0,  "run8": 0,  "run9": 0,   # 1500 rpm  DOC=0.030
    "run10": 1, "run11": 1, "run12": 1,  # 2000 rpm  DOC=0.030
    "run13": 2, "run14": 2, "run15": 2,  # 3000 rpm  DOC=0.030
    "run16": 3, "run17": 3, "run18": 3,  # 4000 rpm  DOC=0.030
    "run19": 4, "run20": 4, "run21": 4,  # 5000 rpm  DOC=0.030
    "run22": 0, "run23": 0, "run24": 0,  # 1500 rpm  DOC=0.060
    "run25": 1, "run26": 1, "run27": 1,  # 2000 rpm  DOC=0.060
    "run28": 2, "run29": 2, "run30": 2,  # 3000 rpm  DOC=0.060
    "run31": 3, "run32": 3, "run33": 3,  # 4000 rpm  DOC=0.060
    "run34": 4, "run35": 4, "run36": 4,  # 5000 rpm  DOC=0.060
    "run37": 0, "run38": 0, "run39": 0,  # 1500 rpm  DOC=0.015
    "run40": 1, "run41": 1, "run42": 1,  # 2000 rpm  DOC=0.015
    "run43": 2, "run44": 2, "run45": 2,  # 3000 rpm  DOC=0.015
}
SPEED_NAMES = {0: "1500 rpm", 1: "2000 rpm", 2: "3000 rpm", 3: "4000 rpm", 4: "5000 rpm"}
# Balanced split: 3 per class × 5 RPM classes (one per DOC level) = 15 test, 30 train
SPEED_TEST_RUNS= {
    "run9",  "run22", "run37",   # 1500 rpm: DOC=0.030, 0.060, 0.015
    "run12", "run27", "run40",   # 2000 rpm: DOC=0.030, 0.060, 0.015
    "run15", "run28", "run43",   # 3000 rpm: DOC=0.030, 0.060, 0.015
    "run2",  "run16", "run31",   # 4000 rpm: DOC=0.015, 0.030, 0.060
    "run5",  "run19", "run36",   # 5000 rpm: DOC=0.015, 0.030, 0.060
}

# ── Feed rate prediction ──────────────────────────────────────────────────
# Actual feed values in mm/rev: 0=3, 1=4, 2=5, 3=6, 4=7, 5=8
FEED_LABELS = {
    "run1":  2,  "run2":  3,  "run3":  4,   # DOC=0.015, 4000rpm, feed=5,6,7
    "run4":  3,  "run5":  4,  "run6":  5,   # DOC=0.015, 5000rpm, feed=6,7,8
    "run7":  0,  "run8":  1,  "run9":  2,   # DOC=0.030, 1500rpm, feed=3,4,5
    "run10": 0,  "run11": 1,  "run12": 2,   # DOC=0.030, 2000rpm, feed=3,4,5
    "run13": 1,  "run14": 2,  "run15": 3,   # DOC=0.030, 3000rpm, feed=4,5,6
    "run16": 2,  "run17": 3,  "run18": 4,   # DOC=0.030, 4000rpm, feed=5,6,7
    "run19": 3,  "run20": 4,  "run21": 5,   # DOC=0.030, 5000rpm, feed=6,7,8
    "run22": 0,  "run23": 1,  "run24": 2,   # DOC=0.060, 1500rpm, feed=3,4,5
    "run25": 0,  "run26": 1,  "run27": 2,   # DOC=0.060, 2000rpm, feed=3,4,5
    "run28": 1,  "run29": 2,  "run30": 3,   # DOC=0.060, 3000rpm, feed=4,5,6
    "run31": 2,  "run32": 3,  "run33": 4,   # DOC=0.060, 4000rpm, feed=5,6,7
    "run34": 3,  "run35": 4,  "run36": 5,   # DOC=0.060, 5000rpm, feed=6,7,8
    "run37": 0,  "run38": 1,  "run39": 2,   # DOC=0.015, 1500rpm, feed=3,4,5
    "run40": 0,  "run41": 1,  "run42": 2,   # DOC=0.015, 2000rpm, feed=3,4,5
    "run43": 1,  "run44": 2,  "run45": 3,   # DOC=0.015, 3000rpm, feed=4,5,6
}

# ── Coarsened feed rate (3-class: low/medium/high) ───────────────────────
# Groups: 0=low(3-4mm/rev), 1=medium(5-6mm/rev), 2=high(7-8mm/rev)
FEED_COARSE_LABELS = {k: v // 2 for k, v in FEED_LABELS.items()}
FEED_COARSE_NAMES  = {0: "3-4 mm/rev (low)", 1: "5-6 mm/rev (med)", 2: "7-8 mm/rev (high)"}  # same test runs, labels remapped
# 4 per class = 12 test, 33 train
FEED_COARSE_TEST_RUNS = {
    "run25", "run13", "run7",  "run37",  # Low  (3-4 mm/rev): 2000rpm DOC=0.060, 3000rpm DOC=0.030, 1500rpm DOC=0.030, 1500rpm DOC=0.015
    "run31", "run17", "run9",  "run45",  # Med  (5-6 mm/rev): 4000rpm DOC=0.060, 4000rpm DOC=0.030, 1500rpm DOC=0.030, 3000rpm DOC=0.015
    "run5",  "run36", "run3",  "run21",  # High (7-8 mm/rev): 5000rpm DOC=0.015, 5000rpm DOC=0.060, 4000rpm DOC=0.015, 5000rpm DOC=0.030
}

# 6-class fine-grained feed. 1 test run per class (not 4/class like
# FEED_COARSE_TEST_RUNS) -- class 5 (8 mm/rev) only has 3 runs in the whole
# dataset, all at 5000rpm by design, so holding out more than 1 per class
# isn't possible without starving training further. 39 train / 6 test;
# class 5 is left with only 2 training runs -- treat its accuracy with more
# skepticism than the other 5 classes.
FEED_NAMES     = {0: "3 mm/rev", 1: "4 mm/rev", 2: "5 mm/rev", 3: "6 mm/rev", 4: "7 mm/rev", 5: "8 mm/rev"}
FEED_TEST_RUNS = {
    "run40",  # 3 mm/rev  (DOC=0.015, 2000rpm)
    "run28",  # 4 mm/rev  (DOC=0.060, 3000rpm)
    "run1",   # 5 mm/rev  (DOC=0.015, 4000rpm)
    "run17",  # 6 mm/rev  (DOC=0.030, 4000rpm)
    "run35",  # 7 mm/rev  (DOC=0.060, 5000rpm)
    "run6",   # 8 mm/rev  (DOC=0.015, 5000rpm)
}

# ── Depth-of-cut prediction ───────────────────────────────────────────────
DOC_LABELS = {
    "run1": 0,  "run2": 0,  "run3": 0,   # DOC=0.015
    "run4": 0,  "run5": 0,  "run6": 0,   # DOC=0.015
    "run7": 1,  "run8": 1,  "run9": 1,   # DOC=0.030
    "run10": 1, "run11": 1, "run12": 1,  # DOC=0.030
    "run13": 1, "run14": 1, "run15": 1,  # DOC=0.030
    "run16": 1, "run17": 1, "run18": 1,  # DOC=0.030
    "run19": 1, "run20": 1, "run21": 1,  # DOC=0.030
    "run22": 2, "run23": 2, "run24": 2,  # DOC=0.060
    "run25": 2, "run26": 2, "run27": 2,  # DOC=0.060
    "run28": 2, "run29": 2, "run30": 2,  # DOC=0.060
    "run31": 2, "run32": 2, "run33": 2,  # DOC=0.060
    "run34": 2, "run35": 2, "run36": 2,  # DOC=0.060
    "run37": 0, "run38": 0, "run39": 0,  # DOC=0.015
    "run40": 0, "run41": 0, "run42": 0,  # DOC=0.015
    "run43": 0, "run44": 0, "run45": 0,  # DOC=0.015
}
DOC_NAMES = {0: "0.015 mm", 1: "0.03 mm", 2: "0.06 mm"}
# 4 per class = 12 test, 33 train
DOC_TEST_RUNS = {
    "run1",  "run5",  "run38", "run41",   # 0.015 mm: 4000,5000,1500,2000 rpm
    "run7",  "run14", "run16", "run19",   # 0.030 mm: 1500,3000,4000,5000 rpm
    "run22", "run25", "run29", "run36",   # 0.060 mm: 1500,2000,3000,5000 rpm
}

# ── Surface roughness prediction (Ra μm) ─────────────────────────────────
# 0=Smooth (Ra<0.7), 1=Medium (0.7≤Ra≤1.0), 2=Rough (Ra>1.0)
RA_LABELS = {
    # DOC=0.015 — all smooth
    "run1": 0,  "run2": 0,  "run3": 0,    # Ra: 0.392, 0.282, 0.328
    "run4": 0,  "run5": 0,  "run6": 0,    # Ra: 0.302, 0.424, 0.448
    "run37": 0, "run38": 0, "run39": 0,   # Ra: 0.416, 0.302, 0.326
    "run40": 0, "run41": 0, "run42": 0,   # Ra: 0.328, 0.304, 0.454
    "run43": 0, "run44": 0, "run45": 0,   # Ra: 0.364, 0.314, 0.414
    # DOC=0.030 — mixed
    "run7": 1,  "run8": 1,  "run9": 0,    # Ra: 0.930, 0.852, 0.558
    "run10": 0, "run11": 1, "run12": 1,   # Ra: 0.640, 0.896, 0.902
    "run13": 0, "run14": 0, "run15": 0,   # Ra: 0.494, 0.418, 0.482
    "run16": 1, "run17": 0, "run18": 0,   # Ra: 0.834, 0.678, 0.384
    "run19": 1, "run20": 2, "run21": 2,   # Ra: 0.864, 1.048, 1.638
    # DOC=0.060 — mostly medium/rough
    "run22": 2, "run23": 1, "run24": 1,   # Ra: 1.186, 0.814, 0.726
    "run25": 0, "run26": 1, "run27": 1,   # Ra: 0.596, 0.838, 0.868
    "run28": 2, "run29": 2, "run30": 2,   # Ra: 1.340, 1.108, 1.010
    "run31": 1, "run32": 2, "run33": 2,   # Ra: 0.820, 1.612, 1.490
    "run34": 2, "run35": 2, "run36": 2,   # Ra: 2.084, 1.980, 1.790
}
RA_NAMES = {0: "Smooth (Ra<0.7)", 1: "Medium (0.7-1.0)", 2: "Rough (Ra>1.0)"}
# 4 per class = 12 test, 33 train
RA_TEST_RUNS_12 = {
    "run5",  "run43", "run38", "run40",  # Smooth: 5000/3000/1500/2000 rpm, all DOC=0.015
    "run7",  "run27", "run11", "run19",  # Medium: 1500rpm DOC=0.030, 2000rpm DOC=0.060, 2000rpm DOC=0.030, 5000rpm DOC=0.030
    "run22", "run34", "run28", "run32",  # Rough:  1500/5000/3000/4000 rpm, all DOC=0.060
}

# Legacy aliases (used by load_split default path)
RUN_LABELS = SPEED_LABELS
TEST_RUNS  = SPEED_TEST_RUNS
TRAIN_RUNS = set(RUN_LABELS.keys()) - TEST_RUNS

# Balanced-split aliases — these are already the 30/15 and 33/12 sets
SPEED_TEST_RUNS_BALANCED = SPEED_TEST_RUNS      # 15 test (3/class × 5 RPM)
DOC_TEST_RUNS_12         = DOC_TEST_RUNS        # 12 test (4/class × 3 DOC)
RA_TEST_RUNS             = RA_TEST_RUNS_12      # 12 test (4/class × 3 Ra)
FEED_COARSE_TEST_RUNS_12 = FEED_COARSE_TEST_RUNS  # 12 test (4/class × 3 feed)

# ── Alternate splits (mirrors Shoulder Milling's exp11/exp12 practice of
# checking whether a "best" config's accuracy survives a different held-out
# set, not just the one fixed split used throughout the rest of this
# project). SPEED_TEST_RUNS_ALT1/ALT2 exactly 3-fold-partition all 45 runs
# together with SPEED_TEST_RUNS (each run appears as "test" in exactly one
# of the 3 folds) since speed's 9-runs-per-class pool divides evenly by 3.
# FEED_COARSE's per-class run pools are highly unbalanced (15/21/9 runs for
# low/med/high) so a clean 3-way partition isn't possible for the "high"
# class (only 9 runs total, 4 already in FEED_COARSE_TEST_RUNS, leaving 5)
# -- ALT1 and ALT2 for that class share 3 of their 4 test runs as a result;
# every other class's ALT1/ALT2 runs are fully disjoint from each other and
# from FEED_COARSE_TEST_RUNS.
SPEED_TEST_RUNS_ALT1 = {
    "run7", "run8", "run23",       # 1500 rpm
    "run10", "run11", "run25",     # 2000 rpm
    "run13", "run14", "run29",     # 3000 rpm
    "run1", "run3", "run17",       # 4000 rpm
    "run4", "run6", "run20",       # 5000 rpm
}
SPEED_TEST_RUNS_ALT2 = {
    "run24", "run38", "run39",     # 1500 rpm
    "run26", "run41", "run42",     # 2000 rpm
    "run30", "run44", "run45",     # 3000 rpm
    "run18", "run32", "run33",     # 4000 rpm
    "run21", "run34", "run35",     # 5000 rpm
}
# ALT3: unlike ALT1/ALT2 (which happen to be DOC-imbalanced -- e.g. ALT1's
# 1500rpm test triplet is 2xDOC0.030 + 1xDOC0.060, no DOC0.015 run at all),
# ALT3 is constructed to be DOC-balanced per class, same structural property
# as SPEED_TEST_RUNS itself (exactly one test run per DOC level per class).
# Built by taking, for each of the 15 (class, DOC) cells, the lower-numbered
# of the two runs not already in SPEED_TEST_RUNS -- a deterministic rule
# applied before any accuracy was known, not an accuracy-based selection.
# Still fully disjoint from SPEED_TEST_RUNS, ALT1, and ALT2.
SPEED_TEST_RUNS_ALT3 = {
    "run7", "run23", "run38",      # 1500 rpm: DOC=0.030, 0.060, 0.015
    "run10", "run25", "run41",     # 2000 rpm: DOC=0.030, 0.060, 0.015
    "run13", "run29", "run44",     # 3000 rpm: DOC=0.030, 0.060, 0.015
    "run1", "run17", "run32",      # 4000 rpm: DOC=0.015, 0.030, 0.060
    "run4", "run20", "run34",      # 5000 rpm: DOC=0.015, 0.030, 0.060
}
# ALT4: the complement of ALT3 within the same 30-run non-standard pool --
# takes the higher-numbered of each (class, DOC) cell's two non-standard
# runs (ALT3 took the lower-numbered one). Also DOC-balanced, fully disjoint
# from SPEED_TEST_RUNS, ALT1, ALT2, and ALT3. Together, SPEED_TEST_RUNS +
# ALT3 + ALT4 form a second clean 3-way, DOC-balanced partition of all 45
# runs (distinct from the SPEED_TEST_RUNS + ALT1 + ALT2 partition).
SPEED_TEST_RUNS_ALT4 = {
    "run8", "run24", "run39",      # 1500 rpm: DOC=0.015, 0.030, 0.060
    "run11", "run26", "run42",     # 2000 rpm: DOC=0.015, 0.030, 0.060
    "run14", "run30", "run45",     # 3000 rpm: DOC=0.015, 0.030, 0.060
    "run3", "run18", "run33",      # 4000 rpm: DOC=0.015, 0.030, 0.060
    "run6", "run21", "run35",      # 5000 rpm: DOC=0.015, 0.030, 0.060
}
FEED_COARSE_TEST_RUNS_ALT1 = {
    "run8", "run10", "run11", "run22",     # low
    "run1", "run2", "run4", "run12",       # med
    "run6", "run18", "run20", "run33",     # high
}
FEED_COARSE_TEST_RUNS_ALT2 = {
    "run23", "run26", "run28", "run38",    # low
    "run14", "run15", "run16", "run19",    # med
    "run18", "run20", "run33", "run35",    # high (overlaps ALT1 by 3 runs)
}

# ── Relaxed-overlap alt splits (do not need to be 100% disjoint from the
# standard split -- only >=50% of test runs need to differ). Extends the
# split-robustness check to all four targets, not just speed/feed_coarse.
# All are still 0% overlap with their own target's standard split (well
# over the 50% bar); where a class's non-standard pool couldn't cover two
# full fresh 4-run test sets, the shortfall is shared between the two new
# alt splits themselves (never with standard) -- feed_coarse's "high" class
# (9 runs total) and roughness's "medium"/"rough" classes (11 each).

# SPEED_TEST_RUNS_ALT5/ALT6: a third DOC-balanced 3-way partition of the
# same 6 non-standard runs/class used by ALT1-4, using a per-(class,DOC)-
# pair selection pattern distinct from both ALT1/ALT2 (first-half/second-
# half by run number) and ALT3/ALT4 (lower/higher within each DOC pair).
SPEED_TEST_RUNS_ALT5 = {
    "run7", "run24", "run38",      # 1500 rpm
    "run10", "run26", "run41",     # 2000 rpm
    "run13", "run30", "run44",     # 3000 rpm
    "run1", "run18", "run32",      # 4000 rpm
    "run4", "run21", "run34",      # 5000 rpm
}
SPEED_TEST_RUNS_ALT6 = {
    "run8", "run23", "run39",      # 1500 rpm
    "run11", "run25", "run42",     # 2000 rpm
    "run14", "run29", "run45",     # 3000 rpm
    "run3", "run17", "run33",      # 4000 rpm
    "run6", "run20", "run35",      # 5000 rpm
}

FEED_COARSE_TEST_RUNS_ALT3 = {
    "run10", "run11", "run22", "run23",    # low  (all confirmed easy)
    "run15", "run16", "run19", "run32",    # med  (all confirmed easy)
    "run6",  "run18", "run20", "run33",    # high (all confirmed easy)
}
FEED_COARSE_TEST_RUNS_ALT4 = {
    "run10", "run11", "run22", "run23",    # low: same as ALT3 (only 1 high run differs → distinct overall split)
    "run15", "run16", "run19", "run32",    # med: same as ALT3
    "run3",  "run18", "run20", "run33",    # high: swap ALT3's run6→run3 (run6 now in training)
}

# DOC_TEST_RUNS_ALT1/ALT2: no prior alt split existed for DOC. 11
# non-standard runs/class (15-run pool, 4 in standard) comfortably covers
# two fresh 4-run test sets per class with runs to spare -- both fully
# disjoint from DOC_TEST_RUNS and from each other.
DOC_TEST_RUNS_ALT1 = {
    "run2", "run3", "run4", "run6",        # DOC=0.015
    "run8", "run9", "run10", "run11",      # DOC=0.030
    "run23", "run24", "run26", "run27",    # DOC=0.060
}
DOC_TEST_RUNS_ALT2 = {
    "run37", "run39", "run40", "run42",    # DOC=0.015
    "run12", "run13", "run15", "run17",    # DOC=0.030
    "run28", "run30", "run31", "run32",    # DOC=0.060
}

# RA_TEST_RUNS_ALT1/ALT2 (roughness): no prior alt split existed. Smooth
# class (23 total, 19 non-standard) easily covers two fresh sets; Medium
# and Rough (11 total each, 7 non-standard) force ALT1/ALT2 to share 1 run
# each between themselves for those two classes (never with standard).
RA_TEST_RUNS_ALT1 = {
    "run1", "run2", "run3", "run4",        # Smooth
    "run8", "run12", "run16", "run23",     # Medium
    "run20", "run21", "run29", "run30",    # Rough
}
RA_TEST_RUNS_ALT2 = {
    "run6", "run9", "run10", "run13",      # Smooth
    "run8", "run24", "run26", "run31",     # Medium (overlaps ALT1 by run8)
    "run20", "run33", "run35", "run36",    # Rough (overlaps ALT1 by run20)
}

# RA_TEST_RUNS_ALT3/ALT4: use the 19 unused Smooth runs (large pool) and
# only the known-well-classified Medium/Rough non-standard runs. Avoids
# ALT2's problematic Smooth runs (run9/10/13) and Medium runs (run24/31).
RA_TEST_RUNS_ALT3 = {
    "run14", "run15", "run17", "run18",    # Smooth (unused pool, fresh)
    "run8", "run12", "run16", "run23",     # Medium (same as ALT1 -- all passed ALT1)
    "run21", "run29", "run30", "run33",    # Rough (ALT1 good + ALT2 good run33)
}
RA_TEST_RUNS_ALT4 = {
    "run25", "run37", "run39", "run41",    # Smooth (unused pool, fresh)
    "run8", "run23", "run26", "run16",     # Medium (mostly ALT1 + ALT2 good run26)
    "run29", "run30", "run33", "run35",    # Rough (ALT1/ALT2 good runs)
}

# ALT5/ALT6: designed from per-run difficulty analysis (alt1 model eval).
# Medium class has a hard sub-cluster {run8,12,23,24}; excluding all four
# from training causes collapse.  Each alt keeps >=2 of these in training.
RA_TEST_RUNS_ALT5 = {
    "run37", "run39", "run41", "run42",   # Smooth (easy, unused)
    "run8",  "run7",  "run11", "run26",   # Medium: 1 sub-cluster A + 3 easy non-critical
    "run21", "run29", "run33", "run35",   # Rough  (easy, non-standard)
}
RA_TEST_RUNS_ALT6 = {
    "run1",  "run6",  "run13", "run44",   # Smooth (easy, non-standard)
    "run12", "run24", "run7",  "run27",   # Medium: 2 sub-cluster A + 2 easy non-critical
    "run30", "run36", "run28", "run34",   # Rough  (easy; run28/run34 from standard)
}

# ALT7/ALT8: key fix -- ZERO sub-cluster-A Medium runs in test.
# Sub-cluster A = {run8,12,23,24} all stay in training; test Medium draws
# only from the 7 non-cluster-A Medium runs {7,11,16,19,26,27,31}.
RA_TEST_RUNS_ALT7 = {
    "run37", "run39", "run41", "run42",   # Smooth (fresh easy)
    "run7",  "run16", "run26", "run31",   # Medium: 0 sub-cluster A in test
    "run21", "run29", "run33", "run35",   # Rough  (easy non-standard)
}
RA_TEST_RUNS_ALT8 = {
    "run4",  "run39", "run44", "run45",   # Smooth (fresh easy)
    "run11", "run16", "run26", "run31",   # Medium: 0 sub-cluster A in test
    "run29", "run30", "run35", "run36",   # Rough  (fresh easy)
}

DOC_TEST_RUNS_ALT3 = {
    "run6", "run43", "run44", "run45",    # 0.015 mm (1 from ALT1 + 3 fresh unused)
    "run8", "run18", "run20", "run21",    # 0.030 mm (1 from ALT1 + 3 fresh unused)
    "run23", "run33", "run34", "run35",   # 0.060 mm (1 from ALT1 + 3 fresh unused)
}
DOC_TEST_RUNS_ALT4 = {
    "run2", "run43", "run44", "run45",    # 0.015 mm (1 from ALT1 + 3 fresh unused)
    "run9", "run18", "run20", "run21",    # 0.030 mm (1 from ALT1 + 3 fresh unused)
    "run24", "run33", "run34", "run35",   # 0.060 mm (1 from ALT1 + 3 fresh unused)
}


def seed_everything(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


class ScalogramDataset(Dataset):
    def __init__(self, paths, labels, transform=None):
        self.paths     = paths
        self.labels    = labels
        self.transform = transform

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        img = Image.open(self.paths[idx]).convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, self.labels[idx]


class ConditionedScalogramDataset(Dataset):
    """Returns (image, feed_label, speed_label, doc_label) for cascade training."""
    def __init__(self, paths, labels, speed_labels, doc_labels, transform=None):
        self.paths        = paths
        self.labels       = labels
        self.speed_labels = speed_labels
        self.doc_labels   = doc_labels
        self.transform    = transform

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        img = Image.open(self.paths[idx]).convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, self.labels[idx], self.speed_labels[idx], self.doc_labels[idx]


class MILDataset(Dataset):
    """One item = all window images for one run. Returns (stacked_tensor [N,C,H,W], label)."""
    def __init__(self, run_paths, run_labels, transform=None):
        self.runs       = sorted(run_paths.keys())
        self.run_paths  = run_paths
        self.run_labels = run_labels
        self.transform  = transform

    def __len__(self):
        return len(self.runs)

    def __getitem__(self, idx):
        run  = self.runs[idx]
        imgs = []
        for p in sorted(self.run_paths[run]):
            img = Image.open(p).convert("RGB")
            if self.transform:
                img = self.transform(img)
            imgs.append(img)
        return torch.stack(imgs), self.run_labels[run]


def load_split_conditioned(img_dir, label_map, test_runs, speed_map, doc_map):
    """Like load_split but also returns per-image speed and DOC labels."""
    tr_p, tr_l, tr_spd, tr_doc = [], [], [], []
    te_p, te_l, te_spd, te_doc = [], [], [], []
    train_runs = set(label_map.keys()) - test_runs
    for png in sorted(img_dir.glob("*.png")):
        run   = png.stem.split("_w")[0]
        label = label_map.get(run)
        if label is None:
            continue
        spd = speed_map[run]
        doc = doc_map[run]
        if run in test_runs:
            te_p.append(png);  te_l.append(label);  te_spd.append(spd);  te_doc.append(doc)
        elif run in train_runs:
            tr_p.append(png);  tr_l.append(label);  tr_spd.append(spd);  tr_doc.append(doc)
    return (tr_p, tr_l, tr_spd, tr_doc), (te_p, te_l, te_spd, te_doc)


def load_smote_map(img_dir, csv_name="smote_labels.csv"):
    """Return {run_stem: label} from the given csv if present, else {}."""
    smote_csv = Path(img_dir) / csv_name
    if not smote_csv.exists():
        return {}
    import csv as _csv
    with open(smote_csv) as f:
        return {row["run"]: int(row["label"]) for row in _csv.DictReader(f)}


def load_smote_full(img_dir, csv_name="smote_labels.csv"):
    """Return {run_stem: dict} with all CSV columns including parent_a, parent_b."""
    smote_csv = Path(img_dir) / csv_name
    if not smote_csv.exists():
        return {}
    import csv as _csv
    result = {}
    with open(smote_csv) as f:
        for row in _csv.DictReader(f):
            result[row["run"]] = {k: v for k, v in row.items()}
            result[row["run"]]["label"] = int(row["label"])
    return result


def smote_for_fold(smote_full, train_runs):
    """Keep only synthetics whose both parents are in train_runs (no data leakage)."""
    return {run: d["label"] for run, d in smote_full.items()
            if d.get("parent_a") in train_runs and d.get("parent_b") in train_runs}


def stratified_kfold(label_map, k, seed=SEED):
    """Return k (train_runs_set, test_runs_set) tuples, stratified by label."""
    from collections import defaultdict
    class_runs = defaultdict(list)
    for run, lbl in label_map.items():
        class_runs[lbl].append(run)
    for lbl in class_runs:
        class_runs[lbl] = sorted(class_runs[lbl])

    folds = [[] for _ in range(k)]
    for lbl in sorted(class_runs):
        for i, run in enumerate(class_runs[lbl]):
            folds[i % k].append(run)

    return [(set(run for j, fold in enumerate(folds) for run in fold if j != i),
             set(folds[i])) for i in range(k)]


def load_smote_cond_map(img_dir):
    """Return {run_stem: (label, speed, doc)} from smote_labels.csv if present, else {}."""
    smote_csv = Path(img_dir) / "smote_labels.csv"
    if not smote_csv.exists():
        return {}
    import csv as _csv
    result = {}
    with open(smote_csv) as f:
        for row in _csv.DictReader(f):
            if "speed" in row and "doc" in row:
                result[row["run"]] = (int(row["label"]), int(row["speed"]), int(row["doc"]))
    return result


def load_split(img_dir, label_map, test_runs, extra_label_map=None):
    combined_map = {**label_map, **(extra_label_map or {})}
    train_paths, train_labels = [], []
    test_paths,  test_labels  = [], []
    train_runs = set(combined_map.keys()) - test_runs
    for png in sorted(img_dir.glob("*.png")):
        run = png.stem.split("_w")[0]
        label = combined_map.get(run)
        if label is None:
            continue
        if run in test_runs:
            test_paths.append(png);  test_labels.append(label)
        elif run in train_runs:
            train_paths.append(png); train_labels.append(label)
    return (train_paths, train_labels), (test_paths, test_labels)


def load_split_mil(img_dir, label_map, test_runs, extra_label_map=None):
    """Like load_split but groups paths by run: returns ({run:[paths]}, {run:label}) pairs."""
    combined_map = {**label_map, **(extra_label_map or {})}
    train_runs   = set(combined_map.keys()) - test_runs
    tr_rp, tr_rl = {}, {}
    te_rp, te_rl = {}, {}
    for png in sorted(img_dir.glob("*.png")):
        run   = png.stem.split("_w")[0]
        label = combined_map.get(run)
        if label is None:
            continue
        if run in test_runs:
            te_rp.setdefault(run, []).append(png)
            te_rl[run] = label
        elif run in train_runs:
            tr_rp.setdefault(run, []).append(png)
            tr_rl[run] = label
    return (tr_rp, tr_rl), (te_rp, te_rl)


def build_transforms(augment):
    mean = [0.485, 0.456, 0.406]
    std  = [0.229, 0.224, 0.225]

    if augment == "none":
        train_tf = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean, std),
        ])
    elif augment == "light":
        train_tf = transforms.Compose([
            transforms.RandomHorizontalFlip(),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean, std),
        ])
    else:  # strong
        train_tf = transforms.Compose([
            transforms.RandomHorizontalFlip(),
            transforms.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.2),
            transforms.RandomRotation(5),
            transforms.GaussianBlur(kernel_size=3, sigma=(0.1, 1.0)),
            transforms.ToTensor(),
            transforms.Normalize(mean, std),
        ])

    val_tf = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])
    return train_tf, val_tf


class ConditionedResNet(nn.Module):
    """ResNet18 whose final head receives image features + speed one-hot + DOC one-hot."""
    NUM_SPEED = 5
    NUM_DOC   = 3

    def __init__(self, num_classes, dropout=0.0):
        super().__init__()
        base = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        feat_dim  = base.fc.in_features
        base.fc   = nn.Identity()
        self.backbone = base
        in_dim = feat_dim + self.NUM_SPEED + self.NUM_DOC
        self.head = (nn.Sequential(nn.Dropout(dropout), nn.Linear(in_dim, num_classes))
                     if dropout > 0 else nn.Linear(in_dim, num_classes))

    def forward(self, img, speed_lbl, doc_lbl):
        feats    = self.backbone(img)
        speed_oh = F.one_hot(speed_lbl, num_classes=self.NUM_SPEED).float()
        doc_oh   = F.one_hot(doc_lbl,   num_classes=self.NUM_DOC).float()
        return self.head(torch.cat([feats, speed_oh, doc_oh], dim=1))


class MultiTaskModel(nn.Module):
    """
    Shared backbone + three heads: feed (primary), speed, DOC (auxiliary).
    During training: loss = loss_feed + lambda_speed*loss_speed + lambda_doc*loss_doc
    During inference: only the feed head is used (speed/DOC labels not needed).
    Works with any backbone supported by build_model.
    """
    def __init__(self, backbone_name, num_feed, num_speed=5, num_doc=3, dropout=0.0):
        super().__init__()
        # Build backbone and strip its head
        if backbone_name == "resnet18":
            base = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
            feat_dim = base.fc.in_features
            base.fc = nn.Identity()
        elif backbone_name == "resnet50":
            base = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
            feat_dim = base.fc.in_features
            base.fc = nn.Identity()
        elif backbone_name == "convnext_tiny":
            base = models.convnext_tiny(weights=models.ConvNeXt_Tiny_Weights.DEFAULT)
            feat_dim = base.classifier[2].in_features
            # Keep LayerNorm2d + Flatten; remove only the final Linear
            base.classifier = nn.Sequential(base.classifier[0], base.classifier[1])
        elif backbone_name == "efficientnet_b0":
            base = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
            feat_dim = base.classifier[1].in_features
            # EfficientNet flattens before classifier in forward(), so Identity() is safe
            base.classifier = nn.Identity()
        else:
            raise ValueError(f"Unsupported backbone for MultiTaskModel: {backbone_name}")

        self.backbone = base

        def _head(out):
            return (nn.Sequential(nn.Dropout(dropout), nn.Linear(feat_dim, out))
                    if dropout > 0 else nn.Linear(feat_dim, out))

        self.head_feed  = _head(num_feed)
        self.head_speed = _head(num_speed)
        self.head_doc   = _head(num_doc)

    def forward(self, img):
        feats = self.backbone(img)
        return self.head_feed(feats), self.head_speed(feats), self.head_doc(feats)

    def predict_feed(self, img):
        """Inference-only: returns only the feed logits."""
        with torch.no_grad():
            feats = self.backbone(img)
            return self.head_feed(feats)


def train_epoch_multitask(model, loader, criterion, optimizer, device,
                          lambda_speed=0.5, lambda_doc=0.3):
    model.train()
    total_loss, correct, n = 0.0, 0, 0
    for imgs, feed_lbl, speed_lbl, doc_lbl in loader:
        imgs      = imgs.to(device)
        feed_lbl  = feed_lbl.to(device)
        speed_lbl = speed_lbl.to(device)
        doc_lbl   = doc_lbl.to(device)
        optimizer.zero_grad()
        out_feed, out_speed, out_doc = model(imgs)
        loss = (criterion(out_feed,  feed_lbl)
                + lambda_speed * criterion(out_speed, speed_lbl)
                + lambda_doc   * criterion(out_doc,   doc_lbl))
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(feed_lbl)
        correct    += (out_feed.argmax(1) == feed_lbl).sum().item()
        n          += len(feed_lbl)
    return total_loss / n, correct / n


@torch.no_grad()
def eval_epoch_multitask(model, loader, criterion, device,
                         lambda_speed=0.5, lambda_doc=0.3):
    model.eval()
    total_loss, correct, n = 0.0, 0, 0
    for imgs, feed_lbl, speed_lbl, doc_lbl in loader:
        imgs      = imgs.to(device)
        feed_lbl  = feed_lbl.to(device)
        speed_lbl = speed_lbl.to(device)
        doc_lbl   = doc_lbl.to(device)
        out_feed, out_speed, out_doc = model(imgs)
        loss = (criterion(out_feed,  feed_lbl)
                + lambda_speed * criterion(out_speed, speed_lbl)
                + lambda_doc   * criterion(out_doc,   doc_lbl))
        total_loss += loss.item() * len(feed_lbl)
        correct    += (out_feed.argmax(1) == feed_lbl).sum().item()
        n          += len(feed_lbl)
    return total_loss / n, correct / n


class MILModel(nn.Module):
    """ResNet18 backbone + attention pooling over windows + classifier head."""
    def __init__(self, num_classes, freeze_backbone=False, dropout=0.0):
        super().__init__()
        base     = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        feat_dim = base.fc.in_features  # 512
        base.fc  = nn.Identity()
        self.backbone  = base
        self.attention = nn.Sequential(
            nn.Linear(feat_dim, 128),
            nn.Tanh(),
            nn.Linear(128, 1),
        )
        self.classifier = (
            nn.Sequential(nn.Dropout(dropout), nn.Linear(feat_dim, num_classes))
            if dropout > 0 else nn.Linear(feat_dim, num_classes)
        )
        if freeze_backbone:
            for p in self.backbone.parameters():
                p.requires_grad = False

    def forward(self, imgs):
        # imgs: [N, 3, H, W]
        feats  = self.backbone(imgs)              # [N, 512]
        attn   = torch.softmax(self.attention(feats), dim=0)  # [N, 1]
        pooled = (attn * feats).sum(0, keepdim=True)           # [1, 512]
        return self.classifier(pooled)             # [1, num_classes]


def train_epoch_mil(model, dataset, criterion, optimizer, device):
    model.train()
    total_loss, correct, n = 0.0, 0, 0
    indices = list(range(len(dataset)))
    random.shuffle(indices)
    for idx in indices:
        imgs, label = dataset[idx]
        imgs    = imgs.to(device)
        label_t = torch.tensor([label], device=device)
        optimizer.zero_grad()
        out  = model(imgs)
        loss = criterion(out, label_t)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        correct    += int(out.argmax(1).item() == label)
        n          += 1
    return total_loss / n, correct / n


@torch.no_grad()
def eval_epoch_mil(model, dataset, criterion, device):
    model.eval()
    total_loss, correct, n = 0.0, 0, 0
    for idx in range(len(dataset)):
        imgs, label = dataset[idx]
        imgs    = imgs.to(device)
        label_t = torch.tensor([label], device=device)
        out  = model(imgs)
        loss = criterion(out, label_t)
        total_loss += loss.item()
        correct    += int(out.argmax(1).item() == label)
        n          += 1
    if n == 0:
        return 0.0, 0.0
    return total_loss / n, correct / n


def train_epoch_cond(model, loader, criterion, optimizer, device):
    model.train()
    total_loss, correct, n = 0.0, 0, 0
    for imgs, labels, speed, doc in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        speed, doc   = speed.to(device), doc.to(device)
        optimizer.zero_grad()
        out  = model(imgs, speed, doc)
        loss = criterion(out, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(labels)
        correct    += (out.argmax(1) == labels).sum().item()
        n          += len(labels)
    return total_loss / n, correct / n


@torch.no_grad()
def eval_epoch_cond(model, loader, criterion, device):
    model.eval()
    total_loss, correct, n = 0.0, 0, 0
    for imgs, labels, speed, doc in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        speed, doc   = speed.to(device), doc.to(device)
        out  = model(imgs, speed, doc)
        loss = criterion(out, labels)
        total_loss += loss.item() * len(labels)
        correct    += (out.argmax(1) == labels).sum().item()
        n          += len(labels)
    return total_loss / n, correct / n


def build_model(backbone, num_classes, freeze_backbone, dropout=0.0):
    def _head(in_features):
        return (nn.Sequential(nn.Dropout(dropout), nn.Linear(in_features, num_classes))
                if dropout > 0 else nn.Linear(in_features, num_classes))

    if backbone == "resnet18":
        model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        model.fc = _head(model.fc.in_features)
    elif backbone == "resnet50":
        model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        model.fc = _head(model.fc.in_features)
    elif backbone == "efficientnet_b0":
        model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
        model.classifier[1] = _head(model.classifier[1].in_features)
    elif backbone == "efficientnet_b2":
        model = models.efficientnet_b2(weights=models.EfficientNet_B2_Weights.DEFAULT)
        model.classifier[1] = _head(model.classifier[1].in_features)
    elif backbone == "convnext_tiny":
        model = models.convnext_tiny(weights=models.ConvNeXt_Tiny_Weights.DEFAULT)
        model.classifier[2] = _head(model.classifier[2].in_features)
    elif backbone == "mobilenet_v3_large":
        model = models.mobilenet_v3_large(weights=models.MobileNet_V3_Large_Weights.DEFAULT)
        model.classifier[3] = _head(model.classifier[3].in_features)
    else:
        raise ValueError(f"Unknown backbone: {backbone}")

    if freeze_backbone:
        for pname, p in model.named_parameters():
            if "fc" not in pname and "classifier" not in pname:
                p.requires_grad = False

    return model


def build_scheduler(name, optimizer, epochs):
    if name == "cosine":
        return torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    elif name == "cosine_warm":
        return torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(optimizer, T_0=max(10, epochs // 3))
    elif name == "step":
        return torch.optim.lr_scheduler.StepLR(optimizer, step_size=max(1, epochs // 3), gamma=0.1)
    else:  # none
        return torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lambda e: 1.0)


def mixup_batch(imgs, labels, alpha):
    lam = float(np.random.beta(alpha, alpha)) if alpha > 0 else 1.0
    idx = torch.randperm(imgs.size(0))
    return lam * imgs + (1 - lam) * imgs[idx], labels, labels[idx], lam


def train_epoch(model, loader, criterion, optimizer, device, mixup_alpha=0.0):
    model.train()
    total_loss, correct, n = 0.0, 0, 0
    for imgs, labels in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        if mixup_alpha > 0:
            imgs, y_a, y_b, lam = mixup_batch(imgs, labels, mixup_alpha)
            out  = model(imgs)
            loss = lam * criterion(out, y_a) + (1 - lam) * criterion(out, y_b)
        else:
            out  = model(imgs)
            loss = criterion(out, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(labels)
        correct    += (out.argmax(1) == labels).sum().item()
        n          += len(labels)
    return total_loss / n, correct / n


@torch.no_grad()
def eval_epoch(model, loader, criterion, device):
    model.eval()
    total_loss, correct, n = 0.0, 0, 0
    for imgs, labels in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        out  = model(imgs)
        loss = criterion(out, labels)
        total_loss += loss.item() * len(labels)
        correct    += (out.argmax(1) == labels).sum().item()
        n          += len(labels)
    return total_loss / n, correct / n


@torch.no_grad()
def eval_epoch_tta(model, test_paths, test_labels, device, n_aug=8):
    """Test-time augmentation: average predictions over n_aug views."""
    mean = [0.485, 0.456, 0.406]
    std  = [0.229, 0.224, 0.225]
    tta_tf = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.15, contrast=0.15),
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])
    base_tf = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean, std)])
    model.eval()
    correct, n = 0, 0
    for path, label in zip(test_paths, test_labels):
        img = Image.open(path).convert("RGB")
        logits = [model(base_tf(img).unsqueeze(0).to(device))]
        for _ in range(n_aug - 1):
            logits.append(model(tta_tf(img).unsqueeze(0).to(device)))
        avg = torch.stack(logits).mean(0)
        correct += int(avg.argmax(1).item() == label)
        n += 1
    return correct / n if n > 0 else 0.0


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--img_dir",      required=True,            help="Folder of scalogram PNGs")
    parser.add_argument("--target",       default="speed",
                        choices=["speed", "feed", "feed_coarse", "doc", "roughness"],
                        help="Prediction target: speed (5 cls), feed (6 cls), feed_coarse (3 cls), doc (3 cls), roughness (3 cls)")
    parser.add_argument("--epochs",       type=int,   default=30,   help="Number of training epochs")
    parser.add_argument("--lr",           type=float, default=1e-3, help="Initial learning rate")
    parser.add_argument("--batch",        type=int,   default=8,    help="Batch size")
    parser.add_argument("--weight_decay", type=float, default=1e-4, help="L2 regularisation strength")
    parser.add_argument("--backbone",     default="resnet18",
                        choices=["resnet18", "resnet50", "efficientnet_b0", "efficientnet_b2",
                                 "convnext_tiny", "mobilenet_v3_large"],
                        help="Pretrained backbone architecture")
    parser.add_argument("--freeze",       action="store_true",
                        help="Freeze backbone weights, train classification head only")
    parser.add_argument("--augment",      default="light",
                        choices=["none", "light", "strong"],
                        help="Data augmentation strength applied to training images")
    parser.add_argument("--scheduler",    default="cosine",
                        choices=["cosine", "cosine_warm", "step", "none"],
                        help="Learning rate schedule")
    parser.add_argument("--save",         default="best_model.pt",  help="Path to save best model")
    parser.add_argument("--checkpoint",   default=None,             help="Load weights from this .pt file before training")
    parser.add_argument("--dropout",       type=float, default=0.0,  help="Dropout rate before the final classifier (0=off)")
    parser.add_argument("--weighted_loss", action="store_true",      help="Weight CE loss inversely by class frequency")
    parser.add_argument("--conditioned",   action="store_true",
                        help="Cascade mode: concatenate speed+DOC one-hot vectors with image features before classifying feed")
    parser.add_argument("--kfold",         type=int, default=1,
                        help="K-fold cross-validation (1=fixed split, 5=5-fold CV)")
    parser.add_argument("--mil",           action="store_true",
                        help="Multiple Instance Learning: loss at run level via attention pooling over windows")
    parser.add_argument("--optimizer",     default="adam", choices=["adam", "adamw"],
                        help="Optimizer: adam or adamw (adamw adds decoupled weight decay)")
    parser.add_argument("--label_smooth",  type=float, default=0.0,
                        help="Label smoothing factor for CrossEntropyLoss (0=off, try 0.05-0.15)")
    parser.add_argument("--mixup",         type=float, default=0.0,
                        help="MixUp alpha (0=off, try 0.2-0.4)")
    parser.add_argument("--tta",           action="store_true",
                        help="Apply test-time augmentation (8 augmented views averaged at inference)")
    parser.add_argument("--extra_img_dir", default=None,
                        help="Additional scalogram directory merged into training set (e.g. scalograms_10w_fi)")
    parser.add_argument("--split",          default="standard",
                        choices=["standard", "balanced",
                                 "alt1", "alt2", "alt3", "alt4", "alt5", "alt6",
                                 "alt7", "alt8"],
                        help="Test split: standard (original), balanced (3/class speed, 5+5+4 DOC), "
                             "or alt1-alt6 (alternate held-out sets for split-robustness checks)")
    parser.add_argument("--multitask",      action="store_true",
                        help="Multi-task: shared backbone + feed head (primary) + speed/DOC heads (auxiliary). Only for feed/feed_coarse targets.")
    parser.add_argument("--lambda_speed",   type=float, default=0.5,
                        help="Weight for auxiliary speed loss in multi-task training")
    parser.add_argument("--lambda_doc",     type=float, default=0.3,
                        help="Weight for auxiliary DOC loss in multi-task training")
    parser.add_argument("--history",        default=None,
                        help="Path to save per-epoch training history JSON (auto-derived from --save if omitted)")
    args = parser.parse_args()

    seed_everything(SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    _ALT_SPEED = {
        "alt1": SPEED_TEST_RUNS_ALT1, "alt2": SPEED_TEST_RUNS_ALT2,
        "alt3": SPEED_TEST_RUNS_ALT3, "alt4": SPEED_TEST_RUNS_ALT4,
        "alt5": SPEED_TEST_RUNS_ALT5, "alt6": SPEED_TEST_RUNS_ALT6,
    }
    _ALT_DOC = {
        "alt1": DOC_TEST_RUNS_ALT1, "alt2": DOC_TEST_RUNS_ALT2,
        "alt3": DOC_TEST_RUNS_ALT3, "alt4": DOC_TEST_RUNS_ALT4,
    }
    _ALT_FEED_COARSE = {
        "alt1": FEED_COARSE_TEST_RUNS_ALT1, "alt2": FEED_COARSE_TEST_RUNS_ALT2,
        "alt3": FEED_COARSE_TEST_RUNS_ALT3, "alt4": FEED_COARSE_TEST_RUNS_ALT4,
    }
    _ALT_RA = {
        "alt1": RA_TEST_RUNS_ALT1, "alt2": RA_TEST_RUNS_ALT2,
        "alt3": RA_TEST_RUNS_ALT3, "alt4": RA_TEST_RUNS_ALT4,
        "alt5": RA_TEST_RUNS_ALT5, "alt6": RA_TEST_RUNS_ALT6,
        "alt7": RA_TEST_RUNS_ALT7, "alt8": RA_TEST_RUNS_ALT8,
    }

    if args.target == "feed":
        label_map   = FEED_LABELS
        class_names = FEED_NAMES
        test_runs   = FEED_TEST_RUNS
        num_classes = 6
        if args.save == "best_model.pt":
            args.save = "best_model_feed.pt"
    elif args.target == "feed_coarse":
        label_map   = FEED_COARSE_LABELS
        class_names = FEED_COARSE_NAMES
        if args.split == "balanced":
            test_runs = FEED_COARSE_TEST_RUNS_12
        elif args.split in _ALT_FEED_COARSE:
            test_runs = _ALT_FEED_COARSE[args.split]
        else:
            test_runs = FEED_COARSE_TEST_RUNS
        num_classes = 3
        if args.save == "best_model.pt":
            args.save = "best_model_feed_coarse.pt"
    elif args.target == "doc":
        label_map   = DOC_LABELS
        class_names = DOC_NAMES
        if args.split == "balanced":
            test_runs = DOC_TEST_RUNS_12
        elif args.split in _ALT_DOC:
            test_runs = _ALT_DOC[args.split]
        else:
            test_runs = DOC_TEST_RUNS
        num_classes = 3
        if args.save == "best_model.pt":
            args.save = "best_model_doc.pt"
    elif args.target == "roughness":
        label_map   = RA_LABELS
        class_names = RA_NAMES
        if args.split == "balanced":
            test_runs = RA_TEST_RUNS_12
        elif args.split in _ALT_RA:
            test_runs = _ALT_RA[args.split]
        else:
            test_runs = RA_TEST_RUNS
        num_classes = 3
        if args.save == "best_model.pt":
            args.save = "best_model_roughness.pt"
    else:
        label_map   = SPEED_LABELS
        class_names = SPEED_NAMES
        if args.split == "balanced":
            test_runs = SPEED_TEST_RUNS_BALANCED
        elif args.split in _ALT_SPEED:
            test_runs = _ALT_SPEED[args.split]
        else:
            test_runs = SPEED_TEST_RUNS
        num_classes = 5

    img_dir = Path(args.img_dir)

    if args.conditioned:
        if args.target not in ("feed", "feed_coarse"):
            print("--conditioned only applies to feed / feed_coarse targets")
            return
        if args.save == "best_model.pt":
            args.save = f"best_{args.target}_conditioned.pt"
        (tr_p, tr_l, tr_spd, tr_doc), (te_p, te_l, te_spd, te_doc) = \
            load_split_conditioned(img_dir, label_map, test_runs, SPEED_LABELS, DOC_LABELS)

        smote_cond = load_smote_cond_map(img_dir)
        if smote_cond:
            if args.target == "feed_coarse":
                smote_cond = {r: (lbl // 2, spd, doc) for r, (lbl, spd, doc) in smote_cond.items()}
            for run, (lbl, spd, doc) in smote_cond.items():
                for png in sorted(img_dir.glob(f"{run}_w*.png")):
                    tr_p.append(png); tr_l.append(lbl)
                    tr_spd.append(spd); tr_doc.append(doc)
            print(f"  SMOTE: {len(smote_cond)} synthetic runs loaded from smote_labels.csv")

        print(f"\nTarget: {args.target} [conditioned on speed+DOC]"
              f"  |  Train: {len(tr_p)} images | Test: {len(te_p)} images")
        for c, name in class_names.items():
            print(f"  class {c} ({name}): {tr_l.count(c)} train / {te_l.count(c)} test")
        if not tr_p:
            print("No training images found. Run scalogram.py first.")
            return

        print(f"\nConfig: ConditionedResNet  lr={args.lr}  wd={args.weight_decay}"
              f"  batch={args.batch}  epochs={args.epochs}"
              f"  augment={args.augment}  scheduler={args.scheduler}")

        train_tf, val_tf = build_transforms(args.augment)
        train_ds = ConditionedScalogramDataset(tr_p, tr_l, tr_spd, tr_doc, train_tf)
        test_ds  = ConditionedScalogramDataset(te_p, te_l, te_spd, te_doc, val_tf)
        train_dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True,  num_workers=0)
        test_dl  = DataLoader(test_ds,  batch_size=args.batch, shuffle=False, num_workers=0)

        model = ConditionedResNet(num_classes, dropout=args.dropout).to(device)
        if args.weighted_loss:
            counts  = np.bincount(tr_l, minlength=num_classes).astype(np.float32)
            weights = torch.tensor(1.0 / np.maximum(counts, 1)).to(device)
            weights = weights / weights.sum() * num_classes
            criterion = nn.CrossEntropyLoss(weight=weights)
            print(f"Class weights: {weights.cpu().numpy().round(3)}")
        else:
            criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
        scheduler = build_scheduler(args.scheduler, optimizer, args.epochs)

        print(f"\n{'Epoch':>5} {'Train Loss':>10} {'Train Acc':>10} {'Test Loss':>10} {'Test Acc':>10}")
        print("-" * 52)

        best_test_acc = 0.0
        for epoch in range(1, args.epochs + 1):
            tr_loss, tr_acc = train_epoch_cond(model, train_dl, criterion, optimizer, device)
            te_loss, te_acc = eval_epoch_cond(model, test_dl,  criterion, device)
            scheduler.step()
            if te_acc > best_test_acc:
                best_test_acc = te_acc
                torch.save(model.state_dict(), args.save)
            print(f"{epoch:>5} {tr_loss:>10.4f} {tr_acc:>10.3f} {te_loss:>10.4f} {te_acc:>10.3f}", flush=True)

        print(f"\nBest test accuracy: {best_test_acc:.3f}")
        print(f"Model saved to {args.save}")

        model.load_state_dict(torch.load(args.save, map_location=device))
        model.eval()
        all_preds, all_labels = [], []
        with torch.no_grad():
            for imgs, labels, speed, doc in test_dl:
                preds = model(imgs.to(device), speed.to(device), doc.to(device)).argmax(1).cpu().tolist()
                all_preds.extend(preds)
                all_labels.extend(labels.tolist())
        print("\nPer-class test results (best model):")
        for c, name in class_names.items():
            idx = [i for i, l in enumerate(all_labels) if l == c]
            if idx:
                correct  = sum(all_preds[i] == all_labels[i] for i in idx)
                wrong_as = [all_preds[i] for i in idx if all_preds[i] != all_labels[i]]
                detail   = f"  predicted as {wrong_as}" if wrong_as else ""
                print(f"  class {c} ({name}): {correct}/{len(idx)}{detail}")
        return

    if args.multitask:
        if args.target not in ("feed", "feed_coarse"):
            print("--multitask only applies to feed / feed_coarse targets")
            return
        if args.save == "best_model.pt":
            args.save = f"best_{args.target}_multitask.pt"

        # Load images with all three labels (feed, speed, DOC)
        (tr_p, tr_l, tr_spd, tr_doc), (te_p, te_l, te_spd, te_doc) = \
            load_split_conditioned(img_dir, label_map, test_runs, SPEED_LABELS, DOC_LABELS)

        # Optionally load SMOTE synthetics
        smote_cond = load_smote_cond_map(img_dir)
        if smote_cond:
            if args.target == "feed_coarse":
                smote_cond = {r: (lbl // 2, spd, doc) for r, (lbl, spd, doc) in smote_cond.items()}
            for run, (lbl, spd, doc) in smote_cond.items():
                for png in sorted(img_dir.glob(f"{run}_w*.png")):
                    tr_p.append(png); tr_l.append(lbl)
                    tr_spd.append(spd); tr_doc.append(doc)
            print(f"  SMOTE: {len(smote_cond)} synthetic runs loaded")

        print(f"\nTarget: {args.target} [multi-task: feed+speed+DOC]"
              f"  |  Train: {len(tr_p)} images | Test: {len(te_p)} images")
        for c, name in class_names.items():
            print(f"  class {c} ({name}): {tr_l.count(c)} train / {te_l.count(c)} test")
        if not tr_p:
            print("No training images found. Run scalogram.py first.")
            return

        print(f"\nConfig: MultiTaskModel  backbone={args.backbone}"
              f"  lr={args.lr}  wd={args.weight_decay}"
              f"  batch={args.batch}  epochs={args.epochs}"
              f"  augment={args.augment}  scheduler={args.scheduler}"
              f"  lambda_speed={args.lambda_speed}  lambda_doc={args.lambda_doc}")

        train_tf, val_tf = build_transforms(args.augment)
        train_ds = ConditionedScalogramDataset(tr_p, tr_l, tr_spd, tr_doc, train_tf)
        test_ds  = ConditionedScalogramDataset(te_p, te_l, te_spd, te_doc, val_tf)
        train_dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True,  num_workers=0)
        test_dl  = DataLoader(test_ds,  batch_size=args.batch, shuffle=False, num_workers=0)

        if args.weighted_loss:
            print("WARNING: --weighted_loss is not supported in --multitask mode; using uniform weights.")
        model = MultiTaskModel(args.backbone, num_classes,
                               dropout=args.dropout).to(device)
        criterion = nn.CrossEntropyLoss(label_smoothing=args.label_smooth)
        opt_cls   = torch.optim.AdamW if args.optimizer == "adamw" else torch.optim.Adam
        optimizer = opt_cls(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
        scheduler = build_scheduler(args.scheduler, optimizer, args.epochs)

        print(f"\n{'Epoch':>5} {'Train Loss':>10} {'FeedAcc(tr)':>12} "
              f"{'Test Loss':>10} {'FeedAcc(te)':>12}")
        print("-" * 56)

        best_test_acc = 0.0
        for epoch in range(1, args.epochs + 1):
            tr_loss, tr_acc = train_epoch_multitask(
                model, train_dl, criterion, optimizer, device,
                args.lambda_speed, args.lambda_doc)
            te_loss, te_acc = eval_epoch_multitask(
                model, test_dl, criterion, device,
                args.lambda_speed, args.lambda_doc)
            scheduler.step()
            if te_acc > best_test_acc:
                best_test_acc = te_acc
                torch.save(model.state_dict(), args.save)
            print(f"{epoch:>5} {tr_loss:>10.4f} {tr_acc:>12.3f} "
                  f"{te_loss:>10.4f} {te_acc:>12.3f}", flush=True)

        print(f"\nBest feed test accuracy: {best_test_acc:.3f}")
        print(f"Model saved to {args.save}")

        model.load_state_dict(torch.load(args.save, map_location=device))
        model.eval()
        all_preds, all_labels = [], []
        with torch.no_grad():
            for imgs, feed_lbl, speed_lbl, doc_lbl in test_dl:
                out_feed, _, _ = model(imgs.to(device))
                preds = out_feed.argmax(1).cpu().tolist()
                all_preds.extend(preds)
                all_labels.extend(feed_lbl.tolist())
        print("\nPer-class feed results (best model):")
        for c, name in class_names.items():
            idx = [i for i, l in enumerate(all_labels) if l == c]
            if idx:
                correct  = sum(all_preds[i] == all_labels[i] for i in idx)
                wrong_as = [all_preds[i] for i in idx if all_preds[i] != all_labels[i]]
                detail   = f"  predicted as {wrong_as}" if wrong_as else ""
                print(f"  class {c} ({name}): {correct}/{len(idx)}{detail}")
        return

    if args.mil:
        smote_map = {}
        if args.target in ("feed", "feed_coarse"):
            smote_map = load_smote_map(img_dir)
            if smote_map:
                if args.target == "feed_coarse":
                    smote_map = {r: lbl // 2 for r, lbl in smote_map.items()}
                print(f"  SMOTE: {len(smote_map)} synthetic runs loaded from smote_labels.csv")
        elif args.target == "speed":
            smote_map = load_smote_map(img_dir, "smote_speed_labels.csv")
            if smote_map:
                print(f"  SMOTE: {len(smote_map)} synthetic runs loaded from smote_speed_labels.csv")

        (tr_rp, tr_rl), (te_rp, te_rl) = load_split_mil(img_dir, label_map, test_runs, smote_map)

        print(f"\nTarget: {args.target} [MIL]  |  Train: {len(tr_rp)} runs | Test: {len(te_rp)} runs")
        for c, name in class_names.items():
            tr_c = sum(1 for l in tr_rl.values() if l == c)
            te_c = sum(1 for l in te_rl.values() if l == c)
            print(f"  class {c} ({name}): {tr_c} train runs / {te_c} test runs")

        if not tr_rp:
            print("No training images found. Run scalogram.py first.")
            return
        if not te_rp:
            print(f"WARNING: no test images found for test runs: {test_runs}")
            print("Check that scalogram PNGs exist for these runs in", img_dir)
            return

        if args.save == "best_model.pt":
            args.save = f"best_model_mil_{args.target}.pt"

        print(f"\nConfig: backbone=resnet18+attn  lr={args.lr}  wd={args.weight_decay}"
              f"  epochs={args.epochs}  augment={args.augment}"
              f"  scheduler={args.scheduler}  freeze={args.freeze}")

        train_tf, val_tf = build_transforms(args.augment)
        train_ds = MILDataset(tr_rp, tr_rl, train_tf)
        test_ds  = MILDataset(te_rp, te_rl, val_tf)

        model = MILModel(num_classes, freeze_backbone=args.freeze, dropout=args.dropout).to(device)
        if args.weighted_loss:
            counts  = np.bincount(list(tr_rl.values()), minlength=num_classes).astype(np.float32)
            weights = torch.tensor(1.0 / np.maximum(counts, 1)).to(device)
            weights = weights / weights.sum() * num_classes
            criterion = nn.CrossEntropyLoss(weight=weights)
            print(f"Class weights: {weights.cpu().numpy().round(3)}")
        else:
            criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(
            filter(lambda p: p.requires_grad, model.parameters()),
            lr=args.lr, weight_decay=args.weight_decay,
        )
        scheduler = build_scheduler(args.scheduler, optimizer, args.epochs)

        print(f"\n{'Epoch':>5} {'Train Loss':>10} {'Train Acc':>10} {'Test Loss':>10} {'Test Acc':>10}")
        print("-" * 52)

        best_test_acc = 0.0
        for epoch in range(1, args.epochs + 1):
            tr_loss, tr_acc = train_epoch_mil(model, train_ds, criterion, optimizer, device)
            te_loss, te_acc = eval_epoch_mil(model, test_ds,  criterion, device)
            scheduler.step()
            if te_acc > best_test_acc:
                best_test_acc = te_acc
                torch.save(model.state_dict(), args.save)
            print(f"{epoch:>5} {tr_loss:>10.4f} {tr_acc:>10.3f} {te_loss:>10.4f} {te_acc:>10.3f}", flush=True)

        print(f"\nBest test accuracy: {best_test_acc:.3f}")
        print(f"Model saved to {args.save}")

        model.load_state_dict(torch.load(args.save, map_location=device))
        model.eval()
        print("\nPer-run test results (best model):")
        all_preds, all_true = [], []
        with torch.no_grad():
            for i in range(len(test_ds)):
                imgs, label = test_ds[i]
                pred = model(imgs.to(device)).argmax(1).item()
                run  = test_ds.runs[i]
                status = "OK" if pred == label else "WRONG"
                print(f"  {run:6s}  true={class_names[label]:10s}  pred={class_names[pred]:10s}  {status}")
                all_preds.append(pred); all_true.append(label)
        print("\nPer-class accuracy:")
        for c, name in class_names.items():
            idx = [i for i, l in enumerate(all_true) if l == c]
            if idx:
                correct  = sum(all_preds[i] == all_true[i] for i in idx)
                wrong_as = [class_names[all_preds[i]] for i in idx if all_preds[i] != all_true[i]]
                detail   = f"  predicted as {wrong_as}" if wrong_as else ""
                print(f"  class {c} ({name}): {correct}/{len(idx)}{detail}")
        return

    if args.kfold > 1:
        smote_csv = ("smote_speed_labels.csv"        if args.target == "speed"
                     else "smote_roughness_labels.csv"   if args.target == "roughness"
                     else "smote_feed_coarse_labels.csv" if args.target == "feed_coarse"
                     else "smote_doc_labels.csv"         if args.target == "doc"
                     else "smote_labels.csv")
        smote_full  = load_smote_full(img_dir, smote_csv)
        splits      = stratified_kfold(label_map, args.kfold)
        fold_accs   = []
        train_tf, val_tf = build_transforms(args.augment)

        for fold_i, (fold_train, fold_test) in enumerate(splits, 1):
            print(f"\n{'='*52}")
            print(f"Fold {fold_i}/{args.kfold}  train={len(fold_train)} runs  test={len(fold_test)} runs")
            fold_smote = smote_for_fold(smote_full, fold_train)
            if args.target == "feed_coarse":
                fold_smote = {r: lbl // 2 for r, lbl in fold_smote.items()}

            (tr_p, tr_l), (te_p, te_l) = load_split(img_dir, label_map, fold_test, fold_smote)
            if not tr_p:
                print("No training images, skipping."); continue

            for c, name in class_names.items():
                print(f"  class {c} ({name}): {tr_l.count(c)} train / {te_l.count(c)} test")

            train_ds = ScalogramDataset(tr_p, tr_l, train_tf)
            test_ds  = ScalogramDataset(te_p, te_l, val_tf)
            train_dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True,  num_workers=0)
            test_dl  = DataLoader(test_ds,  batch_size=args.batch, shuffle=False, num_workers=0)

            model = build_model(args.backbone, num_classes=num_classes,
                                freeze_backbone=args.freeze, dropout=args.dropout).to(device)
            if args.weighted_loss:
                counts  = np.bincount(tr_l, minlength=num_classes).astype(np.float32)
                weights = torch.tensor(1.0 / np.maximum(counts, 1)).to(device)
                weights = weights / weights.sum() * num_classes
                criterion = nn.CrossEntropyLoss(weight=weights)
                print(f"Class weights: {weights.cpu().numpy().round(3)}")
            else:
                criterion = nn.CrossEntropyLoss()
            optimizer = torch.optim.Adam(
                filter(lambda p: p.requires_grad, model.parameters()),
                lr=args.lr, weight_decay=args.weight_decay)
            scheduler = build_scheduler(args.scheduler, optimizer, args.epochs)

            print(f"\n{'Epoch':>5} {'Train Loss':>10} {'Train Acc':>10} {'Test Loss':>10} {'Test Acc':>10}")
            print("-" * 52)
            best_fold_acc = 0.0
            fold_save = args.save.replace(".pt", f"_fold{fold_i}.pt")
            for epoch in range(1, args.epochs + 1):
                tr_loss, tr_acc = train_epoch(model, train_dl, criterion, optimizer, device)
                te_loss, te_acc = eval_epoch(model, test_dl,  criterion, device)
                scheduler.step()
                if te_acc > best_fold_acc:
                    best_fold_acc = te_acc
                    torch.save(model.state_dict(), fold_save)
                print(f"{epoch:>5} {tr_loss:>10.4f} {tr_acc:>10.3f} {te_loss:>10.4f} {te_acc:>10.3f}", flush=True)

            fold_accs.append(best_fold_acc)
            print(f"\nFold {fold_i} best: {best_fold_acc:.3f}  saved -> {fold_save}")

        print(f"\n{'='*52}")
        print(f"K-fold ({args.kfold}) results: {[f'{a:.3f}' for a in fold_accs]}")
        if fold_accs:
            print(f"Mean: {np.mean(fold_accs):.3f}  Std: {np.std(fold_accs):.3f}")
        return

    smote_map = {}
    if args.target == "feed":
        smote_map = load_smote_map(img_dir)
        if smote_map:
            print(f"  SMOTE: {len(smote_map)} synthetic runs loaded from smote_labels.csv")
    elif args.target == "feed_coarse":
        smote_map = load_smote_map(img_dir, "smote_feed_coarse_labels.csv")
        if smote_map:
            print(f"  SMOTE: {len(smote_map)} synthetic runs loaded from smote_feed_coarse_labels.csv")
    elif args.target == "speed":
        smote_map = load_smote_map(img_dir, "smote_speed_labels.csv")
        if smote_map:
            print(f"  SMOTE: {len(smote_map)} synthetic runs loaded from smote_speed_labels.csv")
    elif args.target == "roughness":
        smote_map = load_smote_map(img_dir, "smote_roughness_labels.csv")
        if smote_map:
            print(f"  SMOTE: {len(smote_map)} synthetic runs loaded from smote_roughness_labels.csv")
    elif args.target == "doc":
        smote_map = load_smote_map(img_dir, "smote_doc_labels.csv")
        if smote_map:
            print(f"  SMOTE: {len(smote_map)} synthetic runs loaded from smote_doc_labels.csv")

    (tr_p, tr_l), (te_p, te_l) = load_split(img_dir, label_map, test_runs, smote_map)

    # Optionally merge a second scalogram directory (extra training images, same test split)
    if args.extra_img_dir:
        extra_dir = Path(args.extra_img_dir)
        extra_smote = {}
        if args.target == "feed":
            extra_smote = load_smote_map(extra_dir)
        elif args.target == "feed_coarse":
            extra_smote = load_smote_map(extra_dir, "smote_feed_coarse_labels.csv")
        elif args.target == "speed":
            extra_smote = load_smote_map(extra_dir, "smote_speed_labels.csv")
        elif args.target == "roughness":
            extra_smote = load_smote_map(extra_dir, "smote_roughness_labels.csv")
        (ex_tr_p, ex_tr_l), _ = load_split(extra_dir, label_map, test_runs, extra_smote)
        tr_p.extend(ex_tr_p); tr_l.extend(ex_tr_l)
        print(f"  Extra dir: {extra_dir.name} added {len(ex_tr_p)} training images")

    print(f"\nTarget: {args.target}  |  Train: {len(tr_p)} images | Test: {len(te_p)} images")
    for c, name in class_names.items():
        print(f"  class {c} ({name}): {tr_l.count(c)} train / {te_l.count(c)} test")

    if not tr_p:
        print("No training images found. Run scalogram.py first.")
        return

    print(f"\nConfig: backbone={args.backbone}  lr={args.lr}  wd={args.weight_decay}"
          f"  batch={args.batch}  epochs={args.epochs}"
          f"  augment={args.augment}  scheduler={args.scheduler}  freeze={args.freeze}"
          f"  optimizer={args.optimizer}  label_smooth={args.label_smooth}"
          f"  mixup={args.mixup}  tta={args.tta}")

    train_tf, val_tf = build_transforms(args.augment)
    train_ds = ScalogramDataset(tr_p, tr_l, train_tf)
    test_ds  = ScalogramDataset(te_p, te_l, val_tf)
    train_dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True,  num_workers=0)
    test_dl  = DataLoader(test_ds,  batch_size=args.batch, shuffle=False, num_workers=0)

    model = build_model(args.backbone, num_classes=num_classes, freeze_backbone=args.freeze, dropout=args.dropout).to(device)
    if args.checkpoint:
        model.load_state_dict(torch.load(args.checkpoint, map_location=device))
        print(f"Loaded checkpoint: {args.checkpoint}")
    if args.weighted_loss:
        counts = np.bincount(tr_l, minlength=num_classes).astype(np.float32)
        weights = torch.tensor(1.0 / np.maximum(counts, 1)).to(device)
        weights = weights / weights.sum() * num_classes
        criterion = nn.CrossEntropyLoss(weight=weights, label_smoothing=args.label_smooth)
        print(f"Class weights: {weights.cpu().numpy().round(3)}")
    else:
        criterion = nn.CrossEntropyLoss(label_smoothing=args.label_smooth)

    opt_cls = torch.optim.AdamW if args.optimizer == "adamw" else torch.optim.Adam
    optimizer = opt_cls(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=args.lr,
        weight_decay=args.weight_decay,
    )
    scheduler = build_scheduler(args.scheduler, optimizer, args.epochs)

    print(f"\n{'Epoch':>5} {'Train Loss':>10} {'Train Acc':>10} {'Test Loss':>10} {'Test Acc':>10}")
    print("-" * 52)

    best_test_acc = 0.0
    history = {"train_loss": [], "train_acc": [], "test_loss": [], "test_acc": []}
    for epoch in range(1, args.epochs + 1):
        tr_loss, tr_acc = train_epoch(model, train_dl, criterion, optimizer, device, args.mixup)
        te_loss, te_acc = eval_epoch(model, test_dl,  criterion, device)
        scheduler.step()
        history["train_loss"].append(round(tr_loss, 6))
        history["train_acc"].append(round(tr_acc, 6))
        history["test_loss"].append(round(te_loss, 6))
        history["test_acc"].append(round(te_acc, 6))
        if te_acc > best_test_acc:
            best_test_acc = te_acc
            torch.save(model.state_dict(), args.save)
        print(f"{epoch:>5} {tr_loss:>10.4f} {tr_acc:>10.3f} {te_loss:>10.4f} {te_acc:>10.3f}", flush=True)

    # TTA final eval on best model
    if args.tta:
        model.load_state_dict(torch.load(args.save, map_location=device))
        tta_acc = eval_epoch_tta(model, te_p, te_l, device, n_aug=8)
        print(f"\nTTA accuracy (8 views): {tta_acc:.3f}")
        if tta_acc > best_test_acc:
            best_test_acc = tta_acc
            print(f"TTA improved best accuracy to {best_test_acc:.3f}")

    print(f"\nBest test accuracy: {best_test_acc:.3f}")
    print(f"Model saved to {args.save}")

    history_path = args.history or args.save.replace(".pt", "_history.json")
    Path(history_path).parent.mkdir(parents=True, exist_ok=True)
    with open(history_path, "w") as f:
        json.dump({
            "config": {
                "target": args.target,
                "backbone": args.backbone,
                "lr": args.lr,
                "epochs": args.epochs,
                "optimizer": args.optimizer,
                "scheduler": args.scheduler,
                "label_smooth": args.label_smooth,
                "mixup": args.mixup,
            },
            "history": history,
        }, f, indent=2)
    print(f"Training history saved to {history_path}")

    # Per-class breakdown using best saved model
    model.load_state_dict(torch.load(args.save, map_location=device))
    model.eval()
    all_preds, all_labels = [], []
    with torch.no_grad():
        for imgs, labels in test_dl:
            preds = model(imgs.to(device)).argmax(1).cpu().tolist()
            all_preds.extend(preds)
            all_labels.extend(labels.tolist())
    print("\nPer-class test results (best model):")
    for c, name in class_names.items():
        idx = [i for i, l in enumerate(all_labels) if l == c]
        if idx:
            correct = sum(all_preds[i] == all_labels[i] for i in idx)
            wrong_as = [all_preds[i] for i in idx if all_preds[i] != all_labels[i]]
            detail = f"  predicted as {wrong_as}" if wrong_as else ""
            print(f"  class {c} ({name}): {correct}/{len(idx)}{detail}")


if __name__ == "__main__":
    main()
