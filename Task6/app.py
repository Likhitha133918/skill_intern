from flask import Flask, render_template, request, redirect, url_for, flash
import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Sample project data
projects = [
    {
        "title": "Arduino Smart Irrigation",
        "description": "Automated irrigation system using soil moisture sensor.",
        "tech": "Arduino, Sensors, IoT"
    },
    {
        "title": "Electronic Nose (ESP32)",
        "description": "Industrial smell detection wearable device.",
        "tech": "ESP32, Gas Sensors"
    },
    {
        "title": "Python To-Do CLI App",
        "description": "Persistent command line task manager.",
        "tech": "Python"
    }
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects")
def project_page():
    return render_template("projects.html", projects=projects)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # Here you can connect to database or email service
        print(f"Message from {name} ({email}): {message}")

        flash("Your message has been sent successfully!", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")

@app.context_processor
def inject_year():
    return {'year': datetime.datetime.now().year}

if __name__ == "__main__":
    app.run(debug=True)