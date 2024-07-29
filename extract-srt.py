import ffmpeg

input_video = "output-input.mp4"
input_video_name = input_video.replace(".mp4", "")

def extract_srt(input_video):
    try:
        # Inspect the video file to determine subtitle streams
        probe = ffmpeg.probe(input_video)
    except ffmpeg.Error as e:
        print(f"ffprobe error: {e.stderr.decode('utf-8') if e.stderr else str(e)}")
        return []

    subtitle_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'subtitle']
    
    # Extract each subtitle stream
    extracted_files = []
    for index, stream in enumerate(subtitle_streams):
        output_srt = f"{input_video_name}_subtitle_{index}.srt"
        try:
            (
                ffmpeg
                .input(input_video)
                .output(output_srt, map=f"0:s:{index}", c='srt')
                .run(overwrite_output=True)
            )
            print(f"Extracted {output_srt}")
            extracted_files.append(output_srt)
        except ffmpeg.Error as e:
            print(f"Error extracting subtitle {index}: {e.stderr.decode('utf-8') if e.stderr else str(e)}")
    
    return extracted_files

def run():
    extracted_srts = extract_srt(input_video)
    print("Extracted subtitle files:", extracted_srts)

run()
