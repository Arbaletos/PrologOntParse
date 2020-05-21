import sys

from morph import inflect, multi_inflect

def get_rel(kb, rel, arg1=None, arg2=None):
    ret = []
    for r, args in kb:
        if r!=rel:
            continue
        if arg1 is not None and arg1 != args[0]:
            continue
        if len(args)>1 and arg2 is not None and arg2 != args[1]:
            continue
        ret.append((r, args))
    return ret


if __name__=='__main__':
    if len(sys.argv)<=1:
        print('USAGE: python demandanto.py kb.pr')
        quit()

    inputo = sys.argv[1]

    kb = []
    with open(inputo, 'r', encoding='utf-8') as reader:
        for line in reader:
            line = line.strip()
            if len(line)==0 or ':-' in line:
                continue
            pred = line[:line.index('(')]
            args = line[len(pred)+1:-2].replace("'", '').split(',')
            kb.append((pred, args))
    print(kb)
