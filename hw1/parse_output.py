import json
import _pickle as cp

def removekey(d, key):
  r = dict(d)
  del r[key]
  return r

if __name__ == '__main__':
  filename = 'm'

  with open('parse/%s.txt' % filename, 'r') as file1, \
    open('parse/%s.txt.json' % filename, 'r') as file2:
    movieLine = [line.strip() for line in file1]
    output = json.load(file2)
  
  # reformat input json

  formatData = [{
                  'parse': sentence['parse'],
                  'basicDependencies': sentence['basicDependencies'],
                  'enhancedDependencies': sentence['enhancedDependencies'],
                  'enhancedPlusPlusDependencies': sentence['enhancedPlusPlusDependencies'],
                  'tokens': [removekey(word, 'index') for word in sentence['tokens']],
                } for sentence in output['sentences']]

  with open('parse/%s-format.pkl' % filename, 'wb') as file:
    cp.dump(formatData, file)

  print('Finish formating %s-format.pkl' % filename)
