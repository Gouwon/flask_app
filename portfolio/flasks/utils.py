import json, re

def string_to_dict(*args, **kwargs):
    data = args[0]
    values = [str(type(x)) for x in data.values()]
    _isdict = True if str(type(data)) == "<class 'dict'>" else False
    _haslist = True if "<class 'list'>" in values else False

    if _isdict is True and _haslist is True:
        for k in data:
            _islist = True if str(type(data[k])) == "<class 'list'>" else False
            pattern = re.compile('{')
            target = [ pattern.match(y) for y in args[0][k] ]
            _hasdict = True if target.count(None) == 0 else False
            if _islist is True and _hasdict is True:
                data[k] = list(map(lambda x : json.loads(x, encoding='utf8'), data[k]))
            else:
                pass

    return data
    