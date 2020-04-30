import sys

from morph import read_ng, multiparse
from nltk.tokenize import word_tokenize

import re

    
def get_rules(line, templates):
    ret = []
    for t in templates:
        t_re = re.sub('\$[\w\*]+', '[\W\w]*', t)
        for c in '.?()':
            t_re = t_re.replace(c, '\\' + c) 
        if re.search(t_re, line):
            ret.append(t)
    return ret

def parse_line(line, rule):
    ret = []
    tokens = split_rule(rule)
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
 
 
def kb_to_prolog(kb):
    ret = []
    for a, args in sorted(kb, key=lambda x:x[0]):
        ret.append("{}('{}').".format(a, "','".join(args))) 
    return ret


def split_rule(line):
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
   

if __name__=='__main__':
    if len(sys.argv)<=2:
        print('USAGE: python gram_parse.py templates_file input_file [output_file]')
        quit()
  
    inputo = sys.argv[2]
    lines = []

    templates = [l.strip() for l in open(sys.argv[1])]
    #for t in templates:
    #    print(split_rule(t))


    terms = []        
    for l in open(inputo, 'r', encoding='utf-8'):
        lines += l.strip().split('. ')
    for line in lines:
        #print('line: ', line)
        rules = get_rules(line, templates)
        if rules:
          rule = sorted(rules, key=lambda x: len(x))[-1]
          terms += parse_line(line, rule)
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
    
           