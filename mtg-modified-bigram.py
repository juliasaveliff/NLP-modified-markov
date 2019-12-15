def finish_sentence(sentence, m, corpus, max_length=15):
	# sentence: String[] of starter sentence to complete
    # m: maximum distance to compute modified bigram
    # corpus: String[] of training text

    # Generate one word at a time, stopping if sentence has maximum total tokens
    while len(sentence) < max_length: 

    	# Preprocess corpus
        corpus = [word.lower() for word in corpus]
        vocabulary = list(set(corpus))
        word_to_ix = {}
        ix_to_word = {}
        for (ix, word) in enumerate(vocabulary):
        	word_to_ix[word] = ix
        	ix_to_word[ix] = word

        # Get last m words of sentence
        pattern = sentence[-m:]
        print("starter sentence:", pattern)

        # Stop when the first ., ?, or ! is found
        if pattern[-1] in ['.', '?', '!']:
            break

        # Find wherever previous exists in corpus
        frequency = {}

        # Iterate over every word in corpus
        for i in range(len(corpus)-m): 
        	# Iterate over pattern
        	for k in range(m): 
        		key = pattern[k]
        		d = m - k
        		if key not in frequency: 
        			frequency[key] = {} # TODO replace with probability distribution
        		if corpus[i] == key: 
        			next_word = corpus[i + d]
        			if next_word not in frequency[key]:
        				frequency[key][next_word] = 0
        			frequency[key][next_word] += 1

        combined_frequency = {}
        for key in frequency.keys():
        	for word in frequency[key].keys():
        		if word not in combined_frequency:
        			combined_frequency[word] = 0
        		combined_frequency[word] += frequency[key][word]

        best_words = []
        max_frequency = 0 
        for word in combined_frequency.keys(): 
        	if combined_frequency[word] == max_frequency:
        		best_words.append(word)
        	elif combined_frequency[word] > max_frequency:
        		best_words = []
        		best_words.append(word)
        		max_frequency = combined_frequency[word]

        print("best words:", best_words)

        # Determine best word to add to sentence and continue building
        sentence.append(best_words[0])


    return sentence




import nltk
# nltk.download("brown")
from nltk.corpus import brown
words = brown.words()[:500]
sentence = "the jury had".split()
result = finish_sentence(sentence, 3, words)
print(' '.join(result))
