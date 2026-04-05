from flask import Flask, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret123"

# 🔐 LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect("/")
        else:
            return "<h3>❌ Invalid Login</h3><a href='/login'>Try Again</a>"

    return """
    <html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
    <body style="text-align:center; padding:20px;">
        <h2>Login</h2>
        <form method="POST">
            <input name="username" placeholder="Username"><br><br>
            <input name="password" type="password" placeholder="Password"><br><br>
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    """

# 🚪 LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# 🏠 HOME
@app.route("/", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect("/login")

    result = ""

    if request.method == "POST":
        url = request.form.get("url")
        email = request.form.get("email")
        text = request.form.get("text")

        # 🔥 DEBUG PRINT
        print("URL:", url)
        print("EMAIL:", email)
        print("TEXT:", text)

        try:
            if url and url.strip() != "":
                if "login" in url or "verify" in url or "bank" in url:
                    result = "⚠️ Phishing URL"
                else:
                    result = "✅ Safe URL"

            elif email and email.strip() != "":
                if "@" not in email or "." not in email:
                    result = "❌ Invalid Email"
                elif "verify" in email or "bank" in email:
                    result = "⚠️ Phishing Email"
                else:
                    result = "✅ Safe Email"

            elif text and text.strip() != "":
                t = text.lower()
                if "click" in t or "urgent" in t or "password" in t:
                    result = "⚠️ Suspicious Text"
                else:
                    result = "✅ Safe Text"

            else:
                result = "❗ Enter URL / Email / Message"

        except Exception as e:
            print(e)
            result = "❌ Error"

    return f"""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>

    <body style="text-align:center; padding:20px; font-family:Arial;">

        <h2>🔍 Phishing Detector</h2>

        <a href="/logout">Logout</a><br><br>

        <form method="POST">

            <input type="text" name="url" placeholder="Enter URL"><br><br>

            <input type="text" name="email" placeholder="Enter Email"><br><br>

            <textarea name="text" placeholder="Enter Message"></textarea><br><br>

            <button type="submit">Check</button>

        </form>

        <h3>{result}</h3>

    </body>
    </html>
    """

# 🚀 RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)