from moviepy.editor import VideoFileClip

def extract_audio(video_path, audio_path, bitrate='50k'):
  video = VideoFileClip(video_path)
  audio = video.audio
  audio.write_audiofile(audio_path, bitrate=bitrate)
  video.close()
  audio.close()

# How to use
extract_audio('/content/[YOUR FILE].mp4', '/content/audio.mp3')
