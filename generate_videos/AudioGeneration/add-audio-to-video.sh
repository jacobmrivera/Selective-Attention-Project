VID_FILE="example-crosshair-vid.mp4"
AUDIO_FILE="GLBL-audio-track.wav"
OUTPUT_FILE="example-crosshair-vid-withAudio.mp4"

# found on Stack Overflow: https://stackoverflow.com/questions/11779490/how-to-add-a-new-audio-not-mixing-into-a-video-using-ffmpeg

# The -map option allows you to manually select streams / tracks. See FFmpeg Wiki: Map for more info.
# This example uses -c:v copy to stream copy (mux) the video. No re-encoding of the video occurs. Quality is preserved and the process is fast.
# The -shortest option will make the output the same duration as the shortest input.

echo "Starting audio/video merge"
ffmpeg -i $VID_FILE -i $AUDIO_FILE -map 0:v -map 1:a -c:v copy -shortest $OUTPUT_FILE
echo "Done."
