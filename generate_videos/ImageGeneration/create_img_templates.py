# encoding: utf-8

import sys, os, os.path, argparse
from collections import defaultdict
import random
from math import log
import itertools
import cv2
import numpy as np
from alive_progress import alive_bar
import time

"""
Author: Spencer Caplan
Date: Spring 2023

Loads in a set of base stimulus images and creates permutations of their placement
on a canvas to align with gaze data
"""


################
## Global Params
BOX_WIDTH = 0
INPUT_DIR = ""
OUTPUT_DIR = ""
BOX_THICKNESS = 0
GENERATE_ZERO_PERMS = True # if false, will NOT generate images with only 1, 2, or 3 objects

################



box_color = (0, 0, 0)
roi_list = [[10,10], [858,10], [10,602], [858,602]]


def create_canvas():
	white_background = np.zeros([768,1024,3],dtype=np.uint8)
	white_background.fill(255)
	cv2.imwrite("0_0_0_0_nobox.jpg", white_background)

	# x1,y1 ------
	# |		     |
	# |		     |
	# |		     |
	# --------x2,y2

	white_background_boxes = white_background
	for starting_coord in roi_list:
		white_background_boxes = cv2.rectangle(white_background_boxes, (starting_coord[0], starting_coord[1]),(starting_coord[0]+BOX_WIDTH, starting_coord[1]+BOX_WIDTH), box_color, BOX_THICKNESS)

	cv2.imwrite("0_0_0_0.jpg", white_background_boxes)

	return white_background_boxes


def add_stim_to_canvas(canvas, img, start_loc):
	canvas[start_loc[1]:start_loc[1]+img.shape[0], start_loc[0]:start_loc[0]+img.shape[1]] = img
	canvas = cv2.rectangle(canvas, (start_loc[0], start_loc[1]),(start_loc[0]+BOX_WIDTH, start_loc[1]+BOX_WIDTH), box_color, BOX_THICKNESS)
	return canvas


def load_base_images(sourceDir):
	img_dict = {} #dict mapping from img_num to img_file

	if not os.path.isdir(sourceDir):
		raise Exception("Base image directory path not valid!")

	for filename in os.listdir(sourceDir):
		if filename[-4:] == '.jpg':
			fullPath = os.path.join(sourceDir, filename)
			img_num = filename[:-4]
			# print(fullPath)
			img = cv2.imread(fullPath)
			img_dict[img_num] = cv2.resize(img, (BOX_WIDTH,BOX_WIDTH), interpolation = cv2.INTER_AREA)
	
	return img_dict


def list_to_string(inputList):
	strList = [str(x) for x in inputList]
	outputString = "_".join(strList)
	return (outputString + ".jpg")



def gen_possible_perms_dict():
	to_create = {}

	# Define a list of 20 variables
	variables = list(range(1, num_images+1))
	if GENERATE_ZERO_PERMS:
		for i in range(3): variables.insert(0,0)

	# Generate every possible combination of 4 variables
	combinations = itertools.combinations(variables, 4)

	# Generate every possible permutation of each combination
	permutations = [itertools.permutations(c) for c in combinations]

	# Flatten the list of permutations
	flattened_permutations = [p for sublist in permutations for p in sublist]

	for perm in flattened_permutations:
		key_name = list_to_string(perm)
		to_create[key_name] = list(perm) # change tuple to list, may not be necessary
	return to_create



def mainLogicFlow():
	print("Generating possible image grids")
	canvas_img = create_canvas()
	perms_to_create = gen_possible_perms_dict()

	img_dict = load_base_images(INPUT_DIR)
	
	total_num_perms = len(perms_to_create.keys())
	print("Handling: "+str(total_num_perms) + " bases")
	
	with alive_bar(total_num_perms) as bar:
		for file_string, roi_value in perms_to_create.items():
			bar()
			# print(file_string, roi_value)
			output_string = os.path.join(OUTPUT_DIR, file_string)
			# if os.path.exists(output_string):
			# 	continue

			# add anything that isn't a zero in the appropriate position
			filled_canvas = canvas_img.copy()
			for index, img_num in enumerate(roi_value):
				if img_num > 0:
					filled_canvas = add_stim_to_canvas(filled_canvas, img_dict.get(str(img_num)), roi_list[index])
					cv2.imwrite(output_string, filled_canvas)



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "Create image set for selective attention experiment")

	parser.add_argument("--inputdir", help="directory containing source; if absent will assume hard-coded value")
	parser.add_argument("--outputdir", help="directory to house output files; if absent will assume hard-coded value")
	parser.add_argument("--stimulussize", help="Size in pixels for item stimuli; if absent defaults to 154")
	parser.add_argument("--borderwidth", help="Size in pixels of bounding-box width to draw around stim locs; if absent defaults to 2")

	# num base images to use
	num_images = 20 # the number of base images -- in this case there are 18 of them
	
	args = parser.parse_args()

	if args.stimulussize != None:
		BOX_WIDTH = args.stimulussize
	else:
		BOX_WIDTH = 154

	if args.borderwidth != None:
		BOX_THICKNESS = args.borderwidth
	else:
		BOX_THICKNESS = 2

	if args.inputdir != None:
		INPUT_DIR = args.inputdir
	else:
		img_base_list = ['/Users', 'spcaplan', 'Dropbox',
						 'School and Yearly Files','UT-PostDoc',
						 'SelectiveAttention', 'ImageGeneration',
						 'img_base', 'rand']
		# INPUT_DIR = os.path.join(*img_base_list)
		INPUT_DIR = '../img_base/rand'
	if args.outputdir != None:
		OUTPUT_DIR = args.outputdir
	else:
		output_base_list = ['/Users', 'spcaplan', 'Dropbox',
							'School and Yearly Files', 'UT-PostDoc',
							'SelectiveAttention', 'ImageGeneration',
							'img_base', 'perms']
		output_base_list_jacob_personal = ['/Users','jacobrivera','Documents',
				     						'DiLab','selectiveAttentionProject','img_perms_output']
		# OUTPUT_DIR = os.path.join(*output_base_list_jacob_personal)
		OUTPUT_DIR = os.path.join(OUTPUT_DIR)






	mainLogicFlow()
	print("Done.")



