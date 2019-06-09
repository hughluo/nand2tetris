# d1 d2 d3
dest_dict = {
    'null': '000',
    'M'   : '001',
    'D'   : '010',
    'MD'  : '011',
    'A'   : '100',
    'AM'  : '101',
    'AD'  : '110',
    'AMD' : '111',
}

# j1 j2 j3
jump_dict = {
    'null': '000',
    'JGT' : '001',
    'JEQ' : '010',
    'JGE' : '011',
    'JLT' : '100',
    'JNE' : '101',
    'JLE' : '110',
    'JMP' : '111',
}

# a c1 c2 c3 c4 c5 c6
comp_dict = {
    '0'  : '0101010',
    '1'  : '0111111',
    '-1' : '0111010',
    'D'  : '0001100',
    'A'  : '0110000',
    'M'  : '1110000',
    '!D' : '0001101',
    '!A' : '0110001',
    '!M' : '1110001',
    '-D' : '0001111',
    '-A' : '0110011',
    '-M' : '1110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'M+1': '1110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'M-1': '1110010',
    'D+A': '0000010',
    'D+M': '1000010',
    'D-A': '0010011',
    'D-M': '1010011',
    'A-D': '0000111',
    'M-D': '1000111',
    'D&A': '0000000',
    'D&M': '1000000',
    'D|A': '0010101',
    'D|M': '1010101',
}

predefined_symbol_dict = {
    'SP': '0',
    'LCL': '1',
    'ARG': '2',
    'THIS': '3',
    'THAT': '4',
    'R0': '0',
    'R1': '1',
    'R2': '2',
    'R3': '3',
    'R4': '4',
    'R5': '5',
    'R6': '6',
    'R7': '7',
    'R8': '8',
    'R9': '9',
    'R10': '10',
    'R11': '11',
    'R12': '12',
    'R13': '13',
    'R14': '14',
    'R15': '15',
    'SCREEN': '16384',
    'KBD': '24576'
}


def remove_label(fin_address):
    fin = open(fin_address, 'r')
    fout_address = fin_address+'.nolabel'
    fout = open(fout_address, 'w')
    linenum = 0
    symbol_table = dict()
    for line in fin:
        # clean the comment and empty line
        line = line.strip()
        if '//' in line:
            line = line.split('//')[0]
        if len(line) == 0:
            continue
        if '(' in line:
            symbol = line.replace('(', '').replace(')','')
            symbol_table[symbol] = str(linenum)  
        else:
            fout.write(line+'\n')
            linenum += 1
    fin.close()
    fout.close()
    return symbol_table
        

def remove_variable(fin_address, symbol_table):
    fin = open(fin_address, 'r')
    fout_address = fin_address+'.novar'
    fout = open(fout_address, 'w')
    next_empty_addr = 16
    for line in fin:
        line = line.strip()
        if '@' in line:
            symbol = line[1:]
            if symbol.isdigit():
                fout.write(line+'\n')
            elif symbol in predefined_symbol_dict:
                fout.write('@'+ predefined_symbol_dict[symbol]+'\n')
            elif symbol in symbol_table:
                fout.write('@'+ symbol_table[symbol]+'\n')
            else:
                symbol_table[symbol] = str(next_empty_addr)
                fout.write('@'+ str(next_empty_addr) + '\n')
                next_empty_addr += 1

        else: # c command
            fout.write(line+'\n')

    fin.close()
    fout.close()

def convert_line(str): 
    result = ''
    if str[0] == '@':
        result+='0'
        addr = int(str[1:])
        result+= format(addr, '015b')
    else:
        # handle dest
        if '=' in str:
            dest, rest = str.split('=')
        else:
            dest = 'null'
            rest = str

        dest_code = dest_dict[dest]

        # handle jump
        if ';' in rest:
            comp, jump = rest.split(';')
        else:
            comp = rest
            jump = 'null'
        
        jump_code = jump_dict[jump]

        # handle comp
        comp_code = comp_dict[comp]
        result = '111' + comp_code + dest_code + jump_code

    return result


def convert_file_without_symbol(fin_address):
    fin = open(fin_address, 'r')
    fout_address = fin_address.split('.asm')[0] + '.hack'
    fout = open(fout_address, 'w')
    for line in fin:
        line = line.strip()
        fout.write(convert_line(line) + '\n')
    fin.close()
    fout.close()

def assemble(fin_address):
    symbol_table = remove_label(fin_address)
    remove_variable(fin_address+'.nolabel', symbol_table)
    convert_file_without_symbol(fin_address+'.nolabel.novar')


def main():
    assemble('./add/Add.asm')
    assemble('./max/Max.asm')
    assemble('./max/MaxL.asm')
    assemble('./rect/Rect.asm')
    assemble('./rect/RectL.asm')
    assemble('./pong/Pong.asm')
    assemble('./pong/PongL.asm')

if __name__ == "__main__":
    main()