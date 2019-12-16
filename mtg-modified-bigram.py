def beautify_text(word_list):
	sentence = ''
	for (ix, word) in enumerate(word_list): 
		if ix == 0: 
			sentence += word.capitalize()
		else: 
			if word in ['.', '?', '!', ',', ';']:
				sentence += word
			else: 
				sentence += ' '
				if word_list[ix-1] in ['.', '?', '!']: 
					sentence += word.capitalize()
				else:
					sentence += word
	return sentence

def finish_sentence(sentence, max_distance, corpus_list, max_length=50):
	# sentence: String[] of starter sentence to complete
    # m: maximum distance to compute modified bigram
    # corpus: String[] of training text

    generated_sentence = [word.lower() for word in sentence]

    # Preprocess corpus
    corpus = [word.lower() for word in corpus_list]
    vocabulary = list(set(corpus))
    word_to_ix = {}
    ix_to_word = {}
    for (ix, word) in enumerate(vocabulary):
    	word_to_ix[word] = ix
    	ix_to_word[ix] = word

    for word in generated_sentence: 
    	if word.lower() not in vocabulary: 
    		print(word + ' not in vocabulary')
    		return generated_sentence

    # Generate one word at a time, stopping if sentence has maximum total tokens
    while len(generated_sentence) < max_length: 

    	# If sentence contains less than max_distance 
        if len(generated_sentence) < max_distance: 
        	m = len(generated_sentence)
        else: 
        	m = max_distance

        # Weight of word decreases by 1/2 with distance from next word to gerneate
        # pmf_weights_unnormalized = [2**i for i in range(m)]

        # Weight words equally
        pmf_weights_unnormalized = [1 for i in range(m)]
        pmf_weights = [float(i)/sum(pmf_weights_unnormalized) for i in pmf_weights_unnormalized]

        # Get last m words of sentence
        pattern = generated_sentence[-m:]

        # Stop when the first ., ?, or ! is found
        if pattern[-1] in ['.', '?', '!']:
            break

        # Initialize frequency of all words in vocabulary
        frequency = {}
        # for key in pattern:
        	# frequency[key] = {word:0 for word in vocabulary}

        # Iterate over every word in corpus
        for i in range(len(corpus)-m): 
        	# Iterate over pattern, starting with word farthest from next word to generate
        	for k in range(m): 
        		key = pattern[k]
        		# Count words that appear a distance of d from key
        		d = m - k
        		if key not in frequency: 
        			frequency[key] = {}
        		if corpus[i] == key: 
        			next_word = corpus[i + d]
        			if next_word not in frequency[key]:
        				frequency[key][next_word] = 0
        			frequency[key][next_word] += 1

        # Combine probability mass functions for each key's categorical distribution
        pmf = {}
        for key in frequency.keys():
        	pmf[key] = {}
        	total = sum(frequency[key].values())
        	for word in frequency[key]:
        		pmf[key][word] = float(frequency[key][word]) / total

        # combined_pmf = {word:0 for word in vocabulary}
        combined_pmf = {}
        for (ix, key) in enumerate(pattern):
        	weight = pmf_weights[ix]
        	for word in pmf[key]:
        		if word not in combined_pmf:
        			combined_pmf[word] = 0
        		combined_pmf[word] += pmf[key][word] * weight

        # Get best word option based on combined and weighted probabilities
        best_words = []
        max_probability = 0 
        for word in combined_pmf.keys(): 
        	if combined_pmf[word] == max_probability:
        		best_words.append(word)
        	elif combined_pmf[word] > max_probability:
        		best_words = []
        		best_words.append(word)
        		max_probability = combined_pmf[word]

        generated_sentence.append(best_words[0])

    return beautify_text(generated_sentence)
             

import nltk
# nltk.download("brown")
from nltk.corpus import brown
words = brown.words()[:5000]

sentence = "The jury had"
print(sentence)
print(finish_sentence(sentence.split(), 5, words))

sentence = "When"
print(sentence)
print(finish_sentence(sentence.split(), 5, words))
