# assembler/encoder.py

from utils.bin_utils import register_to_bin, imm_to_bin

# Opcode mapping as provided in the PDF
OPCODES = {
    'add': '00000', 'sub': '00001', 'mul': '00010', 'div': '00011',
    'mod': '00100', 'cmp': '00101', 'and': '00110', 'or': '00111',
    'not': '01000', 'mov': '01001', 'lsl': '01010', 'lsr': '01011',
    'asr': '01100', 'nop': '01101', 'ld': '01110', 'st': '01111',
    'beq': '10000', 'bgt': '10001', 'b': '10010', 'call': '10011',
    'ret': '10100', 'hlt': '11111'
}

def encode_instruction(opcode, operands, symbol_table, pc):
    """
    Encodes an instruction into a 32-bit machine code integer.
    pc: current program counter (instruction address)
    """
    if opcode == 'hlt':
        return 0b11111 << 27  # 5-bit opcode then 27 zeros

    elif opcode in ['nop', 'ret']:
        return int(OPCODES[opcode], 2) << 27

    elif opcode in ['call', 'b', 'beq', 'bgt']:
        # 1-address instruction: PC-relative addressing.
        offset = (symbol_table.get_address(operands[0]) - pc) // 4
        offset_bin = imm_to_bin(offset, 27, signed=True)
        return (int(OPCODES[opcode], 2) << 27) | (offset_bin & 0x7FFFFFF)

    elif opcode in ['add', 'sub', 'mul', 'div', 'mod', 'and', 'or', 'lsl', 'lsr', 'asr']:
        # 3-address instructions (R/I-type)
        if len(operands) == 3:
            rd = register_to_bin(operands[0])
            rs1 = register_to_bin(operands[1])
            if operands[2].lower().startswith('r'):  # R-type
                rs2 = register_to_bin(operands[2])
                # R-type: opcode, 0 modifier bit, rd, rs1, rs2
                return (int(OPCODES[opcode], 2) << 27) | (0 << 26) | (rd << 22) | (rs1 << 18) | (rs2 << 14)
            else:  # I-type
                # For immediate instructions, the immediate value uses 18 bits.
                imm = imm_to_bin(operands[2], 18)
                return (int(OPCODES[opcode], 2) << 27) | (1 << 26) | (rd << 22) | (rs1 << 18) | imm

    # Add logic for 2-address instructions (cmp, not, mov) and load/store (ld, st)
    elif opcode in ['cmp', 'not', 'mov']:
        # For these instructions, the encoding is slightly different.
        # Check if the second operand is a register (R-type) or immediate (I-type).
        rd = register_to_bin(operands[0])
        if operands[1].lower().startswith('r'):
            rs2 = register_to_bin(operands[1])
            return (int(OPCODES[opcode], 2) << 27) | (0 << 26) | (rd << 22) | (rs2 << 18)
        else:
            imm = imm_to_bin(operands[1], 18)
            return (int(OPCODES[opcode], 2) << 27) | (1 << 26) | (rd << 22) | imm

    elif opcode in ['ld', 'st']:
        # Format: ld rd, imm[rs1]
        # Here we assume the operand format is: rd, immediate[rs1]
        rd = register_to_bin(operands[0])
        # Parse the second operand which is in the form imm[rs1]
        imm_part, rs1_part = operands[1].split('[')
        rs1 = register_to_bin(rs1_part[:-1])  # remove trailing ']'
        # For simplicity, assume the third 4-bit field (rs2/imm) is the immediate part if small enough
        imm_val = imm_to_bin(imm_part, 4)
        return (int(OPCODES[opcode], 2) << 27) | (rd << 23) | (rs1 << 19) | imm_val

    else:
        raise ValueError(f"Unknown opcode: {opcode}")
