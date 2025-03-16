from flask import Flask, request, jsonify
from flask_cors import CORS
from assembler_runner import run_assembler
from interpreter.simulator import execute_program  # Import the simulator

app = Flask(__name__)
CORS(app)

@app.route('/run-code', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get('code', '')
    
    try:
        if not code.strip():  # If no code provided, return all zeros
            return jsonify({
                'output': '',
                'registers': [0] * 16
            })
            
        machine_codes = run_assembler(code)
        registers = execute_program(machine_codes)
        output_lines = [f"{mc:032b}" for mc in machine_codes]
        output = "\n".join(output_lines)
        
        response = {
            'output': output,
            'registers': registers
        }
        return jsonify(response)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({
            'output': str(e),
            'registers': [0] * 16
        })

if __name__ == '__main__':
    app.run(debug=True)
