def parse_file(filename):
    result = []

    try:
        with open(filename) as f:
            filedata = f.read()
            for line in filedata.split('\n'):
                line = line.strip()
                if len(line) == 0 or line[0] == '#': continue

                inline_comment = line.find('#')
                string = line if inline_comment == -1 else line[:inline_comment]

                result.append(string.strip())

    except:
        pass

    return result



def load_config(lines):
    conf = {}

    for line in lines:
        whitespace = line.find(' ')
        if whitespace != -1:
            key   = line[:whitespace].strip()
            value = line[whitespace:].strip()

            conf[key] = value

    return conf
