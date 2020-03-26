import sys, pymorphy2

def inflect(word, g):
    words = word.split(' ')
    return ' '.join([morph.parse(w)[0].inflect(g).word for w in words])

def multi_inflect(words, g):
    if len(words) == 1:
        return inflect(words[0], g)
    inflected_words = [inflect(w, g) for w in words]
    return ', '.join(inflected_words[:-1])+' и '+inflected_words[-1]
    
def read_ng(words):
    ng = []
    case = 'nomn'
    for i, w in enumerate(words):
        if len(w)==0 or not (w[0].isalpha()):
            i-=1
            break
        if 'LATN' in morph.parse(w)[0].tag:
            ng += [w]
            continue
        pos = morph.parse(w)[0].tag.POS
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
    
def read_brackets(words):
    ret = []
    line = ' '.join(words).replace(') ', ')')
    ret = line[line.index('(')+1: line.index(')')].split(' ')
    res = line[line.index(')')+2:]
    return ret, res
    
def parse(line):
    ret = []
    words = line.replace('.', '').split(' ')
    if words[0] in ['Пример', 'Примеры']:
        root, res = read_ng(words[1:])
        ret.append(('term', [root]))
        args = multiparse(res[1:])
        for a in args:
            ret.append(('ekz', [root, a]))
        return ret
    ng, res = read_ng(words)
    ret.append(('term', [ng]))
    if len(res) and res[0].startswith('('):
        syns, res = read_brackets(res)
        for s in multiparse(syns): 
            ret.append(('syn', [ng, s]))
    if '-- это вид ' in line:
        arg = read_ng(res[3:])[0]
        ret.append(('hyp', [arg, ng]))
    elif 'подразделяются на ' in line:
        args = multiparse(res[2:])
        for a in args:
            ret.append(('hyp', [ng, a]))
    elif 'состоит из' in line:
        args = multiparse(res[2:])
        for a in args:
            ret.append(('part', [ng, a]))
    elif 'входит в состав ' in line:
        arg = read_ng(res[3:])[0]
        ret.append(('part', [arg, ng]))
    elif len(res) and len(res[0]):
        ret.append(('attr', [ng, ' '.join(res)]))
    return ret
    
def kb_to_prolog(kb):
    ret = []
    for a, args in sorted(kb, key=lambda x:x[0]):
        ret.append("{}('{}').".format(a, "','".join(args))) 
    return ret
   
if __name__=='__main__':

    if len(sys.argv)<=2:
        print('USAGE: python ont_parse.py input_file output_file')
        quit()
    
    morph = pymorphy2.MorphAnalyzer()
    inputo = sys.argv[1]
    kb_gen = []
    lines = []
    for l in open(inputo, 'r', encoding='utf-8'):
        lines += l.strip().split('. ')
    for line in lines:
        for l in parse(line):
            if l not in kb_gen:
                kb_gen.append(l)
    with open(sys.argv[2], 'w', encoding='utf-8') as writer:
        for l in kb_to_prolog(kb_gen):
            writer.write(l + '\n')
            
    