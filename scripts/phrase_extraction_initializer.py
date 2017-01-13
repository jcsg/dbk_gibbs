# Python 3.5
from collections import defaultdict as dd
import sys

def initial_phrase_extraction(srctext,trgtext,berkeley_alignment):

	srclen = len(srctext.split())
	trglen = len(trgtext.split())

	f_aligned = set()
	e_aligned = set()

	alignment = list()

	b_a_lst = berkeley_alignment.split()
	for pair in b_a_lst:
	    [f, e] = pair.split("-")
	    f_aligned.add(int(f))
	    e_aligned.add(int(e))
	    alignment.append((int(f),int(e)))

	alignment = sorted(alignment)

	phrase_set = set()
	phrase = set()
	prev_e = 0
	prev_f = 0
	for f,e in alignment:
	    if abs(e - prev_e) > 1:
	        phrase_set.add(frozenset(phrase))
	        phrase = set([(e,f)])
	    if abs(f - prev_f) > 1:
	        phrase_set.add(frozenset(phrase))
	        phrase = set([(e,f)])
	    else:
	        phrase.add((e,f))
	    prev_e = e
	    prev_f = f
	phrase_set.add(frozenset(phrase))

	return phrase_set

if __name__ == "__main__":
	srctext = sys.argv[1]
	trgtext = sys.argv[2]
	berkeley_alignment = sys.argv[3]
	phrase_set = initial_phrase_extraction(srctext,trgtext,berkeley_alignment)
	for phrase in sorted(phrase_set):
		print(sorted(phrase))
