import sys
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordTokenizer, TreebankWordDetokenizer

# Regex for text cleaning
BEGIN_CHAR_REGEX = re.compile(r'[A-Za-z]')
BEGIN_NUMBER_REGEX = re.compile(r'^[0-9]')

VALUE = re.compile(r'[0-9]+\.?[0-9]*')
SPLITTER = re.compile(r'[- \n]')
SPECIAL_CHAR_BUT_HIF_USER = re.compile(r'(\p{P}(?<![-|(u\/)])|[\|()<>+.=´`~^¨ªº])')


english_stopwords = nltk.corpus.stopwords.words('english')
porter_stemmer = nltk.stem.PorterStemmer()
wordnet_lemmatizer = WordNetLemmatizer()

def cleaner_builder(text, lower_words=False, fold_numbers=False, remove_stopwords=False, do_stemming=False, do_lemmatizing=False):
	tagged_words = _extract_tagged_words(text)
	
	if (lower_words):
		tagged_words = [word.lower() for (word, postag) in tagged_words]

	if (fold_numbers):
		tagged_words = ['NUM' if re.match(BEGIN_NUMBER_REGEX, word) else word for (word, postag) in tagged_words]
	
	if (remove_stopwords):
		tagged_words = [word for (word, postag) in tagged_words if word not in english_stopwords]
	
	if (do_stemming):
		tagged_words = [porter_stemmer.stem(word) for (word, postag) in tagged_words]

	if (do_lemmatizing):
		tagged_words = [wordnet_lemmatizer.lemmatize(word, pos='n') for (word, postag) in tagged_words]

	min_length = 3

	return [(term, postag) for (term, postag) in tagged_words if BEGIN_CHAR_REGEX.match(term) and len(term) >= min_length]

def _extract_tagged_words(text):
	values = [] # find use for values
	def fold_num(match):
		values.append(match)
		return 'NUM' + str(len(values)-1)

	text = re.sub(VALUE, fold_num, text)
	text = re.sub(SPECIAL_CHAR_BUT_HIF_USER, _capture_replace, text)
	words = [word for word in SPLITTER.split(text) if word]
	tagged_words = nltk.pos_tag(words)
	
	return tagged_words

def _capture_replace (match):
	return ' ' + match.group(1) + ' '