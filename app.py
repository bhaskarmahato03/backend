from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__, static_folder="static")
CORS(app)

# Load the data
df = pd.read_csv("hospital_data.csv")

# Health check route
@app.route('/health')
def health_check():
    return jsonify({"message": "Backend working properly!"})

# Serve index.html from static folder
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

# Serve home.html
@app.route('/home')
def serve_home():
    return send_from_directory('static', 'home.html')

# API endpoint - Get all states
@app.route('/hospital/states')
def get_states():
    return jsonify(df["State/UT/Division"].dropna().unique().tolist())

# API endpoint - State info
@app.route('/hospital/state/<string:name>')
def get_state_data(name):
    row = df[df["State/UT/Division"].str.lower() == name.lower()]
    if row.empty:
        return jsonify({"error": "State not found"}), 404
    return jsonify(row.iloc[0].to_dict())

# API endpoint - Compare states
@app.route('/hospital/compare')
def compare_states():
    state1 = request.args.get('state1')
    state2 = request.args.get('state2')
    if not state1 or not state2:
        return jsonify({"error": "Both state1 and state2 are required"}), 400

    row1 = df[df["State/UT/Division"].str.lower() == state1.lower()]
    row2 = df[df["State/UT/Division"].str.lower() == state2.lower()]

    if row1.empty or row2.empty:
        return jsonify({"error": "One or both states not found"}), 404

    return jsonify({
        state1.title(): row1.iloc[0].to_dict(),
        state2.title(): row2.iloc[0].to_dict()
    })

if __name__ == '__main__':
    app.run(debug=False)
