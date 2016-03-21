def poker_numbers_shapes(hands):
  numbers = {}
  shapes = { 'D': [], 'H': [], 'S': [], 'C': [] }

  for hand in hands:
    number = int(hand[0].replace('T', '10').replace('J', '11').replace('Q', '12').replace('K', '13').replace('A', '14'))
    shape = hand[1]

    if number in numbers.keys():
      numbers[number].append(shape)
    else:
      numbers[number] = [shape]

    shapes[shape].append(number)

  return numbers, shapes

def poker_status(numbers, shapes, sorted_numbers):
  status = { 'pairs': [] }

  for v in shapes.values():
    if len(v) == 5:
      status['flush'] = sorted(v)

  # check if one pair, two pair, three, four
  for number, shape in numbers.items():
    shape_count = len(shape)
    if shape_count == 2:
      status['pairs'].append(number)
    elif shape_count == 3:
      status['three'] = [number]
    elif shape_count == 4:
      status['four'] = [number]

  status['pairs'] = sorted(status['pairs'])

  # check if straight
  if len(sorted_numbers) == 5 and sorted_numbers[-1] - sorted_numbers[0] == 4:
    status['straight'] = sorted_numbers

  return status

def poker_rank_score_values(status, sorted_numbers):
  rank = None
  score = 0
  values = []

  # rank for debugging
  if status.get('straight') and status.get('flush'):
    if sorted_numbers[0] == 10:
      rank, score, values = 'RoyalFlush', 900, sorted_numbers
    else:
      rank, score, values = 'StraightFlush', 800, sorted_numbers
  elif status.get('four'):
    rank, score, values = 'FourOfAKind', 700, status['four']
  elif status.get('three') and len(status['pairs']) == 1:
    rank, score, values = 'FullHouse', 600, status['pairs'] + status['three']
  elif status.get('flush'):
    rank, score, values = 'Flush', 500, status['flush']
  elif status.get('straight'):
    rank, score, values = 'Straight', 400, status['straight']
  elif status.get('three'):
    rank, score, values = 'ThreeOfAKind', 300, status['three']
  elif len(status['pairs']) == 2:
    rank, score, values = 'TwoPair', 200, status['pairs']
  elif len(status['pairs']) == 1:
    rank, score, values = 'OnePair', 100, status['pairs']

  if score == 0:
    score, values = sorted_numbers[-1], sorted_numbers

  return rank, score, values

def poker_result(hands):
  result = { 'hands': hands }
  numbers, shapes = poker_numbers_shapes(hands)
  sorted_numbers = sorted(numbers.keys())
  status = poker_status(numbers, shapes, sorted_numbers)
  rank, score, values = poker_rank_score_values(status, sorted_numbers)

  result['rank'] = rank
  result['score'] = score
  result['values'] = values
  result['numbers'] = numbers
  result['status'] = status

  return result

def poker(hands):
  player1 = poker_result(hands[:5])
  player2 = poker_result(hands[5:])

  diff = player1['score'] - player2['score']
  if diff == 0:
    # if same ranked hands then the rank made up of the highest value wins
    for i in reversed(range(len(player1['values']))):
      d = player1['values'][i] - player2['values'][i]
      if d != 0:
        diff += d
        break

    # compare rest values
    if diff == 0:
      rest = lambda player: sorted(set(player['numbers'].keys()) - set(player['values']))
      rest_values1, rest_values2  = rest(player1), rest(player2)
      for i in reversed(range(len(rest_values1))):
        d = rest_values1[i] - rest_values2[i]
        if d != 0:
          diff += d
          break

  return 0 if diff > 0 else 1

wins = [0, 0]

with open('poker.txt') as data_file:
  for line in data_file:
    hands = line.strip().split(' ')
    if len(hands) < 2:
      break

    winner = poker(hands)
    wins[winner] += 1

print("Player 1 wins: {}/{}".format(wins[0], wins[0] + wins[1]))

