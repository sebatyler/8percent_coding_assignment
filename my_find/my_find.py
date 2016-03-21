import sys, os, re

if len(sys.argv) < 3:
  print("Usage: {} <directory> <suffix>".format(sys.argv[0]))
  exit(1)

directory = sys.argv[1]
suffix = sys.argv[2]
regex = re.compile("\.{}$".format(suffix))

for root, dirs, files, rootfd in os.fwalk(directory):
  for filename in files:
    if regex.search(filename):
      print(os.path.abspath(os.path.join(root, filename)))

