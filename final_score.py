top_ten_features = ['staff', 'rooms', 'service', 'food',
                    'breakfast', 'locale', 'pool', 'buffet', 'price', 'lounge']


def get_score(hotel):

    fp1 = open('Classification/positive/' + hotel.split('\n')[0], 'r')
    fp2 = open('Classification/negative/' + hotel.split('\n')[0], 'r')

    tuples1 = fp1.read().split('\n')
    if len(tuples1[-1]) < 2:
        tuples1.remove(tuples1[-1])
    fp1.close()

    tuples2 = fp2.read().split('\n')
    if len(tuples2[-1]) < 2:
        tuples2.remove(tuples2[-1])
    fp2.close()

    for i in range(len(tuples1)):
        tuples1[i] = tuples1[i].split(' ')

    for i in range(len(tuples2)):
        tuples2[i] = tuples2[i].split(' ')

    fp = open('FinalScores/' + hotel.split('\n')[0], 'w')

    for feature in top_ten_features:
        score = 0.0

        for token in tuples1:
            if token[0] == feature:
                score += float(token[-1])
        # endfor

        for token in tuples2:
            if token[0] == feature:
                score += float(token[-1])
        # endfor

        fp.write(feature + ' ' + str(score) + '\n')
    # endfor
    fp.close()

# enddef


fp = open('Hotels', 'r')
hotels = fp.read().split('\n')
fp.close()

for hotel in hotels:
    if hotel == '':
        continue
    get_score(hotel)

# endfor
