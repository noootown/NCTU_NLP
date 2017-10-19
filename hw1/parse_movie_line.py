
if __name__ == '__main__':
  with open('movie_lines-utf8.txt', 'r') as file1, open('movie_lines-input.txt', 'w') as file2:
    for d in [line.strip().split(' +++$+++ ')[-1] for line in file1]:
      file2.writelines('%s\n' % d)
