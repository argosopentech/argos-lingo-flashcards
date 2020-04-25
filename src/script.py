#!/usr/bin/env python3

# This script reads the file 'Esperanto Self-Taught Vocab.csv',
# does some cleaning up and writes the result to 'words.csv'

# Requires apertium and apertium-en-es linux packages (may work on other 
# operating systems)

import csv
import re
import os
import subprocess

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
rows = [re.sub(r'English\.', '', row) for row in rows]
rows = [re.sub(r'&', 'and', row) for row in rows]

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

# Create lessons out of word list
lessons = []
class Lesson:
    title = ''
    words = []
    def __str__(self):
        return self.title + '\n' + '-' * 10 + '\n' + '\n'.join(self.words) 
current_lesson = None
for regex, words in [(r'^[0123456789]*\. ', vocab_words)]:
    for word in words:
        if re.search(regex, word) != None:
            # This row is a title
            word = re.sub(regex, '', word)
            if current_lesson != None:
                lessons.append(current_lesson)
            current_lesson = Lesson()
            current_lesson.title = word
            current_lesson.words = []
        else:
            current_lesson.words.append(word)

# Write to files
output_dir = 'output'
def write_list_to_csv(filename, rows):
    with open(filename, 'w') as output_file:
        csv_writer = csv.writer(output_file)
        for row in rows:
            csv_writer.writerow(row)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(output_dir + '/csv'):
    os.makedirs(output_dir + '/csv')
for lesson in lessons:
    words_as_list = [[word] for word in lesson.words]
    write_list_to_csv(output_dir + '/csv/' + lesson.title + 'csv', words_as_list)
with open(output_dir + '/all_words.csv', 'w') as output_file:
    csv_writer = csv.writer(output_file)
    for row in cleaned_words:
        csv_writer.writerow([row])

# Translate into Spanish
def translate_en_es(word):
    return os.popen('echo ' + word + ' | apertium en-es').read().strip()
if not os.path.exists(output_dir + '/en-es'):
    os.makedirs(output_dir + '/en-es')
for lesson in lessons:
    translated = [[word, translate_en_es(word)] for word in lesson.words]
    translated = filter(lambda x: x[1][0] != '*', translated)
    write_list_to_csv(output_dir + '/en-es/' + lesson.title + 'csv' , translated)
