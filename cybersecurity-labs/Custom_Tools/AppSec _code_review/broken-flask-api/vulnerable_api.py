from flask import Flask, request, jsonify
import sqlite3
import jwt

app = Flask(__name__)
SECRET = "my-secret-key"

def db():
    return sqlite3.connect("users.db")

@app.route("/api/user/<user_id>")
def get_user(user_id):
    conn = db()

    # 1. SQL injection
    query = f"SELECT id, username, email FROM users WHERE id = {user_id}"
    user = conn.execute(query).fetchone()

    if not user:
        return {"error": "User not found"}, 404

    return {
        "id": user[0],
        "username": user[1],
        "email": user[2]
    }


@app.route("/api/admin/delete/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    # 2. Trusting a client-controlled header for authorization
    if request.headers.get("X-Admin") != "true":
        return {"error": "Forbidden"}, 403

    conn = db()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()

    return {"status": "deleted"}


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data["username"]
    password = data["password"]

    conn = db()
    user = conn.execute(
        "SELECT id, password FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    if user and user[1] == password:
        # 3. Hard-coded weak JWT secret
        token = jwt.encode(
            {"user_id": user[0], "role": "user"},
            SECRET,
            algorithm="HS256"
        )
        return {"token": token}

    return {"error": "Invalid credentials"}, 401


@app.route("/api/profile", methods=["GET"])
def profile():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")

    try:
        # 4. JWT claims are trusted without checking authorization properly
        decoded = jwt.decode(
            token,
            SECRET,
            algorithms=["HS256"]
        )

        user_id = decoded["user_id"]

        conn = db()
        user = conn.execute(
            "SELECT id, username, email FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

        return jsonify({
            "id": user[0],
            "username": user[1],
            "email": user[2]
        })

    except Exception:
        return {"error": "Invalid token"}, 401


@app.route("/api/search")
def search():
    term = request.args.get("q", "")

    # 5. Sensitive information exposed in an error response
    try:
        conn = db()
        query = f"SELECT * FROM users WHERE username LIKE '%{term}%'"
        results = conn.execute(query).fetchall()
        return jsonify(results)

    except Exception as e:
        return {
            "error": str(e),
            "database": "users.db"
        }, 500


if __name__ == "__main__":
    app.run(debug=True)
