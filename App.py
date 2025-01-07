from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/launch_nes', methods=['POST'])
def launch_nes():
    data = request.get_json()
    nes_path = data['path']
    try:
        # Run FCEUX with the specified NES game path
        subprocess.run(['fceux', nes_path])
        return jsonify({'status': 'success', 'message': 'NES game launched successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
