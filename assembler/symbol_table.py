# assembler/symbol_table.py

class SymbolTable:
    def __init__(self):
        self.table = {}

    def add_label(self, label, address):
        if label in self.table:
            raise ValueError(f"Duplicate label: {label}")
        self.table[label] = address

    def get_address(self, label):
        if label not in self.table:
            raise ValueError(f"Undefined label: {label}")
        return self.table[label]
