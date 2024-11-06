from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and file.filename.endswith('.txt'):
        content = file.read().decode('utf-8')
        return jsonify({"output": content})
    return jsonify({"error": "Invalid file format. Only .txt files are allowed."}), 400

if __name__ == '__main__':
    app.run(debug=True)