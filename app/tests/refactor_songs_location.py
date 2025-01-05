import os
import shutil


def rename_and_move_wav_files(base_path):
    # Define the base path where the "songs" folder is located
    songs_path = os.path.join(base_path, "songs")

    # Iterate over each folder in the "songs" directory
    for folder_name in os.listdir(songs_path):
        folder_path = os.path.join(songs_path, folder_name)

        # Ensure the current path is a directory
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                # Process only .wav files
                if file_name.endswith(".wav"):
                    # Construct the new file name
                    new_file_name = f"{folder_name}_{file_name}"

                    # Define the source and destination paths
                    source_path = os.path.join(folder_path, file_name)
                    destination_path = os.path.join(songs_path, new_file_name)

                    # Move and rename the file to the "songs" directory
                    shutil.move(source_path, destination_path)

            # Optionally, remove the now-empty folder
            try:
                os.rmdir(folder_path)
            except OSError:
                pass  # Ignore if the folder isn't empty (e.g., contains image files)


# Replace with your base path
base_directory = ""
rename_and_move_wav_files(base_directory)
