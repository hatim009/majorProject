import operator


def similarize_words():

    tokens = []

    fp = open('Hotels', 'r')
    hotels = fp.read().split('\n')
    fp.close()

    for hotel in hotels:
        if hotel == '':
            continue
        fp = open('Features/' + hotel.split('\n')[0], 'r')
        tuples = fp.read().split('\n')
        if len(tuples[-1]) < 2:
            tuples.remove(tuples[-1])
        fp.close()
        for i in range(len(tuples)):
            tuples[i] = tuples[i].split(' ')
        tokens.append(tuples)
    # endfor

    word = {}

    for i in range(len(tokens)):
        for j in range(len(tokens[i])):
            w1 = tokens[i][j][0]
            if word.get(w1, 0) == 1:
                continue
            word[w1] = 1
            for p in range(i, len(tokens)):
                for q in range(len(tokens[p])):
                    if p == i and q == 0:
                        q = j
                    l = 0
                    w2 = tokens[p][q][0]
                    while l < min(len(w1), len(w2)):
                        if w1[l] != w2[l]:
                            break
                        l = l + 1
                    # endwhile
                    if l > (min(len(w1), len(w2)) / 2):
                        tokens[p][q][0] = w1
                # endfor
            # endfor
        # endfor
    # endfor
    return tokens

# enddef


tokens = similarize_words()

fp = open('Hotels', 'r')
hotels = fp.read().split('\n')
fp.close()


it = 0

for hotel in hotels:
    if hotel == '':
        continue
    tuples = tokens[it]
    word_freq = {}

    for token in tuples:
        feature = token[0]
        word_freq[feature] = word_freq.get(feature, 0) + 1

    List = reversed(sorted(word_freq.items(), key=operator.itemgetter(1)))

    pt = 0
    for feature in List:
        for i in range(pt, len(tuples)):
            if feature[0] == tuples[i][0]:
                temp = tuples[i]
                tuples[i] = tuples[pt]
                tuples[pt] = temp
                pt = pt + 1
            # endif
        # endfor
    # endfor

    fp = open('Features Sorted/' + hotel.split('\n')[0], 'w')
    for token in tuples:
        feature = token[0]
        if feature == 'room':
            print 'YES'
        opinion = token[1]
        modifier = ''
        if len(token) == 3:
            modifier = token[2]
        fp.write(feature + ' ' + opinion + ' ' + modifier + '\n')
    # endfor
    fp.close()

    it = it + 1

# endfor
