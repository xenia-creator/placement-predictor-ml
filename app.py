from flask import Flask, request, jsonify, render_template
import pickle, numpy as np, warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Load model and scaler once at startup
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    iq   = float(data['iq'])
    cgpa = float(data['cgpa'])

    # Scale inputs before passing to model
    raw_features = np.array([[cgpa, iq]])
    scaled_features = scaler.transform(raw_features)

    prediction = int(model.predict(scaled_features)[0])
    proba      = model.predict_proba(scaled_features)[0]

    print("RAW:", raw_features)
    print("SCALED:", scaled_features)
    print("PROBA:", proba)

    return jsonify({
        'prediction': prediction,
        'placed': bool(prediction == 1),
        'placement_probability':    round(float(proba[1]) * 100, 1),
        'no_placement_probability': round(float(proba[0]) * 100, 1)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
