from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/launch_nes', methods=['POST'])
def launch_nes():
    data = request.get_json()
    nes_path = data['path']
    try:
        # Run Nestopia with the specified NES game path
        subprocess.run(['nestopia', nes_path])
        return jsonify({'status': 'success', 'message': 'NES game launched successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/launch_xci', methods=['POST'])
def launch_xci():
    data = request.get_json()
    xci_path = data['path']
    try:
        # Run Yuzu with the specified XCI game path
        subprocess.run(['yuzu', xci_path])
        return jsonify({'status': 'success', 'message': 'XCI game launched successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
