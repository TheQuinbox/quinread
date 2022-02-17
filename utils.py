def plural(number, singular, multiple):
	return singular if number in [1, -1] else multiple

def count_words(content):
	word_list = content.split(" ")
	count = len(word_list)
	del word_list
	return count
