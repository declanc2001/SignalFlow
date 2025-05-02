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
            try:
                value_usd = float(row[3]) if isinstance(row[3], (int, float)) or str(row[3]).replace('.', '', 1).isdigit() else 0.0
                transactions.append({
                    "tx_hash": row[0],
                    "from_address": row[1],
                    "to_address": row[2],
                    "value_usd": value_usd,
                    "timestamp": str(row[4]),
                    "block_number": row[5]
                })
            except Exception as e:
                print(f"⚠️ Skipping invalid row: {e}")
                continue

        return render_template("index.html", transactions=transactions)
