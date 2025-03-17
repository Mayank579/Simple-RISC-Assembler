import streamlit as st
import sys
import tempfile
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

def main():
    st.title("Assembler Application")
    st.write("Upload your assembly file (.sr) to get machine code.")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose an assembly file", type=['sr'])
    if uploaded_file is not None:
        # Read the file content as text.
        file_contents = uploaded_file.read().decode("utf-8")
        # Create a temporary file to pass to the assembler (since your parser expects a filepath)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".sr") as tmp:
            tmp.write(file_contents.encode("utf-8"))
            tmp.flush()
            machine_codes = assemble(tmp.name)

        st.subheader("Machine Codes (32-bit binary):")
        for code in machine_codes:
            st.text(f"{code:032b}")

if __name__ == '__main__':
    main()
