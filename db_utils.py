import sqlite3
from uuid import UUID, uuid4
import datetime
import logging

def create_connection(db_file):
    sqlite_connection = None
    try:
        sqlite_connection = sqlite3.connect(db_file)
        cursor = sqlite_connection.cursor()
        logging.info("Successfully Connected to SQLite.")
        return sqlite_connection

    except sqlite3.Error as error:
        logging.error("Error while connecting to sqlite.", error)

        if sqlite_connection is not None:
            sqlite_connection.close()
            logging.info("The SQLite connection is closed.")


def create_transactions_table(sqlite_connection):
    try:
        cursor = sqlite_connection.cursor()
        logging.info("Successfully Connected to SQLite.")

        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS transactions
                                    (id TEXT PRIMARY KEY, date DATE, expense_type TEXT, 
                                    amount BOOL, account_id TEXT)'''
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        logging.info("SQLite table created.")

        # Since the heaviest operation will be the breakdown, these indexes
        # should help with speed but they can still be improved
        sqlite_create_index_query = '''CREATE INDEX IF NOT EXISTS idx_user_daily
                                    ON transactions (account_id, date)'''
        cursor.execute(sqlite_create_index_query)
        sqlite_connection.commit()
        logging.info("SQLite index created.")

        cursor.close()

    except sqlite3.Error as error:
        logging.error("Error while creating a sqlite table.", error)

def insert_multipe_records(sqlite_connection, recordList):
    try:
        cursor = sqlite_connection.cursor()
        logging.info("Connected to SQLite")

        sqlite_insert_query = 'INSERT INTO transactions VALUES (?, ?, ?, ?, ?);'
        cursor.executemany(sqlite_insert_query, recordList)
        sqlite_connection.commit()
        cursor.close()
        logging.info("Total", cursor.rowcount, "Records inserted successfully into transactions table.")

    except sqlite3.Error as error:
        logging.error("Failed to insert multiple records into sqlite table.", error)

def get_transaction_breakdown(sqlite_connection, customer_id, start_date = None, end_date = None):
    try:
        argument_list = [customer_id]
        sqlite_query = '''SELECT account_id, expense_type, ROUND(SUM(amount),
                        2) AS breakdown, COUNT(id) AS sum FROM transactions t2
                        WHERE account_id = ? '''

        if isinstance(start_date, str):
            argument_list.append(start_date)
            sqlite_query = sqlite_query + 'AND  date >= ? '

        if isinstance(end_date, str):
            argument_list.append(end_date)
            sqlite_query = sqlite_query + 'AND  date <= ? '

        sqlite_query = sqlite_query + 'GROUP BY account_id, expense_type;'

        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_query, argument_list)
        rows = cursor.fetchall()
        cursor.close()

        return rows

    except sqlite3.Error as error:
        logging.error("Failed to fetch the account ID transaction breakdown.", error)
 
def delete_transaction(sqlite_connection, transaction_id):
    try:
        sqlite_query = '''DELETE from transactions where id = ?'''

        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_query, (transaction_id, ))
        sqlite_connection.commit()
        logging.info("Transaction deleted successfully")
        cursor.close()

    except sqlite3.Error as error:
        logging.error("Failed to delete record from the transactions table.", error)

def insert_transaction(sqlite_connection, account_id, date, expense_type, amount):
    try:
        record_id = str(uuid4())
        value_tuple = (record_id, date, account_id, expense_type, amount)
        sqlite_query = '''INSERT INTO transactions (id, date, account_id,
                        expense_type, amount) VALUES (?, ?, ?, ?, ?)'''

        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_query, value_tuple)
        sqlite_connection.commit()
        cursor.close()
        return record_id

    except sqlite3.Error as error:
        logging.error("Failed to insert transaction record.", error)
