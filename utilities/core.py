
temp_methods = {
    'upper': lambda x: x.upper(),
    'lower': lambda x: x.lower(),
    'reverse': lambda x: x[::-1],
    'reverseLines': lambda x: '\n'.join(x.split('\n')[::-1]),
    'calcExec': lambda x: eval(x),
    # 'password': lambda x: generate_secure_password()
}

def get_available_methods(**filters) -> list[str]:
    return ['core:' + x for x in temp_methods.keys()]


def get_refactor_fn(method:str):
    method = method[5:]

    if method not in temp_methods:
        return None
    
    return temp_methods[method]


def load_plugin():
    # TODO
    pass