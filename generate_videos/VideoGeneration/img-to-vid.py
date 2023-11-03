import csv
import os
import cv2
import platform
import glob
import numpy as np
from PIL import Image 

name_base = "0_0_0_0"
# name_base = "white"

inputFile = name_base+".jpg"
outputFile = name_base+"aaaa"+".mp4"

fps = 30
# vid_length = fps * 2
length_in_seconds = 12
vid_length = fps*length_in_seconds



def convert_img_to_vid(inputImg, outputVid):

	if not os.path.isfile(inputImg):
		raise Exception("Not a valid path to image")

	img_file = cv2.imread(inputImg)
	height, width, layers = img_file.shape
	fourcc = cv2.VideoWriter_fourcc(*'avc1') # specify the compression codec -- without this the resulting video file will be huge
	video = cv2.VideoWriter(outputVid, fourcc, fps, (width, height)) # third argument is the fps here

	return video
	

if __name__ == "__main__":
	print("running")

	video = convert_img_to_vid(inputFile, outputFile)
	for counter in range(vid_length):
		video.write(cv2.imread('0_0_0_0.jpg'))
	cv2.destroyAllWindows() # Deallocating memory? (Not sure if this is needed)
	video.release()  # releasing generated video 