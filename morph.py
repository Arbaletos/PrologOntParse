import pymorphy2

def inflect(word, g):
    words = word.split(' ')
    return ' '.join([morph.parse(w)[0].inflect(g).word for w in words])

def multi_inflect(words, g):
    if len(words) == 1:
        return inflect(words[0], g)
    inflected_words = [inflect(w, g) for w in words]
    return ', '.join(inflected_words[:-1])+' и '+inflected_words[-1]

def parse(w):
    return morph.parse(w)

morph = pymorphy2.MorphAnalyzer()