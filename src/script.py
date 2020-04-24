#!/usr/bin/env python3

# This script reads the file 'Esperanto Self-Taught Vocab.csv',
# does some cleaning up and writes the result to 'words.csv'

import csv
import re

# Read in csv file into a list of words with titles intermixed
input_file = open('Esperanto Self-Taught Vocab.csv', 'r')
csv_reader = csv.reader(input_file)
rows = list(csv_reader)
rows = [row[0] for row in rows]

# Cleanup junk that got copied and pasted in
rows = [re.sub(r'\(.*\)', '', row) for row in rows]
rows = [re.sub(r'\[.*\]', '', row) for row in rows]
rows = [re.sub(r'—', '', row) for row in rows]
rows = [re.sub(r',', '', row) for row in rows]
rows = [re.sub(r';', '', row) for row in rows]
rows = [re.sub(r'"', '', row) for row in rows]
rows = [re.sub(r'\'', '', row) for row in rows]

# Remove rows without any words
def more_than_one_alnum_char(x):
    return len(''.join(c for c in x if c.isalnum())) > 0
cleaned_words = filter(more_than_one_alnum_char, rows)
cleaned_words = [word.strip() for word in cleaned_words]
cleaned_words = filter(lambda x: len(x) > 0, cleaned_words)
cleaned_words = list(cleaned_words)

# Split into vocab and phrases sections
phrases_index = cleaned_words.index('Useful and Necessary Expressions.')
vocab_words = cleaned_words[1:phrases_index]
phrases = cleaned_words[phrases_index + 1:]

# Write into csv file
with open('words.csv', 'w') as output_file:
    csv_writer = csv.writer(output_file)
    for row in cleaned_words:
        csv_writer.writerow([row])
