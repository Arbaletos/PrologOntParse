import sys

from gramparser import GramParser
from gramparser import DeepGramParser

 
def kb_to_prolog(kb):
    ret = []
    for a, args in sorted(kb, key=lambda x:x[0]):
        ret.append("{}('{}').".format(a, "','".join(args))) 
    return ret


if __name__=='__main__':
    if len(sys.argv)<=2:
        print('USAGE: python gram_parse.py [-r] templates_file input_file [output_file]')
        print('-r for recursive mode (DeepGramParser), needs grammar file')
        print('not key for default mode (GramParser), needs template file')
        quit()
  
    deep = False
    if '-r' in sys.argv:
        deep = True
        del sys.argv[sys.argv.index('-r')]
    inputo = sys.argv[2]
    lines = []

    templates = [l.strip() for l in open(sys.argv[1])]
    
    if deep:
        parser = DeepGramParser(templates)
    else:
        parser = GramParser(templates)
 
    terms = []        
    for l in open(inputo, 'r', encoding='utf-8'):
        lines += l.strip().split('. ')
    for line in lines:
        #print('line: ', line)
        terms += parser.parse(line)
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
    
           
