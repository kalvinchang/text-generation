import numpy, random

# obtains the text from the file
def get_corpus():
    corpus_string = "foo bar foo bar bar"
    return corpus_string.split()

# returns a list of all the distinct words in the original body of text
def get_unique_words(corpus_array):
    unique_word_array = []

    for word in corpus_array:
        if word not in unique_word_array:
            unique_word_array.append(word)

    # the end of the sentence is treated as the next line character
    unique_word_array.append('\n')

    return unique_word_array

# returns a matrix that records the probability of a word occurring given that another word occurs
def create_transition_matrix(unique_words, corpus_array):
    n = len(unique_words)
    transition_matrix = numpy.ndarray((n, n))
    word_count_corpus = len(corpus_array)

    # initialize transition_matrix[n - 1], the row of the end of the line character, to a row of zeros
    # because no word can follow the end of the sentence
    transition_matrix[n - 1] = numpy.zeros(n).tolist()

    # initialize transition_matrix[n - 1][n - 1] to 1
    # because the probability that the next character after the ending is the end is 1
    transition_matrix[n - 1][n - 1] = 1

    for row in range(n):        # index of A in P(A -> B)
        for col in range(n):    # index of B in P(A -> B)
            # calculate P(B | A) = P(A -> B)
            word_count = 0
            A = unique_words[row] # word in question
            B = unique_words[col] # word
            # find all instances of word A in corpus_array
            instances_of_word = [i for i, word in enumerate(corpus_array) if word == A]

            # examine the word right after
            for A_index in instances_of_word:
                # if word right after is the same as the word at unique_words[col]
                    # increment counter
                if A_index != word_count_corpus - 1 and corpus_array[A_index + 1] == B:
                    word_count = word_count + 1
                # if you are examining the last word in the sentence,
                    # move on
                    # because the probability of another word following it is 0 (check A_index != n)

            # probability that the last word in the sentence is followed by the end is nonzero
            if B == '\n' and A == corpus_array[word_count_corpus - 1]:
                word_count = word_count + 1

            if A != '\n':
                # skip the row where A == '\n' because it was addressed above
                # transition_matrix[A][B] = P(A -> B) = P(B | A)
                transition_matrix[row][col] = word_count / len(instances_of_word)

    return transition_matrix

# use the transition matrix to predict the following word given a specific word
def predict_next_word(current_word, unique_words, transition_matrix):
    index = unique_words.index(current_word)
    # get index of current_word inside unique_words
    # return row, whichever has highest probability wins

    return numpy.random.choice(unique_words, 1, p=transition_matrix[index])

# create an output of a certain length
def create_output(unique_words, transition_matrix):
    text_list = []
    generated_text = ''
    # randomly pick one word to start
    next_word = random.choice(unique_words)
    # first word should not be the end - would result in empty text generated
    while next_word == '\n':
        next_word = random.choice(unique_words)
    generated_text += next_word
    text_list.append(next_word)

    while (next_word != '\n'):
        #print(generated_text)
        next_word = predict_next_word(text_list[len(text_list) - 1], unique_words, transition_matrix)[0]
        generated_text += ' ' + next_word
        text_list.append(next_word)

    return generated_text

def text_generation():
    corpus = get_corpus()
    unique_words = get_unique_words(corpus)
    transition_matrix = create_transition_matrix(unique_words, corpus)
    generated_text = create_output(unique_words, transition_matrix)
    return generated_text

#print(create_transition_matrix(get_unique_words(get_corpus()), get_corpus()))
print(text_generation())