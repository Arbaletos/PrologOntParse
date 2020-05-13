import sys

from morph import read_ng, multiparse
from nltk.tokenize import word_tokenize

import re

class GramParser:
    def __init__(self, templates):
        self.templates = templates

    def parse_line(self, line):
        terms = []
        rules = self.get_rules(line)
        if rules:
            rule = sorted(rules, key=lambda x: len(x))[-1]
            terms += self.parse(line, rule)
        return terms

    
    def get_rules(self, line):
        ret = []
        for t in self.templates:
            tokens = self.split_rule(t)
            if all([t.startswith('$') or t in line for t in  tokens]):
                ret.append(t)
        return ret

    def parse(self, line, rule):
        ret = []
        tokens = self.split_rule(rule)
        for i, t in enumerate(tokens):
            if t == '$*':
                continue
            elif t.startswith('$'):
                cur_text = line
                if i+1 < len(tokens):
                    try:
                        cur_text = line[:line.index(tokens[i+1])].strip()
                        line = line[line.index(tokens[i+1]):]
                    except:
                        pass
                try:
                    ng, res = read_ng(word_tokenize(cur_text))
                    ret.append([t, ng, cur_text])
                    #print(t, 'norm:', ng, 'form:', cur_text)
                except Exception as e:
                    #print(e, cur_text)
                    ret.append([e, cur_text])
            else:
                if line.find(t) >= 0:
                    line = line[line.index(t)+len(t):]
        return ret

    def split_rule(self, line):
        tokens = []
        i = 0
        while i < len(line):
            if '$' in line:
                if not line.startswith('$'):
                    tokens.append(line[:line.index('$')])
                line = line[line.index('$')+1:]
                if line.startswith('*'):
                    tokens.append('$*')
                    line = line[1:]
                    continue
                span = re.search('\W', line)
                if span:
                    tokens.append('$' + line[:line.index(span[0])])
                    line = line[line.index(span[0]):]
                else:
                    tokens.append('$'+line)
                    break
            else:
                tokens += [line]
                break
        return tokens
   


 
def kb_to_prolog(kb):
    ret = []
    for a, args in sorted(kb, key=lambda x:x[0]):
        ret.append("{}('{}').".format(a, "','".join(args))) 
    return ret


if __name__=='__main__':
    if len(sys.argv)<=2:
        print('USAGE: python gram_parse.py templates_file input_file [output_file]')
        quit()
  
    inputo = sys.argv[2]
    lines = []

    templates = [l.strip() for l in open(sys.argv[1])]

    parser = GramParser(templates)

    terms = []        
    for l in open(inputo, 'r', encoding='utf-8'):
        lines += l.strip().split('. ')
    for line in lines:
        #print('line: ', line)
        terms += parser.parse_line(line)
    out_file = None
    if len(sys.argv)>3:
        out_file = open(sys.argv[3], 'w', encoding='utf-8')
        out_file.write('relation\tnormalized\tsource\n')
    for t in terms:
        if len(t) == 3:
            print('{}, norm: {}, form: {}'.format(*t))
            if out_file:
                out_file.write('\t'.join(t)+'\n')
        else:
            print(*t)

    if out_file:
        out_file.close()
    
           
