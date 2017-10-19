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

def calLen(vector):
  return math.sqrt(sum([value ** 2 for value in vector]))

def calcosine(va, vb):
  n = 0
  for i in range(len(va)):
    n += va[i] * vb[i]

  return n / calLen(va) / calLen(vb)

def caldice(va, vb):
  n = 0
  for i in range(len(va)):
    n += va[i] * vb[i]

  return 2 * n / (calLen(va) + calLen(vb))

if __name__ == '__main__':
  with open('movie_lines-input.txt', 'r') as file1:
    movieLine = [line.strip().lower() for line in file1]

  N = len(movieLine)

  movieBlob = {}

  with open('movie.txt', 'r') as file:
    for line in file:
      movie = re.findall('(m\d*),(.*)', line)[0]
      movieBlob[movie[0]] = [word.lower() for word in re.findall(r"[\w']+", movie[1])]

  with open('word.json', 'r') as file:
    word = json.load(file)

  with open('idf.json', 'r') as file:
    idfdict = json.load(file)

  idflist = ['%.4f' % idfdict[w] for w in word]

  movietfidf = {}
  movieList = set([k for k, v in movieBlob.items()])

  for k, v in movieBlob.items():
    movietfidf[k] = [tf(w, v) * (idfdict[w] if w in idfdict else 0) for w in word]

  sim = []
  for moviea in movieList:
    for movieb in movieList:
      if moviea == movieb:
        continue
      else:
        # sim.append((moviea, movieb, calcosine(movietfidf[moviea], movietfidf[movieb])))
        sim.append((moviea, movieb, caldice(movietfidf[moviea], movietfidf[movieb])))

  sim.sort(key = lambda m: -m[2])

  ma = sim[0][0]
  mb = sim[0][1]
  mc = ''
  md = ''

  for s in sim[1:]:
    if s[0] == ma or s[0] == mb:
      mc = s[1]
    elif s[1] == ma or s[1] == mb:
      mc = s[0]

    if mc != '' and mc != ma and mc != mb:
      break

  for s in sim[::-1]:
    if s[0] == ma or s[0] == mb:
      md = s[1]
    elif s[1] == ma or s[1] == mb:
      md = s[0]

    if md != '' and md != ma and md != mb:
      break

  movieIDToName = defaultdict(str)

  with open('cornell/movie_titles_metadata.txt', 'r', encoding = 'latin1') as file:
    for line in file:
      info = line.split(' +++$+++ ')
      movieIDToName[info[0]] = info[1]

  # with open('ans/Answer3-1.txt', 'w') as file:
  with open('ans/Answer3-2.txt', 'w') as file:
    file.write('%s|%s|%s\n' % (movieIDToName[ma], movieIDToName[mb], movieIDToName[mc]))
    file.write(','.join(word) + '\n')
    file.write(','.join(['%.4f' % num for num in movietfidf[ma]]) + '\n')
    file.write(','.join(['%.4f' % num for num in movietfidf[mb]]) + '\n')
    file.write(','.join(['%.4f' % num for num in movietfidf[mc]]) + '\n')
    file.write('%s\n' % movieIDToName[md])
    file.write(','.join(['%.4f' % num for num in movietfidf[md]]) + '\n')
