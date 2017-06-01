import json

loop_dict = dict()
new_entity = dict()
counter = 0
open_quote = False
loop_dict[counter] = dict()
loop_dict[counter]['text'] = ''
loop_dict[counter]['intent'] = 'NL'
loop_dict[counter]['entities'] = list()


final_dict = dict()
final_dict['rasa_nlu_data'] = dict()
final_dict['rasa_nlu_data']['entity_examples'] = list()
final_dict['rasa_nlu_data']['intent_examples'] = list()
entity_examples = final_dict['rasa_nlu_data']['entity_examples']
intent_examples = final_dict['rasa_nlu_data']['intent_examples']

with open('ned.train', 'r', encoding='latin1') as trainfile:
	for index, line in enumerate(trainfile):
		line = line.replace("\n", "")
		if(line != ' ' and line != ''):
			split_line = line.split()

			word = split_line[0]
			entity = split_line[2]

			# Add to entities if it's tagged like that
			if(entity != 'O'):
				try: 
					entity = entity.split('-')[1]
				except:
					print("entity was: " + entity)
					print("line was: " + line)
					break
				if(not new_entity): # Entity dict is empty
					new_entity['start'] = len(loop_dict[counter]['text'])
					new_entity['end'] = new_entity['start'] + len(word)
					new_entity['value'] = word
					new_entity['entity'] = entity
					
				else: # Dict is not empty, we are checking if we should add the new entity to the current one, or start a new one
					if(new_entity['entity'] == entity): # They're of the same type, so should be together in one entity
						new_entity['end'] = new_entity['end'] + len(word) + 1 # + 1 because adding space
						new_entity['value'] = new_entity['value'] + " " + word
					else: # Not the same, so append entity, and start new one
						loop_dict[counter]['entities'].append(new_entity)
						if(len(loop_dict[counter]['entities']) > 1):
							number_of_entities = len(loop_dict[counter]['entities'])
							number_1 = loop_dict[counter]['entities'][number_of_entities - 2]['end']
							number_2 = loop_dict[counter]['entities'][number_of_entities - 1]['start']

							if(number_2 <= number_1):
								print('Overlap found! Colliding entities: ')
								print(loop_dict[counter]['entities'][number_of_entities - 2]['value'])
								print(loop_dict[counter]['entities'][number_of_entities - 1]['value'])

						with open('muhentities.txt', 'a') as outputfile:
							outputfile.write(new_entity['value'] + "+++" + new_entity['entity'] + "\n")
						new_entity = dict()
						new_entity['start'] = len(loop_dict[counter]['text'])
						new_entity['end'] = new_entity['start'] + len(word)
						new_entity['value'] = word
						new_entity['entity'] = entity

			elif(entity == 'O' and new_entity): # The next word is not an entity, but we still have an open entity that isn't saved yet
					loop_dict[counter]['entities'].append(new_entity)
					if(len(loop_dict[counter]['entities']) > 1):
						number_of_entities = len(loop_dict[counter]['entities'])
						number_1 = loop_dict[counter]['entities'][number_of_entities - 2]['end']
						number_2 = loop_dict[counter]['entities'][number_of_entities - 1]['start']

						if(number_2 <= number_1):
							print('Overlap found! Colliding entities: ')
							print(loop_dict[counter]['entities'][number_of_entities - 2]['value'])
							print(loop_dict[counter]['entities'][number_of_entities - 1]['value'])

					with open('muhentities.txt', 'a') as outputfile:
						outputfile.write(new_entity['value'] + "+++" + new_entity['entity'] + "\n")
					new_entity = dict()

			# Append word to sentence, i.e. ['text'] part of this dict
			if('.' == word ):
				loop_dict[counter]['text'] = loop_dict[counter]['text'][:-1]
				loop_dict[counter]['text'] += word

			elif (',' == word or ')' == word):
				loop_dict[counter]['text'] = loop_dict[counter]['text'][:-1]
				loop_dict[counter]['text'] += word + " "

			elif ('(' == word ):
				loop_dict[counter]['text'] += word

			elif("'" == word or '"' == word):
				if(open_quote == True):
					open_quote = False
					loop_dict[counter]['text'] = loop_dict[counter]['text'][:-1]
					loop_dict[counter]['text'] += word + " "
				else:
					open_quote = True
					loop_dict[counter]['text'] += word + " "
			else:
				loop_dict[counter]['text'] += word + " "

		# Reached a newline
		else:
			if(new_entity): # If we reached the end of the line with an entity, we need to append it correctly
				loop_dict[counter]['entities'].append(new_entity)
				if(len(loop_dict[counter]['entities']) > 1):
					number_of_entities = len(loop_dict[counter]['entities'])
					number_1 = loop_dict[counter]['entities'][number_of_entities - 2]['end']
					number_2 = loop_dict[counter]['entities'][number_of_entities - 1]['start']

					if(number_2 <= number_1):
						print('Overlap found! Colliding entities: ')
						print(loop_dict[counter]['entities'][number_of_entities - 2]['value'])
						print(loop_dict[counter]['entities'][number_of_entities - 1]['value'])

				with open('muhentities.txt', 'a') as outputfile:
						outputfile.write(new_entity['value'] + "+++" + new_entity['entity'] + "\n")
				new_entity = dict()

			entity_examples.append(loop_dict[counter].copy())
			loop_dict[counter].pop('entities', None)
			intent_examples.append(loop_dict[counter])

			counter = counter + 1

			open_quote = False
			loop_dict[counter] = dict()
			loop_dict[counter]['text'] = ''
			loop_dict[counter]['intent'] = 'NL'
			loop_dict[counter]['entities'] = list()

with open('traindata.json', 'w') as outputfile:
	output = json.dumps(final_dict, indent=4)
	outputfile.write(output)
