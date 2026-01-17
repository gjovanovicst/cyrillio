# Cyrillio - SRT Subtitle Tools

Python tools for processing Serbian subtitle files (.srt):
- Convert Latin script to Cyrillic
- Translate Croatian vocabulary to Serbian

## Scripts

### 1. Latin to Cyrillic Converter (`convert_to_cyrillic.py`)

Converts Serbian Latin subtitles to Cyrillic script.

**Features:**
- Handles digraphs (Lj, Nj, Dž) correctly
- Supports Serbian Latin characters (Č, Ć, Ž, Š, Đ)
- Auto-detects file encoding
- Maintains folder structure

**Usage:**
```bash
# Place .srt files in the original/ folder, then run:
python convert_to_cyrillic.py
```

Converted files appear in the `cyrillic/` folder.

### 2. Croatian to Serbian Translator (`translate_croatian_to_serbian.py`)

Translates Croatian vocabulary to Serbian equivalents in subtitle files.

**Features:**
- 1200+ word mappings covering:
  - Location/time adverbs (ovdje→ovde, uvijek→uvek, gdje→gde)
  - Verb conjugations (vidjeti→videti, osjećati→osećati)
  - Future tense patterns (bit ću→biću, Voljet će→Voleće)
  - Common nouns (čovjek→čovek, dijete→dete, dečki→momci)
  - Days/months (ponedjeljak→ponedeljak, siječanj→januar)
  - Vocabulary (tisuća→hiljada, vlak→voz, glazba→muzika)
- Auto-detects file encoding (UTF-8, CP1250, ISO-8859-2)
- Word boundary matching to avoid partial replacements

**Usage:**
```bash
# Translate a single file (creates file_sr.srt)
python translate_croatian_to_serbian.py subtitle.srt

# Translate text directly
python translate_croatian_to_serbian.py -t "Što radiš?"

# Translate all .srt files in a directory
python translate_croatian_to_serbian.py -r input_folder/

# Translate in place (overwrite original)
python translate_croatian_to_serbian.py -i subtitle.srt

# Specify output file
python translate_croatian_to_serbian.py subtitle.srt -o translated.srt
```

## Folder Structure

```
.
├── convert_to_cyrillic.py           # Latin to Cyrillic converter
├── translate_croatian_to_serbian.py # Croatian to Serbian translator
├── original/                        # Input folder for subtitles
│   └── Movie Name/
│       └── subtitle.srt
└── cyrillic/                        # Output folder for Cyrillic subtitles
    └── Movie Name/
        └── subtitle.srt
```

## Requirements

- Python 3.6+
- Standard library only (no external dependencies)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
