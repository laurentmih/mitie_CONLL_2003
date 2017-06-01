import json

loop_list = list()
counter = 0
open_quote = False
loop_list.append('')

with open('ned.testa', 'r', encoding='latin1') as trainfile:
	for index, line in enumerate(trainfile):
		line = line.replace("\n", "")
		if(line != ' ' and line != ''):
			split_line = line.split()

			word = split_line[0]


			# Append word to sentence, i.e. ['text'] part of this dict
			if('.' in word ):
				loop_list[counter] = loop_list[counter][:-1]
				loop_list[counter] += word

			elif (',' == word or ')' == word):
				loop_list[counter] = loop_list[counter][:-1]
				loop_list[counter] += word + " "

			elif ('(' == word ):
				loop_list[counter] += word

			elif("'" == word or '"' == word):
				if(open_quote == True):
					open_quote = False
					loop_list[counter] = loop_list[counter][:-1]
					loop_list[counter] += word + " "
				else:
					open_quote = True
					loop_list[counter] += word
			else:
				loop_list[counter] += word + " "

		else:
			counter = counter + 1
			loop_list.append('')


with open('lines_output.txt', 'w') as outputfile:
	for lines in loop_list:
		outputfile.write(str(lines) + "\n")
