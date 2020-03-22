from flask import Flask, request, json
from manage import validate_date, get_transaction_breakdown, delete_transaction, insert_transaction, db_init
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/transaction', methods=['POST'])
def add_transaction():
    req = request.form
    date = req.get("date")
    account_id = req.get('account_id')
    expense_type = req.get('expense_type')
    amount = req.get('amount')
    record_id = insert_transaction(account_id, date, expense_type, amount)
    response = app.response_class(
        response=json.dumps(record_id),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/transaction/<string:transaction_id>', methods=['DELETE'])
def remove_transaction(transaction_id):
    delete_transaction(transaction_id)
    response = app.response_class(
        status=204,
    )
    return response

@app.route('/accounts/<string:customer_id>/breakdown')
def breakdown(customer_id):
    start_date = request.args.get('start_date', default = None, type = str)
    end_date = request.args.get('end_date', default = None, type = str)

    rows = get_transaction_breakdown(customer_id, start_date, end_date)
    response = app.response_class(
        response=json.dumps(rows),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    db_init()
    app.run(host='0.0.0.0', debug=True, port=5000)
