import os
import re

base_path = r"/Users/yassientawfik/Documents/Projects/Semester_05_Projects/DSP/05/Spectrogram_Fingerprinting/static/songs"

ORIGINAL_KEYWORDS = ["original", "full"]
VOCALS_KEYWORDS = ["vocal", "vocals", "lyric", "lyrics", "lyrcis"]
INSTR_KEYWORDS = ["instrument", "instruments", "instrumental", "music"]


def classify_file(filename_lower):
    """
    Determine which category this file belongs to:
      - "song"               -> if 'original'/'full' found OR no keywords
      - "vocals"             -> if only vocals keywords
      - "instruments"        -> if only instruments keywords
      - "vocals_instruments" -> if both vocals & instruments keywords
    """
    has_original = any(kw in filename_lower for kw in ORIGINAL_KEYWORDS)
    has_vocals = any(kw in filename_lower for kw in VOCALS_KEYWORDS)
    has_instr = any(kw in filename_lower for kw in INSTR_KEYWORDS)

    # 'original' / 'full' overrides everything => "song"
    if has_original:
        return "song"

    if has_vocals and has_instr:
        return "vocals_instruments"
    elif has_vocals:
        return "vocals"
    elif has_instr:
        return "instruments"
    else:
        # No known keywords => treat as original
        return "song"


def strip_noise_in_name(filename):
    """
    Removes parentheses and contents, and also
    removes any "GroupXX_" / "TeamXX_" prefix.
    Normalizes multiple spaces/underscores -> single underscore.
    """
    # Remove parentheses (and their contents)
    no_parens = re.sub(r"\([^)]*\)", "", filename)

    # Remove GroupXX_/TeamXX_ (case-insensitive)
    no_groups = re.sub(r"(Group\d+_|Team\d+_)", "", no_parens, flags=re.IGNORECASE)

    # Replace multiple spaces/underscores with single underscore
    cleaned = re.sub(r"[ \t_]+", "_", no_groups.strip())

    return cleaned


def infer_song_name(files):
    """
    Given a list of filenames in one folder, try to infer the "song name"
    from a file that has 'original'/'full'. If none, pick the first file.
    Remove any keywords (original, full, music, etc.) from the final name.
    If no files exist, return empty string.
    """
    if not files:
        return ""

    # 1) Look for 'original'/'full'
    for f in files:
        name, _ = os.path.splitext(f)
        lower = name.lower()
        if any(kw in lower for kw in ORIGINAL_KEYWORDS):
            # This file might represent the "real" name
            cleaned = strip_noise_in_name(name)
            # Remove the classification keywords from the name
            for kw in (ORIGINAL_KEYWORDS + VOCALS_KEYWORDS + INSTR_KEYWORDS):
                cleaned = re.sub(kw, "", cleaned, flags=re.IGNORECASE)
            # Clean leftover underscores
            cleaned = re.sub(r"_+", "_", cleaned).strip("_")
            return cleaned

    # 2) If no 'original'/'full', pick the first file
    name, _ = os.path.splitext(files[0])
    cleaned = strip_noise_in_name(name)
    for kw in (ORIGINAL_KEYWORDS + VOCALS_KEYWORDS + INSTR_KEYWORDS):
        cleaned = re.sub(kw, "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned


def ensure_no_collision(dst_path):
    """
    If dst_path already exists, we append _2, _3, ... until
    we find a name that doesn't exist. Return the final path.
    Example: if "vocals.wav" exists, try "vocals_2.wav", "vocals_3.wav", etc.
    """
    if not os.path.exists(dst_path):
        return dst_path

    base, ext = os.path.splitext(dst_path)
    counter = 2
    while True:
        candidate = f"{base}_{counter}{ext}"
        if not os.path.exists(candidate):
            return candidate
        counter += 1


def rename_folder(old_folder_path, new_folder_name):
    """
    Renames the given folder to new_folder_name (in the same parent directory),
    handling case differences or collisions. Returns the new full path.
    """
    parent_dir = os.path.dirname(old_folder_path)
    new_path = os.path.join(parent_dir, new_folder_name)

    # If the new path is the same as old path (case-insensitive), skip
    if old_folder_path.lower() == new_path.lower():
        return old_folder_path  # No rename needed

    # If there's a collision with an existing folder, we keep appending _2, _3, ...
    final_path = new_path
    suffix = 2
    while os.path.exists(final_path) and final_path.lower() != old_folder_path.lower():
        final_path = os.path.join(parent_dir, f"{new_folder_name}_{suffix}")
        suffix += 1

    if final_path != old_folder_path:
        print(f"Renaming folder:\n  {old_folder_path}\n  --> {final_path}\n")
        os.rename(old_folder_path, final_path)

    return final_path


def rename_files_in_folder(folder_path):
    """
    Renames each file in the folder to 'song.ext', 'vocals.ext', 'instruments.ext',
    or 'vocals_instruments.ext'. If there's a collision, appends _2, _3, ...
    """
    for fname in os.listdir(folder_path):
        old_path = os.path.join(folder_path, fname)
        if not os.path.isfile(old_path):
            continue  # skip subfolders if any
        name_part, ext = os.path.splitext(fname)

        # We'll keep the extension as is (no conversion)
        # Classify
        ctype = classify_file(name_part.lower())  # "song", "vocals", "instruments", "vocals_instruments"
        new_fname = f"{ctype}{ext}"  # e.g. "vocals.wav"

        new_path_candidate = os.path.join(folder_path, new_fname)
        # Ensure no collision
        final_new_path = ensure_no_collision(new_path_candidate)

        if final_new_path.lower() != old_path.lower():
            print(f"Renaming file:\n  {old_path}\n  --> {final_new_path}\n")
            os.rename(old_path, final_new_path)


def main():
    # List everything in base_path
    all_items = os.listdir(base_path)

    # For each subfolder (Team_X, etc.)
    for item in all_items:
        old_folder_path = os.path.join(base_path, item)

        if os.path.isdir(old_folder_path):
            # Collect all WAV / MP3 (if any) files
            files = [f for f in os.listdir(old_folder_path)
                     if os.path.isfile(os.path.join(old_folder_path, f))
                     and not f.startswith('.')  # skip hidden
                     ]
            # Infer the new folder name
            song_name = infer_song_name(files)  # might be empty if folder is empty
            if not song_name:
                # If we can't find a name or folder is empty, name it "UntitledSong"
                song_name = "UntitledSong"

            # Clean up weird characters in folder name if needed
            # e.g. remove punctuation except underscores/dashes
            # or you can keep them. Example:
            song_name = re.sub(r"[^\w\-\+]+", "_", song_name.strip())

            # Rename the folder
            new_folder_path = rename_folder(old_folder_path, song_name)

            # Rename files inside the folder
            rename_files_in_folder(new_folder_path)


if __name__ == "__main__":
    main()
