from flask import Flask, render_template
from database import get_connection

app = Flask(__name__)

@app.route("/")
def home():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()

    conn.close()

    return render_template("index.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)