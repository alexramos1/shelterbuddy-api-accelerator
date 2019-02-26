import json

f = open("animals.json", "r")
data = json.loads(f.read())

def gen_dict_extract(var, key):
    if isinstance(var, dict):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, (dict, list)):
                yield from gen_dict_extract(v, key)
    elif isinstance(var, list):
        for d in var:
            yield from gen_dict_extract(d, key)

for i in gen_dict_extract(data, 'Uri'):
    print(i)

