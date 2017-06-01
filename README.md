# Introduction
I wanted to benchmark the `total_word_feature_extractor.dat` that I had trained using [MITIE](https://github.com/mit-nlp/MITIE). In order to do so, I decided to benchmark it on the [CoNLL2003 Dutch NER task](http://www.cnts.ua.ac.be/conll2003/ner/). These files read in the CoNLL training sets, and convert them to a format useable by [Rasa NLU](https://github.com/RasaHQ/rasa_nlu). Subsequently, I trained a model in Rasa, and ran it on the test set. I achieved equivalent performance to the CoNLL 2003 winners.

# Components
## `readlines.py`
Parses the CoNLL data format, and converts it normal sentences, output in `lines_output.json`. Use this to get a better overview of the data in the CoNLL files.
## `main.py`
Reads the CoNLL training file and converts it to a JSON format, output in `traindata.json`. This format is readable by RASA NLU. The file can then be used to train a model with Rasa NLU, and subsequently test it on the test-sets. 