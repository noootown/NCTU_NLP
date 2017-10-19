import math
import json
from functools import reduce

def flatten(arr):
  f = lambda p, c: p + reduce(f, c, []) if isinstance(c, list) else p + [c, ]
  return f([], arr)

def calEntropy(data):
  unigram = flatten(data)
  lu = len(unigram)
  unigramDict = {u: i for i, u in enumerate(unigram)}
  bigram = [[0] * lu for i in range(lu)]

  size = 0
  allNum = 0

  for s in data:
    for i in range(len(s) - 1):
      allNum += 1

      if bigram[unigramDict[s[i]]][unigramDict[s[i + 1]]] == 0:
        size += 1

      bigram[unigramDict[s[i]]][unigramDict[s[i + 1]]] += 1

  hxy = 0
  for i in bigram:
    for j in i:
      hxy += -j / allNum * math.log2(j / allNum) if j != 0 else 0

  hx = 0
  for i in bigram:
    px = sum(i) / allNum
    hx += -px * math.log2(px) if px != 0 else 0

  return size, hx, hxy - hx, hxy

if __name__ == '__main__':
  with open('task/4.json', 'r') as file:
    parseData = json.load(file)

  cutList = [p for p in '<>/:;,.[\"\'\\\n\r“”?!@#$%^&*()']

  data = [[token['word'].lower() for token in s['tokens'] if token['word'] not in cutList] for s in parseData['sentences']]

  size0, hx0, hylx0, hxy0 = calEntropy(data)

  newData = []
  for s in parseData['sentences']:
    for dep in s['basicDependencies']:
      if dep['dep'] == 'ROOT':
        pick = [dep['governor'], dep['dependent']]
        break

    newData.append([w[0] for w in sorted([(dep['dependentGloss'].lower(), dep['dependent'])
                                       for dep in s['basicDependencies']
                                       if dep['governor'] in pick and
                                       dep['dependentGloss'] not in cutList], key = lambda w: w[1])])

  size1, hx1, hylx1, hxy1 = calEntropy(newData)

  with open('ans/Answer4.txt', 'w') as file:
    for line in newData:
      file.write(' '.join(line) + '\n')
    file.write('%d, %.4f, %.4f, %.4f\n' % (size1, hx1, hylx1, hxy1))

    file.write('%d, %.4f, %.4f, %.4f\n' % (size0, hx0, hylx0, hxy0))
