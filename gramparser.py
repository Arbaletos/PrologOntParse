from morph import read_ng, multiparse, check_tag, is_pos
from nltk.tokenize import word_tokenize

import re

class DeepGramParser:

    def __init__(self, templates):
        self.rules = {}
        for t in templates:
            if '::-' not in t:
                print('Incorrect rule format, {}!'.format(t))
                continue
            key, tokens = self.split_rule(t)
            self.rules[key] = self.rules.get(key, []) + [tokens]      

    def parse(self, line, symbol='$EXPRESSION'):
        ret = []
        rules = self.get_rules(line, symbol)
        for rule in rules:
            ret = []
            #print(line, rule)
            terms = self.parse_rule(line, rule)
            for t, text in terms:
                rec = self.parse(text, symbol=t)
                if rec:
                    ret += rec
                if len(rec) == 0 and t in self.rules:
                    ret = []
                    break
                if self.is_valid([(t, text)]):
                    ret += [(t, text)]
                else:
                    ret = []
                    break
            if ret:
                return ret
        return ret

    def is_valid(self, parse):
        for t, text in parse:
            if is_pos(t.split('_')[0][1:]):
                if len(word_tokenize(text))>1:
                    return False
                tag = t[1:].split('_')
                if check_tag(text, tag) is False:
                    return False
        return True

    def get_rules(self, line, symbol):
        ret = []
        if symbol not in self.rules:
            return []

        for rule in self.rules[symbol]:
            if all([t.startswith('$') or t in line for t in rule]):
                ret.append(rule)
        return ret

    def parse_rule(self, line, rule):
        ret = []
        tokens = rule
        for i, t in enumerate(tokens):
            #print('token: "{}", line: "{}"'.format(t, line))
            if t == '$*':
                continue
            elif t.startswith('$'):
                if i+1 < len(tokens):
                    next_token = tokens[i+1]
                    if next_token not in line:  # Something gone wrong
                        #print('shit')
                        return []
                    cur, line = line.split(next_token, maxsplit=1)
                    line = next_token+line
                    ret.append([t, cur])
                else:
                    ret.append([t, line])
            else:
                if line.count(t) > 0:
                    line = line.split(t, maxsplit=1)[1]
        return ret

    def split_rule(self, line):
        exp, line = line.split('::-')
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
        return exp, tokens


class GramParser:

    def __init__(self, templates):
        self.rules = [self.split_rule(t) for t in templates]

    def parse(self, line):
        terms = []
        rules = self.get_rules(line)
        if rules:
            rule = sorted(rules, key=lambda x: len(x))[-1]
            terms += self.parse_rule(line, rule)
        return terms

    def get_rules(self, line):
        ret = []
        for rule in self.rules:
            if all([t.startswith('$') or t in line for t in rule]):
                ret.append(rule)
        return ret

    def parse_rule(self, line, rule):
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
