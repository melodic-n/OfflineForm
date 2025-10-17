from flask import Flask, render_template, request
import csv, os, datetime

app = Flask(__name__)

# --- File paths ---
RESULTS_DIR = "results"
FEEDBACK_FILE = os.path.join(RESULTS_DIR, "feedback.csv")
QUIZ_FILE = os.path.join(RESULTS_DIR, "quiz_results.csv")

# --- Ensure results folder exists ---
os.makedirs(RESULTS_DIR, exist_ok=True)

# --- Correct answers & points ---
CORRECT_ANSWERS = {
    "q1": ("Un programme qui gère le matériel et les logiciels d’un ordinateur", 1),
    "q2": (["Linux", "Windows", "MacOS"], 2),
    "q3": ("Basic input output system", 1),
    "q4": ("ROM", 2),
    "q5": ("RAM", 2),
    "q6": (["Fedora", "kali", "debian"], 2),
    "q7": ("ROM", 2),
    "q8": ("Répértoire racine", 3),
    "q9": ("répértoire", 3),
    "q10": ("commandes user", 3),
    "q11": (["passwd", "shadow"], 3),
    "q12": ("des informations sur password", 3),
    "q13": ("des informations sur user", 3),
    "q14": ("Login:passwd:UID:GUID:Comment:HomeDirectory:Shell", 4),
    "q15": ("root", 3),
    "q16": ("", 4),
    "q17": ("", 3),
    "q18": ("", 1),
    "q19": ("sudo ls /etc/shadow", 10),
}



# --- ROUTES ---

@app.route('/quiz')
def quiz():
    return render_template('Formlinux.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name', 'Anonyme')
    email = request.form.get('email', '')
    responses = {k: v for k, v in request.form.items() if k not in ['name', 'email']}

    total_points = 0
    max_points = sum(v[1] for v in CORRECT_ANSWERS.values())

    # --- Scoring ---
    for question, (correct, pts) in CORRECT_ANSWERS.items():
        user_answer = responses.get(question)

        if not user_answer:
            continue

        # Handle multiple correct answers
        if isinstance(correct, list):
            if isinstance(user_answer, list):
                if set(user_answer) == set(correct):
                    total_points += pts
            else:
                if user_answer in correct:
                    total_points += pts
        else:
            if user_answer.strip().lower() == correct.strip().lower():
                total_points += pts

    # --- Save results ---
    with open(QUIZ_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.datetime.now().isoformat(),
            name,
            email,
            total_points,
            max_points,
            f"{total_points}/{max_points}",
            responses
        ])

    return f"""
        <h2>Merci {name}! Tes réponses ont été enregistrées.</h2>
        <h3>Ton score: {total_points} / {max_points}</h3>
    """


@app.route('/feedback')
def feedback_form():
    name = request.args.get('name', '')
    return render_template('feedback.html', name=name)


@app.route('/feedback_submit', methods=['POST'])
def feedback_submit():
    name = request.form.get('name', 'Anonyme')
    rating = request.form.get('rating', '')
    comment = request.form.get('comment', '')

    with open(FEEDBACK_FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            datetime.datetime.now().isoformat(),
            name,
            rating,
            comment
        ])

    return render_template('feedback_thanks.html', name=name)


@app.route("/attendance")
def attendance():
    return "<h3>Attendance tracking not implemented yet.</h3>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
