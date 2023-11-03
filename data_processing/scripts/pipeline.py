import pandas as pd
import numpy as np
import argparse
import clean_extracted
import bucket_col_funcs
import additional_funcs
import constants


############################################
#
# Created by Jacob Rivera
# Last Modified: 11/03/2023
#
############################################


def add_all_additional_cols(input_file):
    df = clean_extracted.clean_multi_extract(input_file)

    df = bucket_col_funcs.add_buckets(df)
    df = bucket_col_funcs.add_skew_col(df)
    df = bucket_col_funcs.add_correctness_col(df)

    df = additional_funcs.get_num_target_looks_window(df)
    df = additional_funcs.get_target_counts_other_trials(df)
    df = additional_funcs.add_unique_obj_col(df)
    df = additional_funcs.add_trial_num(df)
    df = additional_funcs.add_label_instance_count(df)
    df = additional_funcs.get_pre_label_counts(df, constants.PRELABEL_WINDOW_FILE)

    return df

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()

    # parser.add_argument('i', '--inputfile', type=str, help="path to look_by_word csv", required=True)
    # parser.add_argument('-n', '--numobjs',type=str, help="number of objects in dataset",  required=True)
    # parser.add_argument('-o', '--outputfilename',type=str, help="path/name of output csv", default="x")

    # args = parser.parse_args()

    # input_file = args.inputfile
    # num_objects = args.numobjs
    # output_file = args.outputfilename


    df = add_all_additional_cols(constants.INPUT_FILE)

    df.to_csv(constants.OUTPUT_FILE, index=False)
    print("Outputted: {}".format(constants.OUTPUT_FILE))