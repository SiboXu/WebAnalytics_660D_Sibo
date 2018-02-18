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


def has_travel_word(string):

    traveldic = ['traveling to', 'flying to', 'driving to', 'going to', 'visiting']
    for tword in traveldic:
        if tword in string:
            str = string
            str = str.replace(tword, 'traveling to')

    return str



traveldic = ['travel', 'fly', 'drive', 'go', 'visit']
nlp = spacy.load('en')
sen = 'Who is going to France?'
# Who is [going to | flying to | traveling to | visiting] < place >
doc = nlp(unicode(sen))
cl = ClausIE.get_instance()
tri = cl.extract_triples([preprocess_question(sen)])
for entity in doc.ents:
    print (entity.text, entity.label_)

for t in tri:
    print (str(t.lemma_.text) for t in doc if str(t.lemma) in traveldic)
#    if entity.label_=='GPE':
 #       print(entity.text, entity.label_)

sent = 'Don\'t let Chris forget to take his medicine tomorrow.'
cl = ClausIE.get_instance()
triples = cl.extract_triples([sent])[0]
sentence = triples.subject + ' ' + triples.predicate + ' ' + triples.object
doc_new = nlp (unicode(sentence))
for entity in doc_new.ents:
    print (entity.text, entity.label_)

print (has_travel_word(sen))