# Flask & MongoDB Atlas Assignment

A Flask web application with two parts:
1. An `/api` route that reads from a backend JSON file and returns the data as a JSON response.
2. A frontend form that inserts data into **MongoDB Atlas**, with success redirection and inline error handling.

---

## Project Structure

```
flask_mongo_app/
├── app.py               # Main Flask application
├── data.json            # Backend data file for /api route
├── requirements.txt     # Python dependencies (flask, pymongo, dnspython)
└── templates/
    ├── index.html       # Form page
    └── success.html     # Success page after form submission
```

---

## Part 1 — `/api` Route

The `/api` route reads data from `data.json` and returns it as a JSON response using Flask's `jsonify()`.

### `data.json`
```json
[
  { "id": 1, "name": "Alice Johnson", "email": "alice@example.com", "role": "Developer" },
  { "id": 2, "name": "Bob Smith",     "email": "bob@example.com",   "role": "Designer"  },
  { "id": 3, "name": "Carol White",   "email": "carol@example.com", "role": "Manager"   }
]
```

### `/api` route in `app.py`
```python
@app.route("/api")
def api():
    data_file = os.path.join(os.path.dirname(__file__), "data.json")
    with open(data_file, "r") as f:
        data = json.load(f)
    return jsonify(data)
```

---

## Part 2 — MongoDB Form Submission

A frontend form collects **Name**, **Email**, and **Message**.

- ✅ **On success** → data is saved to MongoDB Atlas and user is redirected to `/success`
- ❌ **On error** → error is displayed on the same page without redirection

### `app.py` — Full Code

```python
from flask import Flask, jsonify, request, render_template, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import json
import os

app = Flask(__name__)

# MongoDB Atlas Connection
MONGO_URI = os.environ.get("MONGO_URI", "your_connection_string_here")
client = MongoClient(MONGO_URI)
db = client["flask_assignment"]
collection = db["submissions"]

# Part 1: /api route
@app.route("/api")
def api():
    data_file = os.path.join(os.path.dirname(__file__), "data.json")
    with open(data_file, "r") as f:
        data = json.load(f)
    return jsonify(data)

# Part 2: Frontend form
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", error=None)

@app.route("/submit", methods=["POST"])
def submit():
    name    = request.form.get("name", "").strip()
    email   = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        return render_template("index.html", error="All fields are required.")

    try:
        collection.insert_one({"name": name, "email": email, "message": message})
        return redirect(url_for("success"))
    except PyMongoError as e:
        return render_template("index.html", error=f"Database error: {str(e)}")

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
```

---

## Setup & Run Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set MongoDB URI
Replace the URI in `app.py` with your actual MongoDB Atlas connection string:
```python
MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/flask_assignment?retryWrites=true&w=majority"
```

### 3. Run the App
```bash
python app.py
```

---

## Route Summary

| Route      | Method | Description                                      |
|------------|--------|--------------------------------------------------|
| `/`        | GET    | Displays the submission form                     |
| `/submit`  | POST   | Handles form submission, inserts into MongoDB    |
| `/success` | GET    | Shows "Data submitted successfully"              |
| `/api`     | GET    | Returns JSON list read from `data.json`          |

---

## Tech Stack

- **Backend:** Python, Flask
- **Database:** MongoDB Atlas
- **Frontend:** HTML, CSS (Jinja2 templates)
