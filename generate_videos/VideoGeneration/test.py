import frame_makers

import argparse
import csv
import os

import numpy as np
import mat_file_funcs
import shutil
import scipy.io
from tqdm import tqdm




inputdir = "/Volumes/multiwork/"
permsdir = '/Volumes/space/spcaplan/img_perm_v1_justone'
subject = '__20221201_18628'
outputdir = "/Users/jacobrivera/Documents/DiLab/selectiveAttentionProject/"
fps = 50
max_blank = 0.3
exper_num = '186'


frame_makers.make_center_obj_frames(inputdir, permsdir, subject, outputdir, fps, max_blank, exper_num, 1)


# make_center_obj_frames(input, permsdir, subject, output, fps, max_blank, experiment, v)