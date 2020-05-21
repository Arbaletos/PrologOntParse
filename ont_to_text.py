import sys

from morph import inflect, multi_inflect
    
def explain(term, kb):
    out = ''
    filt = {}
    for p, a in kb:
        if a[0]==term:
            filt[p] = filt.get(p, [])+[a]
        elif term in a:
            filt['inv_'+p] = filt.get('inv_'+p, [])+[a]
    out += term
    if 'syn' in filt:
        out += ' ('+', '.join([s[1] for s in filt['syn']]) + '). '
    else:
        out += '. '
    if 'inv_hyp' in filt:
        out += '{} -- это вид {}. '.format(term, multi_inflect([s[0] for s in filt['inv_hyp']], {'gent'}))
    if 'hyp' in filt:
        if len(filt['hyp']) >= 1:
            out += '{} подразделяются на {}. '.format(inflect(term, {'plur'}).title(), multi_inflect([s[1] for s in filt['hyp']], {'accs', 'plur'}))
    if 'mer' in filt:
        out += '{} входит в состав {}. '.format(term, multi_inflect([s[1] for s in filt['mer']], {'gent'}))
    if 'inv_mer' in filt:
        if len(filt['inv_mer']) >= 1:
            out += '{} состоит из {}. '.format(term, multi_inflect([s[0] for s in filt['inv_mer']], {'gent', 'plur'}))
    if 'attr' in filt:
        for a in filt['attr']:
            out += '{} {}. '.format(term, a[1])
    if 'inst' in filt:
        if len(filt['inst']) > 1:
            out += 'Примеры {} -- {}. '.format(inflect(term, {'gent', 'plur'}), multi_inflect([s[1] for s in filt['inst']], set()))
        else:
            out += 'Пример {} -- {}. '.format(inflect(term, {'gent', 'sing'}), multi_inflect([s[1] for s in filt['inst']], set()))
    return out
        
   
if __name__=='__main__':
    if len(sys.argv)<=2:
        print('USAGE: python ont_to_text.py input_file.pr output_file')
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

    explained = {}
    with open(sys.argv[2], 'w', encoding='utf-8') as writer:

        for pred, attr in kb:
            if pred == 'term' and attr[0] not in explained:
                ex = explain(attr[0], kb)
                print(ex)
                writer.write(ex+'\n')
    