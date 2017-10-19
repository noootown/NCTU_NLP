sed 's:\ \+\+\+\$\+\+\+\ :qwertyuiop:g' movie_lines-utf8.txt | awk 'BEGIN{FS="qwertyuiop"; OFS=","}{a[$3]=a[$3]?a[$3]" "$5:$5;}END{for (i in a)print i, a[i];}' > movie.txt
sed 's:\ \+\+\+\$\+\+\+\ :qwertyuiop:g' movie_lines-utf8.txt | awk 'BEGIN{FS="qwertyuiop"; OFS=","}{a[$2]=a[$2]?a[$2]" "$5:$5;}END{for (i in a)print i, a[i];}' > char.txt
