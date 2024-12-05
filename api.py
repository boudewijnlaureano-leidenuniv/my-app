import os
import sys
import zipfile
from dotenv import load_dotenv
import json
from openai import OpenAI
import re
from flask import Flask, request, jsonify

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    print("API Key not found. Ensure it's defined in your .env file as OPENAI_API_KEY.")
    sys.exit(1)

# Supported file extensions
CODE_EXTENSIONS = {'.py', '.js', '.java', '.c', '.cpp', '.ts'}
DOC_EXTENSIONS = {'.md', '.txt'}
CONFIG_EXTENSIONS = {'.yaml', '.yml', '.json', '.env'}

# Initialize OpenAI client
OpenAI.api_key = API_KEY
client = OpenAI()

if not os.path.exists('tmp'):
    os.makedirs('tmp')

def extract_zip(file_path, extract_to="repo_contents"):
    try:
        if not os.path.exists(extract_to):
            os.makedirs(extract_to)
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return extract_to
    except Exception as e:
        print(f"Error extracting {file_path}: {e}")
        return None


def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Failed to read {file_path}: {e}")
        return None


# def create_assistant():
#     """Create a new assistant."""
#     try:
#         assistant = client.beta.assistants.create(
#             name="Repo Analyzer",
#             instructions="You are a repository analysis assistant. Answer questions based on provided code or documentation files.",
#             tools=[{"type": "code_interpreter"}, {"type": "file_search"}],
#             model="gpt-4o",
#         )
#         print(f"Created assistant with ID: {assistant.id}")
#         return assistant
#     except Exception as e:
#         print(f"Failed to create assistant: {e}")
#         sys.exit(1)


def create_thread():
    """Create a thread for the assistant."""
    try:
        thread = client.beta.threads.create()
        print(f"Thread created with ID: {thread.id}")
        return thread
    except Exception as e:
        print(f"Failed to create thread: {e}")
        sys.exit(1)

def send_message_to_assistant(thread_id, assistant_id, file_type, file_content, question):
    """Send a message to GPT and return the processed response."""
    try:
        message_content = f"""
        You are analyzing a {file_type} file to answer the following question based on the provided content.
        
        File content:
        plaintext
        {file_content}
        

        Question: "{question}"

        Instructions:
        - Scan the file content completely.
        - Answer the question clearly in the format:
          - Yes: followed by a concise explanation.
          - No: followed by a concise explanation.
          - I want on all answers a concise explanation why.
          - If insufficient information is present, state explicitly: "The file content does not provide sufficient information to answer the question."
        """

        # Create a message in the thread
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message_content,
        )

        # Use create_and_poll to process the message
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id,
            instructions="Analyze the file content and answer the question clearly.",
        )

        if run.status == "completed":
            # Retrieve the processed messages
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            response = [
                msg.content[0].text.value
                for msg in messages
                if msg.content and msg.content[0].type == "text"
            ]
            return "\n".join(response).strip()
        else:
            return f"Run failed with status: {run.status}"
    except Exception as e:
        print(f"Error communicating with assistant: {e}")
        return "Error occurred while processing."
    
def clean_response(response):
    """
    Extract the concise "Yes:" or "No:" response along with its explanation from the provided string.
    """
    match = re.search(r"(Yes:.*?\.|No:.*?\.)(\n|$)", response, re.DOTALL)
    if match:
        # Extract the matched content and strip trailing spaces
        return match.group(1).strip()
    return "The response does not contain a clear Yes or No with an explanation."

def process_repository(zip_path, assistant_id, thread_id, questions):
    extracted_path = extract_zip(zip_path)
    if extracted_path is None:
        return {"error": "Failed to extract the ZIP file."}

    results = {}
    for root, _, files in os.walk(extracted_path):
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1]

            # Hier kunnen we verder gaan met de verwerking van de bestanden
            file_content = read_file(file_path)
            if file_content:
                # Verzend berichten naar GPT (deze code is voor een ander deel van je project)
                results[file] = {
                    "type": ext.lstrip("."),
                    "content": file_content[:100]  # Geef de eerste 100 tekens van het bestand weer
                }

    return results


def format_results_readable(results, output_file="analysis_results.json"):
    """Format the results for better readability and save to a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, indent=4)
    print(f"Results have been saved to {output_file}.")

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_repository():
    """
    API endpoint to analyze a repository from a zip file and answer questions.
    """
    try:            
        if 'file' not in request.files:
            return jsonify({'error': 'File not provided.'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Validate the file type
        if not file.filename.endswith('.zip'):
            return jsonify({'error': 'Only .zip files are supported.'}), 400

        filepath = os.path.join(os.getcwd(), 'tmp', file.filename)
        file.save(filepath)

        # Extract ZIP and process repository
        questions = [
            "Does the repository contain social scoring in any shape or form?",
            "Does the repository include models that can manipulate the user?",
            "Does the repository contain data that imply vulnerabilities?",
            "Does the repository include biometric categorization?",
            "Does the repository contain real-time biometric identification?",
            "Does the repository possess the capability of assessing techniques for recognizing the emotional state of a person?",
            "Does the repository contain algorithms that can predict criminal behavior based on historical data?",
        ]

        # Hier voer je de verwerkingslogica uit met je assistant_id en thread_id
        assistant_id = 'asst_CbG44H0EMGkonjmBICzxm2Ef'
        thread_id = 'thread_inCWbm6c69xJsL02legOeTgd'
        
        # Call the function to process the repository
        analysis_results = process_repository(filepath, assistant_id, thread_id, questions)
        
        # Return the analysis results as JSON
        return jsonify(analysis_results), 200  # Format results properly before returning.

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True) 
    # extracted_path = extract_zip("C:/Users/Boudewijn/Documents/SBIS/my-app/tmp/Leiden2024.zip")

    # for root, _, files in os.walk(extracted_path):
    #     for file in files:
    #         content = read_file(file)
    #         print(content)