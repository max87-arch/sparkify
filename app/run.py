import json

import numpy as np
from flask import Flask
from flask import render_template, request, jsonify
from predicts.churn import predict_churn

# from predicts.categories import predict_categories

app = Flask(__name__)


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    # render web page with plotly graphs
    return render_template('master.html')


# web page that handles user query and displays model results
@app.route('/detect_churn', methods=['POST'])
def detect_churn():
    # save user input in query
    data = json.loads(request.form.get('json', ''))
    query = [list(x.values()) for x in data]

    classification_results = predict_churn(query)
    churn_user = False

    for pred, _, _ in classification_results:
        if pred == 1.0:
            churn_user = True
    # This will render the churn_user.html Please see that file.
    return render_template(
        'detect_churn.html',
        churn_user=churn_user
    )


def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()
