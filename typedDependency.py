import subprocess
import os


def getTypedDependencies(sentence):
    fp = open('temp', 'w')
    fp.write(sentence)
    fp.close()
    cmd = 'java -Xmx12g -cp stanford-parser.jar \
    edu.stanford.nlp.parser.lexparser.LexicalizedParser \
    -outputFormat "typedDependencies" englishPCFG.ser.gz temp'
    typedDependencies = subprocess.check_output(cmd, shell=True)
    os.remove('temp')
    return typedDependencies
# enddef

fp = open('Hotels', 'r')
hotels = fp.read().split('\n')
fp.close()


for hotel in hotels:
    if hotel == '':
        continue
    data = open('datasetClean/' + hotel.split('\n')[0], 'r')
    data = data.read().split('\n\n')
    dep = open('Dependencies/' + hotel.split('\n')[0], 'w')
    for sentence in data:
        if sentence == '':
            continue
        typedDependencies = getTypedDependencies(sentence)
        dep.write(typedDependencies + '\n\n')
        # endfor
    # endfor
    dep.close()
# endfor
