from nltk.tokenize import word_tokenize
from nltk import sent_tokenize
import collections
import re
import sys

if __name__=='__main__':
    if len(sys.argv)<=1:
        print('USAGE: python input_text.txt')
        quit()
  
    inputo = sys.argv[1]
    text = open(inputo, 'r', encoding='utf-8').read()

    sentences = sent_tokenize(text)
    
    opr = []
    for w in ['–','называется','называют', 'выполняет', 'это']:
        opr += [sent for sent in sentences if w in sent]
    
    reg=['\w+\s+\w+\s[–]',
         '\w+\s+\w+\s+\w+\s+\называется',
         '\называют+\s+\w+\s+\w+',
         '\называют+\s+\w+ ',
         '\w+\s+\w+[–]+ \это',
         '\w+\W\s\w+\s\w+\s\w+\s\w+\s+\w+\W\s+[–]+ \это',
         '\w+\s+\w+\s+\выполняет',
         '\w+\s+\w+\s+\ставит',
         '\w+\s+\w+\s+\(+\w\w+\w+тся',
         '\w+\s+\означает',
         '\w+\s+\w+\s+\(+.+\)+[–]',
         '\w+\s+\w+\s+\w+\s+\(+.+\)+[–]',
         '\w+\s+\w+\s+\решает',
         '\противопоставляют+\s+\w+\s+\w+']

    term=[]

    for r in reg:
        for s in sentences:
            term += re.findall(r, s)
    
    tokens = [word_tokenize(t) for t in term]
    del_words=['решает', 'осуществляется', '(', ')', '–', 'называется', 'называют', 'это', 'ставит', 'выполняет', 'означает','противопоставляют','а']
    for i, token in enumerate(tokens):
        tokens[i] = ' '.join([t for t in token if t not in del_words])
    print(tokens)
    

