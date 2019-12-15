def finish_sentence(sentence, m, corpus_list, max_length=15):
	# sentence: String[] of starter sentence to complete
    # m: maximum distance to compute modified bigram
    # corpus: String[] of training text

    generated_sentence = sentence.copy()

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

    # Weight of word decreases by 1/2 with distance from next word to gerneate
    pmf_weights_unnormalized = [2**i for i in range(m)]
    pmf_weights = [float(i)/sum(pmf_weights_unnormalized) for i in pmf_weights_unnormalized]

    # Generate one word at a time, stopping if sentence has maximum total tokens
    while len(generated_sentence) < max_length: 

        # Get last m words of sentence
        pattern = generated_sentence[-m:]
        # print("starter sentence:", pattern)

        # Stop when the first ., ?, or ! is found
        if pattern[-1] in ['.', '?', '!']:
            break

        # Initialize frequency of all words in vocabulary
        frequency = {}
        for key in pattern:
        	frequency[key] = {word:0 for word in vocabulary}

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
        			frequency[key][next_word] += 1

        # Combine probability mass functions for each key's categorical distribution
        pmf = {}
        for key in frequency.keys():
        	pmf[key] = {}
        	total = sum(frequency[key].values())
        	for word in frequency[key]:
        		pmf[key][word] = float(frequency[key][word]) / total

        combined_pmf = {word:0 for word in vocabulary}
        for (ix, key) in enumerate(pattern):
        	weight = pmf_weights[ix]
        	for word in pmf[key]:
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

        # print("best words:", best_words)

        # Determine best word to add to sentence and continue building
        generated_sentence.append(best_words[0])

    return generated_sentence


import nltk
# nltk.download("brown")
from nltk.corpus import brown
words = brown.words()[:1000]
sentence = "the jury had".split()
result = finish_sentence(sentence, 3, words)
print(' '.join(sentence))
print(' '.join(result))

sentence2 = "this judge was the".split()
result2 = finish_sentence(sentence2, 3, words)
print(' '.join(sentence2))
print(' '.join(result2))
