def plural(number, singular, multiple):
	if number == 1 or number == -1:
		return singular
	else:
		return multiple

def count_words(content):
	word_list = content.split(" ")
	count = len(word_list)
	del word_list
	return count
