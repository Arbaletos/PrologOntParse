import sys

from morph import inflect, multi_inflect, parse
from nltk.tokenize import word_tokenize

import re


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
    

def read_brackets(words):
    ret = []
    line = ' '.join(words).replace(') ', ')')
    ret = line[line.index('(')+1: line.index(')')].split(' ')
    res = line[line.index(')')+2:]
    return ret, res
    
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
              print(t, 'norm:', ng, 'form:', cur_text)
          except Exception as e:
              print(e, cur_text)

        else:
          if line.find(t) >= 0:
              line = line[line.index(t)+len(t):]
 
 
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
        print('USAGE: python gram_parse.py template_file input_file')
        quit()
  
    inputo = sys.argv[2]
    lines = []

    templates = [l.strip() for l in open(sys.argv[1])]
    #for t in templates:
    #    print(split_rule(t))
        
    for l in open(inputo, 'r', encoding='utf-8'):
        lines += l.strip().split('. ')
    for line in lines:
        #print('line: ', line)
        rules = get_rules(line, templates)
        if rules:
          rule = sorted(rules, key=lambda x: len(x))[-1]
          parse_line(line, rule)
           