import argparse
import csv
import os
import cv2
import numpy as np
import mat_file_funcs
import shutil
import scipy.io
from tqdm import tqdm


"""
Author: Jacob Rivera
Date: Spring 2023

Creates frames for the baseline video, crosshair video,
and single roi video for a given subject.
"""

EYE_COORDS = 'training_eye_xy.mat'


###########################################################################################
#               BASELINE VIDEO SECTION
#########

def create_baseline_frames(input, experiment, subject, output, permutation_dir):
    matFilesPath = os.path.join(*[input, "experiment_" + experiment, 'included', subject, 'derived/'])

    # gets baseline images names for entire video duration  --   [time, imageName.jpg]
    mat_list = mat_file_funcs.imageFileGatherer(matFilesPath)

    if not os.path.isdir(output+ 'baseline_frames'):
        os.mkdir(output + 'baseline_frames')

    pbar = tqdm(total=len(mat_list), desc='{:25s}'.format('baseline frames'))

    for i in range(len(mat_list)):
        origin = permutation_dir + '/' + mat_list[i][1]
        target = output + 'baseline_frames' + '/' + 'frame_' + str(i).zfill(5) + '.jpg'
        shutil.copy(origin, target)
        pbar.update(1)
    pbar.close()
    return

#########
#               BASELINE VIDEO SECTION
###########################################################################################




###########################################################################################
#               CROSSHAIR VIDEO SECTION
#########
def create_crosshair_frames(input, experiment, subject, output, permutation_dir, height, width):

    matFilesPath = os.path.join(*[input, "experiment_" +  experiment, 'included', subject, 'derived/'])
    crosshair_data = alignCoordsToFrames(matFilesPath)
    data_size = len(scipy.io.loadmat(matFilesPath + EYE_COORDS)['sdata'][0][0][1])

    # gets baseline images names for entire video duration  --   [time, imageName.jpg]
    mat_list = mat_file_funcs.imageFileGatherer(matFilesPath)
    final_size = len(mat_list)
    if not os.path.isdir(output + subject ):
        os.mkdir(output + subject)

    if not os.path.isdir(output + subject + '/crosshair_frames'):
        os.mkdir(output + subject + '/crosshair_frames')

    pbar = tqdm(total=len(mat_list), desc='{:25s}'.format('crosshair frames'))

    for i in range(len(mat_list)):
        origin = permutation_dir + '/' + mat_list[i][1]
        target = output + subject + '/crosshair_frames' + '/' + 'frame_' + str(i).zfill(5) + '.jpg'

        img = cv2.imread(origin)
        x = int(crosshair_data[i][1])
        y = int(crosshair_data[i][2])

        if x != -1 or y != -1:
            horizontalP1 = x, 0
            horizontalP2 = x, height

            verticalP1 = 0, y
            verticalP2 = width, y

            # Purple color in BGR
            color = (236, 3, 252)
            # Line thickness of 9 px
            thickness = 2

            cv2.line(img, horizontalP1, horizontalP2, color, thickness)
            cv2.line(img, verticalP1, verticalP2, color, thickness)

        cv2.imwrite(target, img)
        pbar.update(1)
    pbar.close()

    return [subject, data_size, final_size]



# assignes each coordinate record to a frame,
# inserting empty rows for needed frames
# returns frame_x_y -- [frame_num, x_coord, y_coord]
def alignCoordsToFrames(matPath):
    eye_data = scipy.io.loadmat(matPath + EYE_COORDS)['sdata'][0][0][1]
    rounded_frames = np.zeros(len(eye_data))

    eye_data = np.hstack((eye_data, np.atleast_2d(rounded_frames).T))

    for i in range(len(eye_data)):
        eye_data[i][3] = round(round(eye_data[i][0],3)*50)

    frame_x_y = []
    # frame_x_y.append()

    prev = int(eye_data[0][3])
    curr = int(eye_data[1][3])

    for i in range(1, len(eye_data)):
        # if first frame is or isn't zero, catches for it
        if prev == 0:
            frame_x_y.append([0, eye_data[0][1], eye_data[0][2]])
        elif prev == 1 and i == 1:
            frame_x_y.append([0, -1, -1])

        #all other frames
        curr = int(eye_data[i][3])
        if curr == prev: 
            continue
        elif curr - prev <= 1 :
            frame_x_y.append([curr, eye_data[i][1], eye_data[i][2]])
            prev = curr

        else:
            # fill in empty spaces
            for diff in range(int(prev) + 1, int(curr)):
                frame_x_y.append([diff, -1, -1])

            # append current row
            frame_x_y.append([curr, eye_data[i][1], eye_data[i][2]])
            prev = curr
    if len(frame_x_y) != 15448:
        frame_x_y.append([15447,-1,-1])
    return frame_x_y

