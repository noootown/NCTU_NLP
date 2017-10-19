import math
import re
import json

def tf(word, blob):
  return sum([word == w for w in blob])

def n_containing(word, bloblist):
  return [word in blob for blob in blobList]

def idf(word, bloblist):
  return math.log10(len(blobList) / (1 + n_containing(word, bloblist)))

# code to get pos.json
# from collections import defaultdict
# posdict = defaultdict('')
#
# for f in formatData:
#   for t in f['tokens']:
#     key = t['word'].lower()
#     posdict[key] = t['pos']

if __name__ == '__main__':
  with open('movie_lines-input.txt', 'r') as file1:
    movieLine = [line.strip().lower() for line in file1]

  with open('pos.json', 'r') as file:
    posdict = json.load(file)

  N = len(movieLine)

  blobList = [re.findall(r"[\w']+", line) for line in movieLine]
  data = []

  for line in movieLine:
    data.extend(re.findall(r"[\w']+", line))

  with open('word.json', 'r') as file:
    word = json.load(file)

  with open('idf.json', 'r') as file:
    idfdict = json.load(file)
    idflist = ['%.4f' % idfdict[w] for w in word]

  with open('task/2.txt') as file:
    ml = [line.strip().lower() for line in file]
    blobList1 = [re.findall(r"[\w']+", line) for line in ml]

  with open('ans/Answer2.txt', 'w') as file:
    file.write('|'.join(word) + '\n')
    file.write(','.join([posdict[w] if w in posdict else '' for w in word]) + '\n')
    file.write(','.join(idflist) + '\n')

    for i, blob in enumerate(blobList1):
      scores = [tf(w, blob) * (idfdict[w] if w in idfdict else 0) for w in word]
      file.write(','.join(['%.4f' % s for s in scores]) + '\n')
