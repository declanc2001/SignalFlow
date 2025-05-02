from flask import Flask, render_template
import psycopg2
import os

app = Flask(__name__)
DATABASE_URL = os.environ.get("DATABASE_URL")

@app.route("/")
def index():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions ORDER BY timestamp DESC LIMIT 20;")
        rows = cursor.fetchall()
        conn.close()

        transactions = []
        for row in rows:
            transactions.append({
                "tx_hash": row[0],
                "from_address": row[1],
                "to_address": row[2],
                "value_usd": float(row[3]),
                "timestamp": str(row[4]),
                "block_number": row[5]
            })

        return render_template("index.html", transactions=transactions)

    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
