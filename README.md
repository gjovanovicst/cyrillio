# Cyrillio - SRT Subtitle Converter

A Python tool to convert Serbian Latin subtitles (.srt) to Cyrillic.

## Description

This script automatically converts subtitle files from Latin script to Serbian Cyrillic. It processes `.srt` files located in the `original` directory and saves the converted versions to the `cyrillic` directory, maintaining the folder structure.

It handles:
- Digraphs (Lj, Nj, Dž) correctly.
- Standard Serbian Latin characters (Č, Ć, Ž, Š, Đ).
- Automatic encoding detection for input files.
- Organization of files into movie folders if they are in the root directory.

## Usage

1.  Ensure you have Python installed.
2.  Place your Latin `.srt` files in the `original` folder. You can organize them into subfolders (e.g., by movie name) or put them directly in the root of `original`.
3.  Run the script:

    ```bash
    python convert_to_cyrillic.py
    ```

4.  The converted files will appear in the `cyrillic` folder.

## Folder Structure

```
.
├── convert_to_cyrillic.py  # Main script
├── original/               # Input folder for Latin subtitles
│   └── Movie Name/
│       └── subtitle.srt
└── cyrillic/               # Output folder for Cyrillic subtitles
    └── Movie Name/
        └── subtitle.srt
```

## Requirements

- Python 3.6+
- Standard library only (no external dependencies)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
