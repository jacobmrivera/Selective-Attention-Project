import argparse
import pandas as pd
import constants


############################################
#
# Created by Jacob Rivera
# Last Modified: 10/27/2023
#
############################################


'''
BUCKETS
--------------------------------------
Not Skewed
    - BUCKET 1: Not Skewed + Incorrect
    - BUCKET 2: Not Skewed + Possible
    - BUCKET 3: Not Skewed + Correct
Skewed
    - BUCKET 4: Skewed + Incorrect
    - BUCKET 5: Skewed + Possible
    - BUCKET 6: Skewed + Correct

Definitions
    Skewed:
        - most looked at object has gaze time > 50%
    Not skewed:
        - no objects have gaze time > 50%
    Correct:
        - correct object looked at longest
    Possible:
        - correct object looked at at least 20% of gaze time
    Incorrect:
        - correct object looked at less than 20% of gaze time
'''

# returns a dictionary for a row so that data can be accessed more clearly
def row_to_dict(row):
    sub_dict = {'onset': float(row['onset']),
                'offset': float(row['offset']),
                'category': int(row['category']),}

    for i in range(1, 19):
        sub_dict[str(i)] = float(row['individual_prop_' + str(i)])
    return sub_dict


def find_bucket(instance, num_objects):
    correct = instance['category'] # category column is 'correct' object

    bucket = 0
    skewed = False
    largest_ind = 1

    for i in range(1, num_objects + 1):
        if instance[str(i)] >= constants.MAJORITY_CUTOFF:
            skewed = True

        if instance[str(i)] > instance[str(largest_ind)]:
            largest_ind = i

    # If True, states will be either 4, 5, or 6, if False, 1, 2, or 3
    if skewed:
        bucket += 3

    if instance[str(correct)] >= constants.MAJORITY_CUTOFF and largest_ind == correct:
        bucket += 3
    elif instance[str(correct)] >= constants.POSSIBLE_CUTOFF:
        bucket += 2
    else:
        bucket += 1

    return bucket


def add_buckets(df):
    exp = []
    amount = len(df)

    for i in range(amount):
        instance = row_to_dict(df.iloc[i])
        exp.append(find_bucket(instance, constants.NUM_OBJS))

    df['GazeDistributionBucket'] = exp
    return df

def add_skew_col(df):
    skewed = []

    for i in range(len(df["GazeDistributionBucket"])):
        
        bucket = df.at[i, "GazeDistributionBucket"]
        
        if bucket < 4:
            skewed.append(0)
        else:
            skewed.append(1)
            
    df['skewed'] = skewed
    return df

def add_correctness_col(df):
    correctness = []

    for i in range(len(df["GazeDistributionBucket"])):
        
        bucket = df.at[i, "GazeDistributionBucket"]
        
        if bucket % 3 == 1:
            correctness.append(0)
        elif bucket % 3 == 2:
            correctness.append(1)
        elif bucket % 3 == 0:
            correctness.append(2)
    df["correctness"] = correctness
    return df