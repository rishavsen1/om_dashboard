from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from calculators import (
    calculate_homeowner_savings,
    calculate_rep_value,
    calculate_ci_value,
    calculate_payback_period,
    calculate_yearly_simulation,
)

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    """Serve the main dashboard page"""
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    """Serve the favicon"""
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.svg", mimetype="image/svg+xml")


@app.route("/api/calculate/homeowner", methods=["POST"])
def calculate_homeowner():
    """Calculate homeowner daily savings and energy metrics"""
    try:
        data = request.json
        result = calculate_homeowner_savings(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/calculate/yearly", methods=["POST"])
def calculate_yearly():
    """Calculate blended annual savings across different day types"""
    try:
        data = request.json
        result = calculate_yearly_simulation(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/calculate/rep", methods=["POST"])
def calculate_rep():
    """Calculate REP value proposition"""
    try:
        data = request.json
        result = calculate_rep_value(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/calculate/ci", methods=["POST"])
def calculate_ci():
    """Calculate C&I business value"""
    try:
        data = request.json
        result = calculate_ci_value(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/calculate/payback", methods=["POST"])
def calculate_payback():
    """Calculate payback period"""
    try:
        data = request.json
        result = calculate_payback_period(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/summary/data", methods=["GET"])
def get_summary_data():
    """Get summary table data"""
    # This can be expanded to fetch from database if needed
    summary_data = {
        "homeowners": [312500, 625000, 937500],
        "reps": [100000, 100000, 100000],
        "tdu": [9236018, 23350000, 35025000],
        "region": [4700000, 14100000, 14100000],
    }
    return jsonify(summary_data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
