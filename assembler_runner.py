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

def run_assembler(code_text, labels=None):
    """
    Assemble the code with optional label resolution
    """
    try:
        # Clean and normalize the code
        if isinstance(code_text, list):
            instructions = code_text
        else:
            instructions = [line.strip() for line in code_text.split('\n') if line.strip()]
        
        # Process each instruction
        machine_codes = []
        current_address = 0
        
        for instr in instructions:
            # Skip comments and empty lines
            if not instr or instr.startswith(';'):
                continue
                
            # Remove label if present in instruction
            if ':' in instr:
                instr = instr.split(':', 1)[1].strip()
                if not instr:
                    continue
            
            # Parse instruction and encode
            tokens = instr.split()
            opcode = tokens[0].upper()
            operands = tokens[1:] if len(tokens) > 1 else []
            
            # Encode the instruction
            machine_code = encoder.encode_instruction(opcode, operands, labels, current_address)
            machine_codes.append(machine_code)
            current_address += 4
            
        return machine_codes
        
    except Exception as e:
        raise Exception(f"Assembly error: {str(e)}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        code_file = sys.argv[1]
        machine_codes = assemble(code_file)
        for code in machine_codes:
            print(f"{code:032b}")
    else:
        print("Usage: python assembler_runner.py <assembly_file>")
