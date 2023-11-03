import scipy.io
import os
import numpy as np
from scipy.interpolate import interp1d
import cv2

"""
Author: Jacob Rivera
Date: Spring 2023

Functions to pull relavent information from matlab files.
"""

C_EVENT_1 = 'cstream_training_object_1.mat'
C_EVENT_2 = 'cstream_training_object_2.mat'
C_EVENT_3 = 'cstream_training_object_3.mat'
C_EVENT_4 = 'cstream_training_object_4.mat'

TIME_ROI = 'cstream_training_eye_roi.mat'
EYE_COORDS = 'training_eye_xy.mat'

words_learned = 'cevent_training_words_learned.mat'
words_not_learned = 'cevent_training_words_learned.mat'

def imageFileGatherer(path):
    """Gathers the four matlab files that hold information
        regarding the object for its respective corner, concatenates all four
        objects per time record, and creates a list of the corresonding images.
        This list is returned."""
    data_c_event_1 = scipy.io.loadmat(path + C_EVENT_1)['sdata'][0][0][1]
    data_c_event_2 = scipy.io.loadmat(path + C_EVENT_2)['sdata'][0][0][1]
    data_c_event_3 = scipy.io.loadmat(path + C_EVENT_3)['sdata'][0][0][1]
    data_c_event_4 = scipy.io.loadmat(path + C_EVENT_4)['sdata'][0][0][1]

    assert(np.shape(data_c_event_1) == np.shape(data_c_event_2) == np.shape(data_c_event_3) == np.shape(data_c_event_4))

    size = len(data_c_event_1)
    time_image_array = [] # [timeStart, timeEnd, imageName]

    for i in range(size):
        t = data_c_event_1[i][0]

        one = data_c_event_1[i][1]
        two = data_c_event_2[i][1]
        three = data_c_event_3[i][1]
        four = data_c_event_4[i][1]

        time_image_array.append([i,imageNameBuilder(one, two, three, four)])

    return time_image_array


# Returns a single image name string
def imageNameBuilder(one, two, three, four):
    one = str(int(one))
    two = str(int(two))
    three = str(int(three))
    four = str(int(four))

    return one + '_' + two + '_' + three + '_' + four + '.jpg'


def roi_gatherer(matPath):
    data_time_roi = scipy.io.loadmat(matPath + TIME_ROI)['sdata'][0][0][1]

    time_roi_array = [] # [timeStart, timeEnd, roi]

    for i in range(len(data_time_roi)):
        t = data_time_roi[i][0]
        roi = data_time_roi[i][1]
        time_roi_array.append([t, roi])

    time_on_off_roi = []

    i = 0
    while i < len(time_roi_array) - 1:
        start = time_roi_array[i][0]
        roi = time_roi_array[i][1]
        end = time_roi_array[i][0]
        while(i < len(time_roi_array)-1 and time_roi_array[i][1] == time_roi_array[i+1][1]):
            end = time_roi_array[i+1][0]
            i += 1

        i += 1
        time_on_off_roi.append([start, end, roi])

    # return time_on_off_roi
    return data_time_roi

def roi_gatherer_baseline_included(matPath):
    data_time_roi = scipy.io.loadmat(matPath + TIME_ROI)['sdata'][0][0][1]

    time_roi_array = [] # [timeStart, timeEnd, roi]

    for i in range(len(data_time_roi)):
        t = data_time_roi[i][0]
        roi = data_time_roi[i][1]
        time_roi_array.append([t, roi])

    time_on_off_roi = []

    i = 0
    while i < len(time_roi_array) - 1:
        start = time_roi_array[i][0]
        roi = time_roi_array[i][1]
        end = time_roi_array[i][0]
        while(i < len(time_roi_array)-1 and time_roi_array[i][1] == time_roi_array[i+1][1]):
            end = time_roi_array[i+1][0]
            i += 1

        i += 1
        time_on_off_roi.append([start, end, roi])

    # return time_on_off_roi
    return data_time_roi