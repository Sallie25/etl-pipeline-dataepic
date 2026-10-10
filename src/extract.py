import json


def read_records(path):
    with open(path,encoding='utf-8') as f: return json.load(f)
def make_batches(records,size):
    return [records[i:i+size] for i in range(0,len(records),size)]
