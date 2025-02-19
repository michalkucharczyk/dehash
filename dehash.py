#!/usr/bin/env python3

import argparse
import time
import re
import os
import shutil
import random
import nltk
from nltk.corpus import words

# Ensure the nltk words corpus is downloaded
nltk.download('words')

# Predefined replacement rules
specific_replacements = []

def add_specific_replacement(pattern, replacement, guard):
    """Add a specific replacement rule to the dictionary."""
    specific_replacements.append((pattern, replacement, guard))

add_specific_replacement(
        r".*\[Relaychain\]...Imported #(\d+) \(0x[0-9a-f]{4}…[0-9a-f]{4} → (0x[0-9a-f]{4}…[0-9a-f]{4})\)",
        "RBLOCK",
        "Imported"
)
add_specific_replacement(
        r".*\[Parachain\]...Imported #(\d+) \(0x[0-9a-f]{4}…[0-9a-f]{4} → (0x[0-9a-f]{4}…[0-9a-f]{4})\)",
        "BLOCK",
        "Imported"
)
add_specific_replacement(
        r".*substrate:...Imported #(\d+) \(0x[0-9a-f]{4}…[0-9a-f]{4} → (0x[0-9a-f]{4}…[0-9a-f]{4})\)",
        "BLOCK",
        "Imported"
)
add_specific_replacement(
        r".*substrate_test_runtime_transaction_pool: add_block: (\d+) (0x[0-9a-f]{64}) .*", 
        "BLOCK", 
        "add_block"
)

def filter_and_findall(content, guard_pattern, find_pattern):
    """Filter lines by guard pattern and find all matches of find pattern. This
    is to pre-filter content before using regex."""
    lines = content.split('\n')
    filtered_lines = [line for line in lines if re.search(guard_pattern, line)]
    filtered_content = '\n'.join(filtered_lines)
    return re.findall(find_pattern, filtered_content)

def replace_matches_in_place(content, pattern, replacement):
    """Replace matches in content using the replacement function which is
    intended to map the match (hash) to replacement word. The copy of the
    content is built incrementally. Avoids multiple memcpy operations."""
    matches = [(match.start(), match.end(),match.group()) for match in re.finditer(pattern, content)]
    parts = []
    last_end = 0
    
    for start, end, match_text in matches:
        parts.append(content[last_end:start])
        parts.append(replacement(match_text))
        last_end = end
    
    parts.append(content[last_end:])
    return ''.join(parts)

def create_backup(file_path):
    """Create a backup of the given file."""
    backup_path = file_path + ".bak"
    shutil.copy(file_path, backup_path)
    # print(f"Backup created at {backup_path}")


def get_words(length):
    """Get a shuffled list of four to six letter words."""
    new_words = list({word.upper() for word in words.words() if len(word) == length})
    random.shuffle(new_words)
    return new_words

# The list of generated words and a current word size used
current_word_size = 4
generated_words = get_words(current_word_size)

def append_word_to_dictionary(word):
    global generated_words
    generated_words.append(word)

def generate_word():
    """Generate a four-letter word from the pre-fetched list."""
    global generated_words
    if len(generated_words) == 0:
        global current_word_size
        current_word_size = current_word_size + 1
        generated_words = get_words(current_word_size)
    return generated_words.pop()

def generate_short_hash(long_hash):
    """Generate a short hash from a long hash."""
    return f"0x{long_hash[2:6]}…{long_hash[-4:]}"

def replace_hashes(content, initial_hash_to_word):
    """Build dictionary and replace hashes in the content."""
    start_time = time.time()
    long_hashes = re.findall(r'0x[0-9a-f]{64}', content)
    short_hashes = re.findall(r'0x[0-9a-f]{4}…[0-9a-f]{4}', content)
    # print(f"1 Execution time: {time.time() - start_time}")

    # Create a dictionary to map short hashes to words
    hash_to_word = initial_hash_to_word

    start_time = time.time()
    for (pattern, replacement_prefix, guard) in specific_replacements:
        match_start_time = time.time()
        matches = filter_and_findall(content, guard, pattern)
        # print(f"X Execution time: {time.time() - match_start_time}")

        for match in matches:
            # print("found match:",match)
            number = match[0]
            h = match[1]
            if len(h) == 66:
                h = generate_short_hash(h)

            if h not in hash_to_word:
                replacement_word = f"{replacement_prefix}{number}"

                final_word = replacement_word
                suffix = 1

                while final_word in hash_to_word.values():
                    final_word = f"{replacement_word}f{suffix:02d}"
                    suffix += 1

                hash_to_word[h] = final_word
    # print(f"2 Execution time: {time.time() - start_time}")

    start_time = time.time()
    for long_hash in long_hashes:
        short_hash = generate_short_hash(long_hash)
        if short_hash not in hash_to_word:
            hash_to_word[short_hash] = generate_word()
    # print(f"3 Execution time: {time.time() - start_time}")

    start_time = time.time()
    for short_hash in short_hashes:
        if short_hash not in hash_to_word:
            hash_to_word[short_hash] = generate_word()
    # print(f"4 Execution time: {time.time() - start_time}")

    # print(f"long_hashes count: {len(long_hashes)}")
    # print(f"short_hashes count: {len(short_hashes)}")
    print(f"hash_to_word count: {len(hash_to_word)}")

    start_time = time.time()
    content = replace_matches_in_place(content, r'0x[0-9a-f]{4}…[0-9a-f]{4}', lambda h: hash_to_word[h])
    content = replace_matches_in_place(content, r'0x[0-9a-f]{64}', lambda h: hash_to_word[generate_short_hash(h)])
    # print(f"5 Execution time: {time.time() - start_time}")

    return content, hash_to_word

def write_dictionary_to_file(file_path, hash_to_word):
    """Write the hash-to-word dictionary to a file."""
    dict_file_path = file_path + ".dict"
    with open(dict_file_path, 'w') as dict_file:
        for short_hash, word in hash_to_word.items():
            dict_file.write(f"{short_hash}: {word}\n")

def read_dictionary_from_file(dict_file_path):
    """Read the hash-to-word dictionary from a file."""
    hash_to_word = {}
    with open(dict_file_path, 'r') as dict_file:
        for line in dict_file:
            short_hash, word = line.strip().split(": ")
            hash_to_word[short_hash] = word
    return hash_to_word

def write_dot_file(content, file_path):
    """Write a DOT file representing parent-child relationships."""
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
        dot_file.write("    rankdir=BT;\n")
        for parent, child in edges:
            dot_file.write(f'    "{child}" -> "{parent}";\n')
        dot_file.write("}\n")

    # print(f"DOT file created at {dot_file_path}")

def process_file(file_path, backup, initial_hash_to_word):
    """Process the file by replacing hashes and creating backups if required."""
    if backup:
        create_backup(file_path)

    with open(file_path, 'r') as file:
        content = file.read()

    modified_content, hash_to_word = replace_hashes(content, initial_hash_to_word)

    with open(file_path, 'w') as file:
        file.write(modified_content)

    write_dictionary_to_file(file_path, hash_to_word)        
    write_dot_file(modified_content, file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Replace hashes in the log file with words.')
    parser.add_argument('file', type=str, help='Path to the log file.')
    parser.add_argument('-b', '--backup', action='store_true', help='Create a backup of the original file.')
    parser.add_argument('-d', '--dict-file', type=str, help='Dictionary file name', required=False)
    args = parser.parse_args()

    initial_hash_to_word = {}
    if args.dict_file:
        initial_hash_to_word = read_dictionary_from_file(args.dict_file)

    process_file(args.file, args.backup, initial_hash_to_word)
