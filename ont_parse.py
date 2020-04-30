import sys

from morph import read_ng, multiparse, read_brackets

    
def parse_line(line):
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
    if len(sys.argv)<=1:
        print('USAGE: python ont_parse.py input_file output_file')
        quit()
  
    inputo = sys.argv[1]
    kb_gen = []
    lines = []
    for l in open(inputo, 'r', encoding='utf-8'):
        lines += l.strip().split('. ')
    for line in lines:
        for l in parse_line(line):
            if l not in kb_gen:
                kb_gen.append(l)
    with open(sys.argv[2], 'w', encoding='utf-8') as writer:
        for l in kb_to_prolog(kb_gen)[::-1]:
            writer.write(l + '\n')
            
    