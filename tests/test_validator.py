import pytest
import validator

# These are not exsautive

def test_validate_transaction_body():
    valid_form = {}
    valid_form['date'] = '2020-03-20'
    valid_form['expense_type'] = 'invoice'
    valid_form['account_id'] = 'c1a52ec1-01a6-438b-a845-521144c5d36b'
    valid_form['amount'] = '23.45'
    assert validator.validate_transaction_body(valid_form) == True


    invalid_form_one = {}
    invalid_form_one['date'] = '2020-03-20'
    invalid_form_one['expense_type'] = 'bla ble blu'
    invalid_form_one['account_id'] = 'c1a52ec1-01a6-438b-a845-521144c5d36b'
    invalid_form_one['amount'] = '23.45'
    assert validator.validate_transaction_body(invalid_form_one) == False

def test_validate_transaction_id():
    valid_id = 'c1a52ec1-01a6-438b-a845-521144c5d36b'
    assert validator.validate_transaction_id(valid_id) == True

    valid_id = '1234'
    assert validator.validate_transaction_id(valid_id) == False

def test_validate_breakdown_query():
    valid_id = 'c1a52ec1-01a6-438b-a845-521144c5d36b'
    valid_args = {}
    valid_args['start_date'] = '2020-03-13'
    valid_args['end_date'] = '2020-05-10'
    assert validator.validate_breakdown_query(valid_id, valid_args) == True

    valid_id = 'c1a52ec1-01a6-438b-a845-521144c5d36b'
    invalid_args = {}
    invalid_args['start_date'] = '24-sep-2020'
    invalid_args['end_date'] = '2020-05-10'
    assert validator.validate_breakdown_query(valid_id, invalid_args) == False
