def finish_sentence_simple(sentence, n, corpus, max_length=15):
	# sentence: String[]
	# n: int 
	# corpus: String[]

	corpus = [word.lower() for word in corpus]

	pattern = sentence[-(n-1):]
	output = []
	for item in pattern:
		output.append(item)

	# Stop when generated sentence has max length
	while (len(output) + len (sentence[:-(n-1)])) < max_length:
		frequency={}

		for i in range(n,len(corpus)-1):
			if pattern ==corpus[(i-n+1):i]:
				next_word = corpus[i]

				if next_word not in frequency:
					frequency[next_word] = 0
				frequency[next_word]+=1
		next = ""
		max_freq = 0
		for value in frequency.keys():
			if frequency[value]>max_freq:
				max_freq = frequency[value]
				next = value

		if (n==2):
			pattern = []
		else:
			pattern = pattern[-(n-2):]

		pattern.append(next);

		output.append(next);
		end = [".","!","?"]
		if next in end:
			return sentence[:-(n-1)]+ output

	return sentence[:-(n-1)] + output