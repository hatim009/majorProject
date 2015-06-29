top_ten_features = ['staff', 'rooms', 'service', 'food',
                    'breakfast', 'locale', 'pool', 'buffet', 'price', 'lounge']

fp = open('Hotels', 'r')
hotels = fp.read().split('\n')
hotels.remove(hotels[-1])
fp.close()

print 'Enter 1 to select a feature otherwise 0'

selected_features = {}

i = 1
for feature in top_ten_features:
    check = raw_input('%d. %s : ' % (i, feature))
    selected_features[feature] = check
    i = i + 1
# endfor

scores = []

for i in range(len(hotels)):
    fp = open('FinalScores/' + hotels[i].split('\n')[0], 'r')
    score_list = fp.read().split('\n')
    fp.close()
    if len(score_list) > 10:
        score_list.remove(score_list[-1])
    score_sum = 0
    for token in score_list:
        feature = token.split(' ')[0]
        score = token.split(' ')[1]
        if selected_features[feature] == '1':
            score_sum = score_sum + float(score)
    # endfor
    scores.append([hotels[i].split('\n')[0], score_sum])
# endfor

for i in range(len(hotels)):
    for j in range(i + 1, len(hotels)):
        if scores[i][1] < scores[j][1]:
            temp = scores[i][1]
            scores[i][1] = scores[j][1]
            scores[j][1] = temp
        # endif
    # endfor
# endfor

for i in range(len(hotels)):
    print scores[i][0] + ' ' + str(scores[i][1])
