def finish_sentence(sentence, n, corpus, max_length=15):
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

import json
with open("data.json") as file:
    data = json.load(file)

body = []
titles=[]
sports = []

for item in data["2019"]:
    body = body + item["content"].split()
    titles = titles+ item["title"].split()
    titles.append(".")
sentence = "Duke students are ".split()
print(len(body))
#print(body[0:100])
result = finish_sentence(sentence,3,body)


# import nltk
# # nltk.download("brown")
# from nltk.corpus import brown
# words = brown.words()[:500]
# sentence = "the jury had".split()
# result = finish_sentence(sentence, 3, words)
print(' '.join(result))