#!/usr/bin/env python3

import argparse
import re
import os
import shutil
import random
import nltk
from nltk.corpus import words

# Ensure the nltk words corpus is downloaded
nltk.download('words')

# Predefined replacement rules
specific_replacements = {}

def add_specific_replacement(pattern, replacement):
    specific_replacements[pattern] = replacement

# Adding initial rule for specific replacement
add_specific_replacement(r".*Imported #(\d+) \(0x[0-9a-f]{4}…[0-9a-f]{4} → (0x[0-9a-f]{4}…[0-9a-f]{4})\)", "BLOCK")

def create_backup(file_path):
    backup_path = file_path + ".bak"
    shutil.copy(file_path, backup_path)
    print(f"Backup created at {backup_path}")

def get_four_letter_words():
    four_letter_words = [word.upper() for word in words.words() if len(word) == 4]
    return four_letter_words

# Pre-fetch the list of four-letter words
four_letter_words = get_four_letter_words()

def generate_word():
    word = random.choice(four_letter_words)
    four_letter_words.remove(word)
    return word

def generate_short_hash(long_hash):
    return f"0x{long_hash[2:6]}…{long_hash[-4:]}"

def replace_hashes(content):
    # Find all long hashes
    long_hashes = re.findall(r'0x[0-9a-f]{64}', content)
    short_hashes = re.findall(r'0x[0-9a-f]{4}…[0-9a-f]{4}', content)

    # Create a dictionary to map short hashes to words
    hash_to_word = {}

    for long_hash in long_hashes:
        short_hash = generate_short_hash(long_hash)
        if short_hash not in hash_to_word:
            word = generate_word()
            hash_to_word[short_hash] = word

    for short_hash in short_hashes:
        if short_hash not in hash_to_word:
            word = generate_word()
            hash_to_word[short_hash] = word

    # Apply specific replacements
    for pattern, replacement_prefix in specific_replacements.items():
        print(pattern)
        matches = re.findall(pattern, content)
        for match in matches:
            print(match)
            number = match[0]
            h = match[1]
            replacement_word = f"{replacement_prefix}{number}"
            # content = re.sub(rf'{h}', replacement_word, content)

            final_word = replacement_word
            suffix = 1
            while final_word in hash_to_word.values():
                final_word = f"{replacement_word}f{suffix:02d}"
                suffix += 1

            hash_to_word[h] = final_word

    # Replace short and long hashes in content
    for short_hash, word in hash_to_word.items():
        print(short_hash)
        content = content.replace(short_hash, word)
        long_hash_pattern = re.compile(rf'0x{short_hash[2:6]}[0-9a-f]+{short_hash[-4:]}')
        content = long_hash_pattern.sub(word, content)

    return content, hash_to_word

def write_dictionary_to_file(file_path, hash_to_word):
    dict_file_path = file_path + ".dict"
    with open(dict_file_path, 'w') as dict_file:
        for short_hash, word in hash_to_word.items():
            dict_file.write(f"{short_hash}: {word}\n")

def write_dot_file(content, file_path):
    dot_file_path = file_path + ".dot"
    lines = content.split('\n')
    edges = []

    # Extract parent-child relationships
    for line in lines:
        match = re.search(r'Imported #(\d+) \((\w+) → (\w+)\)', line)
        if match:
            parent = match.group(2)
            child = match.group(3)
            edges.append((parent, child))

    # Write to dot file
    with open(dot_file_path, 'w') as dot_file:
        dot_file.write("digraph G {\n")
        dot_file.write("    rankdir=LR;\n")
        for parent, child in edges:
            dot_file.write(f'    "{child}" -> "{parent}";\n')
        dot_file.write("}\n")

    print(f"DOT file created at {dot_file_path}")

def process_file(file_path, backup=False):
    if backup:
        create_backup(file_path)

    with open(file_path, 'r') as file:
        content = file.read()

    modified_content, hash_to_word = replace_hashes(content)

    with open(file_path, 'w') as file:
        file.write(modified_content)

    write_dictionary_to_file(file_path, hash_to_word)        
    write_dot_file(modified_content, file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Replace hashes in log file with words.')
    parser.add_argument('file', type=str, help='Path to the log file.')
    parser.add_argument('-b', '--backup', action='store_true', help='Create a backup of the original file.')

    args = parser.parse_args()

    process_file(args.file, args.backup)
