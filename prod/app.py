from workerA import add_nums, get_accuracy, get_predictions

from flask import (
   Flask,
   request,
   jsonify,
   Markup,
   render_template 
)

#app = Flask(__name__, template_folder='./templates',static_folder='./static')
app = Flask(__name__)

@app.route("/")
def index():
    return '<h1>Welcome to the Machine Learning Course.</h1>'

@app.route("/predict", methods=['POST', 'GET'])
def predict_star_count():
    predicted = None
    real = None
    if request.method == 'POST':
        repo_link = request.form['repo_link']
        predicted, real = get_predictions.delay(repo_link)

    return render_template('result.html', predicted=predicted, real=real)

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5100,debug=True)
