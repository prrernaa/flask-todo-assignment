from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
import json

app = Flask(__name__)

# --------------------------
# MongoDB Atlas Connection
# --------------------------
client = MongoClient("YOUR_MONGODB_ATLAS_CONNECTION_STRING")
db = client["assignment_db"]
collection = db["users"]

# --------------------------
# API Route - Read from file
# --------------------------
@app.route("/api", methods=["GET"])
def get_data():
    with open("data.json", "r") as file:
        data = json.load(file)
    return jsonify(data)

# --------------------------
# Form Page
# --------------------------
@app.route("/")
def form():
    return render_template("form.html")

# --------------------------
# Form Submission
# --------------------------
@app.route("/submit", methods=["POST"])
def submit():
    try:
        name = request.form["name"]
        email = request.form["email"]

        if not name or not email:
            raise ValueError("All fields are required")

        collection.insert_one({
            "name": name,
            "email": email
        })

        return redirect(url_for("success"))

    except Exception as e:
        return render_template("form.html", error=str(e))

# --------------------------
# Success Page
# --------------------------
@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)