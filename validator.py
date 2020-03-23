import jsonschema
import logging
import datetime
from uuid import UUID, uuid4

# jsonschema should be enought but there seem to be some bugs
def validate_transaction_body(form):
    # This can be later fetched from the OpenAPI doc
    transaction_schema =  {
        "type" : "object",
        "properties" : {
          "date" : {
            "type" : "string",
            "format" : "date"
          },
          "expense_type" : {
            "type" : "string",
            "enum" : [ "invoice", "salary", "services", "office-supplies", "travel" ]
          },
          "account_id" : {
            "type" : "string",
            "format" : "uuid"
          },
          "amount" : {
            "type" : "number",
            "fomat": "float"
          }
        }
    }
    expense_type = form.get('expense_type')

    try:
        account_id = form.get('account_id')
        UUID(account_id).version

        date = form.get("date")
        datetime.datetime.strptime(date, '%Y-%m-%d')

        amount = float(form.get('amount'))

    except ValueError:
        logging.info("Invalid format, check transaction body")
        return False

    try:
        instance={"date" : date, "expense_type": expense_type, "account_id": account_id, "amount": amount }
        jsonschema.validate(instance=instance, schema=transaction_schema)

    except jsonschema.exceptions.ValidationError as error:
        logging.info(error)
        return False
    
    return True

def validate_transaction_id(transaction_id):
    try:
        UUID(transaction_id).version

    except ValueError:
        logging.info("Invalid format, transaction ID should be a valid UUID")
        return False

    return True

def validate_breakdown_query(customer_id, args):
    try:
        UUID(customer_id).version
        start_date = args.get('start_date')
        if start_date != None:
            datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = args.get('end_date')
        if end_date != None:
            datetime.datetime.strptime(end_date, '%Y-%m-%d')

    except ValueError:
        logging.info("Invalid format, customer ID should be a valid UUID")
        return False

    return True
