from __future__ import print_function
import re
import spacy

from pyclausie import ClausIE
re_spaces = re.compile(r'\s+')

def preprocess_question(question):
    # remove articles: a, an, the

    q_words = question.split(' ')

    # when won't this work?
    for article in ('a', 'an', 'the'):
        try:
            q_words.remove(article)
        except:
            pass

    return re.sub(re_spaces, ' ', ' '.join(q_words))


nlp = spacy.load('en')
sen = 'when is Mary going to France?'
# Who is [going to | flying to | traveling to | visiting] < place >
doc = nlp(unicode(sen))
cl = ClausIE.get_instance()
tri = cl.extract_triples([preprocess_question(sen)])
for entity in doc.ents:
    print (entity.text, entity.label_)
#    if entity.label_=='GPE':
 #       print(entity.text, entity.label_)

sent = 'Sally is going to Mexico some time in 2020.'
cl = ClausIE.get_instance()
triples = cl.extract_triples([sent])[0]
sentence = triples.subject + ' ' + triples.predicate + ' ' + triples.object
doc_new = nlp (unicode(sentence))


