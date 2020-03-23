import pytest
import db_utils

sqlite_connection = db_utils.create_connection(':memory:')
db_utils.create_transactions_table(sqlite_connection)

# Basic implementation of db operations

def test_insert_transaction():
    db_utils.insert_transaction(sqlite_connection, '3cdfa224-548c-4ba5-b51c-5ff083f95bbe', '2020-03-20', 'salary', 234.56)

def test_delete_transaction():
    db_utils.delete_transaction(sqlite_connection, '3cdfa224-548c-4ba5-b51c-5ff083f95bbe')

def test_get_transaction_breakdown():
    db_utils.get_transaction_breakdown(sqlite_connection, '3cdfa224-548c-4ba5-b51c-5ff083f95bbe')
