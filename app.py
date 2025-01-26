from flask import Flask, render_template, request, jsonify, send_from_directory
import spacy
import requests
from bs4 import BeautifulSoup
import random
import os

app = Flask(__name__)

# Load NLP model
nlp = spacy.load('en_core_web_sm')

# Serve static files directly from the root folder
@app.route('/<filename>')
def serve_static(filename):
    return send_from_directory(os.getcwd(), filename)

# Scrape content from Wikipedia
def scrape_content(topic):
    try:
        url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = ''.join(p.get_text() for p in soup.find_all('p', limit=3))
        return content
    except Exception as e:
        return f"Error scraping content: {str(e)}"

# Generate questions
def generate_questions(text):
    doc = nlp(text)
    questions = []
    templates = {
        "what": ["What is {0}?", "What are the key features of {0}?"],
        "how": ["How does {0} work?", "How is {0} significant?"],
        "describe": ["Describe {0}.", "What is the impact of {0}?"],
    }
    for chunk in doc.noun_chunks:
        topic = chunk.text.strip()
        question_type = random.choice(list(templates.keys()))
        if topic:
            question = random.choice(templates[question_type]).format(topic)
            questions.append(question)
    return questions[:10] if len(questions) >= 10 else questions + ["Not enough content."]

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    topic = data.get('topic')
    content = scrape_content(topic)
    if "Error" not in content:
        questions = generate_questions(content)
        return jsonify(questions=questions)
    return jsonify(questions=[content])

if __name__ == '__main__':
    app.run(debug=True)
