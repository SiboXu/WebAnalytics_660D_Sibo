from __future__ import print_function
import re
import spacy

from pyclausie import ClausIE


nlp = spacy.load('en')
re_spaces = re.compile(r'\s+')


class Person(object):
    def __init__(self, name, likes=None, has=None, travels=None):
        """
        :param name: the person's name
        :type name: basestring
        :param likes: (Optional) an initial list of likes
        :type likes: list
        :param dislikes: (Optional) an initial list of likes
        :type dislikes: list
        :param has: (Optional) an initial list of things the person has
        :type has: list
        :param travels: (Optional) an initial list of the person's travels
        :type travels: list
        """
        self.name = name
        self.likes = [] if likes is None else likes
        self.has = [] if has is None else has
        self.travels = [] if travels is None else travels

    def __repr__(self):
        return self.name


class Pet(object):
    def __init__(self, pet_type, name=None):
        self.name = name
        self.type = pet_type


class Trip(object):
    def __init__(self, date, place=None):
        self.date = date
        self.place = place


persons = []
pets = []
trips = []


def get_data_from_file(file_path='./chatbot_data.txt'):
    with open(file_path) as infile:
        cleaned_lines = [line.strip() for line in infile if not line.startswith(('$$$', '###', '==='))]

    return cleaned_lines


def select_person(name):
    for person in persons:
        if person.name == name:
            return person


def add_person(name):
    person = select_person(name)

    if person is None:
        new_person = Person(name)
        persons.append(new_person)

        return new_person

    return person


def select_pet(name):
    for person in persons:
        if person.name == name:
            return person


def add_pet(type, name=None):
    pet = None

    if name:
        pet = select_pet(name)

    if pet is None:
        pet = Pet(type, name)
        pets.append(pet)

    return pet


def select_trip(name):
    for person in persons:
        if person.name == name:
            return person


def add_trip(date, place=None):
    trip = None

    if place:
        trip = select_trip(place)

    if trip is None:
        trip = Trip(date, place)
        trips.append(trip)

    return trip


def get_persons_pet(person_name):

    person = select_person(person_name)

    for thing in person.has:
        if isinstance(thing, Pet):
            return thing


def get_persons_trip(person_name):

    person = select_person(person_name)

    for thing in person.travels:
        if isinstance(thing, Trip):
            return thing



