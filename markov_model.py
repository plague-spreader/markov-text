class Model:
	"""
	A class representing a Markov model of the given data.
	
	This class has three internal variables:
		- self.init_probs =
			a list of pairs (probability to choose the i-th word,
			the i-th word). Used when we need to choose the first word (i.e.
			self.current_word is None);
		- self.probs = a dictionary {word:pairs (probability next word,
			next word)}. This represents the probability of choosing the
			next word given the current word;
		- self.current_word = the current word.
	
	There are three "private" methods: _add_to_model, _p_w_pairs,
	_compute_model.
	
	This class is meant to be extended, see the subclasses TextModel and
	ByteModel.
	"""
	
	def _add_to_model(self, words):
		"""
		Add <words> to current model and all the pairs (word, next_word).
		Also adds the pair (last_word, None) where None means
		"end of word generation".
		"""
		
		try:
			self.words.extend(words)
		except AttributeError:
			self.words = words[:]
		words_shift = words[1:]
		words_shift.append(None)
		pairs = [(words[i], words_shift[i]) for i in range(len(words))]
		try:
			self.pairs.extend(pairs)
		except AttributeError:
			self.pairs = pairs
	
	def _p_w_pairs(words):
		"""
		Compute a list (pi, wi) where wi is the word and pi is the
		probability of choosing that word randomly.
		"""
		
		words_set = set(words)
		cum_probs = [words.count(w)/len(words) for w in words_set]
		cum_prob = 0.0
		for i, p in enumerate(cum_probs):
			cum_prob += p
			cum_probs[i] = cum_prob
		return list(zip(cum_probs, words_set))
	
	def _compute_model(self):
		"""
		Compute all the relevant probabilities.
		"""
		
		self.init_probs = Model._p_w_pairs(self.words)
		adj_words = {}
		for i, pair in enumerate(self.pairs):
			word, word_shift = pair
			if word not in adj_words:
				adj_words[word] = [word_shift]
			else:
				adj_words[word].append(word_shift)
		
		self.probs = {k:Model._p_w_pairs(v) for k, v in adj_words.items()}
		self.current_word = None
		del self.words, self.pairs
	
	def next_word(self, p):
		"""
		Given the probability <p> compute the next word if self.current_word
		is not None otherwise choose the first word. self.current_word is
		changed afterwards.
		"""
		
		if self.current_word == None:
			to_iter = self.init_probs
		else:
			to_iter = self.probs[self.current_word]
		
		for pi, wi in to_iter:
			if p < pi:
				self.current_word = wi
				return wi
	
	def multiple_choices(self, pl):
		"""
		Given a list of probabilities <pl> return a list of the same size of
		all the possible next words if self.current_word is not None
		otherwrise return all the first words. Afterwards you may want to use
		the method set_current_word.
		
		This is meant to emulate the smartphone feature of word
		auto-completion.
		"""
		
		if self.current_word == None:
			to_iter = self.init_probs
		else:
			to_iter = self.probs[self.current_word]
		
		ret = []
		for p in pl:
			for pi, wi in to_iter:
				if p < pi:
					ret.append(wi)
		return ret
	
	def set_current_word(self, word):
		"""
		Just set self.current_word to <word>.
		"""
		
		self.current_word = word

class TextModel(Model):
	"""
	This class constructs a Markov model from one or multiple texts.
	"""
	
	def __init__(self, content, sep=None, maxsplit=-1):
		for phrase in content:
			words = phrase.split(sep, maxsplit)
			self._add_to_model(words)
		self._compute_model()

class ByteModel(Model):
	"""
	This class represents a Markov model from a byte stream.
	"""
	
	def __init__(self, content):
		self._add_to_model(content)
		self._compute_model()
