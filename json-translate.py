from multiprocessing import Process, Pool, cpu_count, Value, Manager
from deep_translator import GoogleTranslator
from flatten_json import flatten, unflatten_list
from itertools import islice, chain
from functools import partial
import json 
from sys import argv


import copy

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

def tranlate(orgin, target, src, dest, batch):
    global progress
    translations = []
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
        for phrase in translator.translate(value_data).split('\n'):
            translations.append(phrase)

    for pair, translated in zip(orgin.items(), translations):
        target[pair[0]] = str(translated)
    with progress.get_lock():
        progress.value += 1
        print("Translation Progress: {} / {} Completed".format(progress.value, batch))
    

with open(argv[1]) as input:
    data = json.load(input)
    manager = Manager()
    # lock = manager.Lock()
    progress = Value('i', 0)
    flatten_data = manager.dict(flatten(data, '#'))
    chunk_data_set = split_dict_to_multiple(flatten_data, 64)
    cpus = cpu_count()
    pool = Pool(cpus)
    multi_translate = partial(tranlate,target = flatten_data, src = 'en', dest = argv[3], batch=len(chunk_data_set))
    pool.map(multi_translate, chunk_data_set)

translated_json = unflatten_list(flatten_data.copy(), '#')

with open(argv[2], 'w+') as output:
    json.dump(translated_json, output, indent=4, ensure_ascii=False)

input.close()
output.close()