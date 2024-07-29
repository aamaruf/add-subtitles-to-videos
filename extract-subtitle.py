import argparse
import os
import ffmpeg
import subprocess

input_video_name = None

def download_video(url):
    output_video = "downloaded_video"
    try:
        subprocess.run(["yt-dlp","--no-playlist", "-o", output_video, url], check=True)
        return output_video
    except subprocess.CalledProcessError as e:
        print(f"Error downloading video: {e}")
        return None

def extract_srt(input_video):
    global input_video_name
    input_video_name = os.path.splitext(os.path.basename(input_video))[0]

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

def main():
    parser = argparse.ArgumentParser(description="Extract subtitles from a video file or URL.")
    parser.add_argument("input", help="Path to the video file or URL of the video")
    args = parser.parse_args()

    input_source = args.input
    if input_source.startswith("http://") or input_source.startswith("https://"):
        input_video = download_video(input_source)
        if not input_video:
            print("Failed to download video.")
            return
    else:
        input_video = input_source

    extracted_srts = extract_srt(input_video)
    print("Extracted subtitle files:", extracted_srts)

if __name__ == "__main__":
    main()