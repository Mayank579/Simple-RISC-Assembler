from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from assembler_runner import run_assembler
from interpreter.simulator import execute_program  # Import the simulator

app = Flask(__name__)
CORS(app)

@app.route('/run-code', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get('code', '')
    
    try:
        if not code.strip():
            return jsonify({
                'output': '',
                'registers': [0] * 16
            })
            
        # First pass: collect labels
        labels = {}
        instructions = []
        current_address = 0
        
        for line in code.split('\n'):
            line = line.strip()
            if not line or line.startswith(';'):
                continue
                
            if ':' in line:
                label, *rest = line.split(':')
                label = label.strip().lower()
                labels[label] = current_address
                line = ':'.join(rest).strip()
                if not line:
                    continue
            
            if line:
                instructions.append(line)
                current_address += 4
        
        # Execute program and get register state
        machine_codes = run_assembler(instructions, labels)
        register_state = execute_program(machine_codes)
        
        output_lines = [f"{mc:032b}" for mc in machine_codes]
        output = "\n".join(output_lines)
        
        return jsonify({
            'output': output,
            'registers': register_state  # Send register state to frontend
        })
        
    except Exception as e:
        return jsonify({
            'output': f"Error: {str(e)}",
            'registers': [0] * 16
        })

if __name__ == '__main__':
    app.run(debug=True)