def process_relation_triplet(triplet):
    """
    Process a relation triplet found by ClausIE and store the data

    find relations of types:
    (PERSON, likes, PERSON)
    (PERSON, has, PET)
    (PET, has_name, NAME)
    (PERSON, travels, TRIP)
    (TRIP, departs_on, DATE)
    (TRIP, departs_to, PLACE)

    :param triplet: The relation triplet from ClausIE
    :type triplet: tuple
    :return: a triplet in the formats specified above
    :rtype: tuple
    """

    sentence = triplet.subject + ' ' + triplet.predicate + ' ' + triplet.object

    doc = nlp(unicode(sentence))

    for t in doc:
        if t.pos_ == 'VERB' and t.head == t:
            root = t
        # elif t.pos_ == 'NOUN'

    # also, if only one sentence
    # root = doc[:].root


    """
    CURRENT ASSUMPTIONS:
    - People's names are unique (i.e. there only exists one person with a certain name).
    - Pet's names are unique
    - The only pets are dogs and cats
    - Only one person can own a specific pet
    - A person can own only one pet
    """


    # Process (PERSON, likes, PERSON) relations
    if root.lemma_ == 'like':
        if triplet.subject in [e.text for e in doc.ents if e.label_ == 'PERSON'] and triplet.object in [e.text for e in doc.ents if e.label_ == 'PERSON']:
            s = add_person(triplet.subject)
            o = add_person(triplet.object)
            s.likes.append(o)

        return 'like'

    if root.lemma_ == 'be' and triplet.object.startswith('friends with'):
        fw_doc = nlp(unicode(triplet.object))
        with_token = [t for t in fw_doc if t.text == 'with'][0]
        fw_who = [t for t in with_token.children if t.dep_ == 'pobj'][0].text
        # fw_who = [e for e in fw_doc.ents if e.label_ == 'PERSON'][0].text

        if triplet.subject in [e.text for e in doc.ents if e.label_ == 'PERSON'] and fw_who in [e.text for e in doc.ents if e.label_ == 'PERSON']:
            s = add_person(triplet.subject)
            o = add_person(fw_who)
            s.likes.append(o)
            o.likes.append(s)

        return 'is'

    if len([e.text for e in doc.ents if e.label_ == 'GPE'])>= 1:
        doc = nlp(unicode(sentence))
        dateref = []
        personnames = [entity.text for entity in doc.ents if entity.label_ == 'PERSON']
        place = [str(entity.text) for entity in doc.ents if entity.label_ == 'GPE']
        date = [str(entity.text) for entity in doc.ents if entity.label_ == 'DATE']
        ref = []

        if date == ref and place != ref:
            date = re.findall("(\d+)", sentence)

        if date == ref:
            return False

        else:
            for x in date:
                newdate = x
        #date = [str(x) for x in date if date ]
        # print (place[0])
        # print (date)
            for p in personnames:
                o = add_person(p)
                ptrip = add_trip(newdate,place[0])
                o.travels.append(ptrip)

            return 'ptrip'

       # print ('yes')
        # we need to get the date and location and person's name
        # then restore them into travel



    # Process (PET, has, NAME)

    if ('dog' in triplet.subject or 'cat' in triplet.subject):
        #print ('yes')

        # process (PET, has, NAME)
        if triplet.subject.endswith('name') and ('dog' in triplet.subject or 'cat' in triplet.subject):
            # below is the original syntax for span
            # obj_span = doc.char_span(sentence.find(triplet.object), len(sentence))
            # using chunks to get compound names

            chunks = list(doc.noun_chunks)[-1].root.text
            petdoc = nlp(chunks)
            obj_span = petdoc.char_span(0,len(chunks))

            # handle single names, but what about compound names? Noun chunks might help.
            if len(obj_span) == 1 and obj_span[0].pos_ == 'PROPN':
                name = triplet.object
                subj_start = sentence.find(triplet.subject)
                subj_doc = doc.char_span(subj_start, subj_start + len(triplet.subject))

                s_people = [token.text for token in subj_doc if token.ent_type_ == 'PERSON']
                assert len(s_people) == 1
                s_person = select_person(s_people[0])

                s_pet_type = 'dog' if 'dog' in triplet.subject or ('dog' in triplet.object) else 'cat'

                pet = add_pet(s_pet_type, name)

                s_person.has.append(pet)

            return 'pet'



    if ('dog' in triplet.object or 'cat' in triplet.object):
        ownername= triplet.subject
        if ownername not in persons:
            add_person(ownername)

        s_person = select_person(ownername)
        if s_person.has == []:
            pet_pet_type = 'dog' if 'dog' in triplet.object else 'cat'
            s_person.has.append(pet_pet_type)

        else:
            return 'pet'

    else:
        return False


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


def has_question_word(string):
    # note: there are other question words
    for qword in ('who', 'what', 'does', 'do'):
        if qword in string.lower():
            return True

    return False



