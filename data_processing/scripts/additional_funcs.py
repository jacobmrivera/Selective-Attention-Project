import numpy as np
import pandas as pd
import constants
import clean_extracted


############################################
#
# Created by Jacob Rivera
# Last Modified: 11/03/2023
#
############################################

# used to be get_trial_number
def add_trial_num(df_trial, long=False):
    trials = []

    # last = 0
    for i in range(constants.NUM_TRIALS * len(df_trial.subID.unique())):
        # last = i % constants.NUM_TRIALS
        for _ in range(constants.NUM_LABELS_PER_TRIAL):
            trials.append(i % constants.NUM_TRIALS)
    
    if long:
        df_trial['long_trial'] = trials
        df_trial["long_trial"] = df_trial["long_trial"] +1  
    else:
        df_trial['trial'] = trials  
        df_trial["trial"] = df_trial["trial"] +1 

    return df_trial

def add_label_instance_count(df_count, long=False):

    column = []
    for index, row in df_count.iterrows():
            
        if index % constants.NUM_LABELING_INSTANCES == 0:
            counts = np.zeros(constants.NUM_OBJS, dtype=int)

        label = int(row['category'])
        counts[label - 1] += 1

        column.append(counts[label - 1])
        
    if long:
        df_count['long_labelingInstance'] = column 
    else:
        df_count['labelingInstance'] = column  

    return df_count

# gets the frequency of target gazes
def get_freq(df, index, prefix, target):
    freq_norm = float(df.loc[index, prefix + str(target)])
    return round(freq_norm * constants.NORM_FACTOR)


# of target looks within the labeling window: likely to 1 or 0, but could be 2
def get_num_target_looks_window(df, long=False):
    col = []
    prefix = "individual_freq_"
    
    for index, row in df.iterrows():
        target = int(row["category"])
        col.append(get_freq(df, index, prefix, target))
    
    if long:
        df["long_targetGazeCount"] = col
    else:
        df["targetGazeCount"] = col

    return df



# Add Count of Target Gazes during off windows
#    gets the gaze counts for target in other 3 labeling windows
#    unfortunately, a lot of hard coding...
def get_target_counts_other_trials(df, long=False):
    col = []
    
    prefix = "individual_freq_"
    
    for index, row in df.iterrows():
        target = int(row["category"])
        tot = 0

        if index % constants.NUM_LABELS_PER_TRIAL == 0:
            freq_1 = get_freq(df, index + 1, prefix, target)
            freq_2 = get_freq(df, index + 2, prefix, target)
            freq_3 = get_freq(df, index + 3, prefix, target)

            tot = freq_1 + freq_2 + freq_3
            
        elif index % constants.NUM_LABELS_PER_TRIAL == 1:
            freq_0 = get_freq(df, index - 1, prefix, target)
            freq_2 = get_freq(df, index + 1, prefix, target)
            freq_3 = get_freq(df, index + 2, prefix, target)

            tot = freq_0 + freq_2 + freq_3
            
        elif index % constants.NUM_LABELS_PER_TRIAL == 2:  
            freq_0 = get_freq(df, index - 2, prefix, target)
            freq_1 = get_freq(df, index - 1, prefix, target)
            freq_3 = get_freq(df, index + 1, prefix, target)

            tot = freq_0 + freq_1 + freq_3

        elif index % constants.NUM_LABELS_PER_TRIAL == 3:
            freq_0 = get_freq(df, index - 3, prefix, target)
            freq_1 = get_freq(df, index - 2, prefix, target)
            freq_2 = get_freq(df, index - 1, prefix, target)

            tot = freq_0 + freq_1 + freq_2

        col.append(tot)

    if long:
        df['long_targetGazeCountOffWindows'] = col
    else:
        df['targetGazeCountOffWindows'] = col
    # df['targetGazeCountOffWindows'] = col
    return df




# counts number of objects with gaze greater than 0 - task 3
def add_unique_obj_col(df, long=False):
    col = []
    pre = "individual_prop_"

    for index, row in df.iterrows():
        count = 0
        for j in range(1, constants.NUM_OBJS + 1):
            if float(row[pre+str(j)]) > 0:
                count += 1
        col.append(count)

    if long:
        df['long_uniqueObjectsVisitedCount'] = col
    else:
        df['uniqueObjectsVisitedCount'] = col
    # df['uniqueObjectsVisitedCount'] = col
    return df



def get_pre_label_counts(df_pre, silent_file, long=False):
    col = []

    col_str = 'individual_freq_'
    df_silent = clean_extracted.clean_multi_extract(silent_file)


    i = 0
    first = True
    # for exp in experiments:
        # df_multi = af.clean_multi_extract('./data/look_in_silence_all_exp{}.csv'.format(exp))
    for index, row in df_pre.iterrows():
        if index % constants.NUM_LABELS_PER_TRIAL == 0 and not first:
            i += 1
        first = False

        window = df_silent.iloc[i]

        cur_obj = row['category']
        freq_norm = float(window[col_str + str(int(cur_obj))])

    #     print(round(freq_norm * (2.25/60)), int(cur_obj))
        col.append(round(freq_norm *  constants.NORM_FACTOR))

    if long:
        df_pre['preLabelWindowCount_long'] = col
    else:
        df_pre['preLabelWindowCount'] = col
    return df_pre