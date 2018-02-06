# import spacy

# nlp = spacy.load('en')

def process_data (path_to_file):
    if not isinstance(path_to_file, str):
        raise Exception("{} is not a string".format(path_to_file))
    with open(path_to_file) as infile:
        return ([line for line in infile if not line[0] in ('$', '#', '=')])

def main(path_to_file):
    print (process_data(path_to_file))

m = process_data('/Users/xusibocn/Downloads/chatbot_data.txt')

print (m)

# main ('/Users/xusibocn/Downloads/chatbot_data.txt')


# this is a single line comment

"""multiline uses triple quotest (single  or dounble """

"""
Relation list

(person , linkes , person)
(person, has , object )
(person, travels, place)
(person, Travels, where)

"""

# import spacy

# process_data('/Users/xusibocn/Desktop/SIT/Course/BIA 660/WebAnalytics_660D_Sibo/chatbot_data.txt')

# infile = open('/Users/xusibocn/Desktop/SIT/Course/BIA 660/WebAnalytics_660D_Sibo/chatbot_data.txt', 'r')


# outfile = open('output.tex', 'w')

# file_text = infile.read()

# print (file_text)

