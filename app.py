"""Workforce Register REST API - tracks workers, wages and daily attendance for a manufacturing site."""
from flask import Flask, jsonify, request
app = Flask(__name__)
workers = {}
attendance = []
next_id = {"w": 1, "a": 1}
REQUIRED = ["name", "role", "daily_wage"]

def err(msg, code):
    return jsonify({"error": msg}), code

@app.get("/api/workers")
def list_workers():
    role = request.args.get("role")
    data = [w for w in workers.values() if not role or w["role"] == role]
    return jsonify({"count": len(data), "workers": data}), 200

@app.get("/api/workers/<int:wid>")
def get_worker(wid):
    return (jsonify(workers[wid]), 200) if wid in workers else err("Worker not found", 404)

@app.post("/api/workers")
def create_worker():
    body = request.get_json(silent=True) or {}
    missing = [f for f in REQUIRED if f not in body]
    if missing:
        return err(f"Missing fields: {', '.join(missing)}", 400)
    if not isinstance(body["daily_wage"], (int, float)) or body["daily_wage"] < 300:
        return err("daily_wage must be at least 300", 400)
    wid = next_id["w"]; next_id["w"] += 1
    code = f"WRK-{wid:03d}"
    workers[wid] = {"id": wid, "code": code, "name": body["name"], "role": body["role"],
                    "daily_wage": body["daily_wage"], "site": body.get("site", "Main Plant")}
    return jsonify(workers[wid]), 201

@app.put("/api/workers/<int:wid>")
def update_worker(wid):
    if wid not in workers:
        return err("Worker not found", 404)
    body = request.get_json(silent=True) or {}
    for k in ("name", "role", "daily_wage", "site"):
        if k in body:
            workers[wid][k] = body[k]
    return jsonify(workers[wid]), 200

@app.delete("/api/workers/<int:wid>")
def delete_worker(wid):
    if wid not in workers:
        return err("Worker not found", 404)
    del workers[wid]
    return "", 204

@app.post("/api/attendance")
def mark_attendance():
    body = request.get_json(silent=True) or {}
    wid = body.get("worker_id")
    if wid not in workers:
        return err("Unknown worker_id", 404)
    hours = body.get("hours", 8)
    rec = {"id": next_id["a"], "worker_id": wid, "date": body.get("date"),
           "hours": hours, "machine": body.get("machine"),
           "pay": round(workers[wid]["daily_wage"] * hours / 8, 2)}
    next_id["a"] += 1
    attendance.append(rec)
    return jsonify(rec), 201

@app.get("/api/attendance")
def list_attendance():
    wid = request.args.get("worker_id", type=int)
    data = [a for a in attendance if not wid or a["worker_id"] == wid]
    return jsonify({"count": len(data), "records": data}), 200

if __name__ == "__main__":
    app.run(port=5000)
