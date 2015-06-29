def get_score_mapping():
    files = []
    files.append('score_files/adj_dictionary1.11.txt')
    files.append('score_files/adv_dictionary1.11.txt')
    files.append('score_files/int_dictionary1.11.txt')
    files.append('score_files/noun_dictionary1.11.txt')
    files.append('score_files/verb_dictionary1.11.txt')
    scores = []
    for File in files:
        fp = open(File, 'r')
        text = fp.read().split('\n')
        for score in text:
            if len(score.split('\t')) == 2:
                scores.append(score.split('\t'))
        fp.close()
        # endfor
    # endfor
    scores = scores[:-1]
    score_map = dict(scores)
    return score_map

# enddef


fp = open('Hotels', 'r')
hotels = fp.read().split('\n')
fp.close()


score_map = get_score_mapping()

for hotel in hotels:
    if hotel == '':
        continue
    fp = open('Features Sorted/' + hotel.split('\n')[0], 'r')
    tokens = fp.read().split('\n')
    fp.close()
    if len(tokens[-1]) < 2:
        tokens = tokens[:-1]
    pos = open('Classification/positive/' + hotel.split('\n')[0], 'w')
    neg = open('Classification/negative/' + hotel.split('\n')[0], 'w')
    for token in tokens:
        feature = token.split(' ')[0]
        opinion = token.split(' ')[1]
        score = float(score_map.get(opinion, 0))
        modifier = ''
        if len(token.split(' ')) == 3:
            modifier = token.split(' ')[2]
        if modifier != '':
            if len(modifier.rsplit('-', 1)) == 2:
                if score > 0:
                    score = score - 4
                else:
                    score = score + 4
            else:
                score *= (1 + float(score_map.get(modifier, 0)) / 5)
        if score >= 0:
            pos.write(
                feature + ' ' + opinion + ' ' + modifier + ' ' + str(score) +
                '\n')
        else:
            neg.write(
                feature + ' ' + opinion + ' ' + modifier + ' ' + str(score) +
                '\n')
        # endif
    # endfor

    pos.close()
    neg.close()

# endfor
