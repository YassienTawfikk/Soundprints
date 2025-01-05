import os
import wave


def check_wav_files(directory):
    # Define the target sampling rate and bit depth
    target_sampling_rate = 22050
    target_bit_depth = 16  # 16 bits per sample (2 bytes per sample)

    # Walk through the directory structure
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".wav"):
                path = os.path.join(root, file)
                try:
                    with wave.open(path, 'rb') as wav_file:
                        frame_rate = wav_file.getframerate()
                        sample_width = wav_file.getsampwidth() * 8  # Convert bytes to bits

                        # Check if the file meets the criteria
                        if frame_rate != target_sampling_rate or sample_width != target_bit_depth:
                            print(f"File '{path}' does not meet the format: {frame_rate} Hz, {sample_width} bit")
                except wave.Error as e:
                    print(f"Error reading {path}: {e}")


# Specify the directory containing the WAV files
check_wav_files('static/songs')
