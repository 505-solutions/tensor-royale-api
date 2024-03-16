

def debug_json(json):
    d = {}
    for key in json:
        value = str(json[key])
        i = 0
        for char in value:
            i += 1
            i *= ord(char)
        i %= 10**9
        d[key] = i
    return d