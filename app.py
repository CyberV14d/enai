from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)
client = Groq(api_key="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")  # from Groq Cloud

QUESTIONS = {
    "argument": "Redactează un text argumentativ de 150–300 de cuvinte despre ...",
    "stil_literar": "Identifică o figură de stil într-un text dat și explică folosind exemple."
}

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", questions=QUESTIONS)

@app.route("/evaluate", methods=["POST"])
def evaluate():
    qkey = request.form["question"]
    answer = request.form["answer"]
    prompt = (
        f"Ești profesor de limba română. Evaluează răspunsul unui elev la cerința:\n"
        f"\"{QUESTIONS[qkey]}\"\n\n"
        f"Răspuns elev:\n\"{answer}\"\n\n"
        "Acordă o notă de la 1 la 10 și oferă 2 puncte forte, 2 puncte slabe și sugestii."
    )
    resp = client.chat.completions.create(
        model="mistral-medium",  # adjust as needed 7
        messages=[{"role":"user","content":prompt}],
        temperature=0.7,
        max_tokens=512
    )
    result = resp.choices[0].message.content
    return render_template("index.html", questions=QUESTIONS,
                           answer=answer, result=result, selected=qkey)

if __name__ == "__main__":
    app.run(debug=True)