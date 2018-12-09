import numpy, random

def get_corpus():
    corpus_string = "foo bar foo bar bar"
    return corpus_string.split()

def get_unique_words(corpus_array):
    unique_word_array = []

    for word in corpus_array:
        if word not in unique_word_array:
            unique_word_array.append(word)
    return unique_word_array

def create_transition_matrix(unique_words, corpus_array):
    n = len(unique_words)
    transition_matrix = numpy.ndarray((n, n))
    word_count_corpus = len(corpus_array)

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
                # if you are examining the last word in the sentence, move on
                    # because the probability of another word following it is 0 (check A_index != n)

            # transition_matrix[A][B] = P(A -> B) = P(B | A)
            transition_matrix[row][col] = word_count / len(instances_of_word)

    return transition_matrix

def predict_next_word(current_word, unique_words, transition_matrix):
    index = unique_words.index(current_word)
    # get index of current_word inside unique_words
    # return row, whichever has highest probability wins
    wow = numpy.random.choice(unique_words, 1, p=[0.5, 0.5]) #transition_matrix[index]
    return wow[0]

def create_output(unique_words, transition_matrix, num_words):
    text_list = []
    generated_text = ''
    # randomly pick one word to start
    first_word = random.choice(unique_words)
    generated_text += first_word
    text_list.append(first_word)

    for i in range(num_words):
        #print(generated_text)
        next_word = predict_next_word(text_list[i], unique_words, transition_matrix)
        generated_text += ' ' + next_word
        text_list.append(next_word)

    return generated_text

def text_generation():
    corpus = get_corpus()
    unique_words = get_unique_words(corpus)
    transition_matrix = create_transition_matrix(unique_words, corpus)
    num_words = 10
    generated_text = create_output(unique_words, transition_matrix, num_words)
    return generated_text

#print(create_transition_matrix(get_unique_words(get_corpus()), get_corpus()))
print(text_generation())