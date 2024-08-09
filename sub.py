import time
import math
import ffmpeg
from faster_whisper import WhisperModel
from googletrans import Translator

input_video = "input.mp4"
input_video_name = input_video.replace(".mp4", "")

def extract_audio():
    extracted_audio = f"audio-{input_video_name}.wav"
    stream = ffmpeg.input(input_video)
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, overwrite_output=True)
    return extracted_audio

def transcribe(audio):
    model = WhisperModel("small") # tiny / base / small / medium / large
    segments, info = model.transcribe(audio)
    language = info[0]
    print("Transcription language detected:", language)
    segments = list(segments)
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" %
              (segment.start, segment.end, segment.text))
    return language, segments

def translate_segments(segments, target_language):
    translator = Translator()
    translated_segments = []
    for segment in segments:
        translated_text = translator.translate(segment.text, dest=target_language).text
        translated_segments.append((segment.start, segment.end, translated_text))
    return translated_segments

def format_time(seconds):
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"
    return formatted_time

def generate_subtitle_file(language, segments, translated=False):
    subtitle_file = f"sub-{input_video_name}.{translated}.{language}.srt"
    text = ""
    for index, segment in enumerate(segments):
        segment_start = format_time(segment[0])
        segment_end = format_time(segment[1])
        text += f"{str(index+1)} \n"
        text += f"{segment_start} --> {segment_end} \n"
        text += f"{segment[2]} \n"
        text += "\n"
        
    with open(subtitle_file, "w") as f:
        f.write(text)

    return subtitle_file

def add_custom_watermark(input_video, output_video, watermark_image):
    stream = (
        ffmpeg
        .input(input_video)  # Input the video stream
        .input(watermark_image)  # Input the watermark image
        .filter_complex('overlay=x=10:y=main_h-overlay_h-10')  # Apply overlay filter with position
        .output(output_video)  # Output the final video with watermark
        .run(overwrite_output=True)
    )
    return output_video

def add_subtitle_to_video(soft_subtitle, subtitle_file, subtitle_language):
    video_input_stream = ffmpeg.input(input_video)
    subtitle_input_stream = ffmpeg.input(subtitle_file)
    output_video = f"output-{input_video_name}.mp4"
    subtitle_track_title = subtitle_file.replace(".srt", "")

    if soft_subtitle:
        stream = ffmpeg.output(
            video_input_stream, subtitle_input_stream, output_video, **{"c": "copy", "c:s": "mov_text"},
            **{"metadata:s:s:0": f"language={subtitle_language}",
            "metadata:s:s:0": f"title={subtitle_track_title}"}
        )
        ffmpeg.run(stream, overwrite_output=True)
    else:
        stream = ffmpeg.output(video_input_stream, output_video,
                               vf=f"subtitles={subtitle_file}")

        ffmpeg.run(stream, overwrite_output=True)

def run():
    extracted_audio = extract_audio()
    language, segments = transcribe(audio=extracted_audio)

    # Generate subtitle for detected language
    subtitle_file = generate_subtitle_file(language, segments)

    # Generate subtitle for another selected language
    selected_language = 'bn'  # Example: 'es' for Spanish
    translated_segments = translate_segments(segments, selected_language)
    translated_subtitle_file = generate_subtitle_file(selected_language, translated_segments, translated=True)
    
    # Add watermark to the video
    # watermark_image = "watermark.png"  # Specify the path to your watermark image
    # watermarked_video = f"watermarked-{input_video_name}.mp4"
    # add_custom_watermark(input_video, watermarked_video, watermark_image)

    # Add subtitles to the video
    add_subtitle_to_video(
        soft_subtitle=False,
        subtitle_file=subtitle_file,
        subtitle_language=language,
    )

    add_subtitle_to_video(
        soft_subtitle=False,
        subtitle_file=translated_subtitle_file,
        subtitle_language=selected_language,
    )

run()
