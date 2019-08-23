#! /usr/bin/env python
#######################

import argparse
import random
import markov_model

def main(args):
	in_file = open(args.in_file)
	content = in_file.read()
	in_file.close()
	m = model.TextModel([content])
	while True:
		nw = m.next_word(random.random())
		if nw == None:
			break
		print(nw, end=" ")
	print()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("in_file")
	args = parser.parse_args()
	main(args)
