# main.py

import sys
from assembler import parser, symbol_table, encoder

def first_pass(instructions):
    """
    Build the symbol table by recording labels with their corresponding addresses.
    """
    symtab = symbol_table.SymbolTable()
    pc = 0
    for line_num, label, opcode, operands in instructions:
        if label:
            symtab.add_label(label, pc)
        pc += 4  # each instruction is 4 bytes
    return symtab

def second_pass(instructions, symtab):
    """
    Encode instructions into machine code.
    """
    machine_codes = []
    pc = 0
    for line_num, label, opcode, operands in instructions:
        code = encoder.encode_instruction(opcode, operands, symtab, pc)
        machine_codes.append(code)
        pc += 4
    return machine_codes

def assemble(filepath):
    instructions = parser.parse_file(filepath)
    symtab = first_pass(instructions)
    machine_codes = second_pass(instructions, symtab)
    return machine_codes

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python main.py <assembly_file.sr>")
        sys.exit(1)
    assembly_file = sys.argv[1]
    machine_codes = assemble(assembly_file)
    for code in machine_codes:
        print(f"{code:032b}")  # print as 32-bit binary string
