import sys


if __name__=='__main__':
    if len(sys.argv)<=3:
        print('USAGE: python compile_ont.py ontology_file knowledge_base_file output_file')
        quit()
    ont = [l.strip() for l in open(sys.argv[1], 'r', encoding='utf-8').read().split('\n') if len(l.strip())]
    kb = [l.strip() for l in open(sys.argv[2], 'r', encoding='utf-8').read().split('\n') if len(l.strip())]

    with open(sys.argv[3], 'w', encoding='utf-8') as writer:
        used = set()
        for o in ont:
            pred = o.split('(')[0]
            for l in kb:
                if l.startswith(pred+'('):
                    writer.write(l + '\n')
                    used.add(l)
            writer.write(o + '\n\n')

        if len(used) < len(kb):
            kb = [k for k in kb if k not in used]
            ind = kb[0].split('(')[0]
        for k in kb:
            writer.write(k + '\n')
            i = k.split('(')[0]
            if i != ind:
                writer.write('\n')
                ind = i