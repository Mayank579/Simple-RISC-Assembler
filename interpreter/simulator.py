def execute_program(machine_codes):
    """
    Execute the machine code and return final register values
    """
    registers = [0] * 16  # Initialize all registers to 0
    pc = 0
    
    while pc < len(machine_codes) * 4:
        instr_index = pc // 4
        instruction = machine_codes[instr_index]
        
        # Extract opcode and modifier bit
        opcode = (instruction >> 27) & 0x1F
        is_immediate = (instruction >> 26) & 0x1
        
        # Extract common fields
        rd = (instruction >> 22) & 0xF
        rs1 = (instruction >> 18) & 0xF
        
        # Handle different instruction types
        if opcode == 0x1F:  # HLT
            break
            
        elif opcode <= 0x04:  # Arithmetic: ADD, SUB, MUL, DIV, MOD
            if is_immediate:
                imm = instruction & 0x3FFFF  # 18-bit immediate
                # Sign extend if negative
                if imm & 0x20000:
                    imm = imm - 0x40000
                value2 = imm
            else:
                rs2 = (instruction >> 14) & 0xF
                value2 = registers[rs2]
            
            if opcode == 0:  # ADD
                registers[rd] = registers[rs1] + value2
            elif opcode == 1:  # SUB
                registers[rd] = registers[rs1] - value2
            elif opcode == 2:  # MUL
                registers[rd] = registers[rs1] * value2
            elif opcode == 3:  # DIV
                registers[rd] = registers[rs1] // value2 if value2 != 0 else 0
            elif opcode == 4:  # MOD
                registers[rd] = registers[rs1] % value2 if value2 != 0 else 0
                
        elif opcode == 0x09:  # MOV
            if is_immediate:
                imm = instruction & 0x3FFFF
                if imm & 0x20000:  # Sign extend
                    imm = imm - 0x40000
                registers[rd] = imm
            else:
                rs2 = (instruction >> 14) & 0xF
                registers[rd] = registers[rs2]
        
        pc += 4
    
    return registers
