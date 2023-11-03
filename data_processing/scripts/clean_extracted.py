import pandas as pd


############################################
#
# Created by Jacob Rivera
# Last Modified: 10/27/2023
#
############################################



def clean_multi_extract(data_file):
    df = pd.read_csv(data_file)

    # Clean up data into dataframe with correct header
    header = list(df.columns)

    row_0 = df.iloc[0]
    row_1 = df.iloc[1]
    row_2 = df.iloc[2]

    for i in range(len(header)):
        if i >= 7 and i < 25:
            header[i] = row_0[7] + '_' + row_1[i]
        elif i >= 25 and i < 43:
            header[i] = row_0[25] + '_' + row_1[i]
        elif i >= 43:
            header[i] = row_0[43] + '_' + str(row_1[i])
        else:
            header[i] = row_2[i]

    df.columns = header
    df.rename(columns={'#subID':'subID'}, inplace=True)
    df = df.drop(labels=[0,1,2], axis=0).reset_index()
    # could delete unnecessary columns for faster processing/less memory usage
    return df
