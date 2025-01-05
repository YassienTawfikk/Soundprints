import os
import subprocess
import json
import scipy
import soundfile as sf
from scipy.io.wavfile import read, write


def get_audio_bitrate(file_path):
    """
    Uses ffprobe to get the audio bitrate (in kbps) of the given file.
    Returns an integer bitrate (e.g., 32 for 32 kbps).
    If there's any error, returns None.
    """
    try:
        cmd = [
            "ffprobe", "-v", "quiet", "-print_format", "json",
            "-show_streams", file_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        info = json.loads(result.stdout)

        for stream in info.get("streams", []):
            if stream.get("codec_type") == "audio":
                bit_rate_bps = stream.get("bit_rate")
                if bit_rate_bps:
                    return int(int(bit_rate_bps) / 1000)  # Convert to kbps
        return None
    except Exception as e:
        print(f"ffprobe error on {file_path}: {e}")
        return None


def convert_to_32k_wav(file_path, sample_rate=22050, target_bitrate="32k"):
    """
    Converts the input WAV to WAV at 32 kbps with the specified sample rate.
    Overwrites the original file in-place (creates a temp file first).
    """
    dir_name, base_name = os.path.split(file_path)
    temp_file_path = os.path.join(dir_name, f"temp_{base_name}")

    cmd = [
        "ffmpeg",
        "-y",  # Overwrite output
        "-i", file_path,
        "-c:a", "adpcm_ms",
        "-ar", str(sample_rate),
        "-b:a", target_bitrate,
        temp_file_path
    ]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
    except Exception as e:
        print(f"Error converting {file_path} -> {e}")
        return

    os.remove(file_path)
    os.rename(temp_file_path, file_path)
    print(f"Converted {file_path} to {target_bitrate} at {sample_rate} Hz")


def check_and_convert_sampling_rate(file_path, target_rate=22050):
    """
    Checks the sampling rate of a WAV file and converts it to the target rate if needed.
    """
    try:
        with sf.SoundFile(file_path) as sound_file:
            current_rate = sound_file.samplerate

        if current_rate != target_rate:
            print(f"Converting {file_path} from {current_rate} Hz to {target_rate} Hz")

            rate, data = read(file_path)
            num_samples = int(len(data) * target_rate / rate)
            resampled_data = scipy.signal.resample(data, num_samples)

            write(file_path, target_rate, resampled_data.astype(data.dtype))
        else:
            print(f"{file_path} already at {target_rate} Hz, skipping.")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")


def check_and_convert(directory, desired_bitrate=32, target_rate=22050):
    """
    Walks through the given directory, checks each .wav file's bitrate and sampling rate.
    Converts files to the desired specifications if needed.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".wav"):
                file_path = os.path.join(root, file)

                # Check and convert bitrate
                bitrate = get_audio_bitrate(file_path)
                if bitrate is None:
                    print(f"Could not detect bitrate for {file_path}, skipping.")
                    continue
                if bitrate != desired_bitrate:
                    print(f"{file_path} is {bitrate} kbps, converting to {desired_bitrate} kbps...")
                    convert_to_32k_wav(file_path, sample_rate=target_rate, target_bitrate="32k")

                # Check and convert sampling rate
                check_and_convert_sampling_rate(file_path, target_rate=target_rate)


if __name__ == "__main__":
    directory_path = "/Users/yassientawfik/Downloads/Unknown Songs"  # Specify your directory here
    check_and_convert(directory_path, desired_bitrate=32, target_rate=22050)
