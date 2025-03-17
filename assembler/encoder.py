# assembler/encoder.py

from utils.bin_utils import register_to_bin, imm_to_bin

# Opcode mapping with lowercase keys
OPCODES = {
    'add': '00000', 'sub': '00001', 'mul': '00010', 'div': '00011',
    'mod': '00100', 'cmp': '00101', 'and': '00110', 'or': '00111',
    'not': '01000', 'mov': '01001', 'lsl': '01010', 'lsr': '01011',
    'asr': '01100', 'nop': '01101', 'ld': '01110', 'st': '01111',
    'beq': '10000', 'bgt': '10001', 'b': '10010', 'call': '10011',
    'ret': '10100', 'hlt': '11111'
}

def encode_instruction(opcode, operands, labels, pc):
    """
    Encodes assembly instructions into machine code.
    """
    instruction = 0
    opcode = opcode.lower()
    operands = [op.strip().rstrip(',').strip().lower() for op in operands]

    try:
        instruction |= int(OPCODES[opcode], 2) << 27

        if opcode == 'mov':
            rd = int(operands[0].strip('r'))
            instruction |= 1 << 26          # Set I bit
            instruction |= (rd & 0xF) << 22 # RD field
            imm = int(operands[1].strip('#'))
            instruction |= imm & 0x3FFFF    # Immediate value

        elif opcode == 'cmp':
            rd = int(operands[0].strip('r'))
            instruction |= 1 << 26          # Set I bit
            instruction |= (rd & 0xF) << 18 # RS1 field
            if operands[1].startswith('r'):
                rs2 = int(operands[1].strip('r'))
                instruction |= (rs2 & 0xF) << 14
            else:
                imm = int(operands[1].strip('#'))
                instruction |= imm & 0x3FFFF

        elif opcode in ['bgt', 'b']:
            offset = (labels[operands[0]] - pc - 4) // 4
            instruction |= offset & 0x3FFFF  # Offset field

        elif opcode in ['add', 'sub']:
            rd = int(operands[0].strip('r'))
            rs1 = int(operands[1].strip('r'))
            instruction |= (rd & 0xF) << 22  # RD field
            instruction |= (rs1 & 0xF) << 18 # RS1 field
            if operands[2].startswith('#'):
                instruction |= 1 << 26       # Set I bit
                imm = int(operands[2].strip('#'))
                instruction |= imm & 0x3FFFF
            else:
                rs2 = int(operands[2].strip('r'))
                instruction |= (rs2 & 0xF) << 14

        elif opcode == 'nop':
            instruction |= 0  # No operation, opcode already set

        return instruction
    except Exception as e:
        raise ValueError(f"Error encoding {opcode} {operands}: {str(e)}")