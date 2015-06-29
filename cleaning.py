import enchant

fp = open('Hotels', 'r')
hotels = fp.read().split('\n')
fp.close()


d = enchant.Dict('en_US')
for hotel in hotels:
    if hotel == '':
        continue
    try:
        data = open('datasets/' + hotel.split('\n')[0], "r")
        fp = open('datasetClean/' + hotel.split('\n')[0], "w")
        data = data.read()
        for para in data.split('\n\n\n'):
            if para == '':
                continue
            prev = ''
            for word in para.split():
                if word == prev:
                    continue
                i = 0
                wd = ''
                prevch = ''
                for ch in word:
                    if ch != "\'" and (ch == '.' or ch == ',' or ch == '!' or
                                       ch == '?' or ch == '/' or
                                       ch == '(' or ch == ')'):
                        if ch == '/':
                            ch = ','
                        if prevch == ch:
                            continue
                        if wd == prev or wd == '':
                            fp.write(' ' + ch + ' ')
                            wd = ''
                        else:
                            fp.write(wd + ' ' + ch + ' ')
                            prev = wd
                            wd = ''
                    else:
                        wd = wd + ch
                    prevch = ch
                if wd != '':
                    if wd == prev:
                        continue
                    if d.check(wd):
                        fp.write(wd + ' ')
                        prev = wd

            fp.write('\n\n')
    except:
        continue
