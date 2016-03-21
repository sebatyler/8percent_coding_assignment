import sys

if len(sys.argv) != 2:
  print("Usage: {} <nth>".format(sys.argv[0]))
  exit(1)

def recur(nth, end, add, num):
  if nth == end:
    return num
  else:
    if (nth + 1) % 7 == 0 or int((nth + 1) % 10) == 7 or int((nth + 1) / 10) == 7 :
      return recur(nth + 1, end, -add, num + add)
    else:
      return recur(nth + 1, end, add, num + add)

def pingpong(n):
  return recur(0, n, 1, 0)

print(pingpong(int(sys.argv[1])))

