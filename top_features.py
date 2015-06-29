import operator

fp = open('Hotels', 'r')
hotels = fp.read().split('\n')
fp.close()

word_freq = {}

for hotel in hotels:
    if hotel == '':
        continue
    # endif
    fp = open('Features Sorted/' + hotel.split('\n')[0], 'r')
    tuples = fp.read().split('\n')
    tuples = tuples[:-1]
    fp.close()

    for token in tuples:
        feature = token.split(' ')[0]
        word_freq[feature] = word_freq.get(feature, 0) + 1
    # endfor

# endfor

List = reversed(sorted(word_freq.items(), key=operator.itemgetter(1)))

fp = open('top_features_list.txt', 'w')

for feature in List:
    fp.write(feature[0] + '\n')
# endfor

fp.close()