#########
#                  CROSSHAIR VIDEO SECTION
###########################################################################################


###########################################################################################
#                  SINGLE OBJECT VIDEO SECTION
#########
def make_single_obj_frames(input, permsdir, subject, output, fps, max_blank, experiment):

    if not os.path.isdir(output + subject ):
        os.mkdir(output + subject)

    if not os.path.isdir(output + subject + '/single_object_frames'):
        os.mkdir(output + subject + '/single_object_frames')

    matFilesPath = os.path.join(*[input, "experiment_" + experiment, 'included', subject, 'derived/'])

    # gets baseline images names for entire video duration  --   [time, imageName.jpg]
    mat_times_image = mat_file_funcs.imageFileGatherer(matFilesPath)

    # returns array of shape [start_t, end_t, object_num]
    mat_times_roi = mat_file_funcs.roi_gatherer(matFilesPath)

    # shape: [num_frames, object num, num_frames/fps]
    times_roi = get_frames_per_object(mat_times_roi, max_blank, fps)

    tot = 0
    i = 0
    skip = False
    pbar = tqdm(total=len(times_roi), desc='{:25s}'.format('single object frames'))

    while i < len(times_roi): #for i in range(len(times_roi)):
        prev = tot
        tot += times_roi[i][0]

        skip = False
        if i < len(times_roi) - 2 and (times_roi[i + 1][1] == 0) and (times_roi[i][1] == times_roi[i + 2][1]) and (times_roi[i + 1][0] <= max_blank * 50):
            times_roi[i][2] += times_roi[i + 1][2]
            tot += times_roi[i + 1][0]
            skip = True

        single_image_str = get_roi_image(times_roi[i][1], mat_times_image[int((tot // 572.5)*572.5 + tot%572.5) - 1][1]) 

        for dupes in range(tot - prev):
            origin = permsdir + '/' + single_image_str
            target = output + subject + '/single_object_frames' + '/' + 'frame_' + str(prev+dupes).zfill(5) + '.jpg'

            shutil.copy(origin, target)

        i += 1
        if skip:
            i += 1
            pbar.update(1)
        pbar.update(1)
    pbar.close()
    return

# returns array with properties: [num_frames, object num, num_frames/fps]
def get_frames_per_object(roi_array, max_dur, fps):
    i = 0
    tot = 0
    frames_array = []
    while i < len(roi_array):
        num_frames = 1

        while i < len(roi_array) - 1 and roi_array[i][1] == roi_array[ i+ 1][1] :
            num_frames += 1
            i += 1

        if len(frames_array) > 0 and num_frames < max_dur * fps and roi_array[i][1] == 0 and i < len(roi_array) - 1 and roi_array[i - 1][1] == roi_array[i + 1][1]:
            frames_array[-1][0] += num_frames
        else:
            frames_array.append([num_frames, roi_array[i][1], num_frames / fps])

        tot += num_frames
        i += 1

    return frames_array

# returns file with single desired roi object
def get_roi_image(roi, orignalImage):
    obj_list = orignalImage.strip('.jpg').split('_')
    object_num = obj_list[int(roi) - 1]

    image_name = ''
    for i in range(len(obj_list)):
        if i != roi - 1:
            image_name += '0'
        else:
            image_name += str(object_num)

        if i <= len(obj_list) - 2: image_name += '_'

    image_name += '.jpg'

    return image_name


#########
#                  SINGLE OBJECT VIDEO SECTION
###########################################################################################





###########################################################################################
#                  CENTER OBJECT VIDEO SECTION
#########

def make_center_obj_frames(input, perms_dir, subject, output, fps, max_blank, experiment, v, baseline_frames_folder, orig_perms):

    if not os.path.isdir(output + subject ):
        os.mkdir(output + subject)

    if v == 1:
        if not os.path.isdir(output + subject + '/center_object_frames_v1'):
            os.mkdir(output + subject + '/center_object_frames_v1')
    elif v == 2:
        if not os.path.isdir(output + subject + '/center_object_frames_v2'):
            os.mkdir(output + subject + '/center_object_frames_v2')

    matFilesPath = os.path.join(*[input, "experiment_" + experiment, 'included', subject, 'derived/'])

    # gets baseline images names for entire video duration  --   [time, imageName.jpg]
    mat_times_image = mat_file_funcs.imageFileGatherer(matFilesPath)

    # returns array of shape [start_t, end_t, object_num]
    mat_times_roi = mat_file_funcs.roi_gatherer(matFilesPath)

    # shape: [num_frames, object num, num_frames/fps]
    times_roi = get_frames_per_object(mat_times_roi, max_blank, fps)
    # print(times_roi)
    # print("size: ", len(times_roi))
    tot = 0
    i = 0
    skip = False
    if v == 1:
        pbar = tqdm(total=len(times_roi), desc='{:25s}'.format('center object frames v1'))
    elif v == 2:
        pbar = tqdm(total=len(times_roi), desc='{:25s}'.format('center object frames v2'))

    while i < len(times_roi):
        prev = tot
        tot += times_roi[i][0]

        skip = False
        if i < len(times_roi) - 2 and (times_roi[i + 1][1] == 0) and (times_roi[i][1] == times_roi[i + 2][1]) and (times_roi[i + 1][0] <= max_blank * 50):
            times_roi[i][2] += times_roi[i + 1][2]
            tot += times_roi[i + 1][0]
            skip = True

        single_image_str = get_center_roi_image(times_roi[i][1], mat_times_image[int((tot // 572.5)*572.5 + tot%572.5) - 1][1])
        # print(single_image_str)
        for dupes in range(tot - prev):
            origin = perms_dir + '/' + single_image_str
            if v == 1:
                target = output + subject + '/center_object_frames_v1' + '/' + 'frame_' + str(prev+dupes).zfill(5) + '.jpg'
            elif v == 2:
                target = output + subject + '/center_object_frames_v2' + '/' + 'frame_' + str(prev+dupes).zfill(5) + '.jpg'

            # print(single_image_str)
            # print('target: ', target)
            # print('origin: ', origin)

            shutil.copy(origin, target)


        i += 1
        if skip:
            i += 1
            pbar.update(1)
        pbar.update(1)
    pbar.close()

    frames_folder = output + subject + '/center_object_frames_v1' + '/'

    sub_baseline_frames_prelabel_window(frames_folder, orig_perms, mat_times_image)
    return


# returns file with single desired roi object
def get_center_roi_image(roi, originalImage):

    ''' # my fix
    obj_list = originalImage.strip('.jpg').split('_')
    object_num = obj_list[int(roi) - 1]
    object_image = str(object_num) + '.jpg'
    print(object_image)

    '''
    # print("original image name: ", originalImage)
    obj_list = originalImage.strip('.jpg').split('_')

    if roi == 0:
        object_num = 0
    else:
        object_num = obj_list[int(roi) - 1]

    image_name = str(object_num) + '.jpg'
    return image_name
    # return object_image



def sub_baseline_frames_prelabel_window(frames_folder, perms_folder, mat_times_image):
    frames_to_replace_baseline = []
    frames_to_replace_btwn = []
    num_prelabel_frames_even = 112
    num_prelabel_frames_odd = 113

    num_btwn_trial_frames = 10
    num_trial_frames = 450

    tot = 0
    even = True

    # while the tot number of frames counted up isnt at the max
    while tot <= 15447:
        # sub_array to keep instances of baseline frame sections to
        #   replace with a single baseline image
        # even and odd is to balance the fact that 2.25*50 is not an int
        frames_base = []
        if even:
            for i in range(tot, tot + num_prelabel_frames_even):
                frames_base.append(i)
                even = False
            tot += num_prelabel_frames_even
        else:
            for i in range(tot, tot + num_prelabel_frames_odd):
                frames_base.append(i)
                even = True
            tot += num_prelabel_frames_odd
        # store this sub array
        frames_to_replace_baseline.append(frames_base)
        # update where we are along the frames
        tot += num_trial_frames

        # same process as above except for the blank 0.2s space
        #   between trials. No even or odd because 0.2*50 = 10
        frames_btwn = []
        for i in range(tot, tot + num_btwn_trial_frames):
            frames_btwn.append(i)
        tot += num_btwn_trial_frames
        frames_to_replace_btwn.append(frames_btwn)

    pbar = tqdm(total=len(frames_to_replace_baseline), desc='{:25s}'.format('Replacing baseline frames'))

    # Loop through sub arrays to find baseline image,
    #   Then copy over baseline image and replace the frames
    for i in range(len(frames_to_replace_baseline)):
        # time = int(np.median(frames_to_replace_baseline[i]))
        length = len(frames_to_replace_baseline[i]) // 2
        baseline_file = mat_times_image[frames_to_replace_baseline[i][length]][1] # gets the image name

        for j in range(len(frames_to_replace_baseline[i])):
            target = frames_folder + 'frame_' + str(frames_to_replace_baseline[i][j]).zfill(5) + '.jpg'
            origin = perms_folder + baseline_file
            print(origin, target)
            shutil.copy(origin, target)

        for j in range(len(frames_to_replace_btwn[i])):
            target = frames_folder + 'frame_' + str(frames_to_replace_btwn[i][j]).zfill(5) + '.jpg'
            origin = './VideoGeneration/0_0_0_0.jpg'
            print(origin, target)
            shutil.copy(origin, target)

        pbar.update(1)
    pbar.close()


#########
#                  CENTER OBJECT VIDEO SECTION
###########################################################################################


# create_baseline_frames(INPUT, EXPERIMENT, SUBJECT, OUTPUT, PERMS_DIR)
# create_crosshair_frames(INPUT, EXPERIMENT, SUBJECT, OUTPUT, PERMS_DIR)
# make_single_obj_frames(INPUT, PERMS_DIR, SUBJECT, OUTPUT, FPS, MAX_BLANK, EXPERIMENT)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('inputdir', type=str)
    parser.add_argument('outputdir',type=str)
    parser.add_argument('permsdir', type=str)
    parser.add_argument('exper_num', type=str)
    parser.add_argument('subject', type=str)
    parser.add_argument('fps', type=int)
    parser.add_argument('max_blank', type=float)
    parser.add_argument('height', type=int)
    parser.add_argument('width', type=int)
    parser.add_argument('op', type=str)
    parser.add_argument('orig_perms', type=str)

    args = parser.parse_args()

    inputdir = args.inputdir
    outputdir = args.outputdir
    permsdir = args.permsdir
    exper_num = args.exper_num
    subject = args.subject
    fps = args.fps
    max_blank = args.max_blank
    height = args.height
    width = args.width
    op = args.op
    orig_perms = args.orig_perms

    to_return = ""

    baseline_frames_folder = 'Volumes/space/spcaplan/experiment_185/baseline_frames/'

    if op == 'b':
        create_baseline_frames(inputdir, exper_num, subject, outputdir, permsdir)
    elif op == 'c':
        to_return = create_crosshair_frames(inputdir, exper_num, subject, outputdir, permsdir, height, width)

        filename = outputdir+'experiment_'+exper_num+'_cross_length_log.csv'
        with open(filename, 'a', newline="") as file:
            csv_writer = csv.writer(file) # 2. create a csvwriter object
            csv_writer.writerow([to_return[0], str(to_return[1]) +'/'+ str(to_return[2]), to_return[1]/to_return[2] ])
    elif op == 's':
        make_single_obj_frames(inputdir, permsdir, subject, outputdir, fps, max_blank, exper_num)
    elif op == 'm': # M equals v1
        make_center_obj_frames(inputdir, permsdir, subject, outputdir, fps, max_blank, exper_num, 1, baseline_frames_folder, orig_perms)
    elif op == 'n': # n equals v2
        make_center_obj_frames(inputdir, permsdir, subject, outputdir, fps, max_blank, exper_num, 2, baseline_frames_folder, orig_perms)
    else:
        print("Please enter a correct option")

    # cv2.destroyallwindows()