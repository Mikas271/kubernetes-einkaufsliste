from flask import Flask, request, jsonify, render_template_string
import psycopg2
import os
import time

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "postgres-service")
DB_NAME = os.environ.get("DB_NAME", "einkaufsliste")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "postgres")

def get_db():
    return psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )

def init_db():
    for i in range(10):
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL
                )
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("Datenbank verbunden und bereit!", flush=True)
            return
        except Exception as e:
            print(f"Warte auf Datenbank... ({i+1}/10): {e}", flush=True)
            time.sleep(3)
    raise Exception("Datenbank nicht erreichbar!")

# Beim Modulstart ausfuehren (nicht nur in __main__)
init_db()

# Originales HTML-Design aus deiner einkaufswagen-http.yaml
HTML = """
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Einkaufsliste</title>
    <script>
      async function addItem() {
        const input = document.getElementById("item");
        const name = input.value.trim();
        if (name === "") return;
        const res = await fetch('/items', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({name})
        });
        const item = await res.json();
        addToList(item.id, item.name);
        input.value = "";
      }

      function addToList(id, name) {
        const list = document.getElementById("einkaufsListe");
        const li = document.createElement("li");
        li.textContent = name;
        const btn = document.createElement("button");
        btn.textContent = "Delete";
        btn.onclick = async function() {
          await fetch('/items/' + id, {method: 'DELETE'});
          list.removeChild(li);
        };
        li.appendChild(btn);
        list.appendChild(li);
      }

      async function loadItems() {
        const res = await fetch('/items');
        const items = await res.json();
        const list = document.getElementById("einkaufsListe");
        list.innerHTML = "";  // Liste leeren vor dem Neu-Rendern
        items.forEach(item => addToList(item.id, item.name));
      }
      setInterval(loadItems, 1000);
      window.onload = loadItems;
    </script>
  </head>
  <body>
    <h1><u>Einkaufsliste</u></h1>
    <input id="item" name="listaddField" placeholder="Add Item...">
    <button type="button" onClick="addItem()">Add Item</button>
    <ul id="einkaufsListe">
    </ul>
  </body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/items', methods=['GET'])
def get_items():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM items ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1]} for r in rows])

@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    name = data.get('name', '').strip()
    if not name:
        return jsonify({"error": "Name fehlt"}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO items (name) VALUES (%s) RETURNING id, name", (name,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": row[0], "name": row[1]})

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE id = %s", (item_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)