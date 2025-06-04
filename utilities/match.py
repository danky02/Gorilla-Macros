

def check_match(string:str, match:str) -> str|None:

    target = tuple(zip(string.upper(), string))

    match = match.upper()

    if not match:
        return string

    if len(match) > len(string):
        return None

    target_iter = iter(target)

    result = ""

    try:
        for m in match:
            t, ch = next(target_iter)
            while t != m:
                result += ch
                t, ch = next(target_iter)
            result += "*%s*" % ch
    except StopIteration:
        return None
    
    # match found
    try:
        while True:
            _, ch = next(target_iter)
            result += ch
    except StopIteration:
        pass

    return result.replace("**", '')


def filter_list_by_match(list:list[str], match:str):
    return [m for x in list if (m := check_match(x, match))]


if __name__ == '__main__':
    dataset = [
        "GetElementById",
        "GetElementsByClassName",
        "GetElementsByTags",
    ]

    target_search = "GetsBy"

    result = '\n'.join(filter_list_by_match(dataset, target_search))
    print(result)

