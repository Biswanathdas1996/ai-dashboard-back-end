import os
import logging
import linierRegration
import polynomialRegression
import movingAvarage
import deepLearning
import simpleExtrapolation
import timeSeriesAnalysis
import NLQ_SQL

from flask import Flask, request, jsonify, Response, send_file

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response


@app.route('/api', methods=['GET'])
def default_app():
    return 'app is running successfully'


@app.route('/ask-question', methods=['POST'])
def nlq_app():
    requestData = request.json
    dbUri = requestData.get('dbUri')
    question = requestData.get('question')

    result = NLQ_SQL.searchInDB(dbUri, question)
    return jsonify(result)


@app.route('/api/prediction', methods=['POST'])
def return_linier_regration():
    requestData = request.json
    input_data = requestData.get('data')
    x = requestData.get('x')
    y = requestData.get('y')
    type = requestData.get('type')

    if (type == "linierRegration"):
        result = linierRegration.generate_sales_chart(input_data, x, y)
        return jsonify(result)
    elif (type == "polynomialRegression"):
        result = polynomialRegression.generate_sales_chart(input_data, x, y)
        return jsonify(result)
    elif (type == "movingAvarage"):
        result = movingAvarage.generate_sales_chart(input_data, x, y)
        return jsonify(result)
    elif (type == "deepLearning"):
        result = deepLearning.generate_sales_chart(input_data, x, y)
        return jsonify(result)
    elif (type == "simpleExtrapolation"):
        result = simpleExtrapolation.generate_sales_chart(input_data, x, y)
        return jsonify(result)
    elif (type == "timeSeriesAnalysis"):
        result = timeSeriesAnalysis.generate_sales_chart(input_data, x, y)
        return jsonify(result)
    else:
        return 'No type specified'


if __name__ == '__main__':
    app.run()
