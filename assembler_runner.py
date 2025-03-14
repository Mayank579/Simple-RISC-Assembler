# assembler_runner.py
import sys
import tempfile
from assembler import parser, symbol_table, encoder

def first_pass(instructions):
    symtab = symbol_table.SymbolTable()
    pc = 0
    for line_num, label, opcode, operands in instructions:
        if label:
            symtab.add_label(label, pc)
        pc += 4  # each instruction is 4 bytes
    return symtab

def second_pass(instructions, symtab):
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

def run_assembler(code_text):
    # Write the provided code to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".sr") as tmp:
        tmp.write(code_text.encode("utf-8"))
        tmp.flush()
        machine_codes = assemble(tmp.name)
    return machine_codes

if __name__ == '__main__':
    if len(sys.argv) > 1:
        code_file = sys.argv[1]
        machine_codes = assemble(code_file)
        for code in machine_codes:
            print(f"{code:032b}")
    else:
        print("Usage: python assembler_runner.py <assembly_file>")
