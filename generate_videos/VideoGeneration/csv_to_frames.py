import argparse
import csv
import os
import cv2
import shutil
from tqdm import tqdm

'''
Created by Jacob Rivera
Date created: 6/27/2023
Last modified: 6/28/2023
'''


'''
csv example
0,  10 
1,  3
2,  2
3,  2
4,  1
5,  8
6, -1
7,  0,  10, 5,  7,  2

if second index is 0, then expect background image row with multiple cols
if second index is -1, then give the empty block image
if second index is neither 0 or -1, then it is the roi object 
'''

# Returns a single image name string
def imageNameBuilder(one, two, three, four):
    one = str(int(one))
    two = str(int(two))
    three = str(int(three))
    four = str(int(four))

    return one + '_' + two + '_' + three + '_' + four + '.jpg'



# Creates an array with the name of the image for each frame in video
def get_frame_images_array(filename):
    imageList = []

    with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile)
    
        for row in datareader:
            # if zero, then get baseline image name
            if row[1] == '0':
                image = imageNameBuilder(row[2], row[3], row[4], row[5],)
                imageList.append(image)
            # if -1, then get single empty roi image name
            elif row[1] == '-1':
                image = '0.jpg'
                imageList.append(image)
            # else, get roi image name
            else:
                image = row[1] + '.jpg'
                imageList.append(image)
                
    return imageList

# copies images from imageList to the frameOutputPath for later stitching
def copy_images_to_frames(imageList, frameOutputPath, permPath):

    # for i in range(len(imageList)):
    for i in tqdm(range(len(imageList)), desc = '{:25s}'.format("copying frame images to output dir...")):
        target = frameOutputPath + 'frame_' +  str(i).zfill(5) + '.jpg'
        origin = permPath + imageList[i]
        shutil.copy(origin, target)


# from the frames directory, stitches all frames into one video, and releases to disk at outputPath
def stitch_frames(framePath, outputVideoName, outputPath, fps, width, height):

    video_path = os.path.join(*[outputPath, outputVideoName]) # create full path string
    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'avc1'), fps, (width, height)) # generate video writer object

    # get all files to stitch
    files = os.listdir(framePath)
    files = sorted(files)

    # iterate over files and add them to the video
    for file_name in tqdm(files, desc = '{:25s}'.format("stiching frames...")):
        img = cv2.imread(framePath + '/' + file_name)
        video.write(img)
    video.release()

    return 

# does everything to create videos from csv files, gets an image list, copies frames to output folder, and stiches frames into video
def csv_to_frames(filename, permutationsPath, frameOutputPath): #videoOutputPath, videoOutputName, fps, width, height): # paths expect the end of string to have a
    
    imageList = get_frame_images_array(filename) # ['1.jpg', '4.jpg', '1_3_5_2.jpg', ...]
    copy_images_to_frames(imageList, frameOutputPath, permutationsPath)
    # stitch_frames(frameOutputPath, videoOutputName, videoOutputPath, fps, width, height)
    return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
  
    parser.add_argument('-o', '--outputdir',type=str, help="dir where frames will be saved to")
    parser.add_argument('-p', '--permsdir', type=str, help="dir of object image permuations")
    parser.add_argument('-v', '--outputVidName', type=str, help="name of outputted video")
    parser.add_argument('-c', '--csvPathAndName', type=str, help="full path of csv file")

    args = parser.parse_args()

    frameOutputPath = args.outputdir
    permsdir = args.permsdir
    outputVideoName = args.outputVidName


    # Variables needed for csv_to_frames()
    csv_filename = 'VideoGeneration\\sample-ideal-noisy-learner-frames.csv'
    permutationsPath = 'Z:\\Jacob\\image_permutations\\permuations_baseline\\'
    frameOutputPath = 'C:\\Users\\jacob\\Documents\\SelectiveAttentionProject\\artificalGoodLearner\\frames\\'
    # videoOutputPath = 'C:\\Users\\jacob\\Documents\\SelectiveAttentionProject\\artificalGoodLearner\\'
    # videoOutputName = 'test2.mp4'

    
    csv_to_frames(csv_filename, permutationsPath, frameOutputPath)
