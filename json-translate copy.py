# from multiprocessing import Process, Pool, cpu_count
from deep_translator import GoogleTranslator
from flatten_json import flatten, unflatten_list
from itertools import islice, chain
# from functools import partial
import json 
from sys import argv


import copy

progress

def split_dict_to_multiple(input_dict, max_limit=200):
    """Splits dict into multiple dicts with given maximum size. 
    Returns a list of dictionaries."""
    chunks = []
    curr_dict ={}
    for k, v in input_dict.items():
        if len(curr_dict.keys()) < max_limit:
            curr_dict.update({k: v})
        else:
            chunks.append(copy.deepcopy(curr_dict))
            curr_dict = {k: v}
    # update last curr_dict
    chunks.append(curr_dict)
    return chunks

def tranlate(orgin, src, dest):
    translated = []
    value_data_list = []
    tmp = ""
    value_data_list.append(tmp)
    for key, value in orgin.items():
        batch_num = 0
        if len(value_data_list[batch_num]) <= 4500:
            value_data_list[batch_num] = value_data_list[batch_num] + '\n' + value
        else:
            tmp = ""
            value_data_list.append(tmp)
            batch_num = batch_num + 1

    translator = GoogleTranslator(source=src, target=dest)
    for value_data in value_data_list:
        translated.append(translator.translate(value_data).split('\n'))
    return list(chain.from_iterable(translated))

with open(argv[1]) as input:
    global progress
    data = json.load(input)
    flatten_data = flatten(data, '#')

    chunk_data_set = split_dict_to_multiple(flatten_data, 64)
    progress = 0
    # cpus = cpu_count()
    # pool = Pool(cpus)
    # print("Cpus: {}".format(cpus))
    # multi_translate = partial(tranlate, src = 'en', dest = argv[4])
    # pool_outputs = pool.map(tranlate, chunk_data_set)

    for set in chunk_data_set:
        print("Translation Progress: {} / {}".format(progress, len(list(chunk_data_set)) - 1))
        translations = tranlate(set, 'en', str(argv[3]))
        print(translations)
        for pair, translated in zip(set.items(), translations):
            flatten_data[pair[0]] = str(translated)
        progress = progress + 1
        

    translated_json = unflatten_list(flatten_data, '#')

with open(argv[2], 'w+') as output:
    json.dump(translated_json, output, indent=4, ensure_ascii=False)

input.close()
output.close()

