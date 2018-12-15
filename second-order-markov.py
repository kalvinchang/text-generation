import numpy, random, string

# obtains the text from the file and returns each word as an array
def get_corpus(filename):
    file1 = open(filename, "r", encoding="utf8") #,
    text = file1.read() # corpus as one long string
    return text.split(" ") # corpus as arrays (each word is its own element)
    # split by space only, not new line

# creates a dictionary with pairs as keys and mapping to other pairs 
def get_pairs(corpus_array):
    lexicon = {} 
    for i in range(len(corpus_array) - 2):
        # checks if tuple exists in dictionary 
        lexicon[(corpus_array[i], corpus_array[i+1])] = \
            lexicon.get((corpus_array[i], corpus_array[i+1]), {})
        # adds 1 evevery time pair, next value comb happens
        lexicon[(corpus_array[i],corpus_array[i+1])][(corpus_array[i+1],\
            corpus_array[i+2])] = lexicon[(corpus_array[i],corpus_array[i+1])]\
            .get((corpus_array[i+1],corpus_array[i+2]), 0) + 1

    return lexicon 

# uses dictionary to create transition matrix
def create_2d_transition_matrix(lexicon):
    t_matrix = []
    for in_pair in lexicon:
        row = []
        add = 0
        # creates rows of matrices
        for out_pair in lexicon:
            row.append(lexicon[in_pair].get(out_pair, 0))
            add += lexicon[in_pair].get(out_pair, 0)
        # removes rows with no chance of happening
        if add == 0:
            continue
        # ensures that elements in rows add up to 1
        for num in range(len(row)):
            row[num] /= add
        t_matrix.append(row)

    return t_matrix


# use the transition matrix to predict the following word given a specific word
def predict_next_word(current_pair, lexicon, transition_matrix):
    index = list(lexicon.keys()).index(current_pair)
    # the row of the transition matrix corresponding to the current word serves as a probability distribution
    # the indices of the probability distribution correspond to the tuples in the dictionary
    # numpy picks a word out of the dictionary given the aforementioned probability distribution
    choice = int(numpy.random.choice(len(list(lexicon.keys())), 1,\
        p=transition_matrix[index]))
    return list(lexicon.keys())[choice]

# returns entire string of generated text by drawing successive words from dictionary with predict_next_word
def create_output(lexicon, transition_matrix):
    text_list = []
    generated_text = ''
    # randomly pick one word that is capitalized to start
    capitalized = []
    for i in lexicon:
        if i[0].isupper():
            capitalized.append(i)
    next_pair = random.choice(capitalized)
    generated_text += next_pair[0]
    text_list.append(next_pair)

    # new line was having some problems with the tuple inputs
    # a counter was put in instead for demonstration purposes
    counter = 0 
    while counter <50:
        next_pair = predict_next_word(next_pair, lexicon, transition_matrix)
        # this is here so words are not repeated
        if counter % 2 == 1:
            generated_text += ' ' + next_pair[0] + ' ' + next_pair[1]
            text_list.append(next_pair)
        counter += 1

    return generated_text

# the main function
def text_generation(file_name):
    corpus = get_corpus(file_name)
    lexicon = get_pairs(corpus)
    transition_matrix = create_2d_transition_matrix(lexicon)
    generated_text = create_output(lexicon, transition_matrix)
    return generated_text

# replace file with desired input file
# input file must be in same folder as this Python file
print(text_generation("bts-fake-love.txt"))

