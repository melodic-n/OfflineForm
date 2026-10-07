from flask import Flask, render_template, request, Response
import csv, os, datetime, socket, io
import qrcode
import qrcode.image.svg

app = Flask(__name__)

PORT = 8000


def get_lan_ip():
    """Address the phones on the hotspot can reach, not 127.0.0.1."""
    try:
        # No packet is sent, this only asks the OS which interface it would use
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        pass
    try:
        return socket.gethostbyname(socket.gethostname())
    except OSError:
        return "127.0.0.1"


def attendance_url():
    return f"http://{get_lan_ip()}:{PORT}/attendance"

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

@app.route("/qr")
def qr_page():
    return render_template('qr.html', url=attendance_url())

@app.route("/qr.svg")
def qr_svg():
    img = qrcode.make(
        attendance_url(),
        image_factory=qrcode.image.svg.SvgPathImage,
        border=2
    )
    buf = io.BytesIO()
    img.save(buf)
    return Response(buf.getvalue(), mimetype="image/svg+xml")

def print_startup_qr():
    url = attendance_url()
    qr = qrcode.QRCode(border=2)
    qr.add_data(url)
    print()
    qr.print_ascii(invert=True)
    print(f"  Scan the code above, or open: {url}")
    print(f"  Full-screen version for a projector: http://{get_lan_ip()}:{PORT}/qr\n")

if __name__ == '__main__':
    print_startup_qr()
    app.run(host='0.0.0.0', port=PORT, debug=False)
