# encoding: utf-8

import sys, os, os.path, argparse
import csv
import glob

import librosa

from pydub import AudioSegment # https://github.com/jiaaro/pydub


"""
Author: Spencer Caplan
Date: Spring 2023

Stitch audio files together at given time interval
"""

def loadSourceAudio(dirName):
	audio_dict = {}
	if os.path.isdir(dirName):
		searchPath = os.path.join(AUDIO_DIR,"*.wav")
		# print("Not yet implemented")
		audio_file_list = glob.glob(searchPath)
		for file in audio_file_list:
			curr_audio = AudioSegment.from_wav(file)
			curr_audio_1000ms = curr_audio[:1000]
			curr_id = os.path.basename(file)[:-4]
			# print(librosa.get_duration(filename=file))
			# print(curr_id)
			audio_dict[curr_id] = curr_audio_1000ms
	else:
		raise Exception('audio directory path doesn\'t seem valid')

	return audio_dict


def readTimingFile(filename):
	last_time_added = 0.0
	output_audio = AudioSegment.silent(duration=0)
	if os.path.isfile(filename):
		with open(filename, 'r', encoding='utf-8-sig') as timingfile:
			reader = csv.DictReader(timingfile)
			for row in reader:
				onset = float(row['Onset'])
				offset = float(row['Offset'])
				file_id = row['ObjectNum']
				gap_from_previous = (onset - last_time_added) * 1000 # need convert to milliseconds here
				# print(onset)
				output_audio = output_audio + AudioSegment.silent(duration=gap_from_previous)
				output_audio = output_audio + audio_dict.get(file_id)
				last_time_added = offset
		
		# adding an extra few seconds buffer (since that will simplify merging with video later)
		output_audio = output_audio + AudioSegment.silent(duration=5000)
		print(OUTPUT_NAME)
		output_audio.export(OUTPUT_NAME, format="wav")
	else:
		raise Exception('timing file path doesn\'t seem valid')



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "Create audio sequence for GLBL experiment")

	parser.add_argument("--inputdir", help="directory containing source audio; if absent will assume hard-coded value")
	parser.add_argument("--timingfile", help="path to timing csv; if absent will assume hard-coded value")
	parser.add_argument("--outputfile", help="name for output file; if absent will assume hard-coded value")
	args = parser.parse_args()

	if args.inputdir != None:
		AUDIO_DIR = args.inputdir
	else:
		AUDIO_DIR = "AudioGeneration/audio_base"

	if args.timingfile != None:
		TIMING_NAME = args.timingfile
	else:
		TIMING_NAME = "AudioGeneration/training-word-label-timing.csv"

	if args.outputfile != None:
		OUTPUT_NAME = args.outputfile
	else:
		OUTPUT_NAME = "AudioGeneration/GLBL-audio-track.wav"

	audio_dict = loadSourceAudio(AUDIO_DIR)

	# second_of_silence = AudioSegment.silent(duration=1000)
	# audio_dict['gap'] = second_of_silence

	readTimingFile(TIMING_NAME)

	print('Done.')
	
