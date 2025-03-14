from flask import Flask, request, jsonify
from flask_cors import CORS
from assembler_runner import run_assembler  # Import the function for running the assembler

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/run-code', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get('code', '')
    try:
        machine_codes = run_assembler(code)
        # Format each machine code as a 32-bit binary string
        output_lines = [f"{code:032b}" for code in machine_codes]
        output = "\n".join(output_lines)
    except Exception as e:
        output = str(e)
    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True)
