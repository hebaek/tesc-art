# Public imports
import re

# Local imports
from event     import Event, ChainEvent, ScheduleEvent



def parse_value(value):
    result = {}

    # Already a number
    if type(value) == type(  int(0)): return {'type': 'value', 'value': value }
    if type(value) == type(float(0)): return {'type': 'value', 'value': value }

    # Empty string
    if value == '': return None

    # Integer
    elif re.match('^[+-]?[0-9]*$', value):
        result['type' ] = 'value'
        result['value'] = int(value)

    # Float
    elif re.match('^[+-]?[0-9]*[.][0-9]*$', value):
        result['type']  = 'value'
        result['value'] = float(value)

    # Range
    elif re.match('^[(][+-]?[0-9]*[.]?[0-9]*,[+-]?[0-9]*[.]?[0-9]*[)]$', value):
        parts = value[1:-1].split(',')
        low  = parse_value(parts[0])
        high = parse_value(parts[1])

        if low['type'] == 'value' and high['type'] == 'value':
            result['type']  = 'range'
            result['range'] = (low['value'], high['value'])

    # Variable
    elif re.match('^[A-Za-z].*$', value):
        result['type']     = 'variable'
        result['variable'] = value

    return result



class Variables():
    def __init__(self):
        self.variables = {}



    def reset(self):
        self.variables = {}



    def define(self, name, data):
        if not name in self.variables: self.variables[name] = Variable(name)
        self.variables[name].define(data)



    def add(self, name, value):
        if not name in self.variables: return

        value_analysis = parse_value(value)
        if   value_analysis['type'] == 'value':    value = value_analysis['value']
        elif value_analysis['type'] == 'variable': value = self.variables[value_analysis['variable']].get_value()

        self.variables[name].add(value)



    def sub(self, name, value):
        if not name in self.variables: return

        value_analysis = parse_value(value)
        if   value_analysis['type'] == 'value':    value = value_analysis['value']
        elif value_analysis['type'] == 'variable': value = self.variables[value_analysis['variable']].get_value()

        self.variables[name].sub(value)



    def inc(self, name):
        if not name in self.variables: return
        self.variables[name].inc()



    def dec(self, name):
        if not name in self.variables: return
        self.variables[name].dec()



    def set(self, name, value):
        if not name in self.variables: return

        value_analysis = parse_value(value)
        if   value_analysis['type'] == 'value':    value = value_analysis['value']
        elif value_analysis['type'] == 'variable': value = self.variables[value_analysis['variable']].get_value()

        self.variables[name].set(value)



    def react(self, name):
        if not name in self.variables: return

        events = []
        for test in self.variables[name].get_tests():
            value, low, high = 0, 0, 0

            if 'value' in test:
                value = test['value']

            elif 'range' in test:
                low  = test['range'][0]
                high = test['range'][1]

            elif 'variable' in test:
                if test['variable'] in self.variables:
                    variable = self.variables[test['variable']]
                    value = variable.get_value()

            if (test['comp'] == '==') and (self.variables[name].get_value() == value): events.append(test['event'])
            if (test['comp'] == '!=') and (self.variables[name].get_value() != value): events.append(test['event'])
            if (test['comp'] == '<=') and (self.variables[name].get_value() <= value): events.append(test['event'])
            if (test['comp'] == '>=') and (self.variables[name].get_value() >= value): events.append(test['event'])
            if (test['comp'] == '<' ) and (self.variables[name].get_value() <  value): events.append(test['event'])
            if (test['comp'] == '>' ) and (self.variables[name].get_value() >  value): events.append(test['event'])

            if (test['comp'] == 'IN' ):
                if (self.variables[name].get_value() > low and self.variables[name].get_value() < high):
                    events.append(test['event'])

            if (test['comp'] == '!IN' ):
                if (self.variables[name].get_value() < low or self.variables[name].get_value() > high):
                    events.append(test['event'])

        return events



class Variable():
    def __init__(self, name):
        self.name  = name
        self.value = 0
        self.tests = []



    def define(self, data):
        test = {
            'comp':   data['comp'],
            'cmd':    data['cmd'],
            'target': data['target'],
            'params': data['params'],
        }

        test['event'] = Event(test)

        value_analysis = parse_value(data['value'])
        if   value_analysis['type'] == 'value':    test['value']    = value_analysis['value']
        elif value_analysis['type'] == 'range':    test['range']    = value_analysis['range']
        elif value_analysis['type'] == 'variable': test['variable'] = value_analysis['variable']

        self.tests.append(test)



    def set(self, value): self.value  = value
    def add(self, value): self.value += value
    def sub(self, value): self.value -= value
    def inc(self):        self.value += 1
    def dec(self):        self.value -= 1

    def get_value(self):  return self.value
    def get_tests(self):  return self.tests
