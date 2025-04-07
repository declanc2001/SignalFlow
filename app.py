from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)
DATABASE_URL = os.environ.get("DATABASE_URL")

@app.route("/api/transactions")
def get_transactions():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions ORDER BY timestamp DESC LIMIT 20;")
        rows = cursor.fetchall()
        conn.close()

        result = []
        for row in rows:
            result.append({
                "tx_hash": row[0],
                "from_address": row[1],
                "to_address": row[2],
                "value_usd": row[3],
                "timestamp": row[4].isoformat(),
                "block_number": row[5]
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # default to 5000 if not provided
    app.run(host="0.0.0.0", port=port)
