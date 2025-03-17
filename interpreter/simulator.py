def execute_program(machine_codes, labels=None):
    """
    Execute the machine code and return final register values
    """
    registers = [0] * 16
    memory = [0] * 1024
    pc = 0
    condition_flags = {'N': False, 'Z': False}
    execution_count = 0
    MAX_EXECUTIONS = 1000

    def update_flags(result):
        condition_flags['N'] = result < 0
        condition_flags['Z'] = result == 0
        print(f"Flags updated: N={condition_flags['N']}, Z={condition_flags['Z']}")

    while pc < len(machine_codes) * 4 and execution_count < MAX_EXECUTIONS:
        execution_count += 1
        instr_index = pc // 4
        instruction = machine_codes[instr_index]
        
        opcode = (instruction >> 27) & 0x1F
        is_immediate = (instruction >> 26) & 0x1
        rd = (instruction >> 22) & 0xF
        rs1 = (instruction >> 18) & 0xF

        print(f"\nExecuting at PC={pc}: {bin(instruction)[2:].zfill(32)}")

        if opcode == 0x00:  # ADD
            value2 = 0
            if is_immediate:
                value2 = instruction & 0x3FFFF
                # Handle sign extension
                if value2 & 0x20000:
                    value2 = -(0x40000 - value2)
            else:
                rs2 = (instruction >> 14) & 0xF
                value2 = registers[rs2]

            # Accumulate properly in register
            old_value = registers[rd]
            registers[rd] = registers[rs1] + value2
            print(f"ADD: R{rd} = R{rs1}({registers[rs1]}) + {value2} = {registers[rd]}")
            update_flags(registers[rd])
            print(f"Register R{rd} updated: {registers[rd]}")

        elif opcode == 0x01:  # SUB instruction
            value2 = 0
            if is_immediate:
                value2 = instruction & 0x3FFFF
                if value2 & 0x20000:  # Sign extend
                    value2 = -(0x40000 - value2)
            else:
                rs2 = (instruction >> 14) & 0xF
                value2 = registers[rs2]
            
            old_value = registers[rd]
            registers[rd] = registers[rs1] - value2  # Fixed SUB operation
            print(f"SUB: R{rd} = R{rs1}({registers[rs1]}) - {value2} = {registers[rd]}")
            update_flags(registers[rd])

        elif opcode == 0x09:  # MOV
            if is_immediate:
                imm = instruction & 0x3FFFF
                registers[rd] = imm
                print(f"MOV: R{rd} = {imm}")
                print(f"Register R{rd} updated: {registers[rd]}")

        elif opcode == 0x05:  # CMP
            value2 = 0
            if is_immediate:
                value2 = instruction & 0x3FFFF
            else:
                rs2 = (instruction >> 14) & 0xF
                value2 = registers[rs2]
            result = registers[rs1] - value2
            update_flags(result)
            print(f"CMP: R{rs1}({registers[rs1]}) - {value2} = {result}")

        elif opcode >= 0x18:  # Branch instructions
            offset = instruction & 0x3FFFF
            if offset & 0x20000:
                offset = -(0x40000 - offset)

            should_branch = False
            if opcode == 0x18:    # B
                should_branch = True
            elif opcode == 0x1B:   # BGT
                should_branch = not condition_flags['Z'] and not condition_flags['N']

            if should_branch:
                new_pc = pc + (offset * 4)
                print(f"Branch taken: PC {pc} -> {new_pc}")
                pc = new_pc
                continue

        print("Register state:", " ".join(f"R{i}={v}" for i, v in enumerate(registers) if v != 0))
        print(f"Current register state: R1={registers[1]}")  # Debug R1's value
        pc += 4

    print("Final register state:", registers)
    return list(registers)  # Ensure we return a list
