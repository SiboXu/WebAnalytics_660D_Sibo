
def process_data(path_to_file):
    if not isinstance(path_to_file, str):
        raise Exception("{} is not a string".format(path_to_file))
    with open (path_to_file) as infile:
        return [line for line in infile if not line[0] in ('$', '#', '=')]


process_data ('/Users/xusibocn/Downloads/chatbot_data.txt')

# print ("what is this")
