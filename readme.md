# A Python application capable of extracting audio from an input video, transcribing the extracted audio, generating a subtitle file based on the transcription, and then adding the subtitle to a copy of the input video.

# To build this application, FFmpeg is used to extract audio from an input video. OpenAI’s Whisper is used to generate a transcript for the extracted audio and then this transcript is used to generate a subtitle file. Again, FFmpeg is used to add the generated subtitle file to a copy of the input video.

# FFmpeg is a powerful and open-source software suite for handling multimedia data, including audio and video processing tasks. It provides a command-line tool that allows users to convert, edit, and manipulate multimedia files with a wide range of formats and codecs.

# OpenAI’s Whisper is an automatic speech recognition (ASR) system designed to convert spoken language into written text. Trained on a vast amount of multilingual and multitasking supervised data, it excels at transcribing diverse audio content with high accuracy.