# assembler/parser.py

def parse_line(line):
    """
    Parses a line of assembly code.
    Returns a tuple: (label, opcode, operands)
    """
    # Remove comments and trim whitespace
    line = line.split('#')[0].strip()
    if not line:
        return None, None, None

    label = None
    if ':' in line:
        label, line = line.split(':', 1)
        label = label.strip()

    parts = line.strip().split()
    if not parts:
        return label, None, None

    opcode = parts[0]
    # Assume operands are comma-separated
    operands = [operand.strip() for operand in ' '.join(parts[1:]).split(',') if operand.strip()]
    return label, opcode, operands

def parse_file(filepath):
    """
    Parses an assembly source file and returns a list of instruction tuples.
    Each tuple: (line_number, label, opcode, operands)
    """
    instructions = []
    with open(filepath, 'r') as f:
        for i, line in enumerate(f):
            label, opcode, operands = parse_line(line)
            if opcode:  # Skip empty lines
                instructions.append((i + 1, label, opcode, operands))
    return instructions