def main():
    sents = get_data_from_file()

    cl = ClausIE.get_instance()

    triples = cl.extract_triples(sents)

    for t in triples:
        r = process_relation_triplet(t)

    #   print(r)


    #print(persons)

    #print(pets)

    traveldic = ['travel', 'fly', 'drive', 'go', 'visit']
    #traveldic = {'travel to': 'take a trip',  # verbs here are lemmatized
     #'fly to': 'take a trip',
     #'drive to': 'take a trip',
     #'go to': 'take a trip',
     #}



    question  = ' '

    while question[-1] != '?':
        question = raw_input("Please enter your question: ")

        if question[-1] != '?':
            print('This is not a question... please try again')
    question2 = question
    question = question.lower()
    q_trip = cl.extract_triples([preprocess_question(question)])[0]
    # q_doc = nlp(unicode((question)))
    doc = nlp(unicode(question2))

    # (WHO, has, PET)
    # here's one just for dogs


    if q_trip.subject.lower() == 'who' and q_trip.object == 'dog':
        answer = '{} has a {}.'

        for person in persons:
            pet = person.has
            if 'dog' in pet:
                print(answer.format(person.name, 'dog'))

    elif q_trip.subject.lower() == 'who' and q_trip.object == 'cat':
        answer = '{} has a {}.'

        for person in persons:
            pet = person.has
            if 'cat' in pet:
                print(answer.format(person.name, 'cat'))


    # here's one for cats
    elif q_trip.subject.lower() == 'who' and q_trip.object == 'cat':
        answer = '{} has a {}.'

        for person in persons:
            pet = get_persons_pet(person.name)
            if pet and pet.type == 'cat':
                print (answer.format(person.name, 'cat'))





    # Does someone like someone else?
    elif (q_trip.object.startswith('like')) and (q_trip.subject == 'does'):
        answer = '{}, {} {} {}.'

        doc = nlp(unicode(question2))
        personnames = [entity.text for entity in doc.ents if entity.label_=='PERSON']
        p1 = str(personnames[0])
        p2 = str(personnames[1])
        host_person = [str(person.likes) for person in persons if person.name == p1]

        if p2 in host_person:
            print (answer.format('Yes',p1,'likes', p2))
        else:
            print (answer.format('No', p1,'does not like', p2))


    # Who likes <person>?
    elif (q_trip.subject == 'who') and (q_trip.predicate == 'likes'):
        answer = '{} {} {}'

        doc = nlp(unicode(question2))
        personnames = [entity.text for entity in doc.ents if entity.label_ == 'PERSON']
        p1 = str(personnames[0])
        personlikep1 = []
        for person in persons:
            personlike = person.likes
            for p in set(personlike):
                if p1 == p.name:
                    personlikep1.append(person.name)
        ref = []

        if personlikep1 != ref:
            print (answer.format(' and '.join(personlikep1), 'likes',p1))
        else:
            print ('Sorry, we don\'t know.')



    # Who does <person> like?
    elif (q_trip.object == 'who') and (q_trip.predicate.endswith('like')):
        answer = '{} {} {}'

        # doc = nlp(unicode(question2))
        personnames = [entity.text for entity in doc.ents if entity.label_ == 'PERSON']
        p1 = str(personnames[0])
        likes = [person.likes for person in persons if person.name == p1][0]
        p1likes = [p.name for p in set(likes) ]
        ref = []
        if p1likes != ref:
            print(answer.format(p1, 'likes', ' and '.join(p1likes)))
        else:
            print ('Sorry, we don\'t know.')



    # Who is [going to | flying to | traveling to | visiting] < place >?
    elif (str(t.lemma_) for t in doc if str(t.lemma) in traveldic ) and (q_trip.subject == 'who'):
        answer = '{} {} {}'
        persontrip = []
        ref = []
        qplace = [str(entity.text) for entity in doc.ents if entity.label_ == 'GPE']
        for person in persons:
            qtrip = get_persons_trip(person.name)
            #print (person.travels.date)
            if qtrip and ( qplace[0] in qtrip.place ):
                persontrip.append(person.name)
                # print (person.name)


        if persontrip != ref:
            print (answer.format(' and '.join(persontrip), 'is traveling to', qplace[0]))

        else:
            print ('Sorry, we don\'t know.')



    # Does <person> likes <Pet>?
    elif q_trip.subject.startswith('does') and ( q_trip.object == ('cat') or q_trip.object == ('dog')):
        answer = '{}, {} does not have a {}.'
        new_subj_doc = nlp(unicode(q_trip.subject))
        #people = new_subj_doc[5:].capitalize()
        # ents = list(new_subj_doc.ents)
        # people = [ents[i].text for i in range(len(ents)) if ents[i].label_=='PERSON']
        new_subj_doc_childern = new_subj_doc[0].children
        people = str([t.text.capitalize() for t in new_subj_doc_childern])


        if people in persons:
            pet = get_persons_pet(people)
            if q_trip.object == pet:
                print(answer.format('Yes', people, q_trip.object))
            else:
                print(answer.format('No', people, q_trip.object))

        else:
            print (answer.format('No', people, q_trip.object))


    else:
        print('We don\'t have the material to answer the question.')



if __name__ == '__main__':
    main()
