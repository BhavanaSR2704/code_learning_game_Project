from flask import Flask, render_template, request, jsonify
import subprocess, json, tempfile, os

app = Flask(__name__)

# --------------------- LOGIN PAGE ---------------------
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/home", methods=["POST"])
def home():
    username = request.form["username"]
    return render_template("home.html", username=username)


# --------------------- LOAD CHALLENGES ---------------------
with open("challenges_python.json") as f:
    python_challenges = json.load(f)
with open("challenges_java.json") as f:
    java_challenges = json.load(f)
with open("challenges_c.json") as f:
    c_challenges = json.load(f)

def get_challenge(language, level):
    level = str(level)
    if language == "python":
        return python_challenges[level]
    if language == "java":
        return java_challenges[level]
    if language == "c":
        return c_challenges[level]


# --------------------- DASHBOARD PAGE ---------------------
@app.route("/dashboard/<language>")
def dashboard(language):
    return render_template("dashboard.html", language=language)


# --------------------- LEVEL SELECTION PAGE ---------------------
@app.route("/levels/<language>")
def level_page(language):
    return render_template("level.html", language=language)


# --------------------- CHALLENGE PAGE ---------------------
@app.route("/challenge/<language>/<int:level>")
def challenge_page(language, level):
    return render_template("challenge.html", language=language, level=level)


# --------------------- SEND CHALLENGE DATA ---------------------
@app.route("/get-challenge/<language>/<int:level>")
def get_challenge_route(language, level):
    return jsonify(get_challenge(language, level))


# --------------------- RUN CODE ---------------------
@app.route("/run-code", methods=["POST"])
def run_code():
    data = request.get_json()
    code = data["code"]
    language = data["language"]
    level = data["level"]

    challenge = get_challenge(language, level)
    expected_output = challenge["expected_output"]

    temp_dir = tempfile.mkdtemp()

    try:
        # ---------------- PYTHON FIXED SECTION ----------------
        if language == "python":
            file_path = os.path.join(temp_dir, "code.py")
            with open(file_path, "w") as f:
                f.write(code)

            process = subprocess.run(
                ["python", file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5,
                text=True
            )

            if process.returncode != 0:
                result_output = process.stderr   # clean error only
            else:
                result_output = process.stdout

        # ---------------- JAVA ----------------
        elif language == "java":
            file_path = os.path.join(temp_dir, "Main.java")
            with open(file_path, "w") as f:
                f.write(code)
            subprocess.check_output(["javac", file_path], stderr=subprocess.STDOUT)
            result_output = subprocess.check_output(
                ["java", "-cp", temp_dir, "Main"], stderr=subprocess.STDOUT
            ).decode()

        # ---------------- C ----------------
        elif language == "c":
            file_path = os.path.join(temp_dir, "program.c")
            with open(file_path, "w") as f:
                f.write(code)
            subprocess.check_output(
                ["gcc", file_path, "-o", temp_dir + "/out"], stderr=subprocess.STDOUT
            )
            result_output = subprocess.check_output(
                [temp_dir + "/out"], stderr=subprocess.STDOUT
            ).decode()

        else:
            result_output = "Invalid language."

    except Exception as e:
        result_output = str(e)

    is_correct = result_output.strip() == expected_output.strip()

    return jsonify({
        "output": result_output,
        "correct": is_correct
    })
# --------------------- PROFILE PAGE ---------------------

@app.route('/profile')
def profile():
    return render_template('profile.html')



if __name__ == "__main__":
    app.run(debug=True)
