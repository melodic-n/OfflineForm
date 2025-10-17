from flask import Flask, render_template, request
import csv, os, datetime

app = Flask(__name__)

@app.route("/attendance", methods=["POST"])
def submit_attendance():
    name = request.form.get("name", "Anonyme")
    email = request.form.get("email", "")
    filiere = request.form.get("fa", "N/A")

    os.makedirs("results", exist_ok=True)

    now = datetime.datetime.now()
    filename = f"results/attendance-{now.strftime('%Y%m%d')}.csv"

    # --- Write data ---
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Add header only if new file
        if not file_exists:
            writer.writerow(["timestamp", "name", "email", "filiere"])
        writer.writerow([
            now.isoformat(),
            name,
            email,
            filiere
        ])

    return f"""
        <h2>Merci {name}!</h2>
        <h3>Ta présence a été enregistrée ✅</h3>
    """

@app.route("/attendance")
def attendance():
    return render_template('attendance.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
