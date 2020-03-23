from flask import Flask, request, json, g
import jsonschema
import logging

# The inports need to be cleaned up later
from db_utils import create_connection, get_transaction_breakdown, delete_transaction, insert_transaction
from validator import validate_transaction_body, validate_transaction_id, validate_breakdown_query

# Need to set a global configuration for logging
# logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

# Duplicate value
# More detailed notes in db_init.py
DB_FILE_PATH = 'transactions.sqlite'

@app.before_request
def before_request():
    g.db = create_connection(DB_FILE_PATH)

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/transaction', methods=['POST'])
def add_transaction():
    req = request.form

    if validate_transaction_body(req):
        date = req.get("date")
        account_id = req.get('account_id')
        expense_type = req.get('expense_type')
        amount = float(req.get('amount'))

        record_id = insert_transaction(g.db, account_id, date, expense_type, amount)
        response = app.response_class(
            response=json.dumps({'id': record_id}),
            status=200,
            mimetype='application/json'
        )
        return response
    else:
        response = app.response_class(
            status=400,
            mimetype='application/json'
        )
        return response

@app.route('/transaction/<string:transaction_id>', methods=['DELETE'])
def remove_transaction(transaction_id):
    if validate_transaction_id(transaction_id):
        delete_transaction(g.db, transaction_id)
        response = app.response_class(
            status=204,
        )
        return response
    else:
        response = app.response_class(
            status=400,
        )
        return response

@app.route('/accounts/<string:customer_id>/breakdown')
def breakdown(customer_id):
    if validate_breakdown_query(customer_id, request.args):
        start_date = request.args.get('start_date', default = None, type = str)
        end_date = request.args.get('end_date', default = None, type = str)

        rows = get_transaction_breakdown(g.db, customer_id, start_date, end_date)
        resp = {}
        for row in rows:
            resp[row[1]] = { "sum": row[2], "count": row[3] }
        
        response = app.response_class(
            response=json.dumps(resp),
            status=200,
            mimetype='application/json'
        )
        return response
    else:
        response = app.response_class(
            status=400,
        )
        return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
