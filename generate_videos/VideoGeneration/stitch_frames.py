import argparse
import cv2
import os
from tqdm import tqdm

"""
Author: Jacob Rivera
Date: Spring 2023

Stitches frames for the baseline video, crosshair video,
and single roi video for a given subject, videos are outputted.
"""

def stitch_frames_to_video_base(output, exper_num, fps, width, height):

    video = cv2.VideoWriter(output + 'experiment_'+exper_num+'_baseline.mp4',cv2.VideoWriter_fourcc(*'avc1'), fps, (width, height))

    frames_path = os.path.join(*[output, 'baseline_frames'])
    files = os.listdir(frames_path)
    files = sorted(files)

    for file_name in tqdm(files, desc='{:25s}'.format("baseline stitch")):
        img = cv2.imread(frames_path + '/' + file_name)
        video.write(img)
    video.release()

    return


def stitch_frames_to_video_cross(output, subject, fps, width, height):

    video_path = os.path.join(*[ output, subject, subject + '_crosshair.mp4'])
    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'avc1'), fps, (width, height))

    frames_path = os.path.join(*[output,subject, 'crosshair_frames'])
    files = os.listdir(frames_path)
    files = sorted(files)

    for file_name in tqdm(files, desc = '{:25s}'.format("crosshair stitch")):
        img = cv2.imread(frames_path + '/' + file_name)
        video.write(img)
    video.release()

    return


def stitch_frames_to_video_single(output, subject, fps, width, height):
    video_path = os.path.join(*[ output, subject, subject + '_single_object.mp4'])

    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'avc1'), fps, (width, height))

    frames_path = os.path.join(*[output,subject, 'single_object_frames'])
    files = os.listdir(frames_path)
    files = sorted(files)

    for file_name in tqdm(files, desc = '{:25s}'.format("single object stitch")):
        img = cv2.imread(frames_path + '/' + file_name)
        video.write(img)
    video.release()

    return

def stitch_frames_to_video_center(output, subject, fps, width, height, v):
    if v == 1:
        video_path = os.path.join(*[ output, subject, subject + '_center_object_v1.mp4'])
    elif v == 2:
        video_path = os.path.join(*[ output, subject, subject + '_center_object_v2.mp4'])

    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'avc1'), fps, (width, height))

    if v == 1:
        frames_path = os.path.join(*[output,subject, 'center_object_frames_v1'])
    elif v == 2:
        frames_path = os.path.join(*[output,subject, 'center_object_frames_v2'])

    files = os.listdir(frames_path)
    files = sorted(files)


    if v == 1:
        for file_name in tqdm(files, desc = '{:25s}'.format("center object stitch v1")):
            img = cv2.imread(frames_path + '/' + file_name)
            video.write(img)
    elif v == 2:
        for file_name in tqdm(files, desc = '{:25s}'.format("center object stitch v2")):
            img = cv2.imread(frames_path + '/' + file_name)
            video.write(img)
    video.release()

    return


def stitch_frames(framePath, outputVideoName, outputPath, fps, width, height):
    video_path = os.path.join(*[outputPath, outputVideoName]) # create full path string
    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'avc1'), fps, (width, height)) # generate video writer object

    # get all files to stitch
    files = os.listdir(framePath)
    files = sorted(files)

    # iterate over files and add them to the video
    for file_name in tqdm(files, desc = '{:25s}'.format("stiching frames for " + outputVideoName + "...")):
        img = cv2.imread(framePath + '/' + file_name)
        video.write(img)
    video.release()


# stitch_frames_to_video(INPUT+'/experiment_185/baseline_frames', OUTPUT, EXPERIMENT, FPS, WIDTH, HEIGHT)
# stitch_frames_to_video_cross(INPUT + '/experiment_185/' + SUBJECT + '/crosshair_frames', OUTPUT, EXPERIMENT, SUBJECT, FPS, WIDTH, HEIGHT)
# stitch_frames_to_video_single(INPUT, OUTPUT, EXPERIMENT, SUBJECT, FPS, WIDTH, HEIGHT)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
  
    parser.add_argument('-o', '--outputdir',type=str, help="dir where video will be saved to")
    parser.add_argument('-p', '--permsdir', type=str, help="dir of object image permuations")
    parser.add_argument('-f', '--fps', type=int, help="number of frames per second for video")
    parser.add_argument('-h', '--height', type=int, help="vertical num of pixels in video")
    parser.add_argument('-w', '--width', type=int, help="horizontal num of pixels in video")
    parser.add_argument('-v', '--outputVidName', type=str, help="name of outputted video")
    # parser.add_argument('-i   ', '--inputdir', type=str, help="")
    # parser.add_argument('exper_num', type=str)
    # parser.add_argument('subject', type=str)
    # parser.add_argument('max_blank', type=float)
    # parser.add_argument('op', type=str)

    args = parser.parse_args()

    outputdir = args.outputdir
    permsdir = args.permsdir
    fps = args.fps
    height = args.height
    width = args.width
    outputVideoName = args.outputVidName
    # inputdir = args.inputdir
    # exper_num = args.exper_num
    # subject = args.subject#=

    # max_blank = args.max_blank
 
    # op = args.op

    stitch_frames(permsdir, outputVideoName, outputdir, fps, width, height)


    # if op == 'b':
    #     stitch_frames_to_video_base(outputdir, exper_num, fps, width, height)
    # elif op == 'c':
    #     stitch_frames_to_video_cross(outputdir, subject, fps, width, height)
    # elif op == 's':
    #     stitch_frames_to_video_single(outputdir, subject, fps, width, height)
    # elif op == 'm': # m means v1
    #     stitch_frames_to_video_center(outputdir, subject, fps, width, height, 1)
    # elif op == 'n': # n means v2
    #     stitch_frames_to_video_center(outputdir, subject, fps, width, height, 2)
    # else:
    #     print("Please enter a correct option")

