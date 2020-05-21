import sys

from morph import inflect, multi_inflect, concatenate


class Demandanto:
  
    def __init__(self, kb_path):
        self.kb = []
        with open(inputo, 'r', encoding='utf-8') as reader:
            for line in reader:
                line = line.strip()
                if len(line)==0 or ':-' in line:
                    continue
                pred = line[:line.index('(')]
                args = line[len(pred)+1:-2].replace("'", '').split(',')
                self.kb.append((pred, args))


    def get_rel(self, rel, arg1=None, arg2=None):
        ret = []
        for r, args in self.kb:
            if r!=rel:
                continue
            if arg1 is not None and arg1 != args[0]:
                continue
            if len(args)>1 and arg2 is not None and arg2 != args[1]:
                continue
            cur = []
            if arg1 is None:
                cur.append(args[0])
            if len(args)>1 and arg2 is None:
                cur.append(args[1])
            if cur:
                ret.append(cur)
        return ret

    def ask(self, term):
        questions = []
        hol = [a[0] for a in self.get_rel('mer', term, None)]
        mer = [a[0] for a in self.get_rel('mer', None, term)]
        hyp = [a[0] for a in self.get_rel('hyp', term, None)]
        hyper = [a[0] for a in self.get_rel('hyp', None, term)]
        inst = [a[0] for a in self.get_rel('inst', term, None)]
        attr = [a[0] for a in self.get_rel('attr', term, None)]
        if len(attr) and len(hyper):
            q = 'Что такое {}?'.format(term.lower())
            a = 'Это {}, что {}.'.format(hyper[0].lower(), concatenate(attr))
            questions.append((q, a))
        if len(hyp):
            q = 'Какие есть виды {}?'.format(inflect(term, {'gent', 'plur'}))
            a = '{}'.format(multi_inflect(hyp, set()))
            questions.append((q, a))
        if len(inst):
            q = 'Какие существуют примеры {}?'.format(inflect(term, {'gent', 'plur'}))
            a = '{}'.format(concatenate(inst))
            questions.append((q, a))
        if len(mer):
            q = 'Что является частями {}?'.format(inflect(term, {'gent', 'sing'}))
            a = '{}'.format(concatenate(mer))
            questions.append((q, a))
        if len(hol):
            q = 'Частью чего является {}?'.format(term)
            a = '{}'.format(multi_inflect(hol, {'gent'}))
            questions.append((q, a))

        return questions


if __name__=='__main__':
    if len(sys.argv)<=1:
        print('USAGE: python demandanto.py kb.pr')
        quit()

    inputo = sys.argv[1]

    demandanto = Demandanto(inputo)
    
    for term in demandanto.get_rel('term'):
        q = demandanto.ask(term[0])
        if q:
            print(q)
