from predict_val import compute, display_prediction
from flask import Flask, render_template, request, jsonify
import os
REL_PATH = 'D:/python/project 4/app/static/demo'

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
	img_name = request.form['img_name']
	path = os.path.join(REL_PATH,img_name)
	ex = display_prediction(path)
	result = compute(path)
	return jsonify({'expression' : ex, 'result' : result})

if __name__ == "__main__":
	app.run(host='localhost', port=5000, debug=True)