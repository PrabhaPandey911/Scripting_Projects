sed -n 's/\(.*\),\(.*\),\(.*\),\(.*\),\(\(0[1-9]\|[12][0-9]\|3[01]\)\/\(0[1-9]\|1[012]\)\/\(198[0-9]\)\),\(.*\)/\1/p' address-book.csv | wc -l
#sed -n 's/\(.*\),\(.*\),\(.*\),\(.*\),\(..\/..\/198[0-9]\),\(.*\)/\1/p' address-book.csv