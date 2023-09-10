import logging
import linierRegration
import polynomialRegression
import movingAvarage
import simpleExtrapolation
import timeSeriesAnalysis
import NLQ_SQL
import PDF_CHAT

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


@app.route('/connect', methods=['POST'])
def get_all_tables():
    requestData = request.json
    dbUri = requestData.get('dbUri')
    result = NLQ_SQL.getAllTables(dbUri)
    return jsonify(result)


@app.route('/get-table-data', methods=['POST'])
def fetchAllDataFromTable():
    requestData = request.json
    dbUri = requestData.get('dbUri')
    table = requestData.get('table')
    result = NLQ_SQL.fetchAllDataFromTable(dbUri, table)
    return result


@app.route('/ask-question', methods=['POST'])
def nlq_app():
    requestData = request.json
    config = requestData.get('config')
    dbUri = requestData.get('dbUri')
    question = requestData.get('question')

    result = NLQ_SQL.searchInDB(config, dbUri, question)
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
    elif (type == "simpleExtrapolation"):
        result = simpleExtrapolation.generate_sales_chart(input_data, x, y)
        return jsonify(result)
    elif (type == "timeSeriesAnalysis"):
        result = timeSeriesAnalysis.generate_sales_chart(input_data, x, y)
        return jsonify(result)
    else:
        return 'No type specified'


@app.route('/upload-file', methods=['POST'])
def upload():
    if 'pdf_docs' not in request.files:
        return jsonify({"error": "No file part"}), 400
    pdf_docs = request.files.getlist('pdf_docs')
    if not pdf_docs:
        return jsonify({"error": "No selected file"}), 400
    pdf_docs = request.files.getlist('pdf_docs')
    PDF_CHAT.upload(pdf_docs)
    return jsonify({"message": "PDFs processed successfully"})


@app.route('/upload-text', methods=['POST'])
def uploadText():

    text_data = request.json.get('text_data')
    # config = request.json.get('config')
    PDF_CHAT.uploadText(text_data)
    return jsonify({"message": "PDFs processed successfully"})


@app.route('/process', methods=['POST'])
def proces():
    user_question = request.json.get('user_question')
    config = request.json.get('config')
    messages = PDF_CHAT.process(user_question, config)
    return jsonify(messages)


if __name__ == '__main__':
    app.run()
