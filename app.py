from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

def search_academic_sources(query):
    """Fetch academic sources using the OpenAI API."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    # Prompt structure
    prompt = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an academic search assistant that retrieves and presents scholarly information "
                    "in a structured format. Ensure responses strictly follow this structure:\n\n"
                    "1. **Title**: <Title of the Paper>\n"
                    "2. **Author(s)**: <List of Authors>\n"
                    "3. **Description**: <Brief Summary of the Paper>\n"
                    "4. **Citation**: <APA formatted citation>\n"
                    "5. **Reference Link**: <Clickable URL, if available>\n\n"
                    "Maintain accuracy, conciseness, and consistency in every response."
                )
            },
            {
                "role": "user",
                "content": f"Retrieve academic sources on '{query}' and present them in the specified format."
            }
        ],
        "temperature": 0.3
    }

    response = requests.post(OPENAI_URL, headers=headers, json=prompt)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route("/", methods=["GET"])
def home():
    """Render the homepage."""
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    """Handle search requests and return results."""
    query = request.form.get("query")
    if not query:
        return jsonify({"result": "No query provided."})
    result = search_academic_sources(query)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)