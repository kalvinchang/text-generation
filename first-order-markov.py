import numpy, random, string

# obtains the text from the file and returns each word as an array
def get_corpus(filename):
    file1 = open(filename, "r", encoding="utf8") #,
    text = file1.read() # corpus as one long string
    return text.split(" ") # corpus as arrays (each word is its own element)
    # split by space only, not new line

# returns a list of all the distinct words in the original body of text
def get_unique_words(corpus_array):
    unique_word_array = []

    for word in corpus_array:
        if word not in unique_word_array:
            unique_word_array.append(word)

    # the end of the sentence is treated as the next line character
    unique_word_array.append('\n')
    # capitalize first word automatically (assume it's the first word in a sentence)
    unique_word_array[0].capitalize()

    return unique_word_array

# returns a matrix that records the probability of a word occurring given that another word occurs
def create_transition_matrix(unique_words, corpus_array):
    n = len(unique_words)
    transition_matrix = numpy.ndarray((n, n)) # 2 dimensional array
    word_count_corpus = len(corpus_array)
    # each word in corpus_array has same index in transition_matrix (along rows, along columns)

    # initialize transition_matrix[n - 1], the row of the end of the line character, to a row of zeros
    # because no word can follow the end of the sentence
    transition_matrix[n - 1] = numpy.zeros(n)

    # initialize transition_matrix[n - 1][n - 1] to 1
    # because the probability that the next character after the ending is the end is 1
    transition_matrix[n - 1][n - 1] = 1

    for row in range(n):        # index representing A in P(A -> B)
        for col in range(n):    # index representing B in P(A -> B)
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
                    # do not increment the counter
                    # because the probability of another word following it is 0

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
    # the row of the transition matrix corresponding to the current word serves as a probability distribution
    # the indices of the probability distribution correspond to those of unique_words
    # numpy picks a word out of unique_words given the aforementioned probability distribution
    return numpy.random.choice(unique_words, 1, p=transition_matrix[index])

# returns entire string of generated text by drawing successive words from unique_words with predict_next_word
def create_output(unique_words, transition_matrix):
    text_list = []
    generated_text = ''
    # randomly pick one word that is capitalized to start
    # len(word) > 0 prevents string index out of bounds access
    capitalized_words = [word for word in unique_words if len(word) > 0 and word[0].isupper()]
    next_word = random.choice(capitalized_words)
    # first word should not be the end - would result in empty text generated
    # keep generating text until you hit the end of line character - length is random
    while next_word == '\n':
        next_word = random.choice(unique_words)
    generated_text += next_word
    text_list.append(next_word)

    while next_word != '\n':
        #print(generated_text)
        next_word = predict_next_word(text_list[len(text_list) - 1], unique_words, transition_matrix)[0]
        # take index 0 because numpy.random.choice returns the chosen element as a one-element array
        generated_text += ' ' + next_word
        text_list.append(next_word)

    return generated_text

# the main function
def text_generation(file_name):
    corpus = get_corpus(file_name)
    unique_words = get_unique_words(corpus)
    transition_matrix = create_transition_matrix(unique_words, corpus)
    generated_text = create_output(unique_words, transition_matrix)
    return generated_text

# replace file with desired input file
# input file must be in same folder as this Python file
print(text_generation("hello-world.txt"))
