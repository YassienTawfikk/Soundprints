import os
import random


def randomly_number_songs(base_path):
    # Define the songs folder path
    songs_path = os.path.join(base_path, "songs")

    # Get a list of all .wav files in the songs folder
    wav_files = [file for file in os.listdir(songs_path) if file.endswith(".wav")]

    # Generate a list of random numbers for the number of files
    random_numbers = list(range(1, len(wav_files) + 1))
    random.shuffle(random_numbers)

    # Rename each file with a random number
    for index, file_name in enumerate(wav_files):
        # Construct the new file name with leading zeros
        new_file_name = f"{str(random_numbers[index]).zfill(2)}.wav"

        # Define the source and destination paths
        source_path = os.path.join(songs_path, file_name)
        destination_path = os.path.join(songs_path, new_file_name)

        # Rename the file
        os.rename(source_path, destination_path)


# Replace with your base path
base_directory = ""
randomly_number_songs(base_directory)
