#! /usr/bin/env python

import argparse
import random
import json
import pathlib
import pickle
import markov_model

def do_nothing(*args):
	# literally do nothing.
	pass

def main(args):
	random.seed(args.seed)
	model = None
	my_print = do_nothing
	if args.info:
		my_print = print
	my_print("[+] Checking if \"./model_picke\" exists ...")
	if pathlib.Path("./model_pickle").exists():
		my_print("[+] It exists. Loading ...")
		fp = open("./model_pickle", "rb")
		model = pickle.load(fp)
		fp.close()
		my_print("[+] \"./model_pickle\" loaded.")
	else:
		my_print("[+] It does not exists. Creating the Markov model\
 (this may take a while ...)")
		fp = open(args.json_file)
		content = json.load(fp)
		fp.close()
		model = markov_model.TextModel(content)
		fp = open("./model_pickle", "wb")
		pickle.dump(model, fp)
		fp.flush()
		fp.close()
		my_print("[+] Markov model created and saved in \"./model_pickle\"")
	my_print()
	my_print()
	
	while True:
		nw = model.next_word(random.random())
		if nw == None:
			break
		print(nw, end=" ")
	print()

if __name__ == '__main__':
	ap = argparse.ArgumentParser(description=\
"\
Markov chain generated random text from old chats (requires your chat data\
as JSON list, each element of this list represents a phrase you have\
written in some chat).\n\
\n\
NOTE: private information may be leaked.",\
formatter_class=argparse.RawTextHelpFormatter)
	ap.add_argument("json_file", help="The JSON input file")
	ap.add_argument("-s", "--seed", default=None, type=int, help=\
			"A random seed to input to the random number generator.")
	ap.add_argument("-i", "--info", default=False, action="store_true",\
			help="Gives some informational output.")
	args = ap.parse_args()
	main(args)
