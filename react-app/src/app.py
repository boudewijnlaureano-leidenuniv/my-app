from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    print("Received request to /upload with POST method.")
    
    if 'file' not in request.files:
        print("No file part in the request.")
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file:
        print("File received:", file.filename)
        
        if file.filename.endswith('.txt'):
            try:
                content = file.read().decode('utf-8')
                print("File content read successfully.")
                return jsonify({"output": content})
            except Exception as e:
                print("Error reading file content:", e)
                return jsonify({"error": "Could not read file content"}), 500
        else:
            print("Invalid file format. Only .txt files are allowed.")
            return jsonify({"error": "Invalid file format. Only .txt files are allowed."}), 400
    else:
        print("File is missing or empty.")
        return jsonify({"error": "No file uploaded or file is empty"}), 400

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)
