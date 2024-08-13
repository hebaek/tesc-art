import logging
import sys
import re



commands = [
    'quit',
    'start', 'stop', 'reset',
    'on', 'off', 'toggle', 'random',
    'set', 'read', 'react',
    'add', 'sub', 'inc', 'dec',
]

comparators = [
    '==', '!=', '<=', '>=', '<', '>',
    'IN', '!IN',
]



logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)



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
        logger.error(f'Could not open file "{filename}"')

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



def load_events(lines):
    data = {
        'variables':  {},
        'interrupts': [],
        'schedule':   [],
        'chains':     {},
    }

    context = None
    chain   = None

    for line in lines:
        line = line.strip()
        words = [word.strip() for word in line.split()]


        if line == 'variables:':
            context = 'variables'

        elif line == 'interrupts:':
            context = 'interrupts'

        elif line == 'schedule:':
            context = 'schedule'

        elif words[0] == 'chain:':
            context = 'chain'
            chain = words[1]
            data['chains'][chain] = []

        elif context == 'variables':
            cmdindex = None
            for i in range(0, len(words)):
                if words[i] in commands: cmdindex = i

            if cmdindex != 3:
                logger.error(f'Error in variable definition: {line}')
                continue

            name   = words[0] if len(words) > 0 else None
            comp   = words[1] if len(words) > 1 else None
            value  = words[2] if len(words) > 2 else None
            cmd    = words[3] if len(words) > 3 else None
            target = words[4] if len(words) > 4 else None
            params = words[5] if len(words) > 5 else None

            if comp not in comparators:
                logger.error(f'Error in variable definition: {line}')
                continue

            if name and comp and value and cmd:
                if not name in data['variables']: data['variables'][name] = []
                data['variables'][name].append({ 'comp': comp, 'value': value, 'cmd': cmd, 'target': target, 'params': params })

        elif context == 'interrupts':
            cmdindex = None
            for i in range(0, len(words)):
                if words[i] in commands: cmdindex = i

            if cmdindex != 1:
                logger.error(f'Error in interrupt definition: {line}')
                continue

            name   = words[0] if len(words) > 0 else None
            cmd    = words[1] if len(words) > 1 else None
            target = words[2] if len(words) > 2 else None
            params = words[3] if len(words) > 3 else None

            if name and cmd:
                data['interrupts'].append({ 'name': name, 'cmd': cmd, 'target': target, 'params': params })

        elif context == 'schedule':
            cmdindex = None
            for i in range(0, len(words)):
                if words[i] in commands: cmdindex = i

            if cmdindex != 1:
                logger.error(f'Error in schedule definition: {line}')
                continue

            timestring = words[0] if len(words) > 0 else None
            cmd        = words[1] if len(words) > 1 else None
            target     = words[2] if len(words) > 2 else None
            params     = words[3] if len(words) > 3 else None

            if timestring:
                time = parse_timestring(timestring)

            if time and cmd:
                data['schedule'].append({ 'time': time, 'cmd': cmd, 'target': target, 'params': params })

        elif context == 'chain' and chain:
            cmdindex = None
            for i in range(0, len(words)):
                if words[i] in commands: cmdindex = i

            if cmdindex > 2:
                logger.error(f'Error in event definition for chain {chain}: {line}')
                continue

            if cmdindex == 1: words.insert(1, '')
            if cmdindex == 0: words = ['', ''] + words

            words = words + [None, None, None, None, None][len(words):]

            delaystring  = words[0] if len(words) > 0 else None
            randomstring = words[1] if len(words) > 1 else None
            cmd          = words[2] if len(words) > 2 else None
            target       = words[3] if len(words) > 3 else None
            params       = words[4] if len(words) > 4 else None

            delay = parse_delaystring(delaystring)
            random = parse_delaystring(randomstring)

            if delay and cmd:
                data['chains'][chain].append({ 'delay': delay, 'random': random, 'cmd': cmd, 'target': target, 'params': params })

    return data



def parse_timestring(timestring):
    result = {}

    if timestring == 'boot':
        result['type'] = 'boot'

    elif timestring.find('/') == -1:
        parts = timestring.split(':')
        if len(parts) != 3: return result

        result['hour'  ] = None
        result['minute'] = None
        result['second'] = None

        if re.fullmatch('[01][0-9]|[2][0-3]', parts[0]): result['hour'  ] = int(parts[0])
        if re.fullmatch('[0-5][0-9]',         parts[1]): result['minute'] = int(parts[1])
        if re.fullmatch('[0-5][0-9]',         parts[2]): result['second'] = int(parts[2])

        result['type'] = 'time'

    elif re.match('mondays|tuesdays|wednesdays|thursdays|fridays|saturdays|sundays', timestring):
        parts = timestring.split('/')
        result.update(parse_timestring(parts[1]))
        result['weekday'] = parts[0]
        result['type'] = 'weekday'

    else:
        parts = timestring.split('/')
        result.update(parse_timestring(parts[1]))

        parts = parts[0].split('-')
        if len(parts) != 3: return result

        result['year' ] = None
        result['month'] = None
        result['day'  ] = None

        if re.fullmatch('[2][0-9]{3}',        parts[0]): result['year' ] = int(parts[0])
        if re.fullmatch('[0][0-9]|[1][0-2]',  parts[1]): result['month'] = int(parts[1])
        if re.fullmatch('[0-2][0-9]|[3][01]', parts[2]): result['day'  ] = int(parts[2])

        result['type'] = 'date'

    return result



