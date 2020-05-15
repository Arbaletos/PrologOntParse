import pymorphy2

def inflect(word, g):
    words = word.split(' ')
    return ' '.join([morph.parse(w)[0].inflect(g).word for w in words])

def multi_inflect(words, g):
    if len(words) == 1:
        return inflect(words[0], g)
    inflected_words = [inflect(w, g) for w in words]
    return ', '.join(inflected_words[:-1])+' и '+inflected_words[-1]

def parse(w):
    return morph.parse(w)

def read_ng(words):
    ng = []
    case = 'nomn'
    for i, w in enumerate(words):
        if len(w)==0 or not (w[0].isalpha()):
            i-=1
            break
        if 'LATN' in parse(w)[0].tag:
            ng += [w]
            continue
        pos = parse(w)[0].tag.POS
        if pos in ['NOUN', 'ADJF', 'PRTF', "PREP"]:
            if pos=='PRTF':
                case = 'nomn'
            ng += [inflect(w, set([case, 'sing']))]
            if pos=='NOUN':
                case = 'gent'
            if pos=='PRTF':
                case = 'ablt'
        else:
            i-=1
            break
    return ' '.join(ng), words[i+1:]
 
   
def multiparse(words):
    words = ' '.join(words).replace(' и ', ', ').split(', ')
    return [read_ng(w.split(' '))[0] for w in words]


def check_tag(word, tags):
    for tag in morph.tag(word):
        if all([t in tag for t in tags]):
            return True
    return False
    

def read_brackets(words):
    ret = []
    line = ' '.join(words).replace(') ', ')')
    ret = line[line.index('(')+1: line.index(')')].split(' ')
    res = line[line.index(')')+2:]
    return ret, res

def is_pos(word):
    return word in ['NOUN', 'VERB', 'ADJF']  #  Yup, wee need to extract full list of pos from morph.

morph = pymorphy2.MorphAnalyzer()