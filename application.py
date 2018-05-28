import csv

from flask import Flask, jsonify
from flask import request

from config import PREDICTED_CLV_FILE

app = Flask(__name__)

# define a dict-like cache to store in memory all the clv-predictions
predicted_clv_cache = {}


def populate_cache():
    with open(PREDICTED_CLV_FILE, encoding='utf-8') as clv_file:
        csv_reader = csv.reader(clv_file)
        next(csv_reader)  # skip the headers
        for column in csv_reader:
            predicted_clv_cache[column[0]] = column[1]


populate_cache()


@app.route('/clv')
def clv():
    customer_id = request.args.get('customer_id')
    if not customer_id:
        return "customer_id param is required", 400

    clv_from_cache = predicted_clv_cache.get(customer_id)
    if clv_from_cache is None:
        return 'customer not found', 404
    else:
        return jsonify({"predicted_clv": clv_from_cache})


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)