def parse_delaystring(delaystring):
    result = {}

    p = len(list(filter(lambda x: x == '.', delaystring)))
    k = len(list(filter(lambda x: x == ':', delaystring)))

    temp = ':'*(3-k) + delaystring + '.'*(1-p)
    (left, u) = temp.split('.')
    values = [int(x.rjust(2, '0')) for x in left.split(':')]
    values.append(int(u.ljust(6, '0')))

    keys = ['days', 'hours', 'minutes', 'seconds', 'microseconds']
    result = dict(zip(keys, values))

    return result



def read_file(filename):
    result = []
    linenum = 0

    try:
        with open(filename) as f:
            filedata = f.read()
            for line in filedata.split('\n'):
                linenum += 1
                line = line.strip()
                if len(line) == 0 or line[0] == '#': continue

                inline_comment = line.find('#')
                string = line if inline_comment == -1 else line[:inline_comment]
                words = [word.strip() for word in line.split()]

                result.append({ 'line': linenum, 'words': words })

    except:
        logger.error(f'Could not open file "{filename}"')

    return result



def parse_events_file(lines):
    commands = [
        'quit',
        'start', 'stop', 'reset',
        'on', 'off', 'toggle', 'random',
        'set', 'read', 'react',
        'add', 'sub', 'inc', 'dec',
    ]

    comparators = [
        '==', '!=', '<=', '>=', '<', '>',
        'IN', '!IN',
    ]



    result  = []
    context = None
    chain   = None

    for line in lines:
        linenum = line['line']
        words   = line['words']

        cmdindex = None
        for i in range(0, len(words)):
            if words[i] in commands: cmdindex = i

        if   words    == ['variables:' ]: context = 'variables'
        elif words    == ['interrupts:']: context = 'interrupts'
        elif words    == ['schedule:'  ]: context = 'schedule'
        elif words[0] == 'chain:':        context = 'chain'; chain = words[1]

        elif context == 'variables':
            if len(words) < 6: words = words + [None, None, None, None, None, None]
            if cmdindex == -1:              badline(line, 'no command'        ); continue
            if words[1] not in comparators: badline(line, 'invalid comparator'); continue
            if words[3] not in commands:    badline(line, 'invalid command'   ); continue

            result.append({ 'variable': {
                'name':   words[0],
                'comp':   words[1],
                'value':  words[2],
                'cmd':    words[3],
                'target': words[4],
                'params': words[5],
            }})

        elif context == 'interrupts':
            if len(words) < 4: words = words + [None, None, None, None]
            if cmdindex == -1:           badline(line, 'no command'     ); continue
            if words[1] not in commands: badline(line, 'invalid command'); continue

            result.append({ 'interrupt': {
                'name':   words[0],
                'cmd':    words[1],
                'target': words[2],
                'params': words[3],
            }})

        elif context == 'schedule':
            if len(words) < 4: words = words + [None, None, None, None]
            if cmdindex == -1:           badline(line, 'no command'     ); continue
            if words[1] not in commands: badline(line, 'invalid command'); continue

            result.append({ 'schedule': {
                'name':   words[0],
                'cmd':    words[1],
                'target': words[2],
                'params': words[3],
            }})

        elif context == 'chain':
            if len(words) < 5: words = words + [None, None, None, None, None]
            if cmdindex == -1: badline(line, 'no command'); continue
            if cmdindex == 0: words = [None, None] + words
            if cmdindex == 1: words = [words[0]] + [None] + words[1:]
            if words[2] not in commands: badline(line, 'invalid command'); continue

            result.append({ 'chain': {
                'chain':  chain,
                'delay':  words[0],
                'random': words[1],
                'cmd':    words[2],
                'target': words[3],
                'params': words[4],
            }})

    return result



def badline(line, reason):
    logger.error(f'{reason} in line {line["line"]}: "{" ".join(line["words"])}"')



if __name__ == '__main__':
    lines = read_file('data/events-example.txt')
    data  = parse_events_file(lines)

    for line in data:
        print(line)
