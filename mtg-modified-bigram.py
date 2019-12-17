import random
import numpy as np

def beautify_text(word_list):
	# Edit a list of words and punctuation into a correct format
	text = ''
	for (ix, word) in enumerate(word_list): 
		if ix == 0: 
			text += word.capitalize()
		else: 
			if word in ['.', '?', '!', ',', ';', ':']:
				text += word
			else: 
				text += ' '
				if word_list[ix-1] in ['.', '?', '!']: 
					text += word.capitalize()
				else:
					text += word
	return text


def get_start_phrase(corpus, n=1):
	# Given a corpus, return a phrase commonly found at the start of sentences of length n
	freq = {}

	for i in range(len(corpus)-n):
		if corpus[i] == ".":
			next_phrase = " ".join(corpus[i+1:i+n+1])
			if corpus[i+1]!= "Signup" and corpus[i+1]!= "Cancel":
				if next_phrase not in freq:
					freq[next_phrase] = 0
				freq[next_phrase] += 1
	max_freq = 0
	result = []
	for word in freq.keys():
		if freq[word] == max_freq:
			result.append(word)
		elif freq[word] > max_freq:
			result = []
			result.append(word)
			max_freq = freq[word]
	return random.choice(result).split()


def finish_sentence_simple_ngram_MTG(sentence, n, corpus, max_length=50, end_at_sentence_end=False):
	# sentence: String[]
	# n: int for n-gram 
	# corpus: String[]
	# max_length: maximum length of text to return 
	# end at sentence end: stop when a sentence ending token is added 

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
		if end_at_sentence_end and next in end:
			return sentence[:-(n-1)]+ output

	return beautify_text(sentence[:-(n-1)] + output)


def finish_sentence(sentence, max_distance, corpus_list, max_length=50, starter_length=5, deterministic=True, use_corpus_frequency=False, end_at_sentence_end=False):
	# sentence: String[] of starter sentence to complete
	# max_distance: maximum distance to compute modified bigram
	# corpus_list: String[] of training text
	# max_length: maximum length of text to be generated
	# starter_length: length of starter phrase to generate if no starter setnence is given 
	# deterministic: Bool indicating whether the appended words should be chosen deterministically or not
	# use_corpus_frequency: Bool indicating whether or not bigram frequencies should be scaled by inverse corpus frequency
	# end at sentence end: stop when a sentence ending token is added 

	if len(sentence) == 0:
		generated_sentence = [word.lower() for word in get_start_phrase(corpus_list, starter_length)]
		print("Starter sentence:", beautify_text(generated_sentence))
	else: 
		generated_sentence = [word.lower() for word in sentence]

	# Preprocess corpus
	corpus = [word.lower() for word in corpus_list]
	corpus_size = len(corpus)
	vocabulary = list(set(corpus))

	# Check if there are any unseen words (out-of-vocabulary)
	for word in generated_sentence: 
		if word.lower() not in vocabulary: 
			print(word + ' not in vocabulary')
			return generated_sentence

	# Build corpus (document) frequency
	corpus_frequency = {}
	for word in corpus:
		if word not in corpus_frequency:
			corpus_frequency[word] = 0
		corpus_frequency[word] += 1

	# Generate one word at a time, stopping if sentence has maximum total tokens
	while len(generated_sentence) < max_length: 

		# Determine number of previous words to look at
		if len(generated_sentence) < max_distance: 
			m = len(generated_sentence)
		else: 
			m = max_distance

		# Determine weighting for words in pattern
		pmf_weights_unnormalized = [2**i for i in range(m)]
		pmf_weights = [float(i)/sum(pmf_weights_unnormalized) for i in pmf_weights_unnormalized]

		# Get last m words of sentence
		pattern = generated_sentence[-m:]

		# Stop when the first sentence ender is found
		if end_at_sentence_end and pattern[-1] in ['.', '?', '!']:
			break

		# Map each key in the pattern to counts of every word that ever occurs a distance d afterwards
		raw_counts = {}
		for i in range(len(corpus)-m): 
			# Iterate over pattern, starting with word farthest from next word to generate
			for k in range(m): 
				key = pattern[k]
				# Count words that appear a distance of d from key
				d = m - k
				if key not in raw_counts: 
					raw_counts[key] = {}
				if corpus[i] == key: 
					next_word = corpus[i + d]
					if next_word not in raw_counts[key]:
						raw_counts[key][next_word] = 0
					raw_counts[key][next_word] += 1

		# Normalize counts of every word based on frequency of associated key in corpus AND frequency of word in corpus
		pmf = {}
		for (key, bigram_counts) in raw_counts.items():
			pmf[key] = {}
			key_frequency = corpus_frequency[key]
			for word in bigram_counts: 
				word_frequency = corpus_frequency[word]
				if use_corpus_frequency: 
					pmf[key][word] = (np.log(float(bigram_counts[word])) * np.log(float(corpus_size) / word_frequency)) / key_frequency
				else:
					pmf[key][word] = float(bigram_counts[word]) / key_frequency

		# Combine probability mass functions for each key's categorical distribution
		combined_pmf = {}
		for (ix, key) in enumerate(pattern):
			weight = pmf_weights[ix]
			for word in pmf[key]:
				if word not in combined_pmf:
					combined_pmf[word] = 0
				combined_pmf[word] += pmf[key][word] * weight

		# Get best word option based on combined and weighted probabilities
		if deterministic: 
			best_words = []
			max_probability = 0 
			for word in combined_pmf.keys(): 
				if combined_pmf[word] == max_probability:
					best_words.append(word)
				elif combined_pmf[word] > max_probability:
					best_words = []
					best_words.append(word)
					max_probability = combined_pmf[word]
			word_to_append = best_words[0]

		else: 
			num_to_choose_from = 3
			best_words_to_probabilities = [
				word for (word, value) in sorted(combined_pmf.items(), reverse=True, key=lambda item: item[1])
			][:num_to_choose_from]
			word_to_append = random.choice(best_words_to_probabilities)

		generated_sentence.append(word_to_append)

	return beautify_text(generated_sentence)



# Running the corpus
import nltk
nltk.download("brown")
from nltk.corpus import brown
words = brown.words()[:10000]

f = open("opinion_corpus.txt", "r")
words = [line.rstrip('\n') for line in f]
f.close()
words = words[:100000]

# sentence = "The jury had"
# print(sentence)
# print(finish_sentence(sentence.split(), 5, words))

# sentence = "When"
# print(sentence)
# print(finish_sentence(sentence.split(), 5, words))

# sentence = ['However', ',', 'the', 'Durham', 'faithful']
# sentence = "at the same time".split()
# sentence = ['in', 'fact', ',']
# sentence = "The jury had"

sentence = "at the same time ,".split()
print(beautify_text(sentence))
print("Simple:", finish_sentence_simple_ngram_MTG(sentence, 6, words))
print()
print("Result:", finish_sentence(sentence, 5, words))
print()
print("Result with non-deterministic:", finish_sentence(sentence, 5, words, deterministic=False))
print()
print("Result with document frequency:", finish_sentence(sentence, 5, words, use_corpus_frequency=True))
print()
print("Result with non-deterministic AND document frequency:", finish_sentence(sentence, 5, words, deterministic=False, use_corpus_frequency=True))
print()
