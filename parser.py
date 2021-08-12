import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | VP NP | S Conj S | NP VP Conj VP
AP -> V | V NP | V PP | Adv VP | VP Adv
NP -> N | Det N | NP PP | Det AdjP N
PP -> P NP | P S
AdjP -> Adj | Adj AdjP
VP -> V | V NP | V NP PP | V PP | VP Adv | Adv VP
"""


grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)
    print(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    sentence = sentence.lower()
    sentence = sentence.replace('.', '')
    sentence = nltk.word_tokenize(sentence)
    final = []
    for pos in range(0, len(sentence)):
        try:
            int(sentence[pos])
        except:
            final.append(sentence[pos])
    return final

def np_chunk(tree):
    nounphrase = []
    for ele in tree:
        if ele.label == 'NP':
            nounphrase.append(ele)
    return nounphrase


if __name__ == "__main__":
    main()
