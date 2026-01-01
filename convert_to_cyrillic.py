#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SRT Subtitle Converter: Latin to Cyrillic (Serbian)
Converts all .srt files from 'original' folder to Cyrillic in 'cyrillic' folder
"""

import os
import re
import difflib
import shutil
from pathlib import Path

# Serbian Latin to Cyrillic transliteration map
LATIN_TO_CYRILLIC = {
    # Digraphs must come first (longer matches have priority)
    'Lj': 'Љ', 'lj': 'љ',
    'Nj': 'Њ', 'nj': 'њ',
    'Dž': 'Џ', 'dž': 'џ', 'DŽ': 'Џ',
    'LJ': 'Љ', 'NJ': 'Њ', 'DZ': 'Џ',
    # Single characters
    'A': 'А', 'a': 'а',
    'B': 'Б', 'b': 'б',
    'V': 'В', 'v': 'в',
    'G': 'Г', 'g': 'г',
    'D': 'Д', 'd': 'д',
    'Đ': 'Ђ', 'đ': 'ђ', 'DJ': 'Ђ', 'Dj': 'Ђ', 'dj': 'ђ',
    'E': 'Е', 'e': 'е',
    'Ž': 'Ж', 'ž': 'ж', 'Z': 'З', 'z': 'з',
    'I': 'И', 'i': 'и',
    'J': 'Ј', 'j': 'ј',
    'K': 'К', 'k': 'к',
    'L': 'Л', 'l': 'л',
    'M': 'М', 'm': 'м',
    'N': 'Н', 'n': 'н',
    'O': 'О', 'o': 'о',
    'P': 'П', 'p': 'п',
    'R': 'Р', 'r': 'р',
    'S': 'С', 's': 'с',
    'T': 'Т', 't': 'т',
    'Ć': 'Ћ', 'ć': 'ћ',
    'U': 'У', 'u': 'у',
    'F': 'Ф', 'f': 'ф',
    'H': 'Х', 'h': 'х',
    'C': 'Ц', 'c': 'ц',
    'Č': 'Ч', 'č': 'ч',
    'Š': 'Ш', 'š': 'ш',
}

# Build regex pattern - sort by length descending to match digraphs first
PATTERN = re.compile('|'.join(
    re.escape(k) for k in sorted(LATIN_TO_CYRILLIC.keys(), key=len, reverse=True)
))


def latin_to_cyrillic(text: str) -> str:
    """Convert Serbian Latin text to Cyrillic."""
    return PATTERN.sub(lambda m: LATIN_TO_CYRILLIC[m.group()], text)


def detect_encoding(file_path: Path) -> str:
    """Try to detect the file encoding."""
    encodings = ['utf-8', 'utf-8-sig', 'cp1250', 'cp1251', 'iso-8859-2', 'iso-8859-1', 'latin-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read()
            return encoding
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    return 'utf-8'  # fallback


def convert_srt_file(input_path: Path, output_path: Path) -> bool:
    """
    Convert a single SRT file from Latin to Cyrillic.
    Returns True if successful, False otherwise.
    """
    try:
        # Detect and read with appropriate encoding
        encoding = detect_encoding(input_path)
        print(f"  Detected encoding: {encoding}")
        
        with open(input_path, 'r', encoding=encoding, errors='replace') as f:
            content = f.read()
        
        # Convert to Cyrillic
        converted_content = latin_to_cyrillic(content)
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write with UTF-8 encoding (with BOM for better compatibility)
        with open(output_path, 'w', encoding='utf-8-sig') as f:
            f.write(converted_content)
        
        return True
    
    except Exception as e:
        print(f"  Error: {e}")
        return False


def find_best_match(filename: str, folders: list) -> Path:
    """Find the best matching folder for a filename."""
    # Normalize filename (replace dots/underscores with spaces)
    clean_name = re.sub(r'[._\[\]()-]', ' ', filename).lower().strip()
    
    best_ratio = 0
    best_folder = None
    
    for folder in folders:
        # Normalize folder name
        clean_folder = re.sub(r'[._\[\]()-]', ' ', folder.name).lower().strip()
        
        # Check similarity
        ratio = difflib.SequenceMatcher(None, clean_name, clean_folder).ratio()
        
        # Boost if substring (e.g. "Monster House" in "Monster House 2006")
        if clean_name in clean_folder or clean_folder in clean_name:
            ratio += 0.3
            
        if ratio > best_ratio and ratio > 0.5:  # Threshold
            best_ratio = ratio
            best_folder = folder
            
    return best_folder


def main():
    """Main function to process all SRT files."""
    # Get the script's directory
    script_dir = Path(__file__).parent.resolve()
    
    # Define input and output directories
    original_dir = script_dir / 'original'
    cyrillic_dir = script_dir / 'cyrillic'
    
    # Validate input directory exists
    if not original_dir.exists():
        print(f"Error: Input directory '{original_dir}' does not exist!")
        return
    
    # Find all .srt files recursively (in movie subfolders)
    srt_files = list(original_dir.glob('**/*.srt'))
    
    if not srt_files:
        print(f"No .srt files found in '{original_dir}'")
        print("\nExpected folder structure:")
        print("  original/")
        print("    MovieName1/")
        print("      subtitle.srt")
        print("    MovieName2/")
        print("      subtitle.srt")
        return
    
    print(f"Found {len(srt_files)} SRT file(s) to convert")
    print(f"Output directory: {cyrillic_dir}")
    print("-" * 50)
    
    # Get existing folders in original for matching
    existing_folders = [f for f in original_dir.iterdir() if f.is_dir()]

    # Process each file
    success_count = 0
    for srt_file in srt_files:
        # Preserve folder structure: get relative path from original_dir
        relative_path = srt_file.relative_to(original_dir)
        
        # Check if file is in root of original_dir
        if len(relative_path.parts) == 1:
            # It's in the root. Try to find a matching folder.
            match = find_best_match(srt_file.stem, existing_folders)
            
            if match:
                folder_name = match.name
                print(f"\n[{folder_name} (Matched existing)]")
            else:
                folder_name = srt_file.stem
                print(f"\n[{folder_name} (Auto-created)]")
                # Create the folder in original
                target_folder = original_dir / folder_name
                target_folder.mkdir(exist_ok=True)
                # Add to existing folders so subsequent files can match it
                existing_folders.append(target_folder)
            
            # Move the original file to the folder
            new_original_path = original_dir / folder_name / srt_file.name
            try:
                shutil.move(str(srt_file), str(new_original_path))
                print(f"  -> Moved original to: {folder_name}/{srt_file.name}")
                # Update srt_file path for conversion
                srt_file = new_original_path
            except Exception as e:
                print(f"  ! Failed to move original: {e}")
            
            output_file = cyrillic_dir / folder_name / srt_file.name
        else:
            # It's already in a subfolder, preserve structure
            output_file = cyrillic_dir / relative_path
            movie_folder = relative_path.parts[0]
            print(f"\n[{movie_folder}]")

        print(f"  Converting: {srt_file.name}")
        
        if convert_srt_file(srt_file, output_file):
            print(f"  ✓ Saved to: {output_file.relative_to(cyrillic_dir)}")
            success_count += 1
        else:
            print(f"  ✗ Failed to convert")
    
    # Summary
    print("\n" + "=" * 50)
    print(f"Conversion complete: {success_count}/{len(srt_files)} files converted successfully")


if __name__ == '__main__':
    main()
