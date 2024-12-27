[app]
    |
    |-- [services]                  # Core services for application logic
    |       |-- files_setup.py      # Manages file operations (e.g., file organization and preprocessing)
    |       |-- upload_service.py   # Handles file upload and management
    |       |-- song_mixer.py       # Mixes audio (e.g., weighted averages of songs)
    |
    |-- [models]                    # Domain-specific logic (data representation and operations)
    |       |-- feature_extractor.py  # Extracts and processes audio features (e.g., spectrograms)
    |       |-- fingerprint_matcher.py # Compares fingerprints for similarity identification
    |
    |-- [utils]                     # Helper utilities for shared functionality
    |       |-- clean_cache.py      # Cleans temporary data and cache files
    |
    |-- [ui]                        # User interface components and templates
    |       |-- [template]
    |       |       |-- Mainpage.ui # Layout for the app's main page
    |       |-- Design.py           # Handles PyQt GUI design and interactions
    |
    |-- [tests]                     # Test cases for application components
    |       |-- test_song_mixer.py  # Tests for song mixing functionality
    |       |-- test_feature_extractor.py # Tests for feature extraction module
    |       |-- test_fingerprint_matcher.py # Tests for fingerprint matching
    |       |-- test_ui.py          # Tests for UI functionalities (PyQt components)
    |
    |-- controller.py               # Connects UI, models, and services (acts as the app's brain)
    |
[static]                            # Stores static files for the application
    |
    |-- [features]                  # Extracted audio features (e.g., spectrogram files)
    |-- [fingerprints]              # Fingerprint hashes generated from features
    |-- [images]                    # Static images used in the application
    |-- [songs]                     # Uploaded songs (full, music, and vocals)
    |-- [generated_songs]           # New audio files generated (e.g., mixed tracks)
    |
[main.py]                           # Entry point for starting the application
