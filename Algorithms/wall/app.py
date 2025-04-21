from flask import Flask, jsonify, render_template
import math

app = Flask(__name__)

person = {"x": 0, "y": 2}
obstacle = {"x": 5, "y": 2}
STEP_SIZE = 0.2
MAX_DISTANCE = 5.0
COLLISION_THRESHOLD = 0.4

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def get_status():
    dx = obstacle["x"] - person["x"]
    dy = obstacle["y"] - person["y"]
    distance = math.hypot(dx, dy)

    if distance < COLLISION_THRESHOLD:
        volume = 1.0
        collision = True
    else:
        volume = max(0.0, 1.0 - distance / MAX_DISTANCE)
        collision = False

    # Движение вперёд
    person["x"] += STEP_SIZE

    return jsonify({
        "volume": round(volume, 2),
        "collision": collision
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
 