import sys

if len(sys.argv) != 4:
  print("Usage: {} <from word> <to word> <input file>".format(sys.argv[0]))
  exit(1)

from_word, to_word, input_filename = sys.argv[1:4]

with open(input_filename, encoding='utf-8') as input_file:
  for line in input_file:
    line = line.replace(from_word, to_word)
    print(line, end='')

