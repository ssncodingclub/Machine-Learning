import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import numpy
import cv2
import tensorflow
import tensorflow.keras as K

app = Flask(__name__)
# model = joblib.load('models/salary_predicter.pkl')
model = K.models.load_model('models/sudoku_solver_nn.h5', compile=False)

@app.route('/')
def home():
    # model.predict
    return render_template('index.html', prediction_text='Predicted salary: $ {}'.format(10))


@app.route('/',methods=['POST'])
def predict():
    # Get image from POST data
    imagefile = request.files.get('imagefile', '')
    imagefile.save('static/images/input_img.png')
    # Read image into numpy array
    np_img = cv2.imread('static/images/input_img.png', cv2.IMREAD_GRAYSCALE)
    np_img = np_img/255
    np_img_1d = np_img.reshape(-1, 1024)
    # Predict and Display
    digit_predict = np.argmax(model.predict(np_img_1d))
    prediction_text = "Couldn't find a digit there" if digit_predict==0 else f"That's a {digit_predict}"
    return render_template('index.html', prediction_text=prediction_text, display_img='images/input_img.png')


@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
