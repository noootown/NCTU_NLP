import math
import re
import json
from collections import defaultdict

def tf(word, blob):
  return sum([word == w for w in blob])

def n_containing(word, bloblist):
  return [word in blob for blob in blobList]

def idf(word, bloblist):
  return math.log10(len(blobList) / (1 + n_containing(word, bloblist)))

if __name__ == '__main__':
  with open('movie_lines-input.txt', 'r') as file1:
    movieLine = [line.strip().lower() for line in file1]

  data = []
  blobList = [re.findall(r"[\w']+", line) for line in movieLine]

  for line in movieLine:
    data.extend(re.findall(r"[\w']+", line))

  countDict = defaultdict(int)
  for d in data:
    countDict[d] += 1
  word = [w[0] for w in sorted([w for w in countDict.items()], key = lambda w: -w[1])[0:300]]

  with open('word.json', 'w') as file:
    json.dump(word, file)

  idfdict = defaultdict(int)
  idfdict = {w: idf(w, blobList) for w in word}
  with open('idf.json', 'w') as file:
    json.dump(idfdict, file)

  idflist = ['%.4f' % idfdict[w] for w in word]

  with open('task/1.txt') as file:
    ml = [line.strip().lower() for line in file]
    blobList1 = [re.findall(r"[\w']+", line) for line in ml]

  with open('ans/Answer1.txt', 'w') as file:
    file.write('|'.join(word) + '\n')
    file.write(','.join(idflist) + '\n')

    for i, blob in enumerate(blobList1):
      scores = [tf(w, blob) * (idfdict[w] if w in idfdict else 0) for w in word]
      file.write(','.join(['%.4f' % s for s in scores]) + '\n')
