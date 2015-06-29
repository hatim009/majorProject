import re
from sets import Set
from nltk.corpus import stopwords


def getTokens(typedDependency):
    td = typedDependency.split('\n')
    tokens = []
    for x in td:
        if x == '':
            continue
        # endif
        a, x = x.split('(')
        b, c = x.split(', ')
        b, bv = b.rsplit('-', 1)
        c, cv = c.rsplit('-', 1)
        cv = cv[:-1]
        if re.match("^[A-Za-z'-]*$", b) and re.match("^[A-Za-z'-]*$", b):
            tokens.append([a, b.lower(), bv, c.lower(), cv])
    # endfor
    return tokens
# enddef

features_set = Set()
opinions_set = Set()
modifier_set = Set()


def combine_compound_words(tokens):

    i = len(tokens) - 1
    while i >= 0:
        if tokens[i][0] == 'compound' and int(tokens[i][4]) == int(tokens[i][2]) - 1:
            for j in range(len(tokens)):
                if tokens[j][1:3] == tokens[i][1:3]:
                    tokens[j][1] = tokens[i][3] + '-' + tokens[i][1]
                if tokens[j][3:5] == tokens[i][1:3]:
                    tokens[j][3] = tokens[i][3] + '-' + tokens[i][1]
            # endfor
        # endif
        i = i - 1
    # endfor

    return tokens

# enddef

mods = []


def find_opinions(tokens, feature, feat, id):
    fg = 0
    for opinion in tokens:
        if opinion[0] == 'advmod' or opinion[0] == 'neg':
            if opinion[3].lower() in stopwords.words('english'):
                continue
            # endif
            if feature[1:3] == opinion[1:3]:
                fg = 1
                modifier_set.add(opinion[3])
                if id != -1:
                    mods[id].append(opinion[3])
                feat.write(
                    feature[3] + ' ' + feature[1] + ' ' +
                    opinion[3] + '\n')

            # endif
        # endif
        elif opinion[0] == 'dep':
            if opinion[3].lower() in stopwords.words('english'):
                continue
            # endif
            if feature[1:3] == opinion[1:3]:
                opinions_set.add(opinion[3])
                find_opinions(
                    tokens, ['nsubj', opinion[3], opinion[4], feature[3],
                             feature[4]], feat, -1)
        # endelif
    # endfor

    if fg == 0:
        feat.write(feature[3] + ' ' + feature[1] + '\n')
    # endif
# enddef


def add_tag_to_negation(tokens):
    for i in range(len(tokens)):
        if tokens[i][0] == 'neg':
            tokens[i][3] = tokens[i][3] + '-' + 'neg'
        # endif
    # endfor
    return tokens

# enddef


def valid_feature(tokens, feature):
    for token in tokens:
        if token[0] == 'amod' and feature[0] == 'nsubj' and feature[3:5] == token[3:5]:
            return False
        elif token[0] == 'nsubj' and feature[0] == 'amod' and feature[3:5] == token[1:3]:
            return False
    # endfor

    return True

# enddef


def find_features(tokens, feat):
    i = 0
    for feature in tokens:
        if feature[0] == 'nsubj':
            if feature[3].lower() in stopwords.words('english'):
                continue
            if feature[1].lower() in stopwords.words('english'):
                continue
            if not valid_feature(tokens, feature):
                continue
            # endif
            mods.append([])
            features_set.add(feature[3])
            opinions_set.add(feature[1])
            find_opinions(tokens, feature, feat, len(mods) - 1)
            if i != 0:
                if tokens[i - 1][0] == 'nsubj' and tokens[i - 1][3:5] == feature[3:5]:
                    for mod in mods[len(mods) - 2]:
                        if mod not in mods[len(mods) - 1]:
                            mods[len(mods) - 1].append(mod)
                            feat.write(
                                feature[3] + ' ' + feature[1] + ' ' + mod + '\n')

        # endif
        i = i + 1
    # endfor

# enddef


def find_amod(tokens, feat):

    for token in tokens:
        if token[0] == 'amod':
            if token[3].lower() in stopwords.words('english'):
                continue
            if token[1].lower() in stopwords.words('english'):
                continue
            if token[1] in opinions_set:
                continue
            if token[1] in modifier_set:
                continue
            if token[3] in features_set:
                continue
            if token[3] in modifier_set:
                continue
            if token[1] not in features_set:
                continue
            if not valid_feature(tokens, ['mod', token[3], token[4], token[1], token[2]]):
                continue
            features_set.add(token[1])
            opinions_set.add(token[3])
            fg = 0
            for mod in tokens:
                if mod[0] == 'dep' and mod[1:3] == token[1:3]:
                    if mod[3].lower in stopwords.words('english'):
                        continue
                    if mod[3] in features_set:
                        continue
                    if mod[3] in opinions_set:
                        continue
                    fg = 1
                    modifier_set.add(mod[3])
                    feat.write(token[1] + ' ' + token[3] + ' ' + mod[3] + '\n')
                # endif
                if (mod[0] == 'advmod' or mod[0] == 'neg') and mod[1:3] == token[1:3]:
                    if mod[3].lower() in stopwords.words('english'):
                        continue
                    if mod[3] in features_set:
                        continue
                    if mod[3] in opinions_set:
                        continue
                    fg = 1
                    modifier_set.add(mod[3])
                    feat.write(token[1] + ' ' + token[3] + ' ' + mod[3] + '\n')
                # endif
            # endfor
            if fg == 0:
                feat.write(token[1] + ' ' + token[3] + '\n')
        # endif
    # endfor
# enddef


fp = open('Hotels', 'r')
hotels = fp.read().split('\n')
fp.close()


mode = 'w'

for i in range(2):
    if i == 1:
        mode = 'a'
    for hotel in hotels:
        if hotel == '':
            continue
        dep = open('Dependencies/' + hotel.split('\n')[0], 'r')
        dependencies = dep.read().split('\n\n\n\n')
        feat = open('Features/' + hotel.split('\n')[0], mode)
        for typedDependencies in dependencies:
            for typedDependency in typedDependencies.split('\n\n'):
                tokens = getTokens(typedDependency)
                tokens = add_tag_to_negation(tokens)
                if i == 0:
                    find_features(tokens, feat)
                else:
                    find_amod(tokens, feat)
            # endfor
        # endfor
        dep.close()
        feat.close()
    # endfor
# endfor
