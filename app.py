from flask import Flask, render_template, request
import os
from utils.parser import extract_text
from utils.ranker import rank_resume

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():

    job_description = request.form['job_description']
    file = request.files['resume']

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'],
        file.filename
    )

    file.save(filepath)

    resume_text = extract_text(filepath)

    score = rank_resume(
        resume_text,
        job_description
    )

    return render_template(
        "results.html",
        score=round(score * 100, 2)
    )

if __name__ == "__main__":
    app.run(debug=True)
