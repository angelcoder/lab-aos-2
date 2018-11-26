# Created on Oct 20 2018 by Anhelina Lohvina

# global constants, built-in settings of processor
register_size = 12
byte_size = 8

# all our registers
Memory = {
          'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0,
          'IR': ' ',     # string of current command
          'PS': '+',     # sign of current result
          'PC': 0,       # count of commands
          'TC': 0,       # current tact: 1 or 2
         }

def do_operation():
    operands = Memory["IR"].split()

    val1_is_negative = 1
    val2_is_negative = 1

    if '-' in operands[2] or operands[2].isnumeric():                # operand is number that maybe is negative
        if '-' in operands[2]:                                       # negative
            val1_is_negative = -1
        val1 = int(operands[2].replace('-', '')) * val1_is_negative
    else:                                                            # operand is register
        val1 = Memory[operands[2]]

    if '-' in operands[3] or operands[3].isnumeric():                # operand is number that maybe is negative
        if '-' in operands[3]:                                       # negative
            val2_is_negative = -1
        val2 = int(operands[3].replace('-', '')) * val2_is_negative
    else:                                                            # operand is register
        val2 = Memory[operands[3]]

    if operands[0] == "addition":
        Memory[operands[1]] = val1 + val2
    elif operands[0] == "subtraction":
        Memory[operands[1]] = val1 - val2
    elif operands[0] == "multiplying":
        Memory[operands[1]] = val1 * val2
    elif operands[0] == "division":
        if val2 == 0:
            raise ValueError()
        Memory[operands[1]] = val1 // val2

    if abs(Memory[operands[1]]) > 2048:        # maximum value for a 12-bit integer numbers
        raise ValueError()                     # (including negative) is 2^(11)

    Memory['PS'] = '+' if Memory[operands[1]] >= 0 else '-'


def to_bin(num):                               # returns string of a number in base 2
    s = ''
    for _ in range(register_size):
        s = str(num % 2) + s
        num //= 2
    return s


def print_info():
    print('IR:', Memory['IR'])
    print('R1',  to_bin(Memory['R1']), 'R2',  to_bin(Memory['R2']), sep='\t', end='')
    print('   ', end='')
    print('R3',  to_bin(Memory['R3']), 'R4',  to_bin(Memory['R4']), sep='\t')
    print('PS:', Memory['PS'], 'PC:', Memory['PC'], 'TC:', Memory['TC'], sep='\t')

    input('')


def read():
    fin = open('inputA.txt')
    for line in fin:
        Memory['IR'] = line.strip()
        Memory['TC'] = 1      #current tact
        Memory['PC'] += 1
        print_info()          # first tact
        do_operation()
        Memory['TC'] = 2
        print_info()          # second tact

# driver program
if __name__ == '__main__':
    try:
        print('***************************************************************************************')
        print('IMPORTANT: press "enter" on a keyboard to go to the next tact, each command has 2 tacts')
        print('')
        read()
    except ValueError:
        print(ValueError.__doc__)
