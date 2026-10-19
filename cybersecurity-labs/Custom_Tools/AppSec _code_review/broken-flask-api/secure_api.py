from flask import Flask, request, jsonify
import sqlite3
import jwt
import os
import re
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# SECRET loaded from environment - never hardcode!
SECRET = os.environ.get("JWT_SECRET", os.urandom(32).hex())
if not os.environ.get("JWT_SECRET"):
    raise ValueError("JWT_SECRET environment variable not set - refusing to start")

def db():
    return sqlite3.connect("users.db")

# Rate limiting to stop brute-force attacks
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# ---------- 1. SQL Injection FIXED: parameterized queries ----------
@app.route("/api/user/<user_id>")
def get_user(user_id):
    # Validate the input type first
    if not re.fullmatch(r"\d+", user_id):
        return {"error": "Invalid user id"}, 400

    conn = db()
    try:
        user = conn.execute(
            "SELECT id, username, email FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
    finally:
        conn.close()  # connection always closed

    if not user:
        return {"error": "User not found"}, 404

    return {"id": user[0], "username": user[1], "email": user[2]}


# ---------- 2. Broken Access Control FIXED: server-side role check ----------
@app.route("/api/admin/delete/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    # NEVER trust client-controlled headers (X-Admin can be spoofed by anyone)
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
    except Exception:
        return {"error": "Unauthorized"}, 401

    # Role comes from the verified token, not the client
    if decoded.get("role") != "admin":
        return {"error": "Forbidden"}, 403

    conn = db()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

    return {"status": "deleted"}


# ---------- 3. Auth FIXED: hashed passwords + rate limiting + expiry ----------
@app.route("/api/login", methods=["POST"])
@limiter.limit("5 per minute")  # brute-force protection
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    conn = db()
    user = conn.execute(
        "SELECT id, password FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    conn.close()

    # check_password_hash uses constant-time comparison
    if user and check_password_hash(user[1], password):
        token = jwt.encode(
            {
                "user_id": user[0],
                "role": "user",
                "exp": datetime.now(timezone.utc) + timedelta(hours=1),  # expiry
                "iat": datetime.now(timezone.utc)
            },
            SECRET,
            algorithm="HS256"
        )
        return {"token": token}

    # Generic message - don't leak whether user exists
    return {"error": "Invalid username or password"}, 401


# ---------- 4. JWT/IDOR FIXED: verify ownership of the resource ----------
@app.route("/api/profile", methods=["GET"])
def profile():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")

    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}, 401
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}, 401

    user_id = decoded["user_id"]

    conn = db()
    user = conn.execute(
        "SELECT id, username, email FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    conn.close()

    if not user:
        return {"error": "User not found"}, 404

    return jsonify({"id": user[0], "username": user[1], "email": user[2]})


# ---------- 5. Info disclosure FIXED: parameterized query + generic errors ----------
@app.route("/api/search")
def search():
    term = request.args.get("q", "")

    conn = db()
    try:
        results = conn.execute(
            "SELECT id, username FROM users WHERE username LIKE ?",
            (f"%{term}%",)
        ).fetchall()
    except Exception:
        # Log the real error server-side only; return a generic message
        app.logger.exception("Search query failed")
        return {"error": "Internal server error"}, 500
    finally:
        conn.close()

    return jsonify([{"id": r[0], "username": r[1]} for r in results])


if __name__ == "__main__":
    # debug=False in production!
    app.run(debug=False)
