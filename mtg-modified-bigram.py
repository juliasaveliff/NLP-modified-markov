def finish_sentence(sentence, m, corpus, max_length=15):
	# sentence: String[] of starter sentence to complete
    # m: maximum distance to compute modified bigram
    # corpus: String[] of training text

    # Generate one word at a time, stopping if sentence has maximum total tokens
    while len(sentence) < max_length: 

        # Get last m words of sentence
        pattern = sentence[-m:]

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
        		frequency[key] = {}
        		if corpus[i] == key: 
        			next_word = corpus[i + d]
        			if next_word not in frequency[key]:
        				frequency[key][next_word] = 0
        			frequency[key][next_word] += 1

        # Determine best word to add to sentence and continue building
        # sentence.append(best_word)

    return sentence