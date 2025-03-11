# utils/bin_utils.py

def register_to_bin(reg):
    """
    Convert register name (e.g., 'r3') to a 4-bit binary integer.
    """
    if reg.lower().startswith('r'):
        num = int(reg[1:])
        if 0 <= num < 16:
            return num  # assuming registers 0-15
    raise ValueError(f"Invalid register: {reg}")

def imm_to_bin(value, bits, signed=False):
    """
    Convert an immediate value to binary of given bits.
    Supports signed values if needed.
    """
    value = int(value)
    if signed:
        # Two's complement conversion for negative numbers:
        if value < 0:
            value = (1 << bits) + value
    if not (0 <= value < (1 << bits)):
        raise ValueError(f"Immediate value {value} cannot be represented in {bits} bits")
    return value
