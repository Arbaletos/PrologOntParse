from morph import read_ng, multiparse
from nltk.tokenize import word_tokenize

import re

class GramParser:

    def __init__(self, templates):
        self.rules = [self.split_rule(t) for t in templates]

    def parse_line(self, line):
        terms = []
        rules = self.get_rules(line)
        if rules:
            rule = sorted(rules, key=lambda x: len(x))[-1]
            terms += self.parse(line, rule)
        return terms

    def get_rules(self, line):
        ret = []
        for rule in self.rules:
            if all([t.startswith('$') or t in line for t in rule]):
                ret.append(rule)
        return ret

    def parse(self, line, rule):
        ret = []
        tokens = rule
